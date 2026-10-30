# Printing ecosystem update and architecture review

English | [简体中文](../../zh-CN/research/printing-ecosystem-update-2026-10-30.md)

Review date: 2026-10-30 (Asia/Shanghai). Primary web sources were read in this session; no binaries, printers, or vendor accounts were tested. This is research and a recommendation, not an amendment to the approved architecture.

## Observed popularity and release signals

Rounded stars are the values actually displayed by GitHub, not exact API counts or a global ranking. Month/day labels do not establish publication year. The Orca release index also displayed a nightly dated 21 Nov, inconsistent with the client date; exclude that item from as-of-date chronology rather than inventing an explanation. Repository metadata API reads mostly failed.

| Project | Observed stars | Release/activity evidence | Relevance |
| --- | ---: | --- | --- |
| [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) | 16.2k | [Latest stable API](https://api.github.com/repos/OrcaSlicer/OrcaSlicer/releases/latest): v2.4.2, prerelease=false, published_at=2026-07-07T03:33:49Z. [Release index](https://github.com/OrcaSlicer/OrcaSlicer/releases): v2.5.0-beta explicitly prerelease, displayed 27 Oct 17:22; alpha displayed 16 Oct | Keep stable execution distinct from new experimental integration |
| [OctoPrint](https://github.com/OctoPrint/OctoPrint) | 9.2k | [1.11.8](https://github.com/OctoPrint/OctoPrint/releases/tag/1.11.8) marked Latest, displayed 23 Jun; [2.0.0rc7](https://github.com/OctoPrint/OctoPrint/releases) prerelease, displayed 20 Oct | Adapter compatibility is version-specific, not latest-RC-by-default |
| [Spoolman](https://github.com/Donkie/Spoolman) | 3.0k | [v0.27.0](https://github.com/Donkie/Spoolman/releases) marked Latest, displayed 25 Sep; adds NFC/RFID identification and scan-to-spool/filament behavior | Physical material identity is valuable beyond a generic material label |
| [Obico server](https://github.com/TheSpaghettiDetective/obico-server) | 1.9k | No new release date independently established in this pass | Observation adapter, not quality acceptance |
| [Moonraker](https://github.com/Arksine/moonraker) | 1.5k | No stable release date independently established in this pass | Relevant device protocol despite lower popularity |

## Important new capability: Orca Python plugins

The official [plugin guide](https://www.orcaslicer.com/wiki/plugins/plugins_getting_started) explicitly limits the Python plugin system to nightly or releases newer than 2.4.2. The [2.5 beta notes](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.5.0-beta) describe active-preset edits and background Scripts. These are documented capabilities, not a tested integration or guarantees for stable 2.4.2.

**Inference:** retain the independent edge/CLI baseline. Evaluate an optional Orca plugin bridge separately, using the same contracts. Define two compatibility lanes: accepted stable engine/CLI features, and opt-in prerelease/plugin features. Do not require plugin capabilities in the default stable installer or fork the entire C++ slicer to embed a chat UI.

The official [CLI action reference](https://www.orcaslicer.com/wiki/cli/cli_actions) documents effective-settings export, slicing-cache export/loading, progress pipes, and unrepaired-model info. Build a per-binary capability manifest and a test for each relied-on option. A current wiki does not prove the bundled stable binary implements every option.

## Functional comparison

[Printago Orders](https://docs.printago.io/docs/commerce/orders) already connects SKUs/components to print jobs, adjusts work when orders change, and surfaces failures, missing SKU links, deadlines, and proposed job additions/cancellations. [SimplyPrint AutoPrint](https://help.simplyprint.io/en/article/autoprint-put-your-printers-on-autopilot-1hssb9u/) documents automatic next-job selection after availability/bed-clearance checks, with plan-dependent availability. Neither source demonstrates physical inspection acceptance equivalent to Autumn's proposed validated-process/accepted-kit model.

**Inference:** a generic queue plus agent chat is insufficient differentiation. Autumn should demonstrate a failing first article, evidence-backed parameter experiment, scoped process approval, model revision impact, partial accepted output, and correct deficit/reprint/kit reconciliation on one continuous order. Competitor documentation is not proof Autumn's combined workflow is unique or commercially superior.

## Priority gaps in Autumn's current documents

| Priority | Gap and consequence | Concrete acceptance addition |
| --- | --- | --- |
| P1 | F-04 and install-and-use lack a tested engine/profile bundle contract | On clean Windows, load an authorized 3MF and compatible profiles without existing Orca user settings; preserve original/effective settings, reject unsupported overrides, and open exported output in target Orca |
| P1 | F-09/F-10 need explicit order-change and quantity transition rules | Preview additions/cancellations on revision; reject duplicate allocations, preserve partial accepted quantities, and test accepted first-article contribution and revocation |
| P1 | Device-ready/observation state needs adapter semantics | [Moonraker](https://moonraker.readthedocs.io/en/latest/external_api/printer/) requires connected Klippy and often ready; missing queried fields can be omitted without errors. Missing or stale status must remain unknown, not default-ready |
| P2 | Material records lack operator identification/reservation workflow | Resolve spool identity, loaded-device assignment, planned reservation, measured remaining mass, consumption/return/correction with one ledger; optionally integrate Spoolman scans rather than duplicate inventory |
| P2 | Monitoring state could be confused with healthy printing | [Obico objects](https://www.obico.io/docs/api/api-objects/) distinguish detection enabled, not-watching reasons, confidence, and automatic pause. Store these separately from actual quality and the action owner |
| P2 | Queue/planning scope is broad without manual attention workflow | Show blocked reason, evidence, next actor, retry/reconcile choice, and revision impact before pursuing autonomous fleet optimization |

The current control/edge split, explicit action journal, immutable artifacts, human physical acceptance, and shared local/server business rules are worth retaining. New releases justify targeted compatibility experiments, not replacing architecture based on stars.

Local documents reviewed: [features](../product/functional-spec.md), [runtime](../architecture/runtime-and-deployment.md), [requirements](../product/requirements.md).
