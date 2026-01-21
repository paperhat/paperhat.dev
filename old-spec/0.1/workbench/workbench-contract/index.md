Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Contract

This specification defines what the Paperhat **Workbench** is and what it MUST do.

Paperhat Workshop ("Workshop") is the distributed application that contains Kernel and Workbench.

This document specifies Workbench.

This document is **Normative**.

---

## 1. Purpose

Workbench exists to provide a deterministic, contract-driven way to:

- create new Paperhat Works (filesystem scaffold)
- generate authoring boilerplate (Concepts, Traits, Assemblies, Views, etc.)
- run Paperhat Kernel builds and target realization in **preview mode** with local preview

---

## 2. Authority and Boundaries (Normative)

Workbench MUST NOT redefine Paperhat semantics.

- **Kernel owns** semantic compilation, validation, and deterministic planning.
- **Workbench owns** scaffolding, generators, and developer-facing orchestration.

Workbench MUST treat Kernel as the semantic authority.

---

## 3. Filesystem Contract (Normative)

A Paperhat Work operated on by Workbench MUST have, at minimum:

- `.paperhat/` — reserved for Workbench configuration and runtime artifacts
- `modules/` — the root for authored modules

Rules:

1. Workbench MUST create `.paperhat/` and `modules/` during `paperhat new`.
2. Workbench MUST NOT place authored modules outside `modules/`.
3. `.paperhat/` is a reserved namespace; Workbench MUST NOT treat it as authored module content.

Note (Normative): The Paperhat Work root specification permits `.paperhat/` to be absent in general. Workbench is allowed to impose a stronger requirement for Works it manages.

See also:

- [Workspace and Work Filesystem Roots](../../foundation/workspace-filesystem-root/)
- [Module Filesystem Assembly](../../foundation/module-filesystem-assembly/)

---

## 4. Determinism and Idempotency (Normative)

Workbench MUST be deterministic and retry-safe.

- Given identical inputs (template, answers/flags, versions), Workbench MUST generate identical file trees.
- Generators MUST be idempotent: re-running the same generation with the same inputs MUST NOT drift or corrupt state.
- All variability MUST come from explicit inputs. Workbench MUST NOT consult ambient time/randomness to decide file contents.

---

## 5. CLI Surface (Normative)

Workbench MUST provide a CLI with commands sufficient to cover:

- `paperhat new <template> "Name of work" ...` — create a new Paperhat Work from a named template
- `paperhat create <artifact> ...` — generate authoring boilerplate (Concept, Trait, Assembly, View, etc.)
- `paperhat preview --target <target> ...` — run Kernel builds in watch mode and serve a preview
- `paperhat build --target <target> ...` — produce target outputs deterministically
- `paperhat check ...` — validate filesystem contract and inputs prior to running operations

This spec does not mandate flag names or UX beyond the required capability.

### 5.1 `paperhat new` Placement (Normative)

`paperhat new` MUST create the Work as a new folder inside a Workspace folder selected explicitly or by explicit configuration (for example: `workspace.cdx`).

The created Work MUST be a direct child folder of the Workspace root.

The created Work folder name MUST be a stable kebab-case form of the provided `"Name of work"` (for example: `"Name of work"` → `name-of-work`).

---

## 6. Templates (Normative)

Workbench MUST support multiple templates (for example: "blog", "recipes", etc.).

A template resolution MUST produce a **file plan** that can be:

- previewed (dry-run)
- applied deterministically
- validated against a filesystem contract

---

## 7. Preview Mode (Normative)

Preview mode is for development, not production. It watches work files and updates output when they change.

Workbench preview mode MUST:

- run in watch mode for a selected target (HTML web app, ebook, PDF, etc.)
- treat all external inputs as explicit (no ambient network/time dependencies introduced by Workbench)
- provide a local preview surface (implementation may be a dev server housed under `.paperhat/`)

---

**End of Workbench Contract v0.1**
