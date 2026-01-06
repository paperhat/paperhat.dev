# LIBRARY_REGISTRY_SPEC

**Status:** CANONICAL
**Lock State:** LOCKED
**Audience:** Human Authorities, Orchestrators
**Non-Audience:** Work Packet Executors, Runtime Systems, Application Developers

---

## 1. Purpose

The **Library Registry Specification** defines the authoritative set of Sitebender libraries and their **normative responsibility boundaries**.

Its purpose is to:

- provide a concise, system-level orientation
- establish and preserve clear ownership boundaries
- prevent semantic leakage between libraries
- enable accurate system rehydration in new sessions

This document is a **boundary map**, not an implementation guide.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- records responsibility boundaries and scope only
- serves as an index into existing contracts and specifications

In the event of conflict, this document yields to referenced LOCKED contracts.

---

## 3. Inclusion Rule

Only libraries with **established, reviewed contracts and demonstrated semantic clarity** are included.

Absence from this registry implies **intentional non-inclusion**, not omission.

Libraries are added **incrementally**, one at a time, as understanding becomes canonical.

---

## 4. Registry Structure

Each library entry defines:

- **Name**
- **Primary Responsibility**
- **Owned Concerns**
- **Explicit Non-Responsibilities**
- **Authoritative Contracts**

This structure is mandatory and uniform.

---

## 5. Sitebender Codex

### 5.1 Primary Responsibility

Sitebender Codex defines the **governing semantic, execution, and authority framework** for the entire Sitebender ecosystem.

It is the system of record for **what rules exist, who may act, and how meaning is preserved**.

---

### 5.2 Owned Concerns

- CDX as a human-first language
- Canonical specifications and contracts
- Orchestration, Work Packets, and execution law
- Role definitions and authority boundaries
- Artifact classification and authority flow
- Failure handling and escalation
- Governance, locking, and supersession

---

### 5.3 Explicit Non-Responsibilities

Sitebender Codex does **not**:

- implement application logic
- define runtime behavior
- perform IO
- own domain-specific semantics
- render or persist content

Codex governs; it does not execute.

---

### 5.4 Authoritative Contracts

- CODEX_SYSTEM_CONTRACT
- CDX_LANGUAGE_SPEC
- WORK_PACKET_SPEC
- ORCHESTRATION_CONTRACT
- EXECUTION_ROLES_SPEC
- ARTIFACT_REGISTRY_SPEC
- FAILURE_AND_ESCALATION_SPEC
- GOVERNANCE_AND_LOCKING_SPEC
- WORK_PACKET_TEMPLATE_SPEC
- ORCHESTRATION_DECISION_RECORD_SPEC
- CDX_COMPLIANCE_ENFORCEMENT_SPEC
- NAMING_AND_VOCABULARY_SPEC
- DOCUMENT_STYLE_AND_TONE_SPEC
- CROSS_REFERENCE_RULES_SPEC

---

## 6. Toolsmith

### 6.1 Primary Responsibility

Toolsmith provides **foundational functional abstractions** used across Sitebender libraries, with a strong emphasis on **determinism, composability, and explicit semantics**.

---

### 6.2 Owned Concerns

- Validation and accumulation semantics
- “Helps, not errors” philosophy
- Guard functions and usability checks
- Deterministic composition primitives
- Performance-aware functional patterns

---

### 6.3 Explicit Non-Responsibilities

Toolsmith does **not**:

- define CDX semantics
- perform orchestration
- encode business logic
- manage execution flow
- interpret human intent

It supplies tools; it does not decide.

---

### 6.4 Authoritative Contracts

- Toolsmith Contract (LOCKED)

---

## 7. Scribe

### 7.1 Primary Responsibility

Scribe owns the **end-to-end CDX pipeline**, from human-authored CDX input through internal representation to rendered output.

---

### 7.2 Owned Concerns

- CDX ingestion and parsing
- AST and IR construction
- Semantic preservation across transformations
- Rendering and presentation preparation
- Coordination of the authoring pipeline

---

### 7.3 Explicit Non-Responsibilities

Scribe does **not**:

- define CDX language rules
- own IO mechanisms
- perform routing
- enforce governance
- define domain semantics

Scribe executes the pipeline; it does not govern it.

---

### 7.4 Authoritative Contracts

- SCRIBE_PIPELINE_SPEC
- PRESENTATION_PLAN_SPEC
- VIEWMODEL_CONTRACT

---

## 8. Architect

### 8.1 Primary Responsibility

Architect defines a **semantic language for encoding data and views on that data**, used as a foundational abstraction layer across Sitebender libraries.

---

### 8.2 Owned Concerns

- Declarative semantic encoding
- View definitions over structured data
- Shared semantic vocabulary for representation

---

### 8.3 Explicit Non-Responsibilities

Architect does **not**:

- own the CDX language
- govern execution
- define application state management
- replace higher-level Sitebender libraries

Architect enables expression; it does not own the system.

---

### 8.4 Authoritative Contracts

- Architect Contract (LOCKED)

---

## 9. Registry Invariants

The following invariants are mandatory:

- Each library owns a distinct semantic domain
- No library may silently absorb another’s responsibility
- Cross-library interaction occurs only through contracts
- Absence of ownership implies prohibition

Boundary violations constitute architectural failure.

---

## 10. Evolution Rule

This registry evolves only by:

- adding new library entries
- explicitly expanding an existing entry
- Human Authority approval
- locking under governance rules

Existing entries MUST NOT be weakened or blurred.

---

## 11. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any reasoning, implementation, or execution behavior that violates the boundaries defined here is **non-compliant with Sitebender Codex**.
