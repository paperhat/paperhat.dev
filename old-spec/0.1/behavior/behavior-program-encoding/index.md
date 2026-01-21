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

- embedded into Presentation Plans
- evaluated in the Kernel (native execution)
- evaluated in the HTML runtime (browser user-agent)

This spec defines the default v0.1 encoding as a **Codex opcode tree**.

Clarification (Normative):

- The Behavior semantic value model is defined by Behavior Dialect Semantics; this document specifies how Behavior Programs and their values are represented as Codex values for interchange.
- Implementations MAY serialize Codex values into a transport format as needed by their environment, but serialization is out of scope for this specification.

---

## 2. Non-goals

- This spec does not define the full Behavior Dialect (operator typing rules and signatures); that is defined by the Behavior Dialect specification.
- This spec does not require any particular programming language runtime.
- This spec does not define UI attachment semantics (Validate/ShowIf/etc.); those are defined by Presentation Plan and HTML runtime contracts.

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

- `version` (string) — MUST equal `"0.1"`
- `expression` (Expression) — the root expression node

Example:

```codex
{
  "version": "0.1",
  "expression": { "operation": "And", "arguments": [ {"operation": "IsInteger", "arguments": [{"operation": "Argument"}] } ] }
}
```

---

## 5. Expression Node Shape (Normative)

An Expression node MUST be a Codex `Record` with:

- `operation` (string) — a stable token naming a Behavior Vocabulary Concept

An Expression node MAY include:

- `arguments` (array of Expression)
- `value` (EncodedValue, depending on operation)
- `name` (string, for name-bearing ops)
- `steps` (array of PathStep, for path-bearing ops)

No additional fields are permitted unless explicitly defined by this spec.

---

## 5.1 Encoded Values (`EncodedValue`) (Normative)

An `EncodedValue` MUST be a valid Codex value that encodes a Behavior semantic value.

Normative rules:

1. `<Absent/>` MUST be encoded as a tagged Codex `Record`:

```codex
{ "@paperhat": { "concept": "Absent" } }
```

2. `Boolean` values are encoded as Codex `Boolean` values.
3. `Text` values are encoded as Codex `Text` values.
4. Untagged numeric literals MAY be used as an encoding for an implementation-defined `RealNumber` value.

  - Because `RealNumber` is not orderable in v0.1, authors MUST use tagged numeric encodings (below) whenever ordering/comparability is required.

5. `List` values are encoded as Codex `List` values whose elements are `EncodedValue`.
6. `Record` values are encoded as Codex `Record` values whose field values are `EncodedValue`.

### 5.1.1 Tagged numeric encodings (Normative)

v0.1 defines tagged encodings for orderable numeric domains. These encodings MUST be used to preserve exactness and cross-runtime determinism.

#### `Integer`

Encoding:

```codex
{ "@paperhat": { "concept": "Integer", "value": "-12" } }
```

Rules (Normative):

- `value` MUST be a base-10 integer string matching `-?(0|[1-9][0-9]*)`.

#### `Fraction`

Encoding:

```codex
{ "@paperhat": { "concept": "Fraction", "numerator": "-3", "denominator": "4" } }
```

Rules (Normative):

- `numerator` MUST be a base-10 integer string matching `-?(0|[1-9][0-9]*)`.
- `denominator` MUST be a base-10 integer string matching `(0|[1-9][0-9]*)`.
- `denominator` MUST NOT be `"0"`.
- The sign MUST be carried by `numerator`; `denominator` MUST be non-negative.

Normalization (Normative):

Encoders MUST emit Fractions in canonical normalized form:

- Let $n$ be the integer value of `numerator` and $d$ be the integer value of `denominator`.
- $d$ MUST be $> 0$.
- If $n = 0$, the canonical encoding MUST be `numerator: "0"` and `denominator: "1"`.
- Otherwise, let $g = \gcd(|n|, d)$; encoders MUST emit $n' = n/g$ and $d' = d/g$.

Decoders MUST accept any well-formed Fraction encoding and MUST normalize it to the canonical semantic form before evaluation.

#### `PrecisionNumber`

Encoding:

```codex
{ "@paperhat": { "concept": "PrecisionNumber", "decimal": "12.3400" } }
```

Rules (Normative):

