Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Preview and Build Orchestration Contract

---

## 1. Purpose

This specification defines how the Paperhat Workbench **orchestrates preview and build operations**.

Preview and build orchestration exists to:

* realize authored meaning for specific targets
* support iterative authoring through preview
* produce deterministic, reviewable build artifacts
* coordinate subordinate systems without redefining semantics

This document is **Normative**.

---

## 2. Scope

This specification governs:

* preview orchestration
* build orchestration
* target selection and handling
* watch-mode behavior in preview
* interaction with configuration and Kernel systems
* refusal and diagnostic behavior for preview/build

This specification does **not** define:

* semantic rules
* rendering algorithms
* target-specific presentation details
* UI behavior

---

## 3. Orchestration Role (Normative)

Workbench orchestration is **procedural, not semantic**.

The Workbench MUST:

* sequence required pipeline stages deterministically
* invoke authoritative subsystems in the correct order
* propagate Diagnostics faithfully

The Workbench MUST NOT:

* redefine semantic meaning
* alter validation rules
* bypass subordinate system authority

---

## 4. Target Selection (Normative)

All preview and build operations MUST use **explicit target selection**.

Rules:

* a target MUST be selected explicitly
* ambiguous or implicit target selection is forbidden
* refusal MUST occur if no target is selected

Target identifiers MUST conform to the Work Configuration Contract.

---

## 5. Preview Mode (Normative)

Preview mode exists for **iterative authoring**, not production output.

In preview mode, the Workbench MUST:

* watch authored content under `modules/` for changes
* rebuild deterministically when watched inputs change
* preserve authored content on failure
* surface Diagnostics without corrupting work state
* avoid external network dependencies for preview serving

Preview mode MUST NOT:

* introduce hidden persistence
* consult ambient time, randomness, or network inputs to decide outputs
* apply destructive optimizations
* alter authored content implicitly

---

## 6. Watch Loop Requirements (Normative)

In preview mode, Workbench MUST:

* establish a deterministic watch set rooted at the work inputs used by the selected target
* trigger rebuilds only from explicit observed changes
* ensure rebuild sequencing is deterministic
* ensure failures do not corrupt outputs or work

Workbench MUST treat “watch mode” as an orchestration concern only.

---

## 7. Preview Surface (Normative)

If a selected target declares a preview surface, the Workbench MUST provide it locally.

Rules:

* preview surface MUST NOT require external network access
* preview host/port/path selection MUST be deterministic
* preview behavior MUST be explicitly configured or explicitly defaulted by spec’d deterministic rules

Preview presentation details are implementation-defined, but behavior is not.

---

## 8. Build Mode (Normative)

Build mode exists to produce **deterministic artifacts**.

In build mode, the Workbench MUST:

* validate the work and configuration
* execute the full deterministic pipeline for the selected target(s)
* write outputs to target-specific output folders
* produce identical artifacts given identical inputs

Build mode MUST NOT:

* infer intent
* skip validation
* alter authored content

---

## 9. Failure Handling (Normative)

If preview or build cannot proceed:

* the operation MUST be refused (or, in preview watch mode, the failing rebuild MUST be refused)
* authored content MUST remain unchanged
* Diagnostics MUST be returned

Partial or corrupt outputs are forbidden.

---

## 10. Persistence Discipline (Normative)

Workbench MAY persist:

* build artifacts under `output/{target}/`
* tool-owned runtime artifacts under `.paperhat/`

Workbench MUST NOT persist:

* authored content outside `modules/`
* hidden state affecting determinism

---

## 11. Determinism Requirements (Normative)

Given identical:

* work state
* configuration
* selected target(s)
* Workbench and Kernel versions

Preview and build orchestration MUST produce identical results.

Ambient inputs (time, randomness, environment, network) are forbidden.

---

## 12. Extensibility (Normative)

New preview or build capabilities MAY be added only if:

* target selection remains explicit
* determinism is preserved
* orchestration remains non-semantic
* behavior is specified normatively

---

## 13. Reality Rule (Normative)

This specification defines preview and build orchestration **as it is**.

There is no legacy preview behavior.
There are no implicit build modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
