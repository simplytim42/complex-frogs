from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException
import logging


class AmazonScraper(BaseScraper):
    """
    A scraper for retrieving product information from the Amazon UK website.

    This implementation is not always reliable.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        URL (str): The URL of the product page.
        html (HTMLParser): The parsed HTML content of the product page.
    """

    PRICE_SELECTOR = "span.a-offscreen"
    TITLE_SELECTOR = "span#productTitle"
    URL = ""
    html = None

    def __init__(self, asin: str):
        """
        Initializes a new instance of the AmazonScraper class.

        Args:
            asin (str): The Amazon Standard Identification Number (ASIN) of the product to scrape.
        """
        self.URL = f"https://www.amazon.co.uk/dp/{asin}"

    def __retrieve_html(self):
        try:
            pw = sync_playwright().start()
            browser = pw.chromium.launch()
            context = browser.new_context(extra_http_headers=self.HEADERS)
            page = context.new_page()
            page.goto(self.URL)
            self.html = HTMLParser(page.content())
        except Exception as e:
            logging.error(f"Error getting HTML: {e}")
            raise ScraperException("Failed to get HTML")
        finally:
            browser.close()
            pw.stop()

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
            logging.warning(f"Error getting price: {e}")
            return self.PRICE_404

    def get_title(self) -> str:
        if not self.html:
            self.__retrieve_html()
        try:
            return self.html.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(f"Error getting title: {e}")
            return self.TITLE_404
