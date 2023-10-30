from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException
import logging
import textdistance as td


class AmazonGoogleScraper(BaseScraper):
    """
    A scraper for retrieving Amazon UK product information from the Google Shopping search results page.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        REJECT_COOKIES_SELECTOR (str): The CSS selector for the reject cookies button element.
        PRODUCT_CARDS_SELECTOR (str): The CSS selector for the product card elements.
        PRODUCT_DETAILS_SELECTOR (str): The CSS selector for the product details element.
        html (HTMLParser): The parsed HTML content of the search results page.
        node (SelectolaxNode): The current product card node being processed.
    """

    PRICE_SELECTOR = "span.T14wmb"
    TITLE_SELECTOR = "h3.sh-np__product-title"
    REJECT_COOKIES_SELECTOR = "div.VfPpkd-RLmnJb"
    PRODUCT_CARDS_SELECTOR = "div.KZmu8e"
    PRODUCT_DETAILS_SELECTOR = "div.HUOptb"
    html = None
    node = None

    def __init__(self, id: str):
        """
        Initializes a new instance of the AmazonGoogleScraper class.

        Args:
            id (str): The search query to use. Ideally this should be the
            product name as it appears on Amazon.
        """
        self.query = id
        url_query = id.replace(" ", "+")
        self.URL = f"https://www.google.com/search?q={url_query}&tbm=shop"

    def __repr__(self):
        return f"{__class__.__name__}(query='{self.query}')"

    def __retrieve_html(self):
        try:
            pw = sync_playwright().start()
            browser = pw.chromium.launch()
            context = browser.new_context(extra_http_headers=self.HEADERS)
            page = context.new_page()
            page.goto(self.URL)
            page.click(self.REJECT_COOKIES_SELECTOR)
            page.wait_for_load_state("networkidle")
            self.html = HTMLParser(page.content())

            nodes = self.html.css(self.PRODUCT_CARDS_SELECTOR)
            for node in nodes:
                if node.select(self.PRODUCT_DETAILS_SELECTOR).any_text_contains(
                    "Amazon.co.uk"
                ) and self.__title_match(node):
                    # Found a likely match
                    self.node = node
                    break
        except Exception as e:
            logging.error(
                f"Error getting HTML for '{__class__.__name__}' {self.query}: {e}"
            )
            raise ScraperException(
                f"Failed to get HTML for '{__class__.__name__}' {self.query}"
            )
        finally:
            browser.close()
            pw.stop()

    def __title_match(self, node) -> bool:
        """Returns True if the scraped product title has over 50% similarity
        to the query value
        """
        title = node.css_first(self.TITLE_SELECTOR).text(strip=True)
        similarity = td.levenshtein.normalized_similarity(self.query, title)
        return similarity > 0.5

    def get_html(self) -> str:
        if not self.html:
            self.__retrieve_html()
        return self.html.html

    def get_price(self) -> str:
        if not self.node:
            self.__retrieve_html()
        try:
            return self.node.css_first(self.PRICE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(
                f"Error getting price for '{__class__.__name__}' {self.query}: {e}"
            )
            return self.PRICE_404

    def get_title(self) -> str:
        if not self.node:
            self.__retrieve_html()
        try:
            return self.node.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(
                f"Error getting title for '{__class__.__name__}' {self.query}: {e}"
            )
            return self.TITLE_404
