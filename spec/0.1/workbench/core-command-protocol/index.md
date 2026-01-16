Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Core Command Protocol

---

## 1. Purpose

This specification defines the **canonical command-and-response protocol** for the Paperhat Workbench Core.

It exists to:

* define the closed set of commands the Workbench Core accepts
* define the closed set of responses the Workbench Core produces
* ensure all interaction surfaces invoke identical behavior
* enforce determinism, explicitness, and refusal-first semantics
* provide a stable, strongly-typed interaction boundary

This specification defines **what commands exist and what they mean**.
It does not define UI behavior or implementation details.

---

## 2. Authority

The Workbench Core Command Protocol operates under the authority of:

* **Paperhat Workbench Contract**
* **Paperhat Workbench Core Contract**
* **Paperhat Workbench Principles**
* **Paperhat Workbench Diagnostic Messaging and Help Contract**
* **Paperhat Workbench Workspace Filesystem Contract**
* **Paperhat Workbench Workspace Configuration Contract**
* **Paperhat Workbench Templates and File Plans Contract**

All commands and responses MUST conform to those specifications.

---

## 3. Protocol Characteristics (Normative)

The protocol MUST be:

* closed-world (no ad-hoc commands)
* deterministic
* explicit
* refusal-first
* serializable
* replayable
* interface-agnostic

All interaction surfaces MUST invoke the Workbench Core **exclusively** through this protocol.

---

## 4. Fundamental Concepts

### 4.1 Workspace

A **Workspace** is the canonical unit of operation.

All commands operate on an explicit workspace reference.

---

### 4.2 Snapshot

A **Snapshot** is an immutable view of a workspace state at a specific moment.

Snapshots:

* are read-only
* are deterministic
* may be used for introspection, preview, diff, and explanation
* MUST NOT be mutated

---

### 4.3 Patch

A **Patch** is a deterministic proposal to change authored content.

Patches:

* describe intended changes
* are reviewable prior to application
* MUST NOT be applied implicitly

---

### 4.4 File Plan

A **File Plan** is a deterministic plan describing filesystem changes.

File Plans:

* enumerate file creations, modifications, and deletions (if supported)
* are reviewable prior to application
* MUST be applied explicitly

---

## 5. Command Execution Semantics (Normative)

Each command invocation MUST result in exactly one of:

* a successful response, OR
* a refusal with Diagnostics

Partial execution is forbidden.

All refusals MUST return Diagnostics conforming to the Diagnostic Messaging and Help Contract.

---

## 6. Core Command Set (Normative)

### 6.1 Workspace Commands

* `OpenWorkspace`
* `CreateWorkspace`
* `CheckWorkspace`

---

### 6.2 Snapshot Commands

* `CreateSnapshot`

---

### 6.3 Template and Scaffold Commands

* `ResolveTemplate`
* `DryRunFilePlan`
* `ApplyFilePlan`

---

### 6.4 Authoring Commands

* `ProposePatch`
* `ApplyPatch`

---

### 6.5 Configuration Commands

* `CompileConfig`
* `ReadConfig`

---

### 6.6 Preview and Build Commands

* `StartPreview`
* `StopPreview`
* `BuildTarget`

---

### 6.7 Introspection Commands

* `GetWorkspaceInventory`
* `GetGraph`
* `GetAssembledStructure`
* `GetViewModel`
* `GetPresentationPlan`
* `DiffSnapshots`

---

### 6.8 Assistive Commands

* `CreateAssistSession`
* `ProposeAssistPatch`

---

## 7. Command Semantics: `CheckWorkspace` (Normative)

### 7.1 Purpose

`CheckWorkspace` is the canonical **preflight command**.

It validates that the workspace, configuration, and selected target (if any) satisfy the minimum requirements required to safely invoke other Workbench operations.

---

### 7.2 Inputs

`CheckWorkspace` MUST accept inputs sufficient to:

* select a workspace root (explicit path or current working directory context)
* optionally select a target (when checking preview/build readiness)

This specification does not mandate flag names.

---

### 7.3 Workspace Root Validation

A directory is a valid Workbench workspace root if and only if it contains:

* `modules/`
* `.paperhat/`

If either directory is missing, `CheckWorkspace` MUST refuse with Diagnostics.

---

### 7.4 Filesystem Contract Validation

`CheckWorkspace` MUST validate conformance to the **Workbench Workspace Filesystem Contract**.

At minimum:

* `modules/` MUST exist and MUST be treated as the only authoring root
* `.paperhat/` MUST exist and MUST be treated as a reserved tooling namespace
* Workbench MUST NOT treat `.paperhat/` as an authoring module root

---

### 7.5 Configuration Validation

If configuration sources are present, `CheckWorkspace` MUST:

* validate configuration source presence and structure
* validate that compiled configuration can be produced deterministically
* refuse if configuration compilation would fail

---

### 7.6 Target Selection Validation

If `CheckWorkspace` is invoked in a mode that requires a target, then:

* target selection MUST be explicit
* ambiguous or missing target selection MUST be refused
* Workbench MUST NOT silently change targets based on environment

---

### 7.7 Safety and Hygiene Checks

If `CheckWorkspace` is invoked as a prerequisite for an operation that would modify many files, Workbench MUST ensure that:

* a dry-run mode exists for the operation
* conflicts that would overwrite existing files are detected

On conflict, Workbench MUST either:

* refuse with Diagnostics, OR
* require an explicit override input

---

### 7.8 Diagnostic Requirements

When `CheckWorkspace` refuses, Diagnostics MUST:

* identify the workspace root that was checked
* identify each failed rule
* provide a constructive, non-blaming explanation for each failure

---

## 8. Response Types (Normative)

Each command MUST return exactly one of:

* a command-specific success response
* a refusal containing Diagnostics

Responses MUST be serializable, deterministic, and inspectable.

---

## 9. Determinism Requirements (Normative)

Given identical:

* inputs
* workspace state
* configuration sources
* selected targets
* Workbench and Kernel versions

Command execution MUST produce identical responses.

Ambient environment, time, randomness, or network input MUST NOT influence results.

---

## 10. Extensibility (Normative)

New commands MAY be added only by:

* updating this specification
* assigning explicit semantics
* preserving closed-world guarantees

Ad-hoc or experimental commands are forbidden.

---

## 11. Reality Rule (Normative)

This specification defines the command surface **as it is**.

There is no legacy protocol.
There are no compatibility modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
