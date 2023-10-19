from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException
import logging
import textdistance as td


class AmazonGoogleScraper(BaseScraper):
    PRICE_SELECTOR = "span.T14wmb"
    TITLE_SELECTOR = "h3.sh-np__product-title"
    REJECT_COOKIES_SELECTOR = "div.VfPpkd-RLmnJb"
    PRODUCT_CARDS_SELECTOR = "div.KZmu8e"
    PRODUCT_DETAILS_SELECTOR = "div.HUOptb"
    html = None
    node = None

    def __init__(self, query: str):
        self.query = query
        url_query = query.replace(" ", "+")
        self.URL = f"https://www.google.com/search?q={url_query}&tbm=shop"

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
                    self.node = node
                    break
        except Exception as e:
            logging.error(f"Error getting HTML: {e}")
            raise ScraperException("Failed to get HTML")
        finally:
            browser.close()
            pw.stop()

    def __title_match(self, node) -> bool:
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
            logging.warning(f"Error getting price: {e}")
            return self.PRICE_404

    def get_title(self) -> str:
        if not self.node:
            self.__retrieve_html()
        try:
            return self.node.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(f"Error getting title: {e}")
            return self.TITLE_404
