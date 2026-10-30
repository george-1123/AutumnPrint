---
status: superseded by ADR-0002
---

# Modular monolithic control plane and independent edge executor

English | [简体中文](../../zh-CN/adr/0001-control-plane-and-edge.md)

2026-10-30: [ADR-0002](0002-dual-mode-monorepo.md) supersedes the deployment and repository organization. The original context is retained below. Control/edge separation and device-action reconciliation remain applicable; the assumption that all users require a server does not.

Autumn Print centralizes business rules, authorization, quality quantities, and agent orchestration in a modular monolith. A managed edge executor handles Orca subprocesses, material/device readings, and authorized actions. This supports Windows slicing and factory LAN devices with enterprise collaboration, while avoiding the maintenance cost of early microservices and a deeply forked desktop slicer. The edge executor claims scoped tasks through outbound connections and does not hold business database credentials.

The workbench uses Electron. The React/TypeScript renderer reaches the control plane through restricted preload and main layers. The native enterprise edge executor runs independently; closing a window does not stop slicing or device jobs. The desktop does not hold device credentials or replace the edge executor for print control.

Business records own tasks, action intents, approvals, and physical quantities. Graph checkpoints and queues have separate execution responsibilities. Queue redelivery, graph recovery, or lease expiration cannot by itself authorize another print start: inspect action records and actual device outcomes first, and investigate unknown results.

See the [architecture overview](../architecture/overview.md). This remains an unimplemented design baseline, not a design validated against real binaries, devices, and deployment samples.
