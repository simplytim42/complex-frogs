from abc import ABC, abstractmethod
import httpx
from selectolax.parser import HTMLParser, Node
from playwright.sync_api import sync_playwright
import textdistance as td


class ScraperException(Exception):
    pass


class BaseScraper(ABC):
    """
    An abstract base class for web scrapers. Classes that inherit from this class
    must implement the run() method and ensure that it overwrites the html, price and
    title attributes.

    Attributes:
        HEADERS (dict): A dictionary of HTTP headers to use when making requests.
        PRICE_404 (str): A string to use when the price cannot be found.
        TITLE_404 (str): A string to use when the title cannot be found.
    """

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    PRICE_404 = "Price not found"
    TITLE_404 = "Title not found"
    html: str | None = ""
    price = ""
    title = ""

    @abstractmethod
    def run(self) -> bool:
        """
        Download the HTML content of the page and scrape the data"

        Returns:
            bool: True if the data was scraped successfully, otherwise False.
        """
        pass  # pragma: no cover

    def get_html(self) -> str | None:
        """
        Get the HTML content of the page.

        Returns:
            str: The HTML content of the page.
        """
        return self.html

    def get_price(self) -> str:
        """
        Get the price of the product.

        Returns:
            str: The price of the product.
        """
        return self.price

    def get_title(self) -> str:
        """
        Get the title of the product.

        Returns:
            str: The title of the product.
        """
        return self.title


class GoOutdoorsScraper(BaseScraper):
    """
    A scraper for retrieving product information from the Go Outdoors website.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        URL (str): The URL of the product page.
        SKU (str): The SKU of the product.
        html (HTMLParser): The parsed HTML content of the product page.
    """

    PRICE_SELECTOR = "span.regular-price"
    TITLE_SELECTOR = "span.product-name"
    URL = ""
    SKU = ""

    def __init__(self, id: str):
        """
        Initializes a new instance of the GoOutdoorsScraper class.

        Args:
            id (str): The product ID in the format found in the URL.
            For example: "waterproof-down-jacket-123456".
        """
        self.SKU = id.split("-")[-1]
        self.URL = f"https://www.gooutdoors.co.uk/{self.SKU}/{id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.SKU}')"

    def run(self) -> bool:
        try:
            response = httpx.get(self.URL, headers=self.HEADERS)
            response.raise_for_status()
            temp_html = HTMLParser(response.text)

            self.html = temp_html.html
            self.price = temp_html.css_first(self.PRICE_SELECTOR).text(strip=True)
            self.title = temp_html.css_first(self.TITLE_SELECTOR).text(strip=True)
            return True
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            raise ScraperException(f"{self!r}: {e}")


class AmazonScraper(BaseScraper):
    """
    A scraper for retrieving product information from the Amazon UK website.

    This implementation is not always reliable.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        URL (str): The URL of the product page.
        ASIN (str): The Amazon Standard Identification Number (ASIN) of the product.
        html (HTMLParser): The parsed HTML content of the product page.
    """

    PRICE_SELECTOR = "span.a-offscreen"
    TITLE_SELECTOR = "span#productTitle"
    URL = ""
    ASIN = ""

    def __init__(self, id: str):
        """
        Initializes a new instance of the AmazonScraper class.

        Args:
            id (str): The Amazon Standard Identification Number (ASIN) of the product to scrape.
        """
        self.ASIN = id
        self.URL = f"https://www.amazon.co.uk/dp/{id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.ASIN}')"

    def __get_html_with_playwright(self) -> str:
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        context = browser.new_context(extra_http_headers=self.HEADERS)
        page = context.new_page()
        page.goto(self.URL)
        content = page.content()
        browser.close()
        pw.stop()
        return str(content)

    def run(self) -> bool:
        try:
            temp_html = HTMLParser(self.__get_html_with_playwright())
            self.html = temp_html.html
            self.price = temp_html.css_first(self.PRICE_SELECTOR).text(strip=True)
            self.title = temp_html.css_first(self.TITLE_SELECTOR).text(strip=True)
            return True
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            raise ScraperException(f"{self!r}: {e}")


