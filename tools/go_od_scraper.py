import httpx
import logging
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException


class GoOutdoorsScraper(BaseScraper):
    """
    A scraper for retrieving product information from the Go Outdoors website.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        URL (str): The URL of the product page.
        SKU (str): The SKU of the product.
        html (HTMLParser): The parsed HTML content of the product page.
    """

    PRICE_SELECTOR = "span.regular-price"
    TITLE_SELECTOR = "span.product-name"
    URL = ""
    SKU = ""
    html = None

    def __init__(self, id: str):
        """
        Initializes a new instance of the GoOutdoorsScraper class.

        Args:
            id (str): The product ID in the format found in the URL.
            For example: "waterproof-down-jacket-123456".
        """
        self.SKU = id.split("-")[-1]
        self.URL = f"https://www.gooutdoors.co.uk/{self.SKU}/{id}"

    def __retrieve_html(self):
        try:
            response = httpx.get(self.URL, headers=self.HEADERS)
            response.raise_for_status()
            self.html = HTMLParser(response.text)
        except Exception as e:
            logging.error(
                f"Error getting HTML for '{__class__.__name__}' {self.SKU}: {e}"
            )
            raise ScraperException(
                f"Failed to get HTML for '{__class__.__name__}' {self.SKU}"
            )

    def get_html(self) -> str:
        if not self.html:
            self.__retrieve_html()
        return self.html.html

    def get_price(self) -> str:
        if not self.html:
            self.__retrieve_html()
        try:
            return self.html.css_first(self.PRICE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(
                f"Error getting price for '{__class__.__name__}' {self.SKU}: {e}"
            )
            return self.PRICE_404

    def get_title(self) -> str:
        if not self.html:
            self.__retrieve_html()
        try:
            return self.html.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(
                f"Error getting title for '{__class__.__name__}' {self.SKU}: {e}"
            )
            return self.TITLE_404
