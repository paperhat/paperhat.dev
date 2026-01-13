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

This spec defines the default v0.1 encoding as a **JSON opcode tree**.

---

## 2. Non-goals

- This spec does not define the full Behavior Dialect (operator typing rules and signatures); that is defined by the Behavior Dialect specification.
- This spec does not require any particular programming language runtime.
- This spec does not define UI attachment semantics (Validate/ShowIf/etc.); those are defined by Presentation Plan and HTML runtime contracts.

---

## 3. Determinism and Safety (Hard)

1. A Behavior Program MUST be pure data.
2. A Behavior Program MUST NOT embed executable code (for example: functions, scripts, bytecode, closures).
3. A Behavior Program MUST NOT require network access to evaluate.
4. A Behavior Program MUST be deterministic given:
   - the Program
  - an explicit evaluation environment (`Environment`)

---

## 4. Program Envelope (Hard)

A Behavior Program MUST be a JSON object with:

- `version` (string) — MUST equal `"0.1"`
- `expression` (Expression) — the root expression node

Example:

```json
{
  "version": "0.1",
  "expression": { "operation": "And", "arguments": [ {"operation": "IsInteger", "arguments": [{"operation": "Argument"}] } ] }
}
```

---

## 5. Expression Node Shape (Hard)

An Expression node MUST be a JSON object with:

- `operation` (string)

An Expression node MAY include:

- `arguments` (array of Expression)
- `value` (JSON scalar or JSON object/array, depending on operation)
- `name` (string, for name-bearing ops)

No additional fields are permitted unless explicitly defined by this spec.

Implementations SHOULD validate encoded programs against the v0.1 JSON Schema:

- `gh-pages-specs/paperhat.dev/spec/0.1/behavior-program-encoding/schema/behavior-program-encoding.schema.json`

---

## 6. Core Reserved Ops (Hard)

The following ops are reserved and have encoding defined by this spec:

### 6.1 `Argument`

Represents the primary input value.

Encoding:

```json
{ "operation": "Argument" }
```

### 6.2 `Variable`

Represents a lookup in the evaluation environment.

Encoding:

```json
{ "operation": "Variable", "name": "someName" }
```

Rules:

1. `name` MUST be present.
2. Variable name canonicalization rules are defined by the Behavior Dialect or the embedding contract.

### 6.3 `Constant`

Represents a literal constant.

Encoding:

```json
{ "operation": "Constant", "value": 123 }
```

Rules:

1. `value` MUST be present.
2. `value` MUST be valid JSON.

---

## 7. Operator Nodes (Normative)

All non-reserved ops are treated as operator application nodes.

Encoding:

```json
{ "operation": "And", "arguments": [ /* expressions */ ] }
```

Rules:

1. If the operator takes arguments, `arguments` MUST be present.
2. Operator arity and typing rules are owned by the Behavior Dialect spec.
3. Evaluators MUST reject nodes that violate required fields for the operation.

---

## 8. Environment (`Environment`) Contract (Normative)

Programs evaluate against an explicit environment map.

An environment is a JSON object mapping strings to JSON values.

Example:

```json
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

## 9. Versioning and Compatibility (Hard)

- `version` MUST be present and MUST equal `"0.1"` for this spec.
- Unknown `operation` values MUST be rejected unless a higher-level contract explicitly permits extension.
- Extensions MUST be versioned by introducing a new `version`.

---

## 10. Example (Informative)

Example program fragment (conceptual):

```json
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
