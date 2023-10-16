from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper


class AmazonScraper(BaseScraper):
    html = None

    def __init__(self, asin: str):
        self.asin = asin

    def __get_html(self):
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(f"https://www.amazon.co.uk/dp/{self.asin}")
        self.html = HTMLParser(page.content())
        browser.close()
        pw.stop()

    def get_price(self) -> str:
        if not self.html:
            self.__get_html()
        return self.html.css_first("span.a-offscreen").text(strip=True)

    def get_title(self) -> str:
        if not self.html:
            self.__get_html()
        return self.html.css_first("span#productTitle").text(strip=True)
