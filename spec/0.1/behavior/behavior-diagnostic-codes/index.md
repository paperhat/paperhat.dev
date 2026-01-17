Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Diagnostic Codes

This specification defines the canonical diagnostic code set for v0.1 **Behavior evaluation and decoding**.

This document is **Normative**.

---

## 1. Purpose

These codes exist to:

- make failures stable across runtimes (Kernel vs HTML runtime)
- support tooling, filtering, and localization
- prevent accidental code drift caused by ad-hoc error strings

Codes are not user-facing messages.

---

## 2. Code Structure (Normative)

All diagnostic codes MUST follow:

```
<surfaceName>::<ISSUE_DESCRIPTION>
```

This requirement is shared with the Diagnostic Messaging and Help Philosophy specification.

---

## 3. General Rules (Normative)

1. When a Behavior construct is specified to return `Invalid(...)` for a particular condition, it MUST emit the corresponding code from this registry.
2. When a Behavior construct propagates an operand’s `Invalid(...)`, it MUST NOT wrap or replace the operand’s codes.
3. Implementations MAY add additional diagnostics, but MUST NOT omit the required diagnostic for the condition.

---

## 4. Program Decoding and Encoding Codes (Normative)

### 4.1 Behavior Program Encoding

- `BehaviorProgramEncoding::NULL_NOT_UNDERSTOOD`
  - emitted when an `EncodedValue` contains a null literal in an external serialization.

- `BehaviorProgramEncoding::TAG_NOT_UNDERSTOOD`
  - emitted when a `Record` contains the reserved `"@paperhat"` key but does not match a known tagged encoding.

- `BehaviorProgramEncoding::INTEGER_NOT_UNDERSTOOD`
  - emitted when a tagged `Integer` encoding is present but malformed.

- `BehaviorProgramEncoding::FRACTION_NOT_UNDERSTOOD`
  - emitted when a tagged `Fraction` encoding is present but malformed (including denominator = 0).

- `BehaviorProgramEncoding::PRECISIONNUMBER_NOT_UNDERSTOOD`
  - emitted when a tagged `PrecisionNumber` encoding is present but malformed.

- `BehaviorProgramEncoding::OPERATION_NOT_UNDERSTOOD`
  - emitted when an expression node’s `operation` token is unknown.

- `BehaviorProgramEncoding::NEED_NAME`
  - emitted when a name-bearing reserved op is missing its `name` field (e.g., `Variable`, `Field`).

- `BehaviorProgramEncoding::NEED_STEPS`
  - emitted when a path-bearing reserved op is missing its `steps` field (`Path`).

---

## 5. Core Safe Transform Codes (Normative)

### 5.0 Shared transform safety

- `CoreSafeTransforms::LIMIT_EXCEEDED`
  - emitted when a Core Safe Transform would exceed an active resource limit profile.

### 5.1 `MapElements`

- `MapElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

### 5.2 `FilterElements`

- `FilterElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `FilterElements::NEED_BOOLEAN`
  - emitted when the predicate expression evaluates to `Valid(x)` where `x` is not `Boolean`.

### 5.2A `FindAllElements`

- `FindAllElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `FindAllElements::NEED_BOOLEAN`
  - emitted when the predicate expression evaluates to `Valid(x)` where `x` is not `Boolean`.

### 5.3 `FindFirstElement`

- `FindFirstElement::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `FindFirstElement::NEED_BOOLEAN`
  - emitted when the predicate expression evaluates to `Valid(x)` where `x` is not `Boolean`.

### 5.4 `SortElementsBy`

- `SortElementsBy::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `SortElementsBy::NEED_COMPARABLE_KEYS`
  - emitted when two non-`<Absent/>` keys are not comparable under the v0.1 ordering rules.

### 5.4A `TakeFirstElements`

- `TakeFirstElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `TakeFirstElements::NEED_INTEGER_COUNT`
  - emitted when the count operand is not an `Integer`.

- `TakeFirstElements::NEED_NONNEGATIVE_COUNT`
  - emitted when the count operand is negative.

### 5.4B `DropFirstElements`

- `DropFirstElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `DropFirstElements::NEED_INTEGER_COUNT`
  - emitted when the count operand is not an `Integer`.

- `DropFirstElements::NEED_NONNEGATIVE_COUNT`
  - emitted when the count operand is negative.

### 5.5 `MergeRecords`

- `MergeRecords::NEED_RECORD`
  - emitted when any operand is not a `Record`.

- `MergeRecords::KEY_COLLISION_HIT_SNAG`
  - emitted when a key collision occurs (InvalidOnCollision).

### 5.5A `DistinctElements`

- `DistinctElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

### 5.5B `FlattenElements`

- `FlattenElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `FlattenElements::NEED_LIST_ELEMENTS`
  - emitted when any element of the input list is not a `List`.

### 5.5C `CountElements`

- `CountElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

### 5.5D `SumElements`

- `SumElements::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `SumElements::NEED_ORDERABLE_NUMBER_ELEMENTS`
  - emitted when any element of the input list is not in `OrderableNumber`.

### 5.5E `MinimumElement`

- `MinimumElement::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `MinimumElement::NEED_NONABSENT_ELEMENTS`
  - emitted when any element of the input list is `<Absent/>`.

- `MinimumElement::NEED_MUTUALLY_COMPARABLE_ELEMENTS`
  - emitted when any comparison required to determine the minimum is NotComparable under the v0.1 ordering rules.

### 5.5F `MaximumElement`

