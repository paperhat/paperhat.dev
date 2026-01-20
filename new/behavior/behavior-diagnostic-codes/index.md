Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Diagnostic Codes

This specification defines the canonical diagnostic code set for **Behavior evaluation and decoding**.

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

---

## 3. General Rules (Normative)

1. When a Behavior construct is specified to return `Invalid(...)` for a particular condition, it MUST emit the corresponding code from this registry.
2. When a Behavior construct propagates an operand's `Invalid(...)`, it MUST NOT wrap or replace the operand's codes.
3. Implementations MAY add additional diagnostics, but MUST NOT omit the required diagnostic for the condition.

---

## 4. Program Encoding Codes (Normative)

### 4.1 BehaviorProgramEncoding

- `BehaviorProgramEncoding::TAG_NOT_UNDERSTOOD` — unknown `@paperhat` concept
- `BehaviorProgramEncoding::INTEGER_NOT_UNDERSTOOD` — malformed Integer encoding
- `BehaviorProgramEncoding::FRACTION_NOT_UNDERSTOOD` — malformed Fraction encoding
- `BehaviorProgramEncoding::PRECISIONNUMBER_NOT_UNDERSTOOD` — malformed PrecisionNumber encoding
- `BehaviorProgramEncoding::COMPLEX_NOT_UNDERSTOOD` — malformed Complex encoding
- `BehaviorProgramEncoding::IMAGINARY_NOT_UNDERSTOOD` — malformed Imaginary encoding
- `BehaviorProgramEncoding::TEMPORAL_NOT_UNDERSTOOD` — malformed temporal encoding
- `BehaviorProgramEncoding::COLOR_NOT_UNDERSTOOD` — malformed color encoding
- `BehaviorProgramEncoding::OPERATION_NOT_UNDERSTOOD` — unknown operation token
- `BehaviorProgramEncoding::NEED_NAME` — missing `name` field
- `BehaviorProgramEncoding::NEED_INDEX` — missing `index` field
- `BehaviorProgramEncoding::NEED_STEPS` — missing `steps` field
- `BehaviorProgramEncoding::NEED_VALUE` — missing `value` field
- `BehaviorProgramEncoding::NEED_ARGUMENTS` — missing `arguments` field
- `BehaviorProgramEncoding::VERSION_MISMATCH` — unsupported version

---

## 5. Core Safe Transform Codes (Normative)

### 5.1 Shared

- `CoreSafeTransforms::LIMIT_EXCEEDED` — resource limit exceeded

### 5.2 List Operations

- `MapElements::NEED_LIST`
- `FilterElements::NEED_LIST`
- `FilterElements::NEED_BOOLEAN`
- `ReduceElements::NEED_LIST`
- `FoldElements::NEED_LIST`
- `FoldElements::NEED_NONEMPTY_LIST`
- `FindFirstElement::NEED_LIST`
- `FindFirstElement::NEED_BOOLEAN`
- `FindLastElement::NEED_LIST`
- `FindLastElement::NEED_BOOLEAN`
- `FindAllElements::NEED_LIST`
- `FindAllElements::NEED_BOOLEAN`
- `SortElements::NEED_LIST`
- `SortElements::NEED_COMPARABLE_ELEMENTS`
- `SortElementsBy::NEED_LIST`
- `SortElementsBy::NEED_COMPARABLE_KEYS`
- `TakeFirstElements::NEED_LIST`
- `TakeFirstElements::NEED_INTEGER_COUNT`
- `TakeFirstElements::NEED_NONNEGATIVE_COUNT`
- `DropFirstElements::NEED_LIST`
- `DropFirstElements::NEED_INTEGER_COUNT`
- `DropFirstElements::NEED_NONNEGATIVE_COUNT`
- `DistinctElements::NEED_LIST`
- `FlattenElements::NEED_LIST`
- `FlattenElements::NEED_LIST_ELEMENTS`
- `ZipElements::NEED_LIST`
- `ChunkElements::NEED_LIST`
- `ChunkElements::NEED_POSITIVE_SIZE`
- `WindowElements::NEED_LIST`
- `WindowElements::NEED_POSITIVE_SIZE`
- `SliceElements::NEED_LIST`
- `SliceElements::NEED_INTEGER_INDEX`
- `PartitionElements::NEED_LIST`
- `PartitionElements::NEED_BOOLEAN`
- `GroupElementsByKey::NEED_LIST`
- `GroupElementsByKey::NEED_NONABSENT_KEY`

### 5.3 Aggregation

