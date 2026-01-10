Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Presentation Plan Definition Specification

This specification defines the **Presentation Plan**: what it is, how it is produced, what it may contain, and how it participates in the Paperhat processing pipeline.

This document governs **planning semantics only**.
It does **not** define rendering, layout engines, styling systems, or target-specific output formats.

---

## 1. Purpose

The Presentation Plan exists to:

* separate **planning** from **rendering**
* capture all **design decisions** in a deterministic, inspectable form
* provide a target-neutral intermediate artifact between meaning and realization
* ensure renderers are **pure executors**, not decision-makers
* prevent design policy from leaking into rendering implementations

A Presentation Plan answers one question only:

> **Given this ViewModel and this Design Policy, what should be realized?**

---

## 2. Scope

This specification governs:

* the definition and semantics of Presentation Plans
* the allowed structural and semantic contents of a Presentation Plan
* how Presentation Plans are produced by Scribe
* how Presentation Plans are consumed by renderers

This specification does **not** govern:

* rendering technologies (HTML, PDF, audio, etc.)
* layout systems or styling languages
* interaction, animation, or behavior
* application workflows
* persistence formats

---

## 3. Core Terms (Normative)

### 3.1 Presentation Plan

A **Presentation Plan** is a declarative, target-neutral plan that specifies:

* what structural elements will be realized
* what information is included or omitted
* how elements are grouped, ordered, emphasized, or suppressed
* which semantic signals (Flags, importance levels, density, etc.) apply

A Presentation Plan:

* is derived, never authored directly
* introduces no semantic truth
* performs no IO
* is deterministic and reproducible

---

### 3.2 Planning

**Planning** is the pure transformation:

```
ViewModel + Design Policy → Presentation Plan
```

Planning resolves **policy**, not **meaning**.

---

### 3.3 Renderer

A **Renderer** is a pure function that consumes a Presentation Plan and produces concrete output for a specific target.

Renderers:

* MUST NOT apply Design Policy
* MUST NOT invent structure
* MUST NOT infer intent
* MUST NOT query graphs

---

## 4. Position in the Pipeline (Normative)

The Presentation Plan occupies a fixed position in the Scribe pipeline:

1. Domain Graph queried
2. View Graph applied
3. **ViewModel produced**
4. **Design Policy applied**
5. **Presentation Plan produced**
6. Rendering executed

The Presentation Plan is the **final authoritative artifact** before rendering.

---

## 5. Epistemic Status (Hard)

The Presentation Plan:

* is **non-authoritative**
* asserts no semantic truth
* may be discarded and regenerated at any time
* MUST be fully reproducible from stored graphs and policies

The Presentation Plan exists solely to guide realization.

---

## 6. Structural Content (Normative)

A Presentation Plan consists of a tree of **Planned Nodes**.

Each Planned Node represents a structural unit to be realized.

Planned Nodes MAY include:

* structural type (e.g. Section, List, Item, Text)
* resolved ordering
* grouping membership
* importance level
* density classification
* emphasis or suppression flags
* semantic Flags carried forward from the ViewModel
* target-conditional inclusion markers

Planned Nodes MUST NOT include:

* layout metrics
* styling rules
* pixel values
* typographic instructions
* animation or interaction behavior

---

## 7. Ordering Semantics (Hard)

All ordering in a Presentation Plan MUST be explicit.

* Ordered collections MUST carry resolved order indices
* Unordered collections MUST NOT imply ordering
* Design Policy decisions that affect order MUST be reflected explicitly

Renderers MUST NOT reorder nodes unless explicitly instructed by the Plan.

---

## 8. Inclusion and Suppression (Hard)

The Presentation Plan MUST explicitly encode:

* included nodes
* suppressed nodes
* conditionally included nodes (e.g. target-specific)

Renderers MUST NOT decide whether something appears.

If a node is absent from the Presentation Plan, it MUST NOT be rendered.

---

## 9. Flags and Semantic Signals (Normative)

Semantic Flags originating from Views MAY appear in the Presentation Plan.

Design Policy MAY:

* promote Flags to emphasis
* suppress Flagged nodes
* require verbal marking
* alter grouping or ordering based on Flags

Flags in the Presentation Plan are **signals**, not presentation instructions.

---

## 10. Target Awareness (Normative)

The Presentation Plan MAY include **target conditions** resolved during planning.

Examples:

* screen vs print vs voice
* size or capability classes
* accessibility modes

Target conditions MUST be:

* declarative
* resolved by Design Policy
* explicit in the Plan

Renderers MUST NOT reinterpret target suitability.

---

## 11. Determinism and Stability (Hard)

Given identical inputs:

* Domain Graph
* View Graph
* Design Policy
* execution context

Scribe MUST produce an identical Presentation Plan.

No randomness, heuristics, or environment-dependent behavior is permitted.

---

## 12. Validation (Hard)

Presentation Plans MUST:

* conform to the Presentation Plan ontology
* validate against SHACL constraints
* be internally consistent

Invalid Presentation Plans MUST NOT be rendered.

Failures MUST surface as Help values.

---

## 13. Serialization (Normative)

A Presentation Plan:

* MAY be serialized for debugging, testing, or inspection
* MUST NOT be treated as a persistence boundary
* MUST NOT be edited or authored by humans

Serialization format is implementation-defined.

---

## 14. Non-Goals (Normative)

The Presentation Plan does **not**:

* define visual layout
* define styling
* define interaction
* define animation
* define navigation behavior
* define rendering algorithms

If a concern affects **how something looks or behaves**, it does not belong here.

---

## 15. Relationship to Other Specifications (Normative)

This specification must be read alongside:

* **Codex View Definition Specification**
* **Design Policy Definition Specification**
* **Scribe Library Contract**
* **Paperhat System Contract**

In case of conflict:

1. Paperhat System Contract prevails
2. Scribe Library Contract prevails
3. This specification governs Presentation Plan semantics

---

## 16. Summary

* The Presentation Plan is the **bridge between planning and rendering**
* It is derived, deterministic, and non-authoritative
* It resolves **policy**, not **meaning**
* It encodes all decisions needed for realization
* It leaves renderers with nothing to decide

Renderers execute.
Policies decide.
Meaning remains untouched.

---

**End of Presentation Plan Definition Specification v0.1**
