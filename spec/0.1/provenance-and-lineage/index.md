Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Provenance and Lineage Specification

This specification defines Paperhat’s target-independent semantics for **provenance** and **lineage**: describing where a value came from, how it was produced, and what semantic operations contributed to it.

This document governs semantic meaning, constraints, and recordability requirements.
It does **not** define tracing vendors, logging backends, database schemas, or transport protocols.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* enable reliable explanations of produced values and decisions
* support auditing, debugging, and accountability
* preserve determinism and target independence
* support safe redaction while retaining meaningful provenance

---

## 2. Scope

This specification governs:

* provenance statements for values, records, and artifacts
* lineage graphs and references
* constraints on what may and may not be recorded
* relationships between provenance, run logs, and artifacts

This specification does **not** govern:

* distributed tracing protocols
* vendor tracing systems
* persistence engines
* privacy/compliance programs

---

## 3. Related Specifications

This specification is designed to compose with:

* [Run Logs and Observability](../run-logs-and-observability/)
* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Search, Indexing, and Query](../search-indexing-and-query/)
* [Artifacts and Attachments](../artifacts-and-attachments/)
* [Secrets and Redaction](../secrets-and-redaction/)
* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)

---

## 4. Core Invariants (Hard)

1. **Provenance is semantic.** Provenance MUST refer to semantic concepts (operations, inputs, policies), not target-specific instrumentation.
2. **No secret disclosure.** Provenance records MUST NOT contain secret material.
3. **Deterministic description.** Pipeline MUST be able to validate provenance requirements deterministically.
4. **Stable identities.** Provenance MUST use stable identities for sources and operations.
5. **Target independence.** Semantics MUST NOT require a particular tracing or storage technology.

---

## 5. Definitions (Normative)

### 5.1 Provenance

**Provenance** is a structured description of the origin and production context of a value or record.

---

### 5.2 Lineage

**Lineage** is a graph (or graph-like structure) describing how a value depends on prior values and operations.

---

### 5.3 Provenance Subject

A **ProvenanceSubject** is the thing whose provenance is being described, such as:

* a value
* a record
* an artifact
* a decision

A ProvenanceSubject MUST be referenceable by identity.

---

### 5.4 Provenance Source

A **ProvenanceSource** is an identified origin contributor, such as:

* an authored input binding
* an external input
* a prior artifact
* a declared policy

Sources MUST be identified without embedding the source payload.

---

### 5.5 Provenance Step

A **ProvenanceStep** is an identified operation or transformation contributing to production of a subject.

A step MUST be representable as:

* operation identity
* input references
* output references
* timestamps (optional; treated as external input)

---

## 6. Authoring Requirements (Normative)

Authored artifacts MAY declare provenance requirements.

If a workflow produces externally visible outputs, authored artifacts SHOULD specify whether provenance is:

* **ProvenanceRequired**: outputs MUST be accompanied by provenance references
* **ProvenanceOptional**
* **ProvenanceForbidden**: provenance MUST NOT be recorded for the subject

The required level MUST be target-independent.

---

## 7. Recordability Requirements (Normative)

Systems MUST be able to record provenance such that:

* sources and steps are captured by stable identity
* provenance can be correlated to run logs
* provenance can reference artifacts without copying them

Provenance records MUST be redactable and MUST NOT contain secret material.

---

## 8. Redaction and Minimization (Normative)

Provenance MUST support minimization:

* ability to omit payload values while retaining structural relationships
* ability to replace sensitive fields with redacted markers
* ability to reduce granularity (for example, step-level rather than field-level)

If provenance is minimized, the system MUST still preserve stable references and a truthful structure.

---

## 9. Determinism and External Inputs (Normative)

Provenance capture and interpretation MUST be deterministic with respect to explicit inputs.

If timestamps are included, they MUST be treated as external inputs.

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* distributed tracing headers
* vendor-specific span models
* storage schemas
* logging backends

Targets may implement provenance capture using any appropriate mechanism, provided semantic meaning and constraints are preserved.
