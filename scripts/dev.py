"""Development supervisor. Production OS service registration is not implemented."""

import argparse
import json
import os
import secrets
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
SESSION = RUNTIME / "session.json"


def protect():
    RUNTIME.mkdir(exist_ok=True, mode=0o700)
    if os.name == "nt":
        user = subprocess.check_output(["whoami"], text=True).strip()
        subprocess.run(
            ["icacls", str(RUNTIME), "/inheritance:r", "/grant:r", f"{user}:(OI)(CI)F"],
            check=True,
            capture_output=True,
        )
        # Codex may execute as an isolated account; keep the interactive owner able to connect.
        interactive = os.environ.get("USERDOMAIN", "") + "\\" + os.environ.get("USERNAME", "")
        if interactive.strip("\\") and interactive.lower() != user.lower():
            subprocess.run(
                ["icacls", str(RUNTIME), "/grant", f"{interactive}:(OI)(CI)F"],
                check=True,
                capture_output=True,
            )
    else:
        RUNTIME.chmod(0o700)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")
    path.chmod(0o600)


def healthy(config):
    try:
        request = Request(
            config["url"] + "/tasks", headers={"Authorization": "Bearer " + config["desktop_token"]}
        )
        with urlopen(request, timeout=1) as response:
            return response.status == 200
    except OSError:
        return False


def host():
    protect()
    # OS releases this exclusive lock after crashes, unlike a PID-only lockfile.
    with (RUNTIME / "host.lock").open("a+b") as lock:
        lock.seek(0)
        if os.name == "nt":
            import msvcrt

            if lock.read(1) == b"":
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                return
        else:
            import fcntl

            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return
        from autumn_control.migrate import migrate

        # Fixed for this development workspace; isolated by exclusive host lock.
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        config = {
            "url": f"http://127.0.0.1:{port}",
            "mode": "personal",
            "workspace": "personal",
            "desktop_token": secrets.token_urlsafe(32),
            "edge_token": secrets.token_urlsafe(32),
            "pid": os.getpid(),
        }
        db_url = f"sqlite:///{RUNTIME / 'autumn.sqlite'}"
        migrate(db_url)
        env = {
            **os.environ,
            "AUTUMN_MODE": "personal",
            "AUTUMN_WORKSPACE": "personal",
            "AUTUMN_DATABASE_URL": db_url,
            "AUTUMN_DESKTOP_TOKEN": config["desktop_token"],
            "AUTUMN_EDGE_TOKEN": config["edge_token"],
            "AUTUMN_API_URL": config["url"],
            "AUTUMN_EDGE_JOURNAL": str(RUNTIME / "edge.sqlite"),
        }
        specs = {
            "api": [
                "uvicorn",
                "autumn_api.main:create_app",
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            "worker": ["autumn_worker.main"],
            "edge": ["autumn_edge.main"],
        }
        children = {}
        logs = {}
        attempts = {name: 0 for name in specs}
        stopping = False

        def stop_signal(*_):
            nonlocal stopping
            stopping = True

        signal.signal(signal.SIGTERM, stop_signal)
        signal.signal(signal.SIGINT, stop_signal)
        (RUNTIME / "stop").unlink(missing_ok=True)
        write_json(SESSION, config)
        try:
            while not stopping and not (RUNTIME / "stop").exists():
                for name, args in specs.items():
                    previous = children.get(name)
                    if previous is not None and previous.poll() is None:
                        continue
                    if name == "edge" and not healthy(config):
                        continue
                    if attempts[name] >= 5:
                        raise RuntimeError(f"{name} exited repeatedly; inspect {name}.log")
                    if name in logs:
                        logs[name].close()
                    logs[name] = (RUNTIME / f"{name}.log").open("a", encoding="utf-8")
                    children[name] = subprocess.Popen(
                        [sys.executable, "-m", *args],
                        cwd=ROOT,
                        env=env,
                        stdout=logs[name],
                        stderr=subprocess.STDOUT,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                    )
                    attempts[name] += 1
                    write_json(
                        RUNTIME / "processes.json",
                        {
                            key: {"pid": process.pid, "exit_code": process.poll()}
                            for key, process in children.items()
                        },
                    )
                time.sleep(0.3)
        finally:
            for child in children.values():
                if child.poll() is None:
                    child.terminate()
            for child in children.values():
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
            for log in logs.values():
                log.close()
            SESSION.unlink(missing_ok=True)
            (RUNTIME / "stop").unlink(missing_ok=True)


def start():
    protect()
    if SESSION.exists() and healthy(json.loads(SESSION.read_text())):
        print("Backend already running. Session: .runtime/session.json")
        return
    log = (RUNTIME / "host.log").open("a", encoding="utf-8")
    subprocess.Popen(
        [sys.executable, __file__, "host"],
        cwd=ROOT,
        stdout=log,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        creationflags=(subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
        if os.name == "nt"
        else 0,
        start_new_session=os.name != "nt",
    )
    log.close()
    for _ in range(100):
        if SESSION.exists() and healthy(json.loads(SESSION.read_text())):
            print("Backend ready. Session: .runtime/session.json")
            return
        time.sleep(0.2)
    raise SystemExit("Backend failed to start; inspect .runtime/host.log and api.log")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["start", "stop", "status", "host"])
    args = parser.parse_args()
    if args.command == "host":
        host()
    elif args.command == "start":
        start()
    elif args.command == "stop":
        if SESSION.exists():
            (RUNTIME / "stop").touch()
            for _ in range(100):
                if not SESSION.exists():
                    break
                time.sleep(0.2)
            else:
                raise SystemExit("Shutdown incomplete; inspect runtime logs")
        print("Backend stopped")
    else:
        print(
            "running"
            if SESSION.exists() and healthy(json.loads(SESSION.read_text()))
            else "stopped"
        )
