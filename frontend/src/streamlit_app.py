# app.py
import streamlit as st
from PIL import Image
from io import BytesIO
import requests

from tools.logging_config import setup_logging, get_logger
from parsers.amazon_parser import AmazonParser

setup_logging()
logger = get_logger(__name__)

st.set_page_config(page_title="SKU Tagger from Amazon", layout="centered")

st.title("🛒 Amazon SKU Tagger AI")
st.write("Paste an Amazon product URL below. The app will extract product data and generate tags and a category.")

amazon_url = st.text_input("Enter Amazon Product URL")

if amazon_url:

    parser = AmazonParser()

    with st.spinner("Fetching product data..."):
        title, image_url = parser.extract_amazon_info(amazon_url)

    if title and image_url:
        st.subheader("📝 Extracted Title:")
        st.write(title)

        st.subheader("🖼️ Product Image:")
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        st.image(img, use_column_width=True)

        if st.button("Generate Tags"):
            # 🔁 Replace this with a real call to your model or API
            st.success("✅ Tags: eco, minimal, bamboo, lightweight")
            st.write("**Category:** Home > Kitchen > Cutlery")
            st.write("**Suggested Title:** 'Eco-Friendly Bamboo Utensil Set'")
    else:
        st.error("Could not extract product data. Please check the URL.")
