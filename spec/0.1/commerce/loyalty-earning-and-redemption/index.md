Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Loyalty Earning and Redemption Specification

This specification defines Paperhat’s target-independent semantics for **loyalty programs** as declarative policies and deterministic reckoning, including:

* earning (points, credits, tier progression)
* redemption (conversion to value, applicability constraints)
* deterministic evaluation and audit traces

This document is part of the reckoning domain slice.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define a CRM system, provider APIs, storage engines, or a particular ledger implementation.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model loyalty programs as declarative data
* compute earned and redeemable value deterministically
* keep loyalty rules portable across targets
* ensure loyalty outcomes are auditable and reproducible

---

## 2. Scope

This specification governs:

* loyalty program identity and parameters
* earning rules and tier rules
* redemption rules and applicability scopes
* deterministic ordering and composition with other adjustments
* recordability and trace requirements

This specification does **not** govern:

* member account persistence
* anti-fraud
* marketing campaigns
* UI enrollment flows

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Promotions, Eligibility, and Stacking](../promotions-eligibility-and-stacking/)
* [Stored Value Application](../stored-value-application/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)

---

## 4. Core Invariants (Normative)

1. **Programs are data.** Loyalty programs and rules MUST be representable as declarative data.
2. **Deterministic reckoning.** Earning and redemption outcomes MUST be deterministic given explicit inputs.
3. **Stable identities.** Programs, rules, and resulting awards MUST have stable identities.
4. **Auditable outcomes.** Loyalty results MUST be explainable via traces.
5. **Target independence.** Kernel MUST NOT assume any particular loyalty platform.

---

## 5. Definitions (Normative)

### 5.1 Loyalty Program

A **LoyaltyProgram** is a set of declarative rules that define earning, tiers, and redemption.

---

### 5.2 Member Facts

**MemberFacts** are explicit inputs describing loyalty-related state, such as:

* member identity reference
* current point balance (as input)
* current tier/status (as input)

Persistence of member facts is out of scope.

---

### 5.3 Earning Rule

An **EarningRule** defines how value is earned.

Rules MAY be based on:

* purchase amounts
* item categories
* time windows
* member tier

---

### 5.4 Award

An **Award** is a computed outcome, such as:

* points earned
* tier progress
* bonus multipliers applied

---

### 5.5 Redemption Rule

A **RedemptionRule** defines:

* conversion from points to value
* applicability scope and exclusions
* caps, minimums, and step sizes

---

### 5.6 Loyalty Redemption Position

A **LoyaltyRedemptionPosition** is a computed output describing:

* points redeemed
* value applied
* remaining points (as a computed projection)

---

## 6. Earning Semantics (Normative)

Kernel MUST compute awards deterministically from:

* commerce facts (order/cart facts)
* member facts
* program rules
* explicit external inputs (time, if used)

If multiple earning rules apply, ordering and combination MUST be deterministic.

---

## 7. Tier Semantics (Normative)

A program MAY define tiers.

If tiers exist:

* tier determination MUST be deterministic
* tier progression outcomes MUST be auditable

---

## 8. Redemption Semantics (Normative)

Kernel MUST compute redemption outcomes deterministically from explicit inputs.

Redemption MUST support constraints sufficient to express:

* eligibility and exclusions
* caps and minimums
* conversion rates

Redemption results MUST be representable as structured data and MUST be auditable.

---

## 9. Interaction with Promotions and Stored Value (Normative)

If loyalty redemption is treated as stored value, its application MUST compose with stored value semantics.

If loyalty programs interact with promotions, the ordering MUST be explicit and deterministic.

---

## 10. Trace and Recordability (Normative)

A conforming system SHOULD record:

* programs/rules considered
* eligibility decisions
* awards computed
* redemption decisions and applied values
* ordering/composition decisions

Trace records SHOULD compose with provenance/lineage.

---

## 11. Validation Requirements (Normative)

Kernel MUST be able to validate:

* rules are well-formed
* rule references are valid
* time-dependent rules declare time as explicit input
* conversion rules are coherent (no negative redemption)

---

## 12. Target Independence (Normative)

This specification MUST NOT define:

* provider-specific loyalty platforms
* databases and schemas
* a concrete rule expression language

Targets may implement loyalty programs using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