- `decimal` MUST be a base-10 decimal string with an explicit scale, matching `-?(0|[1-9][0-9]*)(\.[0-9]+)?`.
- Exponent notation MUST NOT be used.
- Trailing zeros in the fractional part MUST be preserved; they are semantically significant for `PrecisionNumber`.

Normalization (Normative):

- Encoders MUST preserve the authored `decimal` string exactly.
- Decoders MUST NOT remove trailing zeros or otherwise change the scale.

Reserved tag key (Normative):

- The key `"@paperhat"` is reserved for tagged encodings (like `<Absent/>`). If a Codex `Record` contains `"@paperhat"`, it MUST conform to a tagged encoding defined by this specification.

---

## 6. Core Reserved Ops (Normative)

The following ops are reserved and have encoding defined by this spec:

### 6.1 `Argument`

Represents the primary input value.

Encoding:

```codex
{ "operation": "Argument" }
```

### 6.2 `Variable`

Represents a lookup in the evaluation environment.

Encoding:

```codex
{ "operation": "Variable", "name": "someName" }
```

Rules:

1. `name` MUST be present.
2. Variable name canonicalization rules are defined by the Behavior Dialect or the embedding contract.

### 6.3 `Constant`

Represents a literal constant.

Encoding:

```codex
{ "operation": "Constant", "value": 123 }
```

Rules:

1. `value` MUST be present.
2. `value` MUST be a valid `EncodedValue`.

### 6.4 `Field`

Represents a field lookup on a Record-like value.

Encoding:

```codex
{ "operation": "Field", "name": "fieldName" }
```

Rules:

1. `name` MUST be present.

### 6.5 `Path`

Represents a bounded path traversal.

Encoding:

```codex
{ "operation": "Path", "steps": [ { "field": "a" }, { "field": "b" } ] }
```

PathStep encoding (Normative):

- A PathStep MUST be one of:
  - `{ "field": "<Text>" }`
  - `{ "index": <Integer> }`

Rules:

1. `steps` MUST be present.
2. `steps` MUST be an array.

---

## 7. Operator Nodes (Normative)

All non-reserved ops are treated as operator application nodes.

Encoding:

```codex
{ "operation": "And", "arguments": [ /* expressions */ ] }
```

Rules:

1. If the operator takes arguments, `arguments` MUST be present.
2. Operator arity and typing rules are owned by the Behavior Dialect spec.
3. Evaluators MUST reject nodes that violate required fields for the operation.

---

## 8. Environment (`Environment`) Contract (Normative)

Programs evaluate against an explicit environment map.

An environment is a Codex `Record` mapping `Text` keys to `EncodedValue`.

Example:

```codex
{
  "w": 10,
  "x": 20,
  "y": 30,
  "z": 40
}
```

Rules:

1. `Argument` is not part of `Environment`; it is provided separately as the primary input.
2. `Variable(name)` MUST resolve using `Environment[name]`.
3. If a variable is missing, evaluation MUST produce an invalid result (diagnostic), not an ambient default.

---

## 9. Versioning and Compatibility (Normative)

- `version` MUST be present and MUST equal `"0.1"` for this spec.
- Unknown `operation` values MUST be rejected unless a higher-level contract explicitly permits extension.
- Extensions MUST be versioned by introducing a new `version`.

---

## 10. Example (Informative)

Example program fragment (conceptual):

```codex
{
  "version": "0.1",
  "expression": {
    "operation": "And",
    "arguments": [
      { "operation": "IsInteger", "arguments": [{ "operation": "Argument" }] },
      {
        "operation": "Or",
        "arguments": [
          {
            "operation": "And",
            "arguments": [
              { "operation": "IsMoreThan", "arguments": [{ "operation": "Variable", "name": "w" }, { "operation": "Argument" }] },
              { "operation": "IsNoMoreThan", "arguments": [{ "operation": "Variable", "name": "x" }, { "operation": "Argument" }] }
            ]
          },
          {
            "operation": "And",
            "arguments": [
              { "operation": "IsNoLessThan", "arguments": [{ "operation": "Variable", "name": "y" }, { "operation": "Argument" }] },
              { "operation": "IsLessThan", "arguments": [{ "operation": "Variable", "name": "z" }, { "operation": "Argument" }] }
            ]
          }
        ]
      }
    ]
  }
}
```

---

**End of Behavior Program Encoding v0.1**
