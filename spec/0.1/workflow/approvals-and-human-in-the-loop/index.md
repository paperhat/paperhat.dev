Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Approvals and Human-in-the-Loop Specification

This specification defines Paperhat’s target-independent semantics for **approvals** and **human-in-the-loop** decisions within workflows.

This document governs semantic meaning and planning interfaces.
It does **not** define UI flows, notification channels, protocols, vendor systems, or identity provider details.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* model approvals and decisions as declarative, auditable steps
* support pausing and resuming workflows based on explicit decision inputs
* define how approval requirements compose with authorization semantics
* prevent target details from leaking into authored content

---

## 2. Scope

This specification governs:

* approval gates and review tasks
* decision requests and decision responses
* evidence, provenance, and audit record requirements
* deadlines and escalation semantics (as declarative data)
* interaction with reliability and run logs

This specification does **not** govern:

* UI composition
* email, SMS, chat, or ticketing protocols
* vendor-specific approval systems

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Authentication and Authorization](../authentication-and-authorization/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)

---

## 4. Core Invariants (Normative)

1. **Approvals are data.** Approval requirements MUST be representable as declarative artifacts.
2. **Decisions are explicit inputs.** A workflow MUST NOT assume a decision without an explicit decision response.
3. **Auditability.** It MUST be possible to record who decided, what they decided, and what evidence was considered.
4. **Target independence.** Authored approval semantics MUST NOT encode UI or protocol details.
5. **Deterministic planning.** The Kernel MUST be able to plan approval gates deterministically.

---

## 5. Definitions (Normative)

### 5.1 Approval Gate

An **ApprovalGate** is a workflow step that requires one or more human decisions before downstream steps may proceed.

An ApprovalGate evaluation MAY produce:

* **Approved** (success-like outcome)
* **Rejected** (failure-like outcome)
* **TimedOut** (timeout outcome)
* **Pending** (explicit pause waiting for decision input)

---

### 5.2 Review Task

A **ReviewTask** is a declared request for review, producing a decision response.

A ReviewTask MUST declare:

* what is being reviewed (semantic subject)
* what decision options exist
* what evidence is required or provided

---

### 5.3 Decision Request

A **DecisionRequest** is the declared intent to obtain a decision.

A DecisionRequest MUST include:

* a decision kind identity
* the allowed outcomes
* required decision metadata (if any)

A DecisionRequest MUST NOT include target details.

---

### 5.4 Decision Response

A **DecisionResponse** is an explicit input provided later.

A DecisionResponse MUST include:

* correlation to the DecisionRequest
* the chosen outcome
* the decider identity reference
* decision time (as an execution fact)

---

### 5.5 Evidence

**Evidence** is declared and/or provided material relevant to a decision.

Evidence MAY include:

* references to run logs
* references to artifacts
* references to state projections

Evidence MUST NOT require embedding secrets.

---

## 6. Authorization and Eligibility (Normative)

Approval gates MUST support declaring who is eligible to decide.

Eligibility MUST be expressed in terms of semantic authorization constructs (for example, roles, capabilities, or policy identities).

This specification does not define the identity provider; it defines the semantic requirement.

---

## 7. Deadlines and Escalation (Normative)

Decision requests MAY declare:

* a deadline
* an escalation policy

Deadline evaluation depends on time, which is an explicit execution fact.

Escalation policy MUST be declarative and MUST NOT embed notification or protocol details.

---

## 8. Interaction With Workflow Pending (Normative)

An approval gate MUST be able to place a workflow into a **Pending** state.

Pending MUST be represented explicitly and MUST be resumable when a DecisionResponse arrives.

---

## 9. Interaction With Reliability (Normative)

Reliability policy MAY apply to:

* validation of decision responses
* timeouts for waiting periods

Reliability policy MUST NOT imply that human decisions are retried.

---

## 10. Run Log Requirements (Normative)

Run logs MUST be able to record:

* the DecisionRequest identity
* eligibility requirements
* evidence references
* the DecisionResponse
* decider identity reference
* timestamps as execution facts

---

## 11. Distinction From External Actions (Normative)

Approvals and decisions are **decision inputs**.

A decision request MUST NOT be used to smuggle protocol-specific work instructions.

If a workflow requires an external action to be performed, it MUST use the workflow external action semantics.

---

## 12. Target Independence (Normative)

This specification MUST NOT define:

* UI components
* notification channels
* ticketing system mechanics
* identity provider protocols

Targets may realize approvals using any appropriate mechanism, provided semantic meaning, auditability, and recordability are preserved.
