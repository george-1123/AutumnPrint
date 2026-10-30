# 仓库与工程结构

[English](../../en/architecture/repository.md) | 简体中文

本文是应用目录、公共包和依赖方向的唯一正文来源。完整目标结构固定，交付顺序见[工程计划](../engineering/delivery-plan.md)。四应用三公共包及构建清单已建立，业务子模块仍为目标，实际状态见[开发启动指南](../engineering/getting-started.md)。

## 单仓库与完整目标目录

采用 **Monorepo：四个应用、三个公共包**。目录表示产品职责，分支只用于开发、修复和发布；不使用“前端分支”“后端分支”维护不同代码树。不按本地版/企业版复制整套工程。

```text
Autumn-ai/
├── apps/
│   ├── desktop/                         # Electron 桌面应用
│   │   ├── src/
│   │   │   ├── main/                    # 窗口、工作区连接、会话、更新
│   │   │   ├── preload/                 # 受限 IPC
│   │   │   ├── renderer/
│   │   │   │   ├── features/            # 订单、工艺、生产、质量等页面
│   │   │   │   ├── components/
│   │   │   │   └── viewer/              # 模型与 G-code 预览
│   │   │   └── shared/                  # 桌面内部 IPC 结构
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── electron.vite.config.ts
│   │   └── electron-builder.yml
│   ├── api/
│   │   ├── src/autumn_api/
│   │   │   ├── routes/
│   │   │   ├── dependencies/
│   │   │   ├── main.py
│   │   │   └── cli.py                   # 开发/运维 CLI，复用业务用例
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── worker/
│   │   ├── src/autumn_worker/
│   │   │   ├── local/                  # 本地宿主、持久队列调度与恢复
│   │   │   ├── server/                 # Celery、outbox 派发与恢复
│   │   │   └── main.py
│   │   ├── tests/
│   │   └── pyproject.toml
│   └── edge/
│       ├── src/autumn_edge/
│       │   ├── connection/             # 注册、领取、心跳、回传
│       │   ├── execution/              # 进程、资源、取消与恢复
│       │   ├── slicing/                # Orca Adapter
│       │   ├── geometry/
│       │   ├── devices/
│       │   ├── journal/                # 本地动作日志
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
│   │   │   ├── agent/                  # 共用图、角色、工具与 checkpoint 适配
│   │   │   ├── infrastructure/         # SQLite/PostgreSQL、文件、模型连接
│   │   │   └── settings.py
│   │   ├── migrations/                 # 两种数据库的受测迁移
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── contracts/
│   │   ├── src/autumn_contracts/       # 版本化命令、回执、事件 DTO
│   │   ├── tests/
│   │   └── pyproject.toml
│   └── sdk-ts/
│       ├── src/                        # 生成的 HTTP 客户端与协议类型
│       └── package.json
├── fixtures/                           # 获准样件、订单、配置与事件
├── tests/                              # 跨应用集成与端到端测试
├── evals/                              # 两种模式共用业务与 Agent 评估
├── deploy/
│   ├── personal/                       # 本地后台注册、安装包与恢复
│   ├── enterprise/                     # API/worker/数据库/身份部署
│   ├── edge/                           # 现场端单独安装与登记
│   └── desktop/                        # 桌面发布、签名与渠道
├── scripts/                            # 协议生成、开发与构建
├── docs/
│   ├── en/                             # 默认英文文档
│   │   ├── README.md                   # 文档导航与职责
│   │   ├── project.md
│   │   ├── CONTEXT.md                  # 业务术语
│   │   ├── guide.md                    # 原指南导航
│   │   ├── technical-design.md         # 原技术设计导航
│   │   ├── deployment-and-project-structure.md
│   │   ├── product/                    # 需求与功能
│   │   ├── architecture/               # 系统、运行、Agent、仓库
│   │   ├── engineering/                # 初始化、交付、验证
│   │   ├── adr/                        # 决策及取舍
│   │   ├── research/                   # 来源与历史调研
│   │   └── LICENSE                     # 许可证原文
│   └── zh-CN/                          # 相同文件名的中文文档
├── .github/workflows/
├── .env.example                        # 开发示例；终端用户通过 UI 配置
├── .gitignore
├── pyproject.toml                      # uv workspace，无应用业务逻辑
├── uv.lock
├── package.json                        # 根级开发命令
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
└── README.md
```

这是完整目标目录，当前文档列出不代表已经生成应用代码。开发指南的阶段仅排列功能交付顺序，不再定义另一套临时目录，也不要求以后搬动应用。

文档按 `docs/en/` 与 `docs/zh-CN/` 分类并使用相同文件名，默认英文。根目录 README 仅作简短入口；中文目录的 Markdown 文件与英文目录对应。

## 依赖与构建规则

- `api`、`worker` → `control-plane` → `contracts`；`edge` → `contracts`。`edge` 不导入 `control-plane`，不随包携带中心数据库或模型凭据。
- `desktop` → `sdk-ts` → HTTP 接口。HTTP OpenAPI 由 API 装配共享 DTO 生成，非 HTTP 的命令/回执 schema 由 `contracts` 生成；二者派生 TypeScript 类型并在 CI 检查漂移，不维护第二份手写协议。
- `control-plane` 不导入应用入口；图工具调用业务 Module Interface，API 与 worker 不各写一套业务规则。控制端的设备模块保存能力与动作意图，现场端的设备模块实现真实协议。
- `contracts` 只含跨进程数据与版本协商，不含 ORM、队列、业务审批、模型或硬件执行；必要 schema 依赖可以携带，不发展成万能公共包。
- 四个应用分别构建、启动、记录版本和验收。Python 使用根 uv workspace/锁文件；应用依赖与 extras 分组，本地构建不安装 Celery/Redis/PostgreSQL 驱动，现场端构建不安装模型框架；企业镜像不携带桌面和几何二进制。
- Agent checkpoint 后端按模式装配，图版本与序列化协议相同。SQLite 与 PostgreSQL 的业务持久化及检索各有 Adapter/迁移与契约测试，不把一个数据库的测试结果当另一个的证明。
