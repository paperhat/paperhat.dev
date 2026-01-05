# CODEX_SYSTEM_CONTRACT (CANONICAL)

This document defines the **foundational nature, scope, and invariants** of **Sitebender Codex**.

It supersedes any interpretation of Sitebender as a “framework” or “toolkit”.

This document is **CANONICAL**.
It is governed by global Change Control.

---

## 1. What Sitebender Codex Is

**Sitebender Codex is a language.**

It is a **declarative, semantic authoring language** for describing:

- meaning
- structure
- constraints
- behavior (as data)
- presentation policy
- bindings to environments

Sitebender Codex is **not**:

- a web framework
- a UI framework
- a component library
- a configuration system layered on top of code

All of those are _applications_ of the language, not the language itself.

---

## 2. The Authoring Surface (Hard)

### 2.1 CDX Is the Only Authoring Language

**All authoring is done in CDX.**

This includes, without exception:

- semantic data
- semantic views
- constraints
- behaviors
- bindings
- design policy
- pipeline configuration
- environment configuration

No other authoring formats are permitted.

Forbidden authoring surfaces:

- JSON
- YAML
- TOML
- XML
- imperative configuration
- embedded scripts
- inline code blocks

If it is authored by a human, it is CDX.

---

### 2.2 Target Users (Critical)

Sitebender Codex is designed for **non-developers**.

Authors may include:

- hobbyists
- designers
- subject-matter experts
- business analysts
- lawyers
- product managers
- educators

Programming experience is **not assumed**.

CDX MUST:

- read like plain English
- minimize cognitive load
- avoid abbreviations in its canonical form
- avoid programming jargon
- avoid implementation detail leakage

Developer convenience is never a justification for authoring complexity.

---

## 3. Closed World Assumption (Hard)

Sitebender Codex operates as a **closed declarative system**.

This means:

- all meaning must be explicitly declared
- nothing is inferred implicitly
- nothing is “filled in” silently
- nothing exists outside what is authored or derived deterministically

If something is not declared, it does not exist.

---

## 4. Internal Representations (Non-Authoring)

### 4.1 Compilation Is Mandatory

All CDX is compiled into internal representations, including:

- abstract syntax structures
- intermediate representations
- semantic graphs (triples)
- constraint graphs
- view models
- presentation plans

These representations are:

- internal
- invisible to end users
- unstable across versions
- optimized for machines

Authors MUST NEVER see or write these representations.

---

### 4.2 Naming and Abbreviation Rule

- **CDX uses full, plain-English names**
- **Internal representations may use abbreviated names freely**

Abbreviations are permitted only where humans do not see them.

---

## 5. Determinism and Explainability (Hard)

Given the same CDX inputs:

- compilation MUST be deterministic
- outputs MUST be reproducible
- validation MUST be consistent

The system MUST be able to explain:

- why something is valid
- why something is invalid
- why something is shown
- why something is hidden
- why something is ordered or grouped

Opaque behavior is forbidden.

---

## 6. Separation of Responsibility (Hard)

Sitebender Codex enforces strict separation:

- **Architect and domain libraries** define meaning
- **Constraints** define validity
- **Behaviors** define optional computation
- **Bindings** define value sources
- **Design Policy** defines appearance
- **Scribe** orchestrates compilation and rendering
- **Warden** enforces validity
- **Renderers** emit target-specific output

No library may assume responsibilities owned by another.

---

## 7. Non-JavaScript Correctness (Hard)

All Sitebender Codex applications MUST be correct **without JavaScript**.

This means:

- data validity does not depend on JS
- form submission does not depend on JS
- persistence does not depend on JS
- constraint enforcement does not depend on JS

JavaScript MAY enhance experience, but MUST NOT enable correctness.

---

## 8. Referential Transparency (Hard)

All authoritative semantics in Sitebender Codex MUST be referentially transparent.

- constraints depend only on the semantic graph
- calculations depend only on declared inputs
- no hidden state may influence correctness

Runtime-only sources (cookies, clocks, APIs, UI state) MUST NOT affect semantic truth.

---

## 9. Multi-Target First Principle

Sitebender Codex is **target-agnostic by design**.

The same CDX may be rendered to:

- HTML
- DOM mutations
- PDF
- LaTeX
- SVG
- Voice systems
- Future targets not yet defined

No authoring construct may assume a specific target.

---

## 10. Change Discipline (Hard)

Any change to Sitebender Codex MUST:

1. be proposed as a textual change to a canonical document
2. preserve existing guarantees explicitly
3. avoid implementation-led reinterpretation

Implementation follows documentation, never the reverse.

---

## 11. Summary

Sitebender Codex is:

> **A language for describing reality, not a toolkit for building websites.**

It prioritizes:

- clarity over cleverness
- explicitness over inference
- meaning over mechanics
- humans over machines

If something cannot be expressed clearly in CDX, it does not belong in the system.

---

## Status

**CANONICAL**

This document is authoritative.
Anything not explicitly permitted is forbidden.
