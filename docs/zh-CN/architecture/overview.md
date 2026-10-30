# 架构总览

[English](../../en/architecture/overview.md) | 简体中文

状态：产品设计基线，整理于 2026-10-30。个人模式工程基础已实现，[实现状态](../engineering/getting-started.md)区分当前行为与目标架构。产品目标见[需求](../product/requirements.md)，用户行为见[功能规格](../product/functional-spec.md)。本文拥有模块、技术、数据和接口设计；[运行部署](runtime-and-deployment.md)、[Agent](agent-and-tools.md)和[仓库结构](repository.md)分别维护其专属内容。

技术版本和外部项目资料仍沿用 2026-10-29 的[调研快照](../research/technology-selection.md)，本次迁移未重新核验发布版本，也不代表集成测试通过。

## 设计结论与假设

采用 **Electron 桌面客户端 + Python 模块化控制端 + 独立现场执行端**，提供完整的个人本地和企业服务器两种部署配置。四个应用（desktop、api、worker、edge）和三个公共包（control-plane、contracts、sdk-ts）位于同一仓库；职责按目录区分。完整目录与依赖见[仓库结构](repository.md)，部署及生命周期见[运行部署](runtime-and-deployment.md)，验收见[验证计划](../engineering/validation.md)。

- 目标是 FDM 工艺验证与小批量生产，先验证一组设备/喷嘴/材料和固定订单样例。
- 按用户要求以 Electron 桌面端为主要交付，先 Windows，随后分别验证 macOS/Linux 打包；渲染进程不直接持有打印机凭据。
- 个人版安装后配置模型 API 即可使用：本机 API/worker、SQLite 业务与持久队列、SQLite checkpoint、本地文件，不要求服务器或开发环境。企业版使用服务器 API/Linux worker、PostgreSQL、Celery/Redis 和企业身份。
- 两种模式共用业务和 LangGraph 图/角色/工具；Agent 在所选控制端的 worker 编排。现场端只执行实际工具和设备动作，无独立大模型 Key；模型推理位置由 API 地址决定。
- 项目尚未得到实际打印机清单。第一个真实设备 Adapter 依据测试设备选择，不能预设所有机器都支持 Moonraker 或 OctoPrint。
- 所有版本号是调研/兼容性候选，实际依赖以引入阶段验证后的锁文件、镜像摘要和二进制哈希固定。

## 全部技术的选定用途

