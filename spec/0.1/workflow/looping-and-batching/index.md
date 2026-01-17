Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Looping and Batching Specification

This specification defines Paperhat’s target-independent semantics for **looping**, **iteration**, and **batch processing** within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete runtime schedulers, worker models, collection libraries, or expression language syntax.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* express iteration as declarative workflow intent
* support deterministic planning for loops and batches
* define bounded execution semantics to avoid runaway loops
* keep iteration semantics target-independent and auditable

---

## 2. Scope

This specification governs:

* loop constructs (for-each style iteration)
* batching semantics (chunking collections)
* loop termination conditions (bounded)
* per-item and per-batch step evaluation
* aggregation of outputs
* failure handling and recordability expectations in iterative contexts

This specification does **not** govern:

* concrete collection APIs
* concrete expression syntax
* concrete runtime scheduling implementations

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Data Transformation and Mapping](../data-transformation-and-mapping/)
* [Conditions and Branching](../conditions-and-branching/)
* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Looping is declarative.** Iteration MUST be representable as data.
2. **Boundedness is explicit.** Unbounded loops MUST NOT be representable.
3. **Deterministic planning.** The Kernel MUST be able to plan loop structure deterministically.
4. **Target independence.** The Kernel MUST NOT assume specific runtime collection mechanics.
5. **Auditability.** Per-item/per-batch attempts MUST be recordable.

---

## 5. Definitions (Normative)

### 5.1 Iterable Source

An **IterableSource** is a declarative source of a collection to iterate.

An IterableSource MAY refer to:

* a step output (collection)
* a state projection (collection)
* an event payload (collection)
* a literal collection

---

### 5.2 Loop

A **Loop** is a declarative construct that evaluates a body for each element in an IterableSource.

A Loop MUST declare:

* the iterable source
* an item binding identity
* a maximum item count (or other explicit bound)

---

### 5.3 Batch

A **Batch** is a declarative grouping of items into chunks.

Batching MUST declare:

* batch size or equivalent declarative batching parameters
* behavior for remainder items

---

### 5.4 Aggregation

An **Aggregation** describes how to produce an output from per-item or per-batch outputs.

Aggregation MUST be declarative and MUST NOT embed target code.

---

## 6. Boundedness and Termination (Normative)

Loop semantics MUST require explicit bounds.

A loop MAY declare termination conditions, but such conditions MUST be bounded and MUST NOT create implicit unbounded evaluation.

---

## 7. Concurrency Interaction (Normative)

Iteration MAY permit concurrency across items or batches, subject to:

* declared concurrency limits
* ordering constraints
* mutual exclusion constraints
* resource/rate limits

---

## 8. Reliability Interaction (Normative)

Reliability policy MUST be applicable at:

* per-item attempt level
* per-batch attempt level

The plan MUST be able to explain:

* which item/batch failed
* what retry policy applied
* what terminal outcome occurred

---

## 9. Recordability (Normative)

Run logs MUST be able to record:

* loop identity
* item index and/or item identity reference
* batch identity (when applicable)
* per-item/per-batch attempt outcomes
* aggregation outcome

Records MUST NOT require embedding secrets.

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* concrete iteration APIs
* concrete batching algorithms as code
* a concrete expression syntax

Targets may realize loops and batches with any appropriate mechanism, provided semantic meaning, boundedness, and recordability requirements are preserved.