- `CountElements::NEED_LIST`
- `SumElements::NEED_LIST`
- `SumElements::NEED_NUMERIC_ELEMENTS`
- `ProductElements::NEED_LIST`
- `ProductElements::NEED_NUMERIC_ELEMENTS`
- `MinimumElement::NEED_LIST`
- `MinimumElement::NEED_NONABSENT_ELEMENTS`
- `MinimumElement::NEED_COMPARABLE_ELEMENTS`
- `MaximumElement::NEED_LIST`
- `MaximumElement::NEED_NONABSENT_ELEMENTS`
- `MaximumElement::NEED_COMPARABLE_ELEMENTS`
- `AverageElements::NEED_LIST`
- `AverageElements::NEED_NONEMPTY_LIST`
- `AverageElements::NEED_NUMERIC_ELEMENTS`

### 5.4 Predicates

- `AnyElementSatisfies::NEED_LIST`
- `AnyElementSatisfies::NEED_BOOLEAN`
- `AllElementsSatisfy::NEED_LIST`
- `AllElementsSatisfy::NEED_BOOLEAN`
- `NoElementSatisfies::NEED_LIST`
- `NoElementSatisfies::NEED_BOOLEAN`

### 5.5 Set Operations

- `SetUnion::NEED_SET`
- `SetIntersection::NEED_SET`
- `SetDifference::NEED_SET`
- `SetSymmetricDifference::NEED_SET`
- `IsSubsetOf::NEED_SET`
- `IsSupersetOf::NEED_SET`
- `SetAdd::NEED_SET`
- `SetRemove::NEED_SET`
- `ListToSet::NEED_LIST`

### 5.6 Map Operations

- `MapGet::NEED_MAP`
- `MapSet::NEED_MAP`
- `MapRemove::NEED_MAP`
- `MapMerge::NEED_MAP`
- `MapMergeWith::NEED_MAP`
- `MapMapValues::NEED_MAP`
- `MapFilterEntries::NEED_MAP`
- `MapFilterEntries::NEED_BOOLEAN`
- `MapFromEntries::NEED_LIST`
- `MapFromEntries::DUPLICATE_KEY`
- `MapFromEntries::NEED_RECORD_ENTRIES`
- `MapFromLists::NEED_LIST`
- `MapFromLists::LENGTH_MISMATCH`
- `MapFromLists::DUPLICATE_KEY`
- `MapContainsKey::NEED_MAP`

### 5.7 Record Operations

- `RecordGet::NEED_RECORD`
- `RecordSet::NEED_RECORD`
- `RecordRemove::NEED_RECORD`
- `RecordMerge::NEED_RECORD`
- `SelectFields::NEED_RECORD`
- `SelectFields::NEED_LIST`
- `SelectFields::NEED_TEXT_FIELD_NAMES`
- `SelectFields::NEED_DISTINCT_FIELD_NAMES`
- `OmitFields::NEED_RECORD`
- `OmitFields::NEED_LIST`
- `RecordFromMap::NEED_MAP`
- `RecordFromMap::NEED_TEXT_KEYS`

### 5.8 Tuple Operations

- `TupleGet::NEED_TUPLE`
- `TupleGet::INDEX_OUT_OF_BOUNDS`
- `TupleToList::NEED_TUPLE`
- `ListToTuple::NEED_LIST`

### 5.9 Range Operations

- `RangeToList::NEED_RANGE`
- `RangeContains::NEED_RANGE`
- `MakeRange::INCOMPATIBLE_TYPES`
- `MakeRange::NEED_POSITIVE_STEP`

### 5.10 Join Operations

- `JoinCollectionsOnKey::NEED_LIST`
- `JoinCollectionsOnKey::NEED_NONABSENT_KEY`
- `JoinCollectionsOnKey::DUPLICATE_KEY`

### 5.11 String Operations

- `SplitString::NEED_TEXT`
- `SplitString::NEED_TEXT_SEPARATOR`
- `SplitString::NEED_NONEMPTY_SEPARATOR`
- `JoinStrings::NEED_LIST`
- `JoinStrings::NEED_TEXT_SEPARATOR`
- `JoinStrings::NEED_TEXT_ELEMENTS`

---

## 6. Math Codes (Normative)

### 6.1 Domain and Presence

- `Math::NEED_PRESENT_NUMBER` — `<Absent/>` where number required
- `Math::NEED_ORDERABLE_NUMBER` — not in OrderableNumber
- `Math::NEED_REAL_NUMBER` — not a real number
- `Math::NEED_COMPLEX_NUMBER` — not a complex number
- `Math::NEED_INTEGER` — not an integer
- `Math::NEED_POSITIVE` — not positive
- `Math::NEED_NONNEGATIVE` — not non-negative
- `Math::NEED_FINITE` — not finite

### 6.2 Operations

