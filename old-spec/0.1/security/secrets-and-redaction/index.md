Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Secrets and Redaction Specification

This specification defines Paperhat’s target-independent semantics for **secrets handling**, **sensitive data classification**, and **redaction**.

This document governs semantic meaning, constraints, and recordability requirements.
It does **not** define secret stores, encryption algorithms, logging backends, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* ensure authored artifacts do not embed secret material
* define how sensitive data may be referenced safely
* define redaction requirements for run logs and other records
* preserve deterministic planning while preventing leakage of sensitive values

---

## 2. Scope

This specification governs:

* secret material prohibition in authored artifacts
* sensitivity classification (semantic)
* redaction intent and required behaviors
* safe referencing of secrets and sensitive values
* recordability constraints for observability

This specification does **not** govern:

* specific secret vault services
* encryption implementations
* logging systems
* regulatory compliance programs

---

## 3. Related Specifications

This specification is designed to compose with:

* [Integrations and Credentials](../integrations-and-credentials/)
* [Run Logs and Observability](../../operations/run-logs-and-observability/)
* [Artifacts and Attachments](../../data/artifacts-and-attachments/)
* [Authentication and Authorization](../authentication-and-authorization/)

---

## 4. Core Invariants (Normative)

1. **No embedded secrets.** Authored artifacts MUST NOT embed secret material.
2. **Secrets are referenced, not copied.** Secret usage MUST be expressed via semantic references.
3. **Redaction is required.** Run logs and records MUST be redactable and must avoid secret leakage.
4. **Deterministic planning.** The Kernel MUST be able to validate secrecy constraints deterministically.
5. **Target independence.** The Kernel MUST NOT assume a particular secret store or logging backend.

---

## 5. Definitions (Normative)

### 5.1 Secret Material

**SecretMaterial** is any value that must not be disclosed, such as private keys, tokens, or raw credential values.

This specification does not enumerate all sensitive values; it defines semantic controls.

---

### 5.2 Sensitive Value

A **SensitiveValue** is a value that may be restricted or redacted based on policy.

Sensitive values MAY include:

* secrets
* personal data
* security-sensitive identifiers

---

### 5.3 Sensitivity Classification

A **SensitivityClassification** is a semantic label used to determine handling requirements.

---

### 5.4 Secret Reference

A **SecretReference** is a semantic reference to secret material.

A SecretReference MUST NOT contain the secret itself.

---

### 5.5 Redaction Intent

A **RedactionIntent** is a declarative requirement describing what must be redacted from records.

Redaction intent MUST be target-independent.

---

## 6. Authoring Constraints (Normative)

Authored artifacts MUST:

* never embed SecretMaterial
* represent secret needs as requirements and references
* classify values as sensitive when required

---

## 7. Recordability Constraints (Normative)

Run logs MUST be able to record:

* that a secret reference was required or used (by identity)
* that redaction was applied
* provenance for secret usage decisions (where applicable)

Run logs MUST NOT record SecretMaterial.

---

## 8. Redaction Semantics (Normative)

Redaction intent MUST support:

* redacting values by sensitivity classification
* redacting values by semantic field identity
* redacting entire records where necessary

Redaction MUST be applied consistently to any emitted records.

---

## 9. Target Independence (Normative)

This specification MUST NOT define:

* vault products
* encryption algorithms
* logging exporters

Targets may implement secret storage and redaction using any appropriate mechanism, provided semantic meaning and constraints are preserved.
