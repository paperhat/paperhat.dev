Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Reckoning and Price Transformations Specification

This specification defines Paperhat’s target-independent semantics for **reckoning**: deterministic calculation of amounts owed and derived positions (final prices, adjustments, refunds, credits, and rewards) from declared entities and declared policies.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define payment processors, tax vendors, database schemas, currency tables, or a particular expression language.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model price transformation as pure, deterministic computation
* separate commerce entities (what exists) from reckoning (how values change)
* ensure every derived amount is auditable and reproducible
* keep policy authoring declarative and target-independent

---

## 2. Scope

This specification governs:

* transformation pipelines that compute derived monetary results
* adjustment semantics (discounts, fees, credits, rewards)
* eligibility and application policies as declarative data
* composition/stacking semantics
* recordability and audit traces of calculations

This specification does **not** govern:

* fulfillment, inventory, or order lifecycle
* payment authorization/settlement
* jurisdictional tax computation details
* fraud, risk scoring, or identity verification

---

## 3. Related Specifications

This specification is designed to compose with:

* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Idempotency and De-duplication](../idempotency-and-deduplication/)

---

## 4. Core Invariants (Hard)

1. **Pure transformations.** Each price transformation MUST be a pure function of explicit inputs.
2. **Deterministic results.** Given identical inputs, the same outputs MUST be produced.
3. **Declarative policies.** Eligibility, stacking, and application policies MUST be expressed as data.
4. **Auditable computation.** Every derived amount MUST be traceable to its inputs and applied policies.
5. **Target independence.** Kernel MUST NOT assume payment processors, databases, or vendor calculators.

---

## 5. Definitions (Normative)

### 5.1 Reckoning

**Reckoning** is the deterministic computation of one or more **Positions** from:

* a set of **Entities** (inputs)
* a set of **Policies** (declared rules)
* explicit external inputs (for example, time)

---

### 5.2 Entity

An **Entity** is a declared thing that exists (for example, a cart, an order, a return, a customer segment membership, or a stored-value balance).

This specification does not define the full commerce entity model.

---

### 5.3 Policy

A **Policy** is declarative data describing how to compute or adjust values.

A policy MAY include:

* eligibility predicates
* applicability scopes
* stacking/composition rules
* parameter values

---

### 5.4 Adjustment

An **Adjustment** is a contribution that changes a base amount.

Adjustments MUST be representable as structured data, including:

* adjustment identity
* kind (discount, fee, credit, reward, tax-intent, other)
* signed amount or amount intent
* application scope (what it applies to)

---

### 5.5 Position

A **Position** is a computed state derived by reckoning.

Positions MAY include:

* final amount owed
* refund amount
* applied credit / remaining credit
* rewards earned / rewards redeemed
* line-item totals and allocations

---

### 5.6 Reckoning Trace

A **ReckoningTrace** is a structured record explaining how outputs were computed.

A trace MUST be sufficient to:

* identify policies evaluated and applied
* identify adjustments produced
* link adjustments to the entity scope they affected
* support reproducibility under explicit inputs

---

## 6. Policy Composition and Stacking (Normative)

Reckoning MUST support composition of multiple applicable policies.

A conforming system MUST define stacking semantics sufficient to express:

* exclusivity (only one policy in a set may apply)
* priority ordering
* compatibility constraints (which policies may co-apply)

Stacking MUST be deterministic and MUST be auditable in the ReckoningTrace.

---

## 7. Allocation and Attribution (Normative)

When an adjustment affects a composite amount (for example, an order total), the system MUST define how the adjustment is allocated and attributed.

Allocation MUST be:

* deterministic
* representable as data
* recorded in the ReckoningTrace

---

## 8. Stored Value Semantics (Normative)

A conforming system MAY include stored value concepts (gift cards, store credit, loyalty value).

If stored value is applied:

* the applied amount and remaining value MUST be represented explicitly
* application MUST be deterministic and auditable

This specification does not define the persistence of balances.

---

## 9. Refund Semantics (Normative)

Refund computation MUST be representable as reckoning over explicit inputs:

* return entities
* refund policies (windows, fees, condition-based adjustments)
* external inputs (for example, time)

Refund results MUST be auditable.

---

## 10. Credit Position Semantics (Normative)

If credit management exists, reckoning MUST be able to compute:

* available credit
* holds and enforcement outcomes
* net terms-related decisions

These computations MUST be deterministic and auditable.

---

## 11. Validation and Safety (Normative)

Kernel MUST validate that:

* all required inputs are declared
* policies are well-formed and reference valid entities
* stacking rules are consistent
* all produced monetary outputs conform to declared rounding/precision policies (if present)

---

## 12. Recordability and Provenance (Normative)

Systems SHOULD be able to emit a ReckoningTrace that composes with provenance/lineage:

* outputs reference the policies and entities that produced them
* intermediate derivations may be represented as lineage steps

Records MUST avoid secret material.

---

## 13. Target Independence (Hard)

This specification MUST NOT define:

* payment flows
* vendor tax engines
* database tables
* a concrete policy expression language

Targets may implement reckoning using any appropriate mechanisms, provided purity, determinism, and auditability are preserved.
