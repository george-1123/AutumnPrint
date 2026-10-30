# 从 0 到 1 的架构与功能评审

[English](../../en/research/architecture-functional-review-2026-10-30.md) | 简体中文

评审日期：2026-10-30（Asia/Shanghai）。范围：当前需求、功能、架构、运行部署、初始化、交付、验证文档，以及本次联网的一手项目资料。这是文档评审与研究建议，不是应用测试或替代 ADR；保留已有未提交改动。

## 结论

**保留单仓库、共用业务 Agent、双模式配置和独立现场端。现有文档可以作为连贯的设计基线，但尚未成为完整的实施与验收契约。** 主要缺口是可执行工作流、可安装的运行环境/配置包、模型能力契约、恢复语义及业务状态转换。增加框架或 Agent 名称不能解决这些问题。

完整目标架构继续保留，实现顺序另行管理。下文没有把任何能力当作已经实现。现有文档已承认不少风险，本次指出的是哪些风险说明仍需落实为具体契约与验收证据。

## 本次核查的高关注与近期项目

以下是相关样本，不是全站排名。Star 为本次打开官方仓库后显示的约数，不是实时精确 API 数；搜索缓存有差异，不能拼接成增长结论。Shell 请求 GitHub 元数据被阻止。版本新、关注高都不能证明兼容、耐久执行或制造质量。

