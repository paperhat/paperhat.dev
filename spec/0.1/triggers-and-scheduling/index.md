Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Triggers and Scheduling Specification

This specification defines Paperhat’s target-independent semantics for **workflow triggers** and **scheduling**.

This document governs **trigger meaning and constraints only**.
It does **not** define protocol implementations, job schedulers, clocks, transport mechanisms, or deployment architecture.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define triggers as declarative workflow entry conditions
* define time-based scheduling without naming a particular scheduler
* define event-based triggering by semantic event patterns
* preserve target independence by separating meaning from realization
* ensure deterministic planning and auditable execution

---

## 2. Scope

This specification governs:

* trigger declarations for workflow entry
* time schedules and calendars as declarative constraints
* event-trigger patterns that reference the eventing vocabulary
* input binding requirements for trigger evaluation
* auditability requirements for trigger activations

This specification does **not** govern:

* how a scheduler is implemented
* how clocks, time zones, or calendars are sourced
* how triggers are transported or invoked
* how workflow runners are hosted

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)
* [Authentication and Authorization](../authentication-and-authorization/)

---

## 4. Core Invariants (Hard)

The following invariants are non-negotiable:

1. **Triggers are declarative.**
2. **Trigger evaluation uses explicit inputs.** Time, actor identity, and environment MUST NOT be implicit.
3. **Deterministic planning.** Given identical facts and inputs, Kernel MUST emit the same trigger plan.
4. **Auditability.** Trigger activations MUST be explainable and recordable.
5. **No protocol semantics.** Triggers must not embed protocol or transport details.

---

## 5. Definitions (Normative)

### 5.1 Trigger

A **Trigger** is a declarative condition that causes a Workflow to begin.

A Trigger MUST specify:

* the target Workflow
* required inputs for the Workflow entry
* activation constraints

---

### 5.2 Trigger Activation

A **Trigger Activation** is a recorded occurrence of a Trigger firing.

Trigger Activations MUST be attributable to explicit inputs and provenance.

---

### 5.3 Trigger Plan

A **Trigger Plan** is an emitted artifact produced by Kernel that describes how a target can realize triggers and scheduling for a workflow.

Plans MUST NOT redefine trigger meaning.

---

## 6. Trigger Kinds (Normative)

Kernel MUST define allowed trigger kinds.

At minimum, trigger kinds MUST include:

* **ManualTrigger** — explicit human or system initiation
* **TimeTrigger** — schedule-based initiation
* **EventTrigger** — initiation based on semantic event patterns

Trigger kinds MUST declare:

* required inputs
* required provenance
* activation constraints

---

## 7. Manual Trigger (Normative)

A ManualTrigger declares that a Workflow may be started by an explicit request.

ManualTrigger MUST NOT define user interface.

ManualTrigger MAY declare authorization requirements.

---

## 8. Time Trigger (Normative)

A TimeTrigger declares that a Workflow may be started based on time schedules.

### 8.1 Schedule Declaration

A schedule MUST be declarative and MAY include:

* time zone declaration
* calendar constraints
* recurrence rules
* exclusion rules

### 8.2 External Inputs

The concept of "current time" is an external input.

TimeTrigger evaluation MUST use explicit time inputs.

---

## 9. Event Trigger (Normative)

An EventTrigger declares that a Workflow may be started when events matching a pattern occur.

EventTrigger MUST:

* reference an event pattern
* declare how event data binds to workflow inputs (via target-independent Value Sources)

EventTrigger MUST NOT require any transport semantics.

---

## 10. Security and Authorization (Normative)

Triggers MAY be gated by authorization policies.

If a trigger requires authorization:

* actor identity MUST be an explicit input
* authorization decisions MUST be explainable and auditable

---

## 11. Determinism and Replay (Hard)

Trigger planning MUST be deterministic.

Trigger activation recording MUST retain sufficient provenance to:

* explain why a trigger fired
* support audit and debugging

Whether trigger activations are replayable depends on trigger kind and Semantics-declared rules.

---

## 12. Target Independence (Hard)

This specification MUST NOT define:

* specific cron syntax
* specific scheduler implementations
* specific webhooks or endpoints
* user interface mechanisms

Targets may realize triggers using target-appropriate mechanisms, provided trigger meaning and constraints are preserved.
