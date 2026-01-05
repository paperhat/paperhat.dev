# WORK_PACKET_SPEC

**Status:** CANONICAL
**Lock State:** LOCKED
**Audience:** Orchestrator LLMs, Human Reviewers
**Non-Audience:** Runtime engines, application developers

---

## 1. Purpose

A **Work Packet** is the smallest _authoritative unit of execution_ delegated to a less-capable LLM within the Sitebender Codex system.

Its purpose is to:

- decompose complex human-authored intent into **bounded, verifiable work**
- ensure execution **without interpretation, invention, or drift**
- preserve **human-first CDX semantics** end-to-end
- enable deterministic orchestration, review, and retry

A Work Packet is **not** a plan, a task list, or a design document.
It is an **execution contract**.

---

## 2. Normative Position

This specification:

- is subordinate to all LOCKED canonical documents
- introduces **no new semantics**
- defines **no implementation strategy**
- constrains _shape, authority, and responsibility only_

If a conflict exists between this document and any LOCKED contract,
**this document yields without exception**.

---

## 3. Definition

A **Work Packet** is a self-contained, execution-ready instruction set that:

1. has a **single, explicit objective**
2. operates within **fixed semantic bounds**
3. produces **auditable artifacts**
4. can be **executed by a less-capable LLM without interpretation**
5. can be **accepted or rejected** without contextual debate

---

## 4. Non-Goals

A Work Packet MUST NOT:

- reinterpret CDX language rules
- infer missing intent
- resolve ambiguities
- introduce new vocabulary
- propose design alternatives
- perform architectural reasoning
- coordinate with other packets implicitly

Reasoning, synthesis, and judgment remain the responsibility of the **orchestrator** or **human authority**, never the packet executor.

---

## 5. Authority Model

### 5.1 Source of Authority

A Work Packet derives authority solely from:

- explicit instruction contained within the packet
- referenced LOCKED canonical documents

It has **no discretionary authority**.

---

### 5.2 Executor Role

The executor LLM:

- executes _exactly_ what is specified
- does not optimize, simplify, or reframe
- does not ask clarifying questions
- does not “fix” perceived problems
- does not extrapolate beyond scope

Failure to comply is treated as **execution failure**, not partial success.

---

## 6. Packet Boundaries

Every Work Packet MUST explicitly define:

- **Scope** — what is included
- **Exclusions** — what is out of scope
- **Inputs** — authoritative materials
- **Outputs** — concrete deliverables
- **Completion Criteria** — objective acceptance rules

Nothing outside these boundaries may be touched.

---

## 7. Determinism Requirements

A valid Work Packet MUST be:

- executable in isolation
- order-independent unless explicitly sequenced
- retryable without semantic drift
- idempotent with respect to meaning

Different executions MAY differ in wording, but MUST NOT differ in substance.

---

## 8. Human-First Constraint

All Work Packets MUST respect the following invariant:

> CDX is a human-first language for non-developers.

Therefore:

- no JSON, YAML, or code-shaped structures
- no imperative configuration metaphors
- no developer-centric abstractions
- no hidden machine affordances

If a packet would require such constructs to execute, the packet is **invalid**.

---

## 9. Artifact Integrity

Outputs produced by a Work Packet:

- MUST be clearly attributable to that packet
- MUST be reviewable without external context
- MUST NOT modify LOCKED documents
- MAY propose changes ONLY if explicitly instructed to do so

Silence, omission, or partial output constitutes failure.

---

## 10. Validation & Rejection

A Work Packet is evaluated strictly on:

- adherence to scope
- adherence to referenced contracts
- completeness of required outputs
- absence of forbidden behavior

There is no concept of “mostly correct.”

---

## 11. Composition Rules

- Work Packets do **not** coordinate with each other
- dependencies MUST be declared externally
- no packet may assume prior execution state
- no packet may mutate shared context implicitly

Composition is an orchestration concern, not a packet concern.

---

## 12. Versioning & Stability

Once issued:

- a Work Packet is immutable
- corrections require issuance of a **new packet**
- supersession must be explicit

Historical packets remain valid artifacts and MUST NOT be retroactively altered.

---

## 13. Failure Semantics

Failure modes are limited to:

- **Non-Execution** — task not performed
- **Out-of-Scope Execution** — unauthorized work
- **Semantic Drift** — meaning altered
- **Artifact Incompleteness** — missing deliverables

There is no partial credit and no silent recovery.

---

## 14. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any system component, human or automated, that violates this specification is **non-compliant with Sitebender Codex**.

---

**END OF DOCUMENT**
