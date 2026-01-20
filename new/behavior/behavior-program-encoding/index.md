Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Program Encoding

This specification defines the canonical **interchange encoding** for Paperhat Behavior Programs.

This document is **Normative**.

---

## 1. Purpose

Paperhat Behavior is an expression language authored in Codex (and potentially derived from other constraint systems).

Behavior MUST compile to a runtime-neutral representation that can be:

- embedded into Adaptive Layouts
- evaluated in the Kernel (native execution)
- evaluated in the HTML runtime (browser user-agent)

This spec defines the encoding as a **Codex opcode tree**.

Clarification (Normative):

- The Behavior semantic value model is defined by Behavior Dialect Semantics; this document specifies how Behavior Programs and their values are represented as Codex values for interchange.
- Implementations MAY serialize Codex values into a transport format as needed by their environment, but serialization is out of scope for this specification.

---

## 2. Non-goals

- This spec does not define the full Behavior Dialect (operator typing rules and signatures); that is defined by the Behavior Dialect specification.
- This spec does not require any particular programming language runtime.
- This spec does not define UI attachment semantics (Validate/ShowIf/etc.); those are defined by the Adaptive Layout and HTML runtime contracts.

---

## 3. Determinism and Safety (Normative)

1. A Behavior Program MUST be pure data.
2. A Behavior Program MUST NOT embed executable code (for example: functions, scripts, bytecode, closures).
3. A Behavior Program MUST NOT require network access to evaluate.
4. A Behavior Program MUST be deterministic given:
   - the Program
   - an explicit evaluation environment (`Environment`)

Diagnostic codes (Normative):

- If decoding/validation of the encoded program fails, evaluators MUST produce `Invalid(...)` using the corresponding codes defined by Behavior Diagnostic Codes.

---

## 4. Program Envelope (Normative)

A Behavior Program MUST be a Codex `Record` with:

- `version` (Text) — MUST equal `"0.1"`
- `expression` (Expression) — the root expression node

Example:

```codex
{
  version: "0.1",
  expression: { operation: "And", arguments: [ { operation: "IsInteger", arguments: [{ operation: "Argument" }] } ] }
}
```

---

## 5. Expression Node Shape (Normative)

An Expression node MUST be a Codex `Record` with:

- `operation` (Text) — a stable token naming a Behavior Vocabulary Concept

An Expression node MAY include:

- `arguments` (List of Expression)
- `value` (EncodedValue, depending on operation)
- `name` (Text, for name-bearing ops)
- `index` (Integer, for index-bearing ops)
- `steps` (List of PathStep, for path-bearing ops)

No additional fields are permitted unless explicitly defined by this spec.

---

## 6. Encoded Values (Normative)

An `EncodedValue` MUST be a valid Codex value that encodes a Behavior semantic value.

### 6.1 Absent

```codex
{ @paperhat: { concept: "Absent" } }
```

### 6.2 Boolean

Encoded directly as Codex `Boolean`:

```codex
true
false
```

### 6.3 Text

Encoded directly as Codex `Text`:

```codex
"hello world"
```

### 6.4 Character

```codex
{ @paperhat: { concept: "Character", value: "A" } }
```

Rules:
- `value` MUST be a single Unicode scalar value encoded as Text.

### 6.5 Integer

```codex
{ @paperhat: { concept: "Integer", value: "-12" } }
```

Rules:
- `value` MUST be a base-10 integer string matching `-?(0|[1-9][0-9]*)`.

### 6.6 Fraction

```codex
{ @paperhat: { concept: "Fraction", numerator: "-3", denominator: "4" } }
```

Rules:
- `numerator` MUST be a base-10 integer string matching `-?(0|[1-9][0-9]*)`.
- `denominator` MUST be a base-10 integer string matching `[1-9][0-9]*`.
- `denominator` MUST NOT be `"0"`.
- The sign MUST be carried by `numerator`; `denominator` MUST be positive.

Normalization:
- Encoders MUST emit Fractions in canonical normalized form (reduced, positive denominator).
- Decoders MUST normalize to canonical form before evaluation.

### 6.7 PrecisionNumber

```codex
{ @paperhat: { concept: "PrecisionNumber", decimal: "12.3400" } }
```

Rules:
- `decimal` MUST be a base-10 decimal string matching `-?(0|[1-9][0-9]*)(\.[0-9]+)?`.
- Exponent notation MUST NOT be used.
- Trailing zeros MUST be preserved; they are semantically significant.

### 6.8 RealNumber

```codex
{ @paperhat: { concept: "RealNumber", value: "3.141592653589793" } }
```

Rules:
- `value` MUST be a decimal string or scientific notation string.
- Used for IEEE 754 approximate values.

### 6.9 Imaginary

