Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# HTML Runtime Data Shapes

This specification defines the canonical **data shapes** used by Paperhat HTML Runtime.

This document is **Normative**.

---

## 1. Purpose

HTML Runtime must interoperate with:

- Kernel outputs (Presentation Plan + embedded Behavior Programs)
- browser-side state
- DOM bindings

This spec exists to define the canonical JSON shapes for:

- `Diagnostic`
- `Validation`

---

## 2. Diagnostic (Hard)

A `Diagnostic` MUST be a JSON object.

Fields:

- `message` (string, required)
- `severity` (string, required)
- `code` (string, optional)
- `path` (string, optional)
- `hint` (string, optional)

Rules:

1. Unknown fields MUST be ignored by the HTML Runtime.
2. `severity` MUST be one of:
   - `error`
   - `warning`
   - `info`

Example:

```json
{
  "message": "Age must be an integer",
  "severity": "error",
  "path": "modules/People/data/person-123/data.cdx",
  "hint": "Use a whole number"
}
```

---

## 3. Validation (Hard)

`Validation` is the only runtime result type.

A `Validation<T>` MUST be encoded as one of the following JSON objects:

### 3.1 Valid

```json
{ "kind": "Valid", "value": "..." }
```

Rules:

- `kind` MUST equal `Valid`
- `value` MUST be present

### 3.2 Invalid

```json
{ "kind": "Invalid", "diagnostics": [ { "message": "...", "severity": "error" } ] }
```

Rules:

- `kind` MUST equal `Invalid`
- `diagnostics` MUST be present
- `diagnostics` MUST be an array (may be empty)

---

## 4. Relationship to Behavior Evaluation (Normative)

Behavior Program evaluation in the HTML runtime MUST yield a `Validation`.

The Behavior Program interchange format is defined by:

- [Behavior Program Encoding](../behavior-program-encoding/)

---

**End of HTML Runtime Data Shapes v0.1**
