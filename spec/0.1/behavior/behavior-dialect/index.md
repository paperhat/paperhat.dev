Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Dialect

This specification defines the **Behavior Dialect** for Paperhat.

The Behavior Dialect is a declarative expression language authored in Codex, compiled by Kernel, and executed in multiple runtimes (native and HTML runtime).

This document is **Normative**.

---

## 1. Purpose

This spec exists to define:

- the canonical evaluation model for Behavior expressions
- operator arity requirements
- operator signature families (typing rules)
- determinism, purity, and error/diagnostic rules

This spec does not define:

- the interchange encoding (see Behavior Program Encoding spec)
- where expressions attach (see Behavior Attachment spec)
- target-specific UI semantics (owned by runtimes/renderers)

---

## 2. Core Principles (Normative)

1. **Purity:** Behavior evaluation MUST be side-effect free.
2. **Determinism:** Given the same program and explicit inputs, evaluation MUST produce the same result.
3. **Target neutrality:** Operators MUST NOT depend on HTML/DOM/PDF/spreadsheet assumptions.
4. **No ambient dependencies:** Evaluation MUST NOT consult time, randomness, filesystem, or network.

Additional safety boundary (Normative):

5. **No dynamic code construction:** Strings are data, never code. A Behavior Program MUST NOT contain or cause:
   - dynamic operator selection (no “operator name from string”)
   - executable data-as-AST (no “evaluate user-provided graph as code”)
   - query-as-string (no SPARQL embedded as a string literal for execution)

Clarification (Normative):

- Paperhat MAY depend on time, randomness, or I/O as *system behavior*.
- Behavior evaluation itself MUST remain deterministic; therefore time/randomness/I/O MUST be supplied as explicit inputs (for example via `Environment` bindings in a Presentation Plan attachment).

---

## 3. Runtime-Neutral Result Model (Normative)

All Behavior evaluation produces a `Validation`.

- `Valid(value)`
- `Invalid(diagnostics)`

A Behavior evaluator MUST NOT throw for user-authored input; it MUST return `Invalid(...)` with diagnostics.

This rule applies to:

- Kernel evaluation
- HTML runtime evaluation

---

## 4. Values and Types (Normative)

Behavior values are **Codex concepts**, not JSON values.

Normative missingness rule:

- v0.1 defines a single canonical missing-value concept: `<Absent/>`.
- v0.1 MUST NOT introduce any semantic `Null` value.

The canonical value model and its determinism rules are defined by:

- Behavior Dialect Semantics (Value Model)

---

## 5. Reserved Operators (Normative)

The following operators are reserved and their intent is fixed:

- `Argument` — the primary input value
- `Variable(name)` — environment lookup
- `Constant(value)` — literal constant
- `Field(name)` — field lookup on a Record-like value
- `Path(steps...)` — bounded path traversal

Encoding is defined by the Behavior Program Encoding spec.

Typing rules:

- `Argument` is dynamically typed (type is determined by caller context)
- `Variable` is dynamically typed (type is determined by the bound value)
- `Constant` has the type implied by the literal value concept

---

## 6. Environment and Missing Variables (Normative)

If `Variable(name)` is evaluated and `name` is missing in the environment, the result MUST be:

- `Invalid([...])`

The diagnostic MUST identify the missing variable name.

Evaluators MUST NOT substitute default values for missing variables.

## 6.1 External Inputs (Time, Randomness, I/O) (Normative)

Paperhat supports time-dependent, random, and I/O-driven behavior by treating the *results* of those operations as explicit inputs to Behavior.

Rules:

1. Behavior MUST NOT contain operations that consult ambient time, randomness, filesystem, or network.
2. If time is needed (for example to validate temporal bounds), the relevant time value MUST be supplied as an explicit input.
3. If randomness is needed (for example UUID generation), the generated value MUST be supplied as an explicit input.
4. If I/O is needed (for example a lookup), the looked-up value MUST be supplied as an explicit input.

This keeps evaluation deterministic while still allowing systems to incorporate effectful sources.

## 6.2 Runtime Tagged Types (Normative)

Implementations MAY represent values using runtime tagged types internally (for example, distinct internal representations for `PrecisionNumber`, `Amount`, or temporal values), in order to perform:

- runtime type checking
- lossless normalization
- domain-safe operations

However:

