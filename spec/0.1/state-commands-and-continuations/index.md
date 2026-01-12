Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat State, Commands, and Continuations Specification

This specification defines Paperhat’s target-independent semantics for **state derivation**, **commands**, **idempotent intent**, **pending intent**, and **continuations**.

This document governs **semantic meaning and constraints only**.
It does **not** define user interface patterns, network protocols, transport mechanisms, URL encoding rules, form handling, or any specific runtime.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define state as a deterministic derived artifact
* define commands as declarative intent that may be accepted or rejected
* define idempotent intent and replay-safe evaluation
* define pending intent as a first-class, target-independent concept
* define continuations as resumable, integrity-protected flow tokens

---

## 2. Scope

This specification governs:

* the semantic model for State, Command, Decision, PendingCommand, and Continuation
* required separation between intent (commands) and facts (events)
* privacy classification for values that may appear in shareable representations
* external input requirements for determinism and reproducibility

This specification does **not** govern:

* how targets represent state (for example, URLs, cookies, client storage)
* how commands are transported (for example, HTTP, message queues)
* how integrity protection is implemented (signatures, encryption)
* how any specific runtime schedules or executes work

---

## 3. Related Specifications

This specification is designed to compose with:

* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)

---

## 4. Core Definitions (Normative)

### 4.1 State

**State** is a deterministic derived artifact.

State is not authoritative mutable storage.

State MUST be derivable from authoritative facts and explicitly bound external inputs.

---

### 4.2 Command

A **Command** is declarative intent.

A Command requests a change.
A Command MAY be accepted or rejected.

Commands MUST NOT be treated as facts.

---

### 4.3 Decision

A **Decision** is the deterministic evaluation result of a Command.

A Decision MUST include:

* acceptance or rejection
* Help/diagnostics (including unmet constraints)
* a canonical reference to produced facts if accepted

---

### 4.4 Pending Command

A **Pending Command** is a Command that has been declared but not yet reconciled with an authority capable of accepting it.

Pending Commands exist to model intermittent connectivity and deferred submission without changing semantics.

---

### 4.5 Continuation

A **Continuation** is a resumable flow token.

A Continuation:

* identifies a flow and a resumable step
* carries a bounded payload with privacy classification (see §8)
* requires integrity protection (see §9)
* has explicit validity constraints (such as expiry)

Continuations MUST NOT require any specific target representation.

---

## 5. Architectural Boundaries (Hard)

### 5.1 Intent vs Fact

Paperhat distinguishes:

* **Intent** (Commands)
* **Facts** (Events)

If a Command is accepted, its acceptance MUST be recorded as one or more Events.

A Command that fails validation MUST NOT produce Events.

---

### 5.2 State as Projection

State SHOULD be defined as a projection over facts.

When events are used as facts, state is derived by event-sourced projection rebuild.

---

## 6. Idempotent Intent (Hard)

Commands MUST support idempotent evaluation.

A Command MUST have an identity sufficient to prevent duplicate application of the same intent.

Given identical:

* Semantics version
* Command identity and content
* relevant authoritative facts
* bound external inputs

Evaluation MUST be deterministic.

If the same Command is evaluated more than once, systems MUST return the same Decision (or an equivalent Decision that references the already-produced facts).

---

## 7. Pending Intent (Normative)

A Pending Command:

* MUST retain the full declarative intent of the Command
* MUST retain a stable identity (idempotency key)
* MUST have a status model (at minimum: pending, submitted, accepted, rejected)

Pending intent is semantic.

Whether a target can submit pending intent is a target capability.

---

## 8. Privacy Classification (Normative)

Values used by State, Command, and Continuation payloads MUST support privacy classification.

At minimum:

* **Public** — may be represented in shareable, user-visible representations
* **Private** — MUST NOT be represented in shareable representations
* **Ephemeral** — MUST NOT be persisted

Privacy classification is semantic meaning.

Targets MUST enforce privacy classification when selecting representations.

---

## 9. Continuations (Normative)

### 9.1 Continuation Payload Modes

A Continuation MAY carry payload in one or more modes:

* **Reference Mode** — payload stored as an authoritative record; token carries only an identifier
* **Envelope Mode** — token carries a small public payload plus references
* **Proof Mode** — token carries proofs required for validation without exposing sensitive values

Targets MAY restrict which modes they support.

---

### 9.2 Continuation Integrity (Hard)

Continuations MUST have integrity protection.

Integrity protection MUST be verifiable by an authority designated by Semantics and bound by Pipeline.

The cryptographic mechanism is a realization detail.

---

### 9.3 Continuation Validity Constraints

Semantics MUST define validity constraints for continuations, including:

* expiry semantics
* required bindings for resume
* replay rules

---

## 10. External Inputs and Determinism (Hard)

Time, actor identity, randomness, locale, and environment are external inputs.

External inputs:

* MUST be modeled explicitly
* MUST have required vs optional semantics
* MUST be bound explicitly during evaluation

Deterministic hashing and replay rules are a responsibility of the Paperhat Pipeline.

---

## 11. Target Independence (Hard)

This specification MUST NOT require:

* URL encoding
* form handling
* scripting
* a specific network protocol
* a specific storage engine

Targets MAY provide realizations that represent intent and state in target-specific forms, as long as semantics and constraints are preserved.
