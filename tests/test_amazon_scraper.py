import pytest

from complex_frogs.scraper import AmazonScraper, ScraperError


@pytest.fixture()
def get_html_namespace():
    namespaces = [
        "complex_frogs",
        "scraper",
        "amazon_scraper",
        "AmazonScraper",
        "_AmazonScraper__get_html_with_playwright",
    ]
    return ".".join(namespaces)


@pytest.fixture()
def mock_http_get_with_data(mocker, get_html_namespace):
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = """
        <html>
            <span class="a-offscreen">£30.00</span>
            <span id="productTitle">Coding Book</span>
        </html>
        """
    return mock_get


@pytest.fixture()
def mock_http_get_no_data(mocker, get_html_namespace):
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = "<html></html>"
    return mock_get


@pytest.fixture()
def mock_http_get_no_html(mocker, get_html_namespace):
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = 42
    return mock_get


@pytest.fixture()
def scraper():
    return AmazonScraper("123456789")


def test_init(scraper):
    assert scraper.ASIN == "123456789"
    assert scraper.URL == "https://www.amazon.co.uk/dp/123456789"


def test_repr(scraper):
    result = repr(scraper)
    assert result == repr(eval(result))


def test_get_html(mock_http_get_with_data, scraper):
    # as we've added span tags to the html, we can check for them here instead of checking
    # for the whole html.
    scraper.run()
    assert "</span>" in scraper.get_html()


def test_get_html_no_html(mock_http_get_no_html, scraper):
    with pytest.raises(ScraperError):
        scraper.run()


def test_get_title(mock_http_get_with_data, scraper):
    result = scraper.run()
    assert result is True
    assert scraper.get_title() == "Coding Book"


def test_get_title_no_title(mock_http_get_no_data, scraper):
    result = scraper.run()
    assert result is False
    assert scraper.get_title() == scraper.TITLE_404


def test_get_price(mock_http_get_with_data, scraper):
    result = scraper.run()
    assert result is True
    assert scraper.get_price() == "£30.00"


def test_get_price_no_price(mock_http_get_no_data, scraper):
    result = scraper.run()
    assert result is False
    assert scraper.get_price() == scraper.PRICE_404