1. Interchange values embedded in Behavior Programs MUST remain pure data (see Behavior Program Encoding).
2. Observable Behavior semantics MUST be consistent across runtimes (Kernel and HTML runtime).
3. Any internal tagging MUST NOT leak target-specific implementation assumptions.

---

## 7. Operator Application (Normative)

An operator application node has:

- an operator identifier (a stable token naming a Behavior Vocabulary concept)
- zero or more arguments (expressions)

Rules:

1. Arity MUST be validated. Violations MUST produce `Invalid([...])`.
2. If any argument evaluates to `Invalid`, the operator MUST either:
   - propagate `Invalid` (default), OR
   - handle it explicitly if defined by the operator’s semantics.

Unless otherwise specified, operators MUST propagate `Invalid`.

---

## 8. Evaluation Order (Normative)

Evaluation order MUST be deterministic.

Unless an operator defines short-circuiting semantics, arguments MUST be evaluated left-to-right.

---

## 9. Logical Operators (Normative)

### 9.1 `Not`

Arity: 1

Signature:

- `Not(Validation<boolean>) -> Validation<boolean>`

Semantics:

- `Valid(true)`  -> `Valid(false)`
- `Valid(false)` -> `Valid(true)`
- `Invalid(d)`   -> `Invalid(d)`

### 9.2 `And`

Arity: 2 or more

Signature:

- `And(Validation<boolean>...) -> Validation<boolean>`

Semantics:

- Evaluate arguments left-to-right.
- If any argument is `Valid(false)`, return `Valid(false)`.
- If an argument is `Invalid(...)` and no earlier argument was `Valid(false)`, return `Invalid(...)`.
- If all arguments are `Valid(true)`, return `Valid(true)`.

### 9.3 `Or`

Arity: 2 or more

Signature:

- `Or(Validation<boolean>...) -> Validation<boolean>`

Semantics:

- Evaluate arguments left-to-right.
- If any argument is `Valid(true)`, return `Valid(true)`.
- If no argument is `Valid(true)` and any argument is `Invalid(...)`, return `Invalid(...)`.
- If all arguments are `Valid(false)`, return `Valid(false)`.

### 9.4 `Xor`

Arity: 2

Signature:

