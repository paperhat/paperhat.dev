Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Artifacts and Attachments Specification

This specification defines Paperhat’s target-independent semantics for **artifacts**, **attachments**, and **binary references** produced and consumed by workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define storage backends, content-addressing algorithms, transport protocols, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows to reference binary data without embedding it in authored artifacts
* define stable artifact identity and provenance expectations
* enable deterministic planning with explicit external data references
* preserve auditability of artifact creation and consumption

---

## 2. Scope

This specification governs:

* artifact identity and metadata
* attachment references and lifetimes (semantic)
* creation and consumption as workflow steps
* integrity expectations (semantic)
* privacy and access intent (semantic)
* recordability requirements

This specification does **not** govern:

* concrete storage technologies
* content-addressing and hashing implementations
* upload/download protocols
* encryption algorithms

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Integrations and Credentials](../integrations-and-credentials/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Data Stores and Shared Variables](../data-stores-and-shared-variables/)

---

## 4. Core Invariants (Normative)

1. **No embedded binaries.** Authored workflow artifacts MUST NOT embed binary payloads.
2. **References are explicit.** Artifact and attachment references MUST be explicit values.
3. **Deterministic planning.** Kernel MUST be able to plan artifact steps deterministically.
4. **Provenance is recordable.** It MUST be possible to record where an artifact came from and how it was used.
5. **Target independence.** Kernel MUST NOT assume a storage backend or protocol.

---

## 5. Definitions (Normative)

### 5.1 Artifact

An **Artifact** is a referenced piece of data (often binary) that workflows may produce or consume.

An Artifact MUST include:

* artifact identity
* declared media type (semantic)
* declared size metadata (when available)
* provenance references

---

### 5.2 Attachment

An **Attachment** is an artifact intended to be associated with another semantic subject (for example, a run, a step attempt, or a decision).

---

### 5.3 Artifact Reference

An **ArtifactReference** is a value that identifies an artifact without embedding its content.

ArtifactReference MAY include:

* a stable identifier
* optional integrity metadata (semantic)

---

### 5.4 Integrity Expectation

An **IntegrityExpectation** is a declarative constraint for verifying an artifact reference.

Integrity expectations MUST be semantic and MUST NOT mandate a particular hashing algorithm.

---

### 5.5 Lifetime and Retention Intent

A **RetentionIntent** is a declarative statement about expected lifetime.

Retention intent MUST be target-independent.

---

## 6. Artifact Creation Semantics (Normative)

Workflows MAY include steps that produce artifacts.

An artifact-producing step MUST declare:

* artifact identity
* output artifact reference
* provenance references

---

## 7. Artifact Consumption Semantics (Normative)

Workflows MAY include steps that consume artifacts.

An artifact-consuming step MUST declare:

* expected artifact identity or type
* required integrity expectations (if any)

---

## 8. Privacy and Access Intent (Normative)

Artifact references MAY be subject to access intent.

Access intent MUST be expressed semantically (for example, via authorization constructs), and MUST NOT embed credential material.

---

## 9. Reliability Interaction (Normative)

Artifact transfer failures MUST be representable as typed failures.

Reliability policy MAY apply to artifact operations, but must remain auditable.

---

## 10. Recordability (Normative)

Run logs MUST be able to record:

* artifact reference identities
* creation and consumption events
* provenance references
* integrity expectation checks (success/failure)

Records MUST NOT require embedding secrets.

---

## 11. Target Independence (Normative)

This specification MUST NOT define:

* storage services
* upload/download protocols
* hashing algorithms

Targets may realize artifacts using any appropriate mechanism, provided semantic meaning and recordability requirements are preserved.
