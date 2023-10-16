from abc import ABC, abstractmethod


class BaseScraper(ABC):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    @abstractmethod
    def get_price(self) -> str:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass
