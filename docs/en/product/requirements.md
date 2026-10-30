# Product requirements

English | [简体中文](../../zh-CN/product/requirements.md)

Status: design baseline, pending implementation and validation. This document defines users, goals, scope, and success criteria. See the [functional specification](functional-spec.md) for behavior and the [architecture overview](../architecture/overview.md) for implementation. Technology, directories, and implementation order are defined elsewhere.

## Users and goals

Autumn Print serves individual FDM users, printing studios, print farms, and enterprise prototyping centers. It connects models, process candidates, trials, production, incidents, and accepted delivery around an order.

Users need to know which information is missing, what the actual tradeoffs between candidates are, which processes have been validated, which changed conditions require review, and which accepted parts are still needed for delivery.

## Requirements baseline

| ID | Requirement | Success criteria | Features |
| --- | --- | --- | --- |
| R-01 | Personal users install the application and configure a model connection | Configure it in the UI and run a sample without deploying a server or installing development tools | F-01, F-02, F-05 |
| R-02 | Enterprise members collaborate through a server | Members access only authorized resources; administrators configure models centrally | F-01, F-12 |
| R-03 | Local and enterprise modes provide the same business agent capabilities | Both verify the same business scenarios, tool facts, and rules; model, device, and authorization differences may affect capabilities | F-02, F-05 |
| R-04 | Process advice is grounded in actual tool results | Parameters, warnings, estimates, and input revisions are traceable; unknown capabilities are explicit | F-03, F-04, F-05 |
| R-05 | Preserve physically validated processes | Measurements, fit, approvals, and applicability conditions are linked; changed models/conditions can be reviewed | F-06, F-07 |
| R-06 | Organize production and delivery quantities correctly | Kits, revisions, accepted quantities, and reprint deficits reconcile; duplicate events do not increase output | F-08, F-09, F-10 |
| R-07 | Long tasks do not depend on the workbench window | Closing a window does not cancel tasks; interrupted state is inspectable; unknown external results are investigated first | F-05, F-08 |
| R-08 | Personal/enterprise data and device control ownership are explicit | No automatic upload/merge of personal data; switching does not migrate active tasks or compete for devices | F-11, F-12 |

## Product scope

- Model/order import, integrity inspection, controlled repair candidates, and actual slicing comparison.
- First-article trials, physical inspection, experiment analysis, process revisions, and approval.
- Devices and materials, batches, incident handling, accepted quantity deficits, reprints, kit completeness, and delivery.
- Agent plans, tool evidence, user waits, recovery, budgets, and history.
- Complete personal workspaces and enterprise collaboration, role/resource authorization, audit, and administration.

## Scope limits

The current domain is FDM. Declare device support by verified model/protocol; do not promise all-brand control, automatic repair of every defect, or universal model API compatibility. Model inference does not replace real slicing, dimensional measurement, physical inspection, or human approval. Other printing processes, general manufacturing certification, and unsupported claims of a best process are outside current commitments.

## User-visible constraints

- Configure API URL, key, and model in the UI. Explain capability-check failures instead of presenting them as success.
- Authorized task content goes to the provider when a remote model is used; locally stored data does not imply local inference.
- Software execution and monitoring are not guaranteed during shutdown or sleep; reconcile actual device outcomes on recovery.
- Personal and enterprise workspaces do not synchronize automatically; migration requires explicit action and authorization review.
- Publish file-size, concurrency, response-time, and device-support limits after measurement; no unvalidated numeric commitments are made here.

## End-to-end acceptance

See the [functional specification](functional-spec.md) for behavior and the [validation plan](../engineering/validation.md) for engineering and failure checks. The fixed 50-kit bracket order is a continuous acceptance fixture, not the only supported order form.
