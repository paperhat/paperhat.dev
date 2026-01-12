Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Contract of Contracts Specification

This specification defines the **meta-level invariants** that all Paperhat Contracts, Specifications, implementations, and authored artifacts MUST obey.

It exists to prevent boundary erosion between:

* languages (Codex, Gloss)
* semantic authority (the Semantics library)
* deterministic processing (the Pipeline library)
* target realization (renderers/adapters)
* non-domain foundational utilities (the Primitives library)

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* establish the canonical **authority model** for Paperhat
* define non-negotiable **tier boundaries** and **responsibility ownership**
* guarantee **determinism** and **reproducibility** of derived outputs
* prevent meaning, policy, and execution concerns from contaminating each other

---

## 2. Scope

This specification governs:

* how Paperhat documents relate to each other (authority, precedence, boundaries)
* the allowed responsibilities of major Paperhat libraries
* determinism requirements for compilation, evaluation, assembly, and rendering
* the rules for modeling and binding external inputs

This specification does **not** govern:

* any specific software implementation
* any specific target runtime, UI system, or delivery mechanism
* product governance, licensing, or deployment practices

---

## 3. Precedence (Normative)

### 3.1 System Contract Precedence

The Paperhat System Contract remains the highest-authority system document.

If any conflict exists between this specification and the Paperhat System Contract, the System Contract takes precedence.

### 3.2 Contract vs Spec

* A **Contract** defines exclusive ownership and invariants.
* A **Specification** defines canonical formats and authoring/processing semantics.

In case of conflict:

1. System Contract
2. Relevant library Contract(s)
3. This Contract of Contracts specification
4. Other specifications
5. Work packets, demos, notes, and examples

---

## 4. Tier Model (Normative)

Paperhat is defined as a strict tiered system:

1. **Codex** — semantic authoring language for structured truth and intent
2. **Gloss** — inline span-binding language for meaning annotation only
3. **Semantics (@paperhat/semantics)** — canonical semantic authority (ontology + constraints + assembly rules + default policy)
4. **Pipeline (@paperhat/pipeline)** — deterministic compiler/orchestrator (enforces and computes)
5. **Primitives (@paperhat/primitives)** — domain-agnostic FP/type utilities used by implementations

No tier may assume responsibilities owned by another tier.

---

## 5. Authority and Non-Authority (Hard)

### 5.1 Semantics Authority

The Semantics library is the sole authority for:

* what Concepts exist
* what Traits exist and how they type-check
* how Concepts may be composed
* which structures are semantically ordered
* how authored Works are assembled into publishable structures
* the schema for behavior-as-data (allowed shapes, constraints, typing)
* default presentation policy per target (policy, not implementation)

Semantics MUST be declarative.
Semantics MUST NOT require an execution environment.

### 5.2 Pipeline Authority

The Pipeline library is the sole authority for:

* deterministic compilation and orchestration of artifacts
* executing validation as specified by Semantics
* evaluation/execution of declarative behavior-as-data
* assembly and rendering orchestration for one or more targets
* reproducibility (caching, hashing, dependency tracking)

Pipeline MUST NOT define new meaning.
Pipeline MUST NOT introduce new Concepts, Traits, composition rules, or defaults.

### 5.3 Codex and Gloss Authority

* Codex and Gloss define the authored surface forms.
* Authored artifacts MAY be invalid.

Validity is determined only by Semantics + Pipeline enforcement.

Gloss MUST answer one question only:

> What does this span of text mean?

Gloss MUST NOT embed structure, presentation, control flow, or execution.

### 5.4 Primitives Authority

Primitives MUST remain domain-agnostic.

Primitives MUST NOT define Paperhat meaning, ontology, or policy.

---

## 6. Single Source of Truth (Hard)

For any rule that affects:

* meaning
* structure
* constraints
* ordering
* assembly
* default presentation policy

That rule MUST exist exactly once, in Semantics.

Pipeline MAY implement evaluation of Semantics-defined rules, but MUST NOT redefine them.

---

## 7. Determinism and Reproducibility (Hard)

Given identical:

* Semantics version and semantic dependencies
* Codex and Gloss sources
* pipeline version and configuration
* bound external inputs (see §9)

Pipeline outputs MUST be deterministic and reproducible.

Any dependency on time, randomness, locale, network, or environment MUST be modeled explicitly as an external input with stable identity and hashing rules.

---

## 8. Evaluation Placement (Normative)

Evaluation of behavior-as-data occurs in Pipeline.

To prevent semantic meaning from leaking into the evaluator:

* Semantics MUST define the allowed computation shapes, typing rules, and constraints for behavior-as-data.
* Pipeline MUST evaluate only what Semantics allows.
* Pipeline MUST treat evaluation as deterministic transformation with explicitly bound inputs.

Pipeline MUST NOT accept hidden inputs.

---

## 9. External Inputs (Normative)

External inputs MUST be modeled explicitly.

An External Input MUST have:

* stable identifier
* schema/type
* provenance
* optionality rule (required vs optional)
* validation rules
* defaulting/absence semantics (if optional)
* hashing rules for reproducibility

Whether an input is required or optional MUST be specified by Semantics, not inferred by Pipeline.

---

## 10. Default Presentation Policy (Normative)

Default presentation policy:

* MUST live in Semantics
* MUST be expressed as target-neutral policy
* MUST NOT be replaced by renderer-specific ad hoc decisions

If a target cannot realize a Semantics policy:

* Pipeline MUST produce a typed incompatibility failure, OR
* apply a Semantics-declared fallback rule

---

## 11. Diagnostics (Normative)

Pipeline MUST be able to explain validation and evaluation failures in authored terms:

* Codex/Gloss source locations (where available)
* the semantic identifiers involved
* the Semantics rule violated

Semantics SHOULD provide human-readable rule names and messages.

---

## 12. Versioning (Normative)

Semantics version changes MAY change meaning and therefore outputs.

Pipeline version changes MUST NOT change meaning given identical Semantics and inputs, except where explicitly declared as a breaking change to evaluation semantics.

Codex and Gloss versions MUST be pinned for reproducibility.
