Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Specifications (0.1)

This index links the active **Paperhat specifications** for version **0.1**.

Specifications define **canonical formats**, **artifact classes**, and **authoring semantics** that implementations MUST follow.

Conformance rule (Normative): `paperhat.dev` is the sole normative source of truth for the Paperhat specification. Conforming implementations MAY be written in any language, but MUST implement the specified semantics exactly.

Note: This index assumes the 0.1 spec folders are organized into category subfolders (e.g. `foundation/`, `behavior/`, `validation/`).

---

## 1. Purpose

This index exists to:

* provide a single click-through entry point for Paperhat Specs on GH Pages
* make the 0.1 spec set browsable and stable
* link only to spec folders (kebab-case) whose document is always `index.md`
* group specs by category so the set remains navigable as it grows

---

## 2. Taxonomy (0.1)

This spec set is organized by:

* [Paperhat Spec Taxonomy](foundation/spec-taxonomy/)

---

## 3. Spec Index (0.1)

### 3.1 Foundation

* [Contract of Contracts](foundation/contract-of-contracts/)
* [Scope, Boundaries, and Non-Goals](foundation/scope-boundaries-and-non-goals/)
* [Kernel Architecture](foundation/kernel-architecture/)
* [Identifier Canonicalization](foundation/identifier-canonicalization/)
* [Workspace and Work Filesystem Roots](foundation/workspace-filesystem-root/)
* [Module Filesystem Assembly](foundation/module-filesystem-assembly/)

### 3.2 Behavior

* [Behavior Dialect](behavior/behavior-dialect/)
* [Behavior Dialect Semantics](behavior/behavior-dialect-semantics/)
* [Behavior Vocabulary](behavior/behavior-vocabulary/)
* [Value Ordering and Structural Equality](behavior/value-ordering-and-structural-equality/)
* [Behavior Diagnostic Codes](behavior/behavior-diagnostic-codes/)
* [Behavior Program Encoding](behavior/behavior-program-encoding/)
* [Behavior Program Surface Form](behavior/behavior-program-surface-form/)

### 3.3 Validation

* [Data Validation and Shape Constraints](validation/data-validation-and-shape-constraints/)
* [Validation Evaluation and Diagnostics](validation/validation-evaluation-and-diagnostics/)
* [Regular Expression Profile](validation/regular-expression-profile/)
* [Diagnostic Messaging and Help Philosophy](validation/diagnostic-messaging-and-help-philosophy/)
* [Localized Messages and Locale Resolution](validation/localized-messages-and-locale-resolution/)

### 3.4 Workflow

* [Workflow Orchestration](workflow/workflow-orchestration/)
* [Workflow Versioning and Compatibility](workflow/workflow-versioning-and-compatibility/)
* [Workflow Testing and Simulation](workflow/workflow-testing-and-simulation/)
* [Subworkflows and Reuse](workflow/subworkflows-and-reuse/)
* [Conditions and Branching](workflow/conditions-and-branching/)
* [Looping and Batching](workflow/looping-and-batching/)
* [Triggers and Scheduling](workflow/triggers-and-scheduling/)
* [Merge, Join, and Correlation](workflow/merge-join-and-correlation/)
* [Concurrency and Parallelism](workflow/concurrency-and-parallelism/)
* [Resource Limits and Rate Limiting](workflow/resource-limits-and-rate-limiting/)
* [Reliability and Failure Semantics](workflow/reliability-and-failure-semantics/)
* [Idempotency and De-duplication](workflow/idempotency-and-deduplication/)
* [Approvals and Human-in-the-Loop](workflow/approvals-and-human-in-the-loop/)
* [Cancellation and Termination](workflow/cancellation-and-termination/)

### 3.5 State

* [State, Commands, and Continuations](state/state-commands-and-continuations/)
* [Durable Execution: Run History and Replay](state/durable-execution-run-history-and-replay/)

### 3.6 Data

