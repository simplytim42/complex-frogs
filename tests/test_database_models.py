from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from complex_frogs.database.models import Base, ScrapedData, ScrapeTargets


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    session = Session(engine)
    Base.metadata.create_all(engine)
    yield session
    Base.metadata.drop_all(engine)


def test_create_scrape_target(session):
    now = datetime.now(tz=timezone.utc)
    target = ScrapeTargets(
        site="test site",
        sku="test sku",
        send_notification=True,
        date_added=now,
        last_scraped=now,
    )
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
    assert retrieved_target.date_added == now
    assert retrieved_target.last_scraped == now


def test_create_scrape_data(session):
    now = datetime.now(tz=timezone.utc)
    target = ScrapeTargets(
        site="test site",
        sku="test sku",
        send_notification=True,
        date_added=now,
        last_scraped=now,
    )
    session.add(target)
    session.commit()

    data = ScrapedData(
        scrape_target_id=target.id,
        title="test title",
        price="test price",
        timestamp=now,
    )
    session.add(data)
    session.commit()

    stmt = select(ScrapedData)
    retrieved_data = session.scalars(stmt).first()

    # make datetimes aware
    retrieved_data.timestamp = retrieved_data.timestamp.replace(
        tzinfo=timezone.utc,
    )

    assert retrieved_data.scrape_target_id == target.id
    assert retrieved_data.title == "test title"
    assert retrieved_data.price == "test price"
    assert retrieved_data.timestamp == now
