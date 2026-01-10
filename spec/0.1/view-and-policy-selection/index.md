Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# View and Design Policy Selection Specification

This specification defines **how Views and Design Policies are selected, combined, and applied** within the Paperhat system.

Its goals are to:

* prevent structural and adaptive concerns from being mixed
* provide deterministic, explainable behavior across targets
* ensure consistent authoring and tooling decisions
* eliminate ambiguity for humans and automated systems

This document is **normative** and binding on all Paperhat implementations.

---

## 2. Scope

This specification governs:

* when to define or select a **View**
* when to define or select a **Design Policy**
* how Views and Design Policies interact
* the default precedence rules used by Scribe
* invalid patterns and forbidden mixes

This specification does **not** define:

* View syntax (see View Definition Specification)
* Design Policy vocabulary (see Design Policy Definition Specification)
* rendering behavior
* schema or ontology rules

---

## 3. Core Definitions (Normative)

### 3.1 View

A **View** is a declarative projection that defines:

* **which semantic structures are included**
* **how they are grouped**
* **their explicit ordering**
* **which semantic signals (Flags) are exposed**

A View expresses **authorial intent**.

A View is **target-independent**.

---

### 3.2 Design Policy

A **Design Policy** is a declarative rule set that defines:

* how a given View adapts under **realization constraints**
* how importance, density, grouping, and emphasis are adjusted
* how structure is linearized, summarized, or collapsed

A Design Policy expresses **adaptive realization**, not intent.

A Design Policy is **constraint-dependent**.

---

## 4. Fundamental Separation Rule (Hard)

> **A View defines what structure exists.**
> **A Design Policy defines how that structure adapts under constraints.**

No rule, document, or system component may violate this separation.

---

## 5. View Selection Rules (Normative)

A **new View MUST be defined or selected** if **any** of the following are true.

### 5.1 Intentional Inclusion or Exclusion

If a structure is included or omitted **by authorial intent**, it MUST be handled by a View.

Examples (valid View differences):

* omitting `<Steps>` entirely in a card view
* omitting `<Equipment>` in an index view
* including `<Provenance>` only in an archival view

---

### 5.2 Structural Re-projection

If the **structural role, grouping, or hierarchy** of data changes, it MUST be handled by a View.

Examples:

* grouping Ingredients by category vs a flat list
* nesting Steps under Phases vs a single sequence
* promoting metadata into the main flow

---

### 5.3 Stable Semantic Slice

If the projection represents a **named, reusable semantic slice**, it MUST be a View.

Examples:

* “recipe card”
* “recipe index entry”
* “meal plan item”

If you can name it, reuse it, and reason about it independently, it is a View.

---

### 5.4 Target-Invariant Difference Test

If a difference **should persist across all targets** (screen, print, voice, export), it MUST be a View.

---

## 6. Design Policy Selection Rules (Normative)

A **Design Policy MUST be defined or selected** when **all** of the following are true.

### 6.1 Structural Invariance

The underlying View structure remains unchanged.

No nodes may be invented, removed, or re-projected.

---

### 6.2 Constraint-Driven Difference

The difference is driven by **realization constraints**, such as:

* target modality (visual vs linear)
* size or density limits
* accessibility requirements
* attention or bandwidth constraints

---

### 6.3 Rule-Explainability

The behavior can be expressed as a declarative rule of the form:

> “When condition X holds, apply adaptation Y.”

---

### 6.4 Reversion Test

If the constraint disappears, the behavior MUST revert.

If it does not revert, the difference belongs in a View, not a Design Policy.

---

## 7. Decisive Classification Test (Normative)

When uncertain, implementations MUST apply both questions:

1. **If a different Design Policy is applied, should the difference remain?**
2. **If a different View is applied, should the difference remain?**

| Answer Pattern | Classification               |
| -------------- | ---------------------------- |
| Yes / No       | **View**                     |
| No / Yes       | **Design Policy**            |
| Yes / Yes      | **Invalid (mixed concerns)** |
| No / No        | **Renderer behavior**        |

Implementations MUST reject Yes/Yes cases.

---

## 8. Default Selection Precedence (Normative)

Unless explicitly overridden, Scribe MUST apply selection in the following order.

### 8.1 View Selection Precedence

1. Explicitly requested View (CLI, API, or pipeline input)
2. Module-declared default View
3. Schema-defined default View (if any)
4. Error if no View is resolvable

---

### 8.2 Design Policy Selection Precedence

1. Explicitly requested Design Policy
2. Target-specific Design Policy matching realization context
3. Module-declared default Design Policy
4. System default Design Policy
5. Error if none is applicable

---

### 8.3 Independence Rule (Hard)

View selection MUST NOT depend on Design Policy selection.
Design Policy selection MUST NOT depend on View selection.

They are orthogonal axes.

---

## 9. Anti-Examples (Normative)

The following patterns are **explicitly forbidden**.

### 9.1 Hiding Structure via Design Policy

❌ Using Design Policy to permanently remove Steps or Sections.

Reason:
Permanent omission is authorial intent → requires a View.

---

### 9.2 Encoding Target Logic in Views

❌ Conditional logic in Views based on screen, print, or voice.

Reason:
Views are target-independent by definition.

---

### 9.3 Presentation Leakage into Views

❌ Using numbering styles, typography, widgets, or layout primitives in Views.

Reason:
Views define structure, not appearance.

---

### 9.4 Cosmetic Design Policies

❌ Design Policies that differ only by styling, branding, or theme.

Reason:
Those belong exclusively to renderers.

---

### 9.5 Mixed Structural and Adaptive Rules

❌ A single rule that both removes structure and adapts realization.

Reason:
This violates the core separation rule.

---

## 10. Enforcement Requirements (Hard)

Implementations MUST:

* reject mixed View/Policy behaviors
* surface violations as Help, not runtime failures
* preserve explainability of all adaptations
* ensure deterministic selection given identical inputs

---

## 11. Summary

* Views define **what structure exists**
* Design Policies define **how that structure adapts**
* Views express **intent**
* Design Policies express **constraint-driven adaptation**
* Selection is deterministic, orthogonal, and explainable
* Mixing concerns is forbidden

---

**End of View and Design Policy Selection Specification v0.1**
