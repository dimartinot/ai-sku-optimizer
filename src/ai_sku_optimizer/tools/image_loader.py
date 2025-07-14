import requests
from PIL import Image
from io import BytesIO

def load_image_from_url(img_url):
    response = requests.get(img_url, timeout=10)
    response.raise_for_status()  # optional: raises error if request failed
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image