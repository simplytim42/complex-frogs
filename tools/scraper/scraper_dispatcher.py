from .amazon_scraper import AmazonScraper
from .go_od_scraper import GoOutdoorsScraper
from .amazon_google_scraper import AmazonGoogleScraper
from .base_scraper import BaseScraper
from typing import Literal


def get_scraper(site: Literal["amz", "amz-g", "go_od"], product_id: str) -> BaseScraper:
    """
    Returns a scraper instance for the specified site and product ID.

    Args:
        site (str): The site to scrape. Must be one of "amz", "amz-g", or "go_od".
        product_id (str): The ID of the product to scrape in the format required for the site chosen.

    Returns:
        BaseScraper: A scraper instance for the specified site and product ID.
    """

    if site == "amz-g":
        return AmazonGoogleScraper(product_id)
    if site == "go_od":
        return GoOutdoorsScraper(product_id)

    # Default to Amazon
    return AmazonScraper(product_id)
