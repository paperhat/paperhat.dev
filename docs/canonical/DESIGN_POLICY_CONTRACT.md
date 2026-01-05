# DESIGN_POLICY_CONTRACT (CANONICAL)

This document defines the **exclusive responsibilities, boundaries, and guarantees** of **Design Policy** in Sitebender Codex.

Design Policy governs **how semantic projections are presented**, without altering meaning, structure, or correctness.

This document is **CANONICAL**.
It is governed by global Codex Change Control.

---

## 1. Purpose

Design Policy exists to answer one question:

> **“Given this meaning and this view, how should it appear in a specific medium?”**

Design Policy defines **presentation decisions**, not semantic truth.

It enables:

- consistent design systems over semantic data
- responsive and adaptive presentation
- multi-target rendering (screen, print, voice, etc.)
- declarative, explainable layout behavior
- reflow, prioritization, and progressive disclosure

Design Policy is **data**, not code.

---

## 2. Scope (Hard)

Design Policy governs **presentation-level interpretation** of semantic projections, including:

- grouping interpretation
- ordering and flow
- alignment and spatial relationships
- hierarchy and prioritization
- contrast, emphasis, and dominance
- balance and visual weight
- use of negative space
- responsive behavior
- progressive disclosure
- pagination and step flows
- widget selection strategy (when applicable)

For time-based or dynamic media, Design Policy may additionally govern:

- pacing and rhythm
- continuity
- transitions
- narrative sequencing
- audio/visual coordination

Design Policy never defines meaning.

---

## 3. Separation of Concerns (Hard)

Design Policy:

- **consumes** semantic projections and ViewModels
- **does not** alter semantic truth
- **does not** invent structure
- **does not** introduce new data
- **does not** enforce constraints
- **does not** define behavior logic

Canonical separation:

- **Architect** defines meaning
- **Scribe** orchestrates the pipeline
- **Design Policy** defines appearance
- **Renderers** implement targets

---

## 4. Relationship to Semantic Projections

Design Policy operates on **semantic groupings**, not on markup or layout boxes.

Examples of semantic groupings:

- Concept groups
- Field groups (from Form IR)
- Sections
- Lists
- Steps
- Narratives
- Hierarchies declared at the meaning level

Design Policy interprets these groupings **by policy**, not by inference.

---

## 5. Ownership and Authoring

Design Policy is:

- authored by site or application owners
- expressed exclusively in **CDX**
- owned by the application, not by Architect
- consumed by Scribe and renderers

End users may author or modify Design Policy without writing code.

---

## 6. Target Awareness (Normative)

Design Policy is **target-aware but target-agnostic**.

This means:

- policies may declare intent relative to a target class (e.g. screen, print, voice)
- policies do not contain target-specific implementation details
- final interpretation is delegated to renderers

Design Policy does not reference DOM, HTML, CSS, ARIA, or platform APIs.

---

## 7. Widget Policy (Subset)

Widget Policy is a **subset** of Design Policy.

Widget Policy governs **selection strategies**, such as:

- radio group vs dropdown
- checkbox group vs autocomplete
- slider vs numeric input
- text field vs multi-line text

These decisions are:

- policy-driven
- configurable
- non-semantic
- overridable per target

Widget Policy never introduces meaning and never affects validity.

---

## 8. Responsive and Adaptive Rules

Design Policy MAY encode rules such as:

- reflow thresholds
- content relocation
- priority-based collapse
- summarization vs expansion
- pagination or wizard transitions

Rules operate on **semantic nodes and groups**, not on layout primitives.

Viewport size, shape, and medium characteristics may be considered.

---

## 9. Progressive Disclosure

Design Policy MAY define:

- what is shown first
- what is hidden initially
- what is revealed on demand
- how secondary content is accessed

Progressive disclosure affects **presentation only**.

Hidden content remains:

- semantically present
- queryable
- valid
- persistent

---

## 10. Relationship to Behavior

Design Policy is **not behavior**.

- It does not compute values
- It does not react to events
- It does not execute logic

Design Policy MAY declare **presentation affordances** that renderers and behaviors can respond to, but it does not define the behavior itself.

---

## 11. Compilation and Use

Design Policy is:

- parsed from CDX
- compiled by Scribe into a presentation plan
- combined with a ViewModel
- consumed by renderers

Compilation is deterministic.

No runtime inference is permitted.

---

## 12. Prohibited Content (Hard)

Design Policy MUST NOT include:

- semantic assertions
- validation rules
- business logic
- behavior logic
- runtime bindings
- references to storage, APIs, or clocks
- HTML, CSS, or platform-specific constructs

If it affects correctness, it is not Design Policy.

---

## 13. Explainability Requirement

Design Policy MUST be explainable in plain language.

The system must be able to answer questions such as:

- “Why is this shown first?”
- “Why is this grouped here?”
- “Why did this collapse on a small screen?”
- “Why is this summarized instead of expanded?”

Opaque or implicit behavior is forbidden.

---

## 14. Summary

Design Policy enables:

> **Design systems over meaning, not markup.**

It provides:

- consistency without rigidity
- adaptability without inference
- presentation control without semantic corruption
- multi-target support without duplication

Design Policy answers **how it appears**, never **what it means**.

---

## Status

**CANONICAL**

This contract is authoritative.
Anything not explicitly permitted is forbidden.
