Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Conditions and Branching Specification

This specification defines Paperhat’s target-independent semantics for **conditions**, **filters**, and **branching** within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define a concrete expression language, syntax, runtime, or target-specific rule engine.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* enable workflows to branch based on declarative conditions
* support deterministic planning and validation of branching
* keep condition semantics target-independent and auditable
* prevent embedding code or syntax into authored content

---

## 2. Scope

This specification governs:

* condition definitions and evaluation requirements
* branching semantics
* gating semantics (allow/deny flow)
* missing and unknown condition outcomes
* recordability and provenance of condition outcomes

This specification does **not** govern:

* expression syntax
* rule engine implementation
* UI for configuring conditions

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [State, Commands, and Continuations](../state-commands-and-continuations/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Hard)

1. **Conditions are data.** A condition MUST be representable as a declarative artifact.
2. **No code leakage.** Authored artifacts MUST NOT embed target code or require a specific expression syntax.
3. **Deterministic planning.** The Kernel MUST be able to validate and plan branching deterministically.
4. **Explicit inputs.** Condition inputs MUST be explicit via declared value sourcing.
5. **Auditable outcomes.** Condition results MUST be recordable.

---

## 5. Definitions (Normative)

### 5.1 Condition

A **Condition** is a declarative predicate that yields a condition result.

A Condition MUST include:

* a condition identity
* declared inputs
* declared evaluation requirements

A Condition MUST NOT depend on implicit environment.

---

### 5.2 Condition Result

A **ConditionResult** represents the evaluation outcome.

At minimum, condition results MUST support:

* **True**
* **False**
* **Unknown** (insufficient information to decide)

The meaning of Unknown MUST be explicit and plan-visible.

---

### 5.3 Branch

A **Branch** is an alternative path of execution selected by condition results.

---

### 5.4 Gate

A **Gate** is a coordination step that blocks progression unless a condition is satisfied.

A gate MUST define what happens on False and Unknown outcomes.

---

## 6. Condition Input Semantics (Normative)

Condition inputs MUST be declared using value sourcing.

Inputs MAY refer to:

* step outputs
* state projections
* event payloads
* literals
* explicitly declared context values

---

## 7. Branching Semantics (Normative)

Branching MUST be expressible without syntax.

A branching construct MUST define:

* the condition(s) evaluated
* the branch selection mapping from results to branches
* the default behavior when results are Unknown

Branching SHOULD support multi-branch selection.

---

## 8. Failure and Validation (Normative)

Condition evaluation MUST distinguish between:

* **ConditionResult = Unknown** (not enough information)
* **Failure** (invalid inputs, type mismatch, or policy rejection)

Typed failures SHOULD align with transformation/mapping failures where appropriate.

---

## 9. Recordability (Normative)

Run logs MUST be able to record:

* the condition identity evaluated
* inputs used (by reference)
* the condition result
* any failures
* branch selection decision

Records MUST NOT require embedding secrets.

---

## 10. Target Independence (Hard)

This specification MUST NOT define:

* a concrete expression language
* a concrete interpreter
* UI configuration patterns

Targets may realize conditions using any appropriate mechanism, provided the semantic meaning and recordability requirements are preserved.
