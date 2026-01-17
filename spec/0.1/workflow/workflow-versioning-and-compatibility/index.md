Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Workflow Versioning and Compatibility Specification

This specification defines Paperhat’s target-independent semantics for **workflow versioning**, **compatibility**, and **migration-safe evolution**.

This document governs semantic meaning and planning interfaces.
It does **not** define deployment pipelines, package registries, or runtime release mechanisms.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define what it means for workflow artifacts to be versioned
* define compatibility expectations for workflow calls and triggers
* allow safe evolution of workflows without breaking running executions
* preserve auditability of what version executed and why

---

## 2. Scope

This specification governs:

* workflow identity and version identity
* compatibility contracts for workflow inputs/outputs
* version selection and pinning semantics
* migration semantics for long-running/pending runs
* recordability requirements for version decisions

This specification does **not** govern:

* packaging formats
* registries
* CI/CD release processes
* deployment topology

---

## 3. Related Specifications

This specification is designed to compose with:

* [Workflow Orchestration](../workflow-orchestration/)
* [Subworkflows and Reuse](../subworkflows-and-reuse/)
* [Triggers and Scheduling](../triggers-and-scheduling/)
* [Run Logs and Observability](../run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Workflow identity is stable.** Workflow identity MUST be stable across versions.
2. **Version selection is explicit.** Any selection/pinning policy MUST be explicit.
3. **Compatibility is semantic.** Compatibility MUST be defined in terms of declared contracts, not runtime behavior.
4. **Runs are attributable.** It MUST be possible to record exactly what version executed.
5. **Pending safety.** Version evolution MUST NOT silently invalidate pending work.

---

## 5. Definitions (Normative)

### 5.1 Workflow Identity

A **WorkflowIdentity** identifies a workflow artifact independently of version.

---

### 5.2 Workflow Version

A **WorkflowVersion** identifies a specific published version of a workflow.

A WorkflowVersion MUST include:

* a version identifier
* a reference to the workflow identity
* declared input/output contracts

---

### 5.3 Compatibility Contract

A **CompatibilityContract** defines compatibility between versions.

At minimum, compatibility MUST consider:

* input parameter contracts
* output contracts
* required external inputs

---

### 5.4 Version Selection Policy

A **VersionSelectionPolicy** defines how a version is chosen at call time.

At minimum, Kernel MUST support:

* exact version pin
* compatibility-based selection

---

### 5.5 Migration Policy

A **MigrationPolicy** defines what happens when a newer version exists.

MigrationPolicy MUST support:

* continue existing runs on their pinned version
* upgrade only at explicit boundaries
* require explicit approval for upgrade (if configured)

---

## 6. Compatibility Semantics (Normative)

A workflow version MUST declare input/output contracts.

Compatibility MUST be evaluated deterministically by Kernel.

Compatibility evaluation MUST NOT require executing the workflow.

---

## 7. Version Pinning Semantics (Normative)

Workflow calls MUST define version selection.

If a call pins a version, the pinned version MUST be used for that call unless an explicit migration policy allows otherwise.

---

## 8. Long-Running and Pending Runs (Normative)

If a run is pending (for example, awaiting approvals or external inputs), version evolution MUST NOT silently change the meaning of the pending request.

A migration policy MUST define whether:

* pending work continues under the original version
* pending work must be re-issued under a new version

---

## 9. Triggers and Versioning (Normative)

Triggers MUST be attributable to a workflow version.

A trigger definition MUST define:

* whether it always targets a specific version
* whether it tracks a compatible version set

---

## 10. Recordability (Normative)

Run logs MUST be able to record:

* workflow identity
* selected workflow version
* version selection policy
* any migration/upgrade decisions and reasons

---

## 11. Target Independence (Normative)

This specification MUST NOT define:

* packaging formats
* registry operations
* deployment mechanisms

Targets may manage versions however they choose, provided semantic meaning, deterministic planning, and recordability requirements are preserved.