| 项目与官方来源 | 显示 Star | 近期依据及比较价值 |
| --- | ---: | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | 393.4k | 个人助手参考，不直接用作打印控制器 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | 258.6k | 本地 Agent/记忆参考，关注度不是采用理由 |
| [Dify](https://github.com/langgenius/dify) | 159.9k | [1.18.0 发布页](https://github.com/langgenius/dify/releases)：应用包与嵌套工作流可见性，显示 23 Oct |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92.2k | 1.34.0，执行环境分离，详见 Agent 调研 |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84.7k | 2.1.0，长任务工作区、委派与运维 |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 67.7k | [1.19.0](https://github.com/Mintplex-Labs/anything-llm/releases)，显示 26 Oct；借鉴本地首次使用，不直接引入知识聊天产品 |
| [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | 53.1k | [2.1.8](https://github.com/CherryHQ/cherry-studio/releases)，显示 26 Oct；模型配置、工作区、桌面分发 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44.1k | 1.2.18，现有运行时选择仍合理 |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | 30.8k | [0.7.32](https://github.com/langchain-ai/deepagents/releases)，显示 23 Oct；LangGraph 上的新一层 harness |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30.4k | 0.24.0，变更记录 2026-10-15；审批与恢复备选 |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | 20.9k | 2.63.0，类型化/延后执行工具、独立评估 |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | 14.4k | Python 1.23.0，2026-10-22；较新的工作流与托管比较对象 |

具体包版本和日期限制见 [Agent 更新](agent-framework-update-2026-10-30.md)。只显示月日的标签不能独立确定年份。Dify 多组件同步升级说明提示我们：共仓库不等于协议自动兼容，不表示要在 Autumn 中部署 Dify。

打印领域：[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) 显示 16.2k，OctoPrint 9.2k，Spoolman 3.0k，Obico 1.9k，Moonraker 1.5k。较低 Star 的领域工具可能比通用 Agent 更关键。一手链接、稳定/预发布区别及发布索引日期异常见[打印生态更新](printing-ecosystem-update-2026-10-30.md)。

## 架构问题

| 编号与优先级 | 当前依据 | 影响与需要补齐的内容 |
| --- | --- | --- |
| A-01 / P1 | [运行部署](../architecture/runtime-and-deployment.md)承诺随包后台，但明确保留 Windows 登记、凭据初始化、升级与卸载待定项 | 明确宿主生命周期、首次凭据、依赖/引擎/预设清单、协议协商、健康与诊断导出。干净 Windows 无开发工具/旧 Orca 预设也应通过；测试初始化失败与升级中断 |
| A-02 / P1 | [运行部署](../architecture/runtime-and-deployment.md)区分业务库、队列、checkpoint 与动作日志，但文字说明还不是状态转换/故障规范 | 明确入队、领取、工具意图、审批消耗、现场接收、结果与 checkpoint 各节点的权威记录；两种后端对每次写入前后注入崩溃。启动结果未知只进入核查，不再次启动 |
| A-03 / P1 | [F-02](../product/functional-spec.md)提出连接与能力检测，但没有供应商契约 | 记录 Adapter/API 类型、工具/schema、取消、限流/超时、用量、上下文与视觉能力。公布已测试路径；能力不足只关闭受影响自动化并解释，不阻止本地资料和人工工具 |
| A-04 / P2 | [Agent 角色](../architecture/agent-and-tools.md)有职责和授权，缺少完整上下文/运行策略 | 明确上下文选择、压缩、工具结果外存、证据时效、委派条件和预算归集。可以对同一业务图评估受限 harness，不增加另一套任务拥有者 |

Deep Agents 在 LangGraph 上提供计划、上下文、委派与工具审批，同时要求工具/沙箱执行授权限制。**推论：** 可借鉴机制或评估受限 harness，不把默认 Shell/文件系统工具直接给打印 Agent。[官方概述](https://docs.langchain.com/oss/python/deepagents/overview)、[仓库与安全说明](https://github.com/langchain-ai/deepagents)。

在同契约实验能证明替代方案有明显收益前，保留 LangGraph。当前 OpenAI/Pydantic/Microsoft 也具备审批或耐久相关机制，不能再以“只有 LangGraph 支持”作为选型依据，详见专题。框架有 checkpoint 不代表个人 SQLite 的生产恢复已经解决。

## 功能问题

| 编号与优先级 | 缺口 | 应补的验收行为 |
| --- | --- | --- |
| F-R01 / P1 | [R-01/F-03](../product/requirements.md)承诺个人可用，但主场景围绕订单与套件 | 提议增加轻量的单模型工艺比较入口，复用业务对象，不强制先建客户、企业成员或机群；实施前确认此项需求，保留完整订单路径 |
| F-R02 / P1 | [F-04](../product/functional-spec.md)缺少具体的引擎与配置导入契约 | 干净机器导入获准 STL/3MF，解析机器/喷嘴/耗材及项目覆盖，保留原始/有效配置，拒绝不支持组合，并在目标引擎打开成果 |
| F-R03 / P1 | [F-05](../product/functional-spec.md)目前主要是能力表和七个角色，缺少贯穿执行轨迹 | 写明请求 → 计划 → 实际工具 → 证据 → 人工等待 → 恢复 → 结果，包括拒绝、取消、缺资料；任务界面显示阻塞原因、下一责任人和安全可用动作 |
| F-R04 / P1 | [数量规则](../product/functional-spec.md)有不变量，缺完整转换与影响规范 | 明确部分验收、首件计入/撤销、返工、预留/分配、改订单后的作业增减和旧版实物处置；使用表驱动用例，不把计划或重复产出算成合格 |
| F-R05 / P2 | 材料与监控能力描述较宽 | 明确材料卷身份、装载、预留、实测消耗/退料/纠正，以及监控覆盖/置信度/暂停拥有者；合理集成现有系统，设备字段缺失保持未知 |

[Cherry Studio](https://github.com/CherryHQ/cherry-studio) 和 [AnythingLLM 桌面版](https://docs.anythingllm.com/installation-desktop/overview)是首次使用体验参考，不是打印能力依据。**推论：** 个人应能先获得模型相关的实际成果，再进入生产管理概念。

[Printago Orders](https://docs.printago.io/docs/commerce/orders)已有 SKU/组件与作业变更；[SimplyPrint AutoPrint](https://help.simplyprint.io/en/article/autoprint-put-your-printers-on-autopilot-1hssb9u/)已有续打与清床检查。因此应演示首件证据 → 工艺适用批准 → 部分合格产出 → 正确补打/齐套；来源不能证明组合独有或商业上更好。

## 验证与文档问题

**V-01 / P1：** [初始化](../engineering/bootstrap.md)和[验证计划](../engineering/validation.md)列出了合适检查，但尚无版本化、可执行的验收包。应定义模型/预设/事件样例清单、预期工具事实、数量/权限断言、故障点与结果证据。两种模式共用确定性契约，Agent 结果/成本和实物质量分别评估。首批必须包括人工等待后重启，以及设备已启动但回执丢失。不能以回复文字匹配判成功。

这是实施准备度缺口，不是已存在应用的失败证据，因为应用尚未实现。历史调研继续保留日期，新版本结论写入新报告，不悄悄覆盖旧快照。

## 建议处理顺序

1. 固定完整功能/模式矩阵，确认个人单模型入口提议（F-R01）。
2. 完成模型供应商、引擎/预设能力契约及验收包清单（A-03、F-R02、V-01）。
3. 完成本地宿主与跨存储状态转换/故障表（A-01、A-02），两种模式用 Fake 工具验证。
4. 跑通一条真实订单到候选/人工等待，以及实物验收/部分产出/补打场景（F-R03、F-R04）。
5. 比较可选 harness，补上下文、评估和人工处置界面，再扩展材料/监控集成（A-04、F-R05）。

完整架构继续在架构文档维护；上述顺序是实施计划，不是缩减替代产品。建议需通过后续明确设计修改，才成为正式需求或已接受 ADR。
