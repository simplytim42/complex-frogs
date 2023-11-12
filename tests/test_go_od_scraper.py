from tools.scraper.go_od_scraper import GoOutdoorsScraper
from selectolax.parser import HTMLParser
import pytest


@pytest.fixture
def scraper_with_data():
    """returns a GoOutdoorsScraper instance with a mocked HTMLParser instance."""

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


@pytest.fixture
def scraper_no_data():
    """returns a GoOutdoorsScraper instance with a mocked HTMLParser instance without
    any data."""

    scraper = GoOutdoorsScraper("down-jacket-123456")
    scraper.retrieved_html = True
    scraper.html = HTMLParser("<html></html>")
    return scraper


def test_init(scraper_with_data):
    expected_url = "https://www.gooutdoors.co.uk/123456/down-jacket-123456"
    assert scraper_with_data.SKU == "123456"
    assert scraper_with_data.URL == expected_url


def test_repr(scraper_with_data):
    assert repr(scraper_with_data) == "GoOutdoorsScraper(id='123456')"


def test_get_html(scraper_with_data):
    # as we've added span tags to the html, we can check for them here instead of checking
    # for the whole html.
    assert "</span>" in scraper_with_data.get_html()


def test_get_title(scraper_with_data):
    assert scraper_with_data.get_title() == "Down Jacket"


def test_get_title_no_title(scraper_no_data):
    assert scraper_no_data.get_title() == scraper_no_data.TITLE_404


def test_get_price(scraper_with_data):
    assert scraper_with_data.get_price() == "£100.00"


def test_get_price_no_price(scraper_no_data):
    assert scraper_no_data.get_price() == scraper_no_data.PRICE_404
