Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Work Configuration Contract

---

## 1. Purpose

This specification defines the **work configuration model** used by the Paperhat Workbench.

It exists to ensure that:

* configuration is explicit, reviewable, and deterministic
* authored meaning is never contaminated by tooling state
* preview and build behavior is fully specified
* configuration compilation is stable and reproducible

This document is **Normative**.

---

## 2. Scope

This specification governs:

* work configuration sources
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

Work configuration MUST be:

* explicit
* deterministic
* idempotent
* reviewable
* tooling-owned once compiled

Workbench MUST NOT infer configuration from ambient environment.

---

## 4. Configuration Locations (Normative)

Workbench work configuration MUST be represented as a single canonical Codex artifact at:

* `.paperhat/configuration.cdx`

This file is the authoritative configuration input for Workbench operations.

### 4.1 Workspace-Level Configuration (Normative)

A Workspace MAY provide a Workspace-level configuration file at:

* `workspace.cdx`

If present, `workspace.cdx` supplies Workspace-scoped defaults (for example: defaults for `paperhat new`, template sources, and other workspace-level behavior).

`workspace.cdx` is not a substitute for the authoritative Work configuration file.

#### 4.1.1 `workspace.cdx` Shape (Normative)

If `workspace.cdx` is present, it MUST be valid Codex and MUST conform to the following minimal shape.

Recognized top-level keys:

* `defaultTemplate` (string) — default template identifier used by `paperhat new` when no template is explicitly provided.
* `templateSources` (array) — an ordered list of template source identifiers.
* `assets` (object) — Workspace-level shared asset settings.

If `assets` is present, it MUST support:

* `enabled` (boolean)
* `path` (string) — MUST be `assets/`.

Rules:

1. `workspace.cdx` MUST be treated as Workspace-scoped defaults only.
2. `workspace.cdx` MUST NOT change the semantic results of a build for an existing Work.
3. Workbench MUST refuse a `workspace.cdx` that contains unknown top-level keys.
4. Workbench MUST treat `templateSources` ordering as authoritative.

### 4.2 User-Level Configuration (Normative)

A user MAY provide user-level configuration under:

* `~/.paperhat/`

User-level configuration supports selecting and organizing multiple Workspaces (for example: separate business and personal Workspaces) and defining user preferences.

User-level configuration is convenience configuration.

#### 4.2.1 Workspace Registry (Normative)

If user-level configuration is used to select and organize multiple Workspaces, the canonical registry file is:

* `~/.paperhat/workspaces.cdx`

If present, `~/.paperhat/workspaces.cdx` MUST be valid Codex and MUST conform to the following minimal shape.

Recognized top-level keys:

* `workspaces` (array) — an ordered list of Workspace registrations.
* `defaultWorkspace` (string) — the name of the default Workspace.

Each entry in `workspaces` MUST contain:

* `name` (string)
* `path` (string) — an absolute path to the Workspace root folder.

Selection rules:

1. If a Workspace root is provided explicitly as a path input, that path is authoritative for the operation.
2. If a Workspace is provided explicitly as a name, Workbench resolves the name using `~/.paperhat/workspaces.cdx`.
3. If no Workspace is provided explicitly, Workbench MAY use `defaultWorkspace` if present.

Rules:

1. User-level configuration MUST NOT change the semantic results of a build for an existing Work.
2. Workbench MUST refuse a registry that contains duplicate `name` entries.
3. Workbench MUST refuse a registry entry whose `path` does not resolve to a Workspace root.

### 4.3 Relationship to the Filesystem Contract (Normative)

This specification assumes the work filesystem requirements defined by the Work Filesystem Contract.

In particular:

* `.paperhat/` is a reserved tooling namespace and MUST NOT be treated as authored content
* build outputs belong under `output/{target}/`
* documentation outputs belong under `documentation/{target}/`

See: [Paperhat Workbench Work Filesystem Contract](../filesystem-contract/).

---

## 5. Configuration Sources (Normative)

Configuration sources:

* are explicit inputs to Workbench operations
* MAY be authored using Paperhat-specified formats (e.g., Codex)
* MUST be treated as authored inputs, not runtime state

Workbench MUST NOT consult time, randomness, network, or environment when interpreting configuration sources.

### 5.1 Configuration Layering (Normative)

Workbench behavior MUST be determined by explicit inputs and explicit configuration sources.

Rules:

1. `.paperhat/configuration.cdx` is authoritative for a Work.
2. `workspace.cdx` MAY supply Workspace-scoped defaults for Workbench operations.
3. User-level configuration under `~/.paperhat/` MAY supply user-scoped defaults and a registry of Workspace roots (for example: `~/.paperhat/workspaces.cdx`).
4. User-level configuration MUST NOT change the semantic results of a build for an existing Work; it may select paths and defaults.

### 5.2 Canonical Configuration File (Normative)

The canonical configuration file is:

* `.paperhat/configuration.cdx`

---

## 6. Compiled Configuration (Normative)

Workbench MUST produce (or accept) a **single canonical configuration artifact**.

Rules:

* compiled configuration MUST be deterministic
* compiled configuration MUST be idempotent
* configuration MUST be deterministic
* users MUST NOT be required to hand-edit any tool-owned derived artifacts

### 6.1 Deterministic Compilation Inputs (Normative)

Determinism is defined over explicit inputs only.

Given identical explicit inputs (including configuration source contents, selected target(s), and Workbench and Kernel versions), compilation MUST produce identical compiled configuration bytes.

Workbench MUST NOT consult ambient time, randomness, network, or environment to decide compiled configuration contents.

---

## 7. Compiled Configuration Location (Normative)

The canonical configuration artifact is located at:

* `.paperhat/configuration.cdx`

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
* identify the work root
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

This specification defines work configuration **as it is**.

There is no legacy configuration format.
There are no implicit defaults.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
