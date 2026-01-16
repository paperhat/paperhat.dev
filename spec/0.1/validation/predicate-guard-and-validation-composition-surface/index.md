Status: NORMATIVE  
Lock State: DRAFT (candidate for LOCKED)  
Version: 0.1  
Editor: Charles F. Munat

# Predicate, Guard, and Validation Composition Surface Specification

This specification defines the canonical **name surface** for Predicates, Guards, and their composition into Validations.

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

## 2. Naming Rules (Normative)

### 2.1 Casing and words

- No ALL-CAPS tokens appear in names.
- Initialisms and acronyms are treated as words using TitleCase segments (for example: `Iri`, `Url`, `Uuid`, `Isbn13`, `Ipv6`, `Json`, `Mime`, `Iso8601`).

### 2.2 Predicate names

- Predicates MUST be named using `Is...` or a plain verb form that reads as a boolean property.
- Predicates MUST be total and MUST NOT yield `Invalid(...)`.

### 2.3 Guard names

- Guards MUST be named using the `Require...` prefix.
- Guards MUST either return `Valid(value)` (unchanged) or `Invalid(...)`.

### 2.4 Composition and control operators

- Boolean composition operators are named as plain operators (`Not`, `And`, `Or`, etc.).
- Conditional enforcement operators use `When` / `Unless`.

---

## 3. Canonical Predicate and Guard Vocabulary (Normative)

This section defines the canonical vocabulary inventory.

Notes:

- This section defines names only.
- Implementations MUST follow the normative evaluation rules in `Validation Evaluation and Diagnostics Specification`.

---

## 3A. Compatibility with v0.1 Behavior Dialect Operator Names (Informative)

Some existing v0.1 Behavior Dialect operators use earlier naming. This section records the preferred mapping.

Rules:

- The names in §3 are the canonical authoring surface for Predicates and Guards.
- The names in the Behavior Dialect remain the canonical runtime operator identifiers where that dialect is used.

Normalization rule (Normative):

- Tooling that renders, reformats, serializes, code-generates, or otherwise *emits* this surface MUST use the canonical spellings from §3.

Compatibility rule (Normative):

- Tooling MAY accept the Behavior Dialect spellings as input aliases when importing or interpreting existing programs.
- If tooling accepts such aliases, it MUST preserve semantics and MUST normalize them to the canonical spellings when emitting this surface.

### 3A.1 Boolean logic

- `ExclusiveOr` ↔ `Xor`

### 3A.2 Equality and ordering

- `IsNotEqualTo` ↔ `IsUnequalTo`
- `IsGreaterThan` ↔ `IsMoreThan`
- `IsGreaterThanOrEqualTo` ↔ `IsNoLessThan`
- `IsLessThanOrEqualTo` ↔ `IsNoMoreThan`

### 3A.3 Pattern matching

- `MatchesRegularExpression` ↔ `Matches`
- `DoesNotMatchRegularExpression` ↔ `DoesNotMatch`

### 3A.4 Alphabetical ordering

- `IsAlphabeticallyAfter` ↔ `IsAfterAlphabetically`
- `IsAlphabeticallyBefore` ↔ `IsBeforeAlphabetically`

### 3.1 Boolean logic and composition

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

Conditional enforcement:

- `When`
- `Unless`

### 3.2 Presence and emptiness

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

### 3.3 Equality, ordering, and relational operators

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

### 3.4 Core type predicates and guards

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

### 3.5 Numeric predicates

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

### 3.6 String predicates

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

### 3.7 Temporal predicates

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

### 3.8 Identifier and structured-string predicates

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

Json-related:

- `IsJsonPointer`
- `IsJson`

Email:

- `IsEmailAddress`

Lexical date/time:

- `IsIso8601DateString`
- `IsIso8601DateTimeString`
- `IsIso8601DurationString`

### 3.9 Collection predicates

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

### 3.10 Rdf and Shacl-aligned predicates

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

## 4. Locks Recommended for Stability (DRAFT)

1. Prefer `IsLanguageTag` as the surface name; treat Bcp47 as the locked profile in prose semantics.
2. Decide whether `IsIpAddress` is a supported umbrella predicate, or only the explicit `IsIpv4Address` / `IsIpv6Address` predicates.

---

**End of Predicate, Guard, and Validation Composition Surface Specification v0.1**
