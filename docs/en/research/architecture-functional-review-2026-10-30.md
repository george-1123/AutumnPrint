# Zero-to-one architecture and functional review

English | [简体中文](../../zh-CN/research/architecture-functional-review-2026-10-30.md)

Reviewed 2026-10-30 (Asia/Shanghai). Scope: current requirements, features, architecture, runtime, bootstrap, delivery, validation, and live primary-source comparisons. This is a document review and research recommendation, not application testing or a replacement ADR. Existing uncommitted changes were retained.

## Verdict

**Keep the monorepo, shared business agents, dual deployment profiles, and independent edge execution. The documentation is a coherent design baseline, but not yet a complete implementation/acceptance contract.** The main gaps concern executable workflows, installable runtime/profile bundles, model capability contracts, recovery semantics, and business-state transitions. More frameworks or more agent names would not resolve them.

The full target architecture should remain explicit; implementation order is a separate concern. No capability below is represented as already implemented. The existing documents acknowledge many risks; this review identifies where those acknowledgments still need concrete contracts and acceptance evidence.

## Current high-attention and recent comparison set

These are relevant samples, not an exhaustive ranking. Stars are rounded figures displayed on official repositories opened this session, not exact live API counts. Search caches differed; use opened pages rather than combining cached counts into growth claims. Shell GitHub metadata requests were blocked. Releases and popularity do not prove compatibility, durability, or manufacturing quality.

