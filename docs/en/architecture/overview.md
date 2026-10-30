# Architecture overview

English | [简体中文](../../zh-CN/architecture/overview.md)

Status: product design baseline, organized on 2026-10-30. Personal-mode bootstrap exists; [implementation status](../engineering/getting-started.md) distinguishes current behavior from target architecture. See [requirements](../product/requirements.md) for product goals and the [functional specification](../product/functional-spec.md) for behavior. This document owns modules, technology, data, and interfaces; [runtime](runtime-and-deployment.md), [agents](agent-and-tools.md), and [repository structure](repository.md) own their respective details.

Technology versions and external project information retain the [2026-10-29 research snapshot](../research/technology-selection.md). This reorganization did not recheck releases or demonstrate successful integration tests.

## Decisions and assumptions

Use an **Electron desktop + Python modular control plane + independent edge executor**, with complete personal local and enterprise server configurations. Four applications (desktop, api, worker, edge) and three shared packages (control-plane, contracts, sdk-ts) share one repository. Directories define responsibilities. See [repository structure](repository.md) for directories/dependencies, [runtime](runtime-and-deployment.md) for deployment/lifecycle, and [validation](../engineering/validation.md) for acceptance.

- Target FDM process validation and small-batch production; initially verify one device/nozzle/material combination and the fixed order fixture.
- Electron is the requested primary deliverable, starting with Windows and separately validating macOS/Linux packaging. The renderer does not hold printer credentials.
- Personal installation provides local API/worker, SQLite business records/durable queue/checkpoints, and local files; configuring the model API requires no server or development environment. Enterprise uses server API/Linux workers, PostgreSQL, Celery/Redis, and enterprise identity.
- Both modes share business logic and LangGraph graphs/roles/tools. Agents orchestrate in the selected control plane's worker. Edge executes actual tools/actions without a separate model key; the API URL determines inference location.
- No actual printer inventory has been supplied. Select the first real device adapter from test hardware; do not assume universal Moonraker or OctoPrint support.
- All versions are research/compatibility candidates. Fix actual dependencies through validated lockfiles, image digests, and binary hashes.

## Technology responsibilities

| Layer | Baseline | Purpose and constraints |
| --- | --- | --- |
| Python runtime/dependencies | Supported Python 3.12 patch + uv + uv.lock | Follow the guide; verify native geometry wheels and tool compatibility |
| Desktop frontend | Electron + React 19 + TypeScript + electron-vite + pnpm | Build main/preload/renderer separately; renderer uses Vite without initial SSR |
| Desktop distribution | electron-builder + electron-updater | Validate installers, signatures, channels, installation/recovery; do not combine with Forge as a second primary chain |
| 3D | Three.js + stable React Three Fiber v9 | Models, beds, orientation, inspection markers, candidate comparison |
| UI/data | shadcn/ui, Tailwind, TanStack Query; TanStack Table when needed | Separate query and view state |
| Frontend build runtime | Node.js 24 LTS baseline; upgrade to 26 LTS after toolchain validation | Record build Node separately from Electron's Node/Chromium; use compatible Vite rather than forcing latest |
| Business entry | FastAPI + Pydantic + Uvicorn | Input validation, authorization, commands, queries, SSE, files |
| Persistence | Personal SQLite; enterprise PostgreSQL 18 candidate; SQLAlchemy 2.x + Alembic | Test migrations, transactions, concurrency separately; exclude enterprise psycopg from personal bundles |
| Agents | One LangGraph runtime + validated provider adapters | Small graphs for simple tasks; delegation, branching, waiting, recovery |
| Background execution | Personal durable queue; enterprise Linux Celery + Redis | Shared bounded execution/idempotency/recovery semantics; one backend per workspace; no Windows Celery |
| Edge | Independent Python process + SQLite action journal + restricted subprocesses | Local native execution, identity, claiming, device actions |
| Slicing | Fixed, accepted stable OrcaSlicer binary | Current candidate v2.4.2; 2.5 Alpha/local development for later plugin research |
| Geometry inspection | Trimesh + explicitly scoped checks | Report pass/fail/unknown/unsupported per check |
| Mesh repair | Limited small repairs; isolated PyMeshLab when necessary | Enable only after defect-fixture acceptance; no assumed complex-topology repair |
| Devices | Fake + one real Moonraker or OctoPrint adapter | Select from real devices and publish capability matrix |
| Files | Local ArtifactStore; existing enterprise S3 or evaluated SeaweedFS | Validate S3 without starting a distributed storage cluster |
| Identity | Personal owner/local authentication; enterprise OIDC (Keycloak/existing IdP) + RBAC/resource policy | No enterprise account for personal use; record people/revisions in confirmations; verify enterprise membership/scope |
| Retrieval | Personal SQLite text search; enterprise PostgreSQL full-text search, optional pgvector | Shared authorization/citation semantics, separate retrieval evaluation; no mandatory embedding key/GPU |
| Planning | Deterministic compatibility checks and explainable heuristics; OR-Tools CP-SAT if justified | LLM proposes constraints; code verifies feasibility |
| Materials/monitoring | Local material ledger; optional Spoolman, Obico/Gadget | Explicit single quantity authority and device control ownership |
| Validation | pytest, Vitest, Testing Library, Playwright | Business/tools/Electron windows/IPC/3D tests; physical validation separately |
| Quality/operations | Ruff, type checking, OpenTelemetry, structured logs, Docker Compose, CI | Basic checks from the outset; telemetry backend scales with need |

