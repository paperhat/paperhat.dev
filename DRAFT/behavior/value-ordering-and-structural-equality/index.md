Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Value Ordering and Structural Equality

This specification defines the canonical rules for:

- structural equality of Behavior values
- comparability and ordering of Behavior values

This document is **Normative**.

---

## 1. Purpose

Behavior is evaluated in multiple runtimes. If equality and ordering are not precisely specified, implementations will diverge in:

- set uniqueness
- map key identity
- join key matching
- stable sorting
- comparison predicates

This specification exists to remove those degrees of freedom.

---

## 2. Scope

This specification governs:

- structural equality used by:
  - Behavior equality operators
  - Set uniqueness
  - Map key identity
  - join key identity
- ordering used by:
  - Behavior ordering operators
  - `SortElementsBy`
  - Range iteration

This specification does not define:

- the full operator inventory
- coercion between unrelated domains

---

## 3. Terms

- `StructuralEquality(a, b)` returns a Boolean.
- `Compare(a, b)` returns one of: `Less`, `Equal`, `Greater`, or `NotComparable`.

---

## 4. Structural Equality (Normative)

### 4.1 Type Sensitivity

Structural equality is type-sensitive.

- Values of different top-level types MUST be structurally unequal.
- Example: `Text("1")` is not equal to `Integer(1)`.
- Example: `List([1, 2])` is not equal to `Tuple(1, 2)`.

### 4.2 Absent

- `<Absent/>` is structurally equal only to `<Absent/>`.

### 4.3 Boolean

- `Boolean` equals `Boolean` iff same truth value.

### 4.4 Text

- `Text` equals `Text` iff identical sequences of Unicode scalar values.

### 4.5 Character

- `Character` equals `Character` iff same Unicode scalar value.

### 4.6 Integer

- `Integer` equals `Integer` iff same integer value.

### 4.7 Fraction

- Two `Fraction` values are structurally equal iff their canonical normalized forms are identical.
- Canonical form: reduced (GCD = 1), positive denominator, zero represented as 0/1.

### 4.8 PrecisionNumber

- Two `PrecisionNumber` values are structurally equal iff their `decimal` representations are identical sequences of Unicode scalar values.
- `"1.0"` is NOT structurally equal to `"1.00"` (trailing zeros are significant).

### 4.9 RealNumber

- Two `RealNumber` values are structurally equal iff they represent the same IEEE 754 value.
- `NaN` is NOT structurally equal to `NaN`.
- `+0` and `-0` are structurally equal.

### 4.10 Imaginary

- Two `Imaginary` values are structurally equal iff their coefficients are structurally equal.

### 4.11 Complex

- Two `Complex` values are structurally equal iff their real parts are structurally equal AND their imaginary parts are structurally equal.

### 4.12 Special Numeric Values

- `PositiveInfinity` equals `PositiveInfinity`.
- `NegativeInfinity` equals `NegativeInfinity`.
- `NotANumber` is NOT structurally equal to anything, including itself.
- `NegativeZero` is structurally equal to positive zero (for RealNumber).

### 4.13 List

Two `List` values are structurally equal iff:
1. They have the same length, AND
2. Each pair of elements at the same index are structurally equal.

### 4.14 Set

Two `Set` values are structurally equal iff:
1. They have the same cardinality, AND
2. Every element in one is structurally equal to some element in the other.

Order is not significant for Set equality.

### 4.15 Tuple

Two `Tuple` values are structurally equal iff:
1. They have the same length, AND
2. Each pair of elements at the same position are structurally equal.

### 4.16 Map

Two `Map` values are structurally equal iff:
1. They have the same set of keys (under structural equality), AND
2. For every key, the associated values are structurally equal.

Key ordering is not significant for Map equality.

### 4.17 Record

Two `Record` values are structurally equal iff:
1. They have the same set of keys, AND
2. For every key, the associated values are structurally equal.

Key ordering is not significant for Record equality.

### 4.18 Range

Two `Range` values are structurally equal iff:
1. Their start values are structurally equal, AND
2. Their end values are structurally equal, AND
3. Their step values are structurally equal (or both absent).

### 4.19 Temporal Values

Temporal values of the same type are structurally equal iff all their components are equal.

- `PlainDate(2024, 1, 15)` equals `PlainDate(2024, 1, 15)`.
- `PlainDate(2024, 1, 15)` does NOT equal `PlainDateTime(2024, 1, 15, 0, 0, 0)` (different types).
- `PlainYearMonth(2024, 6)` equals `PlainYearMonth(2024, 6)`.
- `PlainMonthDay(12, 25)` equals `PlainMonthDay(12, 25)`.
- `YearWeek(2024, 15)` equals `YearWeek(2024, 15)`.

