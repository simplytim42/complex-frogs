from tools.scraper.amazon_google_scraper import AmazonGoogleScraper
from tools.scraper.base_scraper import ScraperException
import pytest


@pytest.fixture
def get_html_namespace():  # type: ignore
    namespaces = [
        "tools",
        "scraper",
        "amazon_google_scraper",
        "AmazonGoogleScraper",
        "_AmazonGoogleScraper__get_html_with_playwright",
    ]
    return ".".join(namespaces)


@pytest.fixture
def mock_http_get_with_data(mocker, get_html_namespace):  # type: ignore
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = """
        <html>
            <div class="KZmu8e">
                <div class="HUOptb">Amazon.co.uk/fake</div>
                <h3 class=sh-np__product-title>Coding Book</h3>
                <span class="T14wmb">£30.00</span>
            </div>
        </html>
        """
    return mock_get


@pytest.fixture
def mock_http_get_no_data(mocker, get_html_namespace):  # type: ignore
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = "<html></html>"
    return mock_get


@pytest.fixture
def mock_http_get_no_html(mocker, get_html_namespace):  # type: ignore
    mock_get = mocker.patch(get_html_namespace)
    mock_get.return_value = 42
    return mock_get


@pytest.fixture
def scraper():  # type: ignore
    return AmazonGoogleScraper("Coding Book")


def test_init(scraper):  # type: ignore
    expected_url = "https://www.google.com/search?q=Coding+Book&tbm=shop"
    assert scraper.query == "Coding Book"
    assert scraper.URL == expected_url


def test_repr(scraper):  # type: ignore
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
    assert scraper.get_title() == "Coding Book"


def test_get_title_no_title(mock_http_get_no_data, scraper):  # type: ignore
    assert scraper.get_title() == scraper.TITLE_404


def test_get_price(mock_http_get_with_data, scraper):  # type: ignore
    assert scraper.get_price() == "£30.00"


def test_get_price_no_price(mock_http_get_no_data, scraper):  # type: ignore
    assert scraper.get_price() == scraper.PRICE_404
