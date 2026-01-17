Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Commerce Entities and Payments Specification

This specification defines Paperhat’s target-independent semantics for **commerce entities** (products, carts, orders, returns, quotes, subscriptions, inventory positions) and **payments as data**.

This document governs semantic meaning, determinism, and validation requirements.
It does **not** define payment gateways, provider APIs, shipping/fulfillment systems, fraud systems, or a complete commerce platform.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define a portable, declarative model of commerce entities
* represent payments as structured data independent of providers
* support deterministic validation and auditable records
* enable composition with separate semantics for workflows, policies, and reckoning

---

## 2. Scope

This specification governs:

* product, variant, and catalog entities
* cart and order entities (as declarative records)
* payment intents and payment events (authorization, capture, refund) as data
* returns, gift cards / stored value entities, subscriptions, and quotes
* inventory position intent (available/reserved) as data

This specification does **not** govern:

* promotion engines and price adjustment rules (see reckoning semantics)
* state machines, events, and distribution protocols
* shipping, fulfillment, tax vendors, or fraud detection

---

## 3. Related Specifications

This specification is designed to compose with:

* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Idempotency and De-duplication](../idempotency-and-deduplication/)

---

## 4. Core Invariants (Normative)

1. **Entities are declarative.** Commerce entities MUST be representable as declarative data.
2. **Stable identities.** Entities MUST have stable, IRI-like identities.
3. **Provider-agnostic payments.** Payment concepts MUST NOT encode provider protocols.
4. **Deterministic validation.** Kernel MUST be able to validate entity conformance deterministically.
5. **Auditability.** Changes and derived decisions SHOULD be explainable via provenance and traces.

---

## 5. Definitions (Normative)

### 5.1 Entity

An **Entity** is a declared thing with a stable identity and typed properties.

Entities SHOULD be representable as a graph of statements. This specification does not require any particular storage engine or query language.

---

### 5.2 Money and Amount

A **MoneyAmount** is a value consisting of:

* a numeric quantity in a declared unit
* a currency identity (or other monetary unit)
* an explicit precision / scale policy (when needed)

Conforming systems MUST avoid ambiguous floating-point semantics for monetary amounts.

---

### 5.3 Price

A **Price** is a MoneyAmount with additional semantics such as:

* base price identity
* applicability scope (product, variant, customer tier, etc.)
* effective time window (optional; time is an explicit external input)

This specification does not define promotion adjustments.

---

### 5.4 Product

A **Product** is an entity representing something that may be purchased.

Products MAY include:

* identifiers (SKU-like codes)
* localized names and descriptions (by message keys)
* variants/options
* base prices
* tax classification intent (semantic)
* media references (as artifact references)

---

### 5.5 Cart and Order

A **Cart** is an entity representing intended purchase contents.

An **Order** is an entity representing a committed purchase record.

Carts and Orders MUST be representable as declarative records, including:

* line items
* quantities
* item references
* base prices and totals (as declared values)

This specification does not define lifecycle state machines.

---

### 5.6 Payment as Data

A **PaymentIntent** is a declarative intent to transfer value.

A **PaymentEvent** is a recorded event describing a payment step, such as:

* Authorization
* Capture
* Void
* Refund

Payment records MUST separate:

* what was intended
* what was attempted
* what was confirmed

Payment records MUST be provider-agnostic.

---

### 5.7 Returns and Refund Records

A **Return** is an entity describing what was returned and why.

A **RefundRecord** is an entity describing refund intent and payment events.

Refund amount calculation semantics belong to reckoning.

---

### 5.8 Stored Value

A **StoredValueInstrument** is an entity representing value that may be applied (e.g., gift card, store credit, rewards value).

A stored value instrument MUST be representable as:

* identity
* balance / available value (as data)
* status
* redemption history references

Balance persistence is out of scope.

---

### 5.9 Subscription

A **Subscription** is an entity representing a recurring purchase agreement.

This specification covers subscription data shape and identities, not billing execution.

---

### 5.10 Quote

A **Quote** is an entity representing a priced offer with terms and an expiration.

This specification covers quote data shape and identities, not acceptance workflows.

---

### 5.11 Inventory Position

An **InventoryPosition** is an entity representing quantities such as:

* available
* reserved

Inventory strategies and event synchronization are out of scope.

---

## 6. Validation Requirements (Normative)

Kernel MUST be able to validate:

* entity identity shape and uniqueness constraints
* required fields (SKU-like codes, currency identity, etc.)
* money amount constraints (non-negative where required, consistent currency where required)
* referential integrity (line items reference existing products/variants)

---

## 7. Recordability and Provenance (Normative)

Systems SHOULD record provenance for:

* origin of entity values
* relationship between orders, payments, returns, and refunds

Records MUST avoid secret material.

---

## 8. Target Independence (Normative)

This specification MUST NOT define:

* payment provider APIs or protocols
* database schemas
* query languages
* shipping/fulfillment systems

Targets may implement storage and provider integrations using any appropriate mechanisms, provided the semantic model and constraints are preserved.
