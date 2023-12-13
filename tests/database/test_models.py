from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from complex_frogs.database.models import Base, ScrapedData, ScrapeTargets


@pytest.fixture()
def timestamp():
    return datetime.now(tz=timezone.utc)


@pytest.fixture()
def target(timestamp):
    return ScrapeTargets(
        site="test site",
        sku="test sku",
        send_notification=True,
        date_added=timestamp,
        last_scraped=timestamp,
    )


@pytest.fixture()
def scraped_data(timestamp):
    return ScrapedData(
        scrape_target_id=1,
        title="test title",
        price="£10",
        timestamp=timestamp,
    )


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    session = Session(engine)
    Base.metadata.create_all(engine)
    yield session
    Base.metadata.drop_all(engine)


def test_scrape_target_repr(target):
    expected_repr = (
        "ScrapeTargets(site='test site', sku='test sku', send_notification=True)"
    )
    assert repr(target) == expected_repr


def test_create_scrape_target(session, target, timestamp):
    session.add(target)
    session.commit()

    stmt = select(ScrapeTargets)
    retrieved_target = session.scalars(stmt).first()

    # make datetimes aware
    retrieved_target.date_added = retrieved_target.date_added.replace(
        tzinfo=timezone.utc,
    )
    retrieved_target.last_scraped = retrieved_target.last_scraped.replace(
        tzinfo=timezone.utc,
    )

    assert retrieved_target.site == "test site"
    assert retrieved_target.sku == "test sku"
    assert retrieved_target.send_notification is True
    # testing datetimes as aware to ensure they can be entereted into the db as naive
    assert retrieved_target.date_added == timestamp
    assert retrieved_target.last_scraped == timestamp


def test_scrape_data_repr(scraped_data):
    expected_repr = "ScrapedData(scrape_target_id=1, title='test title', price='£10')"
    assert repr(scraped_data) == expected_repr


def test_create_scrape_data(session, target, scraped_data, timestamp):
    session.add(target)
    session.commit()

    session.add(scraped_data)
    session.commit()

    stmt = select(ScrapedData)
    retrieved_data = session.scalars(stmt).first()

    # make datetimes aware
    retrieved_data.timestamp = retrieved_data.timestamp.replace(
        tzinfo=timezone.utc,
    )

    assert retrieved_data.scrape_target_id == target.id
    assert retrieved_data.title == "test title"
    assert retrieved_data.price == "£10"
    assert retrieved_data.timestamp == timestamp
