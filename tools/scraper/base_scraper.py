from abc import ABC, abstractmethod


class ScraperException(Exception):
    pass


class BaseScraper(ABC):
    """
    An abstract base class for web scrapers.

    Attributes:
        HEADERS (dict): A dictionary of HTTP headers to use when making requests.
        PRICE_404 (str): A string to use when the price cannot be found.
        TITLE_404 (str): A string to use when the title cannot be found.
    """

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    PRICE_404 = "Price not found"
    TITLE_404 = "Title not found"

    @abstractmethod
    def get_html(self) -> str:
        """
        Get the HTML content of the page.

        Returns:
            str: The HTML content of the page.
        """
        pass

    @abstractmethod
    def get_price(self) -> str:
        """
        Get the price of the product.

        Returns:
            str: The price of the product.
        """
        pass

    @abstractmethod
    def get_title(self) -> str:
        """
        Get the title of the product.

        Returns:
            str: The title of the product.
        """
        pass
