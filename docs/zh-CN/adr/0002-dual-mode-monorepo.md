---
status: accepted
---

# 同一业务 Agent 支持个人本地与企业服务器，采用多应用单仓库

[English](../../en/adr/0002-dual-mode-monorepo.md) | 简体中文

2026-10-30：用户要求个人安装软件、配置大模型 API 即可使用，同时企业采用服务器部署。确定四个应用（desktop、api、worker、edge）与三个公共包（control-plane、contracts、sdk-ts）的 Monorepo；本地与企业共用业务及 Agent 图，通过存储、身份、模型与任务执行 Adapter 装配。目录固定职责，Git 分支只承担开发和发布。

个人版使用随包后台、SQLite 业务/任务与 checkpoint 存储、本地文件及当前用户身份；企业使用服务器 API/Linux worker、PostgreSQL、Celery/Redis、企业身份与文件存储。业务 Agent 只在所选控制端的 worker 中运行；现场端只执行受控工具、设备协议与动作核验，不配置第二套大模型。该决定替代 [ADR-0001](0001-control-plane-and-edge.md) 的服务器统一前提，保留其控制端与现场执行分离原则。

没有选择“所有用户必须部署服务器”，因为它不满足个人安装即用；没有复制两套 Agent 产品，因为规则和修复容易分叉；没有让企业统一使用单机数据库或要求 Windows 运行企业 Celery 栈，因为部署和并发约束不同。

代价是需要维护两套存储/队列 Adapter、迁移与故障测试。两种模式只共用业务语义，不假定数据库锁、权限与性能相同。个人与企业工作区不自动同步，设备写入归属需显式切换。完整约定见[双模式部署与工程结构](../architecture/runtime-and-deployment.md)。本决策已接受，产品尚未实现和验收。
