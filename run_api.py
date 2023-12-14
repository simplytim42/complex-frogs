"""Main API file for Complex Frogs API."""

from fastapi import FastAPI

from complex_frogs.api import root, scrape_data, targets
from complex_frogs.logger.config import LOGS_DIR, setup_logger

setup_logger(LOGS_DIR / "api.log")

description = """
## "Targets"
Each **Target** is a product on the internet that we want to scrape.

Currently we support the following websites:
- [Amazon UK](https://www.amazon.co.uk)
- [Amazon UK via Google Shopping](https://www.google.com/shopping) (this is a workaround for the Amazon in some deployment situations where the main Amazon UK scraper gets blocked)
- [Go Outdoors](https://www.gooutdoors.co.uk)

## "Scrape Data"
Each scrape data is a single scrape of a **Target**.
"""

app = FastAPI(
    title="Complex Frogs API",
    description=description,
    summary="API Access to the Complex Frogs web scraping database",
    version="2.0.0",
    license_info={"name": "MIT License", "identifier": "MIT"},
    contact={
        "name": "Tim MacKay",
        "url": "https://github.com/simplytim42",
    },
)

app.include_router(targets.router)
app.include_router(scrape_data.router)
app.include_router(root.router)
