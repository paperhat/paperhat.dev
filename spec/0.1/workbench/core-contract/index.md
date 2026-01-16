Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Core Contract

---

## 1. Definition

The **Paperhat Workbench Core** is the canonical, headless system that performs all deterministic operations required to author, inspect, preview, and produce Paperhat workspaces.

The Workbench Core is the **only authority** for:

* workspace creation and validation
* template resolution
* File Plan production and application
* authoring mutation via Patches
* configuration compilation
* preview and build orchestration
* introspection and explanation
* diagnostic production and refusal semantics

All interaction surfaces invoke the Workbench Core.
No interaction surface redefines behavior.

---

## 2. Governing Authority

The Workbench Core operates under the authority of:

* **Paperhat Workbench Principles**
* **Paperhat Workbench Diagnostic Messaging and Help Contract**
* **Paperhat Workbench Core Command Protocol**

All Core behavior MUST conform to those specifications.

---

## 3. Non-Negotiable Properties (Normative)

The Workbench Core MUST be:

* deterministic
* explicit
* idempotent
* refusal-first
* reviewable
* explainable
* side-effect disciplined

The Workbench Core MUST NOT:

* infer intent
* consult ambient environment, time, randomness, or network state
* mutate authored content implicitly
* expose partial or corrupt state
* perform unspec’d behavior

---

## 4. Inputs and Outputs (Normative)

### 4.1 Inputs

All inputs to the Workbench Core MUST be explicit and include only:

* workspace references
* template identities and contents
* explicit user inputs
* selected targets
* configuration sources
* explicit command parameters

Implicit inputs are forbidden.

---

### 4.2 Outputs

All outputs from the Workbench Core MUST be explicit and include only:

* command responses
* File Plans
* applied filesystem changes
* Compiled Config artifacts
* preview and build artifacts
* Diagnostics

All outputs MUST be deterministic given identical inputs.

---

## 5. Workspace Authority (Normative)

The workspace is the canonical unit of operation.

The Workbench Core MUST:

* operate on exactly one explicit workspace per command
* enforce the Workbench Workspace Filesystem Contract
* refuse operation on non-conforming workspaces

---

## 6. Mutation Discipline (Normative)

All mutation of authored content MUST occur exclusively through:

* `ApplyPatch`
* `ApplyFilePlan`

The Workbench Core MUST:

* require explicit user intent for mutation
* support review of all mutations prior to application
* refuse mutation by default on conflict

Implicit mutation is forbidden.

---

## 7. Snapshot Discipline (Normative)

The Workbench Core MUST support immutable Snapshots.

Snapshots:

* represent read-only views of workspace state
* MUST be deterministic
* MUST NOT be mutated
* MUST be the basis for all introspection, explanation, and diff operations

---

## 8. Orchestration Role (Normative)

The Workbench Core is responsible for **orchestration**, not semantics.

The Workbench Core MUST:

* sequence pipeline stages deterministically
* invoke authoritative subsystems (e.g., Kernel)
* propagate subordinate Diagnostics without distortion

The Workbench Core MUST NOT:

* redefine semantic rules
* bypass validation
* embed semantic logic

Semantic authority resides elsewhere.

---

## 9. Introspection and Explanation (Normative)

The Workbench Core MUST support read-only introspection into:

* workspace structure
* assembled artifacts
* resolved identifiers and references
* ViewModels
* Presentation Plans
* File Plans
* build artifacts

Introspection MUST be:

* deterministic
* snapshot-based
* non-mutating

---

## 10. Interaction Surfaces (Normative)

The Workbench Core MUST have no knowledge of:

* CLI
* GUI
* desktop environments
* web environments
* dialogs, buttons, or widgets

All interaction surfaces are **clients** of the Workbench Core.

Differences between surfaces are presentation-only and MUST NOT affect behavior.

---

## 11. Diagnostics and Refusal (Normative)

All failures within the Workbench Core MUST result in:

* refusal of the command
* return of Diagnostics conforming to the Diagnostic Messaging and Help Contract

Partial execution is forbidden.

---

## 12. Persistence Discipline (Normative)

The Workbench Core MAY write:

* tool-owned artifacts under `.paperhat/`
* build artifacts under `output/`

The Workbench Core MUST NOT:

* write authored content outside `modules/`
* create hidden state affecting determinism

---

## 13. Extensibility (Normative)

New Core capabilities MAY be added only by:

* extending the Workbench Core Command Protocol
* updating normative specifications
* preserving all non-negotiable properties

Ad-hoc behavior is forbidden.

---

## 14. Reality Rule (Normative)

This specification defines the Workbench Core **as it is**.

There is no legacy behavior.
There are no deprecated modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