For `Instant` and `ZonedDateTime`:
- Comparison is by the underlying epoch time.
- Two `ZonedDateTime` values with the same instant but different time zones are structurally equal.

For `Duration`:
- Comparison is by normalized total duration.
- `P1D` equals `PT24H` (both represent the same duration).

### 4.19.1 TimeZone

- Two `TimeZone` values are structurally equal iff their IANA identifiers are identical.
- `TimeZone("America/New_York")` does NOT equal `TimeZone("US/Eastern")` even though they represent the same zone.
- No alias resolution is performed.

### 4.19.2 Calendar

- `Calendar` is an enumerated type with a fixed set of values.
- The default calendar is `iso8601`.
- Two `Calendar` values are structurally equal iff they are the same enumeration member.
- Supported calendars: `iso8601`, `gregorian`, `julian`, `hebrew`, `islamic`, `islamic-umalqura`, `islamic-civil`, `islamic-tbla`, `persian`, `indian`, `buddhist`, `chinese`, `japanese`, `coptic`, `ethiopic`, `ethiopic-amete-alem`, `roc`.

### 4.20 Color Values

Two color values are structurally equal iff:
1. They are the same color type, AND
2. All their components are equal.

Different color representations are NOT structurally equal even if they represent the same perceptual color:
- `RgbColor(255, 0, 0)` is NOT structurally equal to `HexColor("#ff0000")`.

To compare colors across representations, use explicit conversion operators.

### 4.21 Uuid

- Two `Uuid` values are structurally equal iff their canonical lowercase representations are identical.

### 4.22 IriReference

- Two `IriReference` values are structurally equal iff their string representations are identical.
- No IRI normalization is performed.

### 4.23 LookupToken

- Two `LookupToken` values are structurally equal iff their token strings are identical.

### 4.24 EnumeratedToken

- Two `EnumeratedToken` values are structurally equal iff their token identifiers are identical.

---

## 5. Ordering and Comparability (Normative)

### 5.1 Comparable Domains

Two values are comparable for ordering iff they belong to compatible domains.

#### 5.1.1 Text Ordering

- `Text` values are comparable to `Text` values.
- Ordering is lexicographic by Unicode scalar value (codepoint order).
- This is locale-independent.

#### 5.1.2 Character Ordering

- `Character` values are comparable to `Character` values.
- Ordering is by Unicode scalar value.

#### 5.1.3 Numeric Ordering (Real Numbers)

The following domains are mutually comparable:
- `Integer`
- `Fraction`
- `PrecisionNumber`

Comparison is by exact numeric value.

`RealNumber` values are comparable to each other but NOT to exact numeric types.

#### 5.1.4 Complex Number Ordering

- `Imaginary` and `Complex` values are NOT orderable.
- Attempting to order complex numbers MUST return `NotComparable`.

#### 5.1.5 Temporal Ordering

Temporal values of the same type are comparable:

- `PlainDate` values are ordered chronologically.
- `PlainTime` values are ordered by time of day.
- `PlainDateTime` values are ordered chronologically.
- `PlainYearMonth` values are ordered chronologically (year first, then month).
- `PlainMonthDay` values are ordered by month first, then day (no year context).
- `YearWeek` values are ordered chronologically (year first, then week).
- `Instant` values are ordered by epoch time.
- `ZonedDateTime` values are ordered by their underlying instant.
- `Duration` values are ordered by total duration.

Different temporal types are NOT comparable:
- `PlainDate` is NOT comparable to `PlainDateTime`.
- `PlainYearMonth` is NOT comparable to `PlainDate`.

#### 5.1.5.1 TimeZone Ordering

- `TimeZone` values are NOT orderable.
- Time zones have no inherent ordering (UTC offset varies by date).

#### 5.1.5.2 Calendar Ordering

- `Calendar` values are NOT orderable.
- Calendars are an enumerated set with no inherent ordering.

#### 5.1.6 Collection Ordering

- `List`, `Set`, `Tuple`, `Map`, `Record` are NOT orderable.
- Attempting to order collections MUST return `NotComparable`.

#### 5.1.7 Range Ordering

- `Range` values are NOT orderable.

#### 5.1.8 Color Ordering

- Color values are NOT orderable.

#### 5.1.9 Identity Types

- `Uuid`, `IriReference`, `LookupToken` are NOT orderable.

#### 5.1.10 EnumeratedToken Ordering

- `EnumeratedToken` values are NOT orderable by default.
- Schemas MAY define ordering for specific token sets.

