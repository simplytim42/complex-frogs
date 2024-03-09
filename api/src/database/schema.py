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
