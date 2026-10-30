# Autumn Print technology selection research

English | [简体中文](../../zh-CN/research/technology-selection.md)

Verified: 2026-10-29 (Asia/Shanghai). Covers agents, Electron, 3D, backend/data, geometry, slicing, devices, enterprise deployment. Nothing is implemented. This document records official sources/design judgments; see [architecture](../architecture/overview.md) and [delivery](../engineering/delivery-plan.md).

Architecture revision (2026-10-30): personal local and enterprise server modes share business/agents. Original research dates, versions, popularity remain historical, not reverified. PostgreSQL/Celery/Redis/OIDC execution analysis concerns enterprise mode. Personal production uses SQLite business/durable queue/checkpoints, local owner identity, bundled background runtime. See [current deployment design](../architecture/runtime-and-deployment.md).

## Research method and decisions

Prioritize official repositories/releases/source/docs; distinguish popularity/activity, stable/prerelease status, licenses, applicability. These are representative popular projects for this product, not exhaustive GitHub rankings. Stars/latest branches do not establish compatibility/business validity. Dates/releases change; preserve uncertainty where unverifiable.

Electron is selected. Topics below retain evidence; architecture/delivery define adoption.

| Area | Design baseline |
| --- | --- |
| Desktop | Electron/electron-vite/React/TypeScript, Three.js/R3F, one builder/updater chain |
| Business | Python/uv/FastAPI/Pydantic modular monolith, independent native edge |
| Data | Personal SQLite/enterprise PostgreSQL, SQLAlchemy/Alembic, separate transaction/migration tests, ArtifactStore |
| Execution | Shared LangGraph; local durable queue/SQLite checkpoints versus Linux Celery/Redis/PostgreSQL checkpoints |
| Printing | Fixed stable Orca candidate/Trimesh, per-repair acceptance, Fake plus one real adapter |
| Enterprise | OIDC (development/default self-hosted Keycloak) and resource scope; phase 10 completes administration |

Stars/versions below are snapshots, not installation-tested locks.

## A. Agents and task execution

Research began 2026-10-29 19:54 (Asia/Shanghai), using official repositories, GitHub REST API, framework/product docs. No framework integration, real models, or printers were exercised.

### 1. Conclusion

Use **LangGraph as the shared graph runtime**, with local worker/SQLite durable tasks or enterprise server Linux Celery/Redis bounded fragments. Current workspace records own tasks/events/approvals/action intent; SQLite/PostgreSQL checkpoints do not replace them. Edge executes tools without a second model key.

Shared business CLI verifies real tools. Two task adapters are defined from the target architecture; enable one per workspace, never concurrent dispatch of the same task. Windows personal background uses a durable queue; native edge handles Orca/devices, not Celery.

This is product-specific judgment, not a star ranking. Popular full assistants inform design without importing all permissions/product structure.

### 2. Popularity and maintenance snapshot

Stars are exact API results or displayed approximations and change. API pushed_at is converted to Beijing date; a push is not a stable release or proof all features are stable.

