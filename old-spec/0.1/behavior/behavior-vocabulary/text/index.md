Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Text

This specification defines the v0.1 **Text operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines deterministic, runtime-neutral text predicates and relations for Behavior Programs.

Goals:

- stable behavior across Kernel and HTML runtime
- locale-independent, deterministic Unicode handling
- predictable treatment of `<Absent/>` and non-Text values

---

## 2. Shared Definitions (Normative)

### 2.1 Text model

- `Text` is a sequence of Unicode scalar values.

Length and indexing:

- Unless stated otherwise, “length” is the number of Unicode scalar values.

### 2.2 Evaluation contract

- Each operand is a Behavior expression evaluated to `Validation<Value>`.
- Unless explicitly stated otherwise, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)` (propagation).

### 2.3 Predicate totality policy (Normative)

Unless explicitly stated otherwise, Text operators in this family are *total predicates*:

- If an operand evaluates to `Valid(<Absent/>)`, the result MUST be `Valid(false)`.
- If an operand evaluates to `Valid(x)` where `x` is not `Text`, the result MUST be `Valid(false)`.

This rule avoids “type-error as failure” for common validation predicates.

### 2.4 Locked semantic profiles

This family reuses the locked profiles defined by the validation surface specifications:

- Regular expression profile: [Regular Expression Profile](../../../validation/regular-expression-profile/)
- Alphabetical collation profile and Unicode/case locks: [Predicate, Guard, and Validation Composition Surface Specification](../../../validation/predicate-guard-and-validation-composition-surface/)

Where these profiles define a behavior (for example NFC normalization, case-fold algorithm, or whitespace set), implementations MUST follow them.

---

## 3. Containment Predicates (Normative)

### 3.1 `ContainsSubstring`

Name: `ContainsSubstring`

Arity: 2

Signature:

- `ContainsSubstring(value, needle) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff `needle` occurs as an exact substring of `value`.

### 3.2 `StartsWithSubstring`

Name: `StartsWithSubstring`

Arity: 2

Signature:

- `StartsWithSubstring(value, prefix) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff `value` begins with `prefix`.

### 3.3 `EndsWithSubstring`

Name: `EndsWithSubstring`

Arity: 2

Signature:

- `EndsWithSubstring(value, suffix) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff `value` ends with `suffix`.

---

## 4. Length Predicates (Normative)

For these predicates, `length(value)` is the number of Unicode scalar values.

### 4.1 `HasLengthEqualTo`

Arity: 2

- If `value` is not `Text`, return `Valid(false)`.
- If `n` is not an `Integer`, return `Valid(false)`.
- If `n < 0`, return `Valid(false)`.
- Otherwise return `Valid(length(value) == n)`.

### 4.2 `HasLengthAtLeast`

Arity: 2

- Same domain rules as `HasLengthEqualTo`.
- Return `Valid(length(value) >= n)`.

### 4.3 `HasLengthAtMost`

Arity: 2

- Same domain rules as `HasLengthEqualTo`.
- Return `Valid(length(value) <= n)`.

### 4.4 `HasLengthBetweenInclusive`

Arity: 3

- If `value` is not `Text`, return `Valid(false)`.
- If `min` or `max` is not an `Integer`, return `Valid(false)`.
- If `min < 0` or `max < 0`, return `Valid(false)`.
- If `min > max`, return `Valid(false)`.
- Otherwise return `Valid(min <= length(value) <= max)`.

---

## 5. Character Class Predicates (Normative)

These predicates are defined by Unicode character properties.

The v0.1 conformance suite locks the exact Unicode Character Database behavior used by these predicates.

### 5.1 `ContainsOnlyLetters`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and every scalar is a Unicode Letter.

### 5.2 `ContainsOnlyDigits`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and every scalar is a Unicode Digit.

### 5.3 `ContainsOnlyLettersAndDigits`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and every scalar is either a Unicode Letter or Digit.

### 5.4 `ContainsOnlyWhitespace`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and every scalar is in the locked whitespace set.

### 5.5 `ContainsOnlyPrintableCharacters`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and every scalar is “printable” under the locked v0.1 definition.

---

## 6. Case Predicates (Normative)

### 6.1 `IsUppercase`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and is uppercase under the locked v0.1 definition.

### 6.2 `IsLowercase`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and is lowercase under the locked v0.1 definition.

### 6.3 `IsTitleCase`

Arity: 1

- Return `Valid(true)` iff the value is `Text` and is titlecase under the locked v0.1 definition.

### 6.4 `IsCaseInsensitiveEqualTo`

Arity: 2

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff `SimpleCaseFold(left) == SimpleCaseFold(right)` under the locked v0.1 case-fold profile.

---

## 7. Ordering Predicates (Normative)

These operators use the locked alphabetical collation profile.

### 7.1 `IsAlphabeticallyBefore`

Arity: 2

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff the left value is alphabetically before the right value.

### 7.2 `IsAlphabeticallyAfter`

Arity: 2

- If either operand is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff the left value is alphabetically after the right value.

---

## 8. Pattern Predicates (Normative)

These operators use the v0.1 Regular Expression Profile.

### 8.1 `MatchesRegularExpression`

Arity: 2

- If the value is not `Text`, return `Valid(false)`.
- If the pattern is not `Text`, return `Valid(false)`.
- If the pattern is invalid or uses an unsupported construct under the v0.1 profile, return `Invalid(...)` with code `MatchesRegularExpression::INVALID_PATTERN`.
- Otherwise return `Valid(true)` iff the pattern matches the value.

### 8.2 `DoesNotMatchRegularExpression`

Arity: 2

- Same rules as `MatchesRegularExpression`.
- Otherwise return `Valid(!matches)`.

---

## 9. Relationship to Behavior Dialect (Normative)

These operators are part of the v0.1 Behavior operator inventory.

Tooling MAY accept legacy or shorthand spellings as input aliases, but SHOULD normalize to these canonical spellings when emitting a canonical surface form.

---

## 10. Conformance Appendix (Informative)

See [conformance-appendix/index.md](conformance-appendix/index.md).

---

**End of Behavior Vocabulary — Text v0.1**
