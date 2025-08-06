from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_plan_route():
    res = client.post("/tasks/plan", json={"spec": "hello world"})
    assert res.status_code == 200
    body = res.json()
    assert "steps" in body and len(body["steps"]) >= 1