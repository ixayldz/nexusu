from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_plan_cache_hits():
    body = {"spec": "hello cache"}
    first = client.post("/tasks/plan", json=body).json()
    second = client.post("/tasks/plan", json=body).json()
    assert first == second
