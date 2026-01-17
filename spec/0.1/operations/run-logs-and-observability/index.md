Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Run Logs and Observability Specification

This specification defines Paperhat’s target-independent semantics for **run logs** and **observability**.

This document governs **meaning and required records**.
It does **not** define log transport, storage technology, UI, exporters, or protocols.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* ensure executions are explainable, auditable, and debuggable
* support deterministic planning while allowing non-deterministic execution facts to be recorded explicitly
* enable reliable automation by making outcomes and attempts observable

---

## 2. Scope

This specification governs:

* run identity and correlation
* step attempt recording
* structured outcomes and failures
* provenance of external actions and integrations
* minimum record requirements for retries, timeouts, and dead-letter outcomes

This specification does **not** govern:

* logging frameworks
* observability backends
* dashboards
* metrics protocols
* tracing protocols

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Integrations and Credentials](../integrations-and-credentials/)
* [Eventing and Event Sourcing](../eventing-and-event-sourcing/)

---

## 4. Core Invariants (Normative)

1. **Runs are identifiable.** Each run MUST have a stable run identifier.
2. **Attempts are observable.** Each step attempt MUST be recordable.
3. **Outcomes are typed.** Success and failure MUST be representable as typed outcomes.
4. **External facts are explicit.** Any non-deterministic execution fact (including time) MUST be recorded as explicit run data.
5. **No protocol leakage.** Authored artifacts MUST NOT embed transport/exporter details.

---

## 5. Definitions (Normative)

### 5.1 Run

A **Run** is an execution instance of a workflow (or an equivalent executable plan).

A Run MUST have:

* a RunId
* a reference to the artifact identity being executed (for example, workflow identity + version)
* a start record
* an end record (including terminal status)

---

### 5.2 Run Correlation

Runs MUST be correlatable.

Correlation MAY include:

* parent run identifiers
* triggering event identifiers
* triggering command identifiers
* a stable correlation identifier

---

### 5.3 Step Attempt

A **StepAttempt** is a single attempt to evaluate a step.

A StepAttempt MUST have:

* a stable StepAttemptId
* a step identity (stable within the workflow)
* an attempt index
* an outcome record

---

### 5.4 Outcome

An **Outcome** is the structured result of a step attempt.

Outcome MUST support:

* success
* failure (typed failure kind)
* pending (explicitly indicating that evaluation is paused and requires future input)

---

### 5.5 Execution Facts

**ExecutionFacts** are recorded observations about what happened during execution.

ExecutionFacts MAY include:

* timestamps
* durations
* external action fulfillment evidence
* integration invocation identifiers

ExecutionFacts MUST be represented as explicit data and MUST NOT be required for deterministic planning.

---

## 6. Minimum Required Records (Normative)

### 6.1 Run Start Record

A run start record MUST include:

* RunId
* artifact identity
* start time (as an execution fact)
* trigger reference (when applicable)

---

### 6.2 Run End Record

A run end record MUST include:

* RunId
* terminal status
* end time (as an execution fact)
* a reference to terminal outcome(s)

---

### 6.3 Step Attempt Record

A step attempt record MUST include:

* StepAttemptId
* step identity
* attempt index
* start time (as an execution fact)
* end time (as an execution fact) or an explicit pending marker
* typed outcome

---

## 7. Reliability-Related Records (Normative)

When reliability policy causes retries, timeouts, compensation, or dead-letter outcomes, the run log MUST be able to record:

* the policy identity that applied
* the reason a retry was eligible or ineligible
* the number of attempts taken
* the declared backoff parameters used
* the terminal classification (permanent failure, dead-letter, compensated, etc.)

---

## 8. Provenance Requirements (Normative)

When a step interacts with an integration or external action:

* the run log MUST be able to record the semantic identity of the integration operation
* the run log MUST be able to record the credential requirement identity (but MUST NOT record secret material)
* the run log MUST be able to record fulfillment evidence for external actions

---

## 9. Target Independence (Normative)

This specification MUST NOT define:

* specific log formats
* specific exporters or protocols
* specific storage engines

Targets may realize run logs with any appropriate mechanism, provided the semantic requirements above can be satisfied.
