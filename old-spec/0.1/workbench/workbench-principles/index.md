Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Principles

---

## 1. Purpose

This specification defines the **non-negotiable principles** governing the behavior, boundaries, and obligations of the Paperhat Workbench.

These principles establish **how the system behaves**, independent of interface, implementation language, or deployment model.

This document is **Normative**.

---

---

## 2. Scope

These principles apply to:

* the Workbench Core
* all interaction surfaces (CLI, desktop studio, web)
* all tooling built on or alongside Workbench
* all user-facing behavior and system decisions

These principles constrain **all other Workbench specifications**.

---

## 3. Authoring Studio Principle (Normative)

The Paperhat Workbench is an **Authoring Studio**.

It exists to enable users to:

* create
* organize
* inspect
* preview
* produce

structured meaning using Paperhat.

Workbench is not a developer convenience, not a script wrapper, not an IDE, and not a CMS.

It is the authoritative operator of the authoring experience.

---

## 4. Respect for the User (Normative)

Workbench MUST treat users as competent, well-intentioned collaborators.

The system MUST:

* assume good faith
* avoid condescension
* avoid blame
* avoid scolding
* communicate calmly and constructively

Failures indicate insufficient system clarity, not user error.

This principle applies uniformly to all interfaces and diagnostics.

---

## 5. Determinism and Explicitness (Normative)

Workbench behavior MUST be:

* deterministic
* explicit
* reviewable
* repeatable

Workbench MUST NOT:

* infer intent
* guess defaults that affect behavior
* consult ambient environment, time, randomness, or network state
* perform silent or implicit actions

Same inputs and versions MUST yield the same results.

---

## 6. Immutable Authoring Boundary (Normative)

User-authored content is **sacrosanct**.

Workbench MUST NOT modify authored content except when:

* explicitly instructed
* through a deterministic and reviewable plan
* with refusal-by-default semantics

Workbench MUST NOT:

* auto-correct
* rewrite
* “fix”
* infer improvements
* mutate authored content implicitly

Observation is permitted.
Mutation requires explicit consent.

---

## 7. Queryable Introspection (Normative)

Workbench MUST support **read-only introspection** into its internal products.

Introspection MAY include:

* work structure
* assembled artifacts
* resolved identifiers and references
* graphs and relationships
* ViewModels
* Presentation Plans
* File Plans
* build artifacts

All introspection MUST be:

* deterministic
* snapshot-based
* non-mutating

Workbench may explain everything.
Workbench may invent nothing.

---

## 8. Orchestration Without Semantics (Normative)

Workbench is responsible for **orchestration**, not meaning.

Workbench MUST:

* sequence pipeline stages deterministically
* invoke authoritative subsystems
* enforce boundaries and contracts

Workbench MUST NOT:

* define semantic rules
* bypass validation
* embed meaning or policy

Semantic authority resides elsewhere.

---

## 9. Governance Boundary (Normative)

Workbench is the **compatibility and behavior gatekeeper**.

Workbench MUST enforce:

* explicit version requirements
* specification compatibility
* refusal on undefined or unspec’d behavior

Rule:

> If it is not specified, it does not exist.

No heuristics.
No convenience behavior.
No silent fallback.

---

## 10. No Leakage (Normative)

Responsibilities MUST NOT bleed across boundaries.

In particular:

* semantics MUST NOT leak into Workbench
* UX MUST NOT affect Core behavior
* tooling MUST NOT contaminate authored meaning
* convenience MUST NOT override determinism

Leakage is a design error.

---

## 11. Assistive Systems Discipline (Normative)

Assistive systems, including AI, MUST be constrained.

Assistive systems MAY:

* guide
* suggest
* ask questions
* propose changes

Assistive systems MUST NOT:

* mutate authored content
* apply changes implicitly
* bypass review or refusal semantics

All assistive output MUST pass through explicit, reviewable mechanisms.

---

## 12. Interaction Surface Equality (Normative)

All interaction surfaces are **clients** of the same Workbench Core.

No surface has additional authority.

Differences between surfaces are presentation-only and MUST NOT affect behavior.

---

## 13. Reality Rule (Normative)

This specification defines how Workbench **is**.

There is no legacy behavior.
There are no deprecated modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
