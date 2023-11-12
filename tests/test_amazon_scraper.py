from tools.scraper.amazon_scraper import AmazonScraper
from selectolax.parser import HTMLParser
import pytest


@pytest.fixture
def scraper_with_data():
    """returns a AmazonScraper instance with a mocked HTMLParser instance."""

    scraper = AmazonScraper("123456789")
    scraper.retrieved_html = True
    scraper.html = HTMLParser(
        """
        <html>
            <span class="a-offscreen">£100.00</span>
            <span id="productTitle">Fake</span>
        </html>
        """
    )
    return scraper


@pytest.fixture
def scraper_no_data():
    """returns a AmazonScraper instance with a mocked HTMLParser instance containing
    no data."""

    scraper = AmazonScraper("123456789")
    scraper.retrieved_html = True
    scraper.html = HTMLParser("<html></html>")
    return scraper


def test_init(scraper_with_data):
    assert scraper_with_data.ASIN == "123456789"
    assert scraper_with_data.URL == "https://www.amazon.co.uk/dp/123456789"


def test_repr(scraper_with_data):
    assert repr(scraper_with_data) == "AmazonScraper(id='123456789')"


def test_get_html(scraper_with_data):
    # as we've added span tags to the html, we can check for them here instead of checking
    # for the whole html.
    assert "</span>" in scraper_with_data.get_html()


def test_get_title(scraper_with_data):
    assert scraper_with_data.get_title() == "Fake"


def test_get_title_no_title(scraper_no_data):
    assert scraper_no_data.get_title() == scraper_no_data.TITLE_404


def test_get_price(scraper_with_data):
    assert scraper_with_data.get_price() == "£100.00"


def test_get_price_no_price(scraper_no_data):
    assert scraper_no_data.get_price() == scraper_no_data.PRICE_404
