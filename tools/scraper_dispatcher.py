from .amazon_scraper import AmazonScraper
from .go_od_scraper import GoOutdoorsScraper


def get_scraper(site: str, product_id: str):
    if site not in ["amz", "go_od"]:
        raise ValueError(f"Invalid site: {site}")

    if site == "amz":
        return AmazonScraper(product_id)
    if site == "go_od":
        return GoOutdoorsScraper(product_id)
