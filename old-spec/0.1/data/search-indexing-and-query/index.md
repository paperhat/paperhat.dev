Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Search, Indexing, and Query Specification

This specification defines Paperhat’s target-independent semantics for **search**, **indexing**, and **query** operations used by workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete databases, query languages, ranking algorithms, vector systems, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to express query intent as declarative steps
* define the semantic meaning of indexing and searching
* preserve deterministic planning while allowing runtime data to vary
* keep query syntax and storage implementation out of authored artifacts

---

## 2. Scope

This specification governs:

* index identity and selection (semantic)
* indexing operations (add/update/remove)
* query operations and query intent
* result shaping and type expectations
* pagination and limits (semantic)
* recordability requirements

This specification does **not** govern:

* SQL or other query syntaxes
* ranking/scoring algorithms
* vector embedding algorithms
* storage engines

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../../workflow/workflow-orchestration/)
* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Data Stores and Shared Variables](../data-stores-and-shared-variables/)
* [Run Logs and Observability](../../operations/run-logs-and-observability/)
* [Resource Limits and Rate Limiting](../../workflow/resource-limits-and-rate-limiting/)

---

## 4. Core Invariants (Normative)

1. **Query intent is data.** Query and indexing intent MUST be representable as declarative artifacts.
2. **No syntax leakage.** Authored artifacts MUST NOT embed query language syntax.
3. **Deterministic planning.** Kernel MUST be able to validate and plan query steps deterministically.
4. **Typed results.** Query results MUST be constrained by declared type expectations.
5. **Auditability.** It MUST be possible to record what was asked and what was returned (as permitted data).

---

## 5. Definitions (Normative)

### 5.1 Index

An **Index** is a semantic identity for a searchable collection.

An Index MUST be referencable by identity.

---

### 5.2 Index Document

An **IndexDocument** is a typed unit of indexed content.

Index documents MUST have:

* a document identity
* a declared type expectation

---

### 5.3 Index Operation

An **IndexOperation** is a declarative intent to affect an index.

Index operations MUST include at minimum:

* AddDocument
* UpdateDocument
* RemoveDocument

---

### 5.4 Query

A **Query** is a declarative intent to retrieve results from an index.

A Query MUST declare:

* index identity
* query intent
* expected result type
* result limits

---

### 5.5 Query Intent

A **QueryIntent** describes what is being asked for without binding to a specific syntax.

QueryIntent MAY include:

* semantic filters (field/value constraints)
* semantic text match intent
* semantic similarity intent
* sort intent

These are semantic intents only.

---

### 5.6 Result Window

A **ResultWindow** is a declarative description of paging and limits.

---

## 6. Indexing Semantics (Normative)

Index operations MUST declare:

* index identity
* document identity
* document content source (without embedding binaries)
* document type expectation

Index operations MUST be target-independent.

---

## 7. Query Semantics (Normative)

Queries MUST declare:

* index identity
* query intent
* expected result type
* result window

Queries MUST NOT embed query syntax.

---

## 8. Limits and Resource Governance (Normative)

Query and indexing steps MUST be able to declare limits.

Limits MUST compose with resource/rate limiting semantics.

---

## 9. Recordability (Normative)

Run logs MUST be able to record:

* index identity
* query identity
* query intent (as permitted data)
* result window
* result count
* typed outcome

Records MUST NOT require embedding secrets.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* query languages
* ranking algorithms
* database APIs
* vector embedding algorithms

Targets may realize search and indexing using any appropriate mechanism, provided semantic meaning and recordability requirements are preserved.
