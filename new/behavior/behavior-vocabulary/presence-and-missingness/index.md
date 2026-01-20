Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Presence and Missingness

This specification defines v0.1 operators for working with the canonical missing-value concept `<Absent/>`.

This document is **Normative**.

---

## 1. Canonical Missing Value (Normative)

v0.1 defines a single canonical missing-value concept:

- `<Absent/>`

v0.1 MUST NOT introduce any semantic `Null` value.

---

## 2. Operators (Normative)

### 2.1 `IsAbsent`

Name: `IsAbsent`

Arity: 1

Signature:

- `IsAbsent(Validation<any>) -> Validation<boolean>`

Semantics:

- If the operand is `Invalid(...)`, return `Invalid(...)`.
- If the operand is `Valid(<Absent/>)`, return `Valid(true)`.
- If the operand is `Valid(x)` for any other value `x`, return `Valid(false)`.

---

### 2.2 `IsPresent`

Name: `IsPresent`

Arity: 1

Signature:

- `IsPresent(Validation<any>) -> Validation<boolean>`

Semantics:

- If the operand is `Invalid(...)`, return `Invalid(...)`.
- If the operand is `Valid(<Absent/>)`, return `Valid(false)`.
- If the operand is `Valid(x)` for any other value `x`, return `Valid(true)`.

---

## 3. Notes (Informative)

- Presence is about existence, not “truthiness”. Empty text, empty list, and empty record are present values.
- Operators that require presence SHOULD reject `<Absent/>` with `Invalid(...)` rather than treating it as a domain value.

---

**End of Behavior Vocabulary — Presence and Missingness v0.1**
