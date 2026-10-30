# Agent framework evidence update — 2026-10-30

English | [简体中文](../../zh-CN/research/agent-framework-update-2026-10-30.md)

Scope: primary-source research for Autumn Print's architecture review. Retrieval date: 2026-10-30 (Asia/Shanghai). No dependencies installed, providers called, or physical devices tested. Figures below are rounded values displayed by opened official GitHub pages, not exact live API results or a global ranking. Cached pages can differ. Release dates, latest branches, and popularity are separate evidence.

## Popular and recently maintained comparison set

| Project and official repository | Displayed stars | Release evidence observed | Relevance |
| --- | ---: | --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44.1k | [1.2.18](https://github.com/langchain-ai/langgraph/releases/tag/1.2.18); release list displays 26 Oct 20:04 | Existing graph/state/interrupt choice |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30.4k | [0.24.0](https://github.com/openai/openai-agents-python/releases), changelog dated 2026-10-15 | Lightweight tool/delegation/approval reference |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | 20.9k | [2.63.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.63.0), title dated 2026-10-27; publication display 28 Oct 00:55 | Typed tools, deferred execution, independent evals |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | 14.4k | [Python 1.23.0](https://github.com/microsoft/agent-framework/releases), changelog 2026-10-22; .NET 1.26.0 is a separate release | Newer enterprise workflow/hosting comparison |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84.7k | [2.1.0](https://github.com/bytedance/deer-flow/releases/tag/v2.1.0); display 24 Sep 10:40 | Long-task workspace, delegation, operational reference |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92.2k | [1.34.0](https://github.com/OpenHands/OpenHands/releases), changelog 2026-10-27 | Separate execution/runtime and operator UX reference |

Dates lacking a displayed year/timezone are retained as shown rather than normalized into invented timestamps. Pydantic's separate CLAI2 bleeding entry is explicitly a prerelease rebuild, not its stable package version. Stars indicate attention, not fitness for print control.

## What the newer evidence changes

**LangGraph remains a reasonable baseline, not an exclusive capability winner.** Its [persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence) distinguishes thread checkpoints from cross-thread stores; [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) support external waits. Keep Autumn's business records separate from reasoning state. The persistence guide describes SQLite for local development; Autumn's personal production durability therefore needs its own concurrency, backup, migration, and recovery evidence rather than assuming a saver proves production readiness.

**Approval/resume is no longer a reason to dismiss lightweight alternatives.** OpenAI's [human-in-the-loop guide](https://openai.github.io/openai-agents-python/human_in_the_loop/) documents serialized RunState, approvals across nested agents, trusted application-owned snapshots, replay protection, and external-action reconciliation. It explicitly does not promise exactly-once side effects. Its [model guide](https://openai.github.io/openai-agents-python/models/) warns that provider feature semantics vary and third-party adapters add compatibility layers. Autumn needs a provider acceptance matrix, not merely a reachable base URL.

**Pydantic AI merits a bounded proof of concept, not immediate replacement.** [Deferred tools](https://ai.pydantic.dev/deferred-tools/) separate human approval and externally executed calls; client-submitted approvals do not replace application authorization. Its [durability overview](https://github.com/pydantic/pydantic-ai/blob/main/docs/durable_execution/overview.md) distinguishes settled-step persistence from crash-resilient execution and permits only one durable engine per agent. [Pydantic Evals](https://ai.pydantic.dev/evals/) is independent of Pydantic AI and can evaluate Autumn's chosen runtime without adding a second orchestrator. Current main documentation is not proof every feature ships in the selected release.

**Microsoft's newer framework is an architectural comparison, not a required Azure dependency.** The [overview](https://learn.microsoft.com/en-us/agent-framework/overview/) distinguishes open-ended agents from explicit workflows, supports multiple providers, and identifies itself as the successor to AutoGen/Semantic Kernel. The [Durable Extension](https://learn.microsoft.com/en-us/agent-framework/hosting/durable-extension) distinguishes standard checkpoint resume from recovery across durable workers and documents self-hosted options. Its Python 1.23.0 notes include explicit AG-UI authorization scopes and MCP lifecycle changes: integration surface/version compatibility is implementation work, not solved by a framework name.

**Learn operational capabilities from harnesses without importing their generic action surface.** DeerFlow 2.1's release highlights durable batch delegation, memory backends, execution verification, enterprise authorization, and project/branching workspaces. OpenHands 1.34.0 adds per-conversation Docker runtime/settings and changes key handling. These are useful operator/trace/runtime lessons; neither establishes printer compatibility, physical quality, or a reason to expose shell tools to production agents.

## Recommended review actions (inferences)

- **P1 — Define execution ownership:** one task executor per workspace, bounded worker fragments, stable run/action IDs, authoritative approval consumption, replay-safe edge receipts. Prototype failure windows across SQLite/queue/checkpoint and PostgreSQL/outbox/checkpoint before building role administration.
- **P1 — Make model configuration testable:** record provider/API style, tool calls, schema support, streaming cancellation, usage reporting, timeouts, error behavior. Run fixtures for each advertised model path.
- **P1 — Turn roles into tested workflows:** implement one order-to-candidate loop with evidence and human waits; compare single-role versus delegated outcomes/cost. A seven-role table alone is not an agent design.
- **P2 — Add evaluation and inspection surfaces:** versioned datasets, deterministic quantity/permission/duplicate-action assertions, trace links, budget records, and replay diagnostics; redact sensitive payloads.
- **P2 — Compare alternatives with one shared contract:** LangGraph and a small Pydantic AI or OpenAI SDK prototype must pass the same pause/restart/approval/provider/edge-result tests. Change runtime only for measured maintenance or capability gains; do not combine frameworks as competing owners.

Related local baselines: [agents](../architecture/agent-and-tools.md), [runtime](../architecture/runtime-and-deployment.md), [bootstrap](../engineering/bootstrap.md), [validation](../engineering/validation.md). Recommendations above are review findings, not changes to accepted architecture.
