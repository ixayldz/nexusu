import time
from fastapi.testclient import TestClient
from app.main import app
from app.core.settings import get_settings
from pathlib import Path

client = TestClient(app)
WS = Path(get_settings().workspace_dir)

def _wait(job_id):
    for _ in range(15):
        r = client.get(f"/jobs/{job_id}").json()
        if r["status"] == "finished":
            return r
        time.sleep(0.2)
    raise AssertionError("timeout")

def test_tester_dynamic_import():
    # önce build
    bres = client.post("/tasks/build", json={"steps": ["x"]}).json()
    b_final = _wait(bres["job_id"])
    artifacts = [f["path"] for f in b_final["result"]["files"]]

    # sonra test
    tres = client.post("/tasks/test", json={"artifacts": artifacts}).json()
    t_final = _wait(tres["job_id"])

    assert t_final["result"]["passed"] is True
    assert t_final["result"]["score"] >= 8
