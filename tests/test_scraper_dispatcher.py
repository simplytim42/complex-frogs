from tools.scraper.scraper_dispatcher import get_scraper
from tools.scraper.amazon_scraper import AmazonScraper
from tools.scraper.go_od_scraper import GoOutdoorsScraper
from tools.scraper.amazon_google_scraper import AmazonGoogleScraper
import pytest


@pytest.mark.parametrize(
    "key, instance",
    [
        ("amz", AmazonScraper),
        ("amz-g", AmazonGoogleScraper),
        ("go_od", GoOutdoorsScraper),
    ],
)
def test_get_scraper(key, instance):
    assert isinstance(get_scraper(key, "test"), instance)


def test_get_scraper_incorrect_site():
    with pytest.raises(Exception):
        get_scraper("invalid", "test")
