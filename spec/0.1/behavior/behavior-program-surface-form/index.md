Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Program Surface Form

This specification defines the **Codex surface form** for Behavior Programs.

This is the authoring and compiled artifact format for Behavior expressions in the Paperhat ecosystem.

This document is **Normative**.

---

## 1. Scope

This spec defines:

- how a Behavior Program is represented in Codex
- the required Concepts and Traits used to represent expressions
- stability requirements for node identity, to support deterministic diagnostics and runtime binding

This spec does not define:

- the operator inventory (see Behavior Vocabulary)
- evaluation semantics (see Behavior Dialect — Semantics)
- any particular wire format (TOML, CBOR, etc.). Wire formats, if any, are treated as encodings of this surface form.

---

## 2. Program Model (Normative)

A Behavior Program represents exactly one expression tree.

The root expression is the semantic program.

---

## 3. Required Core Concepts (Normative)

The following Concepts are required in the Behavior Program surface form:

- `BehaviorProgram`
- `Argument`
- `Variable`
- `Constant`
- `Apply`

(TBD: exact names, trait sets, and child shapes; coordinate with the sibling mapping tables.)

---

## 4. Node Identity and Referencing (Normative)

Expression nodes MUST have stable program-local identity suitable for:

- deterministic diagnostic localization
- runtime attachment/binding

A node identity MUST be representable as a stable token value.

(TBD: whether this is a required `id` trait on every expression node, or derived structurally.)

---

## 5. Operator References (Normative)

`Apply` nodes reference an operator Concept from the Behavior Vocabulary.

Operator references MUST be stable and unambiguous.

(TBD: whether operator reference is by `name`, `id`, or a fixed vocabulary IRI.)

---

## 6. Relationship to Other Specifications

This specification works in conjunction with:

- Behavior Dialect — Semantics
- Behavior Vocabulary
- Any runtime binding specs (e.g., HTML runtime)

---

**End of Behavior Program Surface Form v0.1**
