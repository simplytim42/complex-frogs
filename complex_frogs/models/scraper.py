"""Pydantic models."""

from datetime import datetime

from pydantic import BaseModel


class Target(BaseModel):
    """model for a scraping target."""

    id: int  # noqa: A003
    site: str
    sku: str
    send_notification: bool
    date_added: datetime
    last_scraped: datetime


class NewTarget(BaseModel):
    """model for a new scraping target."""

    site: str
    sku: str
    send_notification: bool
