---
status: accepted
---

# Shared business agents for personal and enterprise modes in a multi-application monorepo

English | [简体中文](../../zh-CN/adr/0002-dual-mode-monorepo.md)

2026-10-30: Personal users must be able to install the application and configure a model API, while enterprises use server deployment. Adopt a monorepo with four applications (desktop, api, worker, edge) and three shared packages (control-plane, contracts, sdk-ts). Both modes share business logic and agent graphs, assembled with storage, identity, model, and task-execution adapters. Directories define responsibilities; Git branches serve development and releases.

Personal mode uses bundled background processes, SQLite business/task and checkpoint storage, local files, and the current user's identity. Enterprise mode uses server APIs/Linux workers, PostgreSQL, Celery/Redis, enterprise identity, and enterprise file storage. Business agents run only in the selected control plane's worker. The edge executor performs controlled tools, device protocols, and action reconciliation without a second model configuration. This supersedes [ADR-0001](0001-control-plane-and-edge.md)'s universal-server assumption while retaining control/edge separation.

Requiring every user to deploy a server would violate personal install-and-use requirements. Duplicating agents into separate products would fork rules and fixes. Using a single-machine database for all enterprise deployments, or requiring the enterprise Celery stack on Windows, would ignore different deployment and concurrency constraints.

The cost is maintaining two storage/queue adapters, migrations, and failure-test suites. The modes share business semantics, not assumptions about database locks, authorization, or performance. Personal and enterprise workspaces do not synchronize automatically; device write ownership changes explicitly. See [runtime and deployment](../architecture/runtime-and-deployment.md). This decision is accepted; implementation and acceptance testing are pending.
