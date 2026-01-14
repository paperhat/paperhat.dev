Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Workflow Testing and Simulation Specification

This specification defines Paperhat’s target-independent semantics for **workflow testing** and **simulation**.

This document governs semantic meaning and planning interfaces.
It does **not** define a concrete test runner implementation, CI system integration, transport mocks, or vendor tooling.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* enable workflows to be tested deterministically
* allow simulation of external inputs and outcomes without target-specific mocks
* define expectations for assertions about plans, steps, and outcomes
* provide auditable artifacts for “what was tested” and “what passed”

---

## 2. Scope

This specification governs:

* test case definitions
* simulation inputs (events, state projections, explicit time facts)
* stubbing and expected outputs (as declarative data)
* assertions about plans and outcomes
* handling of nondeterministic execution facts via explicit fixtures

This specification does **not** govern:

* runtime execution engines
* real integrations
* network mocking
* CI pipelines

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Reliability and Failure Semantics](../reliability-and-failure-semantics/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Workflow Versioning and Compatibility](../workflow-versioning-and-compatibility/)

---

## 4. Core Invariants (Normative)

1. **Tests are artifacts.** Test definitions MUST be representable as declarative artifacts.
2. **Inputs are explicit.** Any external input required for evaluation MUST be provided as explicit test fixtures.
3. **Deterministic evaluation.** Given identical artifacts and fixtures, Kernel MUST produce the same planned results.
4. **No target coupling.** Tests MUST NOT depend on target-specific mocks or protocol details.

---

## 5. Definitions (Normative)

### 5.1 Test Case

A **TestCase** is a declarative artifact that specifies:

* the workflow identity/version under test
* test fixtures
* assertions

---

### 5.2 Fixture

A **Fixture** is explicit input data provided for evaluation.

Fixtures MAY include:

* events
* state projections
* explicit time facts
* declared integration outcomes (stubbed)

Fixtures MUST NOT include secrets.

---

### 5.3 Stubbed Outcome

A **StubbedOutcome** is a declared expected result for an integration call or external action fulfillment.

Stubbed outcomes MUST be target-independent and MUST NOT embed protocol details.

---

### 5.4 Assertion

An **Assertion** is a declarative expectation about a plan or an outcome.

Assertions MAY include:

* expected plan structure (steps, dependencies, barriers)
* expected typed outcomes for steps
* expected failure classifications
* expected policy application (reliability, limits)

---

## 6. Plan Assertions (Normative)

Tests SHOULD be able to assert properties of the deterministic plan, including:

* presence/absence of steps
* dependency ordering
* declared retry/backoff policies
* declared concurrency constraints

---

## 7. Outcome Assertions (Normative)

Tests SHOULD be able to assert typed outcomes, including:

* success
* failure (typed failure kind)
* pending
* cancelled

---

## 8. Time in Simulation (Normative)

If a test depends on time (for example, time windows or backoff), the test MUST supply explicit time facts.

The system MUST NOT read wall-clock time implicitly.

---

## 9. Recordability (Normative)

Test execution SHOULD be recordable as an artifact, including:

* what version was tested
* what fixtures were used
* what assertions were evaluated
* pass/fail outcomes

---

## 10. Target Independence (Normative)

This specification MUST NOT define:

* network mock frameworks
* CI tooling
* transport simulation

Targets may provide concrete test runners, provided semantic meaning and determinism requirements are preserved.
