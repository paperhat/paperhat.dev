Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Refund Policies and Refund Reckoning Specification

This specification defines Paperhat’s target-independent semantics for:

* refund policies as declarative data
* deterministic refund reckoning (refund amounts, fees, eligibility windows)
* auditable traces for refund decisions

This document is part of the reckoning domain slice: it specifies how refund policies produce refund adjustments and refund positions.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define payment provider APIs, return logistics, shipping labels, fraud systems, or a particular ledger implementation.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* make refund rules explicit, portable, and deterministic
* separate refund entity facts (what occurred) from refund computation (what is owed)
* ensure refund decisions are auditable and reproducible

---

## 2. Scope

This specification governs:

* refund policy identity and applicability
* eligibility (return windows, conditions)
* fees and adjustments (restocking fees, non-refundable portions)
* allocation of refund amounts across line items and instruments
* trace and recordability requirements

This specification does **not** govern:

* commerce entity schemas beyond references
* state machines for returns workflows
* payment settlement mechanics
* persistence of balances

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Stored Value Application](../stored-value-application/)
* [Promotions, Eligibility, and Stacking](../promotions-eligibility-and-stacking/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)

---

## 4. Core Invariants (Hard)

1. **Policies are data.** Refund policies MUST be representable as declarative data.
2. **Deterministic refund reckoning.** Refund results MUST be deterministic given explicit inputs.
3. **Stable identities.** Refund policies and refund outcomes MUST have stable identities.
4. **Auditable decisions.** Refund eligibility and computed amounts MUST be traceable in a refund trace.
5. **Target independence.** Semantics MUST NOT assume a particular returns system or payment provider.

---

## 5. Definitions (Normative)

### 5.1 Return Facts

**ReturnFacts** are the explicit inputs describing what is being returned, such as:

* order reference
* items/quantities
* timestamps
* condition/reason intents

ReturnFacts MUST be treated as explicit inputs.

---

### 5.2 Refund Policy

A **RefundPolicy** is declarative data defining:

* eligibility rules
* refund amount rules
* fee rules
* method constraints (where applicable)

---

### 5.3 Eligibility Window

An **EligibilityWindow** constrains refunds by time.

If time is used, it MUST be treated as an explicit external input.

---

### 5.4 Refund Adjustment

A **RefundAdjustment** is a structured contribution that changes the refund amount, such as:

* restocking fee
* non-refundable portion
* condition-based deduction

Refund adjustments MUST be auditable and attributable.

---

### 5.5 Refund Position

A **RefundPosition** is a computed output describing what is owed back, including:

* total refund amount
* allocations to line items
* allocations to instruments (payment method vs stored value)
* any remaining balance due or non-refundable remainder

---

### 5.6 Refund Trace

A **RefundTrace** is a structured record explaining:

* which policies were considered
* eligibility outcomes
* fees and deductions applied
* final allocations

---

## 6. Eligibility Semantics (Normative)

Pipeline MUST be able to evaluate refund eligibility deterministically using explicit inputs.

Eligibility SHOULD support rules such as:

* within a return window
* allowed reasons/conditions
* product/category exclusions

Eligibility failures MUST be explainable via structured reasons.

---

## 7. Refund Amount Semantics (Normative)

Refund computation MUST be representable as deterministic transformation from:

* order/line item facts
* return facts
* refund policy parameters

Refund policies MUST be able to express:

* full refund
* partial refund
* fee-based deductions
* caps and minimums

---

## 8. Allocation and Instrument Ordering (Normative)

If refunds must be allocated across line items or instruments, allocation MUST be:

* deterministic
* representable as data
* recorded in the RefundTrace

If refunds are constrained by instrument ordering (for example, refund original payment method before store credit), the ordering MUST be explicit and deterministic.

---

## 9. Trace and Recordability (Normative)

A conforming system SHOULD record:

* return facts reference identities
* policies considered and applied
* eligibility outcomes
* computed refund amounts and allocations

Refund records SHOULD compose with provenance/lineage.

---

## 10. Validation Requirements (Normative)

Pipeline MUST be able to validate:

* refund policies are well-formed
* policy references are valid
* time-dependent windows declare time as an external input
* refund outputs conform to declared rounding/precision policies

---

## 11. Target Independence (Hard)

This specification MUST NOT define:

* provider refund APIs
* shipping/returns logistics
* database schemas
* a concrete rule expression language

Targets may implement refund flows using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
