Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Relational and Predicates

This specification defines the v0.1 **Relational and predicate operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines the canonical v0.1 operators for:

- equality over Behavior values
- ordering over the v0.1 comparable domains
- boolean predicate composition

---

## 2. Shared Definitions (Normative)

### 2.1 Evaluation contract

- Each operand is a Behavior expression evaluated to `Validation<Value>`.
- Unless explicitly stated otherwise, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)` (propagation).

### 2.2 Structural equality and ordering

- Structural equality and comparability are defined by the v0.1 spec: **Value Ordering and Structural Equality**.
- In particular, only the v0.1 comparable domains are permitted for ordering operators.

Diagnostic code rule (Normative):

- Where this specification requires an `Invalid(...)` produced by the operator itself (not propagated from an operand), it MUST use the corresponding code defined by **Behavior Diagnostic Codes**.

---

## 3. Equality Operators (Normative)

### 3.1 `IsEqualTo`

Name: `IsEqualTo`

Arity: 2

Signature:

- `IsEqualTo(Validation<any>, Validation<any>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid(...)`, return `Invalid(...)`.
- Otherwise return `Valid(StructuralEquality(left, right))`.

### 3.2 `IsUnequalTo`

Name: `IsUnequalTo`

Arity: 2

Signature:

- `IsUnequalTo(Validation<any>, Validation<any>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid(...)`, return `Invalid(...)`.
- Otherwise return `Valid(!StructuralEquality(left, right))`.

---

## 4. Ordering Operators (Normative)

Ordering operators compare values using the v0.1 `Compare(a, b)` relation defined by **Value Ordering and Structural Equality**.

Rules:

1. If either operand is `Invalid(...)`, the result MUST be `Invalid(...)`.
2. If the two operands are not comparable under the v0.1 ordering rules, the result MUST be `Invalid(...)`.

### 4.1 `IsLessThan`

Name: `IsLessThan`

Arity: 2

Signature:

- `IsLessThan(Validation<T>, Validation<T>) -> Validation<boolean>` where `T` is comparable.

Semantics:

- If operands are not comparable, return `Invalid(...)` with code `IsLessThan::NEED_COMPARABLE_VALUES`.
- Otherwise return `Valid(Compare(left, right) == Less)`.

### 4.2 `IsMoreThan`

Name: `IsMoreThan`

Arity: 2

Signature:

- `IsMoreThan(Validation<T>, Validation<T>) -> Validation<boolean>` where `T` is comparable.

Semantics:

- If operands are not comparable, return `Invalid(...)` with code `IsMoreThan::NEED_COMPARABLE_VALUES`.
- Otherwise return `Valid(Compare(left, right) == Greater)`.

### 4.3 `IsNoLessThan`

Name: `IsNoLessThan`

Arity: 2

Signature:

- `IsNoLessThan(Validation<T>, Validation<T>) -> Validation<boolean>` where `T` is comparable.

Semantics:

- If operands are not comparable, return `Invalid(...)` with code `IsNoLessThan::NEED_COMPARABLE_VALUES`.
- Otherwise return `Valid(Compare(left, right) in {Greater, Equal})`.

### 4.4 `IsNoMoreThan`

Name: `IsNoMoreThan`

Arity: 2

Signature:

- `IsNoMoreThan(Validation<T>, Validation<T>) -> Validation<boolean>` where `T` is comparable.

Semantics:

- If operands are not comparable, return `Invalid(...)` with code `IsNoMoreThan::NEED_COMPARABLE_VALUES`.
- Otherwise return `Valid(Compare(left, right) in {Less, Equal})`.

---

## 5. Boolean Predicate Composition (Normative)

These operators compose boolean predicates.

Typing rule:

- If an operand evaluates to `Valid(x)` where `x` is not `Boolean`, the operator MUST return `Invalid(...)` with the corresponding `...::NEED_BOOLEAN` code.

### 5.1 `Not`

Name: `Not`

Arity: 1

Signature:

- `Not(Validation<boolean>) -> Validation<boolean>`

Semantics:

- If the operand is `Invalid(...)`, return `Invalid(...)`.
- If the operand is `Valid(true)`, return `Valid(false)`.
- If the operand is `Valid(false)`, return `Valid(true)`.
- If the operand is `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `Not::NEED_BOOLEAN`.

### 5.2 `And`

Name: `And`

Arity: 2 or more

Signature:

- `And(Validation<boolean>...) -> Validation<boolean>`

Semantics (Strict):

- Arguments MUST be evaluated left-to-right.
- If any argument evaluates to `Invalid(...)`, return `Invalid(...)`.
- If any argument evaluates to `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `And::NEED_BOOLEAN`.
- Otherwise return `Valid(true)` iff all arguments are `Valid(true)`.

### 5.3 `Or`

Name: `Or`

Arity: 2 or more

Signature:

- `Or(Validation<boolean>...) -> Validation<boolean>`

Semantics (Strict):

- Arguments MUST be evaluated left-to-right.
- If any argument evaluates to `Invalid(...)`, return `Invalid(...)`.
- If any argument evaluates to `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `Or::NEED_BOOLEAN`.
- Otherwise return `Valid(true)` iff any argument is `Valid(true)`.

---

## 6. Relationship to Behavior Dialect (Normative)

These operators are part of the v0.1 Behavior Dialect operator inventory.

The Behavior Dialect MUST agree with this specification on:

- operator names
- arity
- strictness vs short-circuiting
- type/domain failure behavior

See: [Behavior Dialect](../../behavior-dialect/)

---

**End of Behavior Vocabulary — Relational and Predicates v0.1**
