Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat System Contract

This document defines the **system-level authority, responsibilities, boundaries, and invariants** of **Paperhat**.

It is the **highest-authority normative document** for the Paperhat system.

---

## 1. Purpose

This contract exists to:

* define **what Paperhat is**, at the system level
* establish **authority and precedence** across Paperhat documentation
* define the **non-negotiable invariants** of the system
* clarify the relationship between languages, libraries, tooling, and artifacts
* prevent semantic drift, misclassification, or accidental framework behavior

All other Paperhat documents are interpreted in the context of this contract.

---

## 2. Scope

This contract governs:

* the Paperhat system as a whole
* all Paperhat specifications, contracts, and normative documentation
* the roles and boundaries of Paperhat libraries
* the relationship between authored artifacts and implementations

This contract does **not** govern:

* any specific software implementation
* licensing of implementations
* deployment, hosting, or operational practices
* external systems that consume Paperhat outputs

---

## 3. System Definition

**Paperhat is a semantic authoring and processing system.**

Paperhat consists of:

* declarative semantic languages
* formal specifications
* bounded libraries with exclusive responsibilities
* a deterministic processing pipeline
* optional tooling for authoring, development, and realization

Paperhat is defined by **documents**, not by code.

---

## 4. Non-Framework Declaration (Normative)

Paperhat is **not** a framework.

Specifically:

* Paperhat does not impose a runtime
* Paperhat does not define application lifecycle hooks
* Paperhat does not own execution control flow
* Paperhat does not require a server or event loop
* Paperhat does not embed behavior into authored content

Execution is **optional, external, and non-authoritative**.

Any Paperhat component that introduces required runtime behavior is in violation of this contract.

---

## 5. Core System Invariants (Normative)

The following invariants are **non-negotiable**:

1. **Meaning is authored as data**
2. **Structure is separate from prose**
3. **Presentation is planned, not embedded**
4. **Rendering is realization, not policy**
5. **Pipelines are explicit and deterministic**
6. **Purity and IO are strictly separated**
7. **Authority resides in documentation**
8. **Nothing implicit is allowed to become normative**

All Paperhat specifications and libraries MUST uphold these invariants.

---

## 6. Languages (Normative)

Paperhat includes the following languages:

### 6.1 Codex

* a declarative semantic authoring language
* used to define Concepts, Traits, Values, identity, structure, and schemas
* authoritative source of semantic meaning

### 6.2 Gloss

* an inline semantic span-binding language
* used only to bind Codex-defined meaning to spans of text
* subordinate and dependent on Codex

No other language may assert semantic meaning within Paperhat unless explicitly authorized by specification.

---

## 7. Modules (Normative)

A **Module** is the primary unit of composition in Paperhat.

A Module:

* is a semantic assembly of heterogeneous artifacts
* has a single semantic root
* is inspectable, queryable, and graph-addressable
* exists independently of any target or runtime

Modules are defined semantically by Codex and assembled physically according to the **Module Filesystem Assembly Specification**.

---

## 8. Pipeline (Normative)

Paperhat defines a conceptual processing pipeline with strict phase separation:

1. **Compilation** — CDX → AST → IR → RDF/Turtle (pure)
2. **Storage / Query** — RDF ↔ triple store (IO boundary)
3. **Shaping** — query results → ViewModel (pure)
4. **Planning** — ViewModel + Design Policy → Presentation Plan (pure)
5. **Rendering** — Presentation Plan → target output (pure)

Phase boundaries are normative and MUST NOT be collapsed.

---

## 9. Libraries and Responsibility Ownership (Normative)

Paperhat is composed of libraries with **exclusive responsibilities**.

Each library:

* owns a clearly defined concern
* is governed by its own contract
* MUST NOT subsume responsibilities owned by another library

Examples (non-exhaustive):

* **Scribe** owns the end-to-end pipeline orchestration and compilation
* **Architect** owns semantic meaning, vocabularies, and schemas
* **Warden** owns constraint enforcement
* **Quartermaster** owns tooling and development ergonomics

Library contracts MUST NOT conflict with this system contract.

---

## 10. Tooling (Normative)

Tooling is **explicitly non-authoritative**.

Tooling MAY:

* scaffold projects
* watch files
* orchestrate pipeline runs
* host development servers
* invoke render targets

Tooling MUST NOT:

* define semantic meaning
* introduce implicit structure
* redefine pipeline phases
* impose runtime semantics

Removing all tooling MUST NOT invalidate authored Paperhat artifacts.

---

## 11. Filesystem as Packaging (Normative)

Filesystem structure:

* expresses **packaging and containment**
* does **not** express semantic meaning
* does **not** imply information architecture
* does **not** imply target behavior

All filesystem semantics are defined **only** by specification.

---

## 12. Determinism and Explainability (Normative)

Given identical semantic inputs and configuration:

* compilation MUST be deterministic
* planning MUST be deterministic
* rendering MUST be deterministic

All system behavior MUST be explainable in terms of:

* authored artifacts
* declared policies
* documented specifications

---

## 13. Authority Order (Normative)

In the event of conflict, the following precedence applies (highest first):

1. **Paperhat System Contract**
2. **Library Contracts**
3. **Formal Specifications**
4. **Normative Supporting Documents**
5. **Examples**
6. **Notes**

Lower-authority documents MUST NOT contradict higher-authority documents.

---

## 14. Relationship to Implementations

This contract defines **intent and constraints**, not implementations.

Implementations:

* may vary internally
* may be licensed separately
* MUST conform to all applicable normative documents to claim compliance

No implementation detail can override this contract.

---

## 15. Change Control

This document is **LOCKED**.

Changes require:

* an explicit version increment
* a documented rationale
* review against all dependent specifications and contracts

---

## 16. Summary

Paperhat is:

* a semantic authoring and processing **system**
* governed by explicit contracts and specifications
* deterministic, inspectable, and target-independent
* hostile to implicit behavior and accidental frameworks

This contract is the final authority on what Paperhat **is**.

---

**End of Paperhat System Contract v0.1**
