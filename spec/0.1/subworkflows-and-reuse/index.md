Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Subworkflows and Reuse Specification

This specification defines Paperhat’s target-independent semantics for **subworkflows**, **workflow reuse**, and **workflow calls**.

This document governs semantic meaning and planning interfaces.
It does **not** define runtime module systems, deployment packaging, network calls, or target-specific invocation mechanisms.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to invoke other workflows as reusable units
* define input/output contracts for workflow calls
* preserve determinism and auditability across workflow boundaries
* keep reuse semantics target-independent

---

## 2. Scope

This specification governs:

* workflow call constructs
* parameter mapping into subworkflows
* result mapping out of subworkflows
* version pinning and compatibility expectations
* call boundaries for run logs, correlation, and cancellation

This specification does **not** govern:

* packaging formats
* deployment and distribution
* network protocols
* runtime execution engines

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Cancellation and Termination](../cancellation-and-termination/)
* [Merge, Join, and Correlation](../merge-join-and-correlation/)

---

## 4. Core Invariants (Hard)

1. **Calls are declarative.** A workflow call MUST be representable as data.
2. **Deterministic planning.** The Kernel MUST be able to plan workflow calls deterministically.
3. **Explicit contracts.** Inputs and outputs MUST have declared type expectations.
4. **Auditability across boundaries.** It MUST be possible to trace which subworkflow ran, with what inputs, and what outputs were produced.
5. **Target independence.** Calls MUST NOT assume a transport or deployment mechanism.

---

## 5. Definitions (Normative)

### 5.1 Subworkflow

A **Subworkflow** is a workflow artifact intended to be invoked by another workflow.

---

### 5.2 Workflow Call

A **WorkflowCall** is a step that invokes a target workflow.

A WorkflowCall MUST declare:

* target workflow identity
* version selection or pinning policy
* input mapping into the callee
* expected output type(s)

---

### 5.3 Call Inputs and Outputs

Call inputs MUST be derived from declared value sources.

Call outputs MUST be typed and MUST be usable as step outputs in the caller.

---

### 5.4 Version Pinning

A workflow call MUST define how the callee version is selected.

At minimum, the Kernel MUST support:
At minimum, the Kernel MUST support:

* exact version pin
* compatible version range (semantically defined)

---

## 6. Planning Semantics (Normative)

Kernel planning MUST be able to:

* validate that a callee exists and is compatible
* validate input mappings against callee expectations
* validate caller expectations for callee outputs

Planning MUST remain deterministic.

---

## 7. Run Logs and Correlation (Normative)

A workflow call MUST be observable.

Run logs MUST be able to record:

* call identity
* callee identity and version selected
* correlation between caller run and callee run
* input and output references (as permitted data)

---

## 8. Cancellation Propagation (Normative)

Workflow calls MUST define cancellation propagation semantics.

At minimum:

* cancellation of a caller MAY propagate to the callee
* cancellation of a callee MUST produce a typed outcome visible to the caller

Propagation rules MUST be declarative.

---

## 9. Failure and Reliability (Normative)

Failure outcomes of a callee MUST be representable to the caller.

Reliability policy MAY apply:

* to the call step
* within the callee

The Kernel MUST preserve auditability about where a retry occurred.

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* network invocation
* RPC protocols
* packaging formats

Targets may realize workflow calls using any appropriate mechanism, provided semantic meaning, determinism of planning, and recordability requirements are preserved.
