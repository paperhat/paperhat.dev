Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workspace and Work Filesystem Roots

This specification defines the canonical on-disk containment model for Paperhat authoring: the **Workspace** (container folder) and the **Work** (authoring unit).

This document is **Normative**.

---

## 1. Purpose

Paperhat needs a stable unit of containment for authored Modules, deterministic compilation, and tooling.

This spec exists to:

- define what a Paperhat Workspace and Work are
- define the required top-level folders for a Work
- reserve tooling namespaces without granting them semantic authority

---

## 2. Definitions

- **Workspace**: a container folder that organizes one or more Works.
- **Workspace root**: the folder representing a single Workspace.
- **Work**: the canonical on-disk authoring unit containing authored Modules and (optionally) tooling artifacts.
- **Work root**: the folder representing a single Work.
- **Authoring root**: the folder under which authored Modules are stored.
- **Pack root**: a folder containing one or more packs loadable by Kernel as an explicit input.
- **Pack**: a versioned folder of Codex artifacts.
- **Dialect pack**: a pack that provides one or more dialect ontologies and constraints (authored in the Schema Dialect).
- **Vocabulary pack**: a pack that provides domain vocabulary within one or more dialects.

---

## 3. Workspace Container (Normative)

A Paperhat Workspace is a container folder.

Rules:

1. Tooling MUST treat a Workspace as a container for Works.
2. Tooling MUST NOT treat a Workspace as an authoring root.
3. Tooling MUST treat each Work root as an explicit unit of operation.

### 3.1 Workspace Contents (Normative)

Works MUST be direct child folders of the Workspace root.

Rules:

1. A Workspace root MUST contain one or more Work root folders as direct children.
2. A Workspace root MUST NOT contain non-Work folders except those explicitly permitted by this specification.
3. A folder is a Work root if and only if it conforms to the Work Root requirements in this specification.

A Workspace root MAY also contain:

* `workspace.cdx`

### 3.2 Workspace-Level Shared Assets (Normative)

A Workspace root MAY contain an `assets/` folder for shared, non-authoritative files.

Rules:

1. `assets/` MUST NOT be treated as an authoring root.
2. `assets/` MUST NOT confer semantic authority by its presence.
3. Any use of `assets/` MUST be explicit via configuration or explicit tool inputs.

### 3.3 Workspace Configuration File (Normative)

If present, `workspace.cdx` is the Workspace-level configuration file.

`workspace.cdx` defines Workspace-scoped defaults used by Workbench (for example: defaults for `paperhat new`, workspace naming, template sources, and other workspace-level behavior).

Rules:

1. `workspace.cdx` MUST NOT be treated as an authoring root.
2. `workspace.cdx` MUST NOT override the authoritative work configuration file (`.paperhat/configuration.cdx`) inside any Work.
3. Any effect of `workspace.cdx` on Workbench behavior MUST be explicit and deterministic.

#### 3.3.1 `workspace.cdx` Minimal Shape (Normative)

If `workspace.cdx` is present, it MUST be valid Codex.

Recognized top-level keys:

* `defaultTemplate` (string) — default template identifier used by Workbench when no template is explicitly provided.
* `templateSources` (array) — an ordered list of template source identifiers.
* `assets` (object) — Workspace-level shared asset settings.

If `assets` is present, it MUST support:

* `enabled` (boolean)
* `path` (string) — MUST be `assets/`.

Rules:

1. `templateSources` ordering MUST be treated as authoritative.
2. `workspace.cdx` MUST be treated as Workspace-scoped defaults only.
3. `workspace.cdx` MUST NOT change the semantic results of a build for an existing Work.

See also:

* [Paperhat Workbench Work Configuration Contract v0.1](../../workbench/workspace-configuration-contract/)

---

## 4. Work Root (Normative)

A Paperhat Work root MUST contain:

- `modules/`

A Paperhat Work root MAY contain:

- `.paperhat/`

If `.paperhat/` is present, it MUST be treated as a reserved tooling namespace.

---

## 5. Authoring Root (Normative)

`modules/` is the canonical authoring root.

Rules:

1. Tooling MUST treat `modules/` as the only authoring root.
2. Tooling MUST NOT create additional hidden authoring roots.
3. Tooling MUST NOT infer semantics from filesystem paths beyond what Paperhat specifications explicitly define.

See also:

- `Module Filesystem Assembly v0.1`

---

## 6. Reserved Tooling Namespace (Normative)

`.paperhat/` is reserved for developer tooling configuration and runtime artifacts.

Rules:

1. Tooling MUST NOT treat `.paperhat/` as an authoring root.
2. Tooling MUST NOT place authored Modules under `.paperhat/`.
3. `.paperhat/` MUST be safe to delete for a clean tool re-run, except for any explicitly documented user configuration stored there.

### 6.1 Pack Roots (Normative)

Pack roots are explicit inputs to Kernel.

Tooling MAY provide a conventional folder name such as `packs/` for pack storage, but folder naming confers no semantic authority.

Rules:

1. Kernel MUST treat pack roots as explicit inputs; a `packs/` folder MUST NOT affect outputs unless it is provided to Kernel as an input pack root.
2. Tooling MUST NOT infer semantic meaning from pack folder names; pack identity is declared inside pack Codex.

### 6.2 Compiled Projection Caches (Normative)

Tooling MAY store non-authoritative compiled projection caches under `.paperhat/`.

If present, the following subfolder is reserved for caches:

- `.paperhat/runtime/cache/`

Rules:

1. Caches MUST be safe to delete.
2. Caches MUST NOT be treated as authoring inputs.
3. Cache presence MUST NOT change semantic results; caches exist only to avoid recompilation.

---

## 7. Relationship to Workbench (Non-authoritative)

Paperhat Workshop ("Workshop") is the distributed application that contains Kernel and Workbench.

Workbench (`paperhat`) is one implementation that operates on Works and organizes them inside a Workspace.

Workbench MAY require `.paperhat/` to exist for configuration and runtime artifacts.

By default, Workbench MAY create and use a Workspace folder named `paperhat` under the user’s `Documents` folder, but the Workspace location and name are user-configurable.

Workshop distributes Workbench and Kernel as a cohesive toolchain.

Paperhat remains valid if Workbench is removed or replaced.

---

**End of Workspace and Work Filesystem Roots v0.1**
