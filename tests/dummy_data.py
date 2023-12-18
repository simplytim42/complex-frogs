"""Test data"""

from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database.models import Base, ScrapedData, ScrapeTargets

timestamp = datetime.now(tz=timezone.utc)

scrape_target1 = {
    "id": 1,
    "site": "test site1",
    "sku": "test sku1",
    "send_notification": True,
}

scrape_target2 = {
    "id": 2,
    "site": "test site2",
    "sku": "test sku2",
    "send_notification": True,
}

new_scrape_target = {
    "id": 3,
    "site": "test site3",
    "sku": "test sku3",
    "send_notification": False,
}

scraped_data1 = {
    "scrape_target_id": 1,
    "title": "test title1",
    "price": "£10",
}


def get_empty_db() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    yield session
    Base.metadata.drop_all(bind=engine)


def get_test_db() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    one = ScrapeTargets(
        id=scrape_target1["id"],
        site=scrape_target1["site"],
        sku=scrape_target1["sku"],
        send_notification=scrape_target1["send_notification"],
        date_added=timestamp,
        last_scraped=timestamp,
    )
    one.scraped_data.append(
        ScrapedData(
            scrape_target_id=scraped_data1["scrape_target_id"],
            title=scraped_data1["title"],
            price=scraped_data1["price"],
            timestamp=timestamp,
        ),
    )
    two = ScrapeTargets(
        id=scrape_target2["id"],
        site=scrape_target2["site"],
        sku=scrape_target2["sku"],
        send_notification=scrape_target2["send_notification"],
        date_added=timestamp,
        last_scraped=timestamp,
    )
    session.add(one)
    session.add(two)
    session.commit()
    yield session
    Base.metadata.drop_all(bind=engine)
