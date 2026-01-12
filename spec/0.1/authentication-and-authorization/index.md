Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Authentication and Authorization Specification

This specification defines Paperhat’s target-independent semantics for **authentication** and **authorization** as declarative data.

This document governs **semantic meaning and constraints only**.
It does **not** define user interface flows, protocols, cryptographic algorithms, password handling, transport mechanisms, or deployment architecture.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define authentication and authorization as declarative semantic constructs
* require passwordless authentication as the default (for example, passkeys)
* model proofs, sessions, and claims as data with explicit validity constraints
* define authorization decisions as deterministic evaluation over facts and inputs
* preserve target independence by separating meaning from realization

---

## 2. Scope

This specification governs:

* identity, principals, credentials, proofs, claims, and sessions
* policy definitions for authentication and authorization
* access requests and access decisions
* how authorization integrates with Commands, Events, and Guards
* auditability requirements for security decisions

This specification does **not** govern:

* any specific authentication protocol
* key storage mechanisms
* cryptographic algorithm selection
* transport and session cookie mechanics
* user interface components or flows

---

## 3. Core Invariants (Hard)

The following invariants are non-negotiable:

1. **Security is semantic.** Security properties are expressed as authoritative data.
2. **Authentication is proof evaluation, not a user interface flow.**
3. **Authorization is deterministic evaluation.** Decisions are derived from facts and explicit inputs.
4. **No implicit inputs.** Actor identity, time, and environment must be explicit inputs.
5. **No passwords.** Password-based authentication MUST NOT be supported by Paperhat.
6. **Auditability.** Security decisions MUST be explainable and recordable.

---

## 4. Definitions (Normative)

### 4.1 Principal

A **Principal** is the semantic subject of authentication and authorization.

A Principal may represent:

* a human
* a service
* a device
* a delegated capability bearer

---

### 4.2 Credential and Proof

A **Credential** is a registered authenticator binding (for example, a public-key credential).

A **Proof** is evidence presented to satisfy an authentication policy.

Credentials are persisted facts.
Proofs are evaluated inputs.

---

### 4.3 Claim

A **Claim** is an asserted property about a Principal.

Claims may be:

* derived from verified proofs
* derived from authoritative facts
* derived from policy evaluation

Claims MUST have explicit validity constraints.

---

### 4.4 Session

A **Session** is a bounded authorization context that:

* binds a Principal to a set of verified claims
* has explicit validity constraints (expiry, revocation semantics)
* can be referenced by targets without redefining security meaning

A Session is not a protocol mechanism.
A Session is semantic state.

---

## 5. Authentication (Normative)

### 5.1 Passwordless Default

Paperhat authentication MUST be passwordless.

Semantics MUST support passwordless credential types, including public-key credentials.

Semantics MAY support fallback authentication mechanisms, but MUST NOT support passwords.

---

### 5.2 Authentication Policy

An Authentication Policy defines:

* what proofs are required
* what claims are produced when proofs validate
* what validity constraints apply

Authentication Policy MUST be declarative.

---

### 5.3 Proof Evaluation (Pipeline Responsibility)

Pipeline MUST evaluate proofs deterministically given:

* the declared authentication policy
* the presented proofs
* explicit external inputs (time, issuer keys, environment)

If proof validation fails, Pipeline MUST return Help/diagnostics outcomes.

---

## 6. Authorization (Normative)

### 6.1 Authorization Policy

An Authorization Policy defines:

* what access requests exist
* what claims, roles, permissions, or capabilities satisfy them
* any required contextual constraints (time windows, resource attributes)

Authorization Policy MUST be declarative.

---

### 6.2 Access Request

An Access Request MUST specify:

* actor (Principal or Session reference)
* action being requested
* resource being accessed
* context inputs required for evaluation

---

### 6.3 Access Decision

An Access Decision MUST include:

* allow or deny
* Help/diagnostics explaining the decision
* references to the rules and inputs involved

Authorization evaluation MUST be deterministic given identical facts and inputs.

---

## 7. Integration with Commands, Events, and Guards (Normative)

Security policies integrate with intent and facts:

* Command evaluation MAY require authorization checks.
* Event publication MAY be gated by authorization checks.
* Guards MAY reference claims, roles, permissions, or capabilities.

Actor identity and any security-relevant context MUST be modeled as explicit external inputs.

---

## 8. Capabilities, Roles, and Permissions (Normative)

Semantics MUST support at least one of the following authorization idioms:

* **Capabilities** — explicit delegatable rights
* **Roles and Permissions** — role membership with permission grants
* **Attribute-based rules** — policy decisions based on attributes

If multiple idioms are supported, Semantics MUST define precedence and composition rules.

---

## 9. Auditability (Hard)

Security decisions MUST be auditable.

At minimum, the system MUST be able to record:

* the access request
* the decision
* the policy rule identifiers involved
* the time and relevant context inputs

The representation and storage mechanism is a realization detail.

---

## 10. Target Independence (Hard)

This specification MUST NOT require:

* a specific protocol (for example, HTTP)
* a specific authenticator mechanism
* a specific user interface flow
* a specific session transport (for example, cookies)

Targets MAY realize authentication and authorization using target-appropriate mechanisms, as long as semantic meaning and constraints are preserved.
