Status: NORMATIVE
Lock State: UNLOCKED  
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

> **Given this ViewModel, these DesignIntent sets, and this Design Policy, what should be realized?**

---

## 2. Scope

This specification governs:

* the definition and semantics of Presentation Plans
* the allowed structural and semantic contents of a Presentation Plan
* how Presentation Plans are produced by Kernel
* how Presentation Plans are consumed by renderers

This specification does **not** govern:

* rendering technologies (HTML, PDF, audio, etc.)
* layout systems or styling languages
* interaction or animation semantics
* Behavior Program semantics (owned by the Behavior Dialect specification)
* application workflows
* persistence formats

---

## 3. Core Terms (Normative)

### 3.1 Presentation Plan

A **Presentation Plan** is a declarative, target-neutral planning artifact that specifies:

* what structural elements will be realized
* what information is included or omitted
* how elements are grouped, ordered, emphasized, or suppressed
* which resolved semantic signals apply

A Presentation Plan:

* is derived, never authored directly
* introduces no semantic truth
* performs no IO
* is deterministic and reproducible
* is the **final authoritative planning artifact** provided to renderers

---

### 3.2 Planning

**Planning** is the pure transformation:

```
ViewModel + DesignIntent sets + Design Policy → Presentation Plan
```

Planning resolves **policy** and **intent**, not **meaning**.

---

### 3.3 Renderer

A **Renderer** is a pure function that consumes a Presentation Plan and produces concrete output for a specific target.

Renderers:

* MUST NOT apply Design Policy
* MUST NOT invent structure
* MUST NOT infer intent
* MUST NOT query graphs

---

## 4. Position in the Kernel (Normative)

The Presentation Plan occupies a fixed position in the Paperhat Kernel:

1. Domain Graph queried
2. View Graph applied
3. **ViewModel produced**
4. **DesignIntent sets selected** (by Design Policy)
5. **Intent resolved** (axis values merged per node)
6. **Structural transforms applied** (by Design Policy)
7. **Presentation Plan produced**
8. Rendering executed

The Presentation Plan is the **final planning artifact** before rendering.

---

## 5. Epistemic Status (Normative)

The Presentation Plan:

* is **non-authoritative with respect to semantic truth**
* asserts no domain meaning
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
* **resolved DesignIntent axes**:

  * `size` — resolved SizeIntent (`$Small` | `$Medium` | `$Large`)
  * `emphasis` — resolved EmphasisIntent (`$Subtle` | `$Normal` | `$Strong`)
  * `density` — resolved DensityIntent (`$Compact` | `$Comfortable` | `$Spacious`)
  * `role` — resolved RoleIntent (`$Neutral` | `$Muted` | `$Primary`)
* **plan-level intent metadata** (proximity, visibility, ordering, enumeration, spacing, flagTreatment, etc.)
* semantic Flags carried forward from the ViewModel
* explicit inclusion or suppression markers
* target-conditional inclusion markers
* declarative attachments expressed as Behavior Programs-as-data

Planned Nodes MUST NOT include:

* layout metrics
* styling rules
* pixel values
* typographic instructions
* animation or interaction logic
* executable code

Behavior Program attachments:

* are declarative data only
* MUST NOT require graph queries or policy evaluation at render time
* are consumed by dedicated behavior runtimes, not by Design Policy or renderers

---

## 7. Ordering Semantics (Normative)

All ordering in a Presentation Plan MUST be explicit.

* Ordered collections MUST carry resolved order indices
* Unordered collections MUST NOT imply ordering
* Design Policy decisions that affect order MUST be reflected explicitly

Renderers MUST NOT reorder nodes unless explicitly instructed by the Plan.

---

## 8. Inclusion and Suppression (Normative)

The Presentation Plan MUST explicitly encode:

* included nodes
* suppressed nodes
* conditionally included nodes

Renderers MUST NOT decide whether something appears.

If a node is absent from the Presentation Plan, it MUST NOT be rendered.

---

## 9. Flags and Semantic Signals (Normative)

Semantic Flags originating from Views MAY appear in the Presentation Plan.

Design Policy MAY, based on Flags:

* select or layer DesignIntent sets
* apply structural transforms
* emit plan-level intent metadata
* require explicit marking or grouping

Design Policy MUST NOT directly assign DesignIntent axes in the Presentation Plan.

Flags in the Presentation Plan are **signals**, not presentation instructions.

---

## 10. Target Awareness (Normative)

The Presentation Plan MAY include **explicit target conditions** determined during planning.

Examples:

* screen vs print vs voice
* size or capability classes
* accessibility modes

Target conditions:

* MUST be declarative
* MUST be introduced by Design Policy
* MAY remain as explicit conditions in the Plan when multi-target realization is required

Renderers MUST NOT reinterpret target suitability or apply policy logic.

---

## 11. Determinism and Stability (Normative)

Given identical inputs:

* Domain Graph
* View Graph
* DesignIntent sets
* Design Policy
* context signals
* target medium

Kernel MUST produce an identical Presentation Plan.

No randomness, heuristics, or environment-dependent behavior is permitted.

---

## 12. Validation (Normative)

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
* define interaction semantics
* define animation
* define navigation behavior
* define rendering algorithms

If a concern affects **how something looks or behaves**, it does not belong here.

---

## 15. Relationship to Other Specifications (Normative)

This specification MUST be read alongside:

* [Codex View Definition Specification](../view-definition/)
* [Design Intent Definition Specification](../../design/design-intent-definition/)
* [Design Policy Definition Specification](../../design/design-policy-definition/)
* [Kernel Architecture Specification](../../foundation/kernel-architecture/)
* [Paperhat System Contract](../../../../contracts/PAPERHAT_SYSTEM_CONTRACT/)

Authority:

* Design Intent Definition governs intent axes, assignments, and resolution semantics.
* Design Policy Definition governs intent selection, context consumption, and structural transforms.
* This specification governs the structure and contents of the Presentation Plan.

In case of conflict:

1. Paperhat System Contract prevails
2. Kernel Architecture Specification prevails
3. This specification governs Presentation Plan semantics

---

## 16. Summary

* The Presentation Plan is the **bridge between planning and rendering**
* It is derived, deterministic, and non-authoritative with respect to meaning
* It resolves **policy** and **intent**, not **semantic truth**
* It carries **resolved DesignIntent axes** per node
* It carries **plan-level intent metadata**
* It encodes all decisions required for realization
* It leaves renderers with nothing to decide

Renderers execute.
Intent differentiates.
Policy decides.
Meaning remains untouched.

---

**End of Presentation Plan Definition Specification v0.1**
