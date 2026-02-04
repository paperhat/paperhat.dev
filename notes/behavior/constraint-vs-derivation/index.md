# Behavior in Workshop: Constraint vs Derivation, and SHACL Lowering

## Purpose

This document explains how **Behavior** fits into the **Paperhat Workshop Semantic Authoring System**, specifically:

* the separation between **Constraint Behavior** and **Derivation Behavior**
* how both forms are **normatively lowered** into **SHACL + SHACL-SPARQL** (and SHACL Rules)
* how Behavior integrates with **Codex**, the **triple store**, and **Workshop-rendering**

This is a continuity note intended to allow a future session to resume without re-deriving design decisions.

---

## Authority Model

### Normative Source of Truth

* The **normative reference** for schemas, meta-schemas, and domain data is always the **original Codex documents** stored in a **git repository** (versioned, reviewable, canonical).

### Triple Store as Projection

* The triple store is a **projection** of those Codex-authored ontologies and data.
* The projection MUST be **fully realized**:

  * no semantic loss
  * no “partial export”
  * the Codex-authored meaning must be represented completely as RDF triples
* Schemas and meta-schemas MUST compile to **Turtle** that creates **SHACL Shapes** (constraints) in the database.

---

## Identity and Reference Forms

### Canonical Identity

* **IRI is canonical** for identity and uniqueness (especially in the triple store).

### Tokens for Authoring Convenience

* Lookup tokens may exist for ergonomics, but MUST resolve deterministically to canonical IRIs under a governing schema.
* Tokens MUST NOT introduce an alternative identity system.

Rule:

* **Canonical identity is always IRI**. Tokens are authoring aliases only.

---

## Behavior Overview

Behavior is a declarative expression language authored in Codex. Its evaluation model is:

* **Pure** (no side effects)
* **Deterministic**
* **Runtime-neutral**
* **Total in failure handling**: evaluators never throw for user-authored input; they return:

  * `Valid(value)` or
  * `Invalid(diagnostics)`

Behavior includes:

* a typed value model aligned with Codex values (including `<Absent/>`)
* structural equality and comparability rules that are precisely specified
* a deterministic diagnostic system (stable codes, stable ordering, stable locations)

Behavior is used by Workshop to ensure identical semantics across:

* triple store validation
* server validation
* browser/runtime validation
* form generation (validators/formatters)
* downstream targets (PDF, spreadsheet, etc.)

---

## The Constraint vs Derivation Separation

Workshop distinguishes **two roles** for Behavior programs. This separation is mandatory for clarity, explainability, and determinism.

### 1) Constraint Behavior

Constraint Behavior answers:

> “Does this value satisfy the required condition?”

Characteristics:

* produces a validation judgment (conceptually Boolean / Validation)
* does not create new semantic facts
* is used to define **schema validity**
* powers form validation and authoritative data correctness

Examples:

* “age must be an integer between 0 and 130”
* “emailAddress must match a required structure”
* “a number must be (in [a,b] OR in [c,d]) AND integer”
* “all elements satisfy predicate P”

### 2) Derivation Behavior

Derivation Behavior answers:

> “Given a value, compute another value.”

Characteristics:

* produces a new value (normalization, formatting, projection, computed fields)
* used for projection, formatting, view construction, rendering, and form tooling
* does not determine schema validity unless explicitly paired with constraint behavior
* may create derived facts in the graph

Examples:

* normalize an email (casefold, normalization)
* format a phone number (E.164, national format)
* compute a full name from parts
* map/filter/reduce transforms
* computed keys used for joins or sorting

---

## No Optional Semantics

Workshop avoids “optional” features that lead to incompatible implementations.

Therefore:

* Constraint Behavior lowering is mandatory.
* Derivation Behavior lowering is mandatory.
* The lowering rules are normatively specified with **zero degrees of freedom**.

No approximation is permitted.

---

## Normative Lowering Targets (SHACL)

Because all schemas/meta-schemas MUST compile to SHACL constraints in the store, Behavior must be lowerable without loss.

### Constraint Behavior Lowering

Constraint Behavior MUST lower to SHACL using:

* **SHACL Core constraints** where expressible, and
* **SHACL-SPARQL constraints** where required

Requirement:

* Constraint Behavior semantics MUST be preserved exactly in the generated Shapes.

### Derivation Behavior Lowering

Derivation Behavior MUST lower to SHACL using:

* **SHACL Rules** (e.g., rule-based triple generation) and/or
* SHACL-SPARQL constructs suitable for deterministic derivation

Requirement:

* Derivation Behavior semantics MUST be preserved exactly in the generated Rules.
* Determinism MUST be preserved (no ambiguous rule firing, no engine-dependent freedom).

---

## Structured Value Representation

Workshop’s direction for rich “algebraic” value types (EmailAddress, PhoneNumber, ISBN, IPv4/IPv6, etc.):

### Canonical Representation

* Canonical representation is **node-shaped** in RDF:

  * a node with properties
  * validated by SHACL NodeShapes and PropertyShapes
  * supports querying, joins, and graph reasoning naturally

### Lexical Projection

* A lexical/string projection may be provided for UX and interchange,
* but such projection is **non-normative** unless explicitly specified later.

### Records in Codex

* Codex will include a first-class `record[...]` value form (planned):

  * `record[key: value, key: value]`
* Canonical RDF remains node-shaped; Records are an authoring/value convenience that must have deterministic lowering rules.

---

## Where Behavior Attaches (Open)

The exact attachment point for Behavior programs is not yet decided and must be discussed:

* attached directly to Trait definitions, or
* attached via an intermediate “value shape” Concept, or
* both with strict canonicalization to one model

This is intentionally left open for design discussion.

---

## Why the Separation Exists

The separation between constraint and derivation behavior exists because:

* Constraints answer “is valid?” and must remain explainable and stable.
* Derivations answer “compute this” and typically create new values/facts.
* Mixing them destroys:

  * diagnostic clarity
  * determinism guarantees
  * schema validity boundaries
  * governance and conformance

Workshop supports both—but keeps them distinct and normatively defined.

---

## Summary of Decisions Made

1. **IRI is canonical identity**; tokens may exist only as deterministic authoring aliases.
2. **Codex in git is the normative reference**; triple store is a fully realized projection.
3. **All schemas and meta-schemas MUST compile to Turtle that creates SHACL Shapes** in the store.
4. Behavior is split into:

   * **Constraint Behavior** (lowers to SHACL Core + SHACL-SPARQL constraints)
   * **Derivation Behavior** (lowers to SHACL Rules / equivalent deterministic SHACL-based rule constructs)
5. There is **no optionality**: lowering rules are normative, deterministic, and lossless.
6. Rich value types (EmailAddress, PhoneNumber, etc.) are **canonically node-shaped** in RDF.
7. Codex will add **first-class `record[...]`** values; lowering must remain deterministic and compatible with node-shaped canonical RDF.
8. The exact schema attachment point for Behavior is **TBD** and must be discussed next.

---

## Next Discussion Topics

To continue from here, the next decisions to lock down are:

1. Canonical attachment model for Behavior programs in schemas (Trait-level vs value-shape Concepts).
2. Normative lowering rules:

   * Behavior operator → SHACL Core / SPARQL constraint pattern
   * Derivation operator → SHACL Rule pattern
3. Canonical RDF encoding for `record[...]` and its interaction with node-shaped values.
4. Deterministic rule semantics (ordering/fixpoint) required to ensure cross-engine compatibility.

**End of document**
