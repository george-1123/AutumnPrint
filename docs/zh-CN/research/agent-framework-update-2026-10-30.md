# Agent 框架证据更新 — 2026-10-30

[English](../../en/research/agent-framework-update-2026-10-30.md) | 简体中文

范围：Autumn Print 架构评审的一手资料调研。读取日期：2026-10-30（Asia/Shanghai）。未安装依赖、调用供应商或测试设备。数字为打开官方 GitHub 页面后显示的约数，不是实时精确 API 结果或全站排名。缓存可能不同；发布时间、主分支和关注度分别判断。

## 高关注与近期维护样本

| 官方项目 | 显示 Star | 本次发布依据 | 相关性 |
| --- | ---: | --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44.1k | [1.2.18](https://github.com/langchain-ai/langgraph/releases/tag/1.2.18)，列表显示 26 Oct 20:04 | 现有图/状态/中断选择 |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30.4k | [0.24.0](https://github.com/openai/openai-agents-python/releases)，变更记录 2026-10-15 | 轻量工具、委派与审批参考 |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | 20.9k | [2.63.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.63.0)，标题 2026-10-27，发布显示 28 Oct 00:55 | 类型化工具、延后执行、独立评估 |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | 14.4k | [Python 1.23.0](https://github.com/microsoft/agent-framework/releases)，变更记录 2026-10-22；.NET 1.26.0 是另一发布 | 较新的企业工作流与托管比较 |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84.7k | [2.1.0](https://github.com/bytedance/deer-flow/releases/tag/v2.1.0)，显示 24 Sep 10:40 | 长任务工作区、委派与运维 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92.2k | [1.34.0](https://github.com/OpenHands/OpenHands/releases)，变更记录 2026-10-27 | 执行环境分离与操作者体验 |

未显示年份/时区的日期按原样保存，不补造时间戳。Pydantic 另有 CLAI2 bleeding 条目，明确为预发布重建，不是稳定包版本。Star 反映关注，不证明适合打印控制。

## 新证据带来的调整

**LangGraph 仍是合理基线，但不独占这些能力。** [持久化文档](https://docs.langchain.com/oss/python/langgraph/persistence)区分 thread checkpoint 与跨 thread store；[中断](https://docs.langchain.com/oss/python/langgraph/interrupts)支持外部等待。继续区分业务事实与推理状态。持久化指南将 SQLite 用于本地开发；Autumn 个人正式使用仍需自己的并发、备份、迁移与恢复证据，不能由 saver 的存在推断生产准备完成。

**不能再因审批/恢复而排除轻量备选。** OpenAI [人在环指南](https://openai.github.io/openai-agents-python/human_in_the_loop/)说明序列化 RunState、嵌套 Agent 审批、由可信应用保存状态、重放防护及外部动作核查；不承诺副作用恰好一次。[模型指南](https://openai.github.io/openai-agents-python/models/)说明供应商语义差异和第三方适配层。Autumn 需要供应商验收矩阵，不只是可访问的 base URL。

**Pydantic AI 值得受限验证，不应立即替换。** [Deferred tools](https://ai.pydantic.dev/deferred-tools/)区分人工审批和外部执行，客户端提交批准不能替代应用授权。[耐久概述](https://github.com/pydantic/pydantic-ai/blob/main/docs/durable_execution/overview.md)区分已完成步骤保存与崩溃恢复，单 Agent 只有一个耐久引擎。[Pydantic Evals](https://ai.pydantic.dev/evals/)独立于 Pydantic AI，可评估当前运行时而不引入第二编排器。主分支文档不能证明选定发布包包含每项功能。

**Microsoft 新框架用于比较，不等于必须依赖 Azure。** [概述](https://learn.microsoft.com/en-us/agent-framework/overview/)区分开放式 Agent 与明确工作流，支持多个供应商，并定位为 AutoGen/Semantic Kernel 后继。[Durable Extension](https://learn.microsoft.com/en-us/agent-framework/hosting/durable-extension)区分普通 checkpoint 恢复与跨耐久 worker 恢复，并列出自托管选项。Python 1.23.0 涉及 AG-UI 授权范围和 MCP 生命周期变化，接口兼容仍需具体实施。

**借鉴 harness 运维能力，不照搬通用动作权限。** DeerFlow 2.1 强调耐久批量委派、记忆后端、执行验证、企业授权、项目与分支工作区。OpenHands 1.34.0 加入会话级 Docker 环境/设置并调整密钥处理。可借鉴界面、trace 和运行环境，但不证明打印兼容、实物质量或需要开放 Shell。

## 建议动作（推论）

- **P1 — 执行拥有者：** 每工作区一个执行后端、有界片段、固定 run/action 标识、权威审批消耗、可安全重放的现场回执。在角色管理前验证 SQLite/队列/checkpoint 和 PostgreSQL/outbox/checkpoint 的故障窗口。
- **P1 — 模型配置可测试：** 保存供应商/API 类型、工具、schema、流式取消、用量、超时与错误语义；对每条宣传支持路径运行样例。
- **P1 — 角色变成工作流：** 实现订单到候选、证据和人工等待，比较单角色/委派结果与成本；七角色表不等于 Agent 实现。
- **P2 — 评估与查看：** 版本化数据、确定性数量/权限/重复动作断言、trace 链接、预算和重放诊断，敏感数据脱敏。
- **P2 — 同契约比较备选：** LangGraph 与小规模 Pydantic AI/OpenAI SDK 验证共用等待、重启、审批、供应商和现场结果测试；有维护/能力收益再切换，不设置竞争的任务拥有者。

对应基线：[Agent](../architecture/agent-and-tools.md)、[运行部署](../architecture/runtime-and-deployment.md)、[初始化](../engineering/bootstrap.md)、[验证](../engineering/validation.md)。以上为评审建议，不修改已接受架构。
