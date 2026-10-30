# Agents and tools

English | [简体中文](../../zh-CN/architecture/agent-and-tools.md)

This document owns roles, tools, permissions, and evidence rules. See [runtime](runtime-and-deployment.md) for queues/recovery and the [functional specification](../product/functional-spec.md) for user-visible capabilities. Status: unimplemented design baseline.

## Agent and edge responsibilities

Business agent code lives in `packages/control-plane/src/autumn_control/agent/` and runs through `apps/worker`. Inference orchestration does not run in Electron renderer, API request event loops, or edge executors.

| Agent role | Responsibility | Personal | Enterprise |
| --- | --- | --- | --- |
| Coordinator | Check goals, plan, delegate, summarize, wait | Local worker | Server worker |
| Requirements reviewer | Quantities, kits, materials, revisions, missing acceptance information | Local worker | Server worker |
| Model inspector | Invoke geometry tools; explain inspection/repair differences | Local worker | Server worker |
| Process planner | Constrained candidates, real slicing requests, evidence comparison | Local worker | Server worker |
| Experiment analyst | First-article feedback, hypotheses, parameter experiments, applicability | Local worker | Server worker |
| Production planner | Feasibility checks, batch suggestions, progress | Local worker | Server worker |
| Quality reviewer | Incident investigation, quantity reconciliation, reprints, delivery advice | Local worker | Server worker |

These are configurable roles in one workflow, not necessarily separate services. Simple tasks use one role; delegation fixes role/graph versions, scoped tools, budgets, and evidence. Deployment changes data, model, identity, dispatch, and edge-connection adapters rather than copying prompts/rules.

`apps/edge` is **not a second business agent** and needs no separate model key. It verifies authorization, expiry, file hashes, and device scope; executes Orca, geometry inspection/repair, device reads, and approved actions; and manages processes, resources, files, journals, and receipts. Tools establish geometry facts; business records establish approvals/physical quality. Edge does not independently approve processes or determine reprint quantities.

See [runtime](runtime-and-deployment.md) for the process diagram.

## Agents, tools, and business completion

LangGraph is the sole main graph runtime. Coordination, requirements, model inspection, process planning, experiment analysis, production planning, and quality review are roles delegated as needed. All personal roles orchestrate on the local worker; enterprise roles on server workers. They share graphs, role versions, tool definitions, and evaluations in `packages/control-plane`. Edge executes controlled tools without independent inference orchestration. Feature parity does not promise identical output from different models.

- Graph state stores task/artifact references, hypotheses, missing information, plans, and budgets, not large model files, G-code, or entire photo sets.
- Typed tool parameters call business module interfaces; reads and proposed actions are distinct.
- Agents may propose repair, parameters, trials, plans, and device actions. Business policy, approval, and adapters govern execution.
- Do not give models device/storage credentials or arbitrary network/filesystem/shell capabilities.
- Child-agent permissions are the intersection of user, organization policy, parent-task authorization, role capabilities, and device capabilities.
- Role definitions include name, instruction version, allowed tools, output schema, knowledge scope, model reference, step/concurrency/cost limits, and enabled state.
- Administration supports creating, editing, disabling, publishing, and viewing role runs; active tasks pin role/graph versions.
- Exhausted budgets, insufficient evidence, denied permissions, and waits for physical results are explicit states, not success.
- Route text planning, vision assistance, and structured checking through configured models. Verify tool calls/JSON/images with fixtures rather than assuming all compatible APIs behave alike.

Process knowledge and memory remain distinct. Manuals/history are searchable; validated processes arise only from real records and approvals, never directly from automatic memory extraction.
