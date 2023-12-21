"""Pydantic models."""

from datetime import datetime

from pydantic import BaseModel


class TargetBase(BaseModel):
    """base model for a scraping target."""

    site: str
    sku: str
    send_notification: bool


class TargetIn(TargetBase):
    """model for a new scraping target."""


class TargetOut(TargetBase):
    """model for a scraping target."""

    id: int  # noqa: A003
    date_added: datetime
    last_scraped: datetime


class ScrapeDataBase(BaseModel):
    """base model for the scrape data."""

    scrape_target_id: int
    title: str
    price: str
    timestamp: datetime


class ScrapeDataIn(ScrapeDataBase):
    """model for new scraping data."""


class ScrapeDataOut(ScrapeDataBase):
    """model for a scrape data."""

    id: int  # noqa: A003


class RootMessage(BaseModel):
    """Root API message."""

    detail: str = "Welcome to the Complex Frogs API"


class TargetExistsMessage(BaseModel):
    """Error message for when a target already exists in the database."""

    detail: str = "Target already exists"


class TargetDoesNotExistMessage(BaseModel):
    """Error message for when a target does not exist in the database."""

    detail: str = "Target not found"


class ScrapeDataDoesNotExistMessage(BaseModel):
    """Error message for when scrape data does not exist in the database."""

    detail: str = "Scrape data not found"


class DatabaseErrorMessage(BaseModel):
    """Error message for when there is a database error."""

    detail: str = "Database error"
