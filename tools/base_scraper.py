from abc import ABC, abstractmethod


class ScraperException(Exception):
    pass


class BaseScraper(ABC):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    PRICE_404 = "Price not found"
    TITLE_404 = "Title not found"

    @abstractmethod
    def get_html(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> str:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass
