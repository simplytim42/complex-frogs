import textdistance as td
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser, Node

from .base_scraper import BaseScraper, ScraperError


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

    def __init__(self, product_id: str):
        """
        Initializes a new instance of the AmazonGoogleScraper class.

        Args:
            product_id (str): The search query to use. Ideally this should be the
            product name as it appears on Amazon.
        """
        self.query = product_id
        url_query = product_id.replace(" ", "+")
        self.URL = f"https://www.google.com/search?q={url_query}&tbm=shop"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(product_id='{self.query}')"

    def __get_html_with_playwright(self) -> str:
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        context = browser.new_context(extra_http_headers=self.HEADERS)
        page = context.new_page()
        page.goto(self.URL)
        page.click(self.REJECT_COOKIES_SELECTOR)
        page.wait_for_load_state("networkidle")
        content = page.content()
        browser.close()
        pw.stop()
        return str(content)

    def run(self) -> bool:
        try:
            temp_html = HTMLParser(self.__get_html_with_playwright())
            self.html = temp_html.html

            product_cards = temp_html.css(self.PRODUCT_CARDS_SELECTOR)
            if not product_cards:
                raise AttributeError

            for product_card in product_cards:
                if product_card.select(self.PRODUCT_DETAILS_SELECTOR).any_text_contains(
                    "Amazon.co.uk",
                ) and self.__title_match(product_card):
                    # Found a likely match
                    self.price = product_card.css_first(self.PRICE_SELECTOR).text(
                        strip=True,
                    )
                    self.title = product_card.css_first(self.TITLE_SELECTOR).text(
                        strip=True,
                    )
                    return True
            return False
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            raise ScraperError(f"{self!r}: {e}") from e

    def __title_match(self, product_card: Node) -> bool:
        """Returns True if the scraped product title has over 50% similarity
        to the query value
        """
        title = product_card.css_first(self.TITLE_SELECTOR).text(strip=True)
        similarity: float = td.levenshtein.normalized_similarity(self.query, title)
        return similarity > 0.5
