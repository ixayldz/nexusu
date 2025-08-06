import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _wait(job_id: str):
    for _ in range(15):           # 15 × 0.2s ≈ 3 s
        out = client.get(f"/jobs/{job_id}").json()
        if out["status"] == "finished":
            return out
        time.sleep(0.2)
    raise AssertionError("build job timeout")


def test_build_json():
    res = client.post("/tasks/build", json={"steps": ["x"]}).json()
    assert res["status"] == "queued"
    final = _wait(res["job_id"])
    files = final["result"]["files"]
    assert files and {"path", "content"} <= files[0].keys()
