"""Create Read Update & Delete operations for the database."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ScrapeTargets


def read_targets(session: Session):
    """Get all scraping targets from database."""
    stmt = select(ScrapeTargets)
    return session.scalars(stmt)
