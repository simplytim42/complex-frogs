import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from run_api import app
from src import messages
from src.database import get_db
from tests.dummy_data import (
    new_scrape_target,
    override_get_db,
    scrape_target1,
    scrape_target2,
)


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield None
    app.dependency_overrides = {}


client = TestClient(app)


def test_get_targets():
    response = client.get("/targets/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    targets_in_db = 2
    assert len(data) == targets_in_db
    assert data[0]["site"] == scrape_target1["site"]
    assert data[0]["sku"] == scrape_target1["sku"]
    assert data[0]["send_notification"] == scrape_target1["send_notification"]

    assert data[1]["site"] == scrape_target2["site"]
    assert data[1]["sku"] == scrape_target2["sku"]
    assert data[1]["send_notification"] == scrape_target2["send_notification"]


def test_get_targets_db_error(mocker):
    mocker.patch(
        "src.database.crud.read_targets",
        side_effect=SQLAlchemyError,
    )
    response = client.get("/targets/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data == messages.DatabaseErrorMessage().model_dump()


def test_post_new_target():
    response = client.post("/targets/", json=new_scrape_target)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["site"] == new_scrape_target["site"]
    assert data["sku"] == new_scrape_target["sku"]
    assert data["send_notification"] == new_scrape_target["send_notification"]


def test_post_new_target_already_exists():
    response = client.post("/targets/", json=scrape_target1)
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data == messages.TargetExistsMessage().model_dump()


def test_post_new_target_db_error(mocker):
    mocker.patch(
        "src.database.crud.create_target",
        side_effect=SQLAlchemyError,
    )
    response = client.post("/targets/", json=new_scrape_target)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data == messages.DatabaseErrorMessage().model_dump()


def test_get_target_with_id():
    response = client.get(f"/targets/{scrape_target2['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["site"] == scrape_target2["site"]
    assert data["sku"] == scrape_target2["sku"]
    assert data["send_notification"] == scrape_target2["send_notification"]


def test_get_target_with_id_not_found():
    response = client.get("/targets/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data == messages.TargetDoesNotExistMessage().model_dump()


def test_get_target_with_id_db_error(mocker):
    mocker.patch(
        "src.database.crud.read_target",
        side_effect=SQLAlchemyError,
    )
    response = client.get(f"/targets/{scrape_target2['id']}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data == messages.DatabaseErrorMessage().model_dump()


def test_put_update_target():
    response = client.put(
        f"/targets/{scrape_target1['id']}",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["site"] == new_scrape_target["site"]
    assert data["sku"] == new_scrape_target["sku"]
    assert data["send_notification"] == new_scrape_target["send_notification"]


def test_put_update_target_not_found():
    response = client.put(
        "/targets/99999",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data == messages.TargetDoesNotExistMessage().model_dump()


def test_put_update_target_db_error(mocker):
    mocker.patch(
        "src.database.crud.update_target",
        side_effect=SQLAlchemyError,
    )
    response = client.put(
        f"/targets/{scrape_target1['id']}",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data == messages.DatabaseErrorMessage().model_dump()


def test_delete_target():
    response = client.delete(f"/targets/{scrape_target1['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == scrape_target1["id"]
    assert data["site"] == scrape_target1["site"]
    assert data["sku"] == scrape_target1["sku"]
    assert data["send_notification"] == scrape_target1["send_notification"]


def test_delete_target_not_found():
    response = client.delete("/targets/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data == messages.TargetDoesNotExistMessage().model_dump()


def test_delete_target_db_error(mocker):
    mocker.patch(
        "src.database.crud.delete_target",
        side_effect=SQLAlchemyError,
    )
    response = client.delete(f"/targets/{scrape_target1['id']}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data == messages.DatabaseErrorMessage().model_dump()
