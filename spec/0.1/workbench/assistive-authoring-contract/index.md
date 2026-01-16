Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Assistive Authoring Contract

---

## 1. Purpose

This specification defines the **assistive authoring capabilities** of the Paperhat Workbench.

Assistive authoring exists to:

* guide users through the authoring process
* ask clarifying questions
* surface ambiguities or inconsistencies
* suggest approaches to expressing intent

Assistive authoring is **supportive**, not authoritative.

This document is **Normative**.

---

## 2. Scope

This specification governs:

* AI-guided assistance
* interactive guidance systems
* suggestion and proposal mechanisms

This specification does **not** define:

* semantic rules
* ontology design
* mutation behavior
* implementation technology
* model selection or hosting

---

## 3. Assistive Role (Normative)

Assistive systems are **advisors**, not authors.

Assistive systems MAY:

* ask questions to clarify intent
* explain schema expectations
* point out inconsistencies or gaps
* suggest structures or approaches
* propose candidate content or structure

Assistive systems MUST NOT:

* mutate authored content directly
* apply changes automatically
* bypass review or refusal semantics
* invent meaning without user confirmation

---

## 4. Canonical State Discipline (Normative)

Assistive systems MUST operate over the **canonical authored state**.

Assistive systems:

* observe the same state as all other projections
* do not maintain independent authored representations
* do not create parallel sources of truth

All assistive output MUST be expressed as proposals against the canonical state.

---

## 5. Proposal-Only Semantics (Normative)

All assistive output MUST be expressed as **proposed Patches**.

Rules:

* proposals MUST be deterministic given identical inputs
* proposals MUST be reviewable prior to application
* proposals MUST be rejectable without side effects
* proposals MUST NOT be auto-applied

User approval is required for all mutation.

---

## 6. Interaction Discipline (Normative)

Assistive interaction MUST be explicit and transparent.

The system MUST:

* clearly distinguish between system guidance and authored content
* clearly mark proposed changes as proposals
* preserve user control at all times

Assistive interaction MUST NOT:

* obscure authored content
* overwrite user work
* introduce hidden state

---

## 7. Diagnostic Integration (Normative)

Assistive systems MUST use Diagnostics to communicate issues.

Assistive Diagnostics MUST:

* conform to the Diagnostic Messaging and Help Contract
* preserve non-blaming tone
* avoid imperative or scolding language

Assistive systems MAY reference existing Diagnostics to guide discussion.

---

## 8. Determinism and Governance (Normative)

Assistive behavior MUST be governed.

Rules:

* assistive systems MUST operate within explicit configuration
* assistive systems MUST respect version and compatibility boundaries
* assistive systems MUST NOT introduce heuristic behavior that affects authored meaning

If assistive behavior cannot be specified, it MUST be refused.

---

## 9. Privacy and Boundaries (Normative)

Assistive systems MUST respect workspace boundaries.

They MUST NOT:

* access external network resources implicitly
* leak authored content without explicit authorization
* retain state beyond explicit session scope

---

## 10. Extensibility (Normative)

New assistive capabilities MAY be added only if:

* proposal-only semantics are preserved
* mutation boundaries remain intact
* determinism and governance are maintained
* behavior is specified normatively

---

## 11. Reality Rule (Normative)

This specification defines assistive authoring **as it is**.

There is no legacy assistive behavior.
There are no autonomous agents.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
