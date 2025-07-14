from ai_sku_optimizer.models.product_optimizer import ProductOptimizer

__all__ = ["optimize_product"]

# Create a singleton-style lazy initializer
_optimizer_instance = None

def get_optimizer():
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = ProductOptimizer()
    return _optimizer_instance

def optimize_product(img_url, product_title, product_description):
    """
    Optimizes the product data using the ProductOptimizer model.

    Args:
        img_url (str): URL of the product image
        product_title (str): Raw product title
        product_description (str): Raw product description

    Returns:
        dict: Optimized output (SEO title, category, tags, price, etc.)
    """
    optimizer = get_optimizer()
    result = optimizer.optimize(img_url, product_title, product_description)

    return result["seo_title"], result["category"], result["tags"], result["price_range_eur"]
