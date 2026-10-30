# Feature delivery plan

English | [简体中文](../../zh-CN/engineering/delivery-plan.md)

This document owns implementation order, dependencies, and incremental acceptance. The [functional specification](../product/functional-spec.md) defines complete capabilities; [architecture](../architecture/overview.md) and [repository structure](../architecture/repository.md) define engineering organization. Phases do not introduce temporary layouts or separate business implementations for the two modes. Personal-mode bootstrap exists; [development setup](getting-started.md) records the partial initialization gates. Product phases remain pending.

## Development rules

- **One repository, fixed projects.** Four applications/three packages are directory-separated; branches serve development/releases. API/worker share rules; edge connects by protocol without importing business core.
- **Real tools first.** Prove Orca can slice fixtures before giving agents that capability.
- **Inference has evidence.** Geometry yields dimensions, slicing yields estimates, connectors yield device status, inspections yield quality.
- **Separate estimates, observations, hypotheses, approvals.** Recommendations are not validated processes; hypotheses are not established causes.
- **Authorization accompanies data/actions.** Organizational administration can grow later; file/credential/device scope starts immediately.
- **Preserve originals/history.** Trace models, effective configuration, G-code, measurements, approvals.
- **Physical actions differ from retries.** Re-slicing and restarting a printer have different conditions; unknown external outcomes require reconciliation.
- **Cumulative acceptance.** Test added behavior and rerun the prior order workflow.
- **Complete structure, feature-based acceptance.** Follow [repository structure](../architecture/repository.md); profiles/adapters distinguish modes, without temporary directories/product duplication. Documented trees are not implementation.

## Overall sequence

| Phase | Added capability | Actual outcome |
| --- | --- | --- |
| Bootstrap | Four applications, two modes, protocols, persistence, fixtures | Pass B-01 through B-08 |
| 1 | Local Orca adapter | Slice a real model and preserve results |
| 2 | Controlled single agent/candidate comparison | Compare a few actual slicing alternatives |
| 3 | Electron/accounts/durable tasks/files | Submit work, observe progress/history |
| 4 | First articles/physical inspection | Advance candidates into real inspection results |
| 5 | Process iteration/knowledge/approval | Improve by experiments and retain applicable processes |
| 6 | Multiple roles/long-task recovery | Divide investigations and resume interruptions |
| 7 | One device ecosystem | Execute authorized jobs after readiness |
| 8 | Batches/materials/planning | Organize a small-batch order with validated processes |
| 9 | Incidents/reprints/kit acceptance | Handle failures/rework/revisions and reconcile deficits |
| 10 | Enterprise governance/reliable execution | Collaboration, approvals, audit, operations |
| 11 | Evaluation/deployment/review | Deploy cleanly and validate recovery/business results |

Initially focus on FDM, one testable device/nozzle/material set, and one functional part class. Validate additional materials/devices/multicolor/other processes separately.

## Bootstrap gate

Before feature delivery, pass [bootstrap](bootstrap.md) application/mode/protocol connectivity. The former phase-0 CLI/fixtures are one part, not a replacement for B-01 through B-08.

## Phase 1: connect real Orca slicing

**Reuse:** orders, models, devices, profiles.

**Add:** `SlicerGateway`, Orca execution adapter, results/configuration snapshots.

### Changes

1. Select a runnable OrcaSlicer binary, record version/provenance; source version is not installed-binary version.
2. Inspect its actual help and verify one known-sliceable model/configuration/output.
3. Encapsulate configuration, model checks, slicing, result reading; implement capabilities needed by the fixture first.
4. Preserve input, full effective configuration, engine version, outputs, exit status, warnings, elapsed time in a separate task directory.
5. Validate inheritance and printer/material compatibility; do not assume CLI syntax is identical across versions.
6. If structured statistics are unavailable, use tested parsing with provenance/units; missing fields remain unknown.
7. Pass structured subprocess arguments; bound directories/resources/time/files.
8. Save computable dimensions; do not claim unimplemented thin-wall/support/strength analysis.

