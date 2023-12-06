"""Pydantic models."""

from pydantic import BaseModel


class Target(BaseModel):
    """model for a scraping target."""

    id: int  # noqa: A003
    site: str
    sku: str
    send_notification: bool
