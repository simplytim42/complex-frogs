import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from complex_frogs.api import targets
from complex_frogs.database import get_db
from tests.test_data import (
    get_test_db,
    new_scrape_target,
    scrape_target1,
    scrape_target2,
)

app = FastAPI()
app.include_router(targets.router)
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


def test_get_targets():
    response = client.get("/targets/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    targets_in_db = 2
    assert len(data) == targets_in_db
    assert data[0]["site"] == scrape_target1["site"]
    assert data[1]["site"] == scrape_target2["site"]


def test_get_targets_db_error(mocker):
    mocker.patch(
        "complex_frogs.database.crud.read_targets",
        side_effect=SQLAlchemyError,
    )
    response = client.get("/targets/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Database error"


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
    assert data["detail"] == "Target already exists"


def test_post_new_target_db_error(mocker):
    mocker.patch(
        "complex_frogs.database.crud.create_target",
        side_effect=SQLAlchemyError,
    )
    response = client.post("/targets/", json=new_scrape_target)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Database error"


def test_get_target_with_id():
    response = client.get(f"/targets/{scrape_target2['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["site"] == scrape_target2["site"]


def test_get_target_with_id_not_found():
    response = client.get("/targets/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_get_target_with_id_db_error(mocker):
    mocker.patch(
        "complex_frogs.database.crud.read_target",
        side_effect=SQLAlchemyError,
    )
    response = client.get(f"/targets/{scrape_target2['id']}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Database error"


def test_put_update_target():
    response = client.put(
        f"/targets/{scrape_target1['id']}",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["site"] == new_scrape_target["site"]


def test_put_update_target_not_found():
    response = client.put(
        "/targets/99999",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_put_update_target_db_error(mocker):
    mocker.patch(
        "complex_frogs.database.crud.update_target",
        side_effect=SQLAlchemyError,
    )
    response = client.put(
        f"/targets/{scrape_target1['id']}",
        json=new_scrape_target,
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Database error"


def test_delete_target():
    response = client.delete(f"/targets/{scrape_target1['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_target_not_found():
    response = client.delete("/targets/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_delete_target_db_error(mocker):
    mocker.patch(
        "complex_frogs.database.crud.delete_target",
        side_effect=SQLAlchemyError,
    )
    response = client.delete(f"/targets/{scrape_target1['id']}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Database error"
