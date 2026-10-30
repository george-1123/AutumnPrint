# Autumn-ai · Autumn Print

English | [简体中文](../zh-CN/project.md)

A **3D printing process and production assistant** for individual FDM users, printing studios, print farms, and enterprise prototyping centers.

Connect models and requirements, real slicing comparisons, first-article trials, process approval, batch production, reprints, and quality delivery around a print order.

## Current status

The project is in design and research. Application code, runnable services, and installers have not been implemented. Documented directories, commands, features, and acceptance criteria are implementation targets.

Personal local and enterprise server modes share the same business agents. The edge executor runs Orca, geometry, and device tools. Personal users should be able to install the application and configure a model API; enterprise users connect to a server and sign in.

## Documentation

See the [documentation index](README.md) for reading order and document ownership.

| Topic | Document |
| --- | --- |
| Users, goals, and product scope | [Requirements](product/requirements.md) |
| Complete features, workflows, and business acceptance | [Functional specification](product/functional-spec.md) |
| System, technology, data, and interfaces | [Architecture overview](architecture/overview.md) |
| Local/enterprise operation and recovery | [Runtime and deployment](architecture/runtime-and-deployment.md) |
| Agents, tools, and authorization | [Agents and tools](architecture/agent-and-tools.md) |
| Application directories and package dependencies | [Repository structure](architecture/repository.md) |
| Establishing a runnable engineering foundation | [Bootstrap](engineering/bootstrap.md) |
| Feature implementation order | [Delivery plan](engineering/delivery-plan.md) |
| Tests, failures, and release checks | [Validation plan](engineering/validation.md) |

## Terminology, decisions, and evidence

- [Domain language](CONTEXT.md) and [dual-mode monorepo decision](adr/0002-dual-mode-monorepo.md).
- [Technology research](research/technology-selection.md) and [architecture references](research/architecture-references.md).
- [Orca source and product direction](research/printing-orca-direction.md), [user needs evidence](research/printing-user-needs.md), and [product ecosystem](research/printing-ecosystem.md).

Research preserves sources and historical judgments. The corresponding requirements and architecture documents define the current design. Former combined guides remain as navigation pages rather than duplicate specifications.

English is the default documentation language. Documents use matching filenames under `docs/en/` and `docs/zh-CN/`; update both together, preserving identifiers, commands, source URLs, dates, and decision status. Follow links within the selected language and use the language switch to change languages. Only README remains at the repository root.