- `MaximumElement::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `MaximumElement::NEED_NONABSENT_ELEMENTS`
  - emitted when any element of the input list is `<Absent/>`.

- `MaximumElement::NEED_MUTUALLY_COMPARABLE_ELEMENTS`
  - emitted when any comparison required to determine the maximum is NotComparable under the v0.1 ordering rules.

### 5.5G `SelectFields`

- `SelectFields::NEED_RECORD`
  - emitted when the first operand is not a `Record`.

- `SelectFields::NEED_LIST`
  - emitted when the second operand is not a `List`.

- `SelectFields::NEED_TEXT_FIELD_NAMES`
  - emitted when any selected field name is not `Text`.

- `SelectFields::NEED_DISTINCT_FIELD_NAMES`
  - emitted when the field name list contains duplicates.

### 5.5H `SplitString`

- `SplitString::NEED_TEXT`
  - emitted when the first operand is not `Text`.

- `SplitString::NEED_TEXT_SEPARATOR`
  - emitted when the separator operand is not `Text`.

- `SplitString::NEED_NONEMPTY_SEPARATOR`
  - emitted when the separator is the empty string.

### 5.5I `JoinStrings`

- `JoinStrings::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `JoinStrings::NEED_TEXT_SEPARATOR`
  - emitted when the separator operand is not `Text`.

- `JoinStrings::NEED_TEXT_ELEMENTS`
  - emitted when any element of the list is not `Text`.

### 5.6 `JoinCollectionsOnKey`

- `JoinCollectionsOnKey::NEED_LIST`
  - emitted when either side is not a `List`.

- `JoinCollectionsOnKey::NEED_NONABSENT_KEY`
  - emitted when any computed join key is `<Absent/>`.

- `JoinCollectionsOnKey::DUPLICATE_KEY_HIT_SNAG`
  - emitted when either side contains duplicate keys (RejectDuplicates).

### 5.6A `GroupElementsByKey`

- `GroupElementsByKey::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `GroupElementsByKey::NEED_NONABSENT_KEY`
  - emitted when any computed group key is `<Absent/>`.

### 5.7 `AnyElementSatisfies`

- `AnyElementSatisfies::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `AnyElementSatisfies::NEED_BOOLEAN`
  - emitted when the predicate expression evaluates to `Valid(x)` where `x` is not `Boolean`.

---

## 6. Relational and Predicate Codes (Normative)

### 6.1 Ordering operators

- `IsLessThan::NEED_COMPARABLE_VALUES`
  - emitted when the operands are not comparable under v0.1 Value Ordering and Structural Equality.

- `IsMoreThan::NEED_COMPARABLE_VALUES`
  - emitted when the operands are not comparable under v0.1 Value Ordering and Structural Equality.

- `IsNoLessThan::NEED_COMPARABLE_VALUES`
  - emitted when the operands are not comparable under v0.1 Value Ordering and Structural Equality.

- `IsNoMoreThan::NEED_COMPARABLE_VALUES`
  - emitted when the operands are not comparable under v0.1 Value Ordering and Structural Equality.

### 6.2 Boolean predicate composition

- `Not::NEED_BOOLEAN`
  - emitted when the operand evaluates to `Valid(x)` where `x` is not `Boolean`.

- `And::NEED_BOOLEAN`
  - emitted when any operand evaluates to `Valid(x)` where `x` is not `Boolean`.

- `Or::NEED_BOOLEAN`
  - emitted when any operand evaluates to `Valid(x)` where `x` is not `Boolean`.

---

## 7. Text Predicate Codes (Normative)

### 7.1 Pattern predicates

- `MatchesRegularExpression::INVALID_PATTERN`
  - emitted when the pattern is invalid or uses an unsupported construct under the v0.1 Regular Expression Profile.

- `DoesNotMatchRegularExpression::INVALID_PATTERN`
  - emitted when the pattern is invalid or uses an unsupported construct under the v0.1 Regular Expression Profile.

### 5.8 `AllElementsSatisfy`

- `AllElementsSatisfy::NEED_LIST`
  - emitted when the first operand is not a `List`.

- `AllElementsSatisfy::NEED_BOOLEAN`
  - emitted when the predicate expression evaluates to `Valid(x)` where `x` is not `Boolean`.

---

## 6. Math Operator Codes (Normative)

The Math operator family uses shared diagnostic codes.
These codes are referenced by the Math vocabulary specification.

### 6.1 Domain and presence

- `Math::NEED_PRESENT_NUMBER`
  - emitted when an operand is `<Absent/>` where a number is required.

- `Math::NEED_ORDERABLE_NUMBER`
  - emitted when an operand is not in `OrderableNumber`.

- `Math::NEED_REAL_NUMBER`
  - emitted when an operand is not a `RealNumber`.

- `Math::NEED_FINITE_REAL_NUMBER`
  - emitted when an operator requires a finite real value but receives a special value.

### 6.2 Division and representability

- `Math::DIVIDE_BY_ZERO`
  - emitted when a divisor is zero.

- `Math::NOT_INTEGRAL`
  - emitted when an exact-integer conversion is requested but the value is not integral.

- `Math::NOT_REPRESENTABLE`
  - emitted when an exact representation is required but cannot be achieved.

- `Math::NEED_NONNEGATIVE_SCALE`
  - emitted when a decimal scale is negative.

### 6.3 Ranges and configuration

- `Math::NEED_VALID_RANGE`
  - emitted when a minimum/maximum range is invalid.

- `Math::REAL_NUMBER_REPRESENTATION_UNSPECIFIED`
  - emitted when an operator requires a RealNumber representation contract that is not supplied.

### 6.4 Support surface

- `Math::OPERATOR_NOT_SUPPORTED`
  - emitted when a reserved Math operator is invoked but is not supported in the current conformance profile.

---

**End of Behavior Diagnostic Codes v0.1**
