"""The Base Scraper class. Designed to be inherited by other scraper classes."""

from abc import ABC, abstractmethod


class ScraperError(Exception):
    """An exception raised when an error occurs during scraping."""


class BaseScraper(ABC):
    """An abstract base class for web scrapers.

    Classes that inherit from this class
    must implement the run() method and ensure that it overwrites the html, price and
    title attributes.

    Attributes:
        PRICE_404 (str): A string to use when the price cannot be found.
        TITLE_404 (str): A string to use when the title cannot be found.
    """

    PRICE_404 = "Price not found"
    TITLE_404 = "Title not found"
    html: str | None = ""
    price = ""
    title = ""

    @abstractmethod
    def run(self) -> bool:
        """Download the HTML content of the page and scrape the data.

        Returns:
            bool: True if the data was scraped successfully, otherwise False.
        """
        raise NotImplementedError

    def _get_headers(self) -> dict[str, str]:
        """
        Get the HTTP headers to use when making requests.

        Returns:
            dict: The HTTP headers to use when making requests.
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }

    def get_html(self) -> str | None:
        """
        Get the HTML content of the page.

        Returns:
            str: The HTML content of the page.
        """
        return self.html

    def get_price(self) -> str:
        """
        Get the price of the product.

        Returns:
            str: The price of the product.
        """
        return self.price

    def get_title(self) -> str:
        """
        Get the title of the product.

        Returns:
            str: The title of the product.
        """
        return self.title
