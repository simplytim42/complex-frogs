from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException


class AmazonScraper(BaseScraper):
    html = None

    def __init__(self, asin: str):
        self.asin = asin

    def __get_html(self):
        try:
            pw = sync_playwright().start()
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"https://www.amazon.co.uk/dp/{self.asin}")
            self.html = HTMLParser(page.content())
        except Exception as e:
            print(e)
            raise ScraperException("Failed to get HTML")
        finally:
            browser.close()
            pw.stop()

    def get_price(self) -> str:
        if not self.html:
            self.__get_html()
        try:
            return self.html.css_first("span.a-offscreen").text(strip=True)
        except AttributeError as e:
            print(e)
            return "Price not found"

    def get_title(self) -> str:
        if not self.html:
            self.__get_html()
        try:
            return self.html.css_first("span#productTitle").text(strip=True)
        except AttributeError as e:
            print(e)
            return "Title not found"
