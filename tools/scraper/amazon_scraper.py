from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

from .base_scraper import BaseScraper, ScraperException


class AmazonScraper(BaseScraper):
    """
    A scraper for retrieving product information from the Amazon UK website.

    This implementation is not always reliable.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        URL (str): The URL of the product page.
        ASIN (str): The Amazon Standard Identification Number (ASIN) of the product.
        html (HTMLParser): The parsed HTML content of the product page.
    """

    PRICE_SELECTOR = "span.a-offscreen"
    TITLE_SELECTOR = "span#productTitle"
    URL = ""
    ASIN = ""

    def __init__(self, id: str):
        """
        Initializes a new instance of the AmazonScraper class.

        Args:
            id (str): The Amazon Standard Identification Number (ASIN) of the product to scrape.
        """
        self.ASIN = id
        self.URL = f"https://www.amazon.co.uk/dp/{id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.ASIN}')"

    def __get_html_with_playwright(self) -> str:
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        context = browser.new_context(extra_http_headers=self.HEADERS)
        page = context.new_page()
        page.goto(self.URL)
        content = page.content()
        browser.close()
        pw.stop()
        return str(content)

    def run(self) -> bool:
        try:
            temp_html = HTMLParser(self.__get_html_with_playwright())
            self.html = temp_html.html
            self.price = temp_html.css_first(self.PRICE_SELECTOR).text(strip=True)
            self.title = temp_html.css_first(self.TITLE_SELECTOR).text(strip=True)
            return True
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            raise ScraperException(f"{self!r}: {e}") from e