### Model integrity and repair

Produce a report before deciding whether slicing may proceed. Every check reports checked, issue found, unknown, or unsupported:

| Level | Checks | Handling |
| --- | --- | --- |
| Reading | Parse failure, empty model, invalid/missing objects | Block and explain file/reason |
| Mesh integrity | Holes, non-manifold edges, degeneracy, normals, intersections | Actual geometry tools report location/count/limitations |
| Structure | Disconnected shells, parts, stray fragments | Compare expected structure; separated parts are not automatically defects |
| Dimensions/device | Units, scaling, bounds, build volume | Confirm units, block incompatible devices |
| Process risks | Thin walls, overhangs, supports, critical surfaces | Only implemented algorithms/slicing evidence; mesh pass does not prove printability |

Controlled `GeometryGateway` repair lets agents explain reports/propose/call repairs. Initially implement reading, dimensions, supported mesh checks; mark other checks unsupported.

Preserve originals and create `ModelRevision` for repairs with tool/version/options/before-after defects/geometry differences. Reinspect; changes to surfaces/dimensions/parts/fit need model-owner acceptance before slicing. Preserve failure reasons and request human handling when unreliable.

Target command:

```powershell
uv run --package autumn-api python -m autumn_api.cli slice --order fixtures/orders/bracket-50-sets.json --candidate baseline
```

### Cumulative acceptance

- [ ] Actual model sliced; target Orca opens output.
- [ ] Time/material estimates trace to engine configuration/files.
- [ ] Fixed inputs/effective settings give comparable repeatable results; differences recorded.
- [ ] Timeout/invalid model/incompatible configuration/error exits tested or reproducible.
- [ ] Supported hole/topology checks verified; unsupported is not passed.
- [ ] Repairs preserve revisions; unaccepted changes cannot enter slicing.
- [ ] Generate files only; no real printing.

## Phase 2: single-agent candidate comparison

**Reuse:** same Orca adapter/results.

**Add:** model client, controlled tool loop, candidate plan/comparison report.

### Changes

1. Common configuration/provider adapters, Fake and real model modes.
2. Tools for order reading, checks, repair proposals/controlled repair, profiles, candidates, slicing, results; retain phase-1 acceptance rules.
3. Propose 2–3 candidates from contact/fit/material/deadline requirements, changing a small verified parameter set initially.
4. Shared control-plane validates names/types/ranges/compatibility/combinations in both modes.
5. Compare only after real slicing; show parameter differences, estimates, warnings, limits, required trials.
6. Bound steps/candidates/subprocess concurrency/time/cost.
7. Retain CLI; `analyze-order` submits/observes tasks. The current worker still orchestrates inference/tools; CLI does not create another agent runtime.

### Cumulative acceptance

- [ ] Compare fixed-order candidates with actual numbers.
- [ ] Show speed/material/surface tradeoffs rather than fictitious global optimum.
- [ ] Fake model reproducibly verifies tools; real model failure never becomes simulated success.
- [ ] Reject nonexistent tools, out-of-range parameters, nonexistent results.
- [ ] Distinguish estimates from required physical trials.

## Phase 3: complete the persistent Electron business workbench

**Reuse:** order services, agent runtime, slicing tools.

**Add:** full tasks/model/artifact/history pages on the connected dual-mode desktop/identity foundation; reuse bootstrap connectivity.

### Changes

1. Personal/enterprise first-use choices. Personal owner/protected local keys; enterprise OIDC/resource scope with development identity disabled in production.
2. Shared SQLAlchemy models/Alembic; SQLite personal/PostgreSQL enterprise. Test transactions/migrations separately; journals/checkpoints remain independent.
3. Create/query tasks, results, events, files; return task IDs immediately for long work.
4. Local SQLite durable worker or enterprise Linux Celery/Redis/PostgreSQL outbox, same run/idempotency. Edge runs Orca. Persist SSE through Main to renderer; authenticate loopback API.
5. Order input, model preview, candidate comparison, progress, slice artifacts/history.
6. Authorize upload/preview/download/events; imports stay within workspace.
7. Show input/configuration/engine versions, warnings, tool errors.
8. Named validated main/preload/renderer IPC; renderer holds no device credentials or direct Python/Orca launch capability.
9. electron-vite + React/TypeScript + Three.js/R3F; Windows NSIS via electron-builder, managed Python/runtime dependencies. Check personal connection, enterprise login, imports, packaged paths; users need no uv/pnpm.

