Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Promotions, Eligibility, and Stacking Specification

This specification defines Paperhat’s target-independent semantics for:

* promotions and other pricing programs as declarative policy data
* eligibility determination
* stacking and composition rules
* deterministic application and auditable traces

This document is **part of the reckoning domain slice**: it specifies how policies produce adjustments and how multiple policies compose.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define a policy UI, provider integrations, databases, query languages, or an expression language.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model promotions and pricing programs as data
* define deterministic eligibility and application semantics
* define stacking/composition semantics that are auditable
* keep policy meaning independent of any target implementation

---

## 2. Scope

This specification governs:

* promotion/program identity
* eligibility predicates and applicability scopes
* stacking rules (exclusive, priority, compatibility)
* deterministic selection and application
* trace requirements for explainability

This specification does **not** govern:

* commerce entity schemas (products, orders) beyond references
* payment processing
* persistence and query mechanisms
* scheduling or lifecycle state machines

---

## 3. Related Specifications

This specification is designed to compose with:

* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Hard)

1. **Policies are data.** Promotions and pricing programs MUST be representable as declarative data.
2. **Deterministic evaluation.** Eligibility and stacking decisions MUST be deterministic given explicit inputs.
3. **Stable identities.** Policies MUST have stable, IRI-like identities.
4. **Auditable application.** Applied and rejected policies MUST be explainable via trace records.
5. **Target independence.** Kernel MUST NOT assume any particular rule engine or datastore.

---

## 5. Definitions (Normative)

### 5.1 Promotion / Program

A **Promotion** (or **Program**) is a Policy that may produce one or more **Adjustments** when applicable.

This specification uses “promotion” and “program” interchangeably for policy entities that affect amounts.

---

### 5.2 Eligibility Predicate

An **EligibilityPredicate** is a declarative condition evaluated over explicit inputs that determines whether a policy is eligible.

Eligibility predicates MAY reference:

* entity properties (via references)
* external inputs (for example, time)
* declared attributes (segments, classifications)

Eligibility predicates MUST be deterministic.

---

### 5.3 Applicability Scope

An **ApplicabilityScope** describes what a policy applies to, such as:

* an entire order/cart
* a subset of line items
* a specific product/variant
* a customer segment

Scope MUST be representable as data and MUST be evaluable deterministically.

---

### 5.4 Stacking

**Stacking** is the rule system describing how multiple eligible policies combine.

Stacking MUST support, at minimum:

* **Exclusivity**: only one policy in a set may apply
* **Priority**: deterministic ordering across policies
* **Compatibility**: allow/deny specific combinations

---

### 5.5 Application

**Application** is the process of selecting a set of eligible policies and producing adjustments.

Application MUST produce:

* a set of AppliedPolicies
* a set of RejectedPolicies (with reasons)
* a set of Adjustments

---

## 6. Eligibility Semantics (Normative)

A conforming system MUST define eligibility evaluation such that:

* the evaluation inputs are explicit
* the eligibility outcome is reproducible
* failed predicates can be reported as structured reasons

Eligibility MUST be evaluated prior to stacking resolution.

---

## 7. Stacking Resolution (Normative)

Given a set of eligible policies, stacking resolution MUST:

* deterministically select a set of policies to apply
* record the ordering and the decisions
* produce reasons for rejections due to stacking

If priorities are used, tie-breaking MUST be deterministic.

---

## 8. Adjustment Production (Normative)

Applied policies MUST produce adjustments as structured data.

Adjustments MUST:

* reference the producing policy identity
* include scope and allocation intent (when applicable)
* be compatible with reckoning trace requirements

---

## 9. Trace Requirements (Normative)

A conforming system SHOULD emit trace records sufficient to explain:

* which policies were considered
* eligibility outcomes
* stacking decisions
* the final set of applied policies
* the adjustments produced

Trace records SHOULD compose with provenance/lineage.

---

## 10. Validation Requirements (Normative)

Kernel MUST be able to validate that:

* policy identities are well-formed and unique
* eligibility predicates reference valid inputs
* stacking policies are well-formed
* adjustment kinds and scopes are consistent

---

## 11. Determinism and External Inputs (Normative)

If time influences eligibility or applicability, time MUST be treated as an explicit external input.

All ordering-dependent behavior MUST have deterministic tie-breaking.

---

## 12. Target Independence (Hard)

This specification MUST NOT define:

* a concrete predicate language
* a rule engine
* a database or query language
* provider-specific promotion constructs

Targets may implement eligibility and stacking using any appropriate mechanisms, provided semantic meaning, determinism, and traceability are preserved.
