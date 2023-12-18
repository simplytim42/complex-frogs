from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api import root

app = FastAPI()
app.include_router(root.router)

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_418_IM_A_TEAPOT
    data = response.json()
    assert data["message"] == "Complex Frogs API"
