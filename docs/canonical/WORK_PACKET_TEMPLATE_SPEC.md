# WORK_PACKET_TEMPLATE_SPEC

**Status:** CANONICAL
**Lock State:** LOCKED
**Audience:** Orchestrators, Human Authorities
**Non-Audience:** Work Packet Executors, Runtime Systems

---

## 1. Purpose

The **Work Packet Template Specification** defines the **mandatory structural form** of all Work Packets issued within the Sitebender Codex system.

Its purpose is to:

- enforce uniformity
- prevent ambiguity
- ensure executor determinism
- preserve CDX human-first constraints

This specification governs **shape and expression only**, not meaning.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- constrains structure, language form, and completeness only

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Template Invariant

Every Work Packet MUST:

- include all required sections
- include no extraneous sections
- use plain, declarative language
- be executable without interpretation

Omission or deviation renders the packet invalid.

---

## 4. Required Sections (In Order)

The following sections are **mandatory and ordered**.

No additional sections are permitted.

---

## 5. Objective

### 5.1 Definition

The **Objective** states the single outcome the executor must achieve.

---

### 5.2 Constraints

The Objective MUST:

- describe exactly one goal
- be outcome-oriented
- be stated in plain human language
- avoid method, strategy, or justification

The Objective MUST NOT:

- contain sub-goals
- reference execution steps
- include conditional language
- rely on implied context

---

## 6. Scope

### 6.1 Definition

**Scope** defines what is included in execution.

---

### 6.2 Constraints

Scope MUST:

- explicitly enumerate included materials or domains
- be exhaustive
- be unambiguous

Scope MUST NOT:

- rely on “etc.” or similar language
- assume shared background
- overlap with exclusions

---

## 7. Exclusions

### 7.1 Definition

**Exclusions** define what is explicitly out of scope.

---

### 7.2 Constraints

Exclusions MUST:

- be explicit
- prevent overreach
- include common failure temptations

Exclusions MUST NOT:

- contradict Scope
- introduce new objectives

---

## 8. Inputs

### 8.1 Definition

**Inputs** list all authoritative materials the executor may rely on.

---

### 8.2 Constraints

Inputs MUST:

- be complete
- reference only existing artifacts
- avoid indirect or implied sources

Inputs MUST NOT:

- reference future artifacts
- assume external knowledge
- include executor inference

---

## 9. Outputs

### 9.1 Definition

**Outputs** define the exact artifacts to be produced.

---

### 9.2 Constraints

Outputs MUST:

- be concrete and reviewable
- be enumerable
- be limited to what is required

Outputs MUST NOT:

- include optional items
- allow partial fulfillment
- combine multiple artifact classes

---

## 10. Completion Criteria

### 10.1 Definition

**Completion Criteria** define the objective rules for acceptance.

---

### 10.2 Constraints

Completion Criteria MUST:

- be testable without interpretation
- reference explicit properties or conditions
- align exactly with the Objective

Completion Criteria MUST NOT:

- include qualitative judgment
- rely on “sufficient”, “reasonable”, or similar terms
- require inference or intent guessing

---

## 11. Language Constraints

All Work Packet content MUST:

- use declarative sentences
- avoid imperative or procedural phrasing
- avoid developer-centric terminology
- avoid code-shaped constructs

JSON, YAML, pseudo-code, and step lists are prohibited.

---

## 12. Prohibited Content

A Work Packet MUST NOT include:

- rationale or explanation
- alternatives or suggestions
- examples
- commentary
- error handling strategies

Any such content invalidates the packet.

---

## 13. Immutability

Once issued:

- the Work Packet is immutable
- corrections require a new packet
- supersession must be explicit

---

## 14. Validation Responsibility

The Orchestrator is responsible for:

- ensuring template compliance
- rejecting malformed packets
- preventing executor exposure to invalid packets

Executors are not responsible for detecting template violations.

---

## 15. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any Work Packet not conforming exactly to this template is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
