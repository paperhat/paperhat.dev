Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Documentation Governance

## 1. Purpose

This document defines the **governance rules** for the documentation published at **paperhat.dev**.

Its purpose is to:

* establish **authority and precedence** among documents
* define **normative status**, lock state, and change control
* clarify the relationship between documentation and implementations
* prevent ambiguity, drift, and misinterpretation by humans or automated systems

This document governs **documentation only**.

---

## 2. Scope

This governance applies to all content published in the paperhat.dev repository, including but not limited to:

* system contracts
* library contracts
* formal specifications
* architectural definitions
* examples and notes

It does **not** govern software implementations, tools, or runtime systems, which are maintained in separate repositories under separate licenses.

---

## 3. Document Categories

Documentation in this repository is categorized as follows:

### 3.1 Normative Documents

Normative documents define **binding architectural, semantic, or structural rules**.

Examples include:

* System Contracts
* Library Contracts
* Formal Specifications
* Naming and Assembly Contracts
* Pipeline and Boundary Definitions

Normative documents may be marked **LOCKED** or **DRAFT**.

### 3.2 Non-Normative Documents

Non-normative documents provide:

* explanatory material
* rationale
* historical context
* exploratory notes
* future ideas

These documents are explicitly **non-authoritative** and may change freely.

---

## 4. Lock State

### 4.1 LOCKED

A document marked **LOCKED**:

* is authoritative
* MUST NOT be changed except via an explicit versioned revision
* requires deliberate review and justification to modify
* serves as a stable reference for implementations and tooling

LOCKED documents are intended to be safe inputs for automated systems.

### 4.2 DRAFT

A document marked **DRAFT**:

* is under active development
* may change without notice
* MUST NOT be relied upon as authoritative

---

## 5. Authority Order

In the event of conflict, documents are interpreted according to the following precedence (highest first):

1. **Paperhat System Contract**
2. **Library Contracts**
3. **Formal Specifications**
4. **Normative Supporting Documents**
5. **Examples**
6. **Notes**

Lower-authority documents MUST NOT contradict higher-authority documents.

---

## 6. Relationship to Implementations

The documentation in this repository:

* defines **intent, architecture, semantics, and invariants**
* does **not** mandate any specific implementation strategy
* does **not** grant rights to any software implementation

Software implementations:

* are independent works
* may be licensed separately
* may evolve independently, provided they honor applicable normative contracts

---

## 7. Licensing

All documentation in this repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)** as described in the repository’s `LICENSE` file.

The license applies to **textual, diagrammatic, and illustrative content only**.

No rights are granted to:

* trademarks, service marks, or logos
* project, language, or specification names
* software implementations, unless explicitly stated otherwise

---

## 8. Final Authority

This document is **NORMATIVE and LOCKED**.

Any interpretation of paperhat.dev documentation MUST be consistent with this governance.

---

**End of Paperhat Documentation Governance v0.1**
