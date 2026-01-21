Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Value Ordering and Structural Equality (Behavior v0.1)

This specification defines the canonical v0.1 rules for:

- structural equality of Behavior values
- comparability and ordering of Behavior values

This document is **Normative**.

---

## 1. Purpose

Behavior is evaluated in multiple runtimes. If equality and ordering are not precisely specified, implementations will diverge in:

- set uniqueness
- join key matching
- stable sorting
- comparison predicates (`IsLessThan`, etc.)

This specification exists to remove those degrees of freedom.

---

## 2. Scope (v0.1)

This specification governs:

- structural equality used by:
  - Behavior equality operators
  - set uniqueness
  - join key identity
- ordering used by:
  - Behavior ordering operators
  - `SortElementsBy`

This specification does not define:

- the full numeric operator inventory
- coercion between unrelated domains

---

## 3. Terms

- `StructuralEquality(a, b)` returns a Boolean.
- `Compare(a, b)` returns one of: `Less`, `Equal`, `Greater`, or `NotComparable`.

---

## 4. Domain Rules (Normative)

### 4.1 Missingness

- `<Absent/>` is a value.
- `<Absent/>` MUST be structurally equal only to `<Absent/>`.
- `<Absent/>` MUST NOT be comparable to any other value (including `<Absent/>`) for ordering operators.
  - Rationale: ordering operators must be total only within their domain; `<Absent/>` is missingness, not data.

Note: `SortElementsBy` has its own missingness rule: keys equal to `<Absent/>` sort last.

### 4.2 Text

- `Text` values are structurally equal iff they are identical sequences of Unicode scalar values.
- `Text` ordering is Unicode scalar value codepoint order, lexicographic.

### 4.3 Numbers (v0.1 orderable subset)

v0.1 defines multiple semantic numeric domains, but v0.1 ordering is intentionally conservative to preserve cross-runtime determinism.

Normative rule:

- `Integer`, `Fraction`, and `PrecisionNumber` values are orderable in v0.1.

Consequences:

- If an ordering operator (`IsLessThan`, etc.) is applied to `RealNumber` values, the result MUST be `Invalid(...)`.
- If `SortElementsBy` produces keys that are not `Text`, `Integer`, `Fraction`, `PrecisionNumber`, or `<Absent/>`, the result MUST be `Invalid(...)`.

Numeric ordering (Normative):

All orderable numeric domains MUST be comparable to each other by exact numeric value.

Define an exact rational value function $R(x)$:

- If $x$ is an `Integer`, then $R(x)$ is that integer.
- If $x$ is a `Fraction`, then $R(x)$ is the exact rational value of the fraction.
- If $x$ is a `PrecisionNumber` with an explicit decimal scale, then $R(x)$ is the exact rational value represented by that decimal (for example, `12.3400` and `12.34` are numerically equal but may remain distinct as values in other domains).

Ordering rule:

- For any two numeric values $a$ and $b$ in {`Integer`, `Fraction`, `PrecisionNumber`}, `Compare(a, b)` MUST be the ordering of $R(a)$ vs $R(b)$.

### 4.4 Lists and Records

- Lists and Records are not orderable in v0.1.
- Lists and Records are structurally equal under recursive structural equality as defined below.

---

## 5. Structural Equality (Normative)

### 5.1 Type sensitivity

Structural equality is type-sensitive.

- Values of different top-level domains MUST be structurally unequal.
  - Example: `Text("1")` is not equal to `Integer(1)`.

### 5.2 Scalars

- `<Absent/>` equals `<Absent/>`.
- `Boolean` equals `Boolean` iff same truth value.
- `Text` equals `Text` iff identical Unicode scalar sequence.
- `Integer` equals `Integer` iff same integer value.

`Fraction` equality (Normative):

- A `Fraction` value has a (mathematical) rational value $n/d$ with integer numerator $n$ and integer denominator $d$.
- The canonical normalized form of a `Fraction` value is defined as follows:
  - The denominator MUST be $> 0$.
  - If $n = 0$, the canonical form MUST be $0/1$.
  - Otherwise, let $g = \gcd(|n|, d)$; the canonical form MUST be $(n/g)/(d/g)$.
- Two `Fraction` values are structurally equal iff their canonical normalized forms are identical.

`PrecisionNumber` equality (Normative):

- A `PrecisionNumber` value has an authored decimal representation (a `decimal` string).
- Two `PrecisionNumber` values are structurally equal iff their `decimal` representations are identical sequences of Unicode scalar values.
- In particular, `"1.0"` is NOT structurally equal to `"1.00"`.

### 5.3 Lists

Two `List` values are structurally equal iff:

1. they have the same length, and
2. each pair of elements at the same index are structurally equal.

### 5.4 Records

Two `Record` values are structurally equal iff:

1. they have the same set of keys, and
2. for every key, the associated values are structurally equal.

Key ordering is not semantically relevant.

---

## 6. Ordering / Comparability (Normative)

### 6.1 Comparable pairs

Two values are comparable for ordering in v0.1 iff:

- both are `Text`, or
- both are numeric values in {`Integer`, `Fraction`, `PrecisionNumber`}.

All other pairs are `NotComparable`.

### 6.2 Ordering relation

- `Text` ordering is lexicographic codepoint order.
- Numeric ordering is defined by §4.3.

---

## 7. Required Failure Behavior (Normative)

When an operator requires comparable operands and receives non-comparable operands:

- it MUST return `Invalid(...)`.
- it MUST use a diagnostic code appropriate for the surface (for example `SortElementsBy::NEED_COMPARABLE_KEYS`).

---

**End of Value Ordering and Structural Equality (Behavior v0.1)**
