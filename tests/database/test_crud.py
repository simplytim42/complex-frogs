import pytest
from sqlalchemy.orm import Session

from src.database import crud
from src.database.models import ScrapedData, ScrapeTargets


def test_read_targets(dummy_db: Session, scrape_target1: ScrapeTargets):
    result = crud.read_targets(dummy_db)

    assert isinstance(result[0], ScrapeTargets)
    assert isinstance(result[1], ScrapeTargets)

    assert result[0].site == scrape_target1.site
    assert result[0].sku == scrape_target1.sku


def test_read_targets_empty_db(empty_db: Session):
    result = crud.read_targets(empty_db)

    assert result == []


def test_read_target(dummy_db: Session, scrape_target2: ScrapeTargets):
    result = crud.read_target(dummy_db, 2)

    assert isinstance(result, ScrapeTargets)
    assert result.site == scrape_target2.site
    assert result.sku == scrape_target2.sku


def test_read_target_empty_db(empty_db: Session):
    result = crud.read_target(empty_db, 1)

    assert result is None


def test_read_target_no_data(dummy_db: Session):
    result = crud.read_target(dummy_db, 999999)

    assert result is None


def test_create_target(empty_db: Session, scrape_target1: ScrapeTargets):
    result = crud.create_target(empty_db, scrape_target1)

    assert isinstance(result, ScrapeTargets)
    assert result.site == scrape_target1.site
    assert result.sku == scrape_target1.sku
    assert result.send_notification == scrape_target1.send_notification


def test_create_target_already_exists(dummy_db: Session, scrape_target1: ScrapeTargets):
    with pytest.raises(crud.TargetExistsError):
        crud.create_target(dummy_db, scrape_target1)


def test_update_target(dummy_db: Session, scrape_target1: ScrapeTargets):
    result = crud.update_target(dummy_db, 2, scrape_target1)

    assert isinstance(result, ScrapeTargets)
    assert result.site == scrape_target1.site
    assert result.sku == scrape_target1.sku
    assert result.send_notification == scrape_target1.send_notification


def test_update_target_empty_db(empty_db: Session, scrape_target1: ScrapeTargets):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.update_target(empty_db, 1, scrape_target1)


def test_update_target_no_target(dummy_db: Session, scrape_target1: ScrapeTargets):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.update_target(dummy_db, 999999, scrape_target1)


def test_delete_target(dummy_db: Session):
    id_for_deletion = 2
    deleted_target = crud.delete_target(dummy_db, id_for_deletion)
    assert deleted_target.id == id_for_deletion

    result = crud.read_targets(dummy_db)

    assert len(result) == 1


def test_delete_target_empty_db(empty_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.delete_target(empty_db, 1)


def test_delete_target_no_target(dummy_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.delete_target(dummy_db, 999999)


def test_read_scrape_data(dummy_db: Session, scraped_data1: ScrapedData):
    result = crud.read_scrape_data(dummy_db)

    assert len(result) == 1
    assert isinstance(result[0], ScrapedData)

    assert result[0].title == scraped_data1.title
    assert result[0].price == scraped_data1.price


def test_read_scrape_data_empty_db(empty_db: Session):
    result = crud.read_scrape_data(empty_db)

    assert result == []


def test_read_scrape_data_for_target(dummy_db: Session, scraped_data1: ScrapedData):
    result = crud.read_scrape_data_for_target(dummy_db, 1)

    assert len(result) == 1
    assert isinstance(result[0], ScrapedData)

    assert result[0].title == scraped_data1.title
    assert result[0].price == scraped_data1.price


def test_read_scrape_data_for_target_empty_db(empty_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.read_scrape_data_for_target(empty_db, 1)


def test_read_scrape_data_for_target_no_target(dummy_db: Session):
    with pytest.raises(crud.TargetDoesNotExistError):
        crud.read_scrape_data_for_target(dummy_db, 999999)


def test_read_scrape_data_by_id(dummy_db: Session, scraped_data1: ScrapedData):
    result = crud.read_scrape_data_by_id(dummy_db, 1)

    assert isinstance(result, ScrapedData)

    assert result.title == scraped_data1.title
    assert result.price == scraped_data1.price


def test_read_scrape_data_by_id_empty_db(empty_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.read_scrape_data_by_id(empty_db, 1)


def test_read_scrape_data_by_id_no_data(dummy_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.read_scrape_data_by_id(dummy_db, 999999)


def test_delete_scrape_data(dummy_db: Session):
    id_for_deletion = 1
    deleted_data = crud.delete_scrape_data(dummy_db, id_for_deletion)
    assert deleted_data.id == id_for_deletion

    result = crud.read_scrape_data(dummy_db)
    assert result == []


def test_delete_scrape_data_empty_db(empty_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.delete_scrape_data(empty_db, 1)


def test_delete_scrape_data_no_data(dummy_db: Session):
    with pytest.raises(crud.ScrapedDataDoesNotExistError):
        crud.delete_scrape_data(dummy_db, 999999)
