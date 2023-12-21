"""Create Read Update & Delete operations for the database."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ScrapedData, ScrapeTargets
from .schema import TargetIn


class TargetExistsError(Exception):
    """Raised when a target already exists in the database."""


class TargetDoesNotExistError(Exception):
    """Raised when a target does not exist in the database."""


class ScrapedDataDoesNotExistError(Exception):
    """Raised when scraped data does not exist in the database."""


# ----------------------
# FUNCTIONS FOR TARGETS
# ----------------------
def read_targets(session: Session) -> Sequence[ScrapeTargets]:
    """Get all scraping targets from database."""
    stmt = select(ScrapeTargets)
    return session.scalars(stmt).all()


def read_target(
    session: Session,
    target_id: int,
    for_update: bool = False,
) -> ScrapeTargets | None:
    """Get a single scraping target from database."""
    if for_update:
        stmt = (
            select(ScrapeTargets).where(ScrapeTargets.id == target_id).with_for_update()
        )
    else:
        stmt = select(ScrapeTargets).where(ScrapeTargets.id == target_id)
    return session.scalar(stmt)


def _target_exists(session: Session, target_site: str, target_sku: str) -> bool:
    """Check if a scraping target exists in the database."""
    stmt = select(ScrapeTargets).where(
        ScrapeTargets.site == target_site,
        ScrapeTargets.sku == target_sku,
    )
    return session.scalar(stmt) is not None


def create_target(session: Session, target: ScrapeTargets) -> ScrapeTargets:
    """Create a new scraping target in the database.

    Raises:
        TargetExistsError: If the target already exists in the database.
    """
    if _target_exists(session, target.site, target.sku):
        raise TargetExistsError

    session.add(target)
    session.commit()
    session.refresh(target)
    return target


def update_target(
    session: Session,
    target_id: int,
    new_target: TargetIn,
) -> ScrapeTargets:
    """Update a scraping target in the database.

    Raises:
        TargetDoesNotExistError: If the target does not exist in the database.
    """
    target = read_target(session, target_id, for_update=True)

    if target is None:
        raise TargetDoesNotExistError

    target.site = new_target.site
    target.sku = new_target.sku
    target.send_notification = new_target.send_notification
    session.commit()
    session.refresh(target)
    return target


def delete_target(session: Session, target_id: int) -> None:
    """Delete a scraping target from the database.

    Raises:
        TargetDoesNotExistError: If the target does not exist in the database.
    """
    target = read_target(session, target_id, for_update=True)

    if target is None:
        raise TargetDoesNotExistError

    session.delete(target)
    session.commit()


# ---------------------------
# FUNCTIONS FOR SCRAPED DATA
# ---------------------------
def read_scrape_data(session: Session) -> Sequence[ScrapedData]:
    """Get all scrape data from database."""
    stmt = select(ScrapedData)
    return session.scalars(stmt).all()


def read_scrape_data_for_target(
    session: Session,
    target_id: int,
) -> Sequence[ScrapedData]:
    """Get all scrape data for a target from database.

    Raises:
        TargetDoesNotExistError: If the target does not exist in the database.
    """
    if not read_target(session, target_id):
        raise TargetDoesNotExistError

    stmt = select(ScrapedData).where(ScrapedData.scrape_target_id == target_id)
    return session.scalars(stmt).all()


def read_scrape_data_by_id(session: Session, scrape_data_id: int) -> ScrapedData:
    """Get specific scrape data by id from database.

    Raises:
        ScrapedDataDoesNotExistError: If the scraped data does not exist in the database.
    """
    stmt = select(ScrapedData).where(ScrapedData.id == scrape_data_id)
    scraped_data = session.scalar(stmt)

    if scraped_data is None:
        raise ScrapedDataDoesNotExistError

    return scraped_data


def delete_scrape_data(session: Session, scrape_data_id: int) -> None:
    """Delete scrape data for a target from the database.

    Raises:
        ScrapedDataDoesNotExistError: If the scraped data does not exist in the database.
    """
    scraped_data = read_scrape_data_by_id(session, scrape_data_id)
    session.delete(scraped_data)
    session.commit()