| 层 | 基线选择 | 用途与约束 |
| --- | --- | --- |
| Python 运行与依赖 | Python 3.12 的受支持补丁 + uv + uv.lock | 延续指南，先验证几何库原生轮子和工具兼容 |
| 桌面前端 | Electron + React 19 + TypeScript + electron-vite + pnpm | 主进程、preload 与 renderer 分开构建；渲染层使用 Vite，首期不需要 SSR |
| 桌面分发 | electron-builder + electron-updater | 验证安装包；完善签名、更新渠道、安装与恢复，不并用 Forge 主构建链 |
| 3D | Three.js + React Three Fiber 稳定 v9 | 模型、打印床、朝向、检查标记与候选比较 |
| UI 与数据 | shadcn/ui、Tailwind、TanStack Query；复杂清单按需 TanStack Table | 查询状态和视图状态分别管理 |
| 前端构建环境 | Node.js 24 LTS 基线；26 LTS 经工具链验证后可升级 | 构建 Node 与 Electron 内置 Node/Chromium 分别记录；electron-vite 的 Vite 版本按兼容范围选择，不直接强制最新版 Vite |
| 业务接入 | FastAPI + Pydantic + Uvicorn | 输入校验、权限、命令、查询、SSE 和文件访问 |
| 持久化 | 个人 SQLite；企业 PostgreSQL 18 候选；SQLAlchemy 2.x + Alembic | 两种数据库分别验证迁移、事务与并发，企业 psycopg 依赖不进入个人包 |
| Agent | 单一 LangGraph 运行体系 + 经验证的模型供应商 Adapter | 简单任务使用小图，增加委派、分支、等待与恢复 |
| 后台执行 | 个人本地持久队列；企业 Linux Celery + Redis broker | 共用有界执行、幂等和恢复语义，每工作区只启用一个后端；Windows 本地不运行 Celery |
| 现场端 | Python 独立进程 + 本地 SQLite 动作日志 + 受限工具子进程 | 先本机执行，完善身份、领取与设备动作 |
| 切片 | 固定并验收的 OrcaSlicer 稳定二进制 | 当前候选 v2.4.2，2.5 Alpha/本地 dev 作为后续插件研究 |
| 几何检查 | Trimesh + 明确覆盖的小型检查逻辑 | 报告逐项给出通过/失败/未知/不支持 |
| 网格修复 | 受限小修复；复杂情况按需隔离 PyMeshLab | 通过缺陷样件验收后才启用，不默认复杂拓扑可修 |
| 设备 | Fake + Moonraker 或 OctoPrint 中一个真实 Adapter | 按实际设备选择，声明能力矩阵 |
| 文件 | 本地 ArtifactStore；企业部署复用已有 S3 或评估 SeaweedFS | 本地先行，验证 S3；不先搭分布式存储集群 |
| 身份与授权 | 个人所有者身份与本机认证；企业 OIDC（Keycloak 或已有 IdP）+ RBAC/资源策略 | 个人无需企业账号，确认仍记录人和版本；企业验证成员、资源及审批权限 |
| 知识检索 | 个人 SQLite 文本检索；企业 PostgreSQL 全文检索，可选 pgvector | 共用资料授权和引用语义，分别验证召回；基础功能不要求 embedding Key 或本地 GPU |
| 生产计划 | 先确定性兼容筛选和可解释启发式；达到需要时 OR-Tools CP-SAT | LLM 提出约束，实际可行性由程序检查 |
| 耗材与监控 | 本地材料台账；Spoolman、Obico/Gadget 按需接入 | 各自明确唯一数量事实来源和设备控制权 |
| 验证 | pytest、Vitest、Testing Library、Playwright | 业务、工具、Electron 窗口与 IPC、3D 逐层测试；实物另行验证 |
| 质量与运维 | Ruff、类型检查、OpenTelemetry、结构化日志、Docker Compose、CI | 基础检查从首期开始，遥测后端按规模接入 |

