from tools.scraper.go_od_scraper import GoOutdoorsScraper
from selectolax.parser import HTMLParser
import pytest


@pytest.fixture
def scraper():  # type: ignore
    """returns a GoOutdoorsScraper instance with a mocked HTMLParser instance.
    This stops the scraper from making an http request."""

    scraper = GoOutdoorsScraper("down-jacket-123456")
    scraper.retrieved_html = True
    scraper.html = HTMLParser(
        """
        <html>
            <span class="regular-price">£100.00</span>
            <span class="product-name">Down Jacket</span>
        </html>
        """
    )
    return scraper


def test_init(scraper):  # type: ignore
    assert scraper.SKU == "123456"
    assert scraper.URL == "https://www.gooutdoors.co.uk/123456/down-jacket-123456"


def test_get_title(scraper):  # type: ignore
    assert scraper.get_title() == "Down Jacket"


def test_get_title_no_title(scraper):  # type: ignore
    scraper.html = HTMLParser("<html></html>")
    assert scraper.get_title() == scraper.TITLE_404


def test_get_price(scraper):  # type: ignore
    assert scraper.get_price() == "£100.00"


def test_get_price_no_price(scraper):  # type: ignore
    scraper.html = HTMLParser("<html></html>")
    assert scraper.get_price() == scraper.PRICE_404
