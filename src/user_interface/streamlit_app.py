# streamlit_app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from PIL import Image
from io import BytesIO
import requests

from ai_sku_optimizer.tools.logging_config import setup_logging, get_logger
from ai_sku_optimizer.parsers.amazon_parser import AmazonParser
from ai_sku_optimizer.models import optimize_product

setup_logging()
logger = get_logger(__name__)

st.set_page_config(page_title="SKU Tagger from Amazon", layout="centered")

st.title("🛒 Amazon SKU Tagger AI")
st.write("Paste an Amazon product URL below. The app will extract product data and generate tags and a category.")

amazon_url = st.text_input("Enter Amazon Product URL")

if amazon_url:

    parser = AmazonParser()

    with st.spinner("Fetching product data..."):
        title, description, image_url = parser.extract_amazon_info(amazon_url)

    if title and description and image_url:
        st.subheader("📝 Extracted Title:")
        st.write(title)

        st.subheader("🖼️ Product Image:")
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        st.image(img, use_container_width=True)

        st.subheader("📝 Extracted Description:")
        with st.expander(""):
            st.write(description)

        if st.button("Optimize !"):
            with st.spinner("🔎 Optimizing product..."):
                seo_title, category, tags, price_range_eur = optimize_product(
                    img_url=image_url,
                    product_title=title,
                    product_description=description
                )

            st.success("✅ Product optimized!")
            with st.expander("📦 View Results"):
                st.write(f"**SEO Title:** '{seo_title}'")
                st.write(f"**Category:** '{category}'")
                st.write(f"**Tags:** '{', '.join(tags)}'")
                st.write(f"**price_range_eur:** '{price_range_eur}'")
    else:
        st.error("Could not extract product data. Please check the URL.")
