Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Diagnostic Codes

This specification defines the diagnostic system for **Behavior evaluation**.

This document is **Normative**.

---

## 1. Purpose

Diagnostics exist to:

- tell users clearly what went wrong
- identify exactly where it went wrong
- explain why it went wrong
- suggest how to fix it
- provide stable codes for tooling, filtering, and localization

Diagnostics serve both humans (messages, suggestions) and machines (codes, structured data).

---

## 2. Diagnostic Structure (Normative)

A diagnostic MUST include:

| Field | Required | Description |
|-------|----------|-------------|
| `code` | Yes | Stable machine-readable token |
| `location` | Yes | Reference to the originating expression node |
| `parameter` | If applicable | Name of the parameter that failed |
| `expected` | Yes | What was expected (domain or constraint) |
| `received` | Yes | What was actually received (type or value description) |
| `message` | Yes | Human-readable description of the problem |
| `suggestion` | Yes | Human-readable guidance on how to fix it |

### 2.1 Code Structure (Normative)

All diagnostic codes MUST follow:

```
<OperatorName>::<PARAMETER>_<CONDITION>
```

Where:

- `<OperatorName>` is the operator that produced the diagnostic
- `<PARAMETER>` is the parameter name in SCREAMING_CASE (omitted for non-parameter errors)
- `<CONDITION>` describes the failure condition

Examples:

- `Add::AUGEND_IS_ABSENT`
- `Add::AUGEND_NOT_NUMBER`
- `Add::ADDEND_IS_ABSENT`
- `Add::ADDEND_NOT_NUMBER`
- `Divide::DIVISOR_IS_ZERO`

For non-parameter errors:

- `MakeRange::INCOMPATIBLE_TYPES`
- `LinearAlgebra::DIMENSION_MISMATCH`

### 2.2 Location (Normative)

The location field MUST identify the expression node that produced the diagnostic.

Location format is implementation-defined but MUST be:

- stable across evaluations of the same program
- sufficient to identify the exact expression node
- deterministic

### 2.3 Expected and Received (Normative)

The `expected` field MUST describe:

- the domain constraint (e.g., "AnyNumber", "List", "positive Integer")
- or the structural requirement (e.g., "non-empty", "at least 2 elements")

The `received` field MUST describe:

- the actual type received (e.g., "Text", "Boolean", "Record")
- or the actual condition (e.g., "Absent", "negative", "empty List")

### 2.4 Message (Normative)

Messages MUST be:

- clear and specific
- polite (no blame, no jargon)
- grammatically correct
- consistent in style across all diagnostics

Message template:

> "The {parameter} parameter must be {expected}, but received {received}."

Or for non-parameter errors:

> "{Condition description}."

Examples:

- "The augend parameter must be a number, but received Text."
- "The divisor parameter must not be zero."
- "The list parameter must be a List, but received Absent."

### 2.5 Suggestion (Normative)

Suggestions MUST:

- provide actionable guidance
- be specific to the error
- avoid vague advice like "fix the error"

Suggestion templates:

> "Provide a {expected} value for the {parameter} parameter."

> "Ensure the expression evaluates to {expected}, not {received}."

> "Check that {parameter} is present before calling {operator}."

Examples:

- "Provide a numeric value for the augend parameter."
- "Ensure the divisor is not zero before dividing."
- "Check that the list is present and contains elements."

---

## 3. Diagnostic Ordering (Normative)

When multiple diagnostics are produced, they MUST be ordered deterministically.

Ordering key:

1. By origin expression location in depth-first, left-to-right traversal order
2. If same location, by emission order within that node's evaluation
3. If still tied, by ascending `code` (Unicode scalar value order)

---

## 4. Propagation (Normative)

When a Behavior operator receives an `Invalid(...)` operand:

1. If the operator propagates the error, it MUST NOT wrap or replace the operand's diagnostics.
2. If the operator handles the error explicitly (per its semantics), it MAY produce its own diagnostics.

---

## 5. Condition Categories (Normative)

Diagnostic codes use these condition suffixes:

