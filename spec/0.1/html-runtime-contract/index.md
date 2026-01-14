Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# HTML Runtime Contract

This specification defines what the Paperhat **HTML Runtime** MUST do.

This document is **Normative**.

---

## 1. Purpose

HTML Runtime provides the minimal browser-side runtime needed for Paperhat’s interactive HTML target.

It exists to:

- execute compiled Behavior Programs attached to the Presentation Plan
- update DOM state for progressive enhancement
- surface validation diagnostics to the user

HTML Runtime MUST be scoped to Paperhat only.

---

## 2. Authority and Boundaries (Normative)

HTML Runtime is NOT authoritative for authored meaning.

- Kernel is authoritative for semantics, validation compilation, and planning.
- HTML Runtime is authoritative only for browser interaction state and DOM effects.

HTML Runtime MUST NOT recompile Codex.

HTML Runtime MUST NOT typecheck Behavior Programs.

HTML Runtime MUST execute Behavior Programs exactly as encoded and as defined by:

- [Behavior Program Encoding](../behavior-program-encoding/)

See also:

- [Presentation Plan Encoding](../presentation-plan-encoding/)

---

## 3. Inputs (Normative)

HTML Runtime MUST accept:

- a Presentation Plan (or the subset needed for the current document)
- embedded Behavior Programs encoded as pure data
- an explicit evaluation environment (`Environment`) per evaluation (values from fields/constants/etc.)

HTML Runtime MUST NOT depend on ambient network access.

---

## 4. Behavior Program Execution (Normative)

HTML Runtime MUST be able to evaluate Behavior Programs encoded according to:

- [Behavior Program Encoding](../behavior-program-encoding/)

HTML Runtime MUST support arbitrarily nested programs.

HTML Runtime MUST treat a missing variable as an invalid result with diagnostics.

---

## 5. Core Runtime Types (Normative)

HTML Runtime MUST implement the following canonical result types.

The normative JSON shapes for these types are defined by:

- [HTML Runtime Data Shapes](../html-runtime-data-shapes/)

### 5.1 `Diagnostic`

A diagnostic MUST have, at minimum:

- `message` (string)
- `severity` (string)

A diagnostic MAY have:

- `path` (string)
- `hint` (string)
- `code` (string)

### 5.2 `Validation<T>`

HTML Runtime standardizes on `Validation` only:

- `Valid(value)`
- `Invalid(diagnostics)`

All runtime evaluation results MUST be representable as `Validation`.

---

## 6. Attachment Semantics (Normative)

HTML Runtime MUST support the following attachment kinds when present in the Presentation Plan:

- `Validate` — validates a value and yields diagnostics
- `ShowIf` — determines whether a node is shown
- `EnableIf` — determines whether a node is enabled

Attachment semantics are determined by attachment context.

### 6.1 Conditionals and Invalid Policy (Normative)

For `ShowIf` and `EnableIf`, HTML Runtime MUST interpret `Validation<boolean>` as:

- `Valid(true)` → true
- `Valid(false)` → false
- `Invalid(diagnostics)` → false

If `Invalid` is produced for a conditional, HTML Runtime MAY surface diagnostics in a debug or developer mode.

---

## 7. Progressive Enhancement (Normative)

HTML Runtime MUST support progressive enhancement.

Rules:

1. Base HTML output MUST be usable without client scripting.
2. When client scripting is available, HTML Runtime MUST bind DOM events and apply dynamic behavior.
3. HTML Runtime MUST update UI state deterministically based on program evaluation results.

---

## 8. Watch/Refresh Model (Informative)

In typical dev/watch operation:

- Workbench watches workspace files
- Workbench invokes Kernel to rebuild outputs
- the browser reloads or hot-refreshes
- HTML Runtime reattaches to the updated DOM and plan

---

**End of HTML Runtime Contract v0.1**
