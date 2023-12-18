import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from complex_frogs.database.models import Base, ScrapedData, ScrapeTargets

from . import dummy_data as data


@pytest.fixture()
def scrape_target1():
    return ScrapeTargets(
        site=data.scrape_target1["site"],
        sku=data.scrape_target1["sku"],
        send_notification=data.scrape_target1["send_notification"],
        date_added=data.timestamp,
        last_scraped=data.timestamp,
    )


@pytest.fixture()
def scrape_target2():
    return ScrapeTargets(
        site=data.scrape_target2["site"],
        sku=data.scrape_target2["sku"],
        send_notification=data.scrape_target2["send_notification"],
        date_added=data.timestamp,
        last_scraped=data.timestamp,
    )


@pytest.fixture()
def scraped_data1():
    return ScrapedData(
        scrape_target_id=data.scraped_data1["scrape_target_id"],
        title=data.scraped_data1["title"],
        price=data.scraped_data1["price"],
        timestamp=data.timestamp,
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
