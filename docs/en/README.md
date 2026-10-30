# Documentation index

English | [简体中文](../zh-CN/README.md)

Personal-mode engineering bootstrap is implemented. See [development setup](engineering/getting-started.md) for commands, evidence and remaining gates. Production features, installers and enterprise acceptance remain pending. This index defines document ownership; each rule has one primary location per language.

Latest review: [zero-to-one architecture and functional review, 2026-10-30](research/architecture-functional-review-2026-10-30.md), with separate [agent evidence](research/agent-framework-update-2026-10-30.md) and [printing ecosystem evidence](research/printing-ecosystem-update-2026-10-30.md). Findings are recommendations, not accepted architecture changes or passing application tests.

## Read by question

| Layer | Primary document | Question answered |
| --- | --- | --- |
| Requirements | [Requirements](product/requirements.md) | Who is it for, what does it solve, and what are the scope and success criteria? |
| Features | [Functional specification](product/functional-spec.md) | What can users do, and what are the workflows, rules, exceptions, and business acceptance criteria? |
| Architecture | [Architecture overview](architecture/overview.md) | How are modules, technology, data ownership, and interfaces organized? |
| Runtime | [Runtime and deployment](architecture/runtime-and-deployment.md) | What runs in each mode, and how does it start, recover, and migrate? |
| Agents | [Agents and tools](architecture/agent-and-tools.md) | How are roles, tools, authorization, and evidence organized? |
| Engineering structure | [Repository structure](architecture/repository.md) | Where do the four applications and three shared packages live, and how are they built? |
| Initialization | [Bootstrap](engineering/bootstrap.md) | How do we prove that the applications and both modes work together? |
| Implementation order | [Delivery plan](engineering/delivery-plan.md) | In what dependency order are features implemented? |
| Verification | [Validation plan](engineering/validation.md) | How are tests, fault injection, release checks, and evidence recorded? |
| Terminology | [Domain language](CONTEXT.md) | What do the domain terms mean? |
| Decisions | [Dual-mode ADR](adr/0002-dual-mode-monorepo.md) | Why was the current design chosen, and what does it cost? |
| Evidence | [Technology research](research/technology-selection.md) | Which sources support product and technology judgments? |

## Directory and maintenance rules

```text
docs/en/                         # Same relative paths under docs/zh-CN/
├── README.md
├── project.md
├── CONTEXT.md
├── guide.md                     # Former guide navigation
├── technical-design.md          # Former design navigation
├── deployment-and-project-structure.md
├── product/
│   ├── requirements.md
│   └── functional-spec.md
├── architecture/
│   ├── overview.md
│   ├── runtime-and-deployment.md
│   ├── agent-and-tools.md
│   └── repository.md
├── engineering/
│   ├── bootstrap.md
│   ├── delivery-plan.md
│   └── validation.md
├── adr/
├── research/
└── LICENSE                      # Original English license, retained verbatim
```

Read requirements and features first, then the relevant architecture documents. Read repository structure and bootstrap before implementing. When adding or changing a feature, maintain requirement/feature identifiers and link architecture, delivery, and validation. Technology choices are not user requirements; development phases do not define feature scope.

The former combined guides remain as [guide navigation](guide.md), [technical navigation](technical-design.md), and [deployment navigation](deployment-and-project-structure.md) within each language folder. Research preserves sources and historical judgments and does not override formal requirements or architecture. The [license](LICENSE) is retained verbatim in English.

## Language policy

English is the default. The repository root contains only the English README entry point; documentation lives under `docs/en/` and `docs/zh-CN/` with matching filenames and relative paths, including project overview, glossary, ADRs, engineering documents, and research. Do not add language suffixes or new root documentation files. The tree shows the English folder; the Chinese folder mirrors its Markdown files.

Maintain both versions in the same change. Keep R/F/B identifiers, code, commands, paths, source URLs, dates, quantities, and ADR status aligned. Internal links stay in the selected language; language switches link to the exact counterpart. English is the primary editing baseline; translations must preserve meaning rather than introducing separate decisions. Report and resolve any discrepancy in both versions.