```codex
{ @paperhat: { concept: "Imaginary", coefficient: "3.5" } }
```

Rules:
- `coefficient` is the real coefficient of `i`.
- May use any real numeric encoding for the coefficient.

### 6.10 Complex

```codex
{ @paperhat: { concept: "Complex", real: "2", imaginary: "3" } }
```

Rules:
- `real` and `imaginary` are the real and imaginary parts.
- Both may use any real numeric encoding.

### 6.11 Special Numeric Values

```codex
{ @paperhat: { concept: "PositiveInfinity" } }
{ @paperhat: { concept: "NegativeInfinity" } }
{ @paperhat: { concept: "NotANumber" } }
{ @paperhat: { concept: "NegativeZero" } }
```

### 6.12 List

Encoded directly as Codex `List`:

```codex
[ 1, 2, 3 ]
```

Elements are `EncodedValue`.

### 6.13 Set

```codex
{ @paperhat: { concept: "Set", elements: [ 1, 2, 3 ] } }
```

Rules:
- `elements` MUST contain unique values under structural equality.
- Order in encoding is not significant.

### 6.14 Tuple

```codex
{ @paperhat: { concept: "Tuple", elements: [ "John", "Doe", 30 ] } }
```

Rules:
- `elements` is an ordered list.
- Position is semantically significant.

### 6.15 Map

```codex
{ @paperhat: { concept: "Map", entries: [ { key: "a", value: 1 }, { key: "b", value: 2 } ] } }
```

Rules:
- `entries` is a list of key-value pairs.
- Keys MUST be unique under structural equality.
- Key types: Text, Character, Integer, or EnumeratedToken.

### 6.16 Record

Encoded directly as Codex `Record`:

```codex
{ name: "John", age: 30 }
```

Rules:
- Keys are Text.
- Values are `EncodedValue`.

### 6.17 Range

```codex
{ @paperhat: { concept: "Range", start: 1, end: 10 } }
{ @paperhat: { concept: "Range", start: 1, end: 100, step: 5 } }
```

Rules:
- `start` and `end` are required.
- `step` is optional.
- All must be of compatible types.

### 6.18 Temporal Values

#### PlainDate

```codex
{ @paperhat: { concept: "PlainDate", year: 2024, month: 1, day: 15 } }
```

#### PlainTime

```codex
{ @paperhat: { concept: "PlainTime", hour: 14, minute: 30, second: 0 } }
```

Optional: `millisecond`, `microsecond`, `nanosecond`.

#### PlainDateTime

```codex
{ @paperhat: { concept: "PlainDateTime", year: 2024, month: 1, day: 15, hour: 14, minute: 30, second: 0 } }
```

#### PlainYearMonth

```codex
{ @paperhat: { concept: "PlainYearMonth", year: 2024, month: 6 } }
```

#### PlainMonthDay

```codex
{ @paperhat: { concept: "PlainMonthDay", month: 12, day: 25 } }
```

#### YearWeek

```codex
{ @paperhat: { concept: "YearWeek", year: 2024, week: 15 } }
```

#### Instant

```codex
{ @paperhat: { concept: "Instant", epochNanoseconds: "1705312200000000000" } }
```

Rules:
- `epochNanoseconds` is a string to preserve precision.

#### ZonedDateTime

```codex
{ @paperhat: { concept: "ZonedDateTime", epochNanoseconds: "1705312200000000000", timeZone: "America/New_York" } }
```

#### Duration

```codex
{ @paperhat: { concept: "Duration", iso: "P3DT4H30M" } }
```

Rules:
- `iso` is an ISO 8601 duration string.

#### TimeZone

```codex
{ @paperhat: { concept: "TimeZone", identifier: "America/New_York" } }
```

#### Calendar

Calendar is an enumerated type. The default is `iso8601`.

Supported values: `iso8601`, `gregorian`, `julian`, `hebrew`, `islamic`, `islamic-umalqura`, `islamic-civil`, `islamic-tbla`, `persian`, `indian`, `buddhist`, `chinese`, `japanese`, `coptic`, `ethiopic`, `ethiopic-amete-alem`, `roc`.

```codex
{ @paperhat: { concept: "Calendar", identifier: "iso8601" } }
```

### 6.19 Color Values

#### HexColor

```codex
{ @paperhat: { concept: "HexColor", value: "#ff8800" } }
```

#### RgbColor

```codex
{ @paperhat: { concept: "RgbColor", red: 255, green: 128, blue: 0 } }
{ @paperhat: { concept: "RgbColor", red: 255, green: 128, blue: 0, alpha: 0.5 } }
```

#### HslColor

```codex
{ @paperhat: { concept: "HslColor", hue: 30, saturation: 100, lightness: 50 } }
{ @paperhat: { concept: "HslColor", hue: 30, saturation: 100, lightness: 50, alpha: 0.5 } }
```

