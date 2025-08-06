import time, os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.core.settings import get_settings

client = TestClient(app)
WS = Path(get_settings().workspace_dir)

def _wait(job_id):
    for _ in range(15):
        r = client.get(f"/jobs/{job_id}").json()
        if r["status"] == "finished":
            return r
        time.sleep(0.2)
    raise AssertionError("timeout")

def test_builder_writes_files():
    res = client.post("/tasks/build", json={"steps": ["x"]}).json()
    final = _wait(res["job_id"])
    for f in final["result"]["files"]:
        assert (WS / f["path"]).exists()
