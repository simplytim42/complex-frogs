from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api import scrape_data, targets
from src.database import get_db
from tests.dummy_data import (
    get_empty_db,
    new_scrape_target,
    scrape_target1,
)

app = FastAPI()
app.include_router(targets.router)
app.include_router(scrape_data.router)
app.dependency_overrides[get_db] = get_empty_db

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