Node LTS 依据见[官方版本表](https://nodejs.org/en/about/previous-releases)。其余选型与本次版本快照见[调研](../research/technology-selection.md)；精确补丁尚未形成经过安装验证的依赖集合。

## Module、Interface 与 Seam

按业务职责形成深 Module：调用方学习少量稳定 Interface，配置继承、进程处理和设备差异集中在对应 Implementation。Seam 只设在实际有变化的位置，例如真实 Orca/Fake、真实设备/Fake、本地/S3 文件存储；不会为每个类都增加抽象层。

| Module | 对调用方的 Interface 草案 | 隐藏的 Implementation 复杂度与必须保证的约束 |
| --- | --- | --- |
| Ordering | `create_order`、`revise_requirement`、`get_fulfillment` | 套件、需求版本、首件计入规则、变更影响与合格缺口 |
| Model Preparation | `inspect`、`propose_repair`、`accept_revision` | 文件验证、单位、检测覆盖、修复候选与几何差异；原件不覆盖 |
| Slicing | `submit_slice`、`get_slice_result`、`cancel_slice` | 引擎探测、配置继承、隔离目录、资源、结果解析与缓存收据 |
| Process Validation | `record_trial`、`record_inspection`、`approve_process` | 验证证据、适用条件、批准版本与条件变更复核 |
| Production | `plan_batch`、`propose_action`、`reconcile_action` | 兼容选择、设备占用、准备确认、批准与单写者动作账本 |
| Quality | `classify_output`、`assess_deficit`、`request_reprint` | 待检/合格/返工/报废数量变化、去重、套件与交付约束 |
| Agent Runtime | `start_run`、`resume_run`、`cancel_run` | 模型、图版本、委派、工具授权、预算、中断与执行租约 |
| Knowledge | `ingest`、`search`、`resolve_evidence` | 版本、权限过滤、召回、证据定位与更正 |
| Identity & Policy | `resolve_actor`、`authorize` | 组织成员、角色、资源范围、授权时效、人员与现场端身份 |
| Artifacts | `put`、`open_authorized`、`describe` | 完整上传、hash、不可变对象、派生关系、访问与回收 |

这是待实现的 Interface 约定，方法还包含调用顺序、错误模式、授权和性能约束，不只是一组函数名。测试通过同一 Interface 覆盖业务行为；新增 Adapter 应通过相同契约测试。

跨 Module 的事务由用例协调；不让任一 Module 直接修改其他 Module 的私有表。在当前工作区的同一业务数据库内完成原子操作（个人 SQLite、企业 PostgreSQL），避免不必要的远程一致性问题。

## 业务对象与持久化

个人正式业务版本使用 SQLite，企业使用 PostgreSQL；现场端动作日志在两种模式中均独立保存于 SQLite。业务存储、Agent checkpoint 与现场日志有不同生命周期，不通过复制文件隐式迁移运行任务。SQLite 采用短事务、唯一约束和乐观版本，PostgreSQL 按需使用行锁与 RLS；各自迁移、并发与恢复分别验收。

| 记录组 | 主要对象 | 一致性要求 |
| --- | --- | --- |
| 身份 | organizations、memberships、roles、resource_grants、edge_agents | 所有业务 ID 解析后重新校验当前成员和作用域 |
| 需求 | orders、order_lines、kit_components、model_revisions | 模型与验收要求有版本，旧版不得悄悄顶替新版 |
| 工具成果 | artifacts、profile_snapshots、slice_runs、check_reports | 输入/配置/二进制/结果关联不可变；工具结果区别模拟和实际 |
| 工艺 | candidates、trials、inspections、validated_processes | 批准固定具体版本及证据；变更触发复核 |
| 生产 | batches、print_jobs、device_observations、device_actions | 打印计划与实际动作独立；设备观测有来源时间和新鲜度 |
| 数量 | output_lots、quantity_transitions、order_allocations | 同批实物分类变化不增加总产出，分配不超合格可用量 |
| 异常 | incidents、reprint_requests、dispositions | 补打关联真实缺口与原异常；不等同旧动作重试 |
| 交互 | tasks、agent_runs、steps、task_events、approvals | 乐观版本、防并发恢复、批准对象及参数固定 |
| 执行交接 | outbox、run_leases、edge_commands、action_receipts | 唯一业务标识、事务写入、重投核对、结果未知可追查 |

主记录用明确标识和外键关联；数字数量有范围检查，分类转换与订单分配有唯一幂等键。更新使用事务和行锁/乐观版本，不能只靠模型或前端检查。

数量模型示例：某盘计划 12 个卡扣，实际确认 12 个，其中 8 合格、2 待检、2 报废。把 2 个待检转合格后是 10 合格、2 报废，总量仍为 12；收到重复质检事件不得变成 14。只有被分配到订单、版本匹配且验收通过的数量才能抵扣需求。

这一设计用当前状态表加可追溯转换记录实现，不在首期建立全系统事件溯源架构。

## Orca、模型检查与修复

### 不可变输入与切片收据

一次切片固定模型版本、模型/配置 hash、有效配置、引擎二进制与资源版本、目标机器条件和输出协议。缓存键还需覆盖朝向/布局、对象覆盖、预处理与解析器版本；缓存命中保留来源，不伪装成新一次实际执行。

每次执行独立工作区和可用版本支持的独立配置目录，禁止写用户全局预设。配置继承与覆盖由适配器明确处理，3MF 项目私有设置不能被悄悄丢弃或误当作当前现场机器配置。

Orca 用子进程参数数组启动，保存退出码、日志、警告和产物；按目标版本探测能力。估时、耗材、成本和预览字段缺失为 unknown，不能从模型回答补齐。报价层核查引擎成本组成，再补人工、后处理和损耗，避免重复计算机时。

### 检测覆盖

首选 Trimesh 读取与基础几何/拓扑事实，修复始终生成候选新版本。

| 项目 | 首期约定 |
| --- | --- |
| 可读性、空模型、非法索引、非有限坐标 | 格式验证加明确检测，超限或无效停止 |
| 单位、包围盒、部件与变换 | 保留来源与对象关系；单位未知需确认 |
| 水密、面绕序、退化/重复面、边邻接 | 各检查项独立报告；水密不等于所有拓扑问题均排除 |
| 法线修正、小孔修复 | 在拷贝上受限尝试，前后差异和人工确认必需 |
| 完整自交、非流形顶点、复杂孔洞修复 | 独立验收后才开放，初期 unsupported |
| 薄壁/悬空/强度/尺寸质量 | 按专门算法和试打/测量验证，不从截图或解析成功推出 |

PyMeshLab 是复杂检查/修复的可选隔离后端；Manifold 仅在满足输入条件的布尔操作需要时加入。修复可能改变尺寸、配合和预期孔洞，模型负责人必须看到新版本和差异；无法可靠修复则请求人工处理。

### 隔离边界

检查压缩路径、文件类型、解压尺寸、对象/面数与资源，禁止越界与任意后处理脚本。CPU/内存/运行时长、网络和文件权限由实际执行环境限制。

Windows 现场端需分别实现低权限身份/文件 ACL、进程树与 Job Object 资源控制等措施；普通 subprocess 或安装 Docker Desktop 不自动构成完整沙箱。异常终止后清理子进程、临时数据和租约，但保留诊断证据及不可变输入。

## 文件、3D 与 G-code 预览

业务数据库保存文件元数据、组织、权限、hash、对象键、长度、类型、派生关系与状态；原始模型、G-code、照片和大日志放 ArtifactStore。

- 本地存储采用受管理目录，访问只用已授权引用，不能拼接用户绝对路径。
- 上传完成并校验后才变为可用成果；失败保留清理记录，孤儿对象按保留策略回收。
- 初期由受鉴权代理读取文件；后续直传/下载使用短时限定 URL，并明确撤权在过期前的限制。
- 企业 S3 先复用现有系统；SeaweedFS 作为自托管候选，验证所需分片、Range、校验、生命周期，不因“S3兼容”假定全语义一致。
- Renderer 使用 Three.js/R3F 展示派生模型、打印床与问题标记。原件到预览的坐标、单位与对象映射可追溯，降采样只影响显示。
- 3MF 显示不代表完整还原所有切片器私有数据；起止 G-code、设备宏和后处理配置单独审核。
- G-code 预览按已经实现的方言、层和移动/挤出类型加载；未知宏明确标记，不承诺首版达到 Orca 完整预览或机器仿真。
- 大文件解析用 Web Worker/后端派生，窗口渲染使用适当 BufferGeometry 与分层加载；具体字节/三角形预算经样件测试制定。

前端用 TanStack Query 管业务缓存，事件包含资源版本以去重/失效；URL/路由管理筛选和选择，React 管局部表单。只有出现真实共享视图状态才增加 Zustand，避免复制业务库。

## 身份、企业用户角色与 Agent 角色

个人模式创建本地工作区所有者，无需企业账号与 OIDC，但本机端点、文件及设备动作仍有明确身份和授权，批准保留人、版本及证据。企业正式账号通过 OIDC 接 Keycloak 或已有 IdP；桌面端采用系统浏览器的授权码 + PKCE，校验 state/nonce、回调范围、发行者、受众与时效，不把桌面程序当作可保密的 OAuth confidential client。以下组织权限矩阵适用于企业配置。

令牌生命周期由 Main 中受管理的会话处理，渲染层只拿所需身份摘要。持久凭据使用经过验证的 OS 保护能力；Electron safeStorage 在不同系统的后端保护不同，不满足条件时保留内存会话并要求重新登录，不退化为明文落盘。API 对每个命令仍检查当前组织成员与资源策略，UI 隐藏按钮不算授权。

建议起始权限矩阵如下，允许按组织组合角色并限定空间、订单、设备；系统管理身份默认不自动拥有业务批准权：

| 用户角色 | 订单维护 | 提议工艺/试打 | 批准工艺 | 准备/启动获准作业 | 实物判定/更正 | 排产与交付 | 账号/连接配置 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 操作员 | 查看获准订单 | 提交试打与观察 | 否 | 授权设备内允许 | 记录观察，不能代替质检 | 查看 | 否 |
| 工艺负责人 | 查看 | 允许 | 明确授权范围内允许 | 需另授设备操作权 | 查看证据 | 提供工艺条件 | 否 |
| 质检员 | 查看 | 提交质量问题 | 否 | 否 | 授权检查项内允许，保留更正理由 | 提供合格数量 | 否 |
| 订单管理员 | 允许 | 提出需求 | 否 | 需另授设备操作权 | 查看 | 允许，不能虚构验收 | 否 |
| 系统管理员 | 按资源策略 | 否 | 否 | 否 | 否 | 否 | 允许，敏感变更有审计 |

工艺批准、几何修复接受、设备动作批准和准备确认分别判断。岗位可以一人兼任，是否禁止自批由组织策略配置。Agent 工作角色的编辑和发布是另一种管理权限，不能通过修改提示词取得设备操作或审批权。

数据查询从 tenant/space/resource 条件开始。RLS 可作纵深保护，连接角色、表拥有者/绕过条件与事务级租户上下文必须测试，防止连接池串组织。checkpoint、检索、预览、对象下载和事件流也覆盖同一授权范围。

## 业务 Interface 与对外接口约定

以 `/api/v1` 提供类型化 JSON 命令/查询，Electron Main 消费接口；由 OpenAPI 生成/验证 TypeScript 类型。主要分组：

| 分组 | 例子 | 行为约束 |
| --- | --- | --- |
| 订单与模型 | orders、order-lines、model-revisions、imports | 上传完成、单位与版本确认分别记录 |
| 检查与切片 | inspections、repair-proposals、candidates、slice-runs | 异步提交返回 ID，读状态与取成果分开 |
| 试打与工艺 | trials、measurements、validated-processes | 批准固定输入版本与证据，不接受客户端自写通过 |
| 生产与质量 | batches、print-jobs、incidents、output-lots、reprints | 数量转换事务化，重复事件使用幂等键 |
| 设备与批准 | devices、observations、actions、approvals | 动作意图、批准、实际结果分别查询 |
| Agent | agent-roles、agent-runs、tasks、events | 角色版本固定；恢复与取消为显式命令 |
| 现场端 | edge/register、edge/commands、edge/receipts | 独立机器身份、限定 site/device，不使用员工全权限令牌 |

写命令支持业务幂等键与期望资源版本；版本冲突返回明确冲突及可重新读取的信息。事件含 task_id、递增 sequence、类型、资源版本、来源时间；重连补读并去重，不把连接中断当取消。

普通进度使用 SSE，设备高频观测先在现场汇总为业务变化。确需低延迟双向流再增加 WebSocket，长期事实仍写持久记录。摄像头视频不塞进普通任务事件或日志，按设备能力另行授权呈现。

## 知识、排产与外部产品的取舍

知识使用文档元数据和文本检索：个人使用 SQLite 检索 Adapter，企业使用 PostgreSQL；企业按真实召回需求选择 pgvector。相同资料集分别验收，不要求个人安装向量数据库或额外 embedding 服务。每次检索带工作区/组织/资料授权，引用正文回读再授权；召回不足只在同一授权集合内回退。

工艺资料、观察、假设和批准证据分别呈现。图像模型可建议检查位置或异常类型，未经测量的尺寸/强度字段保持未测。embedding 模型与视觉模型在实际中文术语和样件评估后固定，不默认昂贵模型或本地 GPU 是必需。

排产先做确定性的可执行性检查，再按交期/设备/材料/清床与值守安排生成解释清楚的计划。达到真实优化需求时用 OR-Tools CP-SAT；无解或超时给出阻塞/当前可行结果及局限，不宣称最佳。[官方 Job Shop 示例](https://developers.google.com/optimization/scheduling/job_shop)

Spoolman 若接入则明确选它或 Autumn 作为材料卷账本，不能两边同时独立扣料。Obico/Gadget 是异常观察来源，断流和未监控状态可见；自动暂停行为与责任方进入动作/观测记录，不由另一 Agent 立即无条件恢复。
