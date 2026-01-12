Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Data Validation and Shape Constraints Specification

This specification defines Paperhat’s target-independent semantics for **data validation**, **shape constraints**, and **validation outcomes**.

This document governs semantic meaning, constraints, and recordability requirements.
It does **not** define a schema language, a validator implementation, transport formats, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* make validation requirements explicit and portable
* define a deterministic, auditable model for validating values and records
* separate authored constraints from target-specific schema technologies

---

## 2. Scope

This specification governs:

* constraint declarations for values and structured data
* validation phases (author-time vs run-time)
* validation outcomes and error reporting semantics
* recordability of validation decisions

This specification does **not** govern:

* any specific schema language
* serialization formats
* database schemas
* UI form validation

---

## 3. Related Specifications

This specification is designed to compose with:

* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Conditions and Branching](../conditions-and-branching/)
* [Looping and Batching](../looping-and-batching/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Secrets and Redaction](../secrets-and-redaction/)

---

## 4. Core Invariants (Hard)

1. **Validation is declarative.** Validation requirements MUST be expressed as authored semantic constraints.
2. **Deterministic planning.** Pipeline MUST be able to validate constraint declarations deterministically.
3. **Target independence.** Semantics MUST NOT require a particular schema language or validator.
4. **Typed outcomes.** Validation MUST produce a structured outcome distinguishing success from violation.
5. **No secret disclosure.** Validation records MUST NOT leak secret material.

---

## 5. Definitions (Normative)

### 5.1 Constraint

A **Constraint** is a declarative requirement applied to a value or structured data.

Constraints MAY include:

* presence/requiredness
* type/classification
* shape requirements (fields, cardinality)
* bounds (min/max)
* membership (allowed set)
* format intent (semantic)

This specification does not define a concrete constraint expression syntax.

---

### 5.2 Validation Phase

A **ValidationPhase** identifies when validation is required.

At minimum:

* **AuthorTimeValidation**: validates authored artifacts for well-formedness and completeness
* **RunTimeValidation**: validates runtime values and records

---

### 5.3 Validation Subject

A **ValidationSubject** is the semantic identity of what is being validated.

A ValidationSubject MUST be representable without embedding the validated value.

---

### 5.4 Validation Outcome

A **ValidationOutcome** MUST distinguish:

* **Valid**
* **Invalid** with a list of **Violations**

---

### 5.5 Violation

A **Violation** is a structured description of a failed constraint.

A Violation MUST:

* identify the constraint (by reference)
* identify the subject location/field (by semantic identity)
* provide a human-readable explanation

A Violation MUST NOT include secret material.

---

## 6. Authoring Requirements (Normative)

Authored artifacts MAY declare constraints on:

* inputs to operations
* outputs produced by operations
* intermediate values
* artifact payloads and metadata

Constraints MUST be stable identifiers, not embedded executable code.

If a constraint depends on runtime data, that dependency MUST be expressed using explicit inputs.

---

## 7. Constraint Kinds (Normative)

A conforming system MUST support, at minimum, constraints sufficient to express:

* requiredness (present/absent)
* basic shape constraints for structured values
* value bounds for numeric values
* cardinality constraints for collections

Additional constraint kinds MAY be defined by Semantics packs.

---

## 8. Recordability (Normative)

Systems MUST be able to record validation behavior:

* which constraints were evaluated (by reference)
* which subjects were evaluated (by semantic identity)
* the resulting ValidationOutcome

Records MUST be redactable and MUST NOT contain secret material.

---

## 9. Determinism and External Inputs (Normative)

Validation evaluation MUST be deterministic with respect to explicit inputs.

If time influences validation (for example, temporal bounds), time MUST be treated as an external input.

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* JSON schema, XML schema, protobuf schemas, database schemas
* validator engines
* serialization formats

Targets may implement validation using any appropriate mechanism, provided semantic meaning and constraints are preserved.
