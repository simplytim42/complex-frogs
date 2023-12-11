"""Create Read Update & Delete operations for the database."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ScrapeTargets


class TargetExistsError(Exception):
    """Raised when a target already exists in the database."""


class TargetDoesNotExistError(Exception):
    """Raised when a target does not exist in the database."""


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
    """Create a new scraping target in the database."""
    if _target_exists(session, target.site, target.sku):
        raise TargetExistsError

    session.add(target)
    session.commit()
    return target


def update_target(
    session: Session,
    target_id: int,
    new_target: ScrapeTargets,
) -> ScrapeTargets:
    """Update a scraping target in the database."""
    target = read_target(session, target_id, for_update=True)

    if target is None:
        raise TargetDoesNotExistError

    target.site = new_target.site
    target.sku = new_target.sku
    session.commit()
    return target