| Project | Stars | Maintenance signal (Beijing time) | GitHub license | Use |
| --- | ---: | --- | --- | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | 393,334 | Push 2026-10-29 | MIT | Local tools/channels/credential scope reference, not print kernel |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | 258,285 | Push 2026-10-29 | MIT | Memory/history/skills, not physical process certification |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92,173 | Push 2026-10-29 | MIT | Control/execution separation and isolation; current main repository is Agent Canvas |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84,624 | Push 2026-10-29; v2.1.0 release page dated 2026-09-24 | MIT | Tasks/subtasks/artifacts/workbench, selectively borrowed |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44,073 | Push 2026-10-29; 1.2.18 release dated 2026-10-26 | MIT | Nodes/branches/bounded returns/human waits/state |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30,369 | Push 2026-10-28 | MIT | Lightweight tools/delegation comparison, not a second main runtime |
| [Temporal Python SDK](https://github.com/temporalio/sdk-python) | About 1.2k | 1.35.0 page says 2026-10-28 20:16; interpreted as UTC gives Beijing 10-29, but timezone not explicit: recheck | MIT | Future durable business orchestration candidate, not adopted |

Metadata sources:

- [OpenClaw API](https://api.github.com/repos/openclaw/openclaw): pushed_at `2026-10-29T11:07:05Z`.
- [Hermes API](https://api.github.com/repos/NousResearch/hermes-agent): `2026-10-29T07:22:41Z`.
- [OpenHands API](https://api.github.com/repos/OpenHands/OpenHands): `2026-10-29T10:14:43Z`.
- [DeerFlow API](https://api.github.com/repos/bytedance/deer-flow): `2026-10-29T06:40:09Z`; [releases](https://github.com/bytedance/deer-flow/releases).
- [LangGraph API](https://api.github.com/repos/langchain-ai/langgraph): `2026-10-28T23:08:19Z`; [releases](https://github.com/langchain-ai/langgraph/releases).
- [OpenAI Agents API](https://api.github.com/repos/openai/openai-agents-python): `2026-10-27T19:44:03Z`.
- Temporal API failed; stars/license from [repository](https://github.com/temporalio/sdk-python), activity from [releases](https://github.com/temporalio/sdk-python/releases). SDK stars are not main-platform popularity.

Repository SPDX identifiers do not replace component review. This sample is not exhaustive or a recommendation to install production from main branches.

### 3. Why LangGraph

[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) distinguishes thread checkpoints/cross-thread store. [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers) preserve/recover state. [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) wait for input and restart execution from the interrupted node's beginning.

Implications:

- Represent compare → trial wait → measurements → review → approval branches/waits.
- Explicit inspection/comparison/retrieval/review nodes; application owns types/completion.
- Multiple roles share restricted execution; child agents gain no extra permissions.
- Checkpoints contain references/summaries/reasoning, artifacts hold models/G-code/photos, business tables hold approvals/counts.
- Server resolves thread_id and verifies organization/task ownership; clients cannot choose others' threads.
- Replayed pre-interrupt code cannot contain unguarded print starts, revisions, approvals.

Graph keys associate organization/task/run/version through internal IDs or controlled mappings, not unlimited raw organization strings. One effective executor per run; conditional writes/leases prevent concurrent recovery.

### 4. Other agent projects: reuse and exclusions

#### DeerFlow

[README](https://raw.githubusercontent.com/bytedance/deer-flow/main/README.md) and [2.1 release](https://github.com/bytedance/deer-flow/releases) describe subagents/workspaces/memory/sandbox/trusted execution. Borrow tasks/artifacts/delegation/records, not generic research/creation permissions for physical actions.

#### Hermes and OpenClaw

[Hermes](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) emphasizes cross-session information/skills/schedules; [OpenClaw](https://raw.githubusercontent.com/openclaw/openclaw/main/README.md) local state/entry/replacable models/backends. Borrow retrieval/policy/local execution. Generated skills/memory are not validated production parameters; measurements/approvals remain necessary.

#### OpenHands

[Current repository](https://github.com/OpenHands/OpenHands#readme) distinguishes Agent Canvas, software agent SDK, automation repositories. Borrow control/execution/workspace isolation, without assigning main stars to a fictitious unified Python SDK or assuming a coding agent is required.

#### OpenAI Agents SDK

[Official SDK](https://developers.openai.com/api/docs/guides/agents/sdk) and [orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration) cover tools, collaboration, context, ownership. Viable for lightweight single-agent/expert tools, but this product needs graph state/human waits/explicit review: select LangGraph without a second primary runtime.

### 5. Celery and LangGraph responsibilities

#### Evidence

[Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) covers acknowledgments/redelivery/idempotency/retries; [Redis broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html) visibility timeout/long ETA risk; [FAQ](https://docs.celeryq.dev/en/stable/faq.html) says Windows is unsupported.

#### Proposed ownership (design judgment)

| Layer | Owns | Does not replace |
| --- | --- | --- |
| PostgreSQL | Tasks/orders/approval/process/action/event/outbox facts | Model execution or proof that physical actions happened |
| Celery/Redis | Bounded dispatch/execution/transport redelivery | Process acceptance or long-term business database |
| LangGraph | Reasoning nodes/branches/state/bounded tool retries/interrupts | Physical fleet scheduling or automatic restart authorization |
| Windows/Linux edge | Native tools/device actions/durable deduplication/outcomes | Windows Celery or unlimited cross-tenant permissions |

Checkpoint and exit when waiting for measurement/approval; authorized events dispatch recovery. Do not occupy a Celery task for days or use distant ETA as a scheduling database.

#### Reliability to implement explicitly

1. Transactional task/outbox plus dispatcher retries enable recoverable database/message handoff, not physical exactly-once.
2. Redelivery retains run/action identity; check version/cancellation/lease/prior result before execution.
3. Separate transport and model/tool retry counters/budgets; no auto_retry for all exceptions.
4. Disable generic start retries but still handle broker duplicates: journal same action_id, return prior result, reconcile unknowns rather than restart.
5. Visibility timeout exceeds measured fragment maximum with margin; infinite timeouts cannot hide multi-day waits.
6. Reconnect from durable facts/events, not Celery results or Redis Pub/Sub.
7. Separate CPU slicing and I/O agent queues/concurrency; pass large-file references/checksums, not broker payloads.
8. Physical device lifecycle is independent of worker lifecycle; terminating workers is not safely stopping printers.

#### Synchronous workers and sessions

Use supported Linux workers with explicit synchronous task entries. Each task/branch owns session/transaction/authorization; initialize connections after fork, never share parent transactions.

[SQLAlchemy sessions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) require Session per thread/AsyncSession per task and separate background-process sessions. Manage event-loop/client lifetimes explicitly for async models/LangGraph. Never reuse AsyncSession/old-loop clients across tasks/threads/loops; do not hold transactions through external waits.

### 6. When to reconsider Temporal

[Activities](https://docs.temporal.io/activities) support durability/retries/heartbeat; [Python guide](https://docs.temporal.io/develop/python) covers messages/timers/cancellation/versioning.

Not selected due to infrastructure, determinism, operations. If multi-day flows/receipts/timers/compensation/multisite recovery dominate, evaluate replacing outer orchestration, not independent retries from Temporal/Celery/custom queues.

[Temporal LangGraph integration](https://docs.temporal.io/develop/python/integrations/langgraph) was Public Preview in this research; it describes Temporal-owned durability using InMemorySaver without PostgreSQL/Redis checkpointers and Store/streaming retry limitations. Reassess stability rather than layering over current checkpoints/Celery.

### 7. First validation checklist

- Pin graph/checkpoint/provider/driver versions; verify structured calls.
- Wait for approval → stop → restart → authorized recovery, retaining task/graph/tenant.
- Inject failures around interrupts; reuse references, deduplicate events, record budgets.
- Simulate redelivery, two workers/one run, Redis outages, dispatcher restart.
- Simulate started print/lost cloud receipt; reconcile without restart.
- Fake authorization/readiness/deduplication first, then explicitly authorized hardware.

These are pending checks, not passing tests.

## B. Electron, data, and enterprise infrastructure

Research date: 2026-10-29 (Asia/Shanghai). Research only, no implementation/devices. Stars are approximate repository figures; versions come from official releases/source. Cached retrieval means release/latest may concern different subpackages. Installation still requires locks/compatibility tests. This is a representative sample, not a global ranking.

### 1. Popularity and maintenance

| Project | Approximate stars | Verified release/activity | License | Judgment |
| --- | --- | --- | --- | --- |
| [React](https://github.com/react/react) | 251.8k | [19.3.1, 2026-10-14](https://github.com/react/react/releases/tag/v19.3.1) | MIT | Workbench UI |
| [Vite](https://github.com/vitejs/vite) | 83.6k | [8.3.5, 2026-10-21](https://github.com/vitejs/vite/releases/tag/v8.3.5) | MIT | electron-vite foundation; repository latest points to create-vite@9.3.3, not core Vite |
| [Three.js](https://github.com/mrdoob/three.js) | 117.2k | [r186, 2026-09-24](https://github.com/mrdoob/three.js/releases/tag/r186) | MIT | Interactive 3D |
| [React Three Fiber](https://github.com/pmndrs/react-three-fiber) | 33.3k | [9.8.2, 2026-10-15](https://github.com/pmndrs/react-three-fiber/releases/tag/v9.8.2) | MIT | Stable v9/React19, defer v10 alpha |
| [vtk.js](https://github.com/Kitware/vtk-js) | 1.5k | [38.0.4, 2026-10-28](https://github.com/Kitware/vtk-js/releases/tag/v38.0.4) | BSD-3-Clause | Scientific visualization alternative, not a second initial engine |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | 126.9k | [CLI 4.23.0, 2026-10-27](https://github.com/shadcn-ui/ui/releases/tag/shadcn@4.23.0) | MIT | Selected maintainable UI code; CLI version is not all copied components' version |
| [TanStack Query](https://github.com/TanStack/query) | 50.5k | [Release batch, 2026-10-26](https://github.com/TanStack/query/releases/tag/release-2026-10-26-0932) | MIT | Server state; verify framework packages separately |
| [FastAPI](https://github.com/fastapi/fastapi) | 104.3k | [0.162.0, 2026-10-23](https://github.com/fastapi/fastapi/releases/tag/0.162.0) | MIT | Python business entry |
| [Keycloak](https://github.com/keycloak/keycloak) | 37.6k | [26.8.1, 2026-10-13](https://github.com/keycloak/keycloak/releases/tag/26.8.1) | Apache-2.0 | Optional enterprise IdP; existing OIDC compatible |
| [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | 35.8k | [4.51, 2026-10-25](https://github.com/seaweedfs/seaweedfs/releases/tag/4.51) | Apache-2.0 | Optional self-hosted S3, not initial distributed cluster |
| [Playwright](https://github.com/microsoft/playwright) | 98.8k | [1.64.1, 2026-10-14](https://github.com/microsoft/playwright/releases/tag/v1.64.1) | Apache-2.0 | Critical end-to-end flows |
| [pgvector](https://github.com/pgvector/pgvector) | 23.5k | README 0.8.7; cached tags still show 0.8.6, no unverified date claim | [PostgreSQL License](https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE) | Add for demonstrated vector needs, no separate database initially |
| [MinIO](https://github.com/minio/minio) | 61.3k | Official repository archived/read-only 2026-04-25 | AGPL-3.0 | Not a default new store based on stars |

Some GitHub API reads worked and others did not; direct shell networking was restricted. No uniform real-time exact stars/pushed_at claim. Dates are from accessible official pages; approximations retain repository links.

### 2. Electron recommendation (user's latest choice)

**Electron + electron-vite + React 19 + TypeScript + Three.js + R3F v9 + TanStack Query + necessary shadcn/ui/Tailwind; electron-builder packaging and electron-updater updates.**

React runs in sandboxed renderer; main owns windows/file selection/sign-in/restricted system capabilities; preload is narrow. Python edge owns Orca/geometry/devices. The authenticated 3D workbench does not need initial SSR/Next.js. Enterprise backend remains server-deployable; desktop cannot bypass authorization.

- Query owns order/trial/process/task server state, updated/invalidated by versioned SSE.
- Renderer routes hold filters/selections/deep links, React local forms/dialogs. Add Zustand only for genuinely shared 3D views, not a server database copy.
- Add Table for complex grids; existing components suffice for simple lists. Measure virtualization needs.
- Add React Flow only for an interactive plan editor; start with step/status lists.

Sources: [Vite](https://vite.dev/guide/), [Query](https://github.com/TanStack/query), [R3F](https://r3f.docs.pmnd.rs/getting-started/introduction). R3F v9 pairs with React19; do not adopt v10 alpha just for novelty.

### 3. 3D and files

- Three.js/R3F displays models/beds/orientations/issues/differences/supported paths.
- [STLLoader](https://threejs.org/docs/pages/STLLoader.html) loads binary/ASCII into non-indexed geometry; display is not topology/manufacturing validation.
- Preserve original STL/3MF/hashes; generate bounded GLB previews with object/coordinate maps, never replace manufacturing inputs/configuration.
- Handle foreign 3MF geometry/private settings/start scripts separately; successful preview is not full project reconstruction.
- Restricted Python handles large-model conversion; Web Workers handle renderer parsing/paths with cancel/byte/triangle/decimation limits. Avoid global-state buffers/repeated JSON IPC.
- Preview implemented G-code/layer/travel/extrusion semantics and selected ranges, not all vendor macros/multitool semantics initially.

vtk.js specializes in scientific visualization. Start with one Three.js mesh/preparation engine; reassess vtk.js for demonstrated volume-data/scientific pipelines.

### 4. Backend and storage

**Python + FastAPI + Pydantic + SQLAlchemy 2.x + Alembic + PostgreSQL.** Verify exact patches when locking, not unbounded latest from this snapshot.

- API validates/authorizes/submits/queries/streams. CPU geometry/slicing runs separately. [BackgroundTasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) is not a durable workflow mechanism.
- Pydantic defines I/O/tools/configuration; database transactions/constraints enforce quantities/references/revisions/state.
- SQLAlchemy manages transactions, Alembic migration. [SQLAlchemy docs](https://docs.sqlalchemy.org/) included 2.1; 2.0 guides are not latest. [Alembic](https://alembic.sqlalchemy.org/en/latest/) showed 1.20.1.
- Personal production SQLite, enterprise PostgreSQL; separately test transactions/concurrency/leases/migrations. SQLite does not prove PostgreSQL locks/RLS.
- Foreign keys/uniqueness/transactions/optimistic versions enforce business integrity; application scopes tenants/resources. Test optional [RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) with actual connection roles rather than assuming isolation.
- PostgreSQL docs showed stable 18, 19 RC; production selects supported stable, not RC.
- Metadata/full-text retrieval first; optional pgvector for real recall problems, not multiple Milvus/Qdrant/Elasticsearch stores initially.

### 5. Models, G-code, large files

- DB stores artifact metadata/hash/key/size/type/organization/scope/state, not large ordinary binary fields.
- Small shared local/S3 interface; no arbitrary user absolute paths.
- Evaluate SeaweedFS single-machine/existing S3 uploads/multipart/Range/checksums/lifecycle rather than assuming full S3 semantics.
- Complete validated bounded uploads before artifacts become available; compensate storage/DB failures and collect orphans.
- Authorize downloads. Direct transfer uses short-lived object/method URLs, not public logs/long-term model memory.
- Distinguish previews/manufacturing files; batches reference immutable approved revisions.

### 6. Communication, identity, Windows edge

- HTTPS JSON commands/queries, durable events/SSE replay/deduplication; connections are not task state. [MDN SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events).
- System-browser OIDC authorization-code + PKCE; main validates/exchanges callbacks as public client without packaged secret. Check state/nonce/issuer/exact redirect. Prefer temporary loopback; strictly validate custom scheme/host/path/one-use state if IdP requires it. No embedded login substitute. [RFC8252](https://datatracker.ietf.org/doc/html/rfc8252).
- Main authentication proxy holds short-lived tokens/scoped API. Renderer gets named operations/events, not arbitrary URL/request proxies. No refresh tokens in renderer/localStorage/URLs. Main/authenticated stream forwards scoped SSE and releases subscriptions on disconnect/exit.
- Windows edge runs restricted Orca/geometry and LAN devices, claiming/reporting via authenticated outbound HTTPS without public inbound ports. WebSocket only if needed, never sole factual storage.
- Renderer holds no printer credentials/direct LAN access; one write owner per device.
- Enterprise [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers) or existing IdP establishes identity; Autumn still checks membership/order/device/approval scope.
- Human RBAC and agent roles differ. Agents cannot gain device rights users lack. Explicit policy/audit for process approval/inspection correction/start.

Personal installers register a window-independent current-user API/worker/edge host; enterprise components deploy separately. Leases/facts/recovery cannot depend on UI memory. Exit is not cancel; updates cannot interrupt handoff. Protect discovery, instance authentication, endpoint permissions even on 127.0.0.1.

### 7. Validation and operations

- pytest, compatible Vitest/Testing Library, Playwright for critical orders/approvals/trials. Test actual packaged Electron installation/login/preload/GPU/exit/recovery, not only Vite pages.
- Small geometry/coordinate/revision fixtures; screenshots do not prove geometry/physical quality.
- Structured task/order/slice/job/trace logs from outset; gradually add [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) traces/metrics, not several full clusters.
- Linux Compose can run backend/database; Windows edge installs/versions separately. Containers do not imply identical discovery/GPU/hardware behavior.
- uv/pnpm manage dependencies; pin engines/plugins/edge binaries and validate upgrades.

### 8. Baseline, conditional additions, exclusions

**Complete baseline:** four apps/three packages, Python/API, controlled tools/artifacts, Electron build/distribution, React/TS/Three/R3F, restricted IPC/authorization/logging. Personal SQLite/bundled host, enterprise PostgreSQL/migrations/Celery/Redis. Personal users do not need enterprise infrastructure; see deployment for packaging/acceptance.

**Conditional:** complex Table, Zustand, React Flow, pgvector, SeaweedFS, Keycloak, full telemetry backend, Redis cache.

**Not initially:** Next.js SSR, parallel Forge chain, two 3D engines, Kubernetes/microservices, vector clusters, competing queues, archived MinIO default, R3F v10 alpha, builder27/updater7 alpha.

Product-specific judgments need real models, G-code volumes, networks, IdPs; not universal project quality rankings.

### 9. Electron snapshot and one build chain

| Project | Approximate stars | Verified stable release | License | Decision |
| --- | --- | --- | --- | --- |
| [Electron](https://github.com/electron/electron) | 123.6k | [45.1.0, 2026-10-27](https://github.com/electron/electron/releases/tag/v45.1.0) | MIT | Desktop candidate, follow supported stable |
| [electron-vite](https://github.com/alex8088/electron-vite) | 5.6k | [6.0.0, 2026-10-14](https://github.com/alex8088/electron-vite/releases/tag/v6.0.0) | MIT | Development/main/preload/renderer builds |
| [electron-builder](https://github.com/electron-userland/electron-builder) | 14.7k | [26.18.1, 2026-10-26](https://github.com/electron-userland/electron-builder/releases/tag/electron-builder@26.18.1) | MIT | Installers; 27 prerelease |
| [electron-updater, same repo](https://github.com/electron-userland/electron-builder/tree/master/packages/electron-updater) | Not double-counted | [6.8.12, 2026-10-26](https://github.com/electron-userland/electron-builder/releases/tag/electron-updater@6.8.12) | MIT | Paired updater; 7 prerelease |
| [Forge](https://github.com/electron/forge) | 7.2k | [8.0.1, 2026-09-29](https://github.com/electron/forge/releases/tag/v8.0.1) | MIT | Comparison only |

Select **electron-vite → electron-builder → Windows NSIS**, using electron-updater. Vite handles dev/hot reload/three entry points; builder handles releases/installers/update metadata. [Distribution guide](https://electron-vite.org/guide/distribution) documents integration. Do not maintain parallel Forge package/make. [Forge Vite](https://www.electronforge.io/config/plugins/vite) was experimental with possible minor-version breaking changes, not stable merely because Forge is official.

Candidates: Electron45.1.0/electron-vite6.0.0/Vite8.3.5/builder26.18.1/updater6.8.12/React19/R3F9. Releases/declarations only: no install/lock/build/compatibility results. electron-vite6 [package.json](https://raw.githubusercontent.com/alex8088/electron-vite/v6.0.0/package.json) requires Node `^20.19.0 || >=22.12.0`, Vite6/7/8. Select/test a supported LTS intersection; minimum supported is not recommended current runtime.

**Build Node differs from bundled Node.** pnpm/Vite/builders use host/CI Node; main uses Electron Node; sandbox preload is restricted; renderer lacks Node. Upgrading build Node does not upgrade installed Chromium/Node. Python/Orca/native geometry are external runtimes, not renderer/Electron ABI modules. Controlled extraResources outside ASAR are OS/architecture-specific, verified/versioned. Models/credentials/workspaces stay in managed user data, not installation. [Process model](https://www.electronjs.org/docs/latest/tutorial/process-model), [distribution](https://electron-vite.org/guide/distribution).

### 10. Desktop security and credentials

Follow [security](https://www.electronjs.org/docs/latest/tutorial/security) and [context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation):

- Explicit `nodeIntegration:false`, `contextIsolation:true`, `sandbox:true`, preserve `webSecurity`, restrict CSP/permissions.
- contextBridge exposes typed business operations, not ipcRenderer/shell/arbitrary files/commands/generic channels; do not forward Electron event objects.
- Main validates sender/frame origin/webContents, schemas/resource ownership/limits. Allowlists do not replace server approval. Model/G-code contents are data, not executable scripts/HTML.
- Packaged renderer loads local resources through restricted app protocol/path checks. Reject unauthorized navigation/windows; validate scheme/host before `openExternal`. Remote help/login gets no preload privilege.

Main/edge hold credentials by responsibility. Main protects permitted refresh-token persistence using safeStorage/restricted user data and clears on logout; device keys stay edge. DPAPI does not protect against every program as the same logged-in user. [safeStorage](https://www.electronjs.org/docs/latest/api/safe-storage) marked synchronous APIs deprecated from Electron45; use `isAsyncEncryptionAvailable`, `encryptStringAsync`, `decryptStringAsync`. Validate Linux secret-service provider; `basic_text`/unprotected fallback is not secure even when availability returns true. Refuse sensitive persistence and use memory sessions, not hardcoded-password fallback.

### 11. Windows releases, updates, validation

First target: **Windows x64 full NSIS installer**, preferably per-user. Machine-wide workshop services/enterprise distribution are separate later deployment work. Desktop/edge version/protocol checks are independent; updates contain no printer credentials. Announce other OS support only after testing.

CI emits versioned installers/checksums/metadata, signs production Windows packages, retains publishing credentials, uses HTTPS/publisher checks. Signatures do not replace staged release/rollback. Disable automatic exit/install during jobs; install when idle/user confirms restart, retain manual downloads. [Signing](https://www.electronjs.org/docs/latest/tutorial/code-signing), [builder26 updates](https://www.electron.build/v26/docs/features/auto-update/).

Use electron-updater, not built-in autoUpdater: platforms/protocol/configuration differ. Default builder site has v27; do not apply v27/updater7 `autoInstallEvent/onNextLaunch` or signed-manifest features to builder26/updater6. [Built-in autoUpdater](https://www.electronjs.org/docs/latest/api/auto-updater/) lacks built-in Linux updating; choose Linux distribution/update separately.

Test clean installation/uninstall, signed upgrades, incomplete/invalid metadata/files, offline/proxy, canceled/bad login callbacks/expired tokens, missing Linux secret stores, large-model GPU/RAM, IPC scope violations, edge recovery, no duplicate dispatch on exit/update. These are pending checks, not passed integration tests.

## C. Orca, geometry, and devices

Verified 2026-10-29 (Asia/Shanghai). Research only: no compilation/slicing/devices. Stars approximate GitHub pages, not global rankings; recheck versions before install. Public API returned 403 rate limits; no private tokens were used and missing exact dates were not invented.

### 1. Popularity, releases, and licenses

| Project | Approximate stars | Verifiable release/activity | Repository license | Judgment |
| --- | --- | --- | --- | --- |
| [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) | 16.2k | API latest [v2.4.2](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.4.2), published_at=2026-07-07; local 2.5.0-dev | AGPL-3.0 | Fixed actual slicing engine |
| [Trimesh](https://github.com/mikedh/trimesh) | 3.7k | [5.2.0](https://github.com/mikedh/trimesh/releases), page says 24 Oct | MIT | Basic loading/measurement/topology |
| [Manifold](https://github.com/elalish/manifold) | 2.4k | [v3.5.4](https://github.com/elalish/manifold/releases), 25 Sep | Apache-2.0 | Valid-input solid Booleans, not universal repair |
| [PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab) | 984 | [v2025.7.post1](https://github.com/cnr-isti-vclab/PyMeshLab/releases), asset 2026-01-30 | GPL-3.0 | Optional isolated checks/repairs, test filters individually |
| [Moonraker](https://github.com/Arksine/moonraker) | 1.5k | [master](https://github.com/Arksine/moonraker/commits/master/) shows 2026-09-09 and 0.11.0 preparation; old Releases do not establish maintained version | GPL-3.0 | Direct adapter with Klipper hardware |
| [OctoPrint](https://github.com/OctoPrint/OctoPrint) | 9.2k | [Releases](https://github.com/OctoPrint/OctoPrint/releases): stable 1.11.8; 2.0.0rc7, 20 Oct, prerelease | AGPL-3.0 | Prefer if existing device uses it; no default RC |
| [Spoolman](https://github.com/Donkie/Spoolman) | 3.0k | [v0.27.0](https://github.com/Donkie/Spoolman/releases), 25 Sep | MIT | Future spool inventory adapter, one authority |
| [Obico server](https://github.com/TheSpaghettiDetective/obico-server) | 1.9k | [release branch](https://github.com/TheSpaghettiDetective/obico-server/commits/release/) shows 2026-07-11; [Releases](https://github.com/TheSpaghettiDetective/obico-server/releases) empty | AGPL-3.0 | Incident evidence, not physical inspection |

Some release summaries omit year; retain displayed dates, not tag-year assumptions. Lock tag/commit/binary hash/dependencies during implementation. Repository licenses do not settle component/plugin/model/distribution/service obligations; independent processes alone imply no legal conclusion.

### 2. Combination and adoption order

**First:** fixed Orca + Trimesh + restricted local executor. Read/check/slice/preserve facts; complex repairs unsupported or human-handled.

**Next:** optional isolated PyMeshLab candidates only after defect/dimension/part checks. Add Manifold only for needed valid-input Booleans, not CGAL/libigl/multiple heavy backends together.

**Devices:** Fake plus one real adapter: Moonraker for Klipper, OctoPrint if already deployed. Hardware is unknown, so selection remains conditional, never a universal brand protocol.

### 3. Inspection and repair matrix

| Check/operation | Implementation | Required limits |
| --- | --- | --- |
| Parsing/empty/invalid indices/non-finite coordinates | File validation/Trimesh/format checks | Bound bytes/expanded sizes/faces/resources; parsing is not validity |
| Bounds/area/volume/parts/transforms | Trimesh | Preserve units; confirm unitless STL. Open/invalid-model volume is not precise pricing/quality |
| Watertight/winding/edge adjacency/degenerate/duplicate faces | Trimesh + validated small checks | Watertightness is distinct from excluding all non-manifold vertices; per-check pass/fail/unknown/unsupported |
| Normals/small holes | Restricted Trimesh repair | [Repair docs](https://trimesh.org/trimesh.repair.html) describe in-place changes/nonconvex-hole risk; copy to new revision first |
| Large holes/mesh filters | Optional PyMeshLab worker | [Filters](https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing-close-holes) use heuristic self-intersection prevention, not universal valid-solid repair |
| Complete intersections/non-manifold vertices/complex repair | Separate acceptance, initially unsupported | is_watertight is not intersection testing; automatic filling does not prove shape correctness |
| Solid Booleans | Conditional Manifold | [README](https://github.com/elalish/manifold/blob/master/README.md): non-manifold input returns error; output guarantees do not mean arbitrary repair |
| Thin walls/overhangs/manufacturability/dimensions/strength | Dedicated algorithms/slicing/physical measurement | Unimplemented analysis unavailable; no screenshot-based model pass |

Reports include checker/version/input hash/units/result/location/count where supported/evidence/limits. Preserve scene parts/transforms; disconnected shells are not automatically disposable debris.

Repair creates ModelRevision with original/options/before-after reports/bounds/volume/part changes/available surface deviation. Model owner accepts before process candidates. Unvalidated zero-defect reports cannot be approved. Business requirements determine units/tolerance, not universal hardcoded percentages.

### 4. Slicer interface and isolation

Concentrate validation, detection, workspace, execution, parsing, receipts inside the slicer interface. Callers submit model references/effective snapshots and receive uniform results/errors rather than scattered CLI construction.

- Real Orca and Fake adapters; Fake cannot appear real.
- Pin engine version/digest/resources/presets and derive capabilities from actual `--help`/fixtures.
- [CLI](https://www.orcaslicer.com/wiki/cli/cli_mode) and [actions](https://www.orcaslicer.com/wiki/cli/cli_actions) are references, not proof every stable/dev build exports all features/plugins.
- Preserve original 3MF; validate ZIP paths/expansion; distinguish settings/transforms/sliced files. Not every 3MF is trusted executable work.
- Resolve machine/process/filament inheritance into complete settings/provenance; changes require old-slice review.
- Per-run workspace/datadir where supported; no global presets, unknown inherited postprocessors, unauthorized start/end G-code.
- Argument arrays plus identity/file/network/CPU/memory/time restrictions and whole-process-tree cleanup. Windows requires actual Job Object/process controls, not assumed subprocess/Docker sandbox.
- Preserve exit/warnings/stdout/stderr/final hashes/actual estimates; missing statistics null/unknown, not model-filled.
- Open actual output in target Orca/fixtures. Estimates/measurements remain distinct; no cross-platform byte-identity assumption.

#### Read-only local source verification

Parent task confirmed `D:\project\OrcaSlicer-main\OrcaSlicer-main`; root AGENTS.md was read first. No additional src instructions; tests were not read/written.

- `version.inc`: `2.5.0-dev`, uncompiled, not assumed stable upstream.
- `src/libslic3r/PrintConfig.cpp:11678` / `:11954`: CLI definitions; load_settings/load_filaments at `:11980` / `:11986`.
- `src/slic3r/Utils/PrintHost.cpp:58` / `:68` / `:70` / `:73`: OctoPrint/Obico/SimplyPrint/Moonraker.
- `src/libslic3r/GCode.cpp:2223` / `:2226`: filament/time_cost accumulation; enterprise pricing avoids duplicate machine time and separately adds labor.
- `docs/gpl-mesh-repair-cli-0-to-1.md` is an existing design, not proof an executable repair worker passed acceptance. The independent mesh-repair-worker project was not inspected/modified.

### 5. Windows/LAN edge and device interfaces

Control owns business/tasks/files; site machines run edge, initially colocatable, later separately deployable. Registered site/device scopes and short leases govern outbound claims/reports. Browser holds no device keys/direct printer connection; LAN devices need no public exposure.

#### Queries and actions

- `describe_capabilities(device)`: verified upload/queue/start/pause/resume/cancel/history/state support.
- `observe(device)`: source timestamp/freshness; stale data cannot satisfy readiness.
- `submit/observe_action(action_id)`: authorized type/hash/device execution/readback, unknown retained for reconciliation.

These are draft interfaces; fix fields against real samples. Models propose business actions, not arbitrary network calls/raw G-code.

#### Why Moonraker for Klipper

[Printer API](https://moonraker.readthedocs.io/en/latest/external_api/printer/) supports queries/subscriptions/start/pause/resume/cancel with connected Klippy, often ready prerequisites. Useful for actual state but not universal business idempotency.

[OctoPrint files API](https://docs.octoprint.org/en/main/api/files.html) supports upload/query/permissions/select-print for existing deployments. Untested RCs are not production baselines. Add adapters gradually but assign one scheduling owner per machine.

#### Single writer and unknown outcomes

- Create durable Action with action_id/device_id/tenant/site/file/approval before exclusive execution claims.
- Serialize device actions; durable local journal plus central lease, not just memory locks.
- Recheck authorization/process/nozzle/material/bed/idle/freshness; approved is not executed.
- Timeout queries remote files/jobs/history/local journal; human review when uncorrelatable, never blind restart.
- Single-writer covers controlled channels only. External panels/farm systems can still act; stop/escalate conflicts, no universal exclusion guarantee.
- Choose vendor/SimplyPrint/Printago or Autumn as scheduling authority; no competing automatic queues.
- Confirm print completion, clearance, removal, inspection, quantities separately. Remote pause/cancel is not machine safety certification.

### 6. Later integration choices

Spoolman can expose spool_id for process/batch inventory. One authoritative ledger distinguishes actual/estimated/reserved/returned/corrected material; device/Autumn/Spoolman must not independently deduct.

Obico supplies alerts/evidence. Record automatic pauses/actor so other flows do not immediately resume. Occlusion/disconnection is monitoring_unavailable, not no incident. Explicit policy owns pauses, not competing agents.

#### First reviewable checks

1. Normal/small-hole/non-manifold/self-intersection fixtures with expected capability matrix.
2. Two effective profiles, actual Orca slicing/files/statistics.
3. Before-after dimensions/parts/shape and owner acceptance.
4. Fake duplicates/timeouts/occupancy/offline-recovery state machine.
5. One authorized upload-only and start with same-job readback.
6. Missing measurements/bed clearance/remaining material stay waiting, not invented completion.

## D. Development tools, scheduling, deployment

| Project/evidence | Official sources | Purpose/limits |
| --- | --- | --- |
| uv (~91.3k stars) | [Repository](https://github.com/astral-sh/uv), [projects](https://docs.astral.sh/uv/guides/projects/) | Python/locks; native platform support still tested |
| Ruff (~50.3k) | [Repository](https://github.com/astral-sh/ruff) | Lint/format, not business/device contracts |
| Celery (~29.1k) | [Repository](https://github.com/celery/celery), [broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html) | Linux fragments/redelivery; independent Windows protocol |
| OR-Tools (~14.3k) | [Repository](https://github.com/google/or-tools), [job shop](https://developers.google.com/optimization/scheduling/job_shop) | CP-SAT for real constraints; no LLM optimality claims |
| Node.js | [Release table](https://nodejs.org/en/about/previous-releases) | Supported LTS; build and bundled runtimes separate |
| Redis licenses | [Official terms](https://redis.io/legal/licenses/) | Pin/review chosen version; not all BSD |

Snapshot release table showed Node24/26 LTS. Validate build chain on 24, upgrade 26 after tests; not a replacement of Electron's bundled Node.

Redis8+ offers RSALv2/SSPLv1/AGPLv3 choices; review actual distribution/deployment. This does not conclude Autumn commercial obligations.

## E. Implementation gates

1. Record OS/architecture/versions/locks/engine hashes/fixtures/material licenses.
2. Actual Windows installer/OIDC/restricted IPC; renderer lacks privileged dependencies.
3. Real Orca CLI/inheritance/parsing/cancellation and per-check geometry acceptance.
4. PostgreSQL/Linux worker dispatch failures/concurrent recovery/redelivery/waits/cancellation; window closure does not change business facts.
5. Known authorized hardware before real adapters; read/upload before actions/unknown reconciliation.
6. Separate software/slicing/device/physical evidence; unsupported/unvalidated never appears successful.
