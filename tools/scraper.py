import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url: str):
        self.url = url

    def get_value(self, css_selector: str) -> str:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.css.select(css_selector)[0].string.strip()
