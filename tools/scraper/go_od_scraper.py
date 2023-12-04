import httpx
from selectolax.parser import HTMLParser

from .base_scraper import BaseScraper, ScraperError


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

    def __init__(self, product_id: str):
        """
        Initializes a new instance of the GoOutdoorsScraper class.

        Args:
            product_id (str): The product ID in the format found in the URL.
            For example: "waterproof-down-jacket-123456".
        """
        self.SKU = product_id.split("-")[-1]
        self.URL = f"https://www.gooutdoors.co.uk/{self.SKU}/{product_id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(product_id='{self.SKU}')"

    def run(self) -> bool:
        try:
            response = httpx.get(self.URL, headers=self.HEADERS)
            response.raise_for_status()
            temp_html = HTMLParser(response.text)

            self.html = temp_html.html
            self.price = temp_html.css_first(self.PRICE_SELECTOR).text(strip=True)
            self.title = temp_html.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            msg = f"{self!r}: {e}"
            raise ScraperError(msg) from e
        else:
            return True
