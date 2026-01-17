Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Data Stores and Shared Variables Specification

This specification defines Paperhat’s target-independent semantics for **data stores** and **shared variables** used by workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete databases, key/value engines, transactions, network protocols, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to read and write shared values as declarative intent
* define the meaning of store identity, keys, and value types
* ensure deterministic planning while allowing runtime data to vary
* preserve auditability and recordability of store interactions

---

## 2. Scope

This specification governs:

* store identity and store selection (semantic)
* keys and key derivation semantics
* typed values and validation expectations
* read/write operations as workflow steps
* consistency and concurrency intent (semantic)
* recordability requirements

This specification does **not** govern:

* concrete storage technologies
* transaction implementations
* locking implementations
* query languages

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Resource Limits and Rate Limiting](../resource-limits-and-rate-limiting/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Store operations are data.** Reads and writes MUST be representable as declarative workflow intent.
2. **Target independence.** Store semantics MUST NOT assume a concrete database or protocol.
3. **Deterministic planning.** Kernel MUST be able to validate and plan store interactions deterministically.
4. **Typed values.** Store values MUST be constrained by type expectations.
5. **Auditability.** It MUST be possible to record what was attempted, with what semantic identities.

---

## 5. Definitions (Normative)

### 5.1 Data Store

A **DataStore** is a semantic identity for a storage domain.

A DataStore MUST be referencable by identity.

---

### 5.2 Store Key

A **StoreKey** identifies a value in a store.

Store keys MUST be derived from declared value sources.

---

### 5.3 Store Value

A **StoreValue** is a typed value associated with a StoreKey.

---

### 5.4 Store Operation

A **StoreOperation** is a declarative intent to interact with a store.

Store operations MUST include at minimum:

* **ReadValue**
* **WriteValue**

Store operations MAY include conditional write intent (for example, compare-and-set) as semantic constraints.

---

### 5.5 Consistency Intent

A **ConsistencyIntent** is a declarative statement describing the expected consistency constraints.

Consistency intent MUST be target-independent and MUST NOT define a concrete algorithm.

---

## 6. Read Semantics (Normative)

A read operation MUST declare:

* store identity
* key derivation
* expected value type
* behavior when the key is missing

---

## 7. Write Semantics (Normative)

A write operation MUST declare:

* store identity
* key derivation
* value source
* expected value type

A write MAY declare conditional constraints (for example, write only if current value matches an expected value).

---

## 8. Concurrency and Coordination (Normative)

Store operations MUST compose with:

* mutual exclusion semantics
* ordering constraints
* concurrency limits

A plan MUST be able to explain why a store operation was blocked or serialized.

---

## 9. Reliability Interaction (Normative)

Store operations MAY be subject to retry policy.

If store writes are retried, idempotency requirements MUST be expressible and auditable.

---

## 10. Recordability (Normative)

Run logs MUST be able to record:

* store identity
* operation identity
* key identity (and derived key value when permitted)
* typed outcome
* failures and policy decisions

Records MUST NOT require embedding secrets.

---

## 11. Target Independence (Normative)

This specification MUST NOT define:

* SQL syntax
* database vendor APIs
* transaction/locking implementations

Targets may realize stores using any appropriate mechanism, provided semantic meaning and recordability requirements are preserved.