class AmazonGoogleScraper(BaseScraper):
    """
    A scraper for retrieving Amazon UK product information from the Google Shopping search results page.

    Attributes:
        PRICE_SELECTOR (str): The CSS selector for the product price element.
        TITLE_SELECTOR (str): The CSS selector for the product title element.
        REJECT_COOKIES_SELECTOR (str): The CSS selector for the reject cookies button element.
        PRODUCT_CARDS_SELECTOR (str): The CSS selector for the product card elements.
        PRODUCT_DETAILS_SELECTOR (str): The CSS selector for the product details element.
        html (HTMLParser): The parsed HTML content of the search results page.
        node (SelectolaxNode): The current product card node being processed.
    """

    PRICE_SELECTOR = "span.T14wmb"
    TITLE_SELECTOR = "h3.sh-np__product-title"
    REJECT_COOKIES_SELECTOR = "div.VfPpkd-RLmnJb"
    PRODUCT_CARDS_SELECTOR = "div.KZmu8e"
    PRODUCT_DETAILS_SELECTOR = "div.HUOptb"

    def __init__(self, id: str):
        """
        Initializes a new instance of the AmazonGoogleScraper class.

        Args:
            id (str): The search query to use. Ideally this should be the
            product name as it appears on Amazon.
        """
        self.query = id
        url_query = id.replace(" ", "+")
        self.URL = f"https://www.google.com/search?q={url_query}&tbm=shop"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.query}')"

    def __get_html_with_playwright(self) -> str:
        pw = sync_playwright().start()
        browser = pw.chromium.launch()
        context = browser.new_context(extra_http_headers=self.HEADERS)
        page = context.new_page()
        page.goto(self.URL)
        page.click(self.REJECT_COOKIES_SELECTOR)
        page.wait_for_load_state("networkidle")
        content = page.content()
        browser.close()
        pw.stop()
        return str(content)

    def run(self) -> bool:
        try:
            temp_html = HTMLParser(self.__get_html_with_playwright())
            self.html = temp_html.html

            product_cards = temp_html.css(self.PRODUCT_CARDS_SELECTOR)
            if not product_cards:
                raise AttributeError

            for product_card in product_cards:
                if product_card.select(self.PRODUCT_DETAILS_SELECTOR).any_text_contains(
                    "Amazon.co.uk"
                ) and self.__title_match(product_card):
                    # Found a likely match
                    self.price = product_card.css_first(self.PRICE_SELECTOR).text(
                        strip=True
                    )
                    self.title = product_card.css_first(self.TITLE_SELECTOR).text(
                        strip=True
                    )
                    return True
            return False
        except AttributeError:
            self.price = self.PRICE_404
            self.title = self.TITLE_404
            return False
        except Exception as e:
            raise ScraperException(f"{self!r}: {e}")

    def __title_match(self, product_card: Node) -> bool:
        """Returns True if the scraped product title has over 50% similarity
        to the query value
        """
        title = product_card.css_first(self.TITLE_SELECTOR).text(strip=True)
        similarity: float = td.levenshtein.normalized_similarity(self.query, title)
        return similarity > 0.5


def get_scraper(site: str, product_id: str) -> BaseScraper:
    """
    Returns a scraper instance for the specified site and product ID.

    Args:
        site (str): The site to scrape. Must be one of "amz", "amz-g", or "go_od".
        product_id (str): The ID of the product to scrape in the format required for the site chosen.

    Returns:
        BaseScraper: A scraper instance for the specified site and product ID.
    """

    if site == "amz-g":
        return AmazonGoogleScraper(product_id)
    if site == "go_od":
        return GoOutdoorsScraper(product_id)
    if site == "amz":
        return AmazonScraper(product_id)

    raise Exception(f"Invalid site: {site}")