| Project / official source | Displayed stars | Recent evidence / why compare |
| --- | ---: | --- |
| [OpenClaw](https://github.com/openclaw/openclaw) | 393.4k | Personal-agent reference; not a print controller |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | 258.6k | Local agent/memory reference; popularity alone is not an adoption reason |
| [Dify](https://github.com/langgenius/dify) | 159.9k | [1.18.0 release](https://github.com/langgenius/dify/releases): portable applications and nested workflow visibility; displayed 23 Oct |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 92.2k | 1.34.0: execution/runtime separation; details in agent research |
| [DeerFlow](https://github.com/bytedance/deer-flow) | 84.7k | 2.1.0: long-task workspace/delegation/operations |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 67.7k | [1.19.0 release](https://github.com/Mintplex-Labs/anything-llm/releases), displayed 26 Oct; benchmark local onboarding rather than importing a knowledge-chat product |
| [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | 53.1k | [2.1.8 release](https://github.com/CherryHQ/cherry-studio/releases), displayed 26 Oct; provider setup, workspaces, desktop distribution |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 44.1k | 1.2.18: existing runtime remains a reasonable fit |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | 30.8k | [0.7.32 release](https://github.com/langchain-ai/deepagents/releases), displayed 23 Oct; newer harness layer on LangGraph |
| [OpenAI Agents Python](https://github.com/openai/openai-agents-python) | 30.4k | 0.24.0, changelog 2026-10-15; approval/recovery alternative |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | 20.9k | 2.63.0; typed/deferred tools and independent evaluation |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | 14.4k | Python 1.23.0 dated 2026-10-22; newer workflow/hosting comparison |

Package-specific release evidence and date ambiguities are in the [agent update](agent-framework-update-2026-10-30.md). Month/day release labels above do not independently establish a year. Dify's multi-component upgrade instructions are a useful warning against assuming a shared repository guarantees protocol compatibility; they are not a reason to deploy Dify inside Autumn.

For printing, [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) showed 16.2k stars, OctoPrint 9.2k, Spoolman 3.0k, Obico 1.9k, Moonraker 1.5k. Lower-star domain tools can matter more than general-agent popularity. See the [printing update](printing-ecosystem-update-2026-10-30.md) for primary links, stable/prerelease distinctions, and the release-index chronology anomaly.

## Architecture findings

| ID / priority | Evidence in current design | Consequence and required change |
| --- | --- | --- |
| A-01 / P1 | [Runtime](../architecture/runtime-and-deployment.md) promises bundled execution but explicitly leaves Windows registration/provisioning/update/uninstall pending | Specify host lifecycle, initial credentials, dependency/engine/profile manifest, compatibility negotiation, health and diagnostic export. Accept on clean Windows with no developer tools or pre-existing Orca profiles; also test failed initialization and interrupted upgrades |
| A-02 / P1 | [Runtime](../architecture/runtime-and-deployment.md) separates business DB, queue, checkpoints, and journals, but descriptions are not a transition/failure specification | Define which record wins at each handoff: enqueue, claim, tool intent, approval consumption, edge acceptance, outcome, checkpoint. Inject crashes before/after each write on both backends; unknown starts remain reconciliation work, never another start |
| A-03 / P1 | [F-02](../product/functional-spec.md) checks connectivity/capabilities without a provider contract | Record adapter/API style, tool/schema behavior, cancellation, rate-limit/timeout handling, usage and context limits, and visual capability. Publish tested paths; insufficient capabilities disable affected automation with an actionable message, not all local data/manual tools |
| A-04 / P2 | [Agent roles](../architecture/agent-and-tools.md) define responsibility and scope, but not full context/runtime policy | Specify context selection, compaction, tool-result offloading, evidence freshness, delegation criteria, and budget accounting. Compare a bounded harness against the same business graph, not a second task owner |

Deep Agents documents planning, context management, delegation and approval on top of LangGraph, while warning that tools/sandboxes must enforce authority. **Inference:** borrow these mechanisms or evaluate a restricted harness; do not import default shell/filesystem tools into a printer agent. [Official overview](https://docs.langchain.com/oss/python/deepagents/overview), [repository/security explanation](https://github.com/langchain-ai/deepagents).

Keep LangGraph until a same-contract experiment demonstrates a meaningful benefit elsewhere. Current OpenAI/Pydantic/Microsoft capabilities make “only LangGraph supports approval or recovery” an invalid selection argument; see the agent note. Framework checkpoints are not proof that personal SQLite production recovery is solved.

## Functional findings

| ID / priority | Gap | Required acceptance behavior |
| --- | --- | --- |
| F-R01 / P1 | [R-01/F-03](../product/requirements.md) promise personal usefulness, but the main scenario assumes an order/kit | Add a lightweight single-model process-comparison path using the same domain objects, without forcing customers, enterprise membership, or fleet setup. Confirm it as a requirement before implementation; retain the full order path |
| F-R02 / P1 | [F-04](../product/functional-spec.md) lacks a concrete engine/profile import contract | Import authorized STL/3MF on a clean machine; resolve machine/nozzle/material presets and project overrides; preserve original/effective settings; reject unsupported combinations and open results in the target engine |
| F-R03 / P1 | [F-05](../product/functional-spec.md) is a capability list and seven roles, not a complete worked execution trace | Specify one request → plan → actual tools → evidence → human wait → resume → result sequence, including denial/cancel/missing data. Show blocked reason, next actor and safe available actions in the task UI |
| F-R04 / P1 | [Quantity rules](../product/functional-spec.md) describe invariants, but no complete transition/impact specification | Define partial acceptance, first-article credit/revocation, rework, reservation/allocation, changed-order job additions/cancellations, and old-revision disposition. Add table-driven cases; never count planned or duplicate output as accepted |
| F-R05 / P2 | Material/monitoring capabilities are broad | Define spool identity, loaded assignment, reservation, measured consumption/return/correction, and monitoring coverage/confidence/pause owner. Integrate existing systems when appropriate; missing device fields remain unknown |

[Cherry Studio](https://github.com/CherryHQ/cherry-studio) and [AnythingLLM desktop](https://docs.anythingllm.com/installation-desktop/overview) are onboarding benchmarks, not evidence of printing capability. **Inference:** personal users should reach a useful model-oriented outcome before needing production-administration concepts.

[Printago Orders](https://docs.printago.io/docs/commerce/orders) already addresses SKU/component job changes; [SimplyPrint AutoPrint](https://help.simplyprint.io/en/article/autoprint-put-your-printers-on-autopilot-1hssb9u/) handles continuation and bed checks. Therefore demonstrate first-article evidence → approved applicability → partial accepted output → correct reprints/kits. The sources do not establish that this combination is unique or commercially superior.

## Verification and documentation finding

**V-01 / P1:** [Bootstrap](../engineering/bootstrap.md) and [validation](../engineering/validation.md) enumerate good checks but do not yet provide a versioned executable acceptance pack. Define a manifest for model/profile/event fixtures, expected tool facts, quantity/permission assertions, failure points, and result artifacts. Use the same deterministic contracts across both modes; evaluate agent outcomes and cost separately from physical quality. The initial pack must include a stopped/restarted human wait and a started device action with a lost receipt. Do not use matching prose as success.

This is an implementation-readiness gap, not evidence of a failing application: no application exists. Historical research snapshots remain dated evidence; new release claims belong in new notes rather than silently overwriting them.

## Recommended order of resolution

1. Freeze the complete feature/mode matrix and confirm the proposed personal single-model path (F-R01).
2. Write provider and engine/profile capability contracts plus the acceptance-pack manifest (A-03, F-R02, V-01).
3. Specify host bootstrap and cross-store transition/failure tables (A-01, A-02); verify them with Fake tools in both modes.
4. Run one real order-to-candidate/human-wait loop and one physical inspection/partial-output/reprint scenario (F-R03, F-R04).
5. Compare optional harnesses, improve context/evaluation/operator UI, then expand material/monitoring integrations (A-04, F-R05).

Keep the full architecture in the architecture documents; this order is an implementation plan, not a smaller substitute product. Recommendations require an explicit follow-up design change before they become accepted requirements/ADRs.
