Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Cancellation and Termination Specification

This specification defines Paperhat’s target-independent semantics for **cancellation**, **termination**, and **stopping** of workflow runs and steps.

This document governs semantic meaning and planning interfaces.
It does **not** define concrete runtime interruption mechanisms, process signals, queue semantics, or vendor systems.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* allow workflows and operators to request cancellation in a controlled, auditable way
* define consistent meanings for cancellation versus failure
* ensure termination behavior composes with reliability, run logs, and coordination
* prevent target/runtime details from leaking into authored artifacts

---

## 2. Scope

This specification governs:

* cancellation requests
* cancellation eligibility and authorization requirements
* cancellation propagation rules (run, step, subtree)
* termination outcomes
* graceful stop versus hard stop semantics (as declarative intent)
* recordability requirements

This specification does **not** govern:

* concrete thread/task interruption
* OS signals
* queue visibility timeouts
* vendor-specific cancellation APIs

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Concurrency and Parallelism](../concurrency-and-parallelism/)
* [Approvals and Human-in-the-Loop](../approvals-and-human-in-the-loop/)

---

## 4. Core Invariants (Hard)

1. **Cancellation is data.** Cancellation intent MUST be representable as declarative input.
2. **Auditability.** It MUST be possible to explain who requested cancellation, when, and why.
3. **Deterministic planning.** Pipeline MUST be able to plan cancellation handling deterministically.
4. **No implicit interruption model.** Semantics MUST NOT assume a particular runtime interruption capability.

---

## 5. Definitions (Normative)

### 5.1 Cancellation Request

A **CancellationRequest** is an explicit request to stop a run or a portion of a run.

A CancellationRequest MUST include:

* request identity
* target scope (run, step, subtree)
* requester identity reference
* request time (as an execution fact)
* optional reason (as permitted data)

---

### 5.2 Cancellation Scope

A **CancellationScope** identifies what is being cancelled.

At minimum:

* **RunScope** — cancel the entire run
* **StepScope** — cancel a specific step
* **SubtreeScope** — cancel a branch/subgraph rooted at a step

---

### 5.3 Termination

**Termination** is the semantic end of evaluation for a run or step.

Termination may result from:

* successful completion
* failure
* cancellation

---

### 5.4 Cancellation Outcome

A **CancellationOutcome** is the structured result of applying cancellation.

Outcomes MUST support:

* **Cancelled** — evaluation ended due to cancellation
* **CancellationRejected** — cancellation could not be applied due to policy
* **CancellationDeferred** — cancellation accepted but not yet effective (pending)

---

### 5.5 Graceful Stop vs Hard Stop

A cancellation request MAY declare a preference for **graceful stop** versus **hard stop**.

These are semantic intents only:

* graceful stop means “stop at safe boundaries”
* hard stop means “stop as soon as allowed by policy”

Targets choose the realization mechanism.

---

## 6. Authorization and Eligibility (Normative)

Cancellation MUST support declaring eligibility requirements in terms of semantic authorization constructs.

Cancellation requests MAY be rejected by policy.

---

## 7. Propagation Rules (Normative)

A cancellation request MUST define propagation rules.

Propagation MUST be expressible as declarative policy, including:

* whether in-progress parallel work should be allowed to complete
* whether pending approvals should be invalidated
* whether downstream steps are skipped

---

## 8. Interaction With Reliability (Normative)

Cancellation is not a retryable failure.

Reliability policy MUST NOT cause cancelled work to be retried.

If cancellation is deferred, any waiting behavior MUST be modeled using pending semantics and explicit time inputs.

---

## 9. Interaction With Coordination (Normative)

Cancellation MUST define how joins/barriers/locks behave when upstream work is cancelled.

A plan MUST be able to explain:

* which dependencies were skipped
* which joins were satisfied or failed due to cancellation

---

## 10. Run Log Requirements (Normative)

Run logs MUST be able to record:

* the CancellationRequest
* requester identity reference
* timestamps as execution facts
* scope and propagation decisions
* resulting CancellationOutcome

Records MUST NOT require embedding secrets.

---

## 11. Target Independence (Hard)

This specification MUST NOT define:

* specific interruption APIs
* signal handling
* queue cancel semantics

Targets may implement cancellation using any appropriate mechanism, provided semantic meaning, auditability, and recordability requirements are preserved.
