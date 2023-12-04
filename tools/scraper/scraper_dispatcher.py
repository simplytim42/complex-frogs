from .amazon_google_scraper import AmazonGoogleScraper
from .amazon_scraper import AmazonScraper
from .base_scraper import BaseScraper
from .go_od_scraper import GoOutdoorsScraper


class InvalidSiteError(Exception):
    pass


def get_scraper(site: str, product_id: str) -> BaseScraper:
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
    if site == "amz":
        return AmazonScraper(product_id)

    msg = f"Invalid site: {site}"
    raise InvalidSiteError(msg)
