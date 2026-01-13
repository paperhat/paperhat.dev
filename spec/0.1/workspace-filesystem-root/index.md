Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workspace Filesystem Root

This specification defines the canonical on-disk unit for Paperhat authoring: the **workspace**.

This document is **Normative**.

---

## 1. Purpose

Paperhat needs a stable unit of containment for authored Modules, deterministic compilation, and tooling.

This spec exists to:

- define what a Paperhat workspace is
- define the required top-level directories
- reserve tooling namespaces without granting them semantic authority

---

## 2. Definitions

- **Workspace**: the canonical on-disk unit containing authored Modules and (optionally) tooling artifacts.
- **Workspace root**: the directory representing a single workspace.
- **Authoring root**: the directory under which authored Modules are stored.

---

## 3. Workspace Root (Hard)

A Paperhat workspace root MUST contain:

- `modules/`

A Paperhat workspace root MAY contain:

- `.paperhat/`

If `.paperhat/` is present, it MUST be treated as a reserved tooling namespace.

---

## 4. Authoring Root (Hard)

`modules/` is the canonical authoring root.

Rules:

1. Tooling MUST treat `modules/` as the only authoring root.
2. Tooling MUST NOT create additional hidden authoring roots.
3. Tooling MUST NOT infer semantics from filesystem paths beyond what Paperhat specifications explicitly define.

See also:

- `Module Filesystem Assembly v0.1`

---

## 5. Reserved Tooling Namespace (Normative)

`.paperhat/` is reserved for developer tooling configuration and runtime artifacts.

Rules:

1. Tooling MUST NOT treat `.paperhat/` as an authoring root.
2. Tooling MUST NOT place authored Modules under `.paperhat/`.
3. `.paperhat/` MUST be safe to delete for a clean tool re-run, except for any explicitly documented user configuration stored there.

---

## 6. Relationship to Workbench (Non-authoritative)

Workbench (`paperhat`) is one implementation that operates on workspaces.

Workbench MAY require `.paperhat/` to exist for dev-mode configuration and runtime artifacts.

Paperhat remains valid if Workbench is removed or replaced.

---

**End of Workspace Filesystem Root v0.1**