#### LabColor

```codex
{ @paperhat: { concept: "LabColor", lightness: 70, a: 20, b: -30 } }
```

#### LchColor

```codex
{ @paperhat: { concept: "LchColor", lightness: 70, chroma: 45, hue: 30 } }
```

#### OklabColor

```codex
{ @paperhat: { concept: "OklabColor", lightness: 0.7, a: -0.1, b: 0.1 } }
```

#### OklchColor

```codex
{ @paperhat: { concept: "OklchColor", lightness: 0.7, chroma: 0.15, hue: 180 } }
```

#### ColorFunction

```codex
{ @paperhat: { concept: "ColorFunction", colorSpace: "display-p3", c1: 1, c2: 0.5, c3: 0 } }
```

### 6.20 Identity and Reference Values

#### Uuid

```codex
{ @paperhat: { concept: "Uuid", value: "550e8400-e29b-41d4-a716-446655440000" } }
```

Rules:
- `value` MUST be lowercase, hyphenated UUID format.

#### IriReference

```codex
{ @paperhat: { concept: "IriReference", value: "recipe:spaghetti" } }
```

#### LookupToken

```codex
{ @paperhat: { concept: "LookupToken", token: "spaghettiBolognese" } }
```

### 6.21 EnumeratedToken

```codex
{ @paperhat: { concept: "EnumeratedToken", value: "Featured" } }
```

Rules:
- `value` is the token identifier without the `$` sigil.

---

## 7. Core Reserved Ops (Normative)

The following ops are reserved and have encoding defined by this spec:

### 7.1 `Argument`

Represents the primary input value.

```codex
{ operation: "Argument" }
```

### 7.2 `Variable`

Represents a lookup in the evaluation environment.

```codex
{ operation: "Variable", name: "someName" }
```

Rules:
- `name` MUST be present.

### 7.3 `Constant`

Represents a literal constant.

```codex
{ operation: "Constant", value: { @paperhat: { concept: "Integer", value: "123" } } }
```

Rules:
- `value` MUST be present.
- `value` MUST be a valid `EncodedValue`.

### 7.4 `Field`

Represents a field lookup on a Record-like value.

```codex
{ operation: "Field", name: "fieldName" }
```

Rules:
- `name` MUST be present.

### 7.5 `Index`

Represents an index lookup on a Tuple or List.

```codex
{ operation: "Index", index: 0 }
```

Rules:
- `index` MUST be present.
- `index` MUST be a non-negative integer.

### 7.6 `Path`

Represents a bounded path traversal.

```codex
{ operation: "Path", steps: [ { field: "a" }, { index: 0 }, { field: "b" } ] }
```

PathStep encoding:
- `{ field: "<Text>" }` — field access
- `{ index: <Integer> }` — index access

Rules:
- `steps` MUST be present.
- `steps` MUST be a List.

---

## 8. Operator Nodes (Normative)

All non-reserved ops are treated as operator application nodes.

```codex
{ operation: "Add", arguments: [ /* expressions */ ] }
```

Rules:
1. If the operator takes arguments, `arguments` MUST be present.
2. Operator arity and typing rules are defined by the Behavior Vocabulary.
3. Evaluators MUST reject nodes that violate required fields for the operation.

---

## 9. Environment Contract (Normative)

Programs evaluate against an explicit environment map.

An environment is a Codex `Record` mapping `Text` keys to `EncodedValue`.

```codex
{
  w: { @paperhat: { concept: "Integer", value: "10" } },
  x: { @paperhat: { concept: "Integer", value: "20" } },
  currentTime: { @paperhat: { concept: "Instant", epochNanoseconds: "1705312200000000000" } }
}
```

Rules:
1. `Argument` is not part of `Environment`; it is provided separately as the primary input.
2. `Variable(name)` MUST resolve using `Environment[name]`.
3. If a variable is missing, evaluation MUST produce `Invalid(...)`, not an ambient default.

---

## 10. Reserved Tag Key (Normative)

The key `@paperhat` is reserved for tagged encodings.

If a Codex `Record` contains `@paperhat`, it MUST conform to a tagged encoding defined by this specification.

Unknown concepts under `@paperhat` MUST cause evaluation to produce `Invalid(...)` with code `BehaviorProgramEncoding::TAG_NOT_UNDERSTOOD`.

---

## 11. Versioning and Compatibility (Normative)

- `version` MUST be present and MUST equal `"0.1"` for this spec.
- Unknown `operation` values MUST be rejected with code `BehaviorProgramEncoding::OPERATION_NOT_UNDERSTOOD`.
- Extensions MUST be versioned by introducing a new `version`.

---

**End of Behavior Program Encoding v0.1**
