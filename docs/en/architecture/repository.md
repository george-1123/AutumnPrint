# Repository and engineering structure

English | [简体中文](../../zh-CN/architecture/repository.md)

This document owns application directories, shared packages, and dependency direction. The full target structure is fixed; see the [delivery plan](../engineering/delivery-plan.md) for implementation order. Four app/three package manifests now exist. Nested business modules below remain targets; see [implementation status](../engineering/getting-started.md).

## Monorepo and complete target tree

Use a **monorepo with four applications and three shared packages**. Directories define responsibilities; branches serve development, fixes, and releases. Do not maintain separate frontend/backend code trees on branches or copy the whole product for local/enterprise modes.

```text
Autumn-ai/
├── apps/
│   ├── desktop/                         # Electron application
│   │   ├── src/
│   │   │   ├── main/                    # Windows, connections, sessions, updates
│   │   │   ├── preload/                 # Restricted IPC
│   │   │   ├── renderer/
│   │   │   │   ├── features/            # Orders, processes, production, quality
│   │   │   │   ├── components/
│   │   │   │   └── viewer/              # Model and G-code preview
│   │   │   └── shared/                  # Desktop IPC structures
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── electron.vite.config.ts
│   │   └── electron-builder.yml
│   ├── api/
│   │   ├── src/autumn_api/
│   │   │   ├── routes/
│   │   │   ├── dependencies/
│   │   │   ├── main.py
│   │   │   └── cli.py                   # Development/operations CLI, shared use cases
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── worker/
│   │   ├── src/autumn_worker/
│   │   │   ├── local/                  # Local host, durable scheduling, recovery
│   │   │   ├── server/                 # Celery, outbox dispatch, recovery
│   │   │   └── main.py
│   │   ├── tests/
│   │   └── pyproject.toml
│   └── edge/
│       ├── src/autumn_edge/
│       │   ├── connection/             # Registration, claims, heartbeats, reports
│       │   ├── execution/              # Processes, resources, cancellation, recovery
│       │   ├── slicing/                # Orca adapter
│       │   ├── geometry/
│       │   ├── devices/
│       │   ├── journal/                # Durable local action records
│       │   ├── workspace/
│       │   └── main.py
│       ├── tests/
│       └── pyproject.toml
├── packages/
│   ├── control-plane/
│   │   ├── src/autumn_control/
│   │   │   ├── modules/
│   │   │   │   ├── orders/
│   │   │   │   ├── models/
│   │   │   │   ├── processes/
│   │   │   │   ├── trials/
│   │   │   │   ├── production/
│   │   │   │   ├── quality/
│   │   │   │   ├── inventory/
│   │   │   │   ├── devices/
│   │   │   │   ├── knowledge/
│   │   │   │   ├── artifacts/
│   │   │   │   └── identity/
│   │   │   ├── agent/                  # Shared graphs, roles, tools, checkpoint adapters
│   │   │   ├── infrastructure/         # SQLite/PostgreSQL, files, model connections
│   │   │   └── settings.py
│   │   ├── migrations/                 # Tested migrations for both databases
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── contracts/
│   │   ├── src/autumn_contracts/       # Versioned commands, receipts, event DTOs
│   │   ├── tests/
│   │   └── pyproject.toml
│   └── sdk-ts/
│       ├── src/                        # Generated HTTP client and protocol types
│       └── package.json
├── fixtures/                           # Authorized samples, orders, settings, events
├── tests/                              # Cross-application integration and end-to-end
├── evals/                              # Shared business/agent evaluations
├── deploy/
│   ├── personal/                       # Background registration, installers, recovery
│   ├── enterprise/                     # API/worker/database/identity deployment
│   ├── edge/                           # Independent edge installation/registration
│   └── desktop/                        # Desktop publishing, signatures, channels
├── scripts/                            # Protocol generation, development, builds
├── docs/
│   ├── en/                             # Default English documentation
│   │   ├── README.md                   # Index and ownership
│   │   ├── project.md
│   │   ├── CONTEXT.md                  # Domain language
│   │   ├── guide.md                    # Former guide navigation
│   │   ├── technical-design.md         # Former design navigation
│   │   ├── deployment-and-project-structure.md
│   │   ├── product/                    # Requirements and features
│   │   ├── architecture/               # System, runtime, agents, repository
│   │   ├── engineering/                # Bootstrap, delivery, validation
│   │   ├── adr/                        # Decisions and tradeoffs
│   │   ├── research/                   # Sources and historical findings
│   │   └── LICENSE                     # Original license text
│   └── zh-CN/                          # Matching Chinese Markdown documents
├── .github/workflows/
├── .env.example                        # Development example; users configure in UI
├── .gitignore
├── pyproject.toml                      # uv workspace, no application business logic
├── uv.lock
├── package.json                        # Root development commands
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
└── README.md
```

This is the complete target tree, not implemented application code. Delivery phases sequence features rather than define temporary layouts or future directory moves. Documentation uses matching filenames under `docs/en/` and `docs/zh-CN/`, with English as default. Root README is a short entry point; the Chinese subtree mirrors English Markdown files.

## Dependency and build rules

- `api`, `worker` → `control-plane` → `contracts`; `edge` → `contracts`. Edge does not import the business core or carry central database/model credentials.
- `desktop` → `sdk-ts` → HTTP interfaces. API OpenAPI assembles shared DTOs; contracts generate non-HTTP command/receipt schemas. Derive TypeScript types and check drift in CI rather than hand-maintaining a second protocol.
- Control-plane does not import application entry points. Graph tools call module interfaces; API and worker share business rules. Control-side devices store capabilities/action intent; edge devices implement actual protocols.
- Contracts contain cross-process data/version negotiation, not ORM, queues, approvals, models, or hardware execution. Necessary schema dependencies are allowed; avoid a universal common package.
- Build, start, version, and test applications separately. Use root uv workspace/lockfile and scoped dependencies/extras. Personal builds exclude Celery/Redis/PostgreSQL drivers; edge excludes model frameworks; enterprise images exclude desktop/geometry binaries.
- Assemble checkpoint backends by mode with shared graph/serialization versions. SQLite/PostgreSQL persistence/retrieval have separate adapters/migrations/contract tests; one database's results do not prove the other's behavior.
