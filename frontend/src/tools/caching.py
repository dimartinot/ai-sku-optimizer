import diskcache
from urllib.parse import urlparse, urlunparse

class CachingClient:
    """
    A caching client that fetches a product data from the cache if available.
    """

    def __init__(self, cache_name='amazon_cache'):
        self.cache_obj = diskcache.Cache(cache_name)

    def get_product(self, url):
        """
        Retrieves the product data from the cache using the URL as the key.
        """
        url = self._clean_url(url)  # Clean the URL to avoid cache misses due to query params or fragments
        if url in self.cache_obj:
            return self.cache_obj[url]
        else:
            return None
        
    def cache(self, url, data):
        """
        Caches the product data with the URL as the key.
        """
        url = self._clean_url(url)  # Clean the URL to avoid cache misses due to query params or fragments
        self.cache_obj[url] = data

    def _clean_url(self, url):
        parsed = urlparse(url)
        cleaned = parsed._replace(query="", fragment="")
        return urlunparse(cleaned)