"""Run against the development supervisor; never output session credentials."""

import json
import subprocess
import sys
import time
from pathlib import Path

import httpx

root = Path(__file__).resolve().parents[1]
config = json.loads((root / ".runtime/session.json").read_text())
with httpx.Client(
    base_url=config["url"], headers={"Authorization": f"Bearer {config['desktop_token']}"}
) as client:
    task = client.post(
        "/tasks/diagnostic", json={"idempotency_key": f"process-{time.time_ns()}"}
    ).json()
    for _ in range(80):
        result = client.get(f"/tasks/{task['id']}").json()
        if result["status"] == "succeeded":
            break
        time.sleep(0.25)
    else:
        raise AssertionError("process chain did not complete")
    assert result["result"]["simulated"]
    subprocess.run([sys.executable, "scripts/dev.py", "start"], cwd=root, check=True)
    assert json.loads((root / ".runtime/session.json").read_text())["pid"] == config["pid"]
    # Killing the API verifies bounded supervisor recovery and traceable worker processes.
    processes = json.loads((root / ".runtime/processes.json").read_text())
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/PID", str(processes["api"]["pid"]), "/F"],
            check=True,
            capture_output=True,
        )
    else:
        import os
        import signal

        os.kill(processes["api"]["pid"], signal.SIGTERM)
    for _ in range(80):
        try:
            response = client.get(f"/tasks/{task['id']}")
            if response.status_code == 200:
                assert response.json() == result
                break
        except httpx.TransportError:
            pass
        time.sleep(0.25)
    else:
        raise AssertionError("API did not recover")
subprocess.run([sys.executable, "scripts/dev.py", "stop"], cwd=root, check=True)
subprocess.run([sys.executable, "scripts/dev.py", "start"], cwd=root, check=True)
restarted = json.loads((root / ".runtime/session.json").read_text())
assert restarted["desktop_token"] != config["desktop_token"]
with httpx.Client(
    base_url=restarted["url"], headers={"Authorization": f"Bearer {restarted['desktop_token']}"}
) as client:
    assert client.get(f"/tasks/{task['id']}").json() == result
print(
    "Independent API/worker/edge, singleton reuse, API crash recovery, host restart and durable result passed"
)
