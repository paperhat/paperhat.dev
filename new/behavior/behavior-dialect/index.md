Status: NORMATIVE
Lock State: UNLOCKED
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

- the complete value model (see Behavior Dialect Semantics)
- the interchange encoding (see Behavior Program Encoding)
- the operator inventory (see Behavior Vocabulary)
- target-specific UI semantics (owned by runtimes/renderers)

---

## 2. Core Principles (Normative)

1. **Purity:** Behavior evaluation MUST be side-effect free.
2. **Determinism:** Given the same program and explicit inputs, evaluation MUST produce the same result.
3. **Target neutrality:** Operators MUST NOT depend on HTML/DOM/PDF/spreadsheet assumptions.
4. **No ambient dependencies:** Evaluation MUST NOT consult time, randomness, filesystem, or network.
5. **Value completeness:** Behavior MUST support operations on any value type that can appear as a Trait value in Codex.

Additional safety boundary (Normative):

6. **No dynamic code construction:** Strings are data, never code. A Behavior Program MUST NOT contain or cause:
   - dynamic operator selection (no "operator name from string")
   - executable data-as-AST (no "evaluate user-provided graph as code")
   - query-as-string (no SPARQL embedded as a string literal for execution)

Clarification (Normative):

- Paperhat MAY depend on time, randomness, or I/O as *system behavior*.
- Behavior evaluation itself MUST remain deterministic; therefore time/randomness/I/O MUST be supplied as explicit inputs (for example via `Environment` bindings).

---

## 3. Runtime-Neutral Result Model (Normative)

All Behavior evaluation produces a `Validation`:

- `Valid(value)`
- `Invalid(diagnostics)`

A Behavior evaluator MUST NOT throw for user-authored input; it MUST return `Invalid(...)` with diagnostics.

This rule applies to:

- Kernel evaluation
- HTML runtime evaluation

---

## 4. Values and Types (Normative)

Behavior values are **Codex values**, not JSON values.

The complete value model is defined by **Behavior Dialect Semantics** and includes:

- Scalars: Boolean, Text, Character
- Numerics: Integer, Fraction, PrecisionNumber, RealNumber, Imaginary, Complex
- Collections: List, Set, Tuple, Map, Record, Range
- Temporal: PlainDate, PlainTime, PlainDateTime, Instant, ZonedDateTime, Duration, etc.
- Colors: RgbColor, HslColor, LabColor, OklchColor, etc.
- Identity: Uuid, IriReference, LookupToken, EnumeratedToken
- Missingness: `<Absent/>`

Normative missingness rule:

- `<Absent/>` is the single canonical missing-value concept.
- Implementations MUST NOT introduce any separate "Null" semantic value.

---

## 5. Reserved Operators (Normative)

The following operators are reserved and their intent is fixed:

| Operator | Purpose |
|----------|---------|
| `Argument` | The primary input value |
| `Variable(name)` | Environment lookup |
| `Constant(value)` | Literal constant |
| `Field(name)` | Field lookup on a Record/Map |
| `Index(n)` | Index lookup on a Tuple/List |
| `Path(steps...)` | Bounded path traversal |

Encoding is defined by the Behavior Program Encoding spec.

Typing rules:

- `Argument` is dynamically typed (type is determined by caller context)
- `Variable` is dynamically typed (type is determined by the bound value)
- `Constant` has the type implied by the literal value

---

## 6. Environment and Missing Variables (Normative)

If `Variable(name)` is evaluated and `name` is missing in the environment, the result MUST be:

- `Invalid([...])` with diagnostic identifying the missing variable name.

Evaluators MUST NOT substitute default values for missing variables.

### 6.1 External Inputs (Time, Randomness, I/O)

Paperhat supports time-dependent, random, and I/O-driven behavior by treating the *results* of those operations as explicit inputs to Behavior.

Rules:

1. Behavior MUST NOT contain operations that consult ambient time, randomness, filesystem, or network.
2. If time is needed, the relevant time value MUST be supplied as an explicit input.
3. If randomness is needed, the generated value MUST be supplied as an explicit input.
4. If I/O is needed, the looked-up value MUST be supplied as an explicit input.

This keeps evaluation deterministic while still allowing systems to incorporate effectful sources.

### 6.2 Runtime Tagged Types

Implementations MAY represent values using runtime tagged types internally for:

- runtime type checking
- lossless normalization
- domain-safe operations

However:

1. Interchange values embedded in Behavior Programs MUST remain pure data.
2. Observable Behavior semantics MUST be consistent across runtimes.
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
   - handle it explicitly if defined by the operator's semantics.

Unless otherwise specified, operators MUST propagate `Invalid`.

---

## 8. Evaluation Order (Normative)

Evaluation order MUST be deterministic.

Unless an operator defines short-circuiting semantics, arguments MUST be evaluated left-to-right.

Implementations MAY use any evaluation strategy (including parallelism) provided:

1. The final `Valid(...)`/`Invalid(...)` outcome is identical to reference evaluation.
2. The ordered list of diagnostics is identical to reference ordering rules.

---

## 9. Logical Operators (Normative)

### 9.1 `Not`

Arity: 1

```
Not(Validation<Boolean>) -> Validation<Boolean>
```

