import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from autumn_api.main import create_app
from autumn_contracts import Receipt
from autumn_control.infrastructure import Store
from autumn_control.migrate import migrate
from autumn_control.orders import show_order
from autumn_control.settings import Settings
from autumn_edge.main import run_once
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def environment(tmp_path):
    url = f"sqlite:///{tmp_path / 'test.sqlite'}"
    settings = Settings("personal", "owner", url, "d" * 32, "e" * 32)
    with TestClient(create_app(settings)) as api:
        yield settings, api


def desktop(api):
    api.headers["Authorization"] = "Bearer " + "d" * 32
    return api


def test_complete_roundtrip_and_persistence(environment):
    settings, api = environment
    desktop(api)
    first = api.post("/tasks/diagnostic", json={"idempotency_key": "stable"}).json()
    assert api.post("/tasks/diagnostic", json={"idempotency_key": "stable"}).json() == first
    store = Store(settings.database_url)
    store.dispatch("owner")
    api.headers["Authorization"] = "Bearer " + "e" * 32
    with sqlite3.connect(":memory:") as journal:
        assert run_once(api, "test-edge", journal)
        assert not run_once(api, "test-edge", journal)
    desktop(api)
    task = api.get(f"/tasks/{first['id']}").json()
    assert task["status"] == "succeeded" and task["result"]["simulated"]
    events = api.get(f"/tasks/{first['id']}/events").json()
    assert [event["kind"] for event in events] == [
        "queued",
        "fake_model_completed",
        "fake_tool_completed",
    ]
    assert api.get(f"/tasks/{first['id']}/events?after={events[-1]['sequence']}").json() == []
    with TestClient(create_app(settings)) as reopened:
        assert desktop(reopened).get(f"/tasks/{first['id']}").json() == task
    store.engine.dispose()


def test_credentials_versions_and_origins(environment):
    _, api = environment
    assert api.get("/tasks").status_code == 401
    desktop(api)
    assert api.post("/edge/register", json={"edge_id": "a"}).status_code == 401
    assert api.get("/tasks", headers={"Origin": "https://evil.example"}).status_code == 403
    api.headers["Authorization"] = "Bearer " + "e" * 32
    assert api.get("/tasks").status_code == 401
    assert (
        api.post("/edge/register", json={"edge_id": "a", "protocol_version": "2"}).status_code
        == 422
    )
    assert api.post("/edge/unregistered/claim").status_code == 403


def test_concurrent_submission_and_dispatch(environment):
    settings, _ = environment
    store = Store(settings.database_url)
    with ThreadPoolExecutor(4) as pool:
        tasks = list(pool.map(lambda _: store.submit("owner", "same"), range(8)))
        list(pool.map(lambda _: store.dispatch("owner"), range(8)))
    assert len({task.id for task in tasks}) == 1
    assert len(store.task_events("owner", tasks[0].id)) == 2
    with pytest.raises(KeyError):
        store.get("other", tasks[0].id)
    store.engine.dispose()


def test_receipt_idempotency_and_lease_scope(environment):
    settings, _ = environment
    store = Store(settings.database_url)
    task = store.submit("owner", "receipt")
    store.dispatch("owner")
    store.register("owner", "a")
    store.register("owner", "b")
    command = store.claim("owner", "a")
    assert store.claim("owner", "b") is None
    with pytest.raises(PermissionError):
        store.complete("owner", "b", command.id, command.lease_token, Receipt(message="fake"))
    for _ in range(2):
        store.complete("owner", "a", command.id, command.lease_token, Receipt(message="fake"))
    assert len(store.task_events("owner", task.id)) == 3
    store.engine.dispose()


def test_migration_is_repeatable(tmp_path):
    url = f"sqlite:///{tmp_path / 'migration.sqlite'}"
    migrate(url)
    store = Store(url)
    saved = store.submit("owner", "before-upgrade")
    migrate(url)
    assert store.get("owner", saved.id) == saved
    store.engine.dispose()


def test_order_and_invalid_inputs(tmp_path):
    fixture = ROOT / "fixtures/orders/bracket-50-sets.json"
    result = json.loads(show_order(fixture))
    assert [line["required_quantity"] for line in result["lines"]] == [50, 100]
    assert result["missing_information"]
    value = json.loads(fixture.read_text())
    target = tmp_path / "bad.json"
    for change in (
        {"kits": 0},
        {"kits": True},
        {"models": {}},
        {"models": {"base": "missing.stl", "clip": None}},
    ):
        target.write_text(json.dumps({**value, **change}))
        with pytest.raises(ValueError):
            show_order(target)
    with pytest.raises(FileNotFoundError):
        show_order(tmp_path / "absent.json")


def test_invalid_config():
    with pytest.raises(ValueError):
        Settings("enterprise", "a", "sqlite:///bad", "d" * 32, "e" * 32)
    with pytest.raises(ValueError):
        Settings("personal", "a", "sqlite:///bad", "d" * 32, "d" * 32)


@pytest.mark.skipif(
    not __import__("os").getenv("AUTUMN_TEST_POSTGRES"), reason="PostgreSQL service required"
)
def test_postgres_migration_and_queue():
    import os
    from uuid import uuid4

    url = os.environ["AUTUMN_TEST_POSTGRES"]
    migrate(url)
    store = Store(url)
    workspace = str(uuid4())
    task = store.submit(workspace, "postgres")
    store.dispatch(workspace)
    assert store.get(workspace, task.id).status == "waiting_edge"
    store.engine.dispose()
