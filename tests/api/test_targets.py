from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from complex_frogs.api import targets
from complex_frogs.database import get_db
from tests.test_data import (
    get_test_db,
    new_scrape_target,
    scrape_target1,
    scrape_target2,
    scraped_data1,
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
