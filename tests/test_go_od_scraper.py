from tools.scraper.go_od_scraper import GoOutdoorsScraper
from selectolax.parser import HTMLParser
import pytest


@pytest.fixture
def scraper():
    scraper = GoOutdoorsScraper("down-jacket-123456")
    scraper.html = HTMLParser(
        """
        <html>
            <span class="regular-price">£100.00</span>
            <span class="product-name">Down Jacket</span>
        </html>
        """
    )
    return scraper


class TestGoOutdoorsScraper:
    def test_init(self, scraper):
        assert scraper.SKU == "123456"
        assert scraper.URL == "https://www.gooutdoors.co.uk/123456/down-jacket-123456"

    def test_get_title(self, scraper):
        assert scraper.get_title() == "Down Jacket"

    def test_get_title_no_title(self, scraper):
        scraper.html = HTMLParser("<html></html>")
        assert scraper.get_title() == scraper.TITLE_404

    def test_get_price(self, scraper):
        assert scraper.get_price() == "£100.00"

    def test_get_price_no_price(self, scraper):
        scraper.html = HTMLParser("<html></html>")
        assert scraper.get_price() == scraper.PRICE_404
