import pytest
from fastapi import status
from fastapi.testclient import TestClient

from run_api import app
from src.database import get_db
from tests.dummy_data import (
    get_empty_db,
    new_scrape_target,
    scrape_target1,
)


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = get_empty_db
    yield None
    app.dependency_overrides = {}


client = TestClient(app)


def test_get_targets():
    response = client.get("/targets")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_post_targets():
    response = client.post("/targets", json=new_scrape_target)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["site"] == new_scrape_target["site"]
    assert data["sku"] == new_scrape_target["sku"]
    assert data["send_notification"] == new_scrape_target["send_notification"]


def test_get_target_by_id():
    response = client.get("/targets/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_put_target_by_id():
    response = client.put("/targets/1", json=scrape_target1)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_delete_target_by_id():
    response = client.delete("/targets/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_get_scrape_data():
    response = client.get("/scrape-data")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_scrape_data_by_target():
    response = client.get("/scrape-data/target/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Target not found"


def test_get_scrape_data_by_id():
    response = client.get("/scrape-data/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Scrape data not found"


def test_delete_scrape_data_by_id():
    response = client.delete("/scrape-data/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Scrape data not found"
