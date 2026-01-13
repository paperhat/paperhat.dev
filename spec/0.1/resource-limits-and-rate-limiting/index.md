Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Resource Limits and Rate Limiting Specification

This specification defines Paperhat’s target-independent semantics for **resource limits** and **rate limiting**.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete schedulers, job runners, quota systems, network throttling, or vendor-specific mechanisms.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to declare bounded resource use
* prevent uncontrolled fan-out and runaway execution
* enable targets to enforce limits consistently
* preserve determinism of planning while acknowledging that enforcement occurs at runtime

---

## 2. Scope

This specification governs:

* resource limit declarations
* rate limit declarations
* concurrency limits (as they relate to resource governance)
* limit scopes and identities
* exhaustion outcomes and required recordability

This specification does **not** govern:

* runtime enforcement implementations
* vendor-specific quota systems
* networking details
* scheduler details

---

## 3. Related Specifications

This specification is designed to compose with:

* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Integrations and Credentials](../integrations-and-credentials/)

---

## 4. Core Invariants (Hard)

1. **Limits are declarative.** Limits MUST be expressible as data.
2. **No implementation leakage.** Limits MUST NOT specify how a target enforces them.
3. **Deterministic planning.** Kernel MUST be able to plan with declared limits deterministically.
4. **Observable enforcement.** Limit exhaustion MUST be representable and recordable.

---

## 5. Definitions (Normative)

### 5.1 Limit Scope

A **LimitScope** identifies the semantic boundary within which a limit applies.

Examples include:

* per-run
* per-workflow
* per-step
* per-integration operation
* per-tenant (if tenancy is part of the semantic model)

The meaning of a scope is semantic; it does not imply a specific storage or runtime boundary.

---

### 5.2 Resource Limit

A **ResourceLimit** declares a maximum allowed use of a resource within a LimitScope.

This specification does not mandate a specific set of resources, but targets MUST be able to interpret declared limits.

---

### 5.3 Rate Limit

A **RateLimit** declares a maximum allowed rate of operations within a LimitScope.

A rate limit depends on time; time is an external input and MUST NOT be implicit.

---

### 5.4 Limit Exhaustion

**LimitExhaustion** is an outcome where evaluation cannot proceed due to a declared limit.

LimitExhaustion MUST be expressible as a typed failure outcome.

---

## 6. Declaring Limits (Normative)

Limits MAY attach to:

* workflows
* steps
* integration operations
* triggers

If attached at multiple levels, Kernel MUST define precedence and composition.

---

## 7. Interactions With Concurrency (Normative)

Concurrency limits and resource/rate limits MUST compose.

A plan MUST be able to explain:

* why a step was blocked due to limits
* what limit applied
* what scope identity was used

---

## 8. Interactions With Reliability (Normative)

If a step is blocked due to limits:

* reliability policy MAY define whether to retry later
* any retry delay MUST be expressed via declarative backoff semantics

A plan MUST be able to preserve auditability of limit-related decisions.

---

## 9. Recordability Requirements (Normative)

Run logs MUST be able to record:

* the identity of the applied limit
* the evaluated scope identity
* the exhaustion outcome
* any retry/deferral decisions caused by exhaustion

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* specific quota APIs
* specific rate limiting algorithms
* specific clock sources

Targets may implement enforcement using any appropriate mechanism, provided semantic meaning and required recordability are preserved.
