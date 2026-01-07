# Codex Formatting Error Rules (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex formatters, validators, and normalization tooling

---

## 1. Purpose

This contract defines **how formatting-related errors are classified and handled** in Codex.

Its goals are to:

- draw a hard boundary between parsing, formatting, and semantics
- make canonicalization deterministic and enforceable
- eliminate heuristic or “best-effort” formatting behavior
- ensure round-tripping without reliance on source offsets

This contract governs **formatting and normalization errors only**.

---

## 2. Formatting Phases

Codex processing follows this strict sequence:

1. **Parse**
2. **Validate**
3. **Normalize (canonicalize)**
4. _(Optional)_ Re-parse canonical form

Formatting errors may arise in phases 2 or 3, but **never** alter phase ordering.

---

## 3. Parse vs Formatting Errors (Normative)

### Parse Errors

Parse Errors occur when the input cannot be read into a syntactic structure.

Examples:

- malformed tags
- invalid quoting
- broken indentation
- unterminated Concepts

Parse Errors halt processing immediately.

---

### Formatting Errors

Formatting Errors occur when:

- input parses successfully
- but violates **canonical surface form rules**

Formatting Errors are **distinct from semantic or schema errors**.

---

## 4. Canonical Form Requirement (Normative)

Every valid Codex document MUST normalize to **exactly one canonical textual form**.

If canonicalization is not possible, the document is invalid.

There is no “closest” or “best-effort” canonical form.

---

## 5. Classes of Formatting Errors

Formatting Errors include (non-exhaustive):

- expanded empty Concepts
- non-canonical indentation
- invalid whitespace placement
- invalid casing of Concept or Trait names
- multiple blank lines where forbidden
- blank lines in invalid positions
- non-canonical attribute ordering
- invalid line continuations

Each violation is a **formatting error**, not a schema error.

---

## 6. Formatter Behavior (Normative)

Codex formatters:

- MUST produce canonical output
- MUST NOT reorder Concepts or collections
- MUST NOT invent or remove Concepts or Traits
- MUST NOT infer missing structure
- MUST NOT depend on source offsets

Formatting is purely mechanical.

---

## 7. Normalization Failures

A **normalization failure** occurs when:

- input parses and validates
- but cannot be transformed into canonical form

Normalization failures are **fatal formatting errors**.

Examples:

- ambiguous indentation
- conflicting sectioning rules
- invalid but unfixable whitespace patterns

---

## 8. Formatting vs Schema Errors

The following distinctions are mandatory:

- Formatting Errors concern **how** Codex is written
- Schema Errors concern **what** Codex means

A document MAY have both, but errors MUST be classified correctly.

Tools MUST NOT report schema errors when the true cause is formatting.

---

## 9. Error Reporting Requirements

Formatting error reports SHOULD include:

- error classification: `FormattingError`
- violated rule reference (surface form section)
- location (line number or Concept path)
- expected canonical form (if applicable)

Exact wording and UI presentation are tool-defined.

---

## 10. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

- silently normalize invalid input
- auto-correct formatting errors without reporting them
- accept multiple canonical forms
- treat formatting errors as warnings

If formatting is wrong, the document is invalid.

---

## 11. Non-Goals

This contract does **not**:

- define editor integrations
- prescribe auto-format-on-save behavior
- define diff or patch semantics
- define pretty-printing options
- replace the Surface Form Contract

It strictly defines **error classification and enforcement**.

---

## 12. Summary

- Canonical formatting is mandatory
- Formatting errors are distinct from parse and schema errors
- Normalization must be deterministic or fail
- No heuristic or silent correction is permitted
- Codex formatting is mechanical and enforceable