### 5.2 Absent and Ordering

- `<Absent/>` is NOT comparable to any value for ordering operators.
- Attempting to compare `<Absent/>` MUST return `NotComparable`.

Exception for `SortElementsBy`:
- Elements whose sort key is `<Absent/>` MUST sort last.
- This is a stable sort behavior, not a comparison result.

### 5.3 Cross-Domain Numeric Comparison

For `Integer`, `Fraction`, and `PrecisionNumber`:

Define an exact rational value function R(x):
- If x is `Integer`, R(x) is that integer.
- If x is `Fraction`, R(x) is the exact rational value.
- If x is `PrecisionNumber`, R(x) is the exact rational value of the decimal.

Ordering rule:
- For any two values a and b in {Integer, Fraction, PrecisionNumber}, `Compare(a, b)` MUST be the ordering of R(a) vs R(b).

Example:
- `Integer(1)` equals `Fraction(2, 2)` for ordering purposes.
- `PrecisionNumber("0.5")` equals `Fraction(1, 2)` for ordering purposes.

Note: This cross-domain comparability applies only to ordering. Structural equality remains type-sensitive.

---

## 6. Special Cases (Normative)

### 6.1 NaN Handling

- `NotANumber` is NOT structurally equal to anything.
- `NotANumber` is NOT comparable to anything (returns `NotComparable`).

### 6.2 Infinity Handling

- `PositiveInfinity` is greater than all finite numbers.
- `NegativeInfinity` is less than all finite numbers.
- `PositiveInfinity` equals `PositiveInfinity`.
- `NegativeInfinity` equals `NegativeInfinity`.

### 6.3 Zero Handling

- For structural equality: `+0` and `-0` are equal (RealNumber domain).
- For ordering: `+0` and `-0` are equal.

---

## 7. Required Failure Behavior (Normative)

When an operator requires comparable operands and receives non-comparable operands:

- It MUST return `Invalid(...)`.
- It MUST use a diagnostic code appropriate for the operator (e.g., `IsLessThan::NEED_COMPARABLE_VALUES`).

---

## 8. Summary Tables

### 8.1 Structural Equality by Type

| Type | Equality Rule |
|------|---------------|
| Absent | Equal only to Absent |
| Boolean | Same truth value |
| Text | Identical Unicode sequence |
| Character | Same Unicode scalar |
| Integer | Same integer value |
| Fraction | Same canonical form |
| PrecisionNumber | Identical decimal string |
| RealNumber | Same IEEE 754 value (NaN never equal) |
| Imaginary | Same coefficient |
| Complex | Same real and imaginary parts |
| List | Same length, pairwise equal elements |
| Set | Same cardinality, same elements |
| Tuple | Same length, pairwise equal elements |
| Map | Same keys, same values per key |
| Record | Same keys, same values per key |
| Range | Same start, end, step |
| PlainDate | Same year, month, day |
| PlainTime | Same hour, minute, second, subsecond |
| PlainDateTime | Same date and time components |
| PlainYearMonth | Same year and month |
| PlainMonthDay | Same month and day |
| YearWeek | Same year and week |
| Instant | Same epoch time |
| ZonedDateTime | Same underlying instant |
| Duration | Same normalized total duration |
| TimeZone | Same IANA identifier (no alias resolution) |
| Calendar | Same enumeration member |
| Color | Same type and components |
| Uuid | Same canonical string |
| IriReference | Same string |
| LookupToken | Same token string |
| EnumeratedToken | Same identifier |

### 8.2 Comparability Matrix

| Type | Comparable With |
|------|-----------------|
| Text | Text |
| Character | Character |
| Integer | Integer, Fraction, PrecisionNumber |
| Fraction | Integer, Fraction, PrecisionNumber |
| PrecisionNumber | Integer, Fraction, PrecisionNumber |
| RealNumber | RealNumber |
| Imaginary | Not comparable |
| Complex | Not comparable |
| PlainDate | PlainDate |
| PlainTime | PlainTime |
| PlainDateTime | PlainDateTime |
| PlainYearMonth | PlainYearMonth |
| PlainMonthDay | PlainMonthDay |
| YearWeek | YearWeek |
| Instant | Instant |
| ZonedDateTime | ZonedDateTime |
| Duration | Duration |
| TimeZone | Not comparable |
| Calendar | Not comparable |
| List, Set, Tuple, Map, Record | Not comparable |
| Range | Not comparable |
| Color | Not comparable |
| Uuid, IriReference, LookupToken | Not comparable |
| EnumeratedToken | Not comparable (unless schema-defined) |

---

**End of Value Ordering and Structural Equality v0.1**
