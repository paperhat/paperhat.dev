# ORCHESTRATION_DECISION_RECORD_SPEC

**Status:** CANONICAL  
**Lock State:** LOCKED  
**Audience:** Orchestrators, Validators, Human Authorities  
**Non-Audience:** Work Packet Executors, Runtime Systems

---

## 1. Purpose

The **Orchestration Decision Record Specification** defines the mandatory structure and constraints for recording decisions made during orchestration within the Sitebender Codex system.

Its purpose is to:

- ensure decisions are explicit and auditable
- prevent implicit or undocumented judgment
- preserve traceability from intent to outcome
- enable review without reconstructive inference

This specification governs **decision recording only**, not decision-making.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- constrains record structure and admissible content only

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Definition

An **Orchestration Decision Record (ODR)** is a durable artifact that documents a single orchestration decision affecting execution state.

An ODR does not justify decisions philosophically.
It records **what decision was made and under what authority**.

---

## 4. Decision Scope

An ODR MUST be created for each of the following decisions:

- Work Packet issuance
- Work Packet acceptance
- Work Packet rejection
- Retry authorization
- Escalation initiation
- Escalation resolution
- Execution halt or termination

No other decisions require an ODR.
All listed decisions require exactly one ODR.

---

## 5. Required Sections (In Order)

The following sections are **mandatory and ordered**.

No additional sections are permitted.

---

## 6. Decision Identifier

### 6.1 Definition

A unique identifier for the decision.

---

### 6.2 Constraints

The identifier MUST:

- uniquely identify the decision
- be stable and referable
- not encode meaning beyond identity

---

## 7. Decision Type

### 7.1 Definition

The **Decision Type** classifies the decision.

---

### 7.2 Constraints

Decision Type MUST be one of:

- Issuance
- Acceptance
- Rejection
- Retry Authorization
- Escalation
- Escalation Resolution
- Termination

No other values are permitted.

---

## 8. Subject Artifacts

### 8.1 Definition

**Subject Artifacts** identify the artifacts affected by the decision.

---

### 8.2 Constraints

Subject Artifacts MUST:

- explicitly list artifact identifiers
- reference only existing artifacts
- avoid indirect or implied references

---

## 9. Authority Basis

### 9.1 Definition

The **Authority Basis** records the source of authority under which the decision was made.

---

### 9.2 Constraints

Authority Basis MUST reference:

- the acting role (e.g., Orchestrator, Human Authority)
- applicable LOCKED canonical documents

Narrative justification is prohibited.

---

## 10. Decision Outcome

### 10.1 Definition

The **Decision Outcome** records the concrete result of the decision.

---

### 10.2 Constraints

Decision Outcome MUST:

- be explicit and unambiguous
- describe the resulting execution state
- avoid rationale or explanation

---

## 11. Preconditions (Optional)

### 11.1 Definition

**Preconditions** record explicit conditions that were required for the decision to apply.

---

### 11.2 Constraints

If present, Preconditions MUST:

- be factual
- be verifiable
- avoid interpretation

Preconditions are optional and MUST NOT be used to introduce reasoning.

---

## 12. Prohibited Content

An Orchestration Decision Record MUST NOT include:

- reasoning chains
- speculative language
- alternatives considered
- qualitative assessment
- forward-looking plans

Any such content invalidates the record.

---

## 13. Immutability

Once created:

- an ODR is immutable
- corrections require a new ODR
- supersession must be explicit

Historical records MUST remain intact.

---

## 14. Review and Audit

ODRs MUST be:

- reviewable in isolation
- sufficient to reconstruct execution state
- attributable to the acting authority

Missing or ambiguous records constitute orchestration failure.

---

## 15. Relationship to Other Artifacts

ODRs:

- MAY reference Canonical Specifications
- MAY reference Work Packets and Outputs
- MUST NOT be referenced by Canonical Specifications
- MUST NOT introduce authority

ODRs are records, not rules.

---

## 16. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any orchestration decision made without a conforming Orchestration Decision Record is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
