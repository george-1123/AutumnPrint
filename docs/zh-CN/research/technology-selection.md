# Autumn Print 技术选型调研

[English](../../en/research/technology-selection.md) | 简体中文

核验日期：2026-10-29（Asia/Shanghai）。覆盖 Agent、Electron 桌面端、3D、后端、数据、几何、切片、设备和企业部署。项目尚未实现，本文记录官方来源与设计判断，实际集成选择见 [技术设计](../architecture/overview.md)，增量交付见 [指南](../engineering/delivery-plan.md)。

架构修订说明（2026-10-30）：用户已确定个人本地和企业服务器两种模式，共用业务及 Agent。下文原始调研日期、版本与关注度保留，不代表本次重新核验。涉及 PostgreSQL、Celery/Redis、OIDC 的执行与运维分析适用于企业配置；个人正式配置采用 SQLite 业务/持久队列及 checkpoint、本地所有者身份与随包后台。完整目录和当前交付约束以[双模式部署设计](../architecture/runtime-and-deployment.md)为准。

## 调研方法与最终决定

优先阅读官方 GitHub 仓库、发布页、源文件和文档，分别记录关注度、维护活动、稳定/预发布状态、许可证和实际适用场景。这里是针对打印产品的代表性高 Star 样本，不声称穷尽全 GitHub，也不以 Star 或最新主分支代替兼容性和业务验证。版本、关注度和发布页会变化；不能核实的日期明确保留限制。

前端确定为 Electron。下列专题保存选型证据，技术设计和指南统一规定实际引入时机。

| 领域 | 最终设计基线 |
| --- | --- |
| 桌面 | Electron + electron-vite + React/TypeScript；Three.js/R3F；builder/updater 单一分发链 |
| 业务 | Python/uv + FastAPI/Pydantic + 模块化单体；原生现场端独立运行 |
| 数据 | 个人 SQLite、企业 PostgreSQL；共用 SQLAlchemy/Alembic，分别验证事务迁移；文件另存 ArtifactStore |
| 执行 | 共用 LangGraph；个人本地持久队列与 SQLite checkpoint，企业 Linux Celery/Redis 与 PostgreSQL checkpoint |
| 打印 | 固定 Orca 稳定候选 + Trimesh；修复能力逐项验收；Fake 后选择一个真实设备 Adapter |
| 企业 | 标准 OIDC（开发/默认自托管可用 Keycloak）+ 应用资源授权；阶段 10 完善企业管理 |

以下 Star/版本是取证快照，尚未组合成安装验证过的锁文件。

## A. Agent 与任务执行

调研时间：2026-10-29 19:54 起（Asia/Shanghai）。依据官方仓库、GitHub REST API、官方产品/框架文档。未实现框架接入，未调用真实模型或打印机。

### 1. 结论

采用 **LangGraph 作为共用 Agent 图编排实现**，个人由本机 worker/SQLite 持久队列执行，企业由服务器 Linux Celery/Redis 执行有界片段。业务任务、事件、审批与动作意图分别保存在当前工作区数据库；checkpoint 使用对应模式的 SQLite/PostgreSQL 存储，不替代业务事实。现场端只执行工具，无需第二套模型 Key。

真实工具可以通过共用业务 CLI 验证。完整目标从架构上定义两种任务 Adapter，一个工作区只启用一种后端，不让两者同时派发同一任务。Windows 个人后台使用本地持久队列，现场端独立负责原生 Orca 与设备适配，不运行 Celery worker。

这是适配 Autumn Print 需求的设计判断，不是仅凭 Star 数作出的排名。最高关注度的完整助手作为设计参考，不直接引入其全部运行权限与产品结构。

### 2. 高关注度与维护快照

下表 Star 为本次官方 API 返回的具体值或仓库显示的约数，会变化。活跃日期把 API pushed_at 转成北京时间日期；它只表示仓库最近有推送，不等于最新正式发布或全部功能稳定。

