# Architecture reference projects

English | [简体中文](../../zh-CN/research/architecture-references.md)

Source: research excerpts from the former technical design. Retains the 2026-10-29 context, not renewed verification or mandatory dependencies. See the [architecture overview](../architecture/overview.md) for the formal design.

## How reference projects inform the design

| Reference | What to study | Treatment in Autumn |
| --- | --- | --- |
| OpenClaw / Hermes | Local operation, tool policy, history, skills | Borrow mechanisms without general shell/device permissions |
| DeerFlow | Long tasks, restricted subagents, artifacts, task workbench | Adapt interaction/organization to printing |
| OpenHands | Separate control UI/execution backend, isolated workspaces | Inform control/edge design, not a coding agent as production controller |
| LangGraph | Nodes, branches, interrupts, durable checkpoints | Use graph execution; Autumn owns business state |
| OrcaSlicer | Configuration, slicing, calibration, device adapters | Fixed tool version without an early large C++ fork |
| Printago / SimplyPrint | Orders, queues, material matching, clearance, handoff | Compare capabilities; integrate via API if already the fleet scheduler |
| Trimesh / PyMeshLab | Geometry facts, constrained repairs | Tool evidence rather than fabricated geometry conclusions |

These are representative projects with official sources, not a complete GitHub ranking. Popularity/update dates do not prove physical-production reliability.

## Orca integration and sources

- [Architecture and module design](../architecture/overview.md).
- [Projects, releases, and selection evidence](technology-selection.md).
- [Domain terminology](../CONTEXT.md).
- [Official OrcaSlicer project](https://github.com/OrcaSlicer/OrcaSlicer).
- [CLI guide](https://www.orcaslicer.com/wiki/cli/cli_mode).
- [Calibration guide](https://www.orcaslicer.com/wiki/guides/calibration_guide).
- [Source and product direction research](printing-orca-direction.md).
- [Practitioner evidence](printing-user-needs.md).
- [Product ecosystem and integration limits](printing-ecosystem.md).

The research confirmed local source at `D:\project\OrcaSlicer-main\OrcaSlicer-main`, marked `2.5.0-dev` at that time. It is evidence, not a requirement to modify that project or proof of an installed engine. Implementation must verify the selected binary's actual capabilities.

Initially orchestrate Orca through an independent adapter and preserve its GUI for inspection. Evaluate version-specific plugins if embedding becomes necessary. Review licenses before reuse/modification/distribution rather than deriving obligations from invocation method alone.
