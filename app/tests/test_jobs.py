import time

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _wait_finished(job_id: str):
    """Basit polling – en fazla ~5 sn bekler."""
    for _ in range(10):
        res = client.get(f"/jobs/{job_id}").json()
        if res["status"] == "finished":
            return res
        time.sleep(0.5)
    raise AssertionError("Job did not finish in time")


def test_build_async():
    res = client.post("/tasks/build", json={"steps": ["one"]}).json()
    assert res["status"] == "queued"
    job = _wait_finished(res["job_id"])
    assert job["result"]["success"] is True


def test_test_async():
    res = client.post("/tasks/test", json={"artifacts": ["img"]}).json()
    assert res["status"] == "queued"
    job = _wait_finished(res["job_id"])
    assert job["result"]["passed"] is True