See the [official Node release table](https://nodejs.org/en/about/previous-releases) and [research](../research/technology-selection.md). Exact patches have not been assembled into an installation-tested dependency set.

## Modules, interfaces, and seams

Build deep modules around business responsibilities: callers learn small stable interfaces, while implementations contain configuration inheritance, process handling, and device differences. Place seams where implementations actually vary: real Orca/Fake, real device/Fake, local/S3 storage. Do not add an abstraction for every class.

| Module | Draft caller interface | Hidden complexity and required guarantees |
| --- | --- | --- |
| Ordering | `create_order`, `revise_requirement`, `get_fulfillment` | Kits, requirement revisions, first-article allocation, change impact, accepted deficits |
| Model Preparation | `inspect`, `propose_repair`, `accept_revision` | Files, units, coverage, repair candidates, geometry differences; no original overwrite |
| Slicing | `submit_slice`, `get_slice_result`, `cancel_slice` | Engine detection, inheritance, isolated directories, resources, parsing, cached receipts |
| Process Validation | `record_trial`, `record_inspection`, `approve_process` | Evidence, applicability, approval revision, changed-condition review |
| Production | `plan_batch`, `propose_action`, `reconcile_action` | Compatibility, occupancy, readiness, approval, single-writer ledger |
| Quality | `classify_output`, `assess_deficit`, `request_reprint` | Pending/accepted/rework/scrap transitions, deduplication, kits/delivery |
| Agent Runtime | `start_run`, `resume_run`, `cancel_run` | Model/graph versions, delegation, tool authorization, budgets, interrupts, leases |
| Knowledge | `ingest`, `search`, `resolve_evidence` | Versions, authorized retrieval, evidence location, corrections |
| Identity & Policy | `resolve_actor`, `authorize` | Membership, roles, resource scope, validity, human/edge identities |
| Artifacts | `put`, `open_authorized`, `describe` | Complete uploads, hashes, immutable objects, derivation, access, collection |

These unimplemented interfaces include ordering, error modes, authorization, and performance constraints, not just function names. Tests exercise the same interfaces; new adapters pass the same contract tests.

Use cases coordinate cross-module transactions; modules do not modify another module's private tables. Atomic business operations use the workspace's single business database (personal SQLite, enterprise PostgreSQL), avoiding unnecessary remote consistency problems.

## Business records and persistence

Personal production uses SQLite, enterprise uses PostgreSQL, and both keep separate SQLite edge action journals. Business storage, agent checkpoints, and edge journals have different lifecycles; copying files does not implicitly migrate active tasks. SQLite uses short transactions, unique constraints, optimistic versions; PostgreSQL may use row locks/RLS. Test migrations, concurrency, recovery separately.

| Record group | Main objects | Consistency requirements |
| --- | --- | --- |
| Identity | organizations, memberships, roles, resource_grants, edge_agents | Recheck current membership/scope after resolving business IDs |
| Demand | orders, order_lines, kit_components, model_revisions | Version models/acceptance; never silently substitute old revisions |
| Tool artifacts | artifacts, profile_snapshots, slice_runs, check_reports | Immutable input/configuration/binary/result links; simulated versus actual results |
| Processes | candidates, trials, inspections, validated_processes | Approvals fix revisions/evidence; changes trigger review |
| Production | batches, print_jobs, device_observations, device_actions | Plans distinct from actions; observations have source timestamps/freshness |
| Quantity | output_lots, quantity_transitions, order_allocations | Reclassification does not add output; allocation cannot exceed available accepted parts |
| Incidents | incidents, reprint_requests, dispositions | Reprints link verified deficits/incidents, not original-action retries |
| Interaction | tasks, agent_runs, steps, task_events, approvals | Optimistic versions, exclusive recovery, fixed approval objects/parameters |
| Execution handoff | outbox, run_leases, edge_commands, action_receipts | Unique business identity, transactional writes, redelivery reconciliation, traceable unknowns |

Use explicit IDs/foreign keys and quantity range checks. Classification transitions and order allocations have unique idempotency keys. Updates require transactions and row locks/optimistic versions rather than model/frontend checks alone.

Example: a plate plans 12 clips and confirms 12: 8 accepted, 2 pending, 2 scrap. Accepting the 2 pending gives 10 accepted and 2 scrap, still 12 total. A duplicate inspection event cannot produce 14. Only allocated, revision-matching, accepted parts reduce order demand.

Use current-state tables plus traceable transitions, without initially adopting whole-system event sourcing.

## Orca, model inspection, and repair

### Immutable inputs and slicing receipts

Fix model revision, model/configuration hashes, effective settings, engine binary/resource versions, machine conditions, and output protocol for each slice. Cache keys also cover orientation/layout, object overrides, preprocessing, and parser version. Cache hits preserve provenance and do not masquerade as new executions.

Use an independent workspace and, where supported, configuration directory per run. Never write global user presets. Adapters explicitly handle inheritance/overrides; do not discard private 3MF settings or mistake them for current machine configuration.

Launch Orca with an argument array; preserve exit code, logs, warnings, artifacts, and version-dependent capability detection. Missing time/material/cost/preview fields remain unknown, never filled from model replies. Pricing checks the engine's cost components before adding labor, finishing, and waste to avoid counting machine time twice.

### Inspection coverage

Use Trimesh for loading and basic geometry/topology facts. Repairs always create candidate revisions.

| Item | Initial agreement |
| --- | --- |
| Readability, empty models, invalid indices, non-finite coordinates | Explicit format/check validation; stop on invalid or excessive inputs |
| Units, bounds, parts, transforms | Preserve sources/object relationships; confirm unknown units |
| Watertightness, winding, degenerate/duplicate faces, edge adjacency | Independent check results; watertight does not exclude every topology defect |
| Normal correction, small-hole repair | Restricted attempts on copies; differences and human confirmation required |
| Complete self-intersection/non-manifold vertex detection, complex-hole repair | Unsupported initially; enable after separate acceptance |
| Thin walls/overhangs/strength/dimensional quality | Dedicated algorithms and physical trials/measurements, not screenshots or successful parsing |

PyMeshLab is an optional isolated complex-inspection/repair backend. Add Manifold only for Boolean operations with valid inputs. Repairs may change dimensions, fit, and intended holes; the model owner must see revision/differences. Escalate unreliable repairs for human handling.

### Execution isolation

Validate archive paths, file types, expanded sizes, objects/faces, and resources. Reject path escape and arbitrary postprocessing scripts. Actual execution environments enforce CPU, memory, duration, network, and filesystem restrictions.

Windows edge execution requires low-privilege identities/file ACLs, process-tree management, and Job Object resource controls. Ordinary subprocess execution or installing Docker Desktop does not create a complete sandbox. Clean up processes, temporary data, and leases after abnormal exit while retaining diagnostics and immutable inputs.

## Files, 3D, and G-code preview

The business database owns file metadata, organization, permissions, hash, object key, length, type, derivation, and state. ArtifactStore holds original models, G-code, photos, and large logs.

- Use managed local directories and authorized references, never constructed arbitrary user paths.
- Make uploads available only after completion/validation; retain cleanup records on failure and collect orphans by retention policy.
- Initially serve authenticated proxy reads; direct upload/download later uses short-lived scoped URLs with explicit revocation limitations before expiry.
- Reuse enterprise S3 first. Evaluate SeaweedFS multipart, Range, checksums, and lifecycle semantics rather than assuming full compatibility.
- Three.js/R3F displays derived models, beds, and issue markers. Trace coordinates, units, and objects back to originals; decimation only affects display.
- Displaying 3MF does not fully reproduce private slicer data. Review start/end G-code, device macros, and postprocessing independently.
- Preview only implemented G-code dialects/layers/travel/extrusion types. Mark unknown macros; no initial promise of Orca-complete preview or machine simulation.
- Parse large files in Web Workers/backend derivation; use suitable BufferGeometry and layered loading. Measure byte/triangle budgets with fixtures.

TanStack Query manages business cache, with resource versions for deduplication/invalidation. Routes/URLs hold filters/selections; React holds local forms. Add Zustand only for actual shared view state, without duplicating the business database.

## Identity, user roles, and agent roles

Personal workspaces create a local owner without enterprise accounts/OIDC, but endpoints, files, and device actions retain explicit identity/authorization and approval people/revisions/evidence. Enterprise OIDC uses Keycloak or an existing IdP. Desktop uses the system browser's authorization-code + PKCE flow with state/nonce, callback, issuer, audience, and validity checks; it is not an OAuth client capable of keeping a confidential secret. The following matrix applies to enterprise mode.

Main manages token lifecycles; renderer receives only necessary identity summaries. Persist credentials using validated OS protection. Electron safeStorage protection differs by platform/backend; retain memory-only sessions and require sign-in if inadequate, rather than saving plaintext. API checks current membership/resource policy on each command; hiding UI buttons is not authorization.

Roles can be combined and scoped to spaces/orders/devices. System administration does not automatically grant business approval:

| User role | Orders | Propose process/trial | Approve process | Prepare/start authorized jobs | Physical judgment/correction | Planning/delivery | Accounts/connections |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Operator | View authorized orders | Submit trials/observations | No | Within authorized devices | Observations, not quality acceptance | View | No |
| Process lead | View | Yes | Explicitly authorized scope | Separate device permission | View evidence | Supply process conditions | No |
| Inspector | View | Submit quality issues | No | No | Authorized criteria, with correction reasons | Supply accepted quantities | No |
| Order manager | Yes | Propose requirements | No | Separate device permission | View | Yes, without fabricated acceptance | No |
| System administrator | Resource policy | No | No | No | No | No | Yes; audit sensitive changes |

Process approval, repair acceptance, action approval, and readiness are separate decisions. One person may hold multiple roles; organization policy determines self-approval restrictions. Editing/publishing agent roles is a separate administrative permission; prompt changes cannot grant equipment or approval rights.

Start queries from tenant/space/resource constraints. RLS may add defense in depth; test connection roles, owner/bypass behavior, and transactional tenant context against pooled-connection leakage. Apply the same scope to checkpoints, retrieval, previews, downloads, and event streams.

## Business and external interfaces

Expose typed JSON commands/queries under `/api/v1`, consumed by Electron Main. Generate/validate TypeScript types from OpenAPI.

| Group | Examples | Constraints |
| --- | --- | --- |
| Orders/models | orders, order-lines, model-revisions, imports | Record completed upload, units, and revision confirmation separately |
| Inspection/slicing | inspections, repair-proposals, candidates, slice-runs | Async submission returns ID; status and artifact retrieval are distinct |
| Trials/processes | trials, measurements, validated-processes | Fixed revisions/evidence; clients cannot self-report approval |
| Production/quality | batches, print-jobs, incidents, output-lots, reprints | Transactional quantity transitions and idempotency keys |
| Devices/approval | devices, observations, actions, approvals | Query intent, approval, and actual outcome separately |
| Agents | agent-roles, agent-runs, tasks, events | Fixed role versions; explicit recovery/cancellation |
| Edge | edge/register, edge/commands, edge/receipts | Machine identity scoped to site/device, not an employee's unrestricted token |

Writes support business idempotency keys and expected resource versions; conflicts return explicit errors and reread information. Events include task_id, increasing sequence, type, resource version, and source timestamp. Reconnect/replay with deduplication; disconnection is not cancellation.

Use SSE for ordinary progress. Summarize high-frequency device observations into business changes on edge. Add WebSocket only for genuine low-latency bidirectional needs; persist long-term facts. Camera video is separately authorized rather than embedded in task events/logs.

## Knowledge, planning, and external products

Use document metadata/text retrieval: personal SQLite adapter, enterprise PostgreSQL, optional enterprise pgvector based on actual retrieval needs. Validate the same corpus separately; no personal vector database or additional embedding service is required. Enforce workspace/organization/document scope on each retrieval and citation reread; fallbacks stay within the same authorized set.

Present process references, observations, hypotheses, and approval evidence separately. Vision models may suggest inspection locations/incident types, not invent unmeasured dimensions or strength. Fix embedding/vision models after evaluation on actual Chinese terminology and fixtures; expensive models or local GPUs are not mandatory.

Check feasibility deterministically, then build explainable plans using deadlines, devices, materials, bed clearance, and staffing. Introduce OR-Tools CP-SAT when optimization needs justify it. Report infeasibility/timeouts/current feasible results and limitations, not an unsupported optimum. See the [official job-shop example](https://developers.google.com/optimization/scheduling/job_shop).

If using Spoolman, choose it or Autumn as the spool ledger, never two independent consumption ledgers. Obico/Gadget provides incident observations; disconnected/unmonitored states remain visible. Record automatic pauses and their owner in actions/observations; another agent must not resume unconditionally.
