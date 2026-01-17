Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Reliability and Failure Semantics Specification

This specification defines Paperhat’s target-independent semantics for **reliability**, including failure classification, retry policy, backoff policy, timeouts, compensation, and dead-letter handling.

This document governs **meaning, constraints, and planning interfaces only**.
It does **not** define specific schedulers, timers, transports, protocol details, or deployment architecture.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define failures and reliability policy as declarative data
* enable resilient workflows without embedding runtime mechanisms in the Kernel
* support auditable and explainable failure handling
* preserve determinism of planning and the explicit modeling of external inputs

---

## 2. Scope

This specification governs:

* failure classification and error semantics
* retry and backoff policy meaning
* timeout semantics
* compensation semantics
* dead-letter semantics
* how reliability policy attaches to workflow steps and external action requests

This specification does **not** govern:

* concrete scheduling implementations
* concrete transport mechanisms
* concrete logging pipelines
* concrete storage engines

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Triggers and Scheduling](../triggers-and-scheduling/)
* [Integrations and Credentials](../integrations-and-credentials/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)

---

## 4. Core Invariants (Normative)

The following invariants are non-negotiable:

1. **Failures are modeled as data.**
2. **Policy is declarative.** No imperative retry loops in authored content.
3. **Planning is deterministic.** Given identical artifacts and inputs, the Kernel MUST emit the same reliability plan.
4. **External inputs are explicit.** Time and environment MUST NOT be implicit.
5. **Auditability.** It MUST be possible to explain and record why a retry, compensation, or dead-letter outcome occurred.

---

## 5. Definitions (Normative)

### 5.1 Failure

A **Failure** is a typed outcome that prevents a step from producing its intended result.

A Failure MUST include:

* a failure kind
* Help/diagnostics
* provenance (where applicable)

---

### 5.2 Failure Kinds

The Kernel MUST support failure kinds suitable for reliable systems.

At minimum:

* **TransientFailure** — expected to be resolvable by retry
* **PermanentFailure** — retry is not expected to succeed
* **PolicyFailure** — rejected due to policy/authorization/validation
* **TimeoutFailure** — failure due to exceeding a declared time constraint

---

### 5.3 Reliability Policy

A **ReliabilityPolicy** declares what to do on failures.

A policy MAY specify:

* retry policy
* backoff policy
* timeout policy
* compensation policy
* dead-letter policy

---

### 5.4 Retry Policy

A **RetryPolicy** is a declarative rule set that controls whether and how an operation may be retried.

A RetryPolicy MUST be expressed without embedding runtime loops.

---

### 5.5 Backoff Policy

A **BackoffPolicy** declares delays between retries.

Backoff depends on time, which is an external input.

---

### 5.6 Compensation

A **Compensation** is a declarative intent to mitigate effects when a step fails after partial progress.

Compensation MUST be modeled as intent (for example, as a Command request) and evaluated deterministically by the Kernel.

---

### 5.7 Dead-Letter Handling

A **DeadLetter** outcome represents a permanently halted attempt that is preserved for later inspection or handling.

Dead-letter handling MUST be auditable.

---

## 6. Attaching Reliability Policy (Normative)

ReliabilityPolicy MAY attach to:

* workflow steps
* external action requests
* triggers

If attached at multiple levels, the Kernel MUST define precedence and composition rules.

---

## 7. Timeout Semantics (Normative)

Timeout policy declares a maximum duration for a step.

The evaluation of timeouts depends on explicit time inputs.

Timeout policy MUST NOT embed scheduler implementations.

---

## 8. Retry Semantics (Normative)

RetryPolicy MUST declare:

* which failure kinds are eligible for retry
* maximum attempts
* stopping conditions

RetryPolicy MUST NOT embed protocol or transport details.

---

## 9. Backoff Semantics (Normative)

BackoffPolicy MUST declare:

* the delay strategy as declarative parameters
* any maximum delay constraints

BackoffPolicy MUST NOT embed wall-clock access.

Time is an explicit input.

---

## 10. Compensation Semantics (Normative)

Compensation MUST be expressed as declarative intent.

Compensation SHOULD be expressed using the Command vocabulary so it composes with auditing and idempotency.

---

## 11. Dead-Letter Semantics (Normative)

Dead-letter handling MUST declare:

* what is recorded
* what provenance is retained
* what follow-up actions are permitted

Storage and transport are realization details.

---

## 12. Target Independence (Normative)

This specification MUST NOT define:

* specific retry implementations
* specific backoff algorithms as code
* specific job queue implementations
* specific logging systems

Targets may realize reliability policy using target-appropriate mechanisms, provided semantic meaning and constraints are preserved.
