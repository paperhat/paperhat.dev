Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Workspace Filesystem Contract

This specification defines the **on-disk contract** Workbench MUST enforce for a Paperhat workspace.

This document is **Normative**.

---

## 1. Scope

This contract governs:

- required top-level directories (`.paperhat/`, `modules/`)
- reserved namespaces
- what Workbench MAY place on disk

It does not define authored semantics content formats.

---

## 2. Workspace Root (Normative)

A Paperhat workspace root operated on by Workbench MUST contain:

- `.paperhat/`
- `modules/`

Workbench MUST create these during `paperhat new`.

Note (Normative): The Paperhat workspace root specification permits `.paperhat/` to be absent in general. This contract defines a stronger requirement for Workbench-managed operation.

See also:

- [Workspace Filesystem Root](../workspace-filesystem-root/)

---

## 3. `modules/` (Normative)

`modules/` is the root of authored content.

Rules:

1. Workbench MUST treat `modules/` as the only root for user-authored modules.
2. Workbench MUST NOT create additional hidden authoring roots.
3. Workbench MAY generate boilerplate within `modules/`, but MUST do so deterministically.

---

## 4. `.paperhat/` (Normative)

`.paperhat/` is a reserved namespace.

Rules:

1. Workbench MUST treat `.paperhat/` as Workbench-owned.
2. Workbench MUST NOT treat `.paperhat/` as an authoring module root.
3. Workbench MAY write configuration and runtime artifacts under `.paperhat/`.

---

## 5. Safety and Hygiene (Normative)

Workbench MUST:

- avoid destructive writes by default
- provide a dry-run mode for operations that modify many files
- emit diagnostics when the workspace root does not conform to this contract

---

**End of Workbench Workspace Filesystem Contract v0.1**