- `Valid(true)` -> `Valid(false)`
- `Valid(false)` -> `Valid(true)`
- `Invalid(d)` -> `Invalid(d)`

### 9.2 `And`

Arity: 2 or more

```
And(Validation<Boolean>...) -> Validation<Boolean>
```

- If any argument is `Invalid(...)`, return `Invalid(...)`.
- If all arguments are `Valid(true)`, return `Valid(true)`.
- Otherwise return `Valid(false)`.

### 9.3 `Or`

Arity: 2 or more

```
Or(Validation<Boolean>...) -> Validation<Boolean>
```

- If any argument is `Invalid(...)`, return `Invalid(...)`.
- If any argument is `Valid(true)`, return `Valid(true)`.
- Otherwise return `Valid(false)`.

### 9.4 `Xor`

Arity: 2

```
Xor(Validation<Boolean>, Validation<Boolean>) -> Validation<Boolean>
```

- If either argument is `Invalid`, return `Invalid`.
- Otherwise return `Valid(a != b)`.

### 9.5 `Ternary`

Arity: 3

```
Ternary(Validation<Boolean>, Validation<T>, Validation<T>) -> Validation<T>
```

- If condition is `Valid(true)`, return the then-branch.
- If condition is `Valid(false)`, return the else-branch.
- If condition is `Invalid`, return `Invalid`.

---

## 10. Equality and Comparison (Normative)

### 10.1 Equality

```
IsEqualTo(Validation<any>, Validation<any>) -> Validation<Boolean>
IsUnequalTo(Validation<any>, Validation<any>) -> Validation<Boolean>
```

- If either argument is `Invalid`, return `Invalid`.
- Otherwise compare using structural equality (see Value Ordering and Structural Equality).

### 10.2 Ordering

```
IsLessThan(Validation<T>, Validation<T>) -> Validation<Boolean>
IsMoreThan(Validation<T>, Validation<T>) -> Validation<Boolean>
IsNoLessThan(Validation<T>, Validation<T>) -> Validation<Boolean>
IsNoMoreThan(Validation<T>, Validation<T>) -> Validation<Boolean>
```

Where T is a comparable type.

- If either argument is `Invalid`, return `Invalid`.
- If types are not comparable, return `Invalid([...])`.

Comparable domains are defined by Value Ordering and Structural Equality.

---

## 11. Type Guards (Normative)

Type guards test whether a value belongs to a specific type.

```
TypeGuard(Validation<any>) -> Validation<Boolean>
```

- If input is `Invalid`, return `Invalid`.
- Otherwise return `Valid(true)` or `Valid(false)`.

### 11.1 Scalar Guards

- `IsBoolean`
- `IsText`
- `IsCharacter`

### 11.2 Numeric Guards

- `IsInteger`
- `IsFraction`
- `IsPrecisionNumber`
- `IsRealNumber`
- `IsImaginary`
- `IsComplex`
- `IsNumber` — true for any numeric type

### 11.3 Collection Guards

- `IsList`
- `IsSet`
- `IsTuple`
- `IsMap`
- `IsRecord`
- `IsRange`

### 11.4 Temporal Guards

- `IsPlainDate`
- `IsPlainTime`
- `IsPlainDateTime`
- `IsPlainYearMonth`
- `IsPlainMonthDay`
- `IsYearWeek`
- `IsInstant`
- `IsZonedDateTime`
- `IsDuration`
- `IsTimeZone`
- `IsCalendar`
- `IsTemporal` — true for any temporal type

### 11.5 Color Guards

- `IsColor` — true for any color type
- `IsRgbColor`
- `IsHslColor`
- `IsLabColor`
- `IsLchColor`
- `IsOklabColor`
- `IsOklchColor`
- `IsHexColor`

### 11.6 Identity Guards

- `IsUuid`
- `IsIriReference`
- `IsLookupToken`
- `IsEnumeratedToken`

### 11.7 Missingness Guards

- `IsAbsent` — true iff value is `<Absent/>`
- `IsPresent` — true iff value is not `<Absent/>`

---

## 12. Operator Inventory (Normative)

The complete set of Behavior operators is defined by:

- this specification (core operators), and
- the Behavior Vocabulary specifications

Any operator not defined by either MUST be rejected.

The Behavior Vocabulary includes:

- **Math** — arithmetic, complex numbers, statistics, linear algebra, calculus
- **Core Safe Transforms** — map, filter, reduce, sort, join, set/map operations
- **Text** — string manipulation, pattern matching, encoding
- **Temporal** — date/time construction, arithmetic, comparison
- **Color** — color construction, conversion, manipulation, analysis
- **Identity** — UUID, IRI, token operations
- **Relational and Predicates** — comparison, logical composition
- **Data Shapes** — collection size, membership, record satisfaction
- **Presence and Missingness** — handling `<Absent/>`
- **Formatting** — value formatting

---

## 13. Relationship to Other Specifications

This specification works in conjunction with:

- **Behavior Dialect Semantics** — complete value model
- **Behavior Program Encoding** — interchange format
- **Behavior Vocabulary** — operator inventory
- **Value Ordering and Structural Equality** — comparison rules
- **Behavior Diagnostic Codes** — error codes

---

**End of Behavior Dialect v0.1**
