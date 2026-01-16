Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Predicate, Guard, and Validation Composition Surface Specification

This specification defines the canonical surface vocabulary and determinism locks for Predicates, Guards, and their composition into Validations.

This document is **Normative**.

---

## 1. Purpose (Normative)

Paperhat needs a shared, stable vocabulary for:

- Predicates (total, diagnostic-free boolean checks)
- Guards (type/shape enforcement that may fail with diagnostics)
- Validation composition (AllOf/AnyOf/OneOf, gating, etc.)

This spec exists to prevent drift in naming and to support deterministic compilation targets (including SHACL).

Normative evaluation semantics and diagnostic behavior are defined by:

- `Validation Evaluation and Diagnostics Specification`

---

## 2. Taxonomy and Semantic Classes (Normative)

### 2.1 Predicate

A **Predicate** is a total, side-effect-free operator that:

- accepts one or more values
- returns a Boolean
- does not modify values
- does not produce diagnostics

Predicates are suitable for boolean logic, branching, and compilation targets that accept boolean constraints.

### 2.2 PredicateCombinator

A **PredicateCombinator**:

- accepts one or more Predicates
- returns a Predicate
- remains Boolean-valued

PredicateCombinators do not control validation flow.

### 2.3 Guard

A **Guard** is a value-refining validation operator.

Semantic signature:

```
Guard(value) -> Validation<Value>
```

Normative behavior:

- If the guard condition is satisfied, the result MUST be `Valid(value)` where `value` is the original input value unchanged.
- If the guard condition is not satisfied, the result MUST be `Invalid(...)` with stable diagnostic codes defined by the validation and behavior diagnostic registries.

Guards are authoritative for type and shape enforcement.
Guards do not return Boolean.

### 2.4 ValidationCombinator

A **ValidationCombinator**:

- controls when validation is applied
- is not a Predicate and is not Boolean-valued
- does not refine values

ValidationCombinators are dialect-level control constructs.


## 3. Naming Rules (Normative)

### 3.1 Casing and words

- No ALL-CAPS tokens appear in names.
- Initialisms and acronyms are treated as words using TitleCase segments (for example: `Iri`, `Url`, `Uuid`, `Isbn13`, `Ipv6`, `Mime`, `Iso8601`).

### 3.2 Predicate names

- Predicates MUST be named using `Is...` or a plain verb form that reads as a boolean property.
- Predicates MUST be total and MUST NOT yield `Invalid(...)`.

### 3.3 Guard names

- Guards MUST be named using the `Require...` prefix.
- Guards MUST either return `Valid(value)` (unchanged) or `Invalid(...)`.

### 3.4 Composition and control operators

- Boolean composition operators are named as plain operators (`Not`, `And`, `Or`, etc.).
- ValidationCombinators use `When` / `Unless`.


## 4. Canonical Predicate and Guard Vocabulary (Normative)

This section defines the canonical vocabulary inventory.

Notes:

- This section defines names only.
- Implementations MUST follow the normative evaluation rules in `Validation Evaluation and Diagnostics Specification`.

---

## 4A. Compatibility with v0.1 Behavior Dialect Operator Names (Informative)

Some existing v0.1 Behavior Dialect operators use earlier naming. This section records the preferred mapping.

Rules:

- The names in §3 are the canonical authoring surface for Predicates and Guards.
- The names in the Behavior Dialect remain the canonical runtime operator identifiers where that dialect is used.

Normalization rule (Normative):

- Tooling that renders, reformats, serializes, code-generates, or otherwise *emits* this surface MUST use the canonical spellings from §3.

Compatibility rule (Normative):

- Tooling MAY accept the Behavior Dialect spellings as input aliases when importing or interpreting existing programs.
- If tooling accepts such aliases, it MUST preserve semantics and MUST normalize them to the canonical spellings when emitting this surface.

### 4A.1 Boolean logic

- `ExclusiveOr` ↔ `Xor`

### 4A.2 Equality and ordering

