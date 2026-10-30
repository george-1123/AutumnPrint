# Engineering bootstrap

English | [简体中文](../../zh-CN/engineering/bootstrap.md)

Status: personal-mode engineering bootstrap implemented; full dual-mode gates remain open. Verified commands and limits are in [development setup](getting-started.md). This document defines the complete acceptance target; it does not imply every gate passed. See [features](../product/functional-spec.md) and [repository structure](../architecture/repository.md).

## Definition of complete

Prove desktop, API, worker, edge, shared protocols, and databases work together. Passing the order CLI is only one part, not a substitute for process connectivity. Real model keys, printers, and complete business features are not prerequisites for baseline connectivity tests.

## Steps and deliverables

| ID | Work | Reviewable deliverable | Acceptance |
| --- | --- | --- | --- |
| B-01 | Establish workspace | Four apps/three packages, manifests, locks, ignore rules | Packages install/import; static checks detect prohibited dependencies |
| B-02 | Assemble configuration/identity | Personal/enterprise profiles, workspace/credential references, Fake model/device | Invalid configuration fails explicitly; saved keys do not appear in logs/frontend |
| B-03 | Initialize persistence | SQLite/PostgreSQL migrations, durable tasks/events/checkpoint configuration | Create/upgrade each database; business/queue records are durable |
| B-04 | Start API/worker | Health checks, local task entry, enterprise Celery entry, protected endpoint discovery | Diagnostic task executes and reports events; duplicate submission is idempotent |
| B-05 | Connect edge | Registration, claims, Fake execution, results/action receipts | Reject incompatible versions/credentials; complete protocol round trip |
| B-06 | Connect desktop | Main/preload/renderer, generated SDK, mode selection, subscriptions | Submit/observe the diagnostic task in UI; no direct renderer hardware calls |
| B-07 | Verify lifecycle | Singleton/start/stop/close behavior/crash diagnostics | Background survives window closure; reopen replays; abnormal state is traceable |
| B-08 | Fix reproducible entry points | Validated root development/build/check commands and CI | A new development environment completes these steps; add actual commands/expected output with implementation |

## Connectivity scenarios

Personal: desktop → authenticated local API → SQLite durable task → local worker/Fake model → local edge/Fake tool → receipt/events → desktop. Reopening retrieves the same task.

Enterprise: desktop → enterprise test identity/API → PostgreSQL/outbox → Redis/Celery worker → registered edge/Fake tool → durable result/events → desktop. Another unauthorized identity cannot read the task.

These prove engineering integration only. Real Orca, model API compatibility, physical quality, and production installers have separate acceptance; Fake results do not demonstrate real integration.

## Fixtures and CLI

### Order sample and development CLI

**Deliver:** environment, common entry point, fixed business fixture.

### Work in this repository

1. Configure uv and selected Python 3.12; check native library platform support.
2. Configure fixed `apps/{desktop,api,worker,edge}` and `packages/{control-plane,contracts,sdk-ts}` workspaces/scoped dependencies; generate locks after installation validation. CLI lives in `apps/api`, not root `app/`.
3. Add `fixtures/orders/bracket-50-sets.json`, authorized base/clip models, and profile manifest.
4. Add fictitious devices/spools/criteria/expected incidents; no real device connection.
5. Implement `show-order`, displaying 50 bases, 100 clips, and missing information.
6. Document installation, fixture provenance, and usage; ignore keys, local configuration, runtime data, and virtual environments.

Environment initialization:

```powershell
uv venv --python 3.12
```

After implementation and installation, support:

```powershell
uv sync --package autumn-api --extra local --dev
uv run --package autumn-api python -m autumn_api.cli show-order --fixture fixtures/orders/bracket-50-sets.json
uv run pytest
```

### Cumulative acceptance

- [ ] Install/run the common entry point in a clean environment following README.
- [ ] Expand kits into two part demands and display missing information.
- [ ] Explain unknown models, invalid quantities, and missing files.
- [ ] Data-reading tests require no model key or printer.

## Inputs to confirm before implementation

1. First test printer, firmware, nozzle, connection, permitted scope; use Fake until confirmed.
2. Orca binary, actual CLI capabilities, permitted distribution; local 2.5.0-dev source is not an accepted program.
3. Electron/electron-vite/Vite/React/R3F compatibility and Windows installer sample; do not derive untested locks from star counts.
4. Native geometry, subprocess restrictions, OIDC callbacks, OS credential protection, Electron test support on target systems.
5. Supported defects/repairs, first-article criteria, quantity rules, checked with fixtures/operators.

These are explicit implementation inputs. The revision synchronized dual-mode design/docs while retaining prior research; none of the above validations is claimed complete.

## Records and handoff

Record environment, actual commands, outcomes, and diagnostic references for every gate. [Development setup](getting-started.md) distinguishes implemented behavior from enterprise, checkpoint, identity, transport and installer work still required. Directory creation/static documentation checks are not application acceptance.
