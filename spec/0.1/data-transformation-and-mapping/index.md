Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Data Transformation and Mapping Specification

This specification defines Paperhat’s target-independent semantics for **data transformation** and **mapping** within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define a concrete programming language, runtime, sandbox implementation, or target-specific expression engine.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* express transformations as declarative intent
* enable deterministic planning and validation
* support safe mapping between step outputs and step inputs
* prevent target/runtime details from leaking into authored artifacts

---

## 2. Scope

This specification governs:

* mapping of values from prior step outputs, state projections, event facts, and literal values
* transformation definitions and constraints
* type expectations and validation semantics
* handling of missing or invalid values
* provenance and recordability expectations

This specification does **not** govern:

* concrete expression language syntax
* sandbox execution implementation
* serialization formats

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [State, Commands, and Continuations](../state-commands-and-continuations/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Transformation intent is data.** Transformations MUST be representable as declarative artifacts.
2. **No code leakage.** Authored artifacts MUST NOT require embedding target code.
3. **Deterministic planning.** Kernel MUST be able to validate and plan transformation steps deterministically.
4. **Explicit inputs.** Any required external inputs MUST be declared explicitly.
5. **Typed outcomes.** Transformation failures MUST be representable as typed failures.

---

## 5. Definitions (Normative)

### 5.1 Mapping

A **Mapping** is a declarative rule for producing an output value from one or more ValueSources.

---

### 5.2 ValueSource

A **ValueSource** identifies where a value comes from.

A ValueSource MAY refer to:

* a step output
* a state projection
* an event payload
* a literal value
* a contextual value (explicitly declared)

---

### 5.3 Transformation

A **Transformation** is a declarative description of how to compute a value from inputs.

A Transformation MUST be describable without assuming a specific language or runtime.

---

### 5.4 Type Expectation

A **TypeExpectation** constrains the shape and meaning of values.

Type expectations MUST be validated deterministically by Kernel.

---

### 5.5 Missing Value Handling

A mapping MUST specify how missing required values are handled.

Missing value handling MUST be semantic and MUST NOT assume a UI.

---

## 6. Mapping Semantics (Normative)

A mapping MUST declare:

* input sources
* expected output type
* missing value policy

A mapping MAY declare:

* normalization rules
* validation constraints

---

## 7. Transformation Semantics (Normative)

A transformation MUST be expressible as:

* a transformation identity
* declared inputs
* declared output type
* declared constraints

A transformation MUST NOT embed executable target code.

---

## 8. Validation and Failure (Normative)

If mapping or transformation validation fails, the system MUST produce typed failures, including:

* MissingRequiredValue
* InvalidValue
* TypeMismatch

---

## 9. Recordability (Normative)

Run logs MUST be able to record:

* the mapping/transformation identity applied
* which sources were used
* whether validation succeeded
* failure classifications when applicable

Run logs MUST NOT require recording secret material.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* a concrete expression syntax
* a concrete interpreter or runtime API
* a concrete serialization format

Targets may realize transformations using any appropriate mechanism, provided semantic meaning, determinism of planning, and recordability requirements are preserved.
