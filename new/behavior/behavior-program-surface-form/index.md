Status: NORMATIVE  
Lock State: UNLOCKED  
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

v0.1 surface shape (Normative):

In v0.1, the canonical surface form uses the same core node shape as Behavior Program Encoding:

- A Program is a `Record` with:
	- `version` (`Text`) equal to `"0.1"`
	- `expression` (Expression)

- An Expression is a `Record` with:
	- `operation` (`Text`) naming a Behavior Vocabulary Concept
	- optional `arguments` (`List<Expression>`)
	- optional `value` (Codex value) for constant-like operations
	- optional `name` (`Text`) for name-bearing operations
	- optional `steps` (`List`) for path-bearing operations

No additional fields are permitted unless explicitly defined by Behavior Program Encoding.

---

## 4. Node Identity and Referencing (Normative)

Expression nodes MUST have stable program-local identity suitable for:

- deterministic diagnostic localization
- runtime attachment/binding

A node identity MUST be representable as a stable token value.

v0.1 node identity rule (Normative):

- Expression node identity MUST be derived structurally from the program root using an argument-path address.
- The canonical node identity token is the JSON-Pointer-like path to the expression record, using:
	- `/expression` for the root expression
	- `/arguments/<index>` segments when descending into argument lists

Example:

- `/expression/arguments/0/arguments/2`

Because identity is structural, v0.1 does not require an explicit `id` field on expression nodes.

---

## 5. Operator References (Normative)

`Apply` nodes reference an operator Concept from the Behavior Vocabulary.

Operator references MUST be stable and unambiguous.

v0.1 operator reference rule (Normative):

- An `Apply` operation references its operator by the `operation` token string.
- The token MUST match a Concept name defined by the applicable v0.1 Behavior Vocabulary specifications.
- Any unknown `operation` token MUST be rejected.

---

## 6. Relationship to Other Specifications

This specification works in conjunction with:

- Behavior Dialect — Semantics
- Behavior Vocabulary
- Any runtime binding specs (e.g., HTML runtime)

---

**End of Behavior Program Surface Form v0.1**
