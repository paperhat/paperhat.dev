Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Dialect Semantics

This specification defines the **Behavior Dialect** semantic contract for Paperhat.

The Behavior Dialect is authored in Codex and compiles into an executable (pure) function artifact. This spec defines **what Behavior means**, independent of any host language or runtime.

This document is **Normative**.

---

## 1. Purpose

This spec exists to define:

- the canonical evaluation model for Behavior expressions
- purity and determinism rules
- the complete typed value model (aligned with Codex literal values)
- operator application rules (arity, strictness, evaluation order)
- error and diagnostic rules

This spec does not define:

- the operator vocabulary inventory (see Behavior Vocabulary)
- runtime integration details (owned by target runtimes)

---

## 2. Core Principles (Normative)

1. **Purity:** Behavior evaluation MUST be side-effect free.
2. **Determinism:** Given the same program and explicit inputs, evaluation MUST produce the same result.
3. **No ambient dependencies:** Evaluation MUST NOT consult time, randomness, filesystem, network, or other ambient sources.
4. **Runtime independence:** Semantics MUST NOT depend on any particular host implementation.
5. **Value completeness:** Behavior MUST support operations on any value type that can appear as a Trait value in Codex.

Additional safety boundaries (Normative):

6. **No dynamic code construction:** Strings are data, never code. A Behavior Program MUST NOT contain or cause:
   - dynamic operator selection (no "operator name from string")
   - executable data-as-AST (no "evaluate user-provided graph as code")
   - query-as-string (no SPARQL embedded as a string literal for execution)

Clarifications (Normative):

- Systems MAY depend on time, randomness, or I/O as system behavior.
- Behavior evaluation MUST remain deterministic; therefore time/randomness/I/O MUST be supplied as explicit inputs.

---

## 3. Evaluation Result Model (Normative)

Behavior evaluation produces a `Validation<Value>`:

- `Valid(value)`
- `Invalid(diagnostics)`

An evaluator MUST NOT throw for user-authored input; it MUST return `Invalid(...)` with diagnostics.

Diagnostics MUST be stable and deterministic (ordering and identity rules defined in Section 8).

---

## 4. Expressions (Normative)

A Behavior Program is an expression tree.

Every node is one of:

- `Argument` — the primary input value
- `Variable(name)` — environment lookup
- `Constant(value)` — literal constant value
- `Field(name)` — field lookup on a Record-like value
- `Index(n)` — index lookup on a Tuple or List
- `Path(steps...)` — bounded path traversal
- `Apply(operator, arguments...)` — operator application

Notes:

- `operator` is a reference to a Behavior Vocabulary Concept.
- This spec defines evaluation; the concrete Codex surface form is defined elsewhere.

Path and missingness (Normative):

- `Field(name)`, `Index(n)`, and `Path(...)` MUST be total and deterministic.
- If a referenced field/index/path location is missing, the result MUST be the canonical `<Absent/>` value.
- Operators that require presence or a specific domain MUST return `Invalid(...)` rather than silently accepting `<Absent/>`.

---

## 5. Value Model (Normative)

Behavior Values are **Codex values**. The Behavior Dialect supports all value types defined by the Codex Naming and Value Specification.

### 5.1 Canonical Absent Value

Behavior defines a canonical missing-value concept:

- `<Absent/>`

Normative rules:

1. `<Absent/>` represents "no value exists here" (missing field, missing path location, missing optional trait value).
2. `<Absent/>` is distinct from empty text, empty list, empty set, and empty record; those are present values.
3. Implementations MUST NOT introduce any separate "Null" semantic value.

### 5.2 Boolean

- `Boolean` — `true` or `false`

### 5.3 Text and Character

- `Text` — a sequence of Unicode scalar values
- `Character` — a single Unicode scalar value

### 5.4 Numeric Types

Behavior defines distinct semantic numeric domains. All numeric operators MUST specify which domains they accept and what they return.

#### 5.4.1 Real Number Domains

- `Integer` — exact integer values (unbounded)
- `Fraction` — exact rational numbers (numerator/denominator)
- `PrecisionNumber` — decimal numbers with explicit precision (trailing zeros are significant)
- `RealNumber` — approximate real numbers (IEEE 754 when profiled)

#### 5.4.2 Complex Number Domains

