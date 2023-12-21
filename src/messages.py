"""API message models."""

from pydantic import BaseModel


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
