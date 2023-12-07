"""Database models."""

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""


class ScrapeTargets(Base):
    """This table stores the targets to scrape.

    A target is a combination of a site and a SKU.
    """

    __tablename__ = "scrape_targets"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    site: Mapped[str]
    sku: Mapped[str]
    send_notification: Mapped[bool]
    date_added: Mapped[datetime]
    last_scraped: Mapped[datetime]

    scraped_data: Mapped[List["ScrapedData"]] = relationship(
        back_populates="scrape_target",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"ScrapeTarget(site={self.site!r}, sku={self.sku!r}, send_notification={self.send_notification!r})"


class ScrapedData(Base):
    """This table stores the scraped data."""

    __tablename__ = "scraped_data"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    scrape_target_id: Mapped[int] = mapped_column(ForeignKey("scrape_targets.id"))
    title: Mapped[str]
    price: Mapped[str]
    timestamp: Mapped[datetime]

    scrape_target: Mapped["ScrapeTargets"] = relationship(back_populates="scraped_data")

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"ScrapedData(scrape_target_id={self.scrape_target_id!r}, title={self.title!r}, price={self.price!r})"
