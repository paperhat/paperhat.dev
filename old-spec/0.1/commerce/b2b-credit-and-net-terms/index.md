Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat B2B Credit and Net Terms Specification

This specification defines Paperhat’s target-independent semantics for **B2B credit** and **net terms** decisions, including:

* credit limits and available credit as explicit inputs
* deterministic evaluation of credit positions
* credit holds and enforcement outcomes
* auditable traces for credit decisions

This document is part of the reckoning domain slice.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define invoicing systems, collections processes, legal terms, payment gateways, or persistence engines.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model credit decisions as declarative policy + deterministic evaluation
* keep credit/terms semantics portable across targets
* ensure credit enforcement outcomes are auditable and reproducible

---

## 2. Scope

This specification governs:

* credit position evaluation for a buyer account
* net terms eligibility and enforcement intents
* credit holds and decision outcomes
* trace and recordability requirements

This specification does **not** govern:

* invoice generation
* payment settlement and reconciliation
* customer risk scoring implementations
* persistence of balances or accounts

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Promotions, Eligibility, and Stacking](../promotions-eligibility-and-stacking/)
* [Data Validation and Shape Constraints](../../validation/data-validation-and-shape-constraints/)
* [Provenance and Lineage](../../data/provenance-and-lineage/)

---

## 4. Core Invariants (Normative)

1. **Explicit inputs.** Credit limits, balances, and obligations used in evaluation MUST be explicit inputs.
2. **Deterministic decisions.** Credit decisions MUST be deterministic given explicit inputs.
3. **Declarative policies.** Net terms and hold policies MUST be representable as data.
4. **Auditable outcomes.** Enforcement decisions MUST be traceable.
5. **Target independence.** The Kernel MUST NOT assume any ERP, invoicing, or payments provider.

---

## 5. Definitions (Normative)

### 5.1 Account

An **Account** is an identity representing the buyer party subject to credit evaluation.

---

### 5.2 Credit Limit

A **CreditLimit** is an explicit input describing the maximum credit exposure permitted.

---

### 5.3 Credit Exposure

**CreditExposure** is an explicit input describing outstanding obligations that count against credit.

This may include:

* unpaid invoices
* authorized but not captured amounts (if modeled)
* open orders on terms

The definition of what contributes to exposure MUST be explicit and policy-defined.

---

### 5.4 Available Credit

**AvailableCredit** is a derived position computed from explicit inputs.

---

### 5.5 Net Terms

**NetTerms** is a policy describing deferred payment conditions (e.g., “pay within N days”).

This specification treats the exact legal meaning as out of scope; it models the decision intent and enforcement outcomes.

---

### 5.6 Credit Hold

A **CreditHold** is an enforcement outcome that restricts actions until credit conditions are satisfied.

---

## 6. Credit Evaluation Semantics (Normative)

The Kernel MUST be able to evaluate credit position deterministically from explicit inputs, including:

* CreditLimit
* CreditExposure inputs
* pending obligation intent (e.g., a new order total)
* applicable credit policies

The evaluation MUST produce a structured outcome indicating whether credit conditions are satisfied.

---

## 7. Net Terms Eligibility and Enforcement (Normative)

A conforming system MUST represent net terms eligibility as declarative policy.

If net terms are requested for an obligation, the Kernel MUST be able to produce a decision outcome such as:

* Approved
* ApprovedWithHold
* Denied

Reasons MUST be representable as structured data.

---

## 8. Holds and Decision Outcomes (Normative)

Credit holds MUST be representable as explicit outcomes, including:

* hold identity
* reason
* scope (order-level, account-level)

Holds MUST be auditable.

---

## 9. Trace and Recordability (Normative)

A conforming system SHOULD record:

* inputs used for evaluation (by reference)
* policies considered and applied
* decision outcomes and reasons
* holds created and their scope

Trace records SHOULD compose with provenance/lineage.

---

## 10. Validation Requirements (Normative)

The Kernel MUST be able to validate:

* required inputs are declared
* policies are well-formed
* decisions and holds are representable as data

---

## 11. Target Independence (Normative)

This specification MUST NOT define:

* ERP integrations
* invoice schemas
* collections workflows
* payment provider protocols

Targets may implement credit workflows using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
