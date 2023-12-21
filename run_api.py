"""Main API file for Complex Frogs API."""
import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src import messages
from src.api import root, scrape_data, targets
from src.database import crud
from src.logger.config import LOGS_DIR, setup_logger

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


@app.exception_handler(crud.TargetExistsError)
async def target_exists_handler(
    request: Request,
    exc: crud.TargetExistsError,
) -> JSONResponse:
    """Handle CRUD TargetExistsError."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=messages.TargetExistsMessage().model_dump(),
    )


@app.exception_handler(crud.TargetDoesNotExistError)
async def target_does_not_exist_handler(
    request: Request,
    exc: crud.TargetDoesNotExistError,
) -> JSONResponse:
    """Handle CRUD TargetDoesNotExistError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=messages.TargetDoesNotExistMessage().model_dump(),
    )


@app.exception_handler(crud.ScrapedDataDoesNotExistError)
async def scrape_data_does_not_exist_handler(
    request: Request,
    exc: crud.ScrapedDataDoesNotExistError,
) -> JSONResponse:
    """Handle CRUD ScrapedDataDoesNotExistError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=messages.ScrapeDataDoesNotExistMessage().model_dump(),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    """Handle SQLAlchemy errors."""
    logging.exception(msg=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=messages.DatabaseErrorMessage().model_dump(),
    )