| Suffix | Meaning |
|--------|---------|
| `IS_ABSENT` | Parameter is `<Absent/>` |
| `NOT_<TYPE>` | Parameter is not the required type |
| `IS_EMPTY` | Collection has no elements |
| `IS_ZERO` | Numeric value is zero |
| `IS_NEGATIVE` | Numeric value is negative |
| `OUT_OF_BOUNDS` | Index exceeds collection bounds |
| `NOT_COMPARABLE` | Values cannot be compared |
| `DUPLICATE_KEY` | Key appears more than once |
| `INVALID_FORMAT` | String format is invalid |
| `DIMENSION_MISMATCH` | Matrix/vector dimensions incompatible |

---

## 6. Operator-Specific Codes (Normative)

Each operator MUST define its own diagnostic codes for each failure condition.

### 6.1 Code Definition Requirements

For each operator, the specification MUST define:

- every parameter that can fail
- every condition that can cause failure
- the specific code for each parameter/condition combination
- the message template
- the suggestion template

### 6.2 Example: Add

| Code | Expected | Message | Suggestion |
|------|----------|---------|------------|
| `Add::AUGEND_IS_ABSENT` | AnyNumber | "The augend parameter must be a number, but received Absent." | "Provide a numeric value for the augend parameter." |
| `Add::AUGEND_NOT_NUMBER` | AnyNumber | "The augend parameter must be a number, but received {received}." | "Ensure the augend expression evaluates to a number." |
| `Add::ADDEND_IS_ABSENT` | AnyNumber | "The addend parameter must be a number, but received Absent." | "Provide a numeric value for the addend parameter." |
| `Add::ADDEND_NOT_NUMBER` | AnyNumber | "The addend parameter must be a number, but received {received}." | "Ensure the addend expression evaluates to a number." |

### 6.3 Example: Divide

| Code | Expected | Message | Suggestion |
|------|----------|---------|------------|
| `Divide::DIVIDEND_IS_ABSENT` | AnyNumber | "The dividend parameter must be a number, but received Absent." | "Provide a numeric value for the dividend parameter." |
| `Divide::DIVIDEND_NOT_NUMBER` | AnyNumber | "The dividend parameter must be a number, but received {received}." | "Ensure the dividend expression evaluates to a number." |
| `Divide::DIVISOR_IS_ABSENT` | AnyNumber | "The divisor parameter must be a number, but received Absent." | "Provide a numeric value for the divisor parameter." |
| `Divide::DIVISOR_NOT_NUMBER` | AnyNumber | "The divisor parameter must be a number, but received {received}." | "Ensure the divisor expression evaluates to a number." |
| `Divide::DIVISOR_IS_ZERO` | non-zero number | "The divisor parameter must be non-zero, but received zero." | "Check that the divisor is non-zero before dividing, or handle the zero case explicitly." |

### 6.4 Example: FilterElements

| Code | Expected | Message | Suggestion |
|------|----------|---------|------------|
| `FilterElements::LIST_IS_ABSENT` | List | "The list parameter must be a List, but received Absent." | "Provide a List value for the list parameter." |
| `FilterElements::LIST_NOT_LIST` | List | "The list parameter must be a List, but received {received}." | "Ensure the list expression evaluates to a List." |
| `FilterElements::PREDICATE_RESULT_NOT_BOOLEAN` | Boolean | "The predicate must return a Boolean, but returned {received}." | "Ensure the predicate expression evaluates to true or false." |

---

## 7. Registry Location (Normative)

The complete registry of diagnostic codes is defined per operator in the Behavior Vocabulary specifications.

Each operator definition MUST include its diagnostic codes as part of the operator specification.

This document defines the structure and conventions. The vocabulary specifications define the specific codes.

---

## 8. Localization (Normative)

Diagnostic codes are stable tokens suitable for localization keys.

Implementations MAY provide localized messages and suggestions keyed by diagnostic code.

The `message` and `suggestion` fields defined in the specification are the canonical English forms.

---

## 9. Relationship to Other Specifications

- Operator-specific codes are defined in Behavior Vocabulary specifications
- Diagnostic structure is used by Behavior Dialect Semantics
- Location references use the expression model from Behavior Dialect

---

**End of Behavior Diagnostic Codes v0.1**
