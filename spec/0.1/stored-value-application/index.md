Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Stored Value Application Specification

This specification defines Paperhat’s target-independent semantics for applying **stored value** during reckoning, including gift cards, store credit, and loyalty value.

This document is part of the reckoning domain slice: it defines how stored value contributes adjustments and positions.

This document governs semantic meaning, determinism, and recordability requirements.
It does **not** define balance persistence, provider integrations, payment gateways, or a particular ledger implementation.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model stored value instruments as inputs to deterministic reckoning
* define application strategies and constraints
* ensure application decisions are auditable and reproducible

---

## 2. Scope

This specification governs:

* stored value instrument references and available value inputs
* application intents (how much to apply, where to apply)
* ordering rules (which instruments apply first)
* partial application and remaining balance semantics
* recordability and trace requirements

This specification does **not** govern:

* how balances are stored or synchronized
* fraud detection
* payment authorization/capture
* fulfillment or return workflows

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Promotions, Eligibility, and Stacking](../promotions-eligibility-and-stacking/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)

---

## 4. Core Invariants (Normative)

1. **Deterministic application.** Stored value application MUST be deterministic given explicit inputs.
2. **No hidden state.** Balance availability used for application MUST be treated as explicit input.
3. **Auditable outcomes.** Applied amounts and remaining balances MUST be traceable in a reckoning trace.
4. **Target independence.** Kernel MUST NOT assume any ledger, provider, or persistence technology.

---

## 5. Definitions (Normative)

### 5.1 Stored Value Instrument

A **StoredValueInstrument** is an identified source of value that may be applied toward an obligation.

Examples include gift cards, store credit, and loyalty redemption value.

---

### 5.2 Available Value

**AvailableValue** is the amount of stored value available for application at evaluation time.

AvailableValue MUST be provided as explicit input.

---

### 5.3 Application Intent

An **ApplicationIntent** is declarative data that describes how stored value should be applied.

At minimum it MUST express:

* which instrument(s) are eligible
* the maximum amount to apply (optional)
* an ordering strategy (when multiple instruments exist)
* application scope (order total vs specific line items)

---

### 5.4 Application Result

An **ApplicationResult** is the deterministic outcome of applying stored value.

It MUST express:

* applied amounts (by instrument)
* remaining balances (by instrument)
* any unapplied obligation remainder

---

## 6. Application Strategies (Normative)

A conforming system MUST support strategies sufficient to express:

* apply up to available value
* apply up to a declared cap
* apply instruments in deterministic order

If multiple instruments apply, ordering MUST be deterministic, and tie-breaking MUST be defined.

---

## 7. Constraints and Eligibility (Normative)

Stored value application MAY be subject to declarative constraints such as:

* instrument eligibility scopes
* minimum/maximum redemption limits
* exclusions for specific items or categories

These constraints MUST be representable as data and evaluable deterministically.

---

## 8. Interaction with Promotions and Other Adjustments (Normative)

If stored value application interacts with other adjustments, the system MUST define an explicit ordering policy for:

* promotions/discount adjustments
* fees
* stored value application

This ordering policy MUST be deterministic and recorded in the trace.

---

## 9. Trace and Recordability (Normative)

A conforming system SHOULD record:

* the instruments considered
* the available value inputs used
* the application ordering policy
* applied and remaining amounts
* reasons for non-application (ineligible, insufficient available value, excluded scope)

These records SHOULD compose with provenance/lineage.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* balance persistence models
* ledger schemas
* payment provider APIs
* wallet implementations

Targets may implement stored value application using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
