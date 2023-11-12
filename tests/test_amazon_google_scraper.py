from tools.scraper.amazon_google_scraper import AmazonGoogleScraper
from selectolax.parser import HTMLParser
import pytest


@pytest.fixture
def scraper_with_data():
    """returns a AmazonGoogleScraper instance with a mocked HTMLParser instance."""

    scraper = AmazonGoogleScraper("a fake product title")
    scraper.retrieved_html = True
    scraper.retrieved_node = True
    # uses css_first to return a "Node" instance
    scraper.node = HTMLParser(
        """
        <html>
            <span class="T14wmb">£100.00</span>
            <h3 class="sh-np__product-title">Fake</h3>
        </html>
        """
    ).css_first("html")
    return scraper


@pytest.fixture
def scraper_no_data():
    """returns a AmazonGoogleScraper instance with a mocked HTMLParser instance that
    simulates having no valid data."""

    scraper = AmazonGoogleScraper("a fake product title")
    scraper.retrieved_html = True
    scraper.retrieved_node = True
    # uses css_first to return a "Node" instance
    scraper.node = HTMLParser("<html></html>").css_first("html")
    return scraper


def test_init(scraper_with_data):
    expected_url = "https://www.google.com/search?q=a+fake+product+title&tbm=shop"
    assert scraper_with_data.query == "a fake product title"
    assert scraper_with_data.URL == expected_url


def test_repr(scraper_with_data):
    assert repr(scraper_with_data) == "AmazonGoogleScraper(id='a fake product title')"


def test_get_title(scraper_with_data):
    assert scraper_with_data.get_title() == "Fake"


def test_get_title_no_title(scraper_no_data):
    assert scraper_no_data.get_title() == scraper_no_data.TITLE_404


def test_get_price(scraper_with_data):
    assert scraper_with_data.get_price() == "£100.00"


def test_get_price_no_price(scraper_no_data):
    assert scraper_no_data.get_price() == scraper_no_data.PRICE_404