### Cumulative acceptance

- [ ] Existing candidate comparison works in Electron; CLI retained.
- [ ] Reopening restores history; reconnection does not duplicate slices.
- [ ] Authorized artifact download; guessed IDs cannot cross spaces.
- [ ] Mark abnormal executions explicitly; automatic recovery is not yet claimed here.
- [ ] Actual installer starts; restrict invalid IPC, unauthorized files, arbitrary external execution.
- [ ] Closing windows does not cancel independent background/edge work.
- [ ] Clean Windows needs no development tools/database/Redis; model setup completes the existing workflow.
- [ ] Test same scenario on both backends; switching never mixes data/credentials/events/device control.

## Phase 4: first articles and physical inspection

**Reuse:** candidates, slicing, orders, workbench.

**Add:** trial plans, human execution records, criteria/status.

### Changes

1. Create Trial from candidate, recording goal/device/material/nozzle/file/checks.
2. Operators initially use existing Orca/device UI and enter actual jobs/results; no remote-control requirement yet.
3. Photos, dimensions, fit feedback, surfaces, failures, attachments.
4. Mark measured/unmeasured/unknown/not applicable with person/time.
5. Authorized people confirm; photos cannot fabricate caliper readings/fit.
6. Distinguish print complete, pending inspection, pass, fail, missing information.

### Cumulative acceptance

- [ ] Trial/real inspection link to candidate/slice/configuration.
- [ ] Tight clips retain failure/evidence and cannot enter batch approval.
- [ ] No measurements means unknown/pending.
- [ ] Repeated uploads do not increase accepted quantities twice.
- [ ] UI labels simulated and actual physical records.

## Phase 5: experiments and validated revisions

**Reuse:** first-article issues, measurements, configurations, slicing.

**Add:** hypotheses, controlled experiments, retrieval, approval.

### Changes

1. Organize facts, possible causes, missing information, next checks.
2. Ingest selected Orca/device/filament documentation and trial history with sources/versions/applicability.
3. Explainable experiments vary few factors rather than many arbitrary parameters.
4. Reuse actual supported temperature/PA/flow/retraction procedures; no assumed universal calibration CLI.
5. Compare real measurements/fit; support/refute hypotheses and leave insufficient evidence pending.
6. Approval creates `ValidatedProcess` fixing model/configuration/engine/device/material/evidence.
7. Changed model/nozzle/device/material triggers policy-defined review/revalidation.

### Cumulative acceptance

- [ ] Evidence-backed experiment continues first-article issue and retains differences.
- [ ] Separate documentary suggestions/validated conclusions; history is not current fact.
- [ ] Failed/incompletely checked processes cannot become approved.
- [ ] Edits preserve approved versions; revocation/reapproval retain history.
- [ ] Retrieval respects current user scope.

## Phase 6: delegated roles and long-task recovery

**Reuse:** tools, experiments, knowledge, processes.

**Add:** plans, controlled delegation, persistent execution/waits.

### Changes

1. Delegate requirements, geometry, processes, experiments, review as needed.
2. Explicit inputs/tools/budgets/dependencies/evidence; child scope cannot exceed parent.
3. Parallel independent investigations, coordinated writes; simple queries use one agent.
4. Selected graph runtime handles plans/branches/return/wait/cancel/recovery with existing business interfaces.
5. Shared roles/tools/graph versions; SQLite/PostgreSQL checkpoints. Correlate tasks/steps/events and reconcile business idempotency, without assumed checkpoint/business atomicity.
6. Separate slicing/model retries, human trials, device-action policy.
7. New acceptance information invalidates affected candidates/trials/approvals, not unrelated work.

