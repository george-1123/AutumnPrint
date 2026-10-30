# Development workspace

English | [简体中文](../../zh-CN/engineering/getting-started.md)

Engineering bootstrap, 2026-10-30. This is a developer workflow, not an installer. All diagnostics are simulated: no printer, Orca binary, third-party model or real model service is accessed.

## Install and run

Requires Python 3.12, uv 0.13.6, Node 24 (minimum 22.12), pnpm 11.25.0. First installation needs package registry and Electron release access. From the repository root in PowerShell:

```powershell
uv sync --frozen --all-packages
pnpm install --frozen-lockfile
uv run pnpm dev
$env:AUTUMN_SESSION = (Resolve-Path .runtime/session.json).Path
uv run pnpm dev:desktop
```

Click **运行链路诊断**. Expect `queued → waiting_edge → succeeded` and events `queued`, `fake_model_completed`, `fake_tool_completed`. Closing/reopening the desktop replays the same durable task; the Python backend runs independently.

```powershell
uv run python scripts/dev.py status
uv run pnpm dev:stop
uv run --package autumn-api python -m autumn_api.cli show-order --fixture fixtures/orders/bracket-50-sets.json
```

The fixture expands to 50 bases/100 clips. Model references are deliberately absent; units, profiles and acceptance criteria are unconfirmed. Adjacent `provenance.json` documents original synthetic data and simulated device/material inventory.

## Validation

```powershell
uv run pytest -q
uv run ruff check apps packages scripts tests
uv run ruff format --check apps packages scripts tests
uv run pnpm generate
uv run pnpm check
pnpm build
# Backend must be running:
uv run python tests/process_smoke.py
pnpm test:desktop
```

Generation produces OpenAPI, non-HTTP protocol schemas and derived TypeScript types. CI checks drift, dependency boundaries, Windows/Linux, and a separate PostgreSQL service. Remote CI results have not been observed.

The process test deliberately terminates only the API child created by this project's host to verify bounded recovery. The Electron test closes/reopens after submission, checks replay and restricted IPC, and saves `.runtime/desktop.png`.

Local evidence (Windows, 2026-10-30): Python 3.12.14, Node 24.17.0, pnpm 11.25.0, Electron 45.1.0. Pytest: 7 passed/1 PostgreSQL skip; Ruff, boundary check, TypeScript and desktop build passed. Independent process roundtrip, API crash recovery, whole-host restart with credential rotation, and actual Electron button/close/reopen/IPC tests passed. The Electron runtime was fetched from its official GitHub release and checked against the SHA256 supplied in the npm package. TestClient currently emits an upstream Starlette/httpx deprecation warning; it does not affect these passing results.

The developer host uses an OS file lock, independent API/worker/edge children, explicit stop requests, and at most five starts per child per host lifetime. Logs: `.runtime/{host,api,worker,edge}.log`. Database and edge receipts survive restarts; restarting the host rotates credentials, requiring the desktop to reconnect.

`.runtime/` is ignored and restricted to the executing/interactive user on Windows (0700 directory/0600 session on POSIX). Discovery holds independent random desktop/edge bearer credentials, never exposed to renderer. API checks credentials/origins and binds loopback. This is a developer mechanism; OS keychain storage for real model keys is not implemented. Development data intentionally stays under `.runtime/` for inspection; production per-user managed services and storage remain pending.

## Enterprise and acceptance limits

Shared persistence includes SQLite/PostgreSQL Alembic migrations. Enterprise settings reject SQLite and missing Redis. Optional enterprise dependencies are separate:

```powershell
uv sync --frozen --all-packages --all-extras
# Set AUTUMN_MODE=enterprise, AUTUMN_WORKSPACE, AUTUMN_DATABASE_URL,
# AUTUMN_BROKER_URL and independent AUTUMN_DESKTOP_TOKEN / AUTUMN_EDGE_TOKEN.
uv run python -c "from autumn_control.migrate import migrate; from autumn_control.settings import Settings; migrate(Settings.from_env().database_url)"
uv run uvicorn autumn_api.main:create_app --factory --host 127.0.0.1
# Linux worker; beat wakes the durable task-row outbox:
uv run celery -A autumn_worker.server:app worker -B
```

OIDC/RBAC and multi-user sessions are absent: this entry is development infrastructure. Do not expose it as a production enterprise service. `AUTUMN_TEST_POSTGRES` enables PostgreSQL tests against an isolated test database, creating tables/test rows; never use production data. No PostgreSQL/Redis service was available locally, so enterprise execution remains unverified.

| Gate | Implemented | Full gate still requires |
| --- | --- | --- |
| B-01 | Four apps/three packages, locks, boundary checks | Independent release artifacts |
| B-02 | Configuration validation, separate credentials, explicit Fake | UI mode switching, OS credential store, enterprise identity |
| B-03 | SQLite migration, durable tasks/events, edge journal; PostgreSQL adapter | PostgreSQL acceptance; Agent checkpoints |
| B-04 | Local process roundtrip; durable outbox/Celery entry | Redis/Celery recovery and enterprise end-to-end test |
| B-05 | Version checks, registration, leased claims, journaled/idempotent receipts | Per-edge credentials, heartbeat, real tools |
| B-06 | Electron/React, generated types, validated IPC, cursor polling | SSE, UI connection/mode selection, generated route client |
| B-07 | Single host, background survives closure, API recovery | OS-managed host recovery, real-action graceful shutdown |
| B-08 | Commands, local checks/build, CI definition | Fresh-machine CI, installer and dual-mode acceptance |

Retries here only apply to Fake tools; physical actions require the separately designed uncertain-result reconciliation protocol.

References: [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/), [FastAPI security](https://fastapi.tiangolo.com/reference/security/), [electron-vite](https://electron-vite.org/guide/), [Electron security](https://www.electronjs.org/docs/latest/tutorial/security/).