* [Data Stores and Shared Variables](data/data-stores-and-shared-variables/)
* [Data Transformation and Mapping](data/data-transformation-and-mapping/)
* [Message Pack Imports and Interchange](data/message-pack-imports-and-interchange/)
* [Artifacts and Attachments](data/artifacts-and-attachments/)
* [Provenance and Lineage](data/provenance-and-lineage/)
* [Search, Indexing, and Query](data/search-indexing-and-query/)

### 3.7 Events

* [Eventing and Event Sourcing](events/eventing-and-event-sourcing/)
* [Notifications and Alerts](events/notifications-and-alerts/)

### 3.8 Operations

* [Run Logs and Observability](operations/run-logs-and-observability/)

### 3.9 Security

* [Authentication and Authorization](security/authentication-and-authorization/)
* [Integrations and Credentials](security/integrations-and-credentials/)
* [Secrets and Redaction](security/secrets-and-redaction/)

### 3.10 Design

* [Design Intent Definition](design/design-intent-definition/)
* [Design Policy Definition](design/design-policy-definition/)
* [View and Policy Selection](design/view-and-policy-selection/)

### 3.11 Presentation

* [Presentation Plan Definition](presentation/presentation-plan-definition/)
* [Presentation Plan Encoding](presentation/presentation-plan-encoding/)
* [View Definition](presentation/view-definition/)
* [View Composition: Slots, Fills, and Use](presentation/view-composition-slots-fills-and-use/)

### 3.12 HTML

* [HTML Runtime Contract](html/html-runtime-contract/)
* [HTML Runtime Data Shapes](html/html-runtime-data-shapes/)
* [HTML Runtime DOM Binding Conventions](html/html-runtime-dom-binding/)

### 3.13 Workbench

* [Workbench Index](workbench/)
* [Workbench Principles](workbench/workbench-principles/)
* [Workbench Contract](workbench/workbench-contract/)
* [Core Contract](workbench/core-contract/)
* [Core Command Protocol](workbench/core-command-protocol/)
* [Work Filesystem Contract](workbench/filesystem-contract/)
* [Work Configuration Contract](workbench/workspace-configuration-contract/)
* [Preview and Build Orchestration Contract](workbench/preview-and-build-orchestration-contract/)
* [Template Format](workbench/template-format/)
* [Templates and File Plans](workbench/templates-and-file-plans/)
* [ConceptForm Contract](workbench/conceptform-contract/)
* [Authoring Projections Contract](workbench/authoring-projections-contract/)
* [Assistive Authoring Contract](workbench/assistive-authoring-contract/)
* [Diagnostic Messaging and Help](workbench/diagnostic-messaging-and-help/)
* [Introspection and Explanation Contract](workbench/introspection-and-explanation-contract/)

### 3.14 Adapters

* [Graph Store Adapter Contract](adapters/graph-store-adapter-contract/)
* [Vector Store Adapter Contract](adapters/vector-store-adapter-contract/)

### 3.15 Commerce

* [Commerce Entities and Payments](commerce/commerce-entities-and-payments/)
* [Reckoning and Price Transformations](commerce/reckoning-and-price-transformations/)
* [Promotions, Eligibility, and Stacking](commerce/promotions-eligibility-and-stacking/)
* [Subscriptions and Billing Intents](commerce/subscriptions-and-billing-intents/)
* [Inventory Promising and Availability](commerce/inventory-promising-and-availability/)
* [Fulfillment, Shipping, and Delivery](commerce/fulfillment-shipping-and-delivery/)
* [Tax Intents and Tax Reckoning](commerce/tax-intents-and-tax-reckoning/)
* [Refund Policies and Refund Reckoning](commerce/refund-policies-and-refund-reckoning/)
* [Stored Value Application](commerce/stored-value-application/)
* [Loyalty Earning and Redemption](commerce/loyalty-earning-and-redemption/)
* [B2B Credit and Net Terms](commerce/b2b-credit-and-net-terms/)
