Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Specifications (0.1)

This index links the active **Paperhat specifications** for version **0.1**.

Specifications define **canonical formats**, **artifact classes**, and **authoring semantics** that implementations MUST follow.

---

## 1. Purpose

This index exists to:

* provide a single click-through entry point for Paperhat Specs on GH Pages
* make the 0.1 spec set browsable and stable
* link only to spec folders (kebab-case) whose document is always `index.md`

---

## 2. Taxonomy (0.1)

This spec set is organized by:

* [Paperhat Spec Taxonomy](spec-taxonomy/)

---

## 3. Spec Index (0.1)

### 3.1 Foundation

* [Contract of Contracts](contract-of-contracts/)
* [Identifier Canonicalization](identifier-canonicalization/)
* [Workspace Filesystem Root](workspace-filesystem-root/)
* [Module Filesystem Assembly](module-filesystem-assembly/)

### 3.2 Semantics and Validation

* [Behavior Program Encoding](behavior-program-encoding/)
* [Behavior Dialect](behavior-dialect/)
* [Data Validation and Shape Constraints](data-validation-and-shape-constraints/)
* [Localized Messages and Locale Resolution](localized-messages-and-locale-resolution/)

### 3.3 Execution and Reliability

* [Eventing and Event Sourcing](eventing-and-event-sourcing/)
* [Durable Execution: Run History and Replay](durable-execution-run-history-and-replay/)
* [Reliability and Failure Semantics](reliability-and-failure-semantics/)
* [Concurrency and Parallelism](concurrency-and-parallelism/)
* [Resource Limits and Rate Limiting](resource-limits-and-rate-limiting/)
* [Approvals and Human-in-the-Loop](approvals-and-human-in-the-loop/)
* [Conditions and Branching](conditions-and-branching/)
* [Looping and Batching](looping-and-batching/)
* [Merge, Join, and Correlation](merge-join-and-correlation/)
* [Cancellation and Termination](cancellation-and-termination/)
* [Subworkflows and Reuse](subworkflows-and-reuse/)
* [Workflow Versioning and Compatibility](workflow-versioning-and-compatibility/)
* [Workflow Testing and Simulation](workflow-testing-and-simulation/)
* [State, Commands, and Continuations](state-commands-and-continuations/)
* [Triggers and Scheduling](triggers-and-scheduling/)
* [Workflow Orchestration](workflow-orchestration/)
* [Idempotency and De-duplication](idempotency-and-deduplication/)

### 3.4 Data and Interchange

* [Data Stores and Shared Variables](data-stores-and-shared-variables/)
* [Data Transformation and Mapping](data-transformation-and-mapping/)
* [Artifacts and Attachments](artifacts-and-attachments/)
* [Search, Indexing, and Query](search-indexing-and-query/)
* [Provenance and Lineage](provenance-and-lineage/)
* [Message Pack Imports and Interchange](message-pack-imports-and-interchange/)

### 3.5 Security and Identity

* [Authentication and Authorization](authentication-and-authorization/)
* [Integrations and Credentials](integrations-and-credentials/)
* [Secrets and Redaction](secrets-and-redaction/)

### 3.6 Operations and Observability

* [Run Logs and Observability](run-logs-and-observability/)
* [Notifications and Alerts](notifications-and-alerts/)

### 3.7 Presentation and Realization

* [Design Policy Definition](design-policy-definition/)
* [Presentation Plan Definition](presentation-plan-definition/)
* [Presentation Plan Encoding](presentation-plan-encoding/)
* [View and Policy Selection](view-and-policy-selection/)
* [View Definition](view-definition/)
* [View Composition: Slots, Fills, and Use](view-composition-slots-fills-and-use/)

### 3.8 Domain (Commerce)

* [Reckoning and Price Transformations](reckoning-and-price-transformations/)
* [Commerce Entities and Payments](commerce-entities-and-payments/)
* [Promotions, Eligibility, and Stacking](promotions-eligibility-and-stacking/)
* [Stored Value Application](stored-value-application/)
* [Refund Policies and Refund Reckoning](refund-policies-and-refund-reckoning/)
* [Loyalty Earning and Redemption](loyalty-earning-and-redemption/)
* [B2B Credit and Net Terms](b2b-credit-and-net-terms/)
* [Subscriptions and Billing Intents](subscriptions-and-billing-intents/)
* [Inventory Promising and Availability](inventory-promising-and-availability/)
* [Tax Intents and Tax Reckoning](tax-intents-and-tax-reckoning/)
* [Fulfillment, Shipping, and Delivery](fulfillment-shipping-and-delivery/)
