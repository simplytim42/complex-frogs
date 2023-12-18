from datetime import timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import ScrapedData, ScrapeTargets


def test_create_scrape_target(empty_db: Session, scrape_target1: ScrapeTargets):
    empty_db.add(scrape_target1)
    empty_db.commit()

    stmt = select(ScrapeTargets)
    retrieved_target = empty_db.scalars(stmt).first()

    # make datetimes aware
    retrieved_target.date_added = retrieved_target.date_added.replace(
        tzinfo=timezone.utc,
    )
    retrieved_target.last_scraped = retrieved_target.last_scraped.replace(
        tzinfo=timezone.utc,
    )

    assert retrieved_target.site == scrape_target1.site
    assert retrieved_target.sku == scrape_target1.sku
    assert retrieved_target.send_notification == scrape_target1.send_notification
    # testing datetimes as aware to ensure they can be entereted into the db as naive
    assert retrieved_target.date_added == scrape_target1.date_added
    assert retrieved_target.last_scraped == scrape_target1.last_scraped


def test_create_scrape_data(empty_db: Session, scraped_data1: ScrapedData):
    empty_db.add(scraped_data1)
    empty_db.commit()

    stmt = select(ScrapedData)
    retrieved_data = empty_db.scalars(stmt).first()

    # make datetimes aware
    retrieved_data.timestamp = retrieved_data.timestamp.replace(
        tzinfo=timezone.utc,
    )

    assert retrieved_data.scrape_target_id == scraped_data1.scrape_target_id
    assert retrieved_data.title == scraped_data1.title
    assert retrieved_data.price == scraped_data1.price
    assert retrieved_data.timestamp == scraped_data1.timestamp
