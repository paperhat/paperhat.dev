Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# View Composition: Slots, Fills, and Use Specification

This specification defines **View Composition** in Paperhat: how Views support deterministic composition, reuse, and overrides without changing semantic truth or introducing target-specific behavior.

This document governs **composition semantics only**.
It extends the Codex View Definition Specification.

This document is **Normative**.

---

## 1. Purpose

View Composition exists to:

- allow Views to declare deterministic extension points
- allow assemblies to provide deterministic overrides
- allow View reuse without copying structure
- preserve the View contract: selection + structure + meaningful order, with no presentation and no behavior

A View Composition mechanism answers one question only:

> Given a View, what deterministic structural substitutions and inclusions are applied before ViewModel creation?

---

## 2. Relationship to View Definition (Normative)

The Codex View Definition Specification defines the View kernel: inclusion, structure, and meaningful order.

This specification defines additional View constructs that MAY appear inside Views.

Rules:

- View Composition constructs MUST NOT introduce new domain semantics.
- View Composition constructs MUST NOT change the meaning of projected data.
- View Composition constructs MUST be deterministic and mechanically enforceable.

---

## 2.1 See Also (Informative)

- Pipeline responsibilities for this step: [ViewModel Construction and Composition Resolution](../../../../../../libraries/pipeline/spec/0.1/viewmodel-construction-and-composition-resolution/)

---

## 3. Core Invariants (Hard)

1. **No semantic truth changes.** Composition MUST NOT introduce or modify semantic facts.
2. **No target leakage.** Composition MUST NOT reference targets, renderers, or presentation systems.
3. **Deterministic resolution.** Given identical View Graph and identical external fills, resolved Views MUST be identical.
4. **No computation.** Composition MUST NOT contain conditionals, queries, arithmetic, or state.
5. **Recordability.** A resolved View SHOULD be reproducible and auditable given provenance.

---

## 4. Concepts (Normative)

This specification defines the following composition constructs:

- `Slot` — a named placeholder within a View
- `Fill` — content that supplies a Slot
- `Use` — a structural inclusion of another View

This specification does not define additional projection primitives.
Field projection is already expressed in the View Definition specification via `Text` and binding-relative `source` paths.

---

## 5. Slot (Normative)

A `Slot` is a named placeholder within a View.

Slots:

- reserve a position in the View structure
- do not select data
- do not introduce semantics
- do not affect identity

### 5.1 Traits

A Slot MUST define:

- `name` — required unique token within the View

A Slot MAY define:

- `sequence` — boolean; default `false`

### 5.2 Constraints

- A Slot MUST be self-closing.
- Slot `name` values MUST be unique within the View.

---

## 6. Fill (Normative)

A `Fill` supplies content for a named Slot.

Fills are declarative and structural only.

### 6.1 Local Fill

A **Local Fill** MAY appear inside the same View that declares the Slot.

A Local Fill MUST define:

- `slot` — required Slot name

A Local Fill MAY define:

- `mode` — `replace|prepend|append`; default `replace`

### 6.2 External Fill

An **External Fill** is a Fill provided from outside the View as an explicit input during compilation/assembly.

This specification does not mandate where external fills are authored.
It only defines the meaning of an external fill when supplied.

An External Fill MUST define:

- `view` — required View id
- `slot` — required Slot name

An External Fill MAY define:

- `mode` — `replace|prepend|append`; default `replace`

### 6.3 Fill Content

Fill bodies MAY contain any View structural content that is allowed at the Slot location.

Fill bodies MUST NOT:

- contain `Fill` nodes

---

## 7. Use (Normative)

A `Use` node includes another View’s structure at a specific position.

### 7.1 Traits

A Use MUST define:

- `view` — required View id

### 7.2 Constraints

- Use MUST be self-closing.
- The referenced View id MUST exist.
- The referenced View MUST be valid when evaluated under the current binding context.

Use does not change binding context.

---

## 8. Slot Resolution (Normative)

Slot resolution is deterministic.

### 8.1 Precedence

For a given `(View, Slot)`:

1. External Fill
2. Local Fill
3. Empty (no content)

### 8.2 Modes

If both an external fill and a local fill exist:

- `replace` (default): external replaces local
- `prepend`: external content is placed before local
- `append`: external content is placed after local

Rules:

- `prepend` and `append` are legal only if the Slot declares `sequence=true`.
- If `sequence=false`, any non-`replace` mode is a validation error.

### 8.3 Conflicts

- Multiple external fills for the same `(View, Slot)` are errors.
- Multiple local fills for the same Slot are errors.

---

## 9. Compilation and Pipeline Integration (Normative)

Pipeline MUST:

- validate composition constructs
- resolve Slot/Fills deterministically
- resolve Use deterministically
- produce a resolved View structure prior to ViewModel creation

Resolved View structure MUST be target-independent.

---

## 10. Non-Goals (Normative)

View Composition MUST NOT:

- encode Design Policy
- encode rendering, layout, typography, or styling
- encode behavior or interaction
- include conditionals, queries, or computation

---

## 11. Summary

- Slots define deterministic extension points.
- Fills supply content for Slots, with deterministic precedence.
- Use enables deterministic structural reuse.
- Projection remains governed by View Definition (`Text`, `source` paths, binding contexts).
- Composition does not change semantic truth and does not introduce targets.

---

**End of View Composition Specification v0.1**
