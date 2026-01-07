# Codex CDX → IR Boundary Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all tooling that consumes Codex (`.cdx`) files and produces an intermediate representation (IR)

---

## 1. Purpose

This contract defines the **boundary between Codex (CDX)** and the **Intermediate Representation (IR)** used by downstream systems (e.g. Scribe, renderers, planners, exporters).

Its goals are to:

- make responsibilities at the boundary explicit
- prevent semantic leakage across layers
- guarantee deterministic, tool-independent interpretation
- allow multiple downstream targets without reinterpreting CDX

This contract governs **what CDX guarantees to IR**, and **what IR must not assume**.

---

## 2. Role of Codex (CDX)

Codex is a **semantic authoring language**.

CDX is responsible for:

- declaring **Concepts**, **Traits**, **Values**, and **Content**
- enforcing canonical surface form
- validating against schema
- enforcing identity, reference, collection, and context rules
- producing a deterministic semantic structure

CDX describes **what exists**, not how it is rendered, stored, or executed.

---

## 3. Role of the IR

The IR is a **normalized semantic representation** derived from CDX.

The IR exists to:

- serve as a stable interface between CDX and downstream systems
- enable compilation to multiple targets (HTML, voice, documents, APIs, etc.)
- support analysis, querying, planning, and transformation

The IR is **not authored directly** by humans.

---

## 4. Boundary Guarantee (Normative)

A valid CDX document guarantees that:

- all Concepts are well-formed and schema-valid
- all Traits are authorized and correctly typed
- all Entities have explicit, valid identifiers
- all references point to valid Entities
- all collections obey schema-defined semantics
- all context-sensitive meanings are resolved

The IR MUST NOT need to re-validate CDX semantics.

---

## 5. What CDX Does _Not_ Guarantee

CDX does **not** guarantee:

- rendering intent
- presentation structure
- layout or styling
- execution order
- evaluation semantics
- target-specific constraints

Any such assumptions belong **after** the IR boundary.

---

## 6. Semantic Preservation (Normative)

The transformation from CDX to IR MUST be:

- **lossless** with respect to semantic meaning
- **deterministic**
- **independent of surface formatting**
- **independent of file layout or ordering**

The IR MUST preserve:

- Concept identity
- Trait values
- collection membership and ordering (when semantic)
- explicit relationships and references
- declared provenance

---

## 7. Content Handling

CDX **Content** is opaque.

At the boundary:

- Content MUST be preserved verbatim
- Content MUST NOT be interpreted or transformed
- Content MUST NOT be used to infer semantics

Downstream systems MAY choose to interpret Content, but only **after** the IR.

---

## 8. Identity and References

At the CDX → IR boundary:

- Entity identity is explicit and stable
- References are resolved by identifier, not by position or structure
- No implicit relationships are introduced

The IR MUST NOT invent identity or relationships.

---

## 9. Error Responsibility

All errors in the following categories MUST be resolved **before** IR generation:

- parse errors
- surface form errors
- schema errors
- identity errors
- reference errors
- collection errors
- context errors

The IR MUST assume **error-free input**.

---

## 10. Non-Goals

This contract does **not**:

- define the structure of the IR
- mandate a specific IR format
- define triple encodings
- prescribe query languages
- define rendering pipelines

It defines **responsibility boundaries**, not implementations.

---

## 11. Summary

- CDX is authoritative for semantics
- IR is authoritative for downstream processing
- The boundary is strict and explicit
- Semantics must be fully resolved before IR
- Downstream systems must not reinterpret CDX
