# Functional specification

English | [简体中文](../../zh-CN/product/functional-spec.md)

Status: complete target capabilities, pending implementation. This document defines user behavior, business rules, and acceptance. See [requirements](requirements.md) for goals and [architecture](../architecture/overview.md) for implementation. Feature IDs identify capabilities, not delivery order.

## Feature and mode matrix

| ID | Feature | Personal | Enterprise | Execution and confirmation | Acceptance |
| --- | --- | --- | --- | --- | --- |
| F-01 | Workspace and first use | Create a local workspace | Connect to a server and sign in | User selects; system initializes | No manual configuration editing; preserve failure reasons |
| F-02 | Model connection | Configure personal API URL/key/model | Use administrator-authorized models | User/administrator configures; system checks | Distinguish authentication, reachability, and capability failures; never redisplay a saved key |
| F-03 | Orders and models | Supported | Supported within resource authorization | User supplies; tools inspect | Explicit revisions, units, kits, and missing information; preserve originals |
| F-04 | Inspection, repair, and slicing | Supported | Supported through the selected edge executor | Geometry/slicing tools execute; user accepts repairs | Trace inputs/configuration/engine/results; unsupported checks never appear passed |
| F-05 | Agent tasks and candidate comparison | Supported | Subject to organization policy | Agent proposes; tools establish facts; user supplies input | Inspect plans, evidence, budget, waits, cancellation, errors, and recovery |
| F-06 | First-article trials and inspection | Owner records/confirms | Authorized personnel record/confirm | People execute, measure, and judge | Unmeasured remains unknown; print completion is not acceptance |
| F-07 | Processes and knowledge | Personal process records | Authorized enterprise records | Agent proposes; people approve | Fix revisions and conditions in approvals; edits preserve history |
| F-08 | Devices, materials, and actions | Locally authorized devices | Registered enterprise devices | People prepare/approve; tools execute | Separate action state from device facts; reconcile unknown outcomes first |
| F-09 | Batches and production planning | Supported | Supported with collaboration | Agent proposes; program validates; people confirm | Check material/device compatibility; plans are distinct from actual output |
| F-10 | Incidents, reprints, and delivery | Supported | Subject to role authorization | Agent analyzes; people inspect | Correct deficits, revisions, and kits; repeated handling does not duplicate counts |
| F-11 | Workspace switching and migration | Explicit export | Authorized explicit import | User acts; enterprise reviews | Exclude credentials/active tasks; no automatic sync or control transfer |
| F-12 | Authorization, audit, and administration | Local owner confirmations/history | Organization, roles, resources, approval, and audit | People administer; program enforces | Prompt edits cannot elevate access; revocation affects subsequent operations |

## First use and model configuration

Personal: choose personal mode → create workspace → enter model connection → check connectivity and required capabilities → save credential reference → enter workbench. Invalid keys, unreachable networks, missing tool-call support, and canceled setup are distinct. Failure does not discard existing records or substitute simulated results.

Enterprise: enter enterprise server URL → sign in → select an authorized workspace → use organization-authorized models/devices. Name the model API URL and enterprise server URL separately. Administrator changes to connection permissions do not rewrite existing task evidence.

## Tasks and the business workflow

Import order/model → complete requirements and units → inspect geometry → accept a repair revision if necessary → compare actual slices → print/measure first articles → approve process → plan batches → classify pending/accepted/rework/scrap → fill deficits → verify kits and deliver.

Agents propose plans/candidates; deterministic checks and tools return facts; people approve processes/actions and judge physical parts. See [agents and tools](../architecture/agent-and-tools.md) for execution design.

Distinguish queued, running, waiting for input, waiting for edge results, succeeded, failed, and canceled tasks. Unknown external action outcomes are displayed separately and are not ordinary retryable failures. Users can see who must act next, where evidence is recorded, and what permits recovery. Persistence and message protocols belong to architecture.

## Business objects and rules

