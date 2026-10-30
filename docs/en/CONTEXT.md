# Autumn Print domain language

English | [简体中文](../zh-CN/CONTEXT.md)

Autumn Print connects order requirements, process experiments, production jobs, and accepted delivery for FDM printing studios. These terms define consistent business meanings for documentation, UI, and implementation.

## Orders and models

**Print Order**: A customer commission to deliver finished parts in specified quantities and revisions under defined acceptance conditions.
_Avoid_: Slicing task, print job.

**Order Line**: The demand for one model revision and its delivery conditions within an order.
_Avoid_: Build plate, file.

**Kit**: One deliverable set composed of specified kinds and quantities of accepted parts.
_Avoid_: Total part count, completed print count.

**Model Revision**: A model revision with identifiable provenance, units, and content. An original submission and a repaired result are different revisions.
_Avoid_: Current file, repair overwrite.

**Mesh Inspection**: Checks of file readability, geometry, and mesh structure; these do not constitute physical quality or performance acceptance.
_Avoid_: Print quality certification.

## Processes and validation

**Filament Profile**: An agreed parameter set describing a material's printing behavior, distinct from the physical spool loaded on site.
_Avoid_: Material spool, inventory.

**Material Spool**: An identifiable physical spool with material, color, batch, remaining quantity, and other attributes.
_Avoid_: Filament profile, material type.

**Profile Snapshot**: The complete effective parameters actually used by a slice, with provenance and applicability conditions.
_Avoid_: Preset name, recommended parameters.

**Process Candidate**: A proposed process for a model and production conditions, awaiting comparison or validation.
_Avoid_: Best process, approved process.

**Slice Run**: One execution that generates slicing results from fixed inputs and configuration, with success, warnings, or failure.
_Avoid_: Physical printing, process approval.

**First Article Trial**: Initial production and inspection undertaken to validate a particular process and acceptance conditions.
_Avoid_: Automatic calibration, batch approval.

**Inspection**: A record made by an inspector about physical printed parts using explicit criteria, observations, and measurements.
_Avoid_: Device completion, model inference.

**Validated Process**: An explicitly scoped process revision approved by an authorized person on the basis of physical validation evidence.
_Avoid_: Universally optimal parameters, permanently valid preset.

## Production and delivery

**Production Batch**: A group of part demands and jobs organized under a common production arrangement.
_Avoid_: Order, whole-order delivery.

**Print Job**: Specific printing work associated with a target device, production file, and planned output.
_Avoid_: Slice run, order.

**Device Action**: One specific requested operation on a device, such as upload, start, pause, or cancel.
_Avoid_: Approval, print job completion.

**Readiness Confirmation**: An operator's confirmation of current device, bed, nozzle, loaded material, and other preparation conditions.
_Avoid_: Device online, previous bed clearance.

**Incident**: An event requiring investigation or disposition that may affect a job or accepted delivery.
_Avoid_: Confirmed root cause.

**Accepted Quantity Deficit**: For a specified order line and revision, the difference between demand and accepted quantities currently available to that order.
_Avoid_: Failed job count, remaining print files.

**Reprint Request**: A request for new production to fill a verified accepted quantity deficit, linked to the original incident or demand.
_Avoid_: Original action retry, duplicate start.

**Kit Completeness**: The required accepted quantity has been reached for every kind of part composing a kit.
_Avoid_: Sufficient total count, all devices idle.

## People and assistants

**Personal Workspace**: Orders, processes, documents, and production records managed by an individual owner, with use and approvals attributable to that owner.
_Avoid_: Enterprise offline cache, temporary personal demo.

**Enterprise Workspace**: Orders, processes, documents, and production records managed by an organization and maintained collaboratively within members' authorization scopes.
_Avoid_: Full access for every member, automatic personal workspace replica.

**User Role**: A set of personnel permissions for operations, process engineering, quality inspection, order management, or administration within an organization and authorized resources.
_Avoid_: Agent role.

**Agent Role**: An assistant's work responsibility, such as requirements checking, model inspection, process planning, or quality review, and its permitted capabilities.
_Avoid_: User permission, administrator identity.

**Process Approval**: Explicit acceptance of a specific process revision and its validation evidence.
_Avoid_: Authorization to start printing.

**Action Approval**: Authorization for a specific action on a particular device, file, parameters, and conditions.
_Avoid_: Permanent authorization for all subsequent operations.
