Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Integrations and Credentials Specification

This specification defines Paperhat’s target-independent semantics for **integrations** (connectors) and **credential requirements** for external actions.

This document governs **meaning, constraints, and planning interfaces only**.
It does **not** define network protocols, HTTP request formats, vendor APIs, secret storage mechanisms, or deployment concerns.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define integration operations as semantic identifiers
* define how external actions declare required credentials and secrets without embedding them
* enable state-of-the-art workflow capabilities without collapsing Kernel into an integration framework
* preserve target independence by separating meaning from realization
* ensure auditability and explainability of external action requirements

---

## 2. Scope

This specification governs:

* integration providers and operations as semantic vocabulary
* credential and secret requirements for external actions
* provenance and verification requirements for external results
* how workflows reference integration operations

This specification does **not** govern:

* protocol mechanics (HTTP, OAuth flows, webhooks)
* vendor-specific request schemas
* secret vault implementations
* credential acquisition user interfaces
* scheduling, retry, or backoff mechanics

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../../workflow/workflow-orchestration/)
* [Authentication and Authorization](../authentication-and-authorization/)

---

## 4. Core Invariants (Normative)

The following invariants are non-negotiable:

1. **Integrations are referenced by semantic identity, not by protocol detail.**
2. **Credentials and secrets are never embedded in authored content.**
3. **External action requests may declare requirements; execution is realization.**
4. **No protocol or transport fields.** URLs, headers, methods, queue names, and similar details MUST NOT be semantic content.
5. **Auditability.** It MUST be possible to explain which integration and which credential requirements were involved.

---

## 5. Integration Providers and Operations (Normative)

An **Integration Provider** is a named semantic source of external capabilities.

An **Integration Operation** is a semantic identifier for a callable capability.

Integration Operations MUST declare:

* operation identity
* expected input schema
* expected output schema
* required credential kinds (see §6)
* provenance requirements for returned results (see §7)

Integration Operations MUST NOT declare protocol mechanics.

---

## 6. Credentials and Secrets (Normative)

### 6.1 Credential Requirement

A Credential Requirement declares that an external action requires a credential of a specific kind.

Credential Requirements MUST:

* identify required credential kind
* define required scope/claims (if applicable)
* define validity constraints

Credential Requirements MUST NOT:

* include secret material
* include protocol mechanics

### 6.2 Secret Requirement

A Secret Requirement declares that an external action requires access to named secret material.

Secret Requirements MUST:

* identify secret name or identifier
* define usage constraints

Secret Requirements MUST NOT embed secret values.

---

## 7. External Results and Provenance (Normative)

External action results MUST be bound as explicit results with provenance.

Kernel MUST allow integration operations to declare:

* what provenance is required
* what verification constraints apply

Verification mechanisms are realization details.

---

## 8. Workflow Integration (Normative)

Workflows MAY reference integration operations via `RequestExternalAction`.

`RequestExternalAction` MUST reference:

* an action kind identifier (which may identify an Integration Operation)
* required inputs
* expected output schema
* credential and secret requirements

Workflows MUST remain target-independent.

---

## 9. Target Independence (Normative)

This specification MUST NOT define:

* vendor APIs
* network protocols
* credential acquisition flows
* secret storage implementations

Targets MAY map semantic integration operations to concrete implementations, provided semantic requirements are preserved.