- `IsNotEqualTo` ↔ `IsUnequalTo`
- `IsGreaterThan` ↔ `IsMoreThan`
- `IsGreaterThanOrEqualTo` ↔ `IsNoLessThan`
- `IsLessThanOrEqualTo` ↔ `IsNoMoreThan`

### 4A.3 Pattern matching

- `MatchesRegularExpression` ↔ `Matches`
- `DoesNotMatchRegularExpression` ↔ `DoesNotMatch`

### 4A.4 Alphabetical ordering

- `IsAlphabeticallyAfter` ↔ `IsAfterAlphabetically`
- `IsAlphabeticallyBefore` ↔ `IsBeforeAlphabetically`

Dialect-only derived operators (Informative):

- The Behavior Dialect also defines `IsNotAfterAlphabetically`, `IsNotBeforeAlphabetically`, `IsSameAlphabetically`, and `IsNotSameAlphabetically`.
- These are intentionally omitted from the canonical authoring surface because they are definable without loss using `IsAlphabeticallyBefore` / `IsAlphabeticallyAfter` plus boolean composition (`Not`, `And`, `Equivalent`).

Emission rule (Normative):

- Tooling that emits the canonical authoring surface MUST NOT emit dialect-only derived operator names.

### 4.1 Boolean logic and composition

- `Not`
- `And`
- `Or`
- `ExclusiveOr`
- `Implies`
- `Equivalent`

Quantifiers:

- `AllElementsSatisfy`
- `AnyElementSatisfies`
- `NoElementSatisfies`
- `ExactlyOneElementSatisfies`

Validation control constructs (non-predicate):

- `When`
- `Unless`

### 4.2 Presence and emptiness

Value presence:

- `IsPresent`
- `IsAbsent`

Strings:

- `IsEmptyString`
- `IsNonEmptyString`
- `IsBlankString`
- `IsNonBlankString`

Collections:

- `IsEmptyCollection`
- `IsNonEmptyCollection`

### 4.3 Equality, ordering, and relational operators

Equality:

- `IsEqualTo`
- `IsNotEqualTo`

Ordering (ordered domains only):

- `IsLessThan`
- `IsLessThanOrEqualTo`
- `IsGreaterThan`
- `IsGreaterThanOrEqualTo`

Ranges:

- `IsBetweenInclusive`
- `IsBetweenExclusive`
- `IsOutsideInclusive`
- `IsOutsideExclusive`

Set membership:

- `IsOneOf`
- `IsNotOneOf`

Uniqueness:

- `AllElementsAreDistinct`
- `ContainsNoDuplicates`

### 4.4 Core type predicates and guards

Predicates:

- `IsBoolean`
- `IsInteger`
- `IsRealNumber`
- `IsString`
- `IsBinaryData`

Temporal:

- `IsDate`
- `IsTime`
- `IsDateTime`
- `IsDuration`

Guards:

- `RequireBoolean`
- `RequireInteger`
- `RequireRealNumber`
- `RequireString`
- `RequireBinaryData`
- `RequireDate`
- `RequireTime`
- `RequireDateTime`
- `RequireDuration`

### 4.5 Numeric predicates

Sign and zero:

- `IsZero`
- `IsPositive`
- `IsNegative`
- `IsNonPositive`
- `IsNonNegative`

Parity and divisibility (integers):

- `IsEven`
- `IsOdd`
- `IsDivisibleBy`

Real-number classification:

- `IsNotANumber`
- `IsFinite`
- `IsInfinite`
- `IsPositiveInfinity`
- `IsNegativeInfinity`

Approximate equality:

- `IsApproximatelyEqual`

### 4.6 String predicates

Length:

- `HasLengthEqualTo`
- `HasLengthAtLeast`
- `HasLengthAtMost`
- `HasLengthBetweenInclusive`

Containment:

- `ContainsSubstring`
- `StartsWithSubstring`
- `EndsWithSubstring`

Character classes:

- `ContainsOnlyLetters`
- `ContainsOnlyDigits`
- `ContainsOnlyLettersAndDigits`
- `ContainsOnlyWhitespace`
- `ContainsOnlyPrintableCharacters`

Case:

