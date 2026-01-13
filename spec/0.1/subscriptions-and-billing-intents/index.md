Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Subscriptions and Billing Intents Specification

This specification defines Paperhat’s target-independent semantics for **subscriptions** as declarative entities and **billing intents** as deterministic, auditable reckoning inputs/outputs.

This document governs semantic meaning, determinism, and validation requirements.
It does **not** define payment provider APIs, invoicing platforms, dunning workflows, or persistence engines.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* represent subscriptions as stable entities
* represent billing as explicit intents evaluated deterministically
* separate subscription facts (what exists) from billing execution (target concern)
* enable auditable billing decisions

---

## 2. Scope

This specification governs:

* subscription identity and plan/term data
* billing cadence and cycle boundaries (as data)
* billing intents (what should be charged, when, and for what scope)
* proration intent and cancellation intent (semantic)
* recordability of billing decisions

This specification does **not** govern:

* provider implementations
* settlement and reconciliation
* invoice templates
* collection workflows

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Idempotency and De-duplication](../idempotency-and-deduplication/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)

---

## 4. Core Invariants (Hard)

1. **Subscriptions are data.** Subscription agreements MUST be representable as declarative entities.
2. **Billing is explicit.** Billing decisions MUST be represented as explicit billing intents.
3. **Deterministic evaluation.** Billing intent computation MUST be deterministic given explicit inputs.
4. **Auditable decisions.** Cycle boundaries, proration, and cancellation effects MUST be traceable.
5. **Target independence.** Kernel MUST NOT assume a specific provider billing model.

---

## 5. Definitions (Normative)

### 5.1 Subscription

A **Subscription** is an entity representing an ongoing agreement to provide items/services on a schedule.

A Subscription MUST have:

* a stable identity
* a plan/offer reference
* a billing cadence definition
* an effective time interval (start; optional end)

---

### 5.2 Billing Cadence

A **BillingCadence** is declarative data describing the recurrence schedule.

This specification does not define a concrete calendar DSL.

---

### 5.3 Billing Cycle

A **BillingCycle** is a computed period boundary for a subscription, derived deterministically from:

* subscription start
* cadence
* explicit time input

---

### 5.4 Billing Intent

A **BillingIntent** is a declarative output describing:

* what amount should be charged
* for which period/cycle
* for which subscription scope
* optional proration components

A BillingIntent is not a provider request; it is semantic intent.

---

### 5.5 Proration Intent

A **ProrationIntent** describes how partial-period changes affect charges.

Proration MUST be deterministic and auditable.

---

### 5.6 Cancellation Intent

A **CancellationIntent** describes end-of-term or immediate cancellation semantics.

This specification does not define workflow execution; it defines the intended effect on billing intents.

---

## 6. Billing Intent Computation (Normative)

Kernel MUST be able to compute billing intents deterministically from explicit inputs, including:

* subscription facts
* plan pricing facts
* external inputs (time)
* declared proration policies (if applicable)

---

## 7. Idempotency and De-duplication (Normative)

Billing intents SHOULD be idempotent with respect to a cycle identity.

A conforming system SHOULD be able to derive an IdempotencyIdentity for billing intents from:

* subscription identity
* cycle identity
* intent kind

---

## 8. Trace and Recordability (Normative)

A conforming system SHOULD record:

* cycle boundaries used
* computed billing intents
* proration/cancellation decisions

Records SHOULD compose with provenance/lineage.

---

## 9. Validation Requirements (Normative)

Kernel MUST be able to validate:

* subscription data is well-formed
* cadence definitions are well-formed
* time is treated as explicit external input

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* provider subscription APIs
* invoice formats
* dunning workflows
* database schemas

Targets may implement subscription billing with any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
