from tools.scraper import (
    get_scraper,
    InvalidSiteException,
    AmazonScraper,
    GoOutdoorsScraper,
    AmazonGoogleScraper,
)
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
    with pytest.raises(InvalidSiteException):
        get_scraper("invalid", "test")