- `IsUppercase`
- `IsLowercase`
- `IsTitleCase`
- `IsCaseInsensitiveEqualTo`

Deterministic ordering:

- `IsAlphabeticallyBefore`
- `IsAlphabeticallyAfter`

Patterns:

- `MatchesRegularExpression`
- `DoesNotMatchRegularExpression`

### 4.7 Temporal predicates

Ordering:

- `IsEarlierThan`
- `IsEarlierThanOrEqualTo`
- `IsLaterThan`
- `IsLaterThanOrEqualTo`

Ranges:

- `IsWithinInclusive`
- `IsWithinExclusive`

Proximity:

- `IsWithinDuration`
- `IsAtLeastDurationApart`
- `IsAtMostDurationApart`

### 4.8 Identifier and structured-string predicates

Web identifiers:

- `IsIri`
- `IsIriReference`
- `IsIriAbsolute`
- `IsIriRelativeReference`
- `IsUri`
- `IsUrl`
- `IsUrn`

Universal identifiers:

- `IsUuid`

Publishing identifiers:

- `IsIsbn10`
- `IsIsbn13`
- `IsIssn`

Networking:

- `IsIpv4Address`
- `IsIpv6Address`
- `IsIpAddress`
- `IsDomainName`
- `IsHostName`

Media / content types:

- `IsMimeType`

Language tags:

- `IsLanguageTag`
- `IsBcp47LanguageTag`

Encodings:

- `IsBase64String`
- `IsHexString`

Email:

- `IsEmailAddress`

Lexical date/time:

- `IsIso8601DateString`
- `IsIso8601DateTimeString`
- `IsIso8601DurationString`

### 4.9 Collection predicates

Size:

- `HasElementCountEqualTo`
- `HasElementCountAtLeast`
- `HasElementCountAtMost`
- `HasElementCountBetweenInclusive`

Membership:

- `ContainsElement`
- `DoesNotContainElement`

Key/value maps:

- `ContainsKey`
- `DoesNotContainKey`
- `AllKeysSatisfy`
- `AllValuesSatisfy`

### 4.10 Rdf and Shacl-aligned predicates

Node kind:

- `IsIriNode`
- `IsBlankNode`
- `IsLiteralNode`

Literal datatypes:

- `IsStringLiteral`
- `IsIntegerLiteral`
- `IsDecimalLiteral`
- `IsBooleanLiteral`
- `IsDateLiteral`
- `IsDateTimeLiteral`
- `IsDurationLiteral`

Language-tagged strings:

- `IsLanguageTaggedStringLiteral`
- `HasLanguageTag`
- `HasLanguageTagMatching`

Property cardinality:

- `HasAtLeastPropertyValueCount`
- `HasAtMostPropertyValueCount`
- `HasExactlyPropertyValueCount`

Value sets:

- `HasOnlyAllowedValues`
- `HasNoDisallowedValues`

---

## 5. Determinism Profiles (Normative)

This section locks the semantic profiles that prevent drift across implementations.

### 5.1 Regular expression profile for `MatchesRegularExpression`

`MatchesRegularExpression` and `DoesNotMatchRegularExpression` MUST use the Paperhat Regular Expression Profile 0.1, defined by [Regular Expression Profile](../regular-expression-profile/).

### 5.2 Collation profile for alphabetical ordering

`IsAlphabeticallyBefore` and `IsAlphabeticallyAfter` MUST compare Text using:

1. Unicode Normalization Form C applied to both strings, then
2. Unicode scalar value (code point) order on the normalized strings.

Comparison MUST be locale-independent and MUST be case-sensitive.

### 5.3 Whitespace profile

For `IsBlankString`, `IsNonBlankString`, and `ContainsOnlyWhitespace`, whitespace is exactly the following Unicode scalar values:

- U+0009..U+000D
- U+0020
- U+0085
- U+00A0
- U+1680
- U+2000..U+200A
- U+2028
- U+2029
- U+202F
- U+205F
- U+3000

No other code points are whitespace for these predicates.

### 5.4 Date/time lexical form profile

All “Iso8601” lexical predicates are RFC 3339 profiled.

