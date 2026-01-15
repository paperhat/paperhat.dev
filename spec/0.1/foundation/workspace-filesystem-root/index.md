Status: NORMATIVE  
Lock State: LOCKED  
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
- **Pack root**: a directory containing one or more packs loadable by Kernel as an explicit input.
- **Pack**: a versioned directory of Codex artifacts.
- **Dialect pack**: a pack that provides one or more dialect ontologies and constraints (authored in the Schema Dialect).
- **Vocabulary pack**: a pack that provides domain vocabulary within one or more dialects.

---

## 3. Workspace Root (Normative)

A Paperhat workspace root MUST contain:

- `modules/`

A Paperhat workspace root MAY contain:

- `.paperhat/`

If `.paperhat/` is present, it MUST be treated as a reserved tooling namespace.

---

## 4. Authoring Root (Normative)

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

### 5.1 Pack Roots (Normative)

Pack roots are explicit inputs to Kernel.

Tooling MAY provide a conventional directory name such as `packs/` for pack storage, but directory naming confers no semantic authority.

Rules:

1. Kernel MUST treat pack roots as explicit inputs; a `packs/` directory MUST NOT affect outputs unless it is provided to Kernel as an input pack root.
2. Tooling MUST NOT infer semantic meaning from pack folder names; pack identity is declared inside pack Codex.

### 5.2 Compiled Projection Caches (Normative)

Tooling MAY store non-authoritative compiled projection caches under `.paperhat/`.

If present, the following subdirectory is reserved for caches:

- `.paperhat/runtime/cache/`

Rules:

1. Caches MUST be safe to delete.
2. Caches MUST NOT be treated as authoring inputs.
3. Cache presence MUST NOT change semantic results; caches exist only to avoid recompilation.

---

## 6. Relationship to Workbench (Non-authoritative)

Workbench (`paperhat`) is one implementation that operates on workspaces.

Workbench MAY require `.paperhat/` to exist for configuration and runtime artifacts.

Paperhat remains valid if Workbench is removed or replaced.

---

**End of Workspace Filesystem Root v0.1**