- `Imaginary` — pure imaginary numbers (`2i`, `3.5i`)
- `Complex` — complex numbers with real and imaginary parts (`2+3i`, `1.5-2.5i`)

#### 5.4.3 Special Numeric Values

- `PositiveInfinity`
- `NegativeInfinity`
- `NotANumber`
- `NegativeZero`

#### 5.4.4 Derived Numeric Domains

For convenience in operator specifications:

- `OrderableNumber` := `Integer` | `Fraction` | `PrecisionNumber`
- `ExactNumber` := `Integer` | `Fraction`
- `AnyRealNumber` := `Integer` | `Fraction` | `PrecisionNumber` | `RealNumber`
- `AnyNumber` := `AnyRealNumber` | `Imaginary` | `Complex`

Rules (Normative):

1. Numeric domains MUST NOT be collapsed into a single host "number" type in the semantic contract.
2. Conversions between numeric domains MUST be explicit via vocabulary Concepts.
3. Where an operator admits multiple domains, the result domain MUST be defined and deterministic.

### 5.5 Collection Types

#### 5.5.1 List

- `List<T>` — ordered collection, may contain duplicates, variable length

#### 5.5.2 Set

- `Set<T>` — unordered collection, unique elements under structural equality

#### 5.5.3 Tuple

- `Tuple<T1, T2, ...>` — ordered, fixed-length, positional semantics, heterogeneous

#### 5.5.4 Map

- `Map<K, V>` — key-value collection with unique keys

Map keys may be:
- `Text`
- `Character`
- `Integer`
- `EnumeratedToken`

#### 5.5.5 Record

- `Record` — key-value structure with `Text` keys (a specialization of Map)

#### 5.5.6 Range

- `Range<T>` — declarative interval with start, end, and optional step

Range element types:
- Numeric ranges (`1..10`, `1..100s5`)
- Temporal ranges (`{2024-01-01}..{2024-12-31}`)
- Character ranges (`'A'..'Z'`)

### 5.6 Temporal Types

Temporal values are first-class semantic types, not Text with guards.

- `PlainDate` — calendar date without time (`YYYY-MM-DD`)
- `PlainTime` — time of day without date (`HH:MM:SS`)
- `PlainDateTime` — local date and time without timezone
- `PlainYearMonth` — year and month (`YYYY-MM`)
- `PlainMonthDay` — month and day (`MM-DD`)
- `YearWeek` — ISO week date (`YYYY-Www`)
- `Instant` — absolute point in time (UTC timestamp)
- `ZonedDateTime` — date-time with timezone
- `Duration` — ISO 8601 duration
- `TimeZone` — IANA timezone identifier
- `Calendar` — enumerated calendar system (default: `iso8601`)

### 5.7 Color Types

Color values are first-class semantic types.

- `Color` — abstract color value

Color representations:
- `HexColor` — `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`
- `RgbColor` — `rgb(r g b)` or `rgb(r g b / alpha)`
- `HslColor` — `hsl(h s l)` or `hsl(h s l / alpha)`
- `LabColor` — `lab(l a b)` or `lab(l a b / alpha)`
- `LchColor` — `lch(l c h)` or `lch(l c h / alpha)`
- `OklabColor` — `oklab(l a b)` or `oklab(l a b / alpha)`
- `OklchColor` — `oklch(l c h)` or `oklch(l c h / alpha)`
- `ColorFunction` — wide gamut colors in specified color space

All color representations are convertible to a canonical internal form for operations.

### 5.8 Identity and Reference Types

- `Uuid` — universally unique identifier
- `IriReference` — IRI for identity or reference
- `LookupToken` — shorthand reference (`~token`)

### 5.9 Enumerated Token

- `EnumeratedToken` — schema-defined closed set value (`$Identifier`)

---

## 6. Type Checking and Coercion (Normative)

This spec uses three related ideas:

- **Type checking:** rejecting invalid inputs to an operator.
- **Normalization:** producing a canonical value representation.
- **Coercion:** converting between domains.

Rules (Normative):

1. If an operator receives values outside its domain, evaluation MUST return `Invalid([...])`.
2. Coercion MUST be explicit (via vocabulary Concepts) unless a specific operator family defines a fixed coercion rule.
3. Any implicit coercion rules that do exist MUST be minimal, deterministic, and specified by this document.

