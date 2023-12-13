from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from complex_frogs.database import crud
from complex_frogs.database.models import Base, ScrapedData, ScrapeTargets


@pytest.fixture()
def target1():
    now = datetime.now(tz=timezone.utc)
    return ScrapeTargets(
        site="test site1",
        sku="test sku1",
        send_notification=True,
        date_added=now,
        last_scraped=now,
    )


@pytest.fixture()
def target2():
    now = datetime.now(tz=timezone.utc)
    return ScrapeTargets(
        site="test site2",
        sku="test sku2",
        send_notification=True,
        date_added=now,
        last_scraped=now,
    )


@pytest.fixture()
def scraped_data1():
    now = datetime.now(tz=timezone.utc)
    return ScrapedData(
        scrape_target_id=1,
        title="test title1",
        price="£10",
        timestamp=now,
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
    target1: ScrapeTargets,
    target2: ScrapeTargets,
    scraped_data1: ScrapedData,
):
    target1.scraped_data.append(scraped_data1)
    empty_db.add(target1)
    empty_db.add(target2)
    empty_db.commit()
    return empty_db


def test_read_targets(dummy_db: Session):
    result = crud.read_targets(dummy_db)

    assert isinstance(result[0], ScrapeTargets)
    assert isinstance(result[1], ScrapeTargets)

    assert result[0].site == "test site1"
    assert result[0].sku == "test sku1"


def test_read_targets_empty_db(empty_db: Session):
    result = crud.read_targets(empty_db)

    assert result == []


def test_read_target(dummy_db: Session):
    result = crud.read_target(dummy_db, 2)

    assert isinstance(result, ScrapeTargets)
    assert result.site == "test site2"
    assert result.sku == "test sku2"


def test_read_target_empty_db(empty_db: Session):
    result = crud.read_target(empty_db, 1)

    assert result is None


def test_read_target_no_data(dummy_db: Session):
    result = crud.read_target(dummy_db, 999999)

    assert result is None


def test_create_target(empty_db: Session, target1: ScrapeTargets):
    result = crud.create_target(empty_db, target1)

    assert isinstance(result, ScrapeTargets)
    assert result.site == "test site1"
    assert result.sku == "test sku1"
    assert result.send_notification is True


def test_create_target_already_exists(dummy_db: Session, target1: ScrapeTargets):
    with pytest.raises(crud.TargetExistsError):
        crud.create_target(dummy_db, target1)


def test_update_target(dummy_db: Session, target1: ScrapeTargets):
    result = crud.update_target(dummy_db, 2, target1)

    assert isinstance(result, ScrapeTargets)
    assert result.site == "test site1"
    assert result.sku == "test sku1"
    assert result.send_notification is True


def test_update_target_empty_db(empty_db: Session, target1: ScrapeTargets):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.update_target(empty_db, 1, target1)


def test_update_target_no_target(dummy_db: Session, target1: ScrapeTargets):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.update_target(dummy_db, 999999, target1)


def test_delete_target(dummy_db: Session):
    crud.delete_target(dummy_db, 2)

    result = crud.read_targets(dummy_db)

    assert len(result) == 1


def test_delete_target_empty_db(empty_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.delete_target(empty_db, 1)


def test_delete_target_no_target(dummy_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.delete_target(dummy_db, 999999)


def test_read_scrape_data(dummy_db: Session):
    result = crud.read_scrape_data(dummy_db)

    assert len(result) == 1
    assert isinstance(result[0], ScrapedData)

    assert result[0].title == "test title1"
    assert result[0].price == "£10"


def test_read_scrape_data_empty_db(empty_db: Session):
    result = crud.read_scrape_data(empty_db)

    assert result == []


def test_read_scrape_data_for_target(dummy_db: Session):
    result = crud.read_scrape_data_for_target(dummy_db, 1)

    assert len(result) == 1
    assert isinstance(result[0], ScrapedData)

    assert result[0].title == "test title1"
    assert result[0].price == "£10"


def test_read_scrape_data_for_target_empty_db(empty_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.read_scrape_data_for_target(empty_db, 1)


def test_read_scrape_data_for_target_no_target(dummy_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.read_scrape_data_for_target(dummy_db, 999999)


def test_read_scrape_data_by_id(dummy_db: Session):
    result = crud.read_scrape_data_by_id(dummy_db, 1)

    assert isinstance(result, ScrapedData)

    assert result.title == "test title1"
    assert result.price == "£10"


def test_read_scrape_data_by_id_empty_db(empty_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.read_scrape_data_by_id(empty_db, 1)


def test_read_scrape_data_by_id_no_data(dummy_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.read_scrape_data_by_id(dummy_db, 999999)


def test_delete_scrape_data(dummy_db: Session):
    crud.delete_scrape_data(dummy_db, 1)

    result = crud.read_scrape_data(dummy_db)

    assert result == []


def test_delete_scrape_data_empty_db(empty_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.delete_scrape_data(empty_db, 1)


def test_delete_scrape_data_no_data(dummy_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.delete_scrape_data(dummy_db, 999999)