- `Math::DIVIDE_BY_ZERO`
- `Math::NOT_INTEGRAL` — conversion to integer failed
- `Math::NOT_REPRESENTABLE` — exact representation not possible
- `Math::NEED_NONNEGATIVE_SCALE` — negative decimal scale
- `Math::NEED_VALID_RANGE` — invalid min/max range
- `Math::DOMAIN_ERROR` — input outside mathematical domain
- `Math::OVERFLOW` — result too large
- `Math::UNDERFLOW` — result too small

### 6.3 Linear Algebra

- `LinearAlgebra::NEED_LIST` — not a vector/matrix
- `LinearAlgebra::DIMENSION_MISMATCH` — incompatible dimensions
- `LinearAlgebra::NEED_SQUARE_MATRIX` — square matrix required
- `LinearAlgebra::SINGULAR_MATRIX` — matrix is singular
- `LinearAlgebra::NOT_POSITIVE_DEFINITE` — Cholesky requires positive definite

### 6.4 Statistics

- `Statistics::NEED_NONEMPTY_LIST`
- `Statistics::NEED_NUMERIC_ELEMENTS`
- `Statistics::NEED_SAME_LENGTH_LISTS`
- `Statistics::NEED_VALID_QUANTILE` — quantile not in [0,1]
- `Statistics::NEED_VALID_PERCENTILE` — percentile not in [0,100]

### 6.5 Calculus

- `Calculus::CONVERGENCE_FAILED` — numerical method did not converge
- `Calculus::NEED_BEHAVIOR_EXPRESSION` — function argument required

---

## 7. Relational and Predicate Codes (Normative)

- `IsLessThan::NEED_COMPARABLE_VALUES`
- `IsMoreThan::NEED_COMPARABLE_VALUES`
- `IsNoLessThan::NEED_COMPARABLE_VALUES`
- `IsNoMoreThan::NEED_COMPARABLE_VALUES`
- `Not::NEED_BOOLEAN`
- `And::NEED_BOOLEAN`
- `Or::NEED_BOOLEAN`

---

## 8. Text Codes (Normative)

- `Text::NEED_TEXT`
- `Text::NEED_CHARACTER`
- `Text::INDEX_OUT_OF_BOUNDS`
- `Text::INVALID_REGEX_PATTERN`
- `Text::INVALID_ENCODING`
- `Text::INVALID_BASE64`
- `Text::INVALID_HEX`

---

## 9. Temporal Codes (Normative)

- `Temporal::INVALID_DATE` — invalid date components
- `Temporal::INVALID_TIME` — invalid time components
- `Temporal::INVALID_DATETIME` — invalid datetime components
- `Temporal::INVALID_DURATION` — invalid duration
- `Temporal::INVALID_TIMEZONE` — unknown timezone identifier
- `Temporal::INVALID_FORMAT` — cannot parse temporal string
- `Temporal::AMBIGUOUS_TIME` — DST ambiguity without disambiguation
- `Temporal::NEED_TEMPORAL` — not a temporal type
- `Temporal::NEED_SAME_TYPE` — temporal types must match
- `Temporal::NEED_INSTANT` — Instant required
- `Temporal::NEED_DURATION` — Duration required
- `Temporal::NEED_TIMEZONE` — TimeZone required

---

## 10. Color Codes (Normative)

- `Color::UNKNOWN_COLOR_NAME` — unrecognized named color
- `Color::INVALID_COLOR_STRING` — cannot parse color string
- `Color::INVALID_HEX_COLOR` — invalid hex color format
- `Color::OUT_OF_GAMUT` — color outside specified gamut
- `Color::NEED_COLOR` — not a color type
- `Color::INVALID_BLEND_MODE` — unknown blend mode
- `Color::INVALID_COLOR_SPACE` — unknown color space

---

## 11. Identity Codes (Normative)

- `Identity::INVALID_UUID` — invalid UUID format
- `Identity::NOT_TIME_BASED_UUID` — UUID is not time-based
- `Identity::INVALID_IRI` — invalid IRI format
- `Identity::INVALID_LOOKUP_TOKEN` — invalid lookup token format
- `Identity::INVALID_ENUMERATED_TOKEN` — invalid enumerated token format

---

## 12. Data Shapes and Validation Codes (Normative)

- `AllKeysSatisfy::NEED_RECORD`
- `AllKeysSatisfy::NEED_BOOLEAN`
- `AllValuesSatisfy::NEED_RECORD`
- `AllValuesSatisfy::NEED_BOOLEAN`
- `HasElementCountEqualTo::NEED_COLLECTION`
- `HasElementCountAtLeast::NEED_COLLECTION`
- `HasElementCountAtMost::NEED_COLLECTION`
- `ContainsElement::NEED_COLLECTION`
- `ContainsKey::NEED_MAP_OR_RECORD`

---

**End of Behavior Diagnostic Codes v0.1**
