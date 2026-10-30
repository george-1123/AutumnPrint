# Autumn Print: OrcaSlicer-based process and production agents

English | [简体中文](../../zh-CN/research/printing-orca-direction.md)

> Direction confirmed (2026-10-29): the user accepted the process/production assistant direction. See the current [delivery plan](../engineering/delivery-plan.md); this document preserves product/source research evidence.

Research date: 2026-10-29 (Asia/Shanghai). The user specified 3D printing. These are proposals/source findings, not implemented capabilities. OrcaSlicer was not modified; no printer was connected or controlled.

## 1. Recommended positioning

Help small FDM studios, farms, and prototyping centers move requirements through process preparation, first-article trials/validation, batches, failure reprints, inspection, kits, and traceable delivery.

Suggested name: **Autumn Print — 3D printing process and production assistant**.

Users supply requirements/models; the application reads machines, materials, validated processes, generates comparable Orca slices, organizes trials/measurements, records confirmed conditions, then follows production/incidents.

Orca handles model processing/slicing. Autumn handles goals, plans, tools, experiments, business decisions, collaboration, execution state. Execution facts come from actual tools or human confirmation, never model fabrication.

## 2. Why this direction

Existing ecosystem capabilities:

- [OrcaSlicer repository](https://github.com/OrcaSlicer/OrcaSlicer): profiles, slicing, calibration, network printing.
- [CLI documentation](https://www.orcaslicer.com/wiki/cli/cli_mode): automated headless loading/transformation/slicing.
- [Calibration guide](https://www.orcaslicer.com/wiki/guides/calibration_guide): temperature, volumetric flow, PA, flow ratio, retraction.
- [Discussion #8593](https://github.com/OrcaSlicer/OrcaSlicer/discussions/8593): self-reported 3MF/CLI/farm-API integration, not compatibility proven by this project.

Existing competition:

- [Printago cloud slicing](https://docs.printago.io/docs/printing/cloud-slicer) combines machine/process/material G-code and queue matching.
- [SimplyPrint queues](https://simplyprint.io/features/print-queue) cover fleet matching, clearance, continuation conditions.
- Obico/OctoEverywhere already provide vision failure detection; see [ecosystem research](printing-ecosystem.md).

**Product judgment:** ordinary queues, remote buttons, and language-based parameters are insufficient differentiation. Test a traceable trial → physical acceptance → process version → batch → failure-review loop against actual users' daily work. Existing coverage and willingness to pay remain unproven.

See [original user/workflow evidence](printing-user-needs.md).

## 3. Confirmed local source foundation

The Codex project list identified:

`D:\project\OrcaSlicer-main\OrcaSlicer-main`

Root AGENTS.md was read before read-only investigation. `version.inc` says `2.5.0-dev`; the client did not identify this directory as a Git repository. Correspondence with current upstream commits was not verified.

| Capability | Local source | Findings |
| --- | --- | --- |
| CLI configuration | `src/OrcaSlicer.cpp:1359`, `:1367` | Machine/process and filament loading |
| Arrangement/orientation | `src/OrcaSlicer.cpp:4339`, `:4417` | orient/arrange branches |
| Slicing/export | `src/OrcaSlicer.cpp:5635`, `:5651` | 3MF export/slice actions |
| CLI definitions | `src/libslic3r/PrintConfig.cpp:11678`, `:11954` | Actions/transforms/other settings |
| Geometry | `src/libslic3r/TriangleMesh.hpp:87` | Volume/bounds/transforms/splitting/repair primitives |
| Estimates | `src/libslic3r/Print.hpp:800` | Time/material/weight/cost statistics |
| Cost | `src/libslic3r/GCode.cpp:2207` | Material plus time_cost/estimated duration; not full enterprise pricing |
| Calibration modes | `src/libslic3r/calib.hpp:17` | PA/flow/temperature/volumetric speed/retraction |
| Calibration execution | `src/slic3r/Utils/CalibUtils.hpp:37` | Parameter/device helpers |
| Print hosts | `src/slic3r/Utils/PrintHost.cpp:44` | OctoPrint/PrusaLink/Moonraker/SimplyPrint selection |
| Submission differences | `src/slic3r/Utils/PrintHost.hpp:21` | None/start/simulation/queue actions with implementation-specific support |

**Verification limit:** source structure/public documents only; no compilation, CLI execution, slicing, or device verification. Adapter existence does not imply every model/firmware supports every action.

Current website statistics/plugin features require separate detection in local development source and installed binaries. Pin a runnable engine, inspect actual `--help`, test inputs/inheritance/statistics/errors before depending on interfaces.

## 4. Fictional continuous business scenario

A studio receives 50 snap-fit bracket kits, each with 1 base and 2 clips. Requirements: black PETG, delivery the day after tomorrow, fit with specified mating parts, no obvious support marks on contact surfaces.

Three printers, spools, and process history are available. Order/quality rules specify first-article contribution to delivery.

### Step 1: requirements and model inspection

- Record counts/purpose/material/color/surface zones/dimensions/mating parts/deadline.
- Confirm kits require 50 bases/100 clips.
- Check revisions/units/dimensions/bed capacity/mesh and human-review risks.
- Agents cannot confirm absent load requirements, tolerances, or material substitution permission themselves.

### Step 2: few candidates and actual slicing

- Compatible machine/nozzle/material/process settings produce constrained orientations/layers/walls/supports.
- Orca actually slices; preserve differences/time/material/warnings/files.
- Compare critical surfaces, fit orientation, manual support removal, deadline.
- Fluent explanations/slice duration do not establish strength/tolerance/yield.

### Step 3: first articles and acceptance

- Trial goals/checklist; operator confirms device/material/environment.
- Collect photos/measurements/fit/incidents; actual measurements confirm critical dimensions.
- Tight clips trigger dimension/elephant-foot/model-fit/process checks and hypotheses.
- Vary few factors in reviewable experiments; preserve revisions/settings/machine/material/outcome.
- Responsible approval scopes the process; one successful trial is not permanent universal applicability.

### Step 4: batches

- Split by quantities/compatibility/material/time/clearance.
- Only validated combinations enter plans; nozzle/material/model changes require explicit review.
- Link each plate to order/counts/machine/spool/process/file checksum.
- Separate preparation/dispatch-ready/printing/removal/inspection/accepted/failed/rework.

### Step 5: incidents and reprints

- Use images/logs/human confirmation to scope detached parts/underextrusion.
- Record scrap/pending/usable quantities; reprint only evidenced deficits.
- Images suggest incidents, not hidden defects/root causes/dimensional acceptance.
- Recheck applicability on device/process changes; never resend already-started work.

### Step 6: complete kits and deliver

- Reconcile 50 accepted bases/100 clips; completed job counts do not prove kits.
- Record finishing/assembly/packaging with kit/batch traceability.
- Review planned/actual time, material, labor, scrap.
- Retain evidence-scoped process knowledge for future orders.

## 5. Complete enterprise modules

| Module | Purpose |
| --- | --- |
| Orders/kits | Revisions, counts, components, criteria, deadlines, changes |
| 3D/process planning | Geometry diagnostics, unresolved risks, orientation/support candidates/evidence |
| Orca execution | Profiles, controlled changes, actual slicing, previews/estimates |
| Trials/experiments | Calibration, trials, measurements, fit, approval |
| Process/material records | Validated conditions, revisions, machines/nozzles/spools/changes |
| Batches/device jobs | Planning, readiness, dispatch, observations, clearance |
| Incidents/reprints | Evidence, hypotheses, controlled checks, scrap/deficits |
| Quality/delivery | Item/sampling criteria, accepted quantities, finishing/kits/handover |
| Governance | Operator/process/inspector permissions, approval, audit, budgets, credentials |

Delegate requirements, geometry, candidates, experiments, production, quality as needed. Simple tasks do not invoke every role. Shared evidence/tasks do not turn written conclusions into physical execution facts.

## 6. Integration proposal

### Initially

Autumn owns tasks/experiments/evidence/artifacts; local execution uses fixed Orca. UI previews models/results/plans; Orca GUI remains for inspection/confirmation.

One isolated directory per task preserves hashes/effective configuration/engine/files/exit. Explicitly resolve/validate inheritance rather than guessing parameter names/machine capabilities.

### Subsequently

- Verify one authorized Moonraker/OctoPrint test backend; add other brands by capability matrix.
- Model upload/start/pause/cancel/resume separately; upload is not start.
- Review configuration/G-code before action; readiness/clearance/loading need real confirmation.
- Evaluate version-specific plugins/minimal embedding only if needed. Local development plugin code was seen, not release compatibility.
- Review AGPL-3.0 and component licenses before reuse/distribution/service deployment; invocation alone does not determine obligations.

## 7. Continuous delivery from zero

| Version | Added capability in the same application | Verifiable result |
| --- | --- | --- |
| v0.1 | Models/requirements/profiles/real slice | Downloadable repeatable results/risk list |
| v0.2 | 2–3 candidates/real comparison/web task history | Numeric process comparison with sources |
| v0.3 | Trials/measurements/feedback/signoff | Candidate-to-acceptance record |
| v0.4 | Incidents/few-factor experiments/revisions | Traceable changes/validation |
| v0.5 | One device/readiness/print readback | Approved process executes on test device with evidence |
| v0.6 | Components/batches/materials/planning/reprints | Same order reaches complete accepted kits |
| v0.7 | Roles/approval/audit/recovery/reconciliation | Sustained collaboration/traceable actions |
| v1.0 | Evaluations/deployment/backups/knowledge/actual data | Deliverable studio application |

Start with FDM, one machine/nozzle/material combination and functional part class. Expand devices/materials/multicolor/other processes separately; FDM rules do not automatically apply to resin/other processes.

## 8. Differentiation and quality to validate

Potential value: validate/reuse scoped processes and continuously know missing accepted parts, causes, and responsible next actors. Compare with the target studio's existing slicer/farm tools.

Measure:

- Reproducibility, parameter mapping, warnings.
- Estimate-versus-actual material/time deviations.
- Trials needed for first-article success and completeness of change evidence.
- False/missed alerts and verified hypotheses.
- Accurate quantities/kits; mistaken duplicate dispatch/reprints.
- Verifiable human effort/rework/scrap records.

Only source/public-document research is complete. No sample models, device inventory, production history, or physical trials were obtained. Begin product validation with one device, material, and measurable order.
