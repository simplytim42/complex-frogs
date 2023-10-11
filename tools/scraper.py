import httpx
from selectolax.parser import HTMLParser


class Scraper:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    def __init__(self, url: str):
        self.url = url

    def get_value(self, css_selector: str) -> str:
        response = httpx.get(self.url, headers=self.headers)
        html = HTMLParser(response.text)
        return html.css_first(css_selector).text()