- `IsIso8601DateString` MUST accept only `YYYY-MM-DD`.
- `IsIso8601DateTimeString` MUST accept only `YYYY-MM-DDTHH:MM:SS` with optional fractional seconds, and a REQUIRED timezone designator of `Z` or `±HH:MM`.
- `IsIso8601DurationString` MUST accept only the ISO 8601 duration lexical form defined by this grammar:

```
duration := 'P' date_part [ 'T' time_part ]
date_part := [ number 'Y' ] [ number 'M' ] [ number 'D' ]
time_part := [ number 'H' ] [ number 'M' ] [ number 'S' ]
number := one_or_more_digits [ '.' one_or_more_digits ]
```

An implementation MUST reject any duration string that does not match this grammar exactly.

---

## 6. Evaluation and Equality Locks (Normative)

### 6.1 Predicate totality

Predicates are total over values.

- A Predicate MUST yield `true` or `false` for any input value (including `<Absent/>`).
- A Predicate MUST NOT itself produce diagnostics.

### 6.2 PredicateCombinator determinism

PredicateCombinators MUST be referentially transparent.

- Because Predicates are total and diagnostic-free, the boolean result of a PredicateCombinator MUST be independent of evaluation order.
- Implementations MAY short-circuit or evaluate eagerly.

### 6.3 Presence model

`<Absent/>` is the canonical missing-value concept.

- `IsAbsent(value)` MUST be `true` iff `value` is `<Absent/>`.
- `IsPresent(value)` MUST be `true` iff `value` is not `<Absent/>`.
- Empty strings and empty collections are present.

### 6.4 Equality reuse

`IsEqualTo` MUST use structural equality as defined by `Value Ordering and Structural Equality`.

All equality-dependent predicates (including `IsOneOf`, `ContainsElement`, distinctness checks, and key membership) MUST use `IsEqualTo` equality.

---

## 7. Special Numeric Value Locks (Normative)

Special numeric values are concept-identifiable.

- `IsNotANumber(value)` MUST be `true` iff `value` is `<NotANumber />`.
- `IsPositiveInfinity(value)` MUST be `true` iff `value` is `<PositiveInfinity />`.
- `IsNegativeInfinity(value)` MUST be `true` iff `value` is `<NegativeInfinity />`.

Negative zero classification is locked:

- `IsZero(<NegativeZero />)` MUST be `true`.
- `IsNegative(<NegativeZero />)` MUST be `false`.
- `IsPositive(<NegativeZero />)` MUST be `false`.
- `IsNonNegative(<NegativeZero />)` MUST be `true`.
- `IsNonPositive(<NegativeZero />)` MUST be `true`.

Approximate equality arity is locked:

- `IsApproximatelyEqual(left, right, absoluteTolerance, relativeTolerance)` is the only permitted surface.
- Tolerances MUST be non-negative.
- Semantics MUST match `Behavior Vocabulary — Math`.

---

## 8. Unicode Locks for String Predicates (Normative)

All string predicates operate on sequences of Unicode scalar values.

Where this spec defines a profile by Unicode property (letters, digits, casing), implementations MUST use a single fixed Unicode Character Database version for v0.1 conformance.
The v0.1 conformance suite is co-normative and defines the test vectors that lock this behavior.

Case-insensitive equality is locked:

- `IsCaseInsensitiveEqualTo(a, b)` MUST be `true` iff `SimpleCaseFold(a) == SimpleCaseFold(b)`.
- Case folding MUST be locale-independent.
- No additional normalization is applied unless stated by the collation profile.

---

## 9. Conformance and Rejection Phase (Normative)

### 9.1 Closed-world rule

- The vocabulary defined by this spec is closed-world for v0.1.
- Any construct that uses an undefined operator name is invalid and MUST be rejected.

### 9.2 Rejection timing

An implementation MUST reject violations at the earliest phase in which they are detectable (parse-time when syntactic, otherwise compile-time).
Violations MUST NOT be deferred to runtime when they are statically detectable.

---

**End of Predicate, Guard, and Validation Composition Surface Specification v0.1**
