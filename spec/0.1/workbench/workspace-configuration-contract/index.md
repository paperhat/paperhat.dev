Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Workspace Configuration Contract

---

## 1. Purpose

This specification defines the **workspace configuration model** used by the Paperhat Workbench.

It exists to ensure that:

* configuration is explicit, reviewable, and deterministic
* authored meaning is never contaminated by tooling state
* preview and build behavior is fully specified
* configuration compilation is stable and reproducible

This document is **Normative**.

---

## 2. Scope

This specification governs:

* workspace configuration sources
* compiled configuration artifacts
* target definitions and selection
* configuration compilation behavior

This specification does **not** define:

* semantic meaning
* rendering behavior
* UI presentation
* implementation technology

---

## 3. Configuration Principles (Normative)

Workspace configuration MUST be:

* explicit
* deterministic
* idempotent
* reviewable
* tooling-owned once compiled

Workbench MUST NOT infer configuration from ambient environment.

---

## 4. Configuration Locations (Normative)

If workspace configuration is used, it MUST reside under:

* `.paperhat/config/` — user-authored configuration sources
* `.paperhat/runtime/` — tool-owned compiled artifacts

Authored configuration sources and compiled configuration MUST be separated.

### 4.1 Relationship to the Filesystem Contract (Normative)

This specification assumes the workspace filesystem requirements defined by the Workspace Filesystem Contract.

In particular:

* `.paperhat/` is a reserved tooling namespace and MUST NOT be treated as authored content
* build outputs belong under `output/{target}/`

See: [Paperhat Workbench Workspace Filesystem Contract](../filesystem-contract/).

---

## 5. Configuration Sources (Normative)

Configuration sources:

* are explicit inputs to Workbench operations
* MAY be authored using Paperhat-specified formats (e.g., Codex)
* MUST be treated as authored inputs, not runtime state

Workbench MUST NOT consult time, randomness, network, or environment when interpreting configuration sources.

### 5.1 Recommended Source Paths (Non-binding)

Recommended file names and locations:

* `.paperhat/config/config.cdx` — workspace configuration source
* `.paperhat/config/targets/*.cdx` — target definitions

---

## 6. Compiled Configuration (Normative)

Workbench MUST compile configuration sources into a **single canonical configuration artifact**.

Rules:

* compiled configuration MUST be deterministic
* compiled configuration MUST be idempotent
* compiled configuration MUST be treated as tool-owned
* users MUST NOT be required to hand-edit compiled configuration

### 6.1 Deterministic Compilation Inputs (Normative)

Determinism is defined over explicit inputs only.

Given identical explicit inputs (including configuration source contents, selected target(s), and Workbench and Kernel versions), compilation MUST produce identical compiled configuration bytes.

Workbench MUST NOT consult ambient time, randomness, network, or environment to decide compiled configuration contents.

---

## 7. Compiled Configuration Location (Normative)

The compiled configuration MUST be written to:

* `.paperhat/runtime/config.cdx`

This file is authoritative for preview and build orchestration.

---

## 8. Canonical Serialization (Normative)

Compiled configuration MUST use canonical serialization.

Rules:

* stable key ordering
* stable whitespace policy
* no nondeterministic formatting

Spurious diffs are forbidden.

---

## 9. Target Definitions (Normative)

Targets are defined exclusively via configuration.

Rules:

* target identifiers MUST be explicit and stable
* target identifiers MUST match: `^[a-z][a-z0-9-]*$`
* target behavior MUST be fully defined by configuration and authoritative subsystems

Workbench MUST refuse ambiguous or missing target selection.

---

## 10. Preview Semantics (Normative)

Targets MAY declare preview behavior.

Preview kinds MAY include:

* `none`
* `http`
* `file`

If a target declares preview behavior:

* preview configuration MUST be explicit
* preview behavior MUST be deterministic
* preview MUST NOT require external network access

### 10.1 Preview Persistence Control (Normative)

If Workbench supports persistence steps beyond writing build outputs (for example, writing durable indices, stores, or caches), preview mode MUST support an explicit mode that disables those persistence steps.

This behavior MUST be controlled by explicit configuration or explicit CLI flags.

Workbench MUST NOT infer persistence behavior from ambient environment.

---

## 11. Configuration Change Handling (Normative)

If configuration sources change:

* Workbench MUST recompile configuration deterministically, OR
* Workbench MUST refuse and require explicit restart

Silent reconfiguration is forbidden.

---

## 12. Diagnostics (Normative)

Configuration compilation failures MUST:

* refuse the operation
* return Diagnostics
* identify the workspace root
* identify failing configuration sources
* identify the intended compiled configuration output path
* explain unmet requirements constructively

Partial configuration is forbidden.

---

## 13. Extensibility (Normative)

Configuration capabilities MAY be extended only if:

* determinism is preserved
* compilation remains explicit
* behavior is specified normatively

Ad-hoc configuration behavior is forbidden.

---

## 14. Reality Rule (Normative)

This specification defines workspace configuration **as it is**.

There is no legacy configuration format.
There are no implicit defaults.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
