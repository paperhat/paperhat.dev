Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Contract of Contracts Specification

This specification defines the **meta-level invariants** that all Paperhat Contracts, Specifications, implementations, and authored artifacts MUST obey.

It exists to prevent boundary erosion between:

* languages (Codex, Gloss)
* semantic authority (the Paperhat Kernel)
* deterministic processing (the Paperhat Kernel)
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

## 2.1 Conformance and Implementation Neutrality (Normative)

Paperhat is specified at `paperhat.dev`.

Rules:

1. `paperhat.dev` specifications are the sole normative source of truth for Paperhat semantics.
2. To qualify as a **Paperhat Semantic Authoring System**, an implementation MUST follow the `paperhat.dev` specifications exactly.
3. The Paperhat specifications MUST remain implementation-neutral: they MUST NOT require or assume a particular programming language, runtime, build system, or deployment model.
4. Individual library specifications (for example under `libraries/`) MAY document implementation choices and mapping strategies for a particular library, but such documents are non-authoritative with respect to Paperhat semantics.
5. A library specification MAY reference `paperhat.dev` specifications and MUST defer to them in case of conflict.

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
3. **Kernel** — canonical semantic authority and deterministic compiler/orchestrator (ontology + constraints + assembly rules + default policy; enforces and computes)
4. **Primitives (@paperhat/primitives)** — domain-agnostic FP/type utilities used by implementations

No tier may assume responsibilities owned by another tier.

---

## 5. Authority and Non-Authority (Normative)

### 5.1 Kernel Authority

The Paperhat Kernel is the sole authority for:

* what Concepts exist
* what Traits exist and how they type-check
* how Concepts may be composed
* which structures are semantically ordered
* how authored Works are assembled into publishable structures
* the schema for behavior-as-data (allowed shapes, constraints, typing)
* default presentation policy per target (policy, not implementation)

The Kernel MUST be declarative.
The Kernel MUST NOT require an execution environment.

### 5.2 Kernel Determinism Authority

The Paperhat Kernel is the sole authority for:

* deterministic compilation and orchestration of artifacts
* executing validation as specified by the Kernel
* evaluation/execution of declarative behavior-as-data
* assembly and rendering orchestration for one or more targets
* reproducibility (caching, hashing, dependency tracking)

The Kernel MUST NOT define new meaning.
The Kernel MUST NOT introduce new Concepts, Traits, composition rules, or defaults.

### 5.3 Codex and Gloss Authority

* Codex and Gloss define the authored surface forms.
* Authored artifacts MAY be invalid.

Validity is determined only by Kernel enforcement.

Gloss MUST answer one question only:

> What does this span of text mean?

Gloss MUST NOT embed structure, presentation, control flow, or execution.

### 5.4 Primitives Authority

Primitives MUST remain domain-agnostic.

Primitives MUST NOT define Paperhat meaning, ontology, or policy.

---

## 6. Single Source of Truth (Normative)

For any rule that affects:

* meaning
* structure
* constraints
* ordering
* assembly
* default presentation policy

That rule MUST exist exactly once, in the Kernel.

The Kernel MAY implement evaluation of Kernel-defined rules, but MUST NOT redefine them.

---

## 7. Determinism and Reproducibility (Normative)

Given identical:

* Kernel version and semantic dependencies
* Codex and Gloss sources
* Kernel version and configuration
* bound external inputs (see §9)

Kernel outputs MUST be deterministic and reproducible.

Any dependency on time, randomness, locale, network, or environment MUST be modeled explicitly as an external input with stable identity and hashing rules.

---

## 8. Evaluation Placement (Normative)

Evaluation of behavior-as-data occurs in the Kernel.

To prevent semantic meaning from leaking into the evaluator:

* The Kernel MUST define the allowed computation shapes, typing rules, and constraints for behavior-as-data.
* The Kernel MUST evaluate only what the Kernel allows.
* The Kernel MUST treat evaluation as deterministic transformation with explicitly bound inputs.

The Kernel MUST NOT accept hidden inputs.

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

Whether an input is required or optional MUST be specified by the Kernel.

---

## 10. Default Presentation Policy (Normative)

Default presentation policy:

* MUST live in the Kernel
* MUST be expressed as target-neutral policy
* MUST NOT be replaced by renderer-specific ad hoc decisions

If a target cannot realize a Kernel policy:

* The Kernel MUST produce a typed incompatibility failure, OR
* apply a Kernel-declared fallback rule

---

## 11. Diagnostics (Normative)

The Kernel MUST be able to explain validation and evaluation failures in authored terms:

* Codex/Gloss source locations (where available)
* the semantic identifiers involved
* the Kernel rule violated

The Kernel SHOULD provide human-readable rule names and messages.

---

## 12. Versioning (Normative)

Kernel version changes MAY change meaning and therefore outputs.

Kernel version changes MUST NOT change meaning given identical Kernel inputs, except where explicitly declared as a breaking change to evaluation semantics.

Codex and Gloss versions MUST be pinned for reproducibility.
