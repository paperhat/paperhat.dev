Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Concurrency and Parallelism Specification

This specification defines Paperhat’s target-independent semantics for **concurrency**, **parallelism**, and **coordination** within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete runtimes, thread models, task executors, queues, or deployment architecture.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to express safe parallel evaluation where possible
* provide deterministic planning for concurrency
* constrain coordination semantics so that targets can implement them consistently
* support auditability of ordering, gating, and concurrency decisions

---

## 2. Scope

This specification governs:

* concurrency declarations (what may run concurrently)
* parallel groups and barriers
* ordering constraints (happens-before, must-follow)
* mutual exclusion semantics (locks and guard scopes)
* bounded concurrency (limits)
* idempotency and side-effect constraints as they relate to parallel execution

This specification does **not** govern:

* concrete worker pools
* runtime scheduling algorithms
* specific locking services
* transport-level ordering

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [State, Commands, and Continuations](../state-commands-and-continuations/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)

---

## 4. Core Invariants (Normative)

1. **Planning is deterministic.** Concurrency decisions emitted by Kernel MUST be reproducible given identical artifacts and inputs.
2. **Side effects are explicit.** Steps with side effects MUST be modeled such that ordering and retry semantics remain auditable.
3. **No implicit shared memory.** Kernel MUST NOT assume a shared-memory execution model.
4. **Coordination is declarative.** Concurrency control MUST be expressed as data.

---

## 5. Definitions (Normative)

### 5.1 Concurrency

**Concurrency** is the ability for multiple step evaluations to be in-progress without requiring a specific runtime model.

---

### 5.2 Parallelism

**Parallelism** is concurrency where steps may be evaluated simultaneously.

Kernel does not require that a target evaluates steps in parallel; it requires that parallelism may be planned and preserved where supported.

---

### 5.3 Ordering Constraint

An **OrderingConstraint** is a declarative statement that one step (or group) MUST be evaluated before another.

---

### 5.4 Parallel Group

A **ParallelGroup** is a declarative grouping of steps that MAY be evaluated concurrently.

A ParallelGroup MAY specify:

* a bounded concurrency limit
* a barrier requirement

---

### 5.5 Barrier

A **Barrier** is a coordination point where evaluation MUST wait until all required upstream steps have reached an outcome.

---

### 5.6 Mutual Exclusion

**MutualExclusion** is a declarative intent that a set of steps MUST NOT be evaluated concurrently with one another for a shared scope.

MutualExclusion is target-independent and does not imply a concrete locking implementation.

---

## 6. Concurrency Declarations (Normative)

Workflows MAY declare concurrency using parallel groups.

If parallel groups are declared, Kernel MUST be able to:

* determine which steps are eligible to run concurrently
* determine which steps are blocked by ordering constraints or barriers
* produce a plan that preserves declared constraints

---

## 7. Ordering Constraints (Normative)

Kernel MUST support ordering constraints sufficient to express:

* strict ordering between two steps
* group-level ordering (a group must complete before another begins)

Ordering constraints MUST be expressed without referencing runtime primitives.

---

## 8. Barriers (Normative)

A barrier MAY be declared:

* at the end of a parallel group
* as a separate coordination step

Barrier completion MUST be defined in terms of upstream outcomes.

---

## 9. Bounded Concurrency (Normative)

A ParallelGroup MAY declare a concurrency limit.

A concurrency limit:

* MUST be expressed as declarative data
* MUST NOT imply a specific worker pool size

---

## 10. Mutual Exclusion (Normative)

Mutual exclusion MAY be declared for a named semantic scope.

A mutual exclusion declaration MUST:

* identify the semantic scope being guarded
* describe what operations it applies to (for example, specific steps or step categories)

Targets may realize mutual exclusion using target-appropriate mechanisms.

---

## 11. Interaction With Reliability (Normative)

Retry and timeout behavior MUST respect ordering constraints, barriers, and mutual exclusion.

A plan MUST be able to explain:

* why a step was blocked
* why a step was eligible to proceed
* how a retry impacted ordering and coordination

---

## 12. Target Independence (Normative)

This specification MUST NOT define:

* thread usage
* async runtime APIs
* concrete lock services
* queue semantics

Targets may implement concurrency and coordination with any appropriate mechanism, provided the semantic constraints are preserved.
