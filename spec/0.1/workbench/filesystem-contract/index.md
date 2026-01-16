Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Workspace Filesystem Contract

---

## 1. Purpose

This specification defines the **on-disk filesystem contract** enforced by the Paperhat Workbench.

It exists to ensure that:

* workspaces are structurally unambiguous
* authored content is clearly separated from tooling state
* deterministic operation is possible
* no implicit semantics leak through filesystem layout

This document is **Normative**.

---

## 2. Scope

This specification governs:

* required workspace directories
* required workspace files (when specified)
* reserved namespaces
* where Workbench may read and write data

This specification does **not** define:

* authored content formats
* semantic meaning
* target rendering behavior

---

## 3. Workspace Root (Normative)

A workspace operated on by the Workbench MUST contain:

* `modules/`
* `.paperhat/`
* `output/`
* `documentation/`

Workbench MUST create these directories during workspace creation.

Workbench MUST refuse operation if any required directory is missing.

---

## 4. `modules/` — Authored Content Root (Normative)

`modules/` is the **only** root for user-authored content.

Rules:

* all authored Modules MUST reside under `modules/`
* Workbench MUST NOT treat any other directory as an authoring root
* Workbench MAY generate boilerplate under `modules/` only via explicit, reviewable actions

Authored content under `modules/` is sacrosanct.

---

## 5. `.paperhat/` — Reserved Tooling Namespace (Normative)

`.paperhat/` is a **reserved, Workbench-owned namespace**.

Rules:

* `.paperhat/` MUST NOT be treated as authored content
* `.paperhat/` MAY contain configuration sources
* `.paperhat/` MAY contain tool-owned runtime artifacts
* users MUST NOT be required to hand-edit runtime artifacts

For Workbench-managed workspaces, Workbench MUST create a canonical configuration file at:

* `.paperhat/configuration.cdx`

Workbench MUST NOT place authored Modules under `.paperhat/`.

---

## 6. Output and Documentation Directories (Normative)

Build outputs MUST be written to:

* `output/{target}/`

Documentation outputs MUST be written to:

* `documentation/{target}/`

Rules:

* outputs MUST be target-scoped
* outputs MUST be reproducible
* outputs MUST NOT contaminate authored content

Additional rules for documentation outputs:

* documentation outputs MUST be derived deterministically from the workspace’s explicit inputs (including `modules/`)
* documentation outputs MUST NOT be treated as authored content
* documentation outputs MUST NOT influence Workbench behavior unless explicitly selected as an output destination

Preview artifacts MAY be transient but MUST remain confined to tooling namespaces.

---

## 7. Safety and Hygiene (Normative)

Workbench MUST:

* avoid destructive writes by default
* support dry-run modes for filesystem-altering operations
* detect and refuse unsafe overwrites unless explicitly authorized

Filesystem operations MUST be deterministic and reviewable.

---

## 8. Determinism Requirement (Normative)

Given identical inputs and workspace state:

* filesystem reads and writes MUST be identical
* directory creation and file placement MUST be stable

Ambient filesystem state MUST NOT influence behavior beyond explicit paths.

---

## 9. Extensibility (Normative)

Additional directories MAY be introduced only if:

* their purpose is specified normatively
* ownership boundaries are explicit
* they do not introduce semantic ambiguity

Ad-hoc directories are forbidden.

---

## 10. Reality Rule (Normative)

This specification defines the workspace filesystem **as it is**.

There is no legacy layout.
There are no compatibility shims.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
