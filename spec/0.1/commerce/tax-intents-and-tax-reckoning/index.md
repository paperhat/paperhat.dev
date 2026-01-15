Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Tax Intents and Tax Reckoning Specification

This specification defines Paperhat’s target-independent semantics for **tax computation as deterministic reckoning**, including:

* tax classification intents
* tax jurisdiction inputs
* tax calculation intents and results
* auditable traces for tax decisions

This document is part of the reckoning domain slice.

This document governs semantic meaning, determinism, and validation requirements.
It does **not** define vendor tax engines, jurisdiction databases, payment provider APIs, or a particular persistence model.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* represent tax rules and tax-relevant facts explicitly
* compute tax amounts deterministically from explicit inputs
* keep tax semantics portable across targets
* ensure tax outcomes are auditable and reproducible

---

## 2. Scope

This specification governs:

* tax classification intent for items and charges
* tax context inputs (address/jurisdiction facts, exemptions)
* tax calculation intent (what must be taxed and how)
* tax positions (tax lines, totals)
* trace and recordability requirements

This specification does **not** govern:

* jurisdictional rate tables and their sourcing
* regulatory compliance programs
* invoicing templates
* filing/remittance

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Promotions, Eligibility, and Stacking](../promotions-eligibility-and-stacking/)
* [Stored Value Application](../stored-value-application/)
* [Refund Policies and Refund Reckoning](../refund-policies-and-refund-reckoning/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)

---

## 4. Core Invariants (Normative)

1. **Explicit inputs.** Tax rates, jurisdiction facts, and exemption facts used for computation MUST be explicit inputs.
2. **Deterministic tax reckoning.** Given identical explicit inputs, tax outputs MUST be identical.
3. **Declarative classification.** Taxability MUST be expressible via declarative tax classification intents.
4. **Auditable outputs.** Tax lines and totals MUST be traceable to inputs and policies.
5. **Target independence.** Kernel MUST NOT require a specific vendor tax engine.

---

## 5. Definitions (Normative)

### 5.1 Tax Context

A **TaxContext** is the set of explicit inputs required to compute tax.

TaxContext MAY include:

* ship-to / bill-to jurisdiction facts
* buyer classification and exemption facts
* seller nexus/registration facts (as explicit inputs)
* time (if rate applicability depends on time; time is an explicit external input)

---

### 5.2 Tax Classification Intent

A **TaxClassificationIntent** is a declarative label or structured intent describing taxability characteristics of a line item or charge.

This specification does not define specific tax codes.

---

### 5.3 Tax Rate Inputs

**TaxRateInputs** are explicit inputs defining rate applicability and rate values.

This specification does not define the source of these inputs.

---

### 5.4 Tax Calculation Intent

A **TaxCalculationIntent** declares:

* the taxable base(s)
* the jurisdiction/context to use
* whether prices are tax-inclusive or tax-exclusive
* rounding/precision policies

---

### 5.5 Tax Position

A **TaxPosition** is a computed output describing tax amounts, such as:

* tax line amounts by jurisdiction/category
* total tax
* taxable base breakdown

---

### 5.6 Tax Trace

A **TaxTrace** is a structured record explaining:

* inputs used
* rules/rates applied
* allocation and rounding decisions

---

## 6. Tax Base and Taxability (Normative)

Kernel MUST be able to determine the taxable base deterministically from explicit inputs.

Taxability MUST be representable via tax classification intent and exemption facts.

---

## 7. Rounding and Precision (Normative)

Tax computation MUST have explicit rounding and precision policies.

Rounding MUST be deterministic and recorded in the trace.

---

## 8. Composition with Promotions, Fees, and Stored Value (Normative)

If promotions/adjustments affect taxable base, the ordering MUST be explicit and deterministic.

If stored value affects taxable base, the rule MUST be explicit.

These ordering rules MUST be auditable.

---

## 9. Refund Tax Semantics (Normative)

If refunds require tax reversal, refund tax computation MUST be deterministic and auditable, using explicit inputs.

---

## 10. Trace and Recordability (Normative)

A conforming system SHOULD record:

* tax context inputs (by reference)
* rates applied (by reference)
* tax classification intents used
* computed tax lines and totals

Tax records SHOULD compose with provenance/lineage.

---

## 11. Validation Requirements (Normative)

Kernel MUST be able to validate:

* required inputs are declared
* classification intents are well-formed
* rounding policies are explicit
* tax outputs conform to MoneyAmount constraints

---

## 12. Examples (Non-Normative)

### 12.1 Tax Exclusive Pricing

* Input facts include a taxable base of 100.00 (currency), a jurisdiction reference, and an applicable rate reference (e.g., 0.0825).
* The computed TaxPosition includes a tax line of 8.25 and a total tax of 8.25.
* The TaxTrace records the rate identity used, the rounding policy reference, and the resulting rounding decision (if any).

### 12.2 Tax Inclusive Pricing

* Input facts declare that the price is tax-inclusive and provide the same jurisdiction and rate references.
* The computed TaxPosition deterministically derives the pre-tax base and tax component according to the declared rounding/precision policy.
* The TaxTrace records the inclusive/exclusive flag, the derived base, and the tax component.

### 12.3 Exemption Fact Applied

* Input facts include a buyer exemption reference that is applicable in the declared jurisdiction.
* The computed TaxPosition yields zero tax for the exempt base.
* The TaxTrace records the exemption reference and why it applied.

---

## 13. Target Independence (Normative)

This specification MUST NOT define:

* a specific tax vendor integration
* jurisdiction databases
* remittance workflows
* database schemas

Targets may implement tax computation using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
