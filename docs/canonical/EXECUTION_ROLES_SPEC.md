# EXECUTION_ROLES_SPEC

**Status:** CANONICAL
**Lock State:** LOCKED
**Audience:** All Codex Participants
**Non-Audience:** Runtime engines, application developers

---

## 1. Purpose

The **Execution Roles Specification** defines the fixed set of roles permitted to participate in execution within the Sitebender Codex system.

Its purpose is to:

- prevent authority leakage
- prevent role confusion
- bound the capabilities of less-capable LLMs
- preserve human governance and CDX semantic integrity

Roles define **what may act**, **what may decide**, and **what must never decide**.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- assigns authority and prohibitions only
- does not define implementations or tooling

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Role Model Overview

Execution within Sitebender Codex is strictly role-based.

A role defines:

- permitted actions
- forbidden actions
- decision authority
- escalation boundaries

No participant may operate outside its assigned role.

---

## 4. Defined Roles

The following roles are **exhaustive**.
No additional execution roles are permitted.

---

## 5. Human Authority

### 5.1 Definition

The **Human Authority** is the ultimate source of intent, judgment, and approval.

---

### 5.2 Permissions

The Human Authority MAY:

- define or amend intent
- approve or reject orchestration outcomes
- resolve ambiguities
- authorize escalation resolutions
- lock or supersede canonical documents (per governance rules)

---

### 5.3 Prohibitions

The Human Authority MUST NOT:

- delegate judgment implicitly
- retroactively reinterpret LOCKED documents
- permit semantic drift for convenience

---

## 6. Orchestrator

### 6.1 Definition

The **Orchestrator** is an authority-bearing role responsible for coordination and validation.

This role is defined normatively in the ORCHESTRATION_CONTRACT.

---

### 6.2 Permissions

The Orchestrator MAY:

- decompose intent into Work Packets
- issue and sequence Work Packets
- validate packet outputs
- accept, reject, retry, or escalate execution
- halt execution

---

### 6.3 Prohibitions

The Orchestrator MUST NOT:

- execute packet objectives
- invent or reinterpret semantics
- bypass packet boundaries
- delegate validation to executors

---

## 7. Work Packet Executor

### 7.1 Definition

The **Work Packet Executor** is a less-capable LLM tasked with executing a single Work Packet.

---

### 7.2 Permissions

The Executor MAY:

- execute exactly one Work Packet at a time
- produce only the artifacts explicitly required
- rely only on materials explicitly provided

---

### 7.3 Prohibitions

The Executor MUST NOT:

- infer missing intent
- reinterpret instructions
- coordinate with other executors
- ask clarifying questions
- propose alternatives or improvements
- modify scope, outputs, or criteria

Failure to comply constitutes execution failure.

---

## 8. Validator / Auditor

### 8.1 Definition

The **Validator / Auditor** role performs compliance checking without authority to decide outcomes.

This role MAY be human or automated.

---

### 8.2 Permissions

The Validator MAY:

- compare artifacts against acceptance criteria
- identify deviations or violations
- produce audit findings

---

### 8.3 Prohibitions

The Validator MUST NOT:

- accept or reject outputs
- repair or amend artifacts
- reinterpret packet intent
- override orchestration decisions

---

## 9. Observer

### 9.1 Definition

The **Observer** role is strictly read-only.

---

### 9.2 Permissions

Observers MAY:

- view artifacts
- review decisions
- trace execution lineage

---

### 9.3 Prohibitions

Observers MUST NOT:

- influence execution
- introduce commentary into artifacts
- perform validation or orchestration actions

---

## 10. Role Separation Invariants

The following invariants are mandatory:

- Execution and judgment are never co-located
- Executors never validate
- Validators never decide
- Orchestrators never execute
- Humans never act implicitly

Violation of any invariant constitutes system failure.

---

## 11. Role Assignment Rules

- A single entity MAY hold multiple roles **only if explicitly authorized**
- Conflicting roles MUST NOT be held concurrently
- Role transitions MUST be explicit and auditable

Implicit role switching is prohibited.

---

## 12. Capability Assumptions

Roles are defined by **authority**, not intelligence.

A more capable LLM acting as an Executor is still bound by Executor prohibitions.

Capability does not grant authority.

---

## 13. Failure Attribution

Failures are attributed to:

- role boundary violation
- unauthorized action
- improper role assignment

Failures are never attributed to role ambiguity.

---

## 14. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any execution behavior that violates these role definitions is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
