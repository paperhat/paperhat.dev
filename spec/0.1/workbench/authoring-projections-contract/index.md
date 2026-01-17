Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Authoring Projections Contract

---

## 1. Purpose

This specification defines the **authoring projections** supported by the Paperhat Workbench.

Authoring projections are **distinct, read-only or write-mediated views** over the same canonical authored meaning.

This specification exists to ensure that:

* multiple authoring experiences operate over a single source of truth
* no projection introduces an alternate authoring model
* all projections preserve determinism, reviewability, and user intent
* mutation discipline is enforced uniformly

This document is **Normative**.

---

## 2. Scope

This specification governs:

* text-based authoring
* form-based authoring
* assistive (AI-guided) authoring
* preview and inspection projections

This specification does **not** define:

* semantic rules
* UI layout or widget design
* storage formats
* implementation technologies

---

## 3. Canonical Authored State (Normative)

There exists exactly one **canonical authored state** for a Work.

All authoring projections:

* observe the same canonical state
* propose changes against the same canonical state
* MUST NOT create parallel or competing representations

No projection may introduce a secondary source of truth.

---

## 4. Projection Definition (Normative)

An **Authoring Projection** is a derived view over the canonical authored state.

Projections MAY:

* display authored meaning
* organize authored meaning
* guide user interaction
* propose changes

Projections MUST NOT:

* mutate authored content directly
* bypass mutation review mechanisms
* introduce implicit behavior

All mutation proposals MUST be expressed as Patches.

---

## 5. Text Projection (Codex) (Normative)

The **Text Projection** presents authored content as Codex text.

Characteristics:

* exposes the full expressive power of Codex
* preserves explicit structure and intent
* supports expert authoring and inspection

Rules:

* edits produce deterministic Patches
* no auto-correction or rewriting is permitted
* previews derived from text edits are read-only until applied

The Text Projection is authoritative only through Patch application.

---

## 6. Form Projection (ConceptForm) (Normative)

The **Form Projection** presents authored content as schema-derived forms.

Form Projections MUST:

* be derived mechanically from schema shape and constraints
* support deterministic inclusion, exclusion, grouping, and hiding of properties
* enforce schema validation at proposal time

Form Projections MUST NOT:

* redefine schema semantics
* store independent form state as authored truth
* bypass Patch review and application

All form interactions produce deterministic Patches against the canonical authored state.

---

## 7. Assistive Projection (AI-Guided) (Normative)

The **Assistive Projection** provides guided authoring support.

Assistive systems MAY:

* ask clarifying questions
* highlight ambiguities
* suggest structures
* propose content

Assistive systems MUST NOT:

* apply changes automatically
* mutate authored content directly
* bypass user review or refusal semantics

All assistive output MUST be expressed as proposed Patches requiring explicit user approval.

---

## 8. Preview and Inspection Projections (Normative)

Preview and inspection projections present **derived, read-only views** of authored meaning.

These MAY include:

* structured data views
* graphs and relationships
* outlines and hierarchies
* ViewModels
* Presentation Plans
* target-specific previews

Rules:

* previews MUST be snapshot-based
* previews MUST NOT mutate state
* previews MUST reflect exactly the current canonical state

---

## 9. Projection Consistency (Normative)

All projections MUST satisfy:

* identical canonical state
* identical Patch semantics
* identical validation and refusal behavior
* identical Diagnostics for identical conditions

Differences between projections are strictly presentational.

---

## 10. Mutation Boundary (Normative)

No projection may cross the mutation boundary.

All changes MUST:

* be proposed explicitly
* be reviewable
* be applied only through the Workbench Core

Implicit mutation is forbidden.

---

## 11. Extensibility (Normative)

New projections MAY be added only if:

* they operate over the same canonical authored state
* they produce deterministic Patches
* they introduce no alternate authoring models
* they conform to all mutation and diagnostic contracts

---

## 12. Reality Rule (Normative)

This specification defines authoring projections **as they are**.

There is no legacy projection model.
There are no deprecated authoring modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
