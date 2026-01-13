Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Workflow Orchestration Specification

This specification defines Paperhat’s target-independent semantics for **workflows**: declarative orchestration of multi-step processes expressed as data.

This document governs **workflow semantics only**.
It does **not** define transport protocols, integration runtimes, deployment topology, or vendor-specific automation systems.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define workflows as declarative, inspectable, and validated artifacts
* define steps, gates, and transitions without imperative control flow in authored documents
* ensure workflow evaluation is deterministic given explicit inputs
* define how workflows integrate with Commands, Events, State, and Authorization
* preserve target independence by separating meaning from realization

---

## 2. Scope

This specification governs:

* workflow definitions (structure, step kinds, transitions)
* gating and decision semantics
* workflow inputs and outputs
* workflow execution plans emitted by the Kernel
* auditability and explainability requirements

This specification does **not** govern:

* the runtime that executes external actions
* how integrations are performed (HTTP clients, queues, schedulers)
* retry algorithms and backoff mechanisms
* human interface design for task approval

---

## 3. Related Specifications

This specification is designed to compose with:

* [Authentication and Authorization](../authentication-and-authorization/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)
* [State, Commands, and Continuations](../state-commands-and-continuations/)

---

## 4. Core Invariants (Hard)

The following invariants are non-negotiable:

1. **Workflows are data.**
2. **No imperative control flow in authored content.** Authoring declares structure and constraints, not code.
3. **Deterministic planning.** Given the same workflow definition, facts, and inputs, the Kernel MUST emit the same plan.
4. **Explicit inputs.** Time, actor identity, environment, and integration results MUST NOT be implicit.
5. **Auditability.** Workflow decisions and transitions MUST be explainable and recordable.

---

## 5. Definitions (Normative)

### 5.1 Workflow

A **Workflow** is a declarative process definition consisting of steps, transitions, and constraints.

A Workflow has:

* identity
* input schema
* step graph
* output schema
* validity constraints

---

### 5.2 Step

A **Step** is a node in a workflow graph.

Steps MAY represent:

* evaluation (pure)
* gating/approval (decision)
* emission of intent (command or event)
* external action request (planned effect)

Step execution is not defined by this specification.
This specification defines step meaning and constraints.

---

### 5.3 Gate

A **Gate** is a declarative constraint that must be satisfied before proceeding.

Gates MAY depend on:

* authorization decisions
* state or projection values
* explicit external inputs

---

### 5.4 Transition

A **Transition** connects steps.

Transitions MAY be conditional.
Conditions MUST be declarative and validated.

---

### 5.5 Workflow Plan

A **Workflow Plan** is an emitted, inspectable artifact produced by the Kernel that represents the actionable interpretation of a Workflow for a specific realization target.

Plans MUST NOT redefine workflow meaning.

---

## 6. Workflow Structure (Normative)

A Workflow MUST define:

* a single entry step
* one or more steps
* valid transitions

Workflows MAY be cyclic only if the Kernel explicitly allows the cycle and defines termination semantics.

---

## 7. Step Kinds (Normative)

The Kernel MUST define allowed step kinds.

At minimum, step kinds SHOULD include:

* **Evaluate** — a pure deterministic evaluation producing derived values
* **Decide** — a deterministic decision step producing allow/deny (with Help)
* **EmitCommand** — declaratively requests a Command (see State/Commands)
* **PublishEvent** — declaratively requests an Event publish (see Eventing)
* **RequestExternalAction** — declares a required external result without defining protocol

Step kinds MUST declare:

* required inputs
* produced outputs
* failure modes (as Help/diagnostics)

---

## 8. External Action Requests (Restricted) (Normative)

`RequestExternalAction` exists to support workflows that must pause awaiting outcomes from systems outside Paperhat’s semantic universe.

`RequestExternalAction` MUST be a declaration of requirement only.

It MUST:

* declare an `actionKind` identifier (semantic identity)
* declare required inputs (via target-independent Value Sources)
* declare an expected output schema
* declare provenance and verification requirements for any supplied result
* allow pending semantics when required inputs or results are not yet available

It MUST NOT:

* embed protocol or transport details (for example: URLs, HTTP methods, headers, queue names)
* embed credential material or secrets
* define retry logic, backoff, scheduling, or deployment concerns

The Kernel MAY emit a Workflow Plan that describes how a target can realize the request.
Targets own execution and protocol details.
Workflow meaning and constraints remain unchanged.

---

## 9. Integration with Security (Normative)

Workflows MUST be able to declare security gates.

Security gates MUST be defined in terms of:

* access requests
* required claims, capabilities, roles, or permissions

Authorization evaluation is owned by the Kernel.

---

## 10. Integration with State and Events (Normative)

Workflows MAY:

* emit Commands
* publish Events
* depend on projections/state

Workflows MUST NOT treat mutable target state as authoritative.

---

## 11. Determinism and External Inputs (Hard)

Workflow planning and evaluation MUST be deterministic given:

* Kernel version
* Workflow definition
* authoritative facts (including events)
* bound external inputs

External inputs MUST be explicit.

External action results MUST be represented as explicit facts or inputs with provenance.

---

## 12. Pending and Asynchronous Semantics (Normative)

Workflows MUST support the concept of pending steps.

Pending is not an error.
Pending is a state of incomplete evaluation due to awaiting explicit inputs or external action results.

Targets MAY realize pending with target-specific representations.

---

## 13. Auditability (Hard)

It MUST be possible to record:

* the workflow identity and version
* the step transitions taken
* decisions and their reasons (Help)
* relevant inputs and provenance

Storage is a realization detail.

---

## 14. Target Independence (Hard)

This specification MUST NOT require:

* any specific runtime orchestrator
* any specific integration mechanism
* any specific scheduling system
* any particular user interface

Targets MAY execute workflow plans using target-appropriate systems, provided semantic meaning and constraints are preserved.