| 项目 | Star | 最近维护信号（北京时间） | GitHub 标识许可证 | 本项目如何使用 |
| --- | ---: | --- | --- | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | 393,334 | 2026-10-29 推送 | MIT | 参考本地执行、渠道、工具策略与凭据边界；不直接作为打印运行内核 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | 258,285 | 2026-10-29 推送 | MIT | 参考记忆、历史检索与技能沉淀，不把学习循环当成物理工艺认证 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92,173 | 2026-10-29 推送 | MIT | 参考前端控制中心与执行后端分离、工作区与隔离；当前主仓库是 Agent Canvas |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84,624 | 2026-10-29 推送；release v2.1.0 页面发布于 2026-09-24 | MIT | 参考长任务、子任务、成果和工作台；从业务模块选择性借鉴 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44,073 | 2026-10-29 推送；release 1.2.18 页面发布于 2026-10-26 | MIT | 选作 Agent 节点、分支、有限回退、人机等待与执行状态实现 |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30,369 | 2026-10-28 推送 | MIT | 作为轻量工具/委派运行方式对照，本轮不与 LangGraph 同时承担主编排 |
| [Temporal Python SDK](https://github.com/temporalio/sdk-python) | 约 1.2k | release 1.35.0 页面显示 2026-10-28 20:16，按 UTC 理解对应北京时间 10-29；页面未显式时区，实施前复核 | MIT | 后续复杂耐久业务编排候选，本轮不引入 |

元数据原始来源：

- [OpenClaw API](https://api.github.com/repos/openclaw/openclaw)：pushed_at `2026-10-29T11:07:05Z`。
- [Hermes API](https://api.github.com/repos/NousResearch/hermes-agent)：pushed_at `2026-10-29T07:22:41Z`。
- [OpenHands API](https://api.github.com/repos/OpenHands/OpenHands)：pushed_at `2026-10-29T10:14:43Z`。
- [DeerFlow API](https://api.github.com/repos/bytedance/deer-flow)：pushed_at `2026-10-29T06:40:09Z`；[release 页面](https://github.com/bytedance/deer-flow/releases)。
- [LangGraph API](https://api.github.com/repos/langchain-ai/langgraph)：pushed_at `2026-10-28T23:08:19Z`；[release 页面](https://github.com/langchain-ai/langgraph/releases)。
- [OpenAI Agents API](https://api.github.com/repos/openai/openai-agents-python)：pushed_at `2026-10-27T19:44:03Z`。
- Temporal API 本次读取失败，Star 与许可证采用[仓库页面](https://github.com/temporalio/sdk-python)，维护信号采用[release 页面](https://github.com/temporalio/sdk-python/releases)。不能把 1.2k SDK Star 与主平台关注度等同。

GitHub SPDX 是仓库级标识，不替代逐组件核查。以上是针对本项目的样本，未进行全站穷尽排名，也未把主分支代码视为适合生产直接安装的版本。

### 3. 为什么选择 LangGraph

[官方持久化文档](https://docs.langchain.com/oss/python/langgraph/persistence)区分 thread 级 checkpointer 与跨 thread store；[checkpointer 文档](https://docs.langchain.com/oss/python/langgraph/checkpointers)提供持久状态与恢复机制。[Interrupt 文档](https://docs.langchain.com/oss/python/langgraph/interrupts)支持等待外部输入后继续，且明确恢复时会从中断节点开头重跑。

对 Autumn Print 的含义：

- 需要“比较工艺→等待试打→补测量→复核→等待批准”等分支与长时间等待，图状态适合表达推理过程。
- 检查、参数比较、知识检索和复核可分为明确节点；工具返回类型和业务完成条件由应用控制。
- 多 Agent 是同一个受限执行体系的分工，不让子 Agent 获得更高工具权限。
- checkpoint 只存业务引用、摘要和推理状态；模型、G-code、照片放成果存储，批准与数量放业务表。
- 恢复参数中的 thread_id 由服务端定位并检查组织/任务归属，客户端不能任选另一个 thread。
- 中断前的代码可能重跑，因此打印启动、文件修订与批准生效不能直接写成无保护的节点副作用。

建议 graph key 关联组织、任务、run 与图版本，使用内部 ID 或受控映射，不把原始组织字符串无限拼进 thread_id。每个 run 同时只有一个有效执行者，使用数据库条件更新/租约避免并发恢复同一图。

### 4. 其他 Agent 项目的可借鉴处与不采用处

#### DeerFlow

[官方 README](https://raw.githubusercontent.com/bytedance/deer-flow/main/README.md)与[2.1 release](https://github.com/bytedance/deer-flow/releases)描述子 Agent、工作区、记忆、沙箱与可信执行。适合学习任务与成果体验、按需委派和运行记录；它的通用研究/创作工具权限不能直接套到真实打印机动作。

#### Hermes 与 OpenClaw

[Hermes README](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md)强调跨会话信息、技能与定时工作；[OpenClaw README](https://raw.githubusercontent.com/openclaw/openclaw/main/README.md)强调本地状态、入口和可替换模型/运行后端。适合借鉴资料召回、工具策略和本地执行模式。打印工艺仍需要测量与批准，不把自动生成的技能或记忆当作经过验证的生产参数。

#### OpenHands

[当前官方仓库说明](https://github.com/OpenHands/OpenHands#readme)将 Agent Canvas、软件 Agent SDK 和自动化仓库区分。可以参考“控制中心—执行后端”的拆分和工作区隔离；不把主仓库 Star 归到一个不存在的统一 Python SDK，也不默认需要引入其编码 Agent。

#### OpenAI Agents SDK

[OpenAI 官方文档](https://developers.openai.com/api/docs/guides/agents/sdk)与[编排说明](https://developers.openai.com/api/docs/guides/agents/orchestration)给出工具、Agent 协作、上下文与所有权设计。对于轻量单 Agent 与专家工具调用，是可行备选；本项目已明确需要图状态、人工等待与显式工艺复核，因此本轮采用 LangGraph，不再增加第二个主运行框架。

### 5. Celery 与 LangGraph 的职责分工

#### 事实依据

[Celery 任务文档](https://docs.celeryq.dev/en/stable/userguide/tasks.html)描述消息确认、重投、幂等与任务重试；[Redis broker 文档](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html)说明 visibility timeout 和长 ETA 风险；[官方 FAQ](https://docs.celeryq.dev/en/stable/faq.html)明确 Windows 不受官方支持。

#### 建议分工（设计判断）

| 层 | 拥有什么 | 不拥有或不能替代什么 |
| --- | --- | --- |
| PostgreSQL 业务表 | 任务与订单状态、审批、工艺版本、外部动作、事件与outbox | 不执行模型，也不单靠行状态假装物理动作完成 |
| Celery + Redis | 后台有界任务的投递、worker 执行与传输重投 | 不拥有工艺完成条件，不作为长期业务事实库 |
| LangGraph | 一段推理的节点、分支、状态、有限工具重试与中断 | 不承担农场物理调度，不能自动重复打印启动 |
| Windows/Linux 本地执行端 | 原生工具与单设备动作、持久动作去重、实际结果 | 不运行 Windows Celery worker，不持有跨租户无限权限 |

执行片段遇到等待测量/审批时保存状态并退出 worker。收到已授权业务事件后，再投递恢复命令；不让一个 Celery task 等待几天，也不使用遥远 ETA 当长期调度数据库。

#### 需要显式实现的可靠性规则

1. 业务任务与 outbox 在同一事务提交，派发器重试投递。它解决的是数据库/消息间的可恢复交接，不提供物理动作恰好一次保证。
2. 一个运行的所有重复投递使用同一业务 run/action 标识，执行前检查版本、取消、租约和已完成结果。
3. 传输重投与模型/工具有限重试分开计数和预算；Celery 不对所有异常一律 auto_retry。
4. 设备启动禁用通用自动重试，但仍需抵御 broker 重投：本地账本先识别相同 action_id，已执行返回已知结果；结果未知先查设备和远端作业，不再次启动。
5. Redis visibility timeout 应大于单次有界任务的实际最大运行时间并留裕量；不能通过无限加长 timeout 掩盖跨天等待。
6. 数据库事实和事件是重连来源，Celery result backend 和 Redis Pub/Sub 均不替代持久业务记录。
7. CPU 密集切片与 I/O 密集 Agent 片段使用独立队列/并发上限；大文件只传引用及校验值，不塞进 broker 消息。
8. 设备边缘端的物理作业生命周期独立于 Celery worker 生命周期；中止 worker 不等同于安全停止打印机。

#### 同步 worker 与会话原则

使用官方支持的 Linux worker，推荐明确的同步任务入口。每次任务/并发分支拥有自己的数据库 Session、事务与授权上下文；数据库连接在 fork 后按进程初始化，不传入父进程已开启的事务。

[SQLAlchemy 官方 Session 文档](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)要求 Session per thread、AsyncSession per task，并指出后台子进程应建立自己的会话。调用异步模型或 LangGraph 时建立明确的事件循环生命周期与客户端生命周期；不能把一个 AsyncSession 或绑定旧循环的异步客户端跨任务/线程/循环复用。等待模型和外部动作期间不持有长期数据库事务。

### 6. Temporal 的后续引入条件

[Temporal Activity 文档](https://docs.temporal.io/activities)提供耐久动作、重试与heartbeat；[Python指南](https://docs.temporal.io/develop/python)覆盖工作流消息、定时器、取消与版本等能力。

本轮暂不采用，原因是增加独立基础设施、工作流确定性约束及运维复杂度。若今后跨天流程、外部回执、定时器、补偿与多站点恢复成为主要复杂度，应评估以 Temporal **替换外层工作流调度**；避免 Temporal、Celery 与自建队列同时各自决定同一动作的重试。

特别注意：[Temporal 官方 LangGraph 集成](https://docs.temporal.io/develop/python/integrations/langgraph)本次标注 Public Preview，文档说由 Temporal 管耐久性时无需 PostgreSQL/Redis checkpointer，使用 InMemorySaver；并有 Store 与流式重试等限制。以后若采用该集成，应按当时稳定性重新选型，不能直接把它叠在当前 PostgreSQL checkpoint 与 Celery 调度之上。

### 7. 首个验证清单

- 固定 LangGraph、checkpoint、模型适配器和驱动版本，完成基本结构化工具调用。
- 做一次等待批准→停进程→重启→授权恢复，检查同一任务/图版本与租户归属。
- 在中断节点前后故障注入，验证结果引用复用、事件去重和预算记录。
- 模拟 Celery 重投、两worker竞争同一run、Redis短暂不可用与派发器重启。
- 模拟“本地端已启动打印但云端未收到回执”，确认进入核查且不会再次启动。
- 在假设备上验证授权、准备条件和动作去重，再按明确授权接测试设备。

以上是需要实施的验证，不是本轮已经通过的功能测试。

## B. Electron、数据与企业基础设施

调研日期：2026-10-29（Asia/Shanghai）。只研究，不实现、不连接设备。Star 取 GitHub 仓库页约数；版本取官方 release/源文件。本次网络抓取有缓存，不能把 release/latest 一概理解为所有子包的最新版本；最终安装仍需锁文件与兼容性测试。以下是代表性高关注项目样本，非全站最高排名。

### 1. 高 Star 与近期维护核对

| 项目 | Star 约数 | 本次核实的近期版本/维护 | 许可证 | 本项目判断 |
| --- | --- | --- | --- | --- |
| [React](https://github.com/react/react) | 251.8k | [19.3.1，2026-10-14](https://github.com/react/react/releases/tag/v19.3.1) | MIT | 首选工作台 UI |
| [Vite](https://github.com/vitejs/vite) | 83.6k | [Vite 8.3.5，2026-10-21](https://github.com/vitejs/vite/releases/tag/v8.3.5) | MIT | 作为 electron-vite 的底层构建工具；仓库 latest 当前跳到 create-vite@9.3.3，不能混称 Vite 核心版本 |
| [Three.js](https://github.com/mrdoob/three.js) | 117.2k | [r186，2026-09-24](https://github.com/mrdoob/three.js/releases/tag/r186) | MIT | 首选交互 3D 预览基础 |
| [React Three Fiber](https://github.com/pmndrs/react-three-fiber) | 33.3k | [9.8.2，2026-10-15](https://github.com/pmndrs/react-three-fiber/releases/tag/v9.8.2) | MIT | 采用稳定 v9 配 React19，v10 alpha 延后 |
| [vtk.js](https://github.com/Kitware/vtk-js) | 1.5k | [38.0.4，2026-10-28](https://github.com/Kitware/vtk-js/releases/tag/v38.0.4) | BSD-3-Clause | 保留为科学可视化替代，不首期并用第二引擎 |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | 126.9k | [CLI shadcn@4.23.0，2026-10-27](https://github.com/shadcn-ui/ui/releases/tag/shadcn@4.23.0) | MIT | 采用需要的可维护 UI 代码；CLI 版本不等于全部复制组件版本 |
| [TanStack Query](https://github.com/TanStack/query) | 50.5k | [仓库发行批次，2026-10-26](https://github.com/TanStack/query/releases/tag/release-2026-10-26-0932) | MIT | 服务端状态首选，单个框架包的版本需分别核验 |
| [FastAPI](https://github.com/fastapi/fastapi) | 104.3k | [0.162.0，2026-10-23](https://github.com/fastapi/fastapi/releases/tag/0.162.0) | MIT | Python 接入与业务接口首选 |
| [Keycloak](https://github.com/keycloak/keycloak) | 37.6k | [26.8.1，2026-10-13](https://github.com/keycloak/keycloak/releases/tag/26.8.1) | Apache-2.0 | 正式企业身份可选；兼容已有 OIDC 提供方 |
| [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | 35.8k | [4.51，2026-10-25](https://github.com/seaweedfs/seaweedfs/releases/tag/4.51) | Apache-2.0 | 可选自托管 S3，不首期启动分布式集群 |
| [Playwright](https://github.com/microsoft/playwright) | 98.8k | [1.64.1，2026-10-14](https://github.com/microsoft/playwright/releases/tag/v1.64.1) | Apache-2.0 | 工作台关键流程端到端验证 |
| [pgvector](https://github.com/pgvector/pgvector) | 23.5k | 当前 README 示例为 0.8.7；tags 页面缓存仍显示 0.8.6 等，不声明未核实发布日期 | [PostgreSQL License](https://raw.githubusercontent.com/pgvector/pgvector/master/LICENSE) | 检索需要向量时加入，先不用独立向量数据库 |
| [MinIO](https://github.com/minio/minio) | 61.3k | 官方仓库明确 2026-04-25 已归档，只读 | AGPL-3.0 | 不因高 Star 作为新部署的默认对象存储 |

注意：部分 GitHub API 页面可读，部分不可读；本次直接 shell 请求受网络限制，因此没有声称取得实时精确 Star 或统一 pushed_at 快照。上述 release 日期来自可读的官方页面，约数均有仓库链接。

### 2. Electron 桌面端推荐（按用户最新决定）

**Electron + electron-vite + React 19 + TypeScript + Three.js + React Three Fiber v9 + TanStack Query + 必需的 shadcn/ui/Tailwind UI；electron-builder 负责打包，electron-updater 负责桌面更新。**

产品入口是 Electron 桌面工作台。React 在沙箱 renderer 中运行，Electron main 管窗口、本地文件选择、登录与受限系统能力，preload 只作窄接口桥接；Python Edge 独立执行 Orca/几何处理与设备接入。Autumn 是登录后的 3D 生产工作台，首期不需要 SSR，Next.js 不进入主链。后端仍可部署在企业服务器，桌面端也不能绕过服务端权限。

- TanStack Query 管理订单、试验、工艺、任务等服务端状态；SSE 到达时按版本更新或失效相关查询。
- renderer 路由存筛选与选中订单，封装桌面深链接；React 局部状态管理表单和弹窗。Zustand 仅在多个 3D 面板确实共享视图状态时引入，不复制整个服务端数据库。
- TanStack Table 可在订单/质量数据网格复杂后加入，简单清单先用已有组件；虚拟化以实际性能测试决定。
- React Flow 仅在需要可交互计划图/流程编辑器时加入。首期使用步骤列表和状态视图即可。

依据：[Vite 入门](https://vite.dev/guide/)、[TanStack Query 仓库功能](https://github.com/TanStack/query)、[R3F 介绍](https://r3f.docs.pmnd.rs/getting-started/introduction)。R3F 文档明确 v9 配 React19、v10 仍 alpha，不推荐为了最新版本使用 alpha。

### 3. 3D 与文件呈现

- 用 Three.js/R3F 展示模型、打印床、朝向、检查问题位置、候选差异和支持显示的切片路径。
- Three.js 官方 [STLLoader](https://threejs.org/docs/pages/STLLoader.html)可读取二进制/ASCII STL，返回非索引几何；这只是显示，不构成拓扑或制造验证。
- 导入原始 STL/3MF 后，后端保留原件与哈希，再生成受限大小的 GLB 等预览派生物，保存对象/坐标映射。预览文件不能替代用于制造的原始模型和有效配置。
- 外来 3MF 的几何、切片器私有设置和启动脚本需分别处理。预览加载成功不代表复原了全部 Orca 项目语义。
- 大模型读取/转换放在受限 Python 进程；renderer 的解析和切片路径加载可用 Web Worker，保留取消、三角形/字节上限和降采样提示。大缓冲不塞进普通全局状态，也不反复经 JSON IPC 复制。
- G-code 预览按已实现命令语义、层和挤出/移动类型解析；只加载选定层范围，不在首版承诺所有厂商宏与多工具语义。

vtk.js 擅长科学可视化数据处理（其定位为 Visualization Toolkit for the Web）；本项目以交互网格和打印准备为主，因此先只用一个 Three.js 渲染体系。后期若实际出现体数据或特定科学管线需求，再验证 vtk.js 的独立价值。

### 4. 后端与存储

**Python + FastAPI + Pydantic + SQLAlchemy 2.x + Alembic + PostgreSQL。** 精确补丁版本在建立锁文件时核验，不以本文快照直接构造无上限 latest 依赖。

- FastAPI 处理验证、权限、任务提交、查询与事件传输。切片/几何长 CPU 任务放独立执行进程；官方 [BackgroundTasks 文档](https://fastapi.tiangolo.com/tutorial/background-tasks/)也把重计算与多进程分布式工作作为另需工具的场景。不能把 BackgroundTasks 当耐久工作流。
- Pydantic 用于外部输入输出、工具参数与配置；数据库约束和事务另行保证数量、引用、版本和状态一致性。
- SQLAlchemy 管业务事务，Alembic 做迁移；当前官方 [SQLAlchemy 文档](https://docs.sqlalchemy.org/)已提供 2.1，已有2.0指南不应被误当最新。[Alembic 文档](https://alembic.sqlalchemy.org/en/latest/)本次显示1.20.1。
- 正式业务持久层个人选择 SQLite，企业选择 PostgreSQL；分别验证事务、并发、租约和迁移，不能用 SQLite 模拟 PostgreSQL 锁/RLS 并声称验证通过。
- PostgreSQL 外键、唯一约束、事务与乐观版本是主要业务一致性工具；租户/资源过滤在应用执行，RLS 可作纵深保护。官方 [RLS 文档](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)应结合数据库连接角色与测试设计，避免当成自动隔离保证。
- 当前 PostgreSQL 官方文档稳定分支为18，19仍RC；新部署选受支持稳定版本而非RC。
- 技术资料与历史工艺先用元数据/全文检索；有实际召回问题时再加 pgvector。不首期并用 Milvus、Qdrant、Elasticsearch 等多套存储。

### 5. 模型、G-code 与大文件

- 业务 DB 只存 artifact 元数据、hash、对象键、长度、类型、所属组织、访问范围和处理状态，大二进制不直接作为普通业务字段塞入数据库。
- 初始本地 ArtifactStore 与未来 S3 adapter 共用小接口；本地目录不能由用户传入任意绝对路径。
- 自托管S3可评估SeaweedFS单机模式/组织已有S3，测试实际需要的上传、分片、Range、校验和生命周期行为；不把“S3兼容”理解为全语义一致。
- 分片上传、大小限制、校验及完成确认后才创建可用 artifact；数据库与存储失败分步补偿，孤儿文件有回收策略。
- 文件下载先鉴权。需要直传/直下时签发短时、限定对象与方法的地址，禁止把签名地址写进公共日志或直接交给模型长期保存。
- 预览派生文件与制造文件分别标识；批次引用已批准版本的不可变文件。

### 6. 通信、身份与 Windows 本地执行端

- 常规业务用 HTTPS JSON 命令和查询。任务/步骤进度用持久化事件 + SSE，按序号补读，UI去重；SSE连接本身不是任务状态。参见 [MDN SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)。
- 桌面登录使用系统浏览器 OIDC Authorization Code + PKCE，由 main 接收、验证回调并交换授权码；按 public client 配置，不把 client secret 打包。校验 state/nonce、issuer、精确 redirect URI；优先评估临时 loopback 回调，若企业 IdP 要求自定义 scheme 则严格验证 scheme/host/path 与单次状态。不能用内嵌登录页代替系统浏览器。依据：[IETF RFC8252](https://datatracker.ietf.org/doc/html/rfc8252)。
- main 的认证代理持有短期 access token，与受限 API 客户端连接后端；renderer 经命名业务接口调用与事件订阅获得所需数据，不能获得任意 URL/任意请求代理。refresh token 不进入 renderer/localStorage，不通过 URL 传递。SSE 由 main 或认证流客户端订阅后转发窄事件；断开/退出要释放订阅。
- Windows本地执行端运行受控Orca/几何子进程并接局域网设备。它主动通过认证HTTPS领取获准任务、上传结果；起步不需要暴露公网入站端口。确需低延迟双向连接再加WebSocket，不用它存唯一事实。
- renderer 不持有打印机凭据，也不直接连接局域网设备；设备控制由本地执行端承担，并保留单台设备的单一写入责任。
- 企业OIDC由Keycloak或客户已有IdP接入；[Keycloak官方OIDC说明](https://www.keycloak.org/securing-apps/oidc-layers)支持标准身份集成。登录成功只确认身份；实际组织成员、订单/设备/批准权限仍由Autumn后端检查。
- 用户RBAC角色与Agent工作角色分开。Agent角色不能授予人类没有的设备权限。工艺批准、质检更正和设备启动应有明确业务策略与审计。

个人安装包登记独立于窗口的当前用户后台，监督本机 API、worker 与 Edge；企业服务器和现场端分别部署。设备租约、任务事实与恢复不能依赖 renderer/main 内存。桌面退出不取消设备任务，更新不能打断在途提交。本地 HTTP 使用受保护发现记录、实例认证与端点权限，不能因为绑定 127.0.0.1 就开放无鉴权设备控制。

### 7. 验证与运维

- Python用pytest；renderer 用Vitest/Testing Library（按实现时兼容版本固定），关键订单/审批/试验流程用Playwright。桌面安装、登录回调、preload 权限、GPU预览、退出与恢复应测试真实打包后的 Electron，不能只测 Vite 开发页后声称桌面集成通过。
- Three.js/R3F预览要有小样件、坐标与版本测试；浏览器截图不能代替几何正确性或实物检查。
- 日志从首期结构化输出并关联task/order/slice/job/trace ID。OpenTelemetry逐步接入trace与metrics；先不部署完整多套可观测集群。参见 [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)。
- 后端与数据库可用Linux Docker Compose；Windows本地执行端单独安装和版本管理，不因服务容器化就假定局域网发现、GPU或硬件工具完全相同。
- 可用uv管理Python依赖、pnpm管理前端；实际版本、引擎/插件和本地执行端二进制要锁定并有升级验证。

### 8. 起步、延后与不采用

**完整设计基线：** 四应用三公共包、Python/FastAPI、受控工具、模型/切片 artifact、Electron 构建分发主链、React/TS、Three/R3F、受限 IPC、授权与日志；个人随包 SQLite/本地后台，企业 PostgreSQL/迁移与 Celery/Redis。个人用户无需企业基础设施；具体安装、裁剪与验收见部署设计。

**有条件加入：** TanStack复杂表格、Zustand、React Flow、pgvector、SeaweedFS、Keycloak、完整OpenTelemetry后端、Redis缓存。

**首期不采用：** Next.js SSR、Electron Forge 第二套打包主链、双3D引擎、Kubernetes、微服务拆分、专用向量库集群、同时部署多套队列、MinIO归档仓库作为默认新存储、R3F v10 alpha、builder27/updater7 alpha。

上述取舍是针对当前产品目标的设计判断，需在实际大模型、G-code体积、设备网络与组织身份环境中验证，并不是各项目质量的普遍排名。

### 9. Electron 项目快照与唯一构建链

| 项目 | Star 约数 | 本次核实的稳定发行 | 许可证 | 决定 |
| --- | --- | --- | --- | --- |
| [Electron](https://github.com/electron/electron) | 123.6k | [45.1.0，2026-10-27](https://github.com/electron/electron/releases/tag/v45.1.0) | MIT | 桌面壳候选；随受支持稳定版升级 |
| [electron-vite](https://github.com/alex8088/electron-vite) | 5.6k | [6.0.0，2026-10-14](https://github.com/alex8088/electron-vite/releases/tag/v6.0.0) | MIT | 开发与 main/preload/renderer 构建 |
| [electron-builder](https://github.com/electron-userland/electron-builder) | 14.7k | [26.18.1，2026-10-26](https://github.com/electron-userland/electron-builder/releases/tag/electron-builder@26.18.1) | MIT | 打包与安装器；27仍预发行 |
| [electron-updater（同一仓库）](https://github.com/electron-userland/electron-builder/tree/master/packages/electron-updater) | 不重复计 Star | [6.8.12，2026-10-26](https://github.com/electron-userland/electron-builder/releases/tag/electron-updater@6.8.12) | MIT | 与 builder 配套更新；7仍预发行 |
| [Electron Forge](https://github.com/electron/forge) | 7.2k | [8.0.1，2026-09-29](https://github.com/electron/forge/releases/tag/v8.0.1) | MIT | 调研对照，不加入主链 |

**选 electron-vite → electron-builder → Windows NSIS，应用内使用 electron-updater。** electron-vite 处理开发服务器、热更新与三个进程入口；builder 处理发行文件、安装器与更新元数据。二者职责互补，[electron-vite 官方发行指南](https://electron-vite.org/guide/distribution)有对应集成方式。Forge 也能承担项目工具链，但不再与其并行维护另一套 make/package 配置。当前 [Forge Vite 插件官方页](https://www.electronforge.io/config/plugins/vite)仍标为 experimental，并提醒次版本可能有破坏变更，不能仅因 Forge 是官方工具就把该插件描述成稳定保证。

版本候选为 Electron45.1.0、electron-vite6.0.0、Vite8.3.5、builder26.18.1、updater6.8.12，renderer沿用React19/R3F9。这里只核实发布与声明范围，尚未安装、建立锁文件、运行打包或完成兼容性测试。electron-vite6 的 [package.json](https://raw.githubusercontent.com/alex8088/electron-vite/v6.0.0/package.json)声明 Node `^20.19.0 || >=22.12.0`、Vite6/7/8；应选受维护的构建 Node LTS 并验证交集，不能把最低支持版本当当前推荐运行环境。

**构建 Node 与 Electron 内置 Node 分开。** pnpm/Vite/打包器使用开发机或CI的Node；main运行Electron自带Node；sandbox preload只有受限能力，renderer没有Node。升级开发机Node不会升级已安装应用内的Chromium/Node。Python、Orca与几何原生库是独立的外部运行时，不应塞进renderer或尝试当Electron ABI原生模块加载。可执行资源通过受控 extraResources 放在ASAR外，按系统/架构分别打包、校验与记录版本；源模型、凭据与工作目录放在用户数据/受管存储，避免写安装目录。依据：[Electron进程模型](https://www.electronjs.org/docs/latest/tutorial/process-model)、[electron-vite发行指南](https://electron-vite.org/guide/distribution)。

### 10. 桌面安全与凭据边界

遵循 [Electron security 官方建议](https://www.electronjs.org/docs/latest/tutorial/security)及[contextIsolation说明](https://www.electronjs.org/docs/latest/tutorial/context-isolation)，以下为本项目设计要求：

- 显式配置 `nodeIntegration:false`、`contextIsolation:true`、`sandbox:true`，保留 `webSecurity`，限制CSP与权限请求。
- preload 经 `contextBridge` 仅暴露类型化业务方法，例如选择模型、读取批准任务、订阅指定任务事件。不要直接暴露 `ipcRenderer`、shell、任意文件路径读写、任意命令或通用channel发送器；事件回调不透传Electron事件对象。
- main校验每个IPC的sender/frame origin与所属webContents，并验证schema、资源归属和参数上限；接口白名单不能替代后端审批与组织权限。模型/G-code文件内容是输入数据，不能转化为可执行脚本或渲染HTML。
- 生产renderer加载应用随包发布的本地资源，评估受限自定义app协议及路径边界。拒绝非允许导航/新窗口；文档链接通过校验scheme/host后交系统浏览器，不能对用户输入直接 `openExternal`。远程帮助或登录页面不获得preload能力。

凭据仅由main或Edge按职责持有。main用 `safeStorage` 配合受限用户数据目录保存允许持久化的refresh token，注销时清理；设备密钥留在Edge。Windows DPAPI不能防御同一登录用户下所有其他程序。[safeStorage官方文档](https://www.electronjs.org/docs/latest/api/safe-storage)当前已将同步API标为Electron45起弃用，应使用 `isAsyncEncryptionAvailable`、`encryptStringAsync`、`decryptStringAsync`。Linux依赖secret service；要验证实际provider，`basic_text`或不受保护fallback不能被当成安全加密，即使available返回true，也应拒绝持久化敏感token并采用会话内保存。不要通过开启硬编码密码fallback来让登录“成功”。

### 11. Windows 发行、更新与后续验证

首个桌面发行目标为 **Windows x64 NSIS完整安装器**，优先按用户安装；车间服务/企业软件分发按机器安装属于后续独立部署方案。桌面壳和Edge有独立版本及协议兼容检查，更新包不携带打印机凭据。其他系统只在实际验证后宣布支持。

由CI产出版本化安装器、校验与更新元数据，正式包进行Windows签名；发布凭据留在CI，更新使用HTTPS并验证发布者。签名不能替代灰度/回滚设计。默认关闭在生产作业中自动退出安装的行为，在空闲且用户确认重启时安装，并保留手动下载安装方式。依据：[Electron代码签名](https://www.electronjs.org/docs/latest/tutorial/code-signing)、[builder26更新文档](https://www.electron.build/v26/docs/features/auto-update/)。

明确使用 `electron-updater`，不要混成Electron内置 `autoUpdater`：二者平台能力、协议与配置不同。builder当前默认网站已有v27文档；本方案候选为builder26/updater6，不能直接套用v27/updater7新增的 `autoInstallEvent/onNextLaunch` 或签名manifest行为。Electron[内置autoUpdater文档](https://www.electronjs.org/docs/latest/api/auto-updater/)说明其不内建Linux更新；未来Linux要另外决定发行包与更新机制。

实现阶段必须验证：干净Windows机器安装/卸载；已签名旧版升新版；发布元数据与文件不完整/校验失败；断网与代理；登录取消/错误回调/失效token；Linux若扩展时的secret-store缺失；大模型显存与内存；沙箱IPC越权；Edge异常退出恢复；桌面退出或升级时已提交作业不重复发送。这是待做验证清单，本次没有声明集成测试通过。

## C. Orca、几何与设备

核验日期：2026-10-29（Asia/Shanghai）。仅研究，未编译 Orca、未切片样件、未连接设备。Star 为 GitHub 页面约数，不是全站排名；版本为本次读取可见值，安装前须重新核验。公开 GitHub API 直连被 403 限流，未借用任何私有令牌；不能可靠取得的精确日期不补造。

### 1. 项目关注度、发布与许可证快照

| 项目 | Star 约数 | 最近可核验版本/活动 | 仓库声明许可证 | 用途判断 |
| --- | --- | --- | --- | --- |
| [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) | 16.2k | API latest 为 [v2.4.2](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.4.2)，published_at=2026-07-07；本地源码 2.5.0-dev | AGPL-3.0 | 实际切片引擎，固定版本验收 |
| [Trimesh](https://github.com/mikedh/trimesh) | 3.7k | [Release 5.2.0](https://github.com/mikedh/trimesh/releases)，页面显示 24 Oct | MIT | 首选基础读取、几何测量与拓扑检查 |
| [Manifold](https://github.com/elalish/manifold) | 2.4k | [v3.5.4](https://github.com/elalish/manifold/releases)，页面显示 25 Sep | Apache-2.0 | 后续经验证的流形实体布尔操作，不作为通用坏网格修复器 |
| [PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab) | 984 | [v2025.7.post1](https://github.com/cnr-isti-vclab/PyMeshLab/releases)，资产日期 2026-01-30 | GPL-3.0 | 独立进程的可选检查/候选修复后端，逐项测滤镜能力 |
| [Moonraker](https://github.com/Arksine/moonraker) | 1.5k | [master 提交页](https://github.com/Arksine/moonraker/commits/master/)可见 2026-09-09，以及准备 0.11.0 的提交；旧 Releases 标签不代表当前维护版本 | GPL-3.0 | 有 Klipper 测试设备时优先做直接接入 |
| [OctoPrint](https://github.com/OctoPrint/OctoPrint) | 9.2k | [发布页](https://github.com/OctoPrint/OctoPrint/releases)：Latest 稳定 1.11.8；另有 2.0.0rc7，页面显示 20 Oct 且明确 Pre-release | AGPL-3.0 | 若首台设备已使用它则优先接；不为追最新默认用 RC |
| [Spoolman](https://github.com/Donkie/Spoolman) | 3.0k | [v0.27.0](https://github.com/Donkie/Spoolman/releases)，页面显示 25 Sep | MIT | 后续耗材卷库存 Adapter；库存真源只能选一处 |
| [Obico server](https://github.com/TheSpaghettiDetective/obico-server) | 1.9k | [release 分支提交页](https://github.com/TheSpaghettiDetective/obico-server/commits/release/)可见 2026-07-11；[Releases](https://github.com/TheSpaghettiDetective/obico-server/releases)没有发布条目 | AGPL-3.0 | 后续订阅异常证据，不能替代实物质检 |

部分 GitHub 发布摘要省略年份，表中保留原页面日期字符串；不能用标签中的年份代替实际发布时间。精确版本锁定需要实施时记录 tag、commit、二进制哈希与完整依赖。许可证列仅记录仓库页面声明，第三方依赖、插件、模型、分发和服务化需单独核查，不由“独立进程”推导法律结论。

### 2. 建议组合及引入顺序

**首版：固定 Orca 二进制 + Trimesh + 受控本地执行端。** 先读取、检测、切片并保存事实。复杂修复暂为明确的未支持项或人工处理。

**第二步：加入隔离候选修复后端。** 可评估 PyMeshLab；必须通过特定缺陷样件和尺寸/部件变化检查，才对用户展示可用操作。Manifold 仅在需要布尔操作且满足输入条件时引入；不同时安装 CGAL、libigl 和多套大后端。

**设备阶段：模拟 Adapter + 一个真实后端。** 测试设备是 Klipper 则接 Moonraker；设备现有 OctoPrint 则先接 OctoPrint。实际机器生态未给出，因此第一真实 Adapter 仍是有条件的选定，不把任一后端当全品牌统一协议。

### 3. 模型检查与修复的能力矩阵

| 检查/操作 | 首选实现 | 必须保留的限制 |
| --- | --- | --- |
| 格式解析、空模型、非法面索引、坐标非有限值 | 文件验证 + Trimesh + 格式级检查 | 对不可信文件设字节、解压、面数与资源上限；解析成功不是模型有效证明 |
| 包围盒、面积、体积、部件与变换 | Trimesh | 单位来源另存；STL 无明确单位时请用户确认。开口/错误模型的体积不作为精确成本或质量依据 |
| 水密性、绕序、边邻接数量、退化/重复面 | Trimesh 检查与经验证的小型检测实现 | “不是水密”与“所有非流形顶点均排除”不是同一结论；各项分别返回 pass/fail/unknown/unsupported |
| 法线方向修正与小孔候选补洞 | Trimesh 受限 repair | [官方 repair 文档](https://trimesh.org/trimesh.repair.html)说明原位修改、补洞对非凸孔洞可能产生错误；始终拷贝到新版本后执行 |
| 大孔补洞/更多网格滤镜 | 可选 PyMeshLab worker | [滤镜文档](https://pymeshlab.readthedocs.io/en/latest/filter_list.html#meshing-close-holes)的防自交是启发式，不能承诺所有坏模型恢复正确实体 |
| 完整自交检测、非流形顶点、复杂拓扑修复 | 独立功能验收，初始 unsupported | 不用 is_watertight 代替自交检测，不用任意自动补洞证明零件形状正确 |
| 实体布尔组合 | 按需 Manifold | [官方 README](https://github.com/elalish/manifold/blob/master/README.md)明确非流形输入会返回错误状态；manifold 输出性质不代表输入任意可修 |
| 薄壁、悬空、可制造性、尺寸与强度 | 后续专门算法、切片检查及实际测量/试打 | 首版未实现的分析明确 unavailable；不能由语言模型凭截图声明检查通过 |

每个报告项含检查器名/版本、输入哈希、单位、结果、位置/数量（若支持）、依据和限制。保留模型部件与场景变换，不能把多个壳体一律当碎片删除。

修复生成新的 ModelRevision，保存原件、操作参数、前后报告、包围盒/体积/部件变化和可用的表面偏差指标；只有模型负责人确认后才进入候选工艺。未经有效性验证的“零缺陷”结果不能批准。量纲与容差由业务输入决定，不硬编码统一百分比。

### 4. Orca Interface 与执行隔离建议

建议在 Slicer 模块的 Interface 内部集中完成：输入和配置验证、能力探测、工作目录、进程执行、结果解析与证据收据。调用方提交模型引用与有效配置快照，获得统一结果或明确错误，不散落拼接 CLI。

- Adapter 至少有真实 Orca 和用于流程测试的 fake，fake 结果不能显示成真实切片。
- 固定 engine version、binary digest、资源/预设版本；初次以目标二进制的实际 `--help` 与标准样件建立 capability manifest。
- 当前[官方 CLI](https://www.orcaslicer.com/wiki/cli/cli_mode)和[CLI Actions](https://www.orcaslicer.com/wiki/cli/cli_actions)可参考，但不据当前网页推断旧稳定版或本地 dev 已包含所有导出和插件功能。
- 上传 3MF 保留原文件；按 ZIP 路径、解压资源上限验证，区分项目配置、网格/对象变换和已切片文件。不能把任何 3MF 自动当作可信可执行作业。
- 机器/工艺/耗材配置继承解析后保存完整有效配置与来源，配置变化使旧切片需要复核。
- 一次运行独立 workspace 与 datadir（以实际版本支持为准），不写用户全局配置或系统预设；阻断继承外部未知后处理脚本和未获准起止 G-code。
- 使用参数数组启动进程，限制运行身份、文件/网络、内存/CPU/时间，终止时清理整个子进程树。Windows 本地需 Job Object/进程级限制等真实实现；普通 subprocess 与 Docker Desktop 安装并不自动构成完整沙箱。
- 输出保留退出码、警告、stdout/stderr、最终文件哈希和实际估算字段。未支持的统计字段为 null/unknown，不让模型补全。
- 切片成功仍需目标版本 Orca 打开与标准样件验证。用于报价的估算与实测分别记录，不能默认所有输出字节跨平台一致。

#### 本地代码只读核验

路径 `D:\project\OrcaSlicer-main\OrcaSlicer-main` 已由父任务确认；本次先读根 AGENTS.md。相关 src 无额外 AGENTS；未读写 tests。

- `version.inc`：`2.5.0-dev`，未编译，不假设等同上游稳定。
- `src/libslic3r/PrintConfig.cpp:11678` / `:11954`：CLI 动作及配置定义，load_settings/load_filaments 在 `:11980` / `:11986`。
- `src/slic3r/Utils/PrintHost.cpp:58` / `:68` / `:70` / `:73`：OctoPrint、Obico、SimplyPrint、Moonraker Adapter。
- `src/libslic3r/GCode.cpp:2223` / `:2226`：局部成本累计包括耗材及配置的 time_cost，企业报价层需防止重复计机时，还需另算人工等项目。
- `docs/gpl-mesh-repair-cli-0-to-1.md` 是现有设计说明，不能作为某个可运行修复 worker 已通过验收的证明；本轮未检查或改动独立 mesh-repair-worker 项目。

### 5. Windows/局域网执行端与设备 Interface

建议中心部署业务模块、任务数据库与文件；现场机器运行 Edge Worker，首期可同机，后续分开部署。Edge 使用已登记的 site/device scope 和短期租约领取动作，通过受限出站连接回传事件。浏览器不直连打印机，不保存设备 API Key，不要求把局域网设备暴露公网。

#### 查询与动作

- `describe_capabilities(device)`：逐项声明上传、队列、启动、暂停、继续、取消、历史/状态的实测支持情况。
- `observe(device)`：回传状态、来源时间和新鲜度；过期数据不能满足启动前置条件。
- `submit/observe_action(action_id)`：按获准的动作类型、文件哈希和目标设备执行并回读，未知结果保留 reconcile 状态。

这是建议 Interface 形状，具体字段实施时按能力样例固定。模型只能提出业务 Action，不能直接调用任意网络地址或发送原始 G-code。

#### 为什么有 Klipper 时优先 Moonraker

[Moonraker 官方 Printer API](https://moonraker.readthedocs.io/en/latest/external_api/printer/)具有查询/订阅及启动、暂停、继续、取消，明确要求 Klippy 已连接，很多操作还要求 ready。它适合直接观察现场状态，但不提供所有外部业务的幂等保证。

[OctoPrint 文件 API](https://docs.octoprint.org/en/main/api/files.html)具有上传、文件查询、权限与选取打印等能力，适合现有部署；最新 RC 不能未经验证成为生产基线。一个机群可逐步增加 Adapter，但单台机器的打印调度权只能有明确的一个拥有者。

#### 单写者与未知结果

- 物理写动作先创建数据库 Action，包含 action_id、device_id、tenant/site、文件和批准版本，再由唯一设备执行通道领取。
- 同设备动作串行化，并在本地持久化执行日志和结果；中心租约和本地去重共同使用，不能仅靠临时内存锁。
- 下发前核对授权、工艺版本、喷嘴、材料、清床、设备空闲与状态新鲜度。approved 状态不等于已执行。
- 请求超时后先查远端文件、设备当前任务/历史和本地日志。不能关联到原作业时转人工核查，禁止盲目再启动。
- 单写者保证只覆盖受控通道；原生面板或其他农场系统仍可能动作，检测到外部占用就退出/升级，不能承诺排除所有现场操作。
- 同机使用 SimplyPrint、Printago 或原厂调度时，要选它或 Autumn 作为调度事实来源，避免两个系统同时自动排队开打。
- 打印完成、清床、取件、质检、合格数量各自确认。远程暂停/取消接口不等同机器级安全保证。

### 6. 后续模块取舍

Spoolman 可作为库存 Adapter，使用其外部 spool_id 关联本地工艺和批次。只选一套库存作为事实来源，明确实际消耗、估算消耗、预留、退料和纠正事件；不能同时让设备、Autumn 与 Spoolman 无协调扣减。

Obico 作为观察来源接入其告警与证据；若它配置了自动暂停，要把该行为和执行者记录到设备状态中，避免另一个流程马上恢复。摄像头断流/遮挡为 monitoring_unavailable，不是“无异常”。是否自动暂停由明确设备策略控制，不放任两个 Agent 争夺控制。

#### 首批可评审验证项

1. 一份正常模型、一份小孔模型、一份非流形/自交样例和预期检查能力矩阵。
2. 目标 Orca 版本的两套有效配置，实际切片与文件/估算回读。
3. 修复前后尺寸、部件和形状差异及模型负责人确认。
4. fake 设备的重复请求、超时、外部占用、断网恢复状态机。
5. 获准真实设备的一次仅上传与一次启动，能回读同一作业。
6. 在缺测量/无清床/余量未知时保持等待，不编造完成。

## D. 开发工具、排产与部署补充

| 项目/依据 | 官方来源 | 本项目用途与限制 |
| --- | --- | --- |
| uv（约 91.3k Star） | [仓库](https://github.com/astral-sh/uv)、[项目管理](https://docs.astral.sh/uv/guides/projects/) | Python 环境与锁文件；原生库平台支持仍须实测 |
| Ruff（约 50.3k Star） | [仓库](https://github.com/astral-sh/ruff) | Python 检查与格式化；不能代替业务/设备契约测试 |
| Celery（约 29.1k Star） | [仓库](https://github.com/celery/celery)、[Redis broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html) | Linux 后台片段；重投可能重复，Windows 原生端使用独立执行协议 |
| OR-Tools（约 14.3k Star） | [仓库](https://github.com/google/or-tools)、[Job Shop](https://developers.google.com/optimization/scheduling/job_shop) | 真实约束优化需要时接 CP-SAT；LLM 不能宣称求出了最优生产计划 |
| Node.js | [官方版本表](https://nodejs.org/en/about/previous-releases) | 选择受维护 LTS，构建 Node 与 Electron 内置 Node 分别管理 |
| Redis 许可 | [官方许可说明](https://redis.io/legal/licenses/) | 固定发行版并核查对应条款；不能把所有 Redis 版本一概写成 BSD 许可 |

Node 版本表本次显示 24 与 26 为 LTS。当前设计先用 Node 24 LTS 验证构建链，26 经验证后升级；这与 Electron 自带 Node 的版本无直接替换关系。

Redis 8 及以后存在 RSALv2、SSPLv1、AGPLv3 许可选择；应按实际采用发行版、部署及分发方式核查。该事实不等于对 Autumn 商业发布许可义务作出结论。

## E. 进入实现的验证门槛

1. 记录目标 OS/架构、工具/框架版本、锁文件、引擎哈希、模型样件与资料许可。
2. 完成实际 Windows Electron 安装包、OIDC 回调与受限 IPC，核对 renderer 无特权依赖。
3. 用真实 Orca 样件核实 CLI、配置继承、结果解析和可取消性，逐项验收几何检查/修复。
4. 在 PostgreSQL 和 Linux worker 上注入派发失败、竞争恢复、消息重投、等待与取消；窗口关闭不改变业务事实。
5. 得到明确测试设备后才实现首个真实 Adapter，先测只读和上传，再验证获准动作及未知结果核查。
6. 软件测试、实际切片、设备作业与实物质量分别留证，未支持或未验证能力不显示为成功。
