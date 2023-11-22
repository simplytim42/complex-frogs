from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class ScrapeTargets(Base):
    __tablename__ = "scrape_targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    site: Mapped[str]
    sku: Mapped[str]
    send_notification: Mapped[bool]
    date_added: Mapped[datetime]
    last_scraped: Mapped[Optional[datetime]]

    scraped_data: Mapped[List["ScrapedData"]] = relationship(
        back_populates="scrape_target", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"ScrapeTarget(site={self.site!r}, sku={self.sku!r}, send_notification={self.send_notification!r})"


class ScrapedData(Base):
    __tablename__ = "scraped_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    scrape_target_id: Mapped[int] = mapped_column(ForeignKey("scrape_targets.id"))
    title: Mapped[str]
    price: Mapped[str]
    timestamp: Mapped[datetime]

    scrape_target: Mapped["ScrapeTargets"] = relationship(back_populates="scraped_data")

    def __repr__(self):
        return f"ScrapedData(scrape_target_id={self.scrape_target_id!r}, title={self.title!r}, price={self.price!r})"
