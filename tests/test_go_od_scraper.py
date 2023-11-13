from tools.scraper.go_od_scraper import GoOutdoorsScraper
from tools.scraper.base_scraper import ScraperException
import pytest


@pytest.fixture
def mock_http_get_with_data(mocker):  # type: ignore
    mock_response = mocker.Mock()
    mock_response.text = """
        <html>
            <span class="regular-price">£100.00</span>
            <span class="product-name">Down Jacket</span>
        </html>
        """
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def mock_http_get_no_data(mocker):  # type: ignore
    mock_response = mocker.Mock()
    mock_response.text = "<html></html>"
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def mock_http_get_no_html(mocker):  # type: ignore
    mock_response = mocker.Mock()
    mock_response.text = 42
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def scraper():  # type: ignore
    return GoOutdoorsScraper("down-jacket-123456")


def test_init(scraper):  # type: ignore
    expected_url = "https://www.gooutdoors.co.uk/123456/down-jacket-123456"
    assert scraper.SKU == "123456"
    assert scraper.URL == expected_url


def test_repr(scraper):  # type: ignore
    # result of a repr method should be able to recreate the object
    result = repr(scraper)
    assert result == repr(eval(result))


def test_get_html(mock_http_get_with_data, scraper):  # type: ignore
    # as we've added span tags to the html, we can check for them here instead of checking
    # for the whole html.
    assert "</span>" in scraper.get_html()


def test_get_html_no_html(mock_http_get_no_html, scraper):  # type: ignore
    with pytest.raises(ScraperException):
        scraper.get_html()


def test_get_title(mock_http_get_with_data, scraper):  # type: ignore
    assert scraper.get_title() == "Down Jacket"


def test_get_title_no_title(mock_http_get_no_data, scraper):  # type: ignore
    assert scraper.get_title() == scraper.TITLE_404


def test_get_price(mock_http_get_with_data, scraper):  # type: ignore
    assert scraper.get_price() == "£100.00"


def test_get_price_no_price(mock_http_get_no_data, scraper):  # type: ignore
    assert scraper.get_price() == scraper.PRICE_404
