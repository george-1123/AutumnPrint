# 开发启动指南

[English](../../en/engineering/getting-started.md) | 简体中文

2026-10-30 工程基础。这是开发环境，不是终端安装包。诊断均为模拟，不访问真实打印机、Orca、第三方模型或模型服务。

## 安装与启动

需要 Python 3.12、uv 0.13.6、Node 24（最低 22.12）、pnpm 11.25.0。首次安装需要访问包源与 Electron 发布地址。在仓库根目录运行 PowerShell：

```powershell
uv sync --frozen --all-packages
pnpm install --frozen-lockfile
uv run pnpm dev
$env:AUTUMN_SESSION = (Resolve-Path .runtime/session.json).Path
uv run pnpm dev:desktop
```

点击 **运行链路诊断**。预期状态 `queued → waiting_edge → succeeded`，事件为 `queued`、`fake_model_completed`、`fake_tool_completed`。关窗后重新打开可补读同一任务，Python 后台独立运行。

```powershell
uv run python scripts/dev.py status
uv run pnpm dev:stop
uv run --package autumn-api python -m autumn_api.cli show-order --fixture fixtures/orders/bracket-50-sets.json
```

样例展开为 50 个底座、100 个卡扣。模型引用有意留空，单位、配置和验收条件未确认。相邻 `provenance.json` 记录原创虚构来源与模拟设备/材料清单。

## 验证

```powershell
uv run pytest -q
uv run ruff check apps packages scripts tests
uv run ruff format --check apps packages scripts tests
uv run pnpm generate
uv run pnpm check
pnpm build
# 后台运行时：
uv run python tests/process_smoke.py
pnpm test:desktop
```

生成入口输出 OpenAPI、非 HTTP 协议 schema 和派生 TypeScript 类型。CI 检查漂移、依赖方向、Windows/Linux，并设置独立 PostgreSQL 服务作业；尚未观察远端 CI 结果。

进程测试仅终止本项目宿主创建的 API 子进程以验证有界恢复。Electron 测试提交后关窗重开、验证补读与受限 IPC，截图位于 `.runtime/desktop.png`。

本机记录（Windows，2026-10-30）：Python 3.12.14、Node 24.17.0、pnpm 11.25.0、Electron 45.1.0。pytest 为 7 通过、1 项 PostgreSQL 跳过；Ruff、依赖边界、TypeScript 与桌面构建通过。独立进程往返、API 崩溃恢复、整个宿主重启及凭据轮换、真实 Electron 按钮提交/关窗重开/IPC 测试通过。Electron 来自官方 GitHub 发布，并核对 npm 包附带的 SHA256。TestClient 当前产生一条上游 Starlette/httpx 弃用提示，不影响上述通过结果。

开发宿主采用 OS 文件锁、独立 API/worker/edge 子进程、显式停止请求，每个子进程在一次宿主生命周期中最多启动五次。日志位于 `.runtime/{host,api,worker,edge}.log`。数据库和现场回执跨重启保留；宿主重启会轮换凭据，需要重开桌面。

`.runtime/` 已忽略，并在 Windows 限制为执行/交互账号访问（POSIX 目录 0700、session 文件 0600）。发现记录保存独立随机桌面/现场 bearer 凭据，renderer 不接收凭据。API 检查凭据和来源并绑定 loopback。这是开发机制，真实模型 Key 的系统凭据库尚未实现。开发数据有意放在 `.runtime/` 便于检查，正式用户目录与托管服务仍待实现。

## 企业与完整门槛

共享存储提供 SQLite/PostgreSQL Alembic 迁移。企业配置拒绝 SQLite 或缺少 Redis，企业依赖位于独立 extra：

```powershell
uv sync --frozen --all-packages --all-extras
# 设置 AUTUMN_MODE=enterprise、AUTUMN_WORKSPACE、AUTUMN_DATABASE_URL、
# AUTUMN_BROKER_URL 和独立 AUTUMN_DESKTOP_TOKEN / AUTUMN_EDGE_TOKEN。
uv run python -c "from autumn_control.migrate import migrate; from autumn_control.settings import Settings; migrate(Settings.from_env().database_url)"
uv run uvicorn autumn_api.main:create_app --factory --host 127.0.0.1
# Linux worker：beat 定期唤醒持久任务行构成的 outbox。
uv run celery -A autumn_worker.server:app worker -B
```

OIDC/RBAC、多用户会话未实现，此入口属于开发基础，不应用作正式企业服务。设置 `AUTUMN_TEST_POSTGRES` 可针对隔离测试库运行 PostgreSQL 测试，会创建表和测试行，禁止指向生产数据。本机没有 PostgreSQL/Redis，因此企业执行未在本机验证。

| 门槛 | 已实现 | 完整门槛剩余工作 |
| --- | --- | --- |
| B-01 | 四应用三公共包、锁文件、依赖检查 | 独立发布产物 |
| B-02 | 配置校验、独立凭据、显式 Fake | UI 模式切换、系统凭据库、企业身份 |
| B-03 | SQLite 迁移、持久任务/事件、现场日志；PostgreSQL Adapter | PostgreSQL 验收、Agent checkpoint |
| B-04 | 本地进程往返、持久 outbox/Celery 入口 | Redis/Celery 恢复与企业端到端测试 |
| B-05 | 版本校验、登记、租约领取、日志化幂等回执 | 每现场端独立凭据、心跳、真实工具 |
| B-06 | Electron/React、生成类型、IPC 校验、游标轮询 | SSE、UI 连接/模式选择、生成路由客户端 |
| B-07 | 单宿主、关窗后台存活、API 恢复 | OS 托管宿主恢复、真实动作优雅停止 |
| B-08 | 命令、本地检查/构建、CI 定义 | 干净机器 CI、安装包和双模式验收 |

当前重试只适用于 Fake 工具，真实动作需要另行实现设计中的结果未知核查协议。

参考：[uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/)、[FastAPI 安全工具](https://fastapi.tiangolo.com/reference/security/)、[electron-vite](https://electron-vite.org/guide/)、[Electron 安全指南](https://www.electronjs.org/docs/latest/tutorial/security/)。
