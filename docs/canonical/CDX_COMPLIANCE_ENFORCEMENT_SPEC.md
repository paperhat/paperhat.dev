# CDX_COMPLIANCE_ENFORCEMENT_SPEC

**Status:** CANONICAL  
**Lock State:** LOCKED  
**Audience:** Orchestrators, Validators, Human Authorities  
**Non-Audience:** Work Packet Executors, Runtime Systems, Application Developers

---

## 1. Purpose

The **CDX Compliance Enforcement Specification** defines the uniform rules for detecting, classifying, and enforcing compliance with CDX constraints across the Paperhat Codex system.

Its purpose is to:

- ensure consistent enforcement of CDX human-first invariants
- prevent fragmented or role-specific interpretations
- provide objective grounds for rejection, failure, or escalation
- preserve semantic integrity without discretionary judgment

This specification governs **enforcement consistency only**, not language semantics.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- defines detection, classification, and enforcement outcomes only

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Definition

A **CDX Compliance Violation** occurs when any artifact, instruction, or output contravenes the constraints of CDX as defined in LOCKED canonical documents.

Compliance is evaluated against **form, expression, and affordance**, not intent.

---

## 4. Enforcement Scope

CDX compliance enforcement applies to:

- Canonical Specifications (prior to locking)
- Work Packets
- Orchestration Decision Records
- Execution Outputs
- Validation and Audit Artifacts

No artifact class is exempt.

---

## 5. Compliance Invariants

The following invariants are mandatory and universal:

- CDX is human-first and non-developer-facing
- No JSON, YAML, or code-shaped constructs
- No imperative configuration metaphors
- No hidden machine affordances
- No reliance on executor inference

Violation of any invariant constitutes non-compliance.

---

## 6. Violation Classes

The following violation classes are **exhaustive**.

No additional classes are permitted.

---

## 7. Structural Violation

### 7.1 Definition

A **Structural Violation** occurs when an artifact’s shape or organization violates required structure.

---

### 7.2 Examples

- Missing required sections
- Extraneous sections
- Incorrect section ordering
- Mixed artifact classes

---

### 7.3 Enforcement Outcome

- Immediate rejection
- No repair or partial acceptance
- Retry permitted only if structure can be corrected without reinterpretation

---

## 8. Expression Violation

### 8.1 Definition

An **Expression Violation** occurs when prohibited language forms or constructs are used.

---

### 8.2 Examples

- JSON, YAML, or pseudo-code
- Step lists or procedural phrasing
- Developer-centric terminology
- Embedded machine affordances

---

### 8.3 Enforcement Outcome

- Immediate rejection
- Mandatory escalation if repeated
- No executor-led correction

---

## 9. Semantic Affordance Violation

### 9.1 Definition

A **Semantic Affordance Violation** occurs when content enables or invites interpretation beyond explicit instruction.

---

### 9.2 Examples

- Implicit assumptions
- “Reasonable”, “sufficient”, or similar terms
- Conditional or speculative phrasing
- Unbounded references

---

### 9.3 Enforcement Outcome

- Rejection
- Escalation if ambiguity cannot be removed mechanically
- No acceptance under any circumstance

---

## 10. Context Leakage Violation

### 10.1 Definition

A **Context Leakage Violation** occurs when an artifact relies on undeclared context.

---

### 10.2 Examples

- “As discussed earlier”
- “Using the same approach”
- References to unstated prior decisions

---

### 10.3 Enforcement Outcome

- Immediate rejection
- Mandatory escalation if blocking progress

---

## 11. Authority Violation

### 11.1 Definition

An **Authority Violation** occurs when an artifact exceeds its permitted authority.

---

### 11.2 Examples

- Outputs asserting normative rules
- Work Packets modifying Canonical meaning
- Audit artifacts making decisions

---

### 11.3 Enforcement Outcome

- Immediate rejection
- Mandatory escalation
- Execution halt until resolved

---

## 12. Enforcement Responsibility

- **Orchestrators** enforce compliance at issuance and acceptance
- **Validators** detect and report violations
- **Human Authorities** resolve escalated compliance conflicts

Executors have no enforcement authority.

---

## 13. Enforcement Consistency Rule

The same violation MUST result in the same enforcement outcome regardless of:

- artifact author
- execution stage
- perceived intent
- convenience or urgency

Discretionary enforcement is prohibited.

---

## 14. Remediation Limits

Remediation is limited to:

- rejection
- retry under unchanged semantics
- escalation

Silent correction, reinterpretation, or normalization is forbidden.

---

## 15. Auditability

All detected violations MUST be:

- recorded
- attributable
- classifiable by violation type
- reviewable without external context

Undocumented enforcement actions are invalid.

---

## 16. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any compliance enforcement behavior inconsistent with this specification is **non-compliant with Paperhat Codex**.

---

**END OF DOCUMENT**
