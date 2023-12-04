import pytest

from tools.scraper import (
    AmazonGoogleScraper,
    AmazonScraper,
    GoOutdoorsScraper,
    InvalidSiteError,
    get_scraper,
)


@pytest.mark.parametrize(
    ("key", "instance"),
    [
        ("amz", AmazonScraper),
        ("amz-g", AmazonGoogleScraper),
        ("go_od", GoOutdoorsScraper),
    ],
)
def test_get_scraper(key, instance):
    assert isinstance(get_scraper(key, "test"), instance)


def test_get_scraper_incorrect_site():
    with pytest.raises(InvalidSiteError):
        get_scraper("invalid", "test")
