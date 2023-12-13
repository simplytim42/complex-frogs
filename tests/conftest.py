from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from complex_frogs.database.models import Base, ScrapedData, ScrapeTargets


@pytest.fixture()
def timestamp():
    return datetime.now(tz=timezone.utc)


@pytest.fixture()
def scrape_target1(timestamp):
    return ScrapeTargets(
        site="test site1",
        sku="test sku1",
        send_notification=True,
        date_added=timestamp,
        last_scraped=timestamp,
    )


@pytest.fixture()
def scrape_target2(timestamp):
    return ScrapeTargets(
        site="test site2",
        sku="test sku2",
        send_notification=True,
        date_added=timestamp,
        last_scraped=timestamp,
    )


@pytest.fixture()
def scraped_data1(timestamp):
    return ScrapedData(
        scrape_target_id=1,
        title="test title1",
        price="£10",
        timestamp=timestamp,
    )


@pytest.fixture()
def empty_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def dummy_db(
    empty_db: Session,
    scrape_target1: ScrapeTargets,
    scrape_target2: ScrapeTargets,
    scraped_data1: ScrapedData,
):
    scrape_target1.scraped_data.append(scraped_data1)
    empty_db.add(scrape_target1)
    empty_db.add(scrape_target2)
    empty_db.commit()
    return empty_db
