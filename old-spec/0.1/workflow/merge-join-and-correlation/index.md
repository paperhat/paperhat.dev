Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Merge, Join, and Correlation Specification

This specification defines Paperhat’s target-independent semantics for **merge**, **join**, **fan-in**, and **correlation** within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define transport mechanisms, streaming systems, database joins, or concrete runtime implementations.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* express fan-in and join semantics declaratively
* enable deterministic planning of dependencies and coordination
* allow workflows to correlate multiple signals to a single joined outcome
* preserve auditability of merge and join decisions

---

## 2. Scope

This specification governs:

* merge and join constructs
* correlation keys and correlation groups
* join modes (all/any/quorum)
* time windows and time-based joins (as explicit external inputs)
* missing/late data behavior
* recordability requirements

This specification does **not** govern:

* transport- or protocol-level correlation
* concrete storage engines
* query languages

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Looping and Batching](../looping-and-batching/)
* [Conditions and Branching](../conditions-and-branching/)
* [Eventing and Event Sourcing](../../events/eventing-and-event-sourcing/)
* [Run Logs and Observability](../../operations/run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Joins are declarative.** Join requirements MUST be representable as data.
2. **Deterministic planning.** The Kernel MUST be able to plan join structure deterministically.
3. **Explicit correlation.** Correlation MUST be defined via declared keys and sources.
4. **Time is explicit.** Time windowing depends on time inputs that MUST be explicit execution facts.
5. **Auditability.** It MUST be possible to explain why a join completed (or did not).

---

## 5. Definitions (Normative)

### 5.1 Correlation Key

A **CorrelationKey** is a declarative definition of how multiple items/attempts/events are grouped.

A CorrelationKey MUST declare:

* key identity
* key derivation inputs (via value sourcing)
* key type expectation

---

### 5.2 Correlation Group

A **CorrelationGroup** is the set of items that share the same CorrelationKey value.

---

### 5.3 Join

A **Join** is a coordination construct that waits for required upstream signals within a CorrelationGroup.

A Join MUST declare:

* what upstream signals are considered
* join mode
* behavior on missing/late signals

---

### 5.4 Merge

A **Merge** is a construct that combines multiple values into a single value.

A Merge MUST declare:

* merge identity
* merge inputs
* merge output type expectation
* merge conflict policy (when applicable)

---

### 5.5 Join Modes

Join modes MUST include at minimum:

* **AllOf** — complete only when all required signals are present
* **AnyOf** — complete when any required signal is present

Join modes MAY include quorum-style completion.

---

### 5.6 Time Window

A **TimeWindow** constrains which signals are eligible to participate in a join.

TimeWindow evaluation depends on time facts that MUST be explicit.

---

## 6. Correlation Semantics (Normative)

Correlation keys MUST be derived from declared value sources.

Correlation MUST NOT depend on implicit transport-specific metadata.

---

## 7. Join Completion Semantics (Normative)

Join completion MUST be defined in terms of:

* required signals
* join mode
* any declared windowing constraints

A Join MUST define behavior for:

* missing signals
* late-arriving signals
* duplicate signals

---

## 8. Merge Semantics (Normative)

Merge MUST define:

* merge ordering policy (if order matters)
* conflict policy (if conflicts are possible)

Merge MUST be declarative and MUST NOT embed target code.

---

## 9. Failure and Pending (Normative)

Join evaluation MAY be Pending while awaiting signals.

Failure MUST be used when:

* required inputs are invalid
* correlation key derivation fails
* join policy rejects the observed signals

---

## 10. Recordability (Normative)

Run logs MUST be able to record:

* join identity
* correlation key identity and derived key value (as permitted data)
* which signals were observed
* join completion decision and reason
* merge identity and merge outcome

Records MUST NOT require embedding secrets.

---

## 11. Target Independence (Normative)

This specification MUST NOT define:

* message brokers
* streaming systems
* SQL joins
* runtime event loops

Targets may realize joins and merges using any appropriate mechanism, provided semantic meaning and recordability requirements are preserved.
