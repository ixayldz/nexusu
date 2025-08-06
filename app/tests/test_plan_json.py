from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_plan_json():
    res = client.post("/tasks/plan", json={"spec": "json demo"}).json()
    assert len(res["steps"]) >= 1
    assert {"id", "title", "description"} <= res["steps"][0].keys()
