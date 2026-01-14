Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Idempotency and De-duplication Specification

This specification defines Paperhat’s target-independent semantics for **idempotency**, **request identity**, and **de-duplication**.

This document governs semantic meaning, constraints, and recordability requirements.
It does **not** define storage engines, hash algorithms, transport headers, databases, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* prevent unintended repeated effects when operations are retried, replayed, or duplicated
* provide a target-independent semantic model for “same request” detection
* define a minimal, auditable, deterministic interface for idempotent execution

---

## 2. Scope

This specification governs:

* idempotency identity and keying
* de-duplication policies and windows
* semantic outcomes for duplicates and replays
* recordability constraints for observing idempotency behavior

This specification does **not** govern:

* retry strategy (see reliability semantics)
* logging backends (see run logs)
* transport-layer protocols
* cryptographic design

---

## 3. Related Specifications

This specification is designed to compose with:

* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Cancellation and Termination](../cancellation-and-termination/)
* [Integrations and Credentials](../integrations-and-credentials/)

---

## 4. Core Invariants (Normative)

1. **Idempotency is semantic, not transport.** Idempotency MUST be defined in authored meaning, not in protocol headers.
2. **No secret material in keys.** Idempotency identities MUST NOT embed secret material.
3. **Deterministic planning.** The Kernel MUST be able to validate the presence and shape of idempotency requirements deterministically.
4. **Target independence.** The Kernel MUST NOT require a particular storage or dedup engine.
5. **Auditable outcomes.** Systems MUST be able to record whether an execution was new, replayed, or rejected.

---

## 5. Definitions (Normative)

### 5.1 Idempotent Operation

An **IdempotentOperation** is an operation whose semantic effects are defined such that applying the same operation more than once results in:

* a single intended effect, and
* repeat applications producing a replayed outcome rather than new effects.

---

### 5.2 Idempotency Identity

An **IdempotencyIdentity** is a stable identity representing “this request is the same request.”

An IdempotencyIdentity MUST be:

* stable for all duplicates of the same request intent
* bounded in size and safe to store
* safe to record (no secret material)

---

### 5.3 De-duplication

**De-duplication** is the act of detecting duplicates of an IdempotencyIdentity and applying a policy-defined outcome.

---

### 5.4 De-duplication Window

A **DeDuplicationWindow** is the interval or scope in which duplicates are considered duplicates.

This window MAY be expressed as:

* time-based
* count-based
* workflow-run scoped
* environment scoped

Targets MAY implement any efficient mechanism consistent with these semantics.

---

## 6. Authoring Requirements (Normative)

Authored artifacts that express operations with externally visible effects SHOULD declare one of:

* **IdempotencyRequired**: the operation MUST be executed idempotently
* **IdempotencyUnsupported**: the operation is not safe to replay and MUST be treated accordingly

If IdempotencyRequired is declared, the authored artifact MUST specify:

* the IdempotencyIdentity source (semantic)
* the DeDuplicationWindow
* the duplicate handling policy (see below)

---

## 7. Duplicate Handling Policy (Normative)

A **DuplicateHandlingPolicy** MUST define what happens when a duplicate is detected.

At minimum, the policy MUST support these outcomes:

* **ReplayResult**: return the prior outcome associated with the identity
* **RejectDuplicate**: reject the duplicate request
* **NoOp**: accept but produce no additional effects

The chosen policy MUST be target-independent.

---

## 8. Recordability (Normative)

Systems MUST be able to record, without revealing secret material:

* the presence of an IdempotencyIdentity (by stable identity)
* whether the operation was executed new, replayed, or rejected
* the DeDuplicationWindow and policy used (by reference)
* correlation to any run log record for the execution

Records MUST NOT contain secret material.

---

## 9. Determinism and External Inputs (Normative)

If the IdempotencyIdentity is derived from runtime data, that derivation MUST be expressed as a deterministic evaluation of explicit inputs.

Time MAY influence de-duplication window evaluation, and MUST be treated as an external input.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* transport headers
* database schemas
* cache engines
* hashing or cryptographic algorithms

Targets may implement idempotency and deduplication via any appropriate mechanism, provided semantic meaning and constraints are preserved.
