Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Presentation Plan Encoding

This specification defines the canonical **Codex interchange encoding** for a Paperhat **Presentation Plan payload** as exchanged between:

- the Paperhat **Kernel** (producer)
- the Paperhat **HTML Runtime** (consumer)

This document is **Normative**.

---

## 1. Purpose

The Presentation Plan Definition specification defines what a Presentation Plan *is* and what it may contain.

This specification defines one concrete, runtime-facing serialization for a subset of the Presentation Plan sufficient for:

- stable node identity
- attaching and executing embedded Behavior Programs
- deterministic DOM binding for progressive enhancement

---

## 2. Scope

This specification governs:

- the Codex shape of a Presentation Plan payload consumed by HTML Runtime
- attachment encoding for `Validate`, `ShowIf`, and `EnableIf`
- binding sources for `Argument` and `Environment` values

This specification does **not** govern:

- the full Presentation Plan ontology
- rendering, styling, or layout
- Behavior Program semantics (owned by Behavior Dialect)
- any particular transport serialization of this payload

---

## 3. Determinism and Safety (Normative)

1. A Presentation Plan payload MUST be pure data.
2. A Presentation Plan payload MUST NOT embed executable code.
3. Evaluation inputs MUST be explicit via `argument` and `environment` bindings.
4. For identical inputs, Kernel MUST emit byte-for-byte equivalent payloads when serialized using a canonical policy.

---

## 4. Payload Envelope (Normative)

A Presentation Plan payload MUST be a Codex `Record` with:

- `version` (string) — MUST equal `"0.1"`
- `root` (string) — the root `nodeId`
- `nodes` (array of `PlannedNode`)

Example:

```codex
{
  "version": "0.1",
  "root": "n_root",
  "nodes": [
    { "id": "n_root", "children": ["n_field"], "attachments": [] },
    {
      "id": "n_field",
      "children": [],
      "attachments": [
        {
          "id": "a_validate_field",
          "kind": "Validate",
          "argument": { "kind": "FieldValue", "fieldId": "email" },
          "environment": {},
          "program": { "version": "0.1", "expression": { "operation": "IsString", "arguments": [{ "operation": "Argument" }] } }
        }
      ]
    }
  ]
}
```

---

## 5. Planned Nodes (Normative)

A `PlannedNode` MUST be a Codex `Record` with:

- `id` (string) — stable within the payload
- `children` (array of string) — ordered child `nodeId`s
- `attachments` (array of `Attachment`) — MAY be empty

A `PlannedNode` MAY include:

- `role` (string) — a target-neutral role label for renderer consumption

Rules:

1. Node IDs MUST be unique within the payload.
2. All `children` MUST refer to existing node IDs.
3. Cycles are forbidden.

---

## 6. Attachments (Normative)

An `Attachment` MUST be a Codex `Record` with:

- `id` (string) — unique within the payload
- `kind` (string) — MUST be one of: `Validate`, `ShowIf`, `EnableIf`
- `program` (Behavior Program) — encoded per Behavior Program Encoding v0.1
- `argument` (BindingSource) — provides the `Argument` value
- `environment` (Record) — maps variable names to `BindingSource`

Rules:

1. Attachment IDs MUST be unique within the payload.
2. For a given node, multiple attachments MAY exist, but attachment order MUST be explicit and deterministic.
3. A single node MUST NOT contain multiple attachments of the same `kind`.

---

## 7. Binding Sources (Normative)

A `BindingSource` MUST be a Codex `Record` with:

- `kind` (string)

Supported kinds in v0.1:

### 7.1 `Constant`

- `kind`: `"Constant"`
- `value`: any Codex value

### 7.2 `FieldValue`

- `kind`: `"FieldValue"`
- `fieldId`: string

Semantics:

- Produces the current UI value for the field identified by `fieldId`.

### 7.3 `NodeValue`

- `kind`: `"NodeValue"`
- `nodeId`: string

Semantics:

- Produces an implementation-defined value associated with `nodeId`.
- If no value exists, the binding MUST evaluate to `Invalid(...)`.

---

## 8. Attachment Result Expectations (Normative)

HTML Runtime MUST interpret attachment results as:

- `Validate` MUST evaluate to `Validation<any>`; invalid diagnostics are surfaced.
- `ShowIf` MUST evaluate to `Validation<boolean>`; `Invalid` is treated as false.
- `EnableIf` MUST evaluate to `Validation<boolean>`; `Invalid` is treated as false.

(Conditional invalid policy is further constrained by the HTML Runtime contract.)

---

## 9. Versioning and Compatibility (Normative)

- `version` MUST equal `"0.1"`.
- Unknown `kind` values MUST be rejected.
- Unknown `BindingSource.kind` values MUST be rejected.

---

**End of Presentation Plan Encoding v0.1**
