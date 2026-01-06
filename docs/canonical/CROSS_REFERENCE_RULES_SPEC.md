# CROSS_REFERENCE_RULES_SPEC

**Status:** CANONICAL  
**Lock State:** LOCKED  
**Audience:** Orchestrators, Validators, Human Authorities  
**Non-Audience:** Work Packet Executors, Runtime Systems, Application Developers

---

## 1. Purpose

The **Cross-Reference Rules Specification** defines the mandatory rules governing how artifacts within the Sitebender Codex corpus may reference one another.

Its purpose is to:

- prevent circular authority
- preserve unidirectional authority flow
- ensure references are stable, explicit, and auditable
- eliminate ambiguity introduced by informal citation

Cross-referencing is an authority-bearing act and is therefore governed.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- constrains reference form, legality, and direction only

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Definition

A **Cross-Reference** is any explicit citation, mention, or dependency whereby one artifact relies on another for authority, definition, or constraint.

Incidental mention without authority reliance does not constitute a cross-reference.

---

## 4. Reference Legality Invariant

A cross-reference is legal only if:

- the referenced artifact exists
- the referenced artifact is identifiable
- the reference respects authority flow
- the reference does not introduce dependency ambiguity

Any violation renders the referencing artifact invalid.

---

## 5. Authority Direction Rule

Authority MUST flow strictly downward:

**Canonical Specifications
→ Governance Artifacts
→ Orchestration
→ Work Packets
→ Execution Outputs
→ Audit Artifacts**

No artifact may reference upward or laterally in a way that implies authority.

---

## 6. Permitted Reference Matrix

The following reference relationships are permitted:

- Canonical Specifications → Canonical Specifications
- Governance Artifacts → Canonical Specifications
- Orchestration Decision Records → Canonical Specifications, Work Packets, Outputs
- Work Packets → Canonical Specifications
- Audit Artifacts → Any artifact class

All other reference relationships are prohibited.

---

## 7. Prohibited Reference Patterns

The following patterns are explicitly forbidden:

- Canonical Specifications referencing Outputs
- Canonical Specifications referencing Work Packets
- Work Packets referencing Outputs
- Outputs referencing any Canonical artifact
- Circular references of any kind
- Implicit or inferred references

Violation constitutes system failure.

---

## 8. Reference Precision Requirements

All cross-references MUST:

- name the artifact explicitly
- avoid pronouns or shorthand
- avoid “this document” or “the above”
- be resolvable without external context

Ambiguous references are invalid.

---

## 9. Version and State Awareness

References MUST respect artifact state:

- Draft artifacts MUST NOT be referenced authoritatively
- Superseded artifacts MAY be referenced only for historical context
- Locked artifacts MAY be referenced freely
- Canonical but unlocked artifacts MAY be referenced with caution

Implicit version selection is prohibited.

---

## 10. Temporal Constraint

Artifacts MUST NOT reference:

- future artifacts
- hypothetical documents
- “upcoming” revisions
- planned supersessions

All references MUST be to extant artifacts.

---

## 11. Reference Scope Limitation

A reference MUST be limited to:

- the minimum required authority
- the specific document or section relevant

Broad or blanket references (“all contracts”, “the system spec”) are prohibited.

---

## 12. Reference Form

References MUST be:

- explicit
- declarative
- non-narrative

Embedded commentary about referenced artifacts is prohibited.

---

## 13. Enforcement

- Orchestrators MUST reject artifacts with illegal references
- Validators MUST flag reference violations
- Human Authorities resolve escalations involving reference legality

No role may waive cross-reference compliance.

---

## 14. Auditability

All references MUST be:

- reviewable in isolation
- traceable to an existing artifact
- sufficient to establish authority provenance

Untraceable references are invalid.

---

## 15. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any artifact containing non-compliant cross-references is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