### Cumulative acceptance

- [ ] Real delegation/failures/evidence/summary visible; verify child completion claims.
- [ ] Bound review/delegation attempts, concurrency, budgets.
- [ ] Restart resumes the same task after saved execution points.
- [ ] Physical-measurement waits survive restart and resume.
- [ ] Unknown external outcomes are not blindly resent.

## Phase 7: one verified device ecosystem

**Reuse:** validated processes, task permissions, execution records.

**Add:** `PrinterGateway`, observations, action preview/reconciliation.

### Changes

1. Select hardware/backend; verify read/upload/start/pause/cancel support separately.
2. Read-only first, showing online/busy/fault/unknown capabilities.
3. Separate upload/start actions; check approved process, machine, nozzle, material, file hash.
4. Operator confirms bed/load/readiness; approval fixes job/revision.
5. Reread status before start against intervening occupancy.
6. Idempotency/result queries; timeout is unknown, not assumed failure/resend.
7. Preserve raw/normalized events; shared model names do not imply full compatibility.

### Three print-submission modes

| Mode | User intent | Record |
| --- | --- | --- |
| Upload only | Send accepted slice for later manual start | Device/remote file/upload outcome; not started |
| Queue | Hand work to a queue-capable backend | Queue ID/wait conditions/status; no assumed device occupancy |
| Upload and start | Immediate execution after readiness/authorization | Upload/start request/actual response/job identity |

Show only verified adapter modes. Continue observations/progress and supported pause/cancel/resume. Distinguish sent requests/effective actions; investigate unknowns.

### Cumulative acceptance

- [ ] Traceable authorized test job matches approved file/revision.
- [ ] Block busy devices, wrong material/nozzle, missing readiness.
- [ ] Upload is not print success; read back actual outcomes.
- [ ] Repeated clicks/timeouts/recovery do not blindly restart.
- [ ] Completion enters removal/inspection pending; confirm bed clearance separately.

## Phase 8: small-batch production

**Reuse:** fixed order, process versions, devices/materials.

**Add:** batches, capacity/material planning, board.

### Changes

1. Calculate demand from lines/kits/first-article allocation/accepted quantities.
2. Split into batches/plates with parts/counts/process/device.
3. Plan around compatibility, loaded materials, availability, clearance/finishing resources.
4. Preserve deadline assumptions/uncertainty; no invented precise yield without actual failure data.
5. Show preparation/ready/printing/removal/inspection/accepted/incident states.
6. Other machines/material changes check applicability and return to trials if needed.
7. Record actual output/consumption/time separately; estimates do not overwrite facts.

### Cumulative acceptance

- [ ] Split the same 50-kit order into traceable batches.
- [ ] Material shortages/occupancy/no staffing explain blocked plans.
- [ ] Uninspected planned counts are not accepted stock.
- [ ] Changed applicability cannot silently reuse old files.
- [ ] Trace every plate's order/configuration/device/material.

## Phase 9: incidents, reprints, revisions, and kits

**Reuse:** batches, device records, inspections, quantities.

**Add:** incident cases, deficits, rework/reprints, delivery state.

### Changes

1. Human/verified-monitoring incidents link photos/logs/original job/scope.
2. Vision anomalies remain observations/hypotheses until checked.
3. Classify physical parts pending/usable/rework/scrap with provenance/reasons.
4. Reprint actual per-part accepted deficits; distinguish new production from original retries.
5. Model revision flags affected slices/processes/plans/old parts for responsible-person review.
6. Reconcile rework/reinspection/revocation without duplicate accounting.
7. Require 50 accepted bases/100 clips before kit checks, then finishing/packaging/handover.

### Cumulative acceptance

