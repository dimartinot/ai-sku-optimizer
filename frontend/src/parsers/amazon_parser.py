import requests
from bs4 import BeautifulSoup

from tools.logging_config import get_logger, setup_logging
from tools.caching import CachingClient


setup_logging()
logger = get_logger(__name__)

class AmazonParser:
    """
    Parser for Amazon product pages.
    """

    def __init__(self) -> None:
        self.session = None
        self.caching_client = CachingClient(cache_name='amazon_cache')

    @staticmethod
    def get_headers() -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

    def get_session(self):
        self.session = requests.Session() if not self.session else self.session
        headers = self.get_headers()
        self.session.headers.update(headers)
        return self.session

    def fetch_product_data(self, url):
        """
        Fetches the HTML content of the Amazon product page.
        """
        session = self.get_session()
        res = session.get(url, timeout=10)
        return res

    def get_title_and_image(self, html_content):
        """
        Extracts the product title and image URL from the HTML content.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.find(id="productTitle").get_text(strip=True)

        img_tag = soup.find("img", {"id": "landingImage"})
        image_url = img_tag["src"] if img_tag else None

        return title, image_url

    def extract_amazon_info(self, url):
        """
        Extracts product title and image URL from an Amazon product page.
        """
        try:
            logger.info(f"Fetching Amazon product data from URL: {url}")

            from_cache = self.caching_client.get_product(url)

            if from_cache is None:
                res = self.fetch_product_data(url).text
                self.caching_client.cache(url, res)
            else:
                res = from_cache
            
            logger.info(f"URL successfully loaded. Now parsing HTML content.")

            title, image_url = self.get_title_and_image(res)            

            return title, image_url

        except Exception as e:
            logger.warning(f"Error extracting Amazon product info: {e}")
            return None, None