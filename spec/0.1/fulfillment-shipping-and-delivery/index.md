Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Fulfillment, Shipping, and Delivery Specification

This specification defines Paperhat’s target-independent semantics for **fulfillment and shipment planning**, including:

* fulfillment intents (what must be shipped/provided)
* shipment intents and shipment records
* carrier/service selection as intent (not as integration)
* delivery status and tracking references as data

This specification is designed to compose with commerce entities, inventory promising, and workflow orchestration.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* represent fulfillment obligations and shipment plans as explicit data
* enable deterministic planning and auditable execution traces
* remain target-independent with respect to carriers, warehouses, and transport APIs

---

## 2. Scope

This specification governs:

* fulfillment intent (what is owed to the buyer)
* fulfillment units and allocation intent (where and how to fulfill)
* shipment intent and shipment records
* delivery milestones and tracking references
* trace and recordability requirements

This specification does **not** govern:

* carrier/provider integrations
* warehouse management system APIs
* address normalization vendors
* packing label formats

---

## 3. Related Specifications

This specification is designed to compose with:

* [Commerce Entities and Payments](../commerce-entities-and-payments/)
* [Inventory Promising and Availability](../inventory-promising-and-availability/)
* [Reckoning and Price Transformations](../reckoning-and-price-transformations/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Idempotency and Deduplication](../idempotency-and-deduplication/)

---

## 4. Core Invariants (Hard)

1. **Explicit inputs.** Availability, locations, cutoff times, and carrier/service constraints used for planning MUST be explicit inputs.
2. **Deterministic planning.** Given identical inputs, fulfillment allocation and shipment planning outputs MUST be identical.
3. **Target independence.** The Kernel MUST NOT require a specific carrier or warehouse system.
4. **Recordability.** Plans and execution events MUST be representable as data and traceable.

---

## 5. Definitions (Normative)

### 5.1 Fulfillment Intent

A **FulfillmentIntent** declares what must be provided for a commerce transaction, including:

* items and quantities to deliver
* destination and delivery constraints
* permissible partial shipments policy

---

### 5.2 Fulfillment Unit

A **FulfillmentUnit** is a plan unit that may be shipped together (e.g., by origin location and constraints).

---

### 5.3 Allocation Intent

An **AllocationIntent** is a deterministic plan describing:

* which inventory sources satisfy which fulfillment units
* reservation/hold references (as data)
* tie-breaking rules for equal candidates

---

### 5.4 Shipment Intent

A **ShipmentIntent** declares the planned shipment:

* origin and destination
* packed contents
* shipping service constraints (service class intent)
* readiness and cutoff constraints

This specification treats carrier/service selection as intent, not as a protocol integration.

---

### 5.5 Shipment Record

A **ShipmentRecord** is a record of a shipment created and/or executed, including:

* shipment identity
* timestamps (as explicit external inputs)
* tracking references
* status milestones

---

### 5.6 Delivery Status and Milestones

A **DeliveryStatus** is a state derived from recorded events (e.g., shipped, in-transit, delivered, exception).

Milestones MUST be recordable and MUST compose with provenance.

---

## 6. Deterministic Fulfillment Planning (Normative)

The Kernel MUST be able to deterministically derive a fulfillment plan from explicit inputs, including:

* promised availability and constraints
* eligible fulfillment locations
* policies for splitting/merging shipments
* service-level constraints

Tie-breaking rules MUST be explicit and deterministic.

---

## 7. Shipping Charges and Taxes (Non-Normative)

Shipping charges and taxability are governed by other specifications.
This spec only defines the semantics of fulfillment/shipment facts that those computations may reference.

---

## 8. Exceptions and Returns (Non-Normative)

Shipment exceptions, returns, and reverse logistics may be modeled via additional slices.
This spec limits itself to outbound fulfillment and delivery status.

---

## 9. Trace and Recordability (Normative)

A conforming system SHOULD record:

* fulfillment intents and derived plans
* allocation decisions and tie-breaks
* shipment intents and shipment records
* delivery milestone events

These records SHOULD compose with provenance/lineage.

---

## 10. Validation Requirements (Normative)

The Kernel MUST be able to validate:

* required inputs are declared
* plans reference valid identities and quantities
* timestamps are explicit external inputs when used
* tracking references are treated as opaque identifiers

---

## 11. Examples (Non-Normative)

### 11.1 Single-Origin Shipment Plan

* A FulfillmentIntent declares 1 unit of Item A to a destination reference, with partial shipments disallowed.
* Explicit inputs declare that a single fulfillment location can satisfy the entire quantity.
* The Kernel deterministically produces one FulfillmentUnit, one AllocationIntent selecting that location, and one ShipmentIntent.

### 11.2 Split Shipment Plan

* A FulfillmentIntent declares 2 units of Item A to a destination reference, with partial shipments allowed.
* Explicit inputs declare that no single location can satisfy the full quantity before a cutoff, but two locations can satisfy 1 unit each.
* The Kernel deterministically produces two FulfillmentUnits, two AllocationIntent decisions, and two ShipmentIntent outputs, recording tie-breaks if candidates are equal.

### 11.3 Delivery Milestone Recording

* A ShipmentRecord references an opaque tracking identifier and records milestone events (e.g., shipped, delivered) with event-time external input references.
* DeliveryStatus is derived from recorded milestone events.
* Provenance can link milestone events back to the shipment and fulfillment intent.

---

## 12. Target Independence (Hard)

This specification MUST NOT define:

* specific carrier APIs
* warehouse integration protocols
* address validation vendor specifics
* a particular operational UI
