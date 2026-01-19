Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Value Source Specification

This specification defines the canonical **Value Source** categories for Paperhat.

A Value Source declares where a value originates. The runtime resolves Value Sources to populate Behavior Environment bindings.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define a canonical, exhaustive set of Value Source categories
* ensure consistent semantics across workflow, eventing, and presentation specifications
* clarify the relationship between Value Sources and Behavior evaluation

---

## 2. Relationship to Behavior (Normative)

Behavior is a pure expression language. It receives values through three mechanisms:

* `Argument` — the primary input value
* `Variable(name)` — environment lookup
* `Constant(value)` — literal constant

Value Sources are NOT Behavior concepts. Value Sources tell the runtime HOW to populate the Environment that Behavior evaluates against.

The relationship is:

1. Authored artifacts declare Value Sources for named bindings.
2. The runtime resolves each Value Source to an actual value.
3. The runtime populates the Behavior Environment with resolved values.
4. Behavior evaluates against the populated Environment using `Variable(name)`.

Behavior never sees Value Sources. It only sees resolved values in its Environment.

---

## 3. Value Source Categories (Normative)

The following categories are exhaustive for v0.1.

### 3.1 FromLiteral

A constant value authored directly in the declaration.

The value is known at authoring time and does not depend on runtime state or context.

### 3.2 FromContext

An ambient value provided by the runtime from session or execution context.

Context values are not persisted state. They describe the circumstances of execution.

Sub-kinds:

* **Actor** — the identity performing the action (from authentication/authorization context)
* **Tenant** — the organizational or customer context (for multi-tenant systems)
* **Locale** — language and region preferences
* **Time** — the current timestamp at the moment of resolution

Context sub-kinds are target-neutral. Both Kernel and HTML runtime provide these values.

### 3.3 FromState

An observable or persisted value read by the runtime.

State values are mutable and may change between executions.

Sub-kinds:

* **Projection** — a CQRS read model derived from event history (rebuildable from events)
* **Application** — in-memory application state (Redux, React Context, Zustand, MobX, etc.)
* **URL** — location state (path, query string, hash)
* **Storage** — browser persistence (localStorage, sessionStorage, IndexedDB, cookies)
* **DOM** — element-bound state (form values, element content, data-attributes)

State sub-kinds vary by target:

* Kernel: Projection, Application
* HTML runtime: Projection, Application, URL, Storage, DOM

### 3.4 FromTriggeringEvent

A value extracted from the event that triggered the current execution.

This category applies only in reactive contexts where execution is triggered by an event.

### 3.5 FromStepOutput

A value produced by a named previous step in a workflow.

The step MUST have completed before this Value Source can be resolved.

### 3.6 FromWorkflowInput

An input parameter passed to the workflow when it was invoked.

Workflow inputs are declared in the workflow definition and supplied by the caller.

### 3.7 FromIteration

The current element in an iteration context.

This category applies when mapping, filtering, or otherwise iterating over a collection. The runtime binds the current element for each iteration.

---

## 4. Resolution Semantics (Normative)

### 4.1 Resolution Order

Value Sources are resolved before Behavior evaluation begins.

All declared Value Sources for a given Behavior invocation MUST be resolved to populate the Environment.

### 4.2 Missing Values

If a Value Source cannot be resolved (for example, a referenced step has not completed, or a state key does not exist), the runtime MUST either:

* populate the Environment binding with `<Absent/>`, OR
* fail resolution with a typed diagnostic

The choice depends on the binding's declared optionality.

### 4.3 Determinism

For a given execution context, Value Source resolution MUST be deterministic.

For durable event sourcing and replay:

* FromLiteral is deterministic by definition.
* FromContext values (Time, Actor, Tenant, Locale) MUST be captured at event time for replay.
* FromState (Projection) MUST be rebuildable from event history.
* FromTriggeringEvent is captured in the event record.
* FromStepOutput, FromWorkflowInput, and FromIteration are determined by the workflow execution.

---

## 5. Target Independence (Normative)

Value Source categories are semantic, not implementation-specific.

Authors declare WHAT value they need and WHERE it comes from semantically.

Targets realize the resolution using appropriate mechanisms:

* Kernel may resolve FromState/Projection via SPARQL queries.
* HTML runtime may resolve FromState/URL via `window.location`.
* HTML runtime may resolve FromState/Storage via `localStorage.getItem()`.

These realizations are target details, not semantics.

---

## 6. Relationship to Other Specifications

This specification is referenced by:

* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Eventing and Event Sourcing](../../events/eventing-and-event-sourcing/)
* [Workflow Orchestration](../../workflow/workflow-orchestration/)

---

**End of Value Source Specification v0.1**
