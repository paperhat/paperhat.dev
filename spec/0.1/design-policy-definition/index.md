Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Design Policy Definition Specification

## 1. Purpose

This specification defines **Design Policies** in Paperhat: what they are, what they may express, how they are applied, and how they participate in the processing pipeline.

A Design Policy exists to adapt a **fixed View structure** to **realization constraints** without changing meaning or structure.

This document governs **Design Policy authoring and semantics only**.

It does **not** define:

* rendering
* layout, styling, or typography
* widgets or UI components
* domain semantics
* View structure
* application behavior

This document is **Normative**.

---

## 2. Core Principle (Hard)

> **Design Policy adapts realization, not meaning.**

A Design Policy:

* MUST NOT invent structure
* MUST NOT remove structure by intent
* MUST NOT change semantic truth
* MUST NOT encode presentation

A Design Policy answers one question only:

> **How should this View be realized under these constraints?**

---

## 3. Scope

This specification governs:

* the structure of Design Policy documents
* allowed Design Policy Concepts
* constraint-based adaptation rules
* interaction with Views and the ViewModel
* production of a Presentation Plan

This specification does **not** govern:

* View selection
* View authoring
* renderer behavior
* target-specific output formats
* filesystem layout beyond module scoping

---

## 4. Core Terms (Normative)

### 4.1 Design Policy

A **Design Policy** is a declarative rule set that:

* operates on a ViewModel
* is conditional on realization constraints
* produces a Presentation Plan
* is deterministic and explainable

Design Policies are **target-aware**, but **target-neutral in intent**.

---

### 4.2 Presentation Plan

A **Presentation Plan** is a derived, ephemeral structure that:

* results from applying a Design Policy to a ViewModel
* specifies what will be realized and how
* is consumed by renderers
* is not persisted

---

### 4.3 Constraint

A **Constraint** is a condition describing the realization context.

Examples:

* target modality (screen, print, voice)
* size or density limits
* accessibility modality
* linear vs spatial realization

Constraints are inputs to Design Policy evaluation.

---

## 5. Module Scope and Files (Normative)

### 5.1 Module Containment

All Design Policies are **module-scoped**.

A Design Policy MUST be authored within a module’s `designs/` directory.

Design Policies MUST NOT be global or shared across modules.

---

### 5.2 One Policy per File (Hard)

Each Design Policy document:

* MUST contain exactly one `<DesignPolicy>` root Concept
* MUST reside in its own folder
* MUST be named `design.cdx`

---

### 5.3 Identity

A Design Policy MAY declare an `id` Trait.

If present, the `id` is resolved using the module’s `idBase` per the Codex ID Resolution Specification.

---

## 6. Design Policy Root (Normative)

### 6.1 Root Concept

A Design Policy document MUST have a single root Concept:

```cdx
<DesignPolicy>
	…
</DesignPolicy>
```

---

## 7. Targets and Applicability (Normative)

### 7.1 Targets

`<Targets>` declares the realization targets to which the policy applies.

* Targets are symbolic identifiers
* No target hierarchy is implied
* Target interpretation is system-defined

Example:

```cdx
<Targets>
	<Target>voice</Target>
</Targets>
```

---

### 7.2 Conditional Application

Conditional application is expressed using `<When>` blocks.

Rules:

* Conditions MUST be declarative
* Conditions MUST NOT depend on View identity
* Conditions MAY depend on:

  * target
  * capacity attributes (e.g. width)
  * modality

---

## 8. Importance and Priority (Normative)

### 8.1 Importance

Importance assigns **relative semantic priority**.

Allowed Concepts:

* `<Primary>`
* `<Secondary>`
* `<Tertiary>`
* `<Deemphasized>`

Importance affects:

* omission under constraint
* summarization priority
* realization order

Importance MUST NOT encode appearance.

---

## 9. Grouping and Association (Normative)

### 9.1 Group

`<Group>` expresses semantic association.

Traits:

* `tightly` — boolean, default false

Groups influence:

* collapse decisions
* separation
* linearization

---

## 10. Ordering and Flow (Normative)

### 10.1 Ordering Rules

Allowed Concepts:

* `<PreserveOrder>`
* `<AllowReorder>`
* `<Move>`
* `<Promote>`
* `<Demote>`

Rules:

* Ordering MAY only change when explicitly allowed
* Ordered structures retain semantic ordering unless overridden

---

## 11. Density and Compression (Normative)

### 11.1 Density

Allowed Concepts:

* `<Compact>`
* `<Comfortable>`
* `<Expanded>`

Density expresses **information packing**, not visibility.

---

## 12. Inclusion, Omission, and Collapse (Normative)

Allowed Concepts:

* `<Include>`
* `<Omit>`
* `<Collapse>`
* `<Expand>`

Rules:

* Omission MUST be constraint-driven
* Permanent omission is forbidden
* All omission MUST be explainable

---

## 13. Summarization and Aggregation (Normative)

Allowed Concepts:

* `<Summarize>`
* `<Enumerate>`
* `<Aggregate>`

Summarization:

* MUST preserve meaning
* MUST be deterministic
* MUST be reversible when constraints are removed

---

## 14. Semantic Signaling (Normative)

### 14.1 Flag-Based Rules

Design Policies MAY reference semantic Flags exposed by Views.

Allowed Concepts:

* `<Mark>`
* `<Emphasize>`
* `<Subdue>`
* `<Neutralize>`

Rules:

* Flags MUST NOT imply presentation
* Flags express semantic importance only

---

## 15. Proximity and Separation (Normative)

Allowed Concepts:

* `<Close>`
* `<Separate>`
* `<Attach>`
* `<Isolate>`

These express **conceptual distance**, not spacing units.

---

## 16. Interaction Constraints (Normative)

Allowed Concepts:

* `<AllowProgressiveDisclosure>`
* `<DisallowProgressiveDisclosure>`

These express **whether progressive reveal is permitted**, not how it is implemented.

---

## 17. Negative Constraints (Normative)

Allowed Concepts:

* `<Avoid>`
* `<Forbid>`
* `<Require>`

Negative constraints explicitly prevent behaviors.

---

## 18. Non-Goals (Hard)

Design Policies MUST NOT:

* define layout units
* define typography or styling
* define widgets or UI components
* reference HTML, CSS, or platform APIs
* invent or remove View structure
* modify domain semantics

If a rule answers **“what does this look like?”**, it is invalid.

---

## 19. Compilation and Pipeline Integration (Normative)

### 19.1 Application

Design Policies are applied by Scribe to a ViewModel.

* Application is pure
* Application is deterministic
* Output is a Presentation Plan

---

### 19.2 Presentation Plan

The Presentation Plan:

* is ephemeral
* is not persisted
* contains no rendering primitives
* is consumed by renderers only

---

## 20. Error Handling (Normative)

* Invalid references → Help
* Conflicting rules → Help
* Non-determinism → Help
* Policy failure invalidates realization

---

## 21. Relationship to Other Specifications (Normative)

This specification must be read in conjunction with:

* Codex View Definition Specification
* View and Design Policy Selection Specification
* Codex Naming and Value Specification
* Codex ID Resolution Specification

In case of conflict:

* This document governs Design Policy semantics
* View spec governs structure
* Selection spec governs precedence

---

## 22. Summary

* Design Policies adapt realization under constraint
* They do not change meaning or structure
* They operate on ViewModels
* They produce Presentation Plans
* They are declarative, deterministic, and explainable
* They are module-scoped and target-aware

---

**End of Design Policy Definition Specification v0.1**