- `Xor(Validation<boolean>, Validation<boolean>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise return `Valid(a != b)`.

### 9.5 `Ternary`

Arity: 3

Signature:

- `Ternary(Validation<boolean>, Validation<T>, Validation<T>) -> Validation<T>`

Semantics:

- If condition is `Valid(true)`, return the then-branch.
- If condition is `Valid(false)`, return the else-branch.
- If condition is `Invalid`, return `Invalid`.

---

## 10. Equality and Comparison Families (Normative)

### 10.1 Equality

Operators:

- `IsEqualTo`
- `IsUnequalTo`

Arity: 2

Signatures:

- `IsEqualTo(Validation<any>, Validation<any>) -> Validation<boolean>`
- `IsUnequalTo(Validation<any>, Validation<any>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise compare values for structural equality.

### 10.2 Ordering

Operators:

- `IsLessThan`
- `IsMoreThan`
- `IsNoLessThan`
- `IsNoMoreThan`

Arity: 2

Signatures:

- `OrderingOp(Validation<T>, Validation<T>) -> Validation<boolean>` where `T` is comparable.

Comparable sets in v0.1:

- numbers compare numerically
- strings compare by Unicode codepoint order

If types do not match or are not comparable, the result MUST be `Invalid([...])`.

---

## 11. Type Guard Families (Normative)

Operators:

- `IsBoolean`
- `IsNumber`
- `IsString`
- `IsInteger`

Arity: 1

Signatures:

- `TypeGuard(Validation<any>) -> Validation<boolean>`

Semantics:

- If the input is `Invalid`, return `Invalid`.
- Otherwise return `Valid(true)` or `Valid(false)`.

`IsInteger` MUST return `Valid(true)` only when the value is a `Number` with no fractional component.

---

## 12. Pattern Matching Families (Normative)

Operators:

- `Matches`
- `DoesNotMatch`

Arity: 2

Signatures:

- `Matches(Validation<string>, Validation<string>) -> Validation<boolean>`
- `DoesNotMatch(Validation<string>, Validation<string>) -> Validation<boolean>`

The pattern language for v0.1 MUST conform to the v0.1 Regular Expression Profile.

If the pattern is invalid or uses an unsupported construct, the result MUST be `Invalid([...])`.

---

## 13. Alphabetical Relations (Normative)

Operators:

- `IsAfterAlphabetically`
- `IsBeforeAlphabetically`
- `IsNotAfterAlphabetically`
- `IsNotBeforeAlphabetically`
- `IsSameAlphabetically`
- `IsNotSameAlphabetically`

Arity: 2

Signatures:

- `AlphabeticalOp(Validation<string>, Validation<string>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise compare strings by Unicode codepoint order.

Mapping:

- `IsAfterAlphabetically(a,b)` is `a > b`
- `IsBeforeAlphabetically(a,b)` is `a < b`
- `IsNotAfterAlphabetically(a,b)` is `a <= b`
- `IsNotBeforeAlphabetically(a,b)` is `a >= b`
- `IsSameAlphabetically(a,b)` is `a == b`
- `IsNotSameAlphabetically(a,b)` is `a != b`

---

## 14. Length and Size Relations (Normative)

Operators:

- `IsLength`
- `IsNotLength`
- `IsSameLength`
- `IsNotSameLength`
- `IsLongerThan`
- `IsShorterThan`
- `IsNoLongerThan`
- `IsNoShorterThan`

Arity: 2

Signatures:

- `LengthOp(Validation<T>, Validation<number>) -> Validation<boolean>`

Where length is defined for v0.1 as:

- for `string`: length is the number of Unicode scalar values
- for `array`: length is the element count

If the left argument is not a `string` or `array`, evaluation MUST return `Invalid([...])`.

The right argument MUST be a number that is an integer and is $\ge 0$.

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise compute `len(left)`.

Mapping:

- `IsLength(x,n)` is `len(x) == n`
- `IsNotLength(x,n)` is `len(x) != n`
- `IsSameLength(a,b)` is `len(a) == len(b)` (see rule below)
- `IsNotSameLength(a,b)` is `len(a) != len(b)` (see rule below)
- `IsLongerThan(x,n)` is `len(x) > n`
- `IsShorterThan(x,n)` is `len(x) < n`
- `IsNoLongerThan(x,n)` is `len(x) <= n`
- `IsNoShorterThan(x,n)` is `len(x) >= n`

Special case (Normative):

For `IsSameLength` and `IsNotSameLength`, the right argument MUST be `Validation<string|array>`, not a number.
If this is violated, evaluation MUST return `Invalid([...])`.

---

## 15. Set and Collection Relations (Normative)

Operators:

- `IsMember`
- `InSet`
- `IsSubset`
- `IsSuperset`
- `IsDisjointSet`
- `IsOverlappingSet`

Representation:

In v0.1, a set value is represented as a `List` whose elements are unique under structural equality.

Arity:

- `IsMember`: 2
- `InSet`: 2
- `IsSubset`: 2
- `IsSuperset`: 2
- `IsDisjointSet`: 2
- `IsOverlappingSet`: 2

Signatures:

- `IsMember(Validation<any>, Validation<List>) -> Validation<boolean>`
- `InSet(Validation<any>, Validation<List>) -> Validation<boolean>`
- `SetRel(Validation<List>, Validation<List>) -> Validation<boolean>`

Semantics:

1. If any argument is `Invalid`, return `Invalid`.
2. If a required set argument is not a `List`, return `Invalid([...])`.
3. If a set argument contains duplicates (by structural equality), return `Invalid([...])`.

Membership:

- `IsMember(x, set)` and `InSet(x, set)` are equivalent in v0.1.
- The result is `Valid(true)` iff some element of `set` is structurally equal to `x`.

Set relations:

- `IsSubset(a,b)` is true iff every element of `a` is in `b`.
- `IsSuperset(a,b)` is true iff every element of `b` is in `a`.
- `IsDisjointSet(a,b)` is true iff `a` and `b` share no equal elements.
- `IsOverlappingSet(a,b)` is true iff `a` and `b` share at least one equal element.

---

## 16. Sequence Ordering (Normative)

Operators:

- `IsAscending`
- `IsDescending`

Arity: 1

Signatures:

- `IsAscending(Validation<array>) -> Validation<boolean>`
- `IsDescending(Validation<array>) -> Validation<boolean>`

Semantics:

- If the input is `Invalid`, return `Invalid`.
- If the input is not an `array`, return `Invalid([...])`.
- For arrays of length 0 or 1, return `Valid(true)`.

Comparable element sets in v0.1:

- numbers compare numerically
- strings compare by Unicode codepoint order

If the array contains mixed or non-comparable element types, return `Invalid([...])`.

Ordering definition:

- `IsAscending` means non-decreasing ($a_i \le a_{i+1}$ for all adjacent pairs)
- `IsDescending` means non-increasing ($a_i \ge a_{i+1}$ for all adjacent pairs)

---

## 17. Additional Type Guards (Normative)

Operators:

- `IsArray`
- `IsMap`
- `IsSet`
- `IsRealNumber`
- `IsPrecisionNumber`

Arity: 1

Signatures:

- `TypeGuard(Validation<any>) -> Validation<boolean>`

Semantics:

- If the input is `Invalid`, return `Invalid`.
- `IsArray` returns true iff the value is a `List`.
- `IsMap` returns true iff the value is a `Record`.
- `IsSet` returns true iff the value is a `List` with no duplicates under structural equality.

Numeric notes (Normative):

- In the runtime-neutral v0.1 value model, both `IsRealNumber` and `IsPrecisionNumber` MUST behave equivalently to `IsNumber`.
- This is a semantic distinction carried by schemas; the runtime-neutral interchange representation does not require separate numeric encodings.

---

## 18. Temporal Operators (v0.1)

The Behavior Vocabulary includes temporal guards and relations.

Temporal types are **semantic types**.
They are not tied to any particular host implementation (for example, ECMAScript Temporal).

In v0.1, temporal values MUST be represented as `Text` values.

### 18.1 Supported temporal encodings (Normative)

The following encodings are used by temporal guards in v0.1:

- `PlainDate` is a string matching `YYYY-MM-DD`.
- `PlainTime` is a string matching `HH:MM:SS` with optional fractional seconds.
- `PlainDateTime` is a string matching `YYYY-MM-DDTHH:MM:SS` with optional fractional seconds and with no time zone designator.
- `PlainYearMonth` is a string matching `YYYY-MM`.
- `PlainMonthDay` is a string matching `MM-DD`.
- `YearWeek` is a string matching `YYYY-Www` (ISO week date form).
- `Instant` is a string matching a restricted RFC 3339 timestamp (date + time + `Z` or numeric offset).
- `ZonedDateTime` is a string matching an RFC 3339 timestamp that includes an offset and a bracketed time zone identifier.
- `TimeZone` is an IANA time zone identifier string (for example `America/Los_Angeles`).
- `Calendar` is a calendar identifier string (for v0.1, `iso8601` MUST be recognized).
- `Duration` is an ISO 8601 duration string (for example `P3DT4H30M`).

If a value cannot be parsed according to the required encoding, temporal operators MUST return `Invalid([...])`.

### 18.2 Temporal type guards (Normative)

Operators:

- `IsCalendar`
- `IsTimeZone`
- `IsDuration`
- `IsInstant`
- `IsPlainDate`
- `IsPlainTime`
- `IsPlainDateTime`
- `IsPlainMonthDay`
- `IsPlainYearMonth`
- `IsYearWeek`
- `IsZonedDateTime`

Arity: 1

Signatures:

- `TemporalGuard(Validation<any>) -> Validation<boolean>`

Semantics:

- If the input is `Invalid`, return `Invalid`.
- If the input is not a string, return `Valid(false)`.
- Otherwise return `Valid(true)` iff the string parses according to the required encoding.

If an encoding requires a restricted identifier set (for example `Calendar`), unrecognized identifiers MUST return `Valid(false)`.

### 18.3 Date relations (Normative)

Operators:

- `IsAfterDate`
- `IsBeforeDate`
- `IsNotAfterDate`
- `IsNotBeforeDate`
- `IsSameDate`

Arity: 2

Signatures:

- `DateRel(Validation<string>, Validation<string>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise parse both as `PlainDate`.
- Comparison is by chronological order.

### 18.4 Time relations (Normative)

Operators:

- `IsAfterTime`
- `IsBeforeTime`
- `IsNotAfterTime`
- `IsNotBeforeTime`
- `IsSameTime`

Arity: 2

Signatures:

- `TimeRel(Validation<string>, Validation<string>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise parse both as `PlainTime`.
- Comparison is by chronological order within a day.

### 18.5 DateTime relations (Normative)

Operators:

- `IsAfterDateTime`
- `IsBeforeDateTime`
- `IsNotAfterDateTime`
- `IsNotBeforeDateTime`
- `IsSameDateTime`

Arity: 2

Signatures:

- `DateTimeRel(Validation<string>, Validation<string>) -> Validation<boolean>`

Semantics:

- If either argument is `Invalid`, return `Invalid`.
- Otherwise parse both as `PlainDateTime`.
- Comparison is by chronological order in local date-time ordering.

---

## 19. Compile-Time Constructor Concepts (Normative)

The Behavior Vocabulary includes constructor-like concepts:

- `makeAlphabeticalConstructor`
- `makeAmountConstructor`
- `makeLengthConstructor`

In v0.1, these concepts are **authoring-time compile-time constructs** and MUST NOT appear in a compiled, runtime-neutral Behavior Program.

If any of these concepts are present as runtime operators in a Behavior Program:

- Kernel evaluation MUST return `Invalid([...])`.
- HTML Runtime evaluation MUST return `Invalid([...])`.

---

## 20. Operator Inventory (Normative)

This specification defines the complete set of v0.1 Behavior operators.

Any operator not defined by this document MUST be rejected.

## 21. Relational Operators and Guards (Inventory Summary) (Normative)

This section is a non-exhaustive *index* of the relational operators and guards defined elsewhere in this document.
In case of conflict, the normative per-operator sections win.

Relational operators (comparisons and relations):

- Equality: `IsEqualTo`, `IsUnequalTo`
- Ordering (numbers/strings): `IsLessThan`, `IsMoreThan`, `IsNoLessThan`, `IsNoMoreThan`
- Pattern: `Matches`, `DoesNotMatch`
- Alphabetical: `IsAfterAlphabetically`, `IsBeforeAlphabetically`, `IsNotAfterAlphabetically`, `IsNotBeforeAlphabetically`, `IsSameAlphabetically`, `IsNotSameAlphabetically`
- Length/size: `IsLength`, `IsNotLength`, `IsSameLength`, `IsNotSameLength`, `IsLongerThan`, `IsShorterThan`, `IsNoLongerThan`, `IsNoShorterThan`
- Set/collection: `IsMember`, `InSet`, `IsSubset`, `IsSuperset`, `IsDisjointSet`, `IsOverlappingSet`
- Sequence ordering: `IsAscending`, `IsDescending`
- Temporal (relations): `IsAfterDate`, `IsBeforeDate`, `IsNotAfterDate`, `IsNotBeforeDate`, `IsSameDate`, `IsAfterTime`, `IsBeforeTime`, `IsNotAfterTime`, `IsNotBeforeTime`, `IsSameTime`, `IsAfterDateTime`, `IsBeforeDateTime`, `IsNotAfterDateTime`, `IsNotBeforeDateTime`, `IsSameDateTime`

Guards (type tests):

- Scalar: `IsBoolean`, `IsNumber`, `IsString`, `IsInteger`
- Structural: `IsArray`, `IsMap`, `IsSet`
- Numeric refinements: `IsRealNumber`, `IsPrecisionNumber`
- Temporal: `IsCalendar`, `IsTimeZone`, `IsDuration`, `IsInstant`, `IsPlainDate`, `IsPlainTime`, `IsPlainDateTime`, `IsPlainMonthDay`, `IsPlainYearMonth`, `IsYearWeek`, `IsZonedDateTime`

## 22. Candidate Additions (Informative)

The following operator families are common in constraint systems but are not defined in v0.1 unless explicitly added elsewhere:

- Presence/missingness: `IsPresent`, `IsAbsent`
- String relations: `StartsWith`, `EndsWith`, `ContainsSubstring`
- Numeric ranges: `IsBetween`, `IsNotBetween`
- Collection relations: `IsEmpty`, `IsNotEmpty`, `ContainsAll`, `ContainsAny`
- Temporal relations beyond Plain types: `IsAfterInstant`, `IsBeforeInstant`, and ZonedDateTime comparisons

If added in future versions, they MUST preserve determinism and MUST NOT introduce ambient dependencies.

---

## 23. Relationship to Other Specifications

This specification works in conjunction with:

- Behavior Program Encoding (interchange form)

---

**End of Behavior Dialect v0.1**
