# Validation plan

English | [简体中文](../../zh-CN/engineering/validation.md)

This document owns engineering test layers, fault injection, and release checks. The [functional specification](../product/functional-spec.md) owns business acceptance; [bootstrap](bootstrap.md) owns initialization gates. No application execution results exist; all checks remain pending.

## Tests, observability, and performance

- Business: pytest for kits, quantity transitions, repair acceptance, process approval, model changes, resource scope, and accepted deficits.
- Adapters: shared interface contracts for Fake/real tools; fixed Orca fixtures for inputs, inheritance, warnings, parsing, cancellation.
- Data: personal SQLite quantity transactions/short-transaction contention/queue/checkpoint/backups; real enterprise PostgreSQL concurrency/leases/outbox/RLS/migrations. Neither substitutes for the other.
- Devices: Fake fault injection for starts with lost receipts, duplicates, external occupancy, stale observations, uncleared beds, failover.
- Desktop: Vitest/Testing Library for UI/pure logic, Playwright for critical Electron flows, plus IPC origin/schema/file scope/external links.
- 3D: fixed dimensions, coordinates, units, multi-object fixtures. Preview screenshots do not prove manufacturing geometry or accepted physical quality.
- Operations: separately fail local queue/enterprise broker; restart API/worker/edge. Closing, sleep, disconnection, model failure, and storage failure stay traceable; unknown device results never trigger another start.
- Both modes: shared business/agent contracts, clean-machine personal installation, enterprise authorization, workspace switching, credential isolation, explicit migration; see deployment checks.

Structured logs/OpenTelemetry correlate organization/order/task/run/slice/job/action IDs and record calls, retries, latency, engine versions, and provider-reported usage. Date/version cost configuration and label estimates; exclude sensitive files/device keys from telemetry.

Measure limits against fixtures: model bytes/faces, first preview frame/window response, slicing concurrency/memory, event replay, transfer, observation latency. No tested capacity/quality promises exist yet.

## Complete delivery acceptance

- Install personal mode on clean Windows without Python/Node/Docker/PostgreSQL/Redis. Configure model connection and complete order, real slicing comparison, history; runtime dependencies install offline.
- Pass shared business/agent scenarios in both modes using identical fixtures/Fake models/tools. Evaluate real models by evidence/constraints, not exact wording.
- Test transactions/quantities/migrations/concurrency/recovery/backups separately on SQLite/PostgreSQL; test duplicates/crashes/leases/cancellation separately for local queue/Celery.
- Preserve traceable tasks across closure/desktop exit/host crash/sleep/disconnection/model API failures; generic retries never repeat device starts.
- Verify enterprise authorization/revocation/checkpoint/file/event isolation and personal credential/local endpoint/workspace isolation.
- Mode switching does not mix events/leak keys/automatically migrate data/compete for devices; export/import retains references/evidence and reviews approvals.
- Exercise personal install/uninstall, enterprise deployment, signed updates, database/checkpoint upgrades, backup/restore; defer incompatible updates during in-flight actions.

Related: [architecture](../architecture/overview.md), [delivery](delivery-plan.md), [dual-mode decision](../adr/0002-dual-mode-monorepo.md).

## Requirements traceability

Acceptance records cite R-xx requirements, F-xx features, B-xx bootstrap gates, mode, fixture, result, and evidence. R-01/F-01/F-02 map to clean installation/model setup; R-03/F-05 to shared agents; R-06/F-09/F-10 to quantities/kits; R-07/F-05/B-07 to interruption/recovery; R-08/F-11/F-12 to switching/migration/access. Add complete automated cases during implementation; no passing result is claimed.
