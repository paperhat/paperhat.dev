# NAMING_AND_VOCABULARY_SPEC

**Status:** CANONICAL  
**Lock State:** LOCKED  
**Audience:** All Codex Participants  
**Non-Audience:** Runtime engines, application developers

---

## 1. Purpose

The **Naming and Vocabulary Specification** defines the **authoritative terminology** permitted within the Sitebender Codex corpus.

Its purpose is to:

- prevent semantic drift through synonym creep
- ensure consistent human-first expression
- eliminate ambiguous or developer-centric language
- preserve long-term stability of meaning

Vocabulary discipline is a governance mechanism.

---

## 2. Normative Position

This specification:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- constrains terminology, naming, and usage only

In the event of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Vocabulary Authority Rule

Only terms defined or used in LOCKED canonical documents are permitted as **authoritative vocabulary**.

Unlisted or alternative terms MUST NOT be substituted where an authoritative term exists.

---

## 4. Canonical Terms

The following terms are **canonical** and MUST be used exactly as written.

Near-synonyms are prohibited.

---

### 4.1 Roles

- **Human Authority**
- **Orchestrator**
- **Work Packet Executor**
- **Validator**
- **Auditor**
- **Observer**

Pluralization MUST preserve the full term (e.g., _Human Authorities_, not _Authorities_).

---

### 4.2 Artifacts

- **Canonical Specification**
- **Contract**
- **Specification**
- **Work Packet**
- **Execution Output**
- **Validation Artifact**
- **Audit Artifact**
- **Governance Artifact**
- **Orchestration Decision Record**

Do not abbreviate artifact names in canonical text.

---

### 4.3 States

- **Draft**
- **Canonical**
- **Locked**
- **Superseded**

No alternative state names are permitted.

---

### 4.4 Actions

- **Issue**
- **Execute**
- **Validate**
- **Accept**
- **Reject**
- **Retry**
- **Escalate**
- **Resolve**
- **Halt**
- **Terminate**
- **Supersede**
- **Lock**

Action verbs MUST be used in their canonical form.

---

### 4.5 Qualifiers

- **Explicit**
- **Implicit**
- **Authoritative**
- **Immutable**
- **Reviewable**
- **Auditable**
- **Deterministic**
- **Human-first**

Avoid introducing new qualifiers where a canonical one applies.

---

## 5. Prohibited Synonyms

The following substitutions are explicitly forbidden:

- _Task_, _Job_, _Ticket_ → **Work Packet**
- _Agent_, _Worker_, _Bot_ → role-specific canonical term
- _Approve_ → **Accept**
- _Decline_ → **Reject**
- _Fix_, _Correct_ → **Reject** or **Retry**
- _Workflow_ → **Orchestration**
- _Config_, _Configuration_ → prohibited
- _Schema_, _DSL_, _API_ → prohibited in CDX context

---

## 6. Capitalization Rules

- Canonical terms MUST be capitalized when used as defined terms
- Lowercase usage is permitted only for generic, non-authoritative reference
- Inconsistent capitalization constitutes a compliance violation

---

## 7. Singular and Plural Rules

- Use singular when referring to a specific role or artifact
- Use plural only when referring to multiple concrete instances
- Avoid collective shorthand (e.g., _the Orchestration_)

---

## 8. Abbreviation Rules

- Abbreviations are prohibited in Canonical Specifications
- Initialisms are prohibited unless explicitly defined in a LOCKED document
- Shortened forms (e.g., _packet_, _record_) are prohibited when ambiguity exists

---

## 9. Developer-Centric Vocabulary Prohibition

The following categories of language MUST NOT appear in canonical text:

- implementation-oriented terms
- runtime or execution engine references
- programming language constructs
- data structure names
- algorithmic terminology

Violation constitutes a CDX compliance failure.

---

## 10. Ambiguity Prevention Rule

Where two terms could plausibly apply, the more **specific canonical term** MUST be used.

Preference for precision overrides brevity.

---

## 11. Evolution Constraint

Vocabulary MAY evolve only through:

- explicit introduction in a new Canonical Specification
- Human Authority approval
- locking under governance rules

Silent vocabulary expansion is prohibited.

---

## 12. Enforcement

- Orchestrators MUST reject artifacts using prohibited or substituted terms
- Validators MUST flag vocabulary violations
- Human Authorities resolve escalations involving terminology disputes

No role may waive vocabulary compliance.

---

## 13. Auditability

All terminology decisions MUST be:

- traceable to this specification
- reviewable without contextual inference

Undocumented vocabulary deviations are invalid.

---

## 14. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any artifact using non-compliant terminology is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