Coercion policy (Normative):

- No general implicit coercion lattice is defined.
- An operator MAY accept multiple domains only if its own vocabulary definition explicitly says so.
- Where ordering or equality requires comparability across numeric domains, it MUST follow the cross-domain numeric comparability rules in Value Ordering and Structural Equality.
- No implicit coercion is permitted between unrelated domains (for example `Text` to `Integer`, `Record` to `List`).

Numeric promotion rules (Normative):

When arithmetic operators accept mixed numeric domains, the following promotion rules apply:

1. `Integer` + `Fraction` -> `Fraction`
2. `Integer` + `PrecisionNumber` -> `PrecisionNumber`
3. `Fraction` + `PrecisionNumber` -> `PrecisionNumber`
4. Any exact type + `RealNumber` -> `RealNumber`
5. Any real type + `Imaginary` -> `Complex`
6. Any real type + `Complex` -> `Complex`

---

## 7. Collection Semantics (Normative)

### 7.1 List Semantics

- Ordered by position
- Allows duplicates
- Zero-indexed for `Index` access
- Length is variable

### 7.2 Set Semantics

- Unordered (iteration order is deterministic but unspecified)
- Unique elements under structural equality
- Membership testing is the primary operation

### 7.3 Tuple Semantics

- Ordered by position
- Fixed length (schema-defined)
- Zero-indexed for `Index` access
- Heterogeneous element types
- Positional meaning (position determines semantics)

### 7.4 Map Semantics

- Key-value pairs
- Unique keys under structural equality
- Key types are restricted (see Section 5.5.4)
- Iteration order is deterministic (insertion order)

### 7.5 Range Semantics

- Inclusive endpoints
- Optional step value
- May be iterated to produce elements
- May be tested for membership

---

## 8. Diagnostics (Normative)

A diagnostic MUST include:

- a stable code (token)
- an optional human-readable message
- a stable location reference to the originating expression node (program-local)

Code structure (Normative):

- Codes MUST follow the pattern `<surfaceName>::<ISSUE_DESCRIPTION>`.
- Where a Behavior diagnostic code is required, it MUST use the corresponding code defined by Behavior Diagnostic Codes.

Diagnostics ordering MUST be deterministic.

Diagnostics ordering key (Normative):

1. Diagnostics MUST be ordered by the **origin expression location** in authored operand order.
2. The origin expression location is the expression node that first produced the diagnostic.
3. Origin expression locations MUST be ordered by a depth-first, left-to-right traversal of the program expression tree.
4. If a single expression node produces multiple diagnostics, they MUST be ordered in the sequence they are produced by that node's normative semantics.
5. If two diagnostics still tie (same origin expression location and same emission ordinal), they MUST be ordered by ascending diagnostic `code` (Unicode scalar value order).

---

## 9. Evaluation Order and Strictness (Normative)

Implementations MAY evaluate operands using any strategy (including reordering, parallelism, or short-circuiting) provided that:

1. the final `Valid(...)` / `Invalid(...)` outcome is identical to the reference evaluation defined by this specification, and
2. the ordered list of produced diagnostics is identical to the reference ordering rules.

Unless explicitly stated otherwise, evaluation MUST behave observably as if:

- argument expressions were evaluated left-to-right, and
- diagnostics were accumulated and emitted in authored operand order.

Operators MAY be implemented as curried and/or higher-order functions internally, but the observable semantics MUST match this specification.

---

## 10. Boundedness (Normative)

An implementation MUST enforce policy-bounded limits sufficient to prevent resource exhaustion.

Limits MUST be enforceable for:

- maximum program depth
- maximum expression depth
- maximum collection length processed per operator
- maximum output size
- maximum join output size
- maximum iteration count (for Range expansion)
- maximum recursion depth (for nested structures)

When a limit is exceeded, evaluation MUST return `Invalid(...)` with the appropriate diagnostic code.

---

## 11. Relationship to Other Specifications

This specification works in conjunction with:

- Codex Naming and Value Specification (defines literal value forms)
- Behavior Vocabulary (operator inventory and semantics per operator)
- Value Ordering and Structural Equality (comparison rules)
- Target runtimes (HTML runtime, native runtime, etc.)

---

**End of Behavior Dialect Semantics v0.1**
