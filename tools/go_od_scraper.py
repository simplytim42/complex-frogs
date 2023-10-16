import httpx
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper


class GoOutdoorsScraper(BaseScraper):
    html = None

    def __init__(self, id: str):
        sku = id.split("-")[-1]
        self.url = f"https://www.gooutdoors.co.uk/{sku}/{id}"

    def __get_html(self):
        response = httpx.get(self.url, headers=self.headers)
        response.raise_for_status()
        self.html = HTMLParser(response.text)

    def get_price(self) -> str:
        if not self.html:
            self.__get_html()
        return self.html.css_first("span.regular-price").text(strip=True)

    def get_title(self) -> str:
        if not self.html:
            self.__get_html()
        return self.html.css_first("span.product-name").text(strip=True)