The following define complete business meanings. Canonical terminology is in [CONTEXT.md](../CONTEXT.md).

| Object | Meaning | Relationships and constraints |
| --- | --- | --- |
| `Order / OrderLine` | Deadline, part quantity, material, and acceptance requirements | Lines reference fixed model revisions; kits cannot be represented by a total count alone |
| `ModelRevision` | Original model, revision, hash, units, and inspection | Changes/repairs create a new revision and preserve the original |
| `Machine / MachineState` | Device capabilities and current observations | Model/nozzle/firmware conditions are distinct from live state |
| `MaterialSpool` | Material, color, batch, remaining amount, and status | Physical spool is distinct from a filament profile |
| `ProfileSnapshot` | Complete effective slice configuration | Preserve resolved inheritance, sources, and engine version |
| `ProcessCandidate` | Process awaiting comparison | Changes have scope, differences, and reasons; not trial-approved |
| `SliceRun` | One actual slice and its output | Bind input hashes, configuration, engine, exit status, warnings, and estimates |
| `Trial / Inspection` | Trial production and physical acceptance | Preserve photos, measurements, fit feedback, inspector, and conclusion separately |
| `ValidatedProcess` | Approved process and applicability | Bind validated model, machine conditions, material, and evidence |
| `Batch / PrintJob` | Batch and device-specific job | Associate parts/planned quantities; verify real output separately |
| `Incident / ReprintRequest` | Incident, impact, and reprint | Preserve original batch/cause; calculate from accepted deficit |
| `Approval / AuditEvent` | Decision about a specific revision/action | Review changed parameters/conditions; approval does not prove execution |
| `Task / Step / Event` | Agent task, steps, and progress | Conversation, slice, print, inspection, and order states are distinct |

### Four facts that must remain distinct

| Fact | What it proves | What still needs confirmation |
| --- | --- | --- |
| Slicing succeeded | Engine generated corresponding output | Device conditions, trial performance, and physical quality |
| Device reports completion | This device job ended | Part removal, actual quantity, appearance, and dimensions |
| First article passed | Recorded conditions met inspected criteria | Applicability to other machines, materials, or models |
| Order ready for delivery | Accepted parts meet kit/quantity requirements | Finishing, packaging, handover, and other agreed work |

Pending parts do not count as accepted output. Reclassifying the same parts from pending to accepted changes classification, not total quantity. Rework, scrap, inspection revocation, and old-revision quarantine must also be traceable.

## Continuous acceptance scenario

### Fixed business fixture

A studio receives an order for **50 kits of black PETG snap-fit brackets**:

- Each kit contains **1 base and 2 clips**: 50 bases and 100 clips in total.
- Clips must assemble with the specified mating part; record customer-confirmed critical dimensions and tolerances.
- Contact surfaces should have no obvious support marks; the responsible person confirms the inspection method.
- There are 3 sample printers and several spools; one printer has a newly replaced nozzle.
- The order has a deadline, staffing periods, and bed-clearance time.
- Order rules explicitly state whether accepted first articles count toward delivery.

Use synthetic or authorized models, devices, and material records. This demonstrates ordinary functional parts and makes no safety-critical performance certification claim.

### Scenario events

1. Model import reveals that units need confirmation.
2. Two orientations trade off contact-surface supports against printing time.
3. First articles finish printing, but clips fit too tightly.
4. Revised trials pass, producing a process with explicit applicability.
5. One production plate encounters an incident; some parts await inspection and others are scrap.
6. The customer revises the clip model, requiring review of queued work and old-revision parts.
7. Reprinting and inspection finish; accepted quantities complete the kits for delivery.

The same order spans these events. Other models/materials verify reuse. See the engineering delivery plan for implementation order.

## Workbench entry points

Orders/models, process comparison, first articles/experiments, process library, agent task details, devices/materials, production board, incidents/quality, and settings. Enterprise workspaces also expose organization and role administration. Pages expose functions; they do not determine authorization.
