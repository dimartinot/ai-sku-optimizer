from transformers import BlipProcessor, BlipForConditionalGeneration, AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os
import re
import json
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

from huggingface_hub import login
login(os.getenv("HF_TOKEN"))

from ai_sku_optimizer.tools.logging_config import setup_logging, get_logger
from ai_sku_optimizer.tools.image_loader import load_image_from_url

setup_logging()
logger = get_logger(__name__)

class ProductOptimizer:

    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.pipe = pipe = pipeline("text-generation", model=model_id, torch_dtype=torch.bfloat16, device_map="auto")

    
    def _build_prompt(self, caption, product_title, product_description):
        return f"""Given the product title, description, and image caption below, return only a JSON object with the following fields:
        - seo_title: an SEO-optimized product title
        - category: a string representing the product category
        - tags: a list of 5–10 relevant search tags
        - price_range_eur: a string representing the estimated price range in euros

        Product data:
        - Title: "{product_title}"
        - Description: "{product_description}"
        - Image Captioning: "{caption}"

        If specs are contradictory between image captioning and product title/description, 
        prioritize the image title/description, they are scraped, while captioning is generated.

        DO NOT include any explanation or formatting. DO NOT use markdown or code blocks.

        Example format (no extra text, just valid JSON):

        {{
        "seo_title": "...",
        "category": "...",
        "tags": [...],
        "price_range_eur": "..."
        }}
        
        Now respond with JSON only.
        """
    
    def _extract_json_from_text(self, text):
        # Match the first {...} block (non-greedy to avoid overshooting)
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None

    def _get_product_caption(self, img_url) -> str:
        raw_image = load_image_from_url(img_url)
        inputs = self.processor(raw_image, return_tensors="pt")
        output = self.blip_model.generate(**inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption
    
    def _prompt(self, prompt, temperature=0.7, max_new_tokens=512) -> dict:

        # Format as chat-style prompt
        messages = [
            {
                "role": "system",
                "content": "You are an e-commerce content assistant.",
            },
            {"role": "user", "content": prompt.strip()},
        ]

        logger.info(f"Launching tokenizer")
        prompt = self.pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        logger.info(f"Inputs for LLM: {prompt}")
        outputs = self.pipe(
            prompt, 
            max_new_tokens=max_new_tokens, 
            do_sample=True, 
            temperature=temperature, 
            top_k=50, 
            top_p=0.95
        )

        logger.info(f"Outputs of LLM: {outputs}")
        full_text = outputs[0]["generated_text"]
        # 🔍 Extract only the part after the assistant tag
        split_token = "<|assistant|>"
        if split_token in full_text:
            response = full_text.split(split_token)[-1].strip()
        else:
            response = full_text[len(prompt):].strip()  # fallback if template changes

        logger.info(f"Decoded output of LLM: {response}")
        return response

    def optimize(self, img_url, product_title, product_description):
        caption = self._get_product_caption(img_url)
        logger.info(f"Caption generated: {caption}")
        prompt = self._build_prompt(caption, product_title, product_description)
        logger.info(f"Prompt for LLM: {prompt}")
        
        response = self._prompt(prompt)
        response = self._extract_json_from_text(response)
        logger.info(f"Response from LLM: {response}")

        return response