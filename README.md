# 🛍️ Amazon SEO Description Generator

This is a demo app that allows users to paste an Amazon product URL and receive an SEO-optimized product description based on the product title and features.

---

## 🚀 Features

- 🧠 Extracts product title and bullet points from any Amazon product page
- 📄 Generates an SEO-friendly description from the extracted content
- ⚡ Fast, cached scraping to reduce duplicate requests
- 🖥️ Simple UI powered by [Streamlit](https://streamlit.io)

---

## 🏗️ How It Works

1. The user pastes an Amazon product URL into the Streamlit app
2. The app scrapes the page (once) and caches the HTML content
3. It extracts key elements like title and bullet points using BeautifulSoup
4. It generates an SEO-ready product description via a prompt
5. Optionally, the prompt can be sent to an LLM (e.g., OpenAI GPT-4)

---

## 📦 Requirements

- Python 3.8+
- pip

---

## 🧰 Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/t.dimartino/ai-sku-optimizer
cd ai-sku-optimizer

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Run the App Locally

`streamlit run streamlit_app.py`

Then open your browser to http://localhost:8501
