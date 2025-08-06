import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _wait(job_id: str):
    for _ in range(15):
        out = client.get(f"/jobs/{job_id}").json()
        if out["status"] == "finished":
            return out
        time.sleep(0.2)
    raise AssertionError("test job timeout")


def test_test_json():
    res = client.post("/tasks/test", json={"artifacts": ["img"]}).json()
    assert res["status"] == "queued"
    final = _wait(res["job_id"])
    assert final["result"]["score"] >= 0
