import pytest

from tools.scraper import GoOutdoorsScraper, ScraperException


@pytest.fixture
def mock_http_get_with_data(mocker):
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
def mock_http_get_no_data(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "<html></html>"
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def mock_http_get_no_html(mocker):
    mock_response = mocker.Mock()
    mock_response.text = 42
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value = mock_response
    return mock_get


@pytest.fixture
def scraper():
    return GoOutdoorsScraper("down-jacket-123456")


def test_init(scraper):
    expected_url = "https://www.gooutdoors.co.uk/123456/down-jacket-123456"
    assert scraper.SKU == "123456"
    assert expected_url == scraper.URL


def test_repr(scraper):
    # result of a repr method should be able to recreate the object
    result = repr(scraper)
    assert result == repr(eval(result))


def test_get_html(mock_http_get_with_data, scraper):
    # as we've added span tags to the html, we can check for them here instead of checking
    # for the whole html.
    scraper.run()
    assert "</span>" in scraper.get_html()


def test_get_html_no_html(mock_http_get_no_html, scraper):
    with pytest.raises(ScraperException):
        scraper.run()
        scraper.get_html()


def test_get_title(mock_http_get_with_data, scraper):
    result = scraper.run()
    assert result is True
    assert scraper.get_title() == "Down Jacket"


def test_get_title_no_title(mock_http_get_no_data, scraper):
    result = scraper.run()
    assert result is False
    assert scraper.get_title() == scraper.TITLE_404


def test_get_price(mock_http_get_with_data, scraper):
    result = scraper.run()
    assert result is True
    assert scraper.get_price() == "£100.00"


def test_get_price_no_price(mock_http_get_no_data, scraper):
    result = scraper.run()
    assert result is False
    assert scraper.get_price() == scraper.PRICE_404
