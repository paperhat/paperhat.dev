# ARTIFACT_REGISTRY_SPEC

**Status:** CANONICAL  
**Lock State:** LOCKED  
**Audience:** Orchestrators, Validators, Human Authorities  
**Non-Audience:** Runtime engines, application developers

---

## 1. Purpose

The **Artifact Registry Specification** defines the authoritative classes of artifacts within the Sitebender Codex system and the rules governing their creation, immutability, reference, and authority.

Its purpose is to:

- prevent circular authority
- prevent silent mutation of meaning
- preserve auditability
- ensure that authority flows in one direction only

Artifacts are the **only durable record** of system state and intent.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- defines classification and governance rules only
- does not prescribe storage, tooling, or format

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Definition

An **Artifact** is any discrete, reviewable output produced, referenced, or governed by the Sitebender Codex system.

Artifacts are immutable units of meaning.
They may be superseded, but never altered.

---

## 4. Artifact Classes

The following artifact classes are **exhaustive**.

No other artifact classes are permitted.

---

## 5. Canonical Specifications

### 5.1 Definition

**Canonical Specifications** define the semantic, architectural, or governance rules of the system.

Examples include:

- system contracts
- language specifications
- pipeline specifications
- governance documents

---

### 5.2 Authority

Canonical Specifications are the **highest authority artifacts**.

---

### 5.3 Immutability

Once LOCKED:

- they MUST NOT be modified
- they MAY be superseded only by explicit replacement
- historical versions remain authoritative for their issuance period

---

### 5.4 Reference Rules

Canonical Specifications:

- MAY reference other Canonical Specifications
- MUST NOT reference Work Packets or Outputs
- MUST NOT depend on execution artifacts

---

## 6. Work Packets

### 6.1 Definition

**Work Packets** are execution contracts issued by Orchestration.

They are defined normatively in WORK_PACKET_SPEC.

---

### 6.2 Authority

Work Packets derive authority from:

- Orchestration
- referenced Canonical Specifications

They introduce no independent authority.

---

### 6.3 Immutability

Once issued:

- Work Packets are immutable
- corrections require issuance of a new packet
- original packets remain auditable artifacts

---

### 6.4 Reference Rules

Work Packets:

- MAY reference Canonical Specifications
- MUST NOT reference Outputs from other packets
- MUST NOT reference future or hypothetical artifacts

---

## 7. Execution Outputs

### 7.1 Definition

**Execution Outputs** are artifacts produced by Work Packet Executors.

---

### 7.2 Authority

Execution Outputs have **no authority**.

They are evaluated solely against:

- Work Packet criteria
- referenced Canonical Specifications

---

### 7.3 Immutability

Execution Outputs:

- MUST NOT be altered after submission
- MAY be rejected or superseded
- remain auditable even if invalid

---

### 7.4 Reference Rules

Execution Outputs:

- MUST NOT be referenced by Canonical Specifications
- MAY be referenced by audit artifacts
- MUST NOT be treated as normative sources

---

## 8. Validation and Audit Artifacts

### 8.1 Definition

**Validation and Audit Artifacts** record evaluation, findings, and compliance status.

---

### 8.2 Authority

These artifacts:

- do not alter authority
- do not modify other artifacts
- exist solely to document compliance

---

### 8.3 Reference Rules

Audit artifacts:

- MAY reference any artifact class
- MUST NOT be referenced by Canonical Specifications
- MUST NOT introduce new requirements

---

## 9. Governance Artifacts

### 9.1 Definition

**Governance Artifacts** define locking, supersession, and authority transitions.

---

### 9.2 Authority

Governance Artifacts define _process_, not semantics.

They do not override Canonical Specifications.

---

### 9.3 Reference Rules

Governance Artifacts:

- MAY reference Canonical Specifications
- MUST NOT depend on Execution Outputs

---

## 10. Authority Flow Invariant

Authority flows strictly in one direction:

**Canonical Specifications
→ Orchestration
→ Work Packets
→ Execution Outputs**

No artifact may derive authority from an artifact below it.

---

## 11. Prohibited Relationships

The following are explicitly forbidden:

- Canonical Specifications citing Outputs
- Outputs redefining rules
- Work Packets modifying Canonical text
- Audit artifacts acting as authority
- Circular citation of any kind

Violation constitutes system failure.

---

## 12. Supersession Rules

Supersession:

- MUST be explicit
- MUST identify the superseded artifact
- MUST NOT retroactively alter meaning
- preserves historical auditability

Implicit supersession is prohibited.

---

## 13. Artifact Identity

Each artifact MUST be:

- uniquely identifiable
- attributable to its issuer
- reviewable in isolation

Anonymous or ambiguous artifacts are invalid.

---

## 14. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any artifact handling or reference behavior inconsistent with this specification is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