- [ ] Partial plate failure preserves usable quantities and fills deficits.
- [ ] Wrong part ratios remain incomplete despite equal total counts.
- [ ] Revisions identify affected objects; old parts do not impersonate new accepted parts.
- [ ] Duplicate monitoring/inspection/approval does not add output/redispatch.
- [ ] Delivery traces models/processes/batches/materials/inspection.

## Phase 10: governance and reliable execution

**Reuse:** authorization, approvals, recovery, audit links.

**Add:** enterprise role/identity/operations/resource UI.

### Changes

1. Operator/process/inspection/order/admin permissions; organizational approval policy.
2. Production identity/optional SSO; disable development identity.
3. PostgreSQL constraints/transactions/migrations and record relationships.
4. Operate/negotiate/recover enterprise workers, personal host, native edge; API submits/queries/controls, windows do not own task lifetime.
5. Reliable dispatch/claims/leases/timeouts/concurrency; reconcile external actions before recovery.
6. Restrict models/tools/resources/concurrency/cost; adapters hold credentials, not model messages/logs.
7. Audit process approval/model replacement/inspection correction/actions/reprints/permissions.
8. Multi-organization isolation covers database/files/retrieval/cache/checkpoints/logs/credentials.

### Cumulative acceptance

- [ ] Users access/operate only authorized orders/processes/devices.
- [ ] Revocation affects later access/approval/execution.
- [ ] API/worker restart independently without permanently losing work.
- [ ] Idempotent leases/redelivery prevent repeated physical operations.
- [ ] Trace decisions/outcomes by order/person/process/device.

## Phase 11: evaluation, deployment, delivery review

**Reuse:** complete order application and earlier checks.

**Add:** fixed evaluations, CI, deployment, recovery, metrics.

### Changes

1. Fixed normal/unknown-unit/broken/incompatible/tradeoff fixtures.
2. Fixed trial failures/material shortages/busy/unknown-start/partial failure/revision/incomplete-kit events.
3. Fake automation, real Orca, device trials, physical inspection keep distinct evidence.
4. Evaluate tool facts/files/configuration/state/quantity/citations, not exact model wording.
5. Track estimate deviations/trial counts/scrap/rework/deficit accuracy/duplicate actions/human effort.
6. Separate materials/machine time/labor/finishing/waste; avoid duplicate engine cost components.
7. Document deployment/migrations/storage/engine/profile backups/credentials/health/rollback.
8. Exercise personal offline dependencies/SQLite restore, enterprise/PostgreSQL restore, sleep/crashes/offline devices. Explicit export/import excludes credentials/active tasks/unreviewed production authority.
9. Windows NSIS/signatures/electron-updater/server-edge compatibility; do not replace execution during active jobs.

### Final cumulative acceptance

- [ ] README guides clean setup and distinguishes demo/slicing/device modes.
- [ ] Same order reaches import/trials/batches/incidents/reprints/kits/delivery.
- [ ] Key conclusions trace tools/measurements/people.
- [ ] Approved applicability/version and changed-condition review are visible.
- [ ] Software/device/physical quality/order delivery remain distinct and linked.
- [ ] Roles/approvals/audit/recovery/external reconciliation work.
- [ ] Automated coverage for quantities/revisions/duplicate events/actions.
- [ ] Actual fixture/physical records; unknown/unvalidated is not success.
- [ ] Backup/restore/rollback exercised, remaining limitations documented.
- [ ] Personal install-and-use and enterprise deployment separately accepted; shared agent contracts, differences limited to capability/data/permissions/collaboration.

## Keep each increment integrated

1. Run the previous order path first.
2. Pick a concrete increment, such as linking a new candidate after trial failure.
3. Connect data/tools/authorization/tasks/pages.
4. Test new/old paths, especially revisions/quantities/physical actions.
5. Update actual commands/configuration/limitations/demos in README.
6. Leave a runnable commit before the next increment.

At each phase ask: where is the order, where is evidence, who must act, what changes require review, and can the next session continue?

All phases deliver one application organized around actual slicing, physical validation, and business outcomes.
