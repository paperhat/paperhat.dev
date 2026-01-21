Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Inventory Promising and Availability Specification

This specification defines Paperhat’s target-independent semantics for **inventory availability** and **inventory promising** (reserving and committing quantities).

This document governs semantic meaning, determinism, and validation requirements.
It does **not** define warehouse systems, fulfillment, event systems, databases, or synchronization protocols.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* represent availability and reservation intents as declarative data
* allow deterministic evaluation of whether an order/cart can be promised
* separate inventory facts (inputs) from workflow execution (target concern)
* ensure promising decisions are auditable

---

## 2. Scope

This specification governs:

* inventory positions as explicit inputs
* availability intents and constraints
* reservation / promise intents and outcomes
* deterministic allocation across sources (warehouses) when applicable
* recordability and trace requirements

This specification does **not** govern:

* fulfillment workflows
* warehouse operations
* eventing and synchronization
* shipping and routing optimization

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Data Validation and Shape Constraints](../../validation/data-validation-and-shape-constraints/)
* [Provenance and Lineage](../../data/provenance-and-lineage/)

---

## 4. Core Invariants (Normative)

1. **Explicit inventory inputs.** Availability facts used for decisions MUST be explicit inputs.
2. **Deterministic promising.** Promising decisions MUST be deterministic given explicit inputs.
3. **Declarative intents.** Reservation and promise intents MUST be representable as data.
4. **Auditable outcomes.** Decisions MUST be traceable.
5. **Target independence.** Kernel MUST NOT assume a specific warehouse system.

---

## 5. Definitions (Normative)

### 5.1 Inventory Position

An **InventoryPosition** is an explicit input describing quantities, such as:

* available quantity
* reserved quantity

This specification does not define how positions are synchronized.

---

### 5.2 Availability Intent

An **AvailabilityIntent** declares what is needed to consider an item “available,” including:

* required quantity
* allowed sources (optional)
* substitution rules (optional)

---

### 5.3 Promise / Reservation Intent

A **PromiseIntent** is a declarative request to reserve or commit quantities for a scope (cart/order).

This specification models intent and deterministic decision outcomes, not execution.

---

### 5.4 Promising Outcome

A **PromisingOutcome** MUST distinguish:

* Promised (with allocations)
* NotPromised (with reasons)

---

### 5.5 Allocation

An **Allocation** is a deterministic assignment of required quantities to sources.

Allocation MUST be deterministic and auditable.

---

## 6. Promising Semantics (Normative)

Kernel MUST be able to evaluate promising deterministically from explicit inputs:

* required line items
* inventory positions
* availability and allocation policies (if any)

If allocation across multiple sources occurs, tie-breaking MUST be deterministic.

---

## 7. Constraints and Reasons (Normative)

Promising decisions MUST be able to produce structured reasons such as:

* insufficient available quantity
* excluded source
* invalid inventory facts

---

## 8. Trace and Recordability (Normative)

A conforming system SHOULD record:

* positions used (by reference)
* policies used (by reference)
* allocations produced
* decisions and reasons

Trace records SHOULD compose with provenance/lineage.

---

## 9. Validation Requirements (Normative)

Kernel MUST be able to validate:

* required inputs are declared
* quantity constraints are well-formed
* allocation policies are deterministic

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* warehouse APIs
* fulfillment workflows
* event protocols
* database schemas

Targets may implement inventory systems using any appropriate mechanisms, provided semantic meaning, determinism, and auditability are preserved.
