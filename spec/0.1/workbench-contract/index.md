Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Contract

This specification defines what the Paperhat **Workbench** is and what it MUST do.

This document is **Normative**.

---

## 1. Purpose

Workbench exists to provide a deterministic, contract-driven way to:

- create new Paperhat applications (filesystem scaffold)
- generate authoring boilerplate (Concepts, Traits, Assemblies, Views, etc.)
- run Paperhat Kernel builds and target realization in **dev/watch** mode with local preview

---

## 2. Authority and Boundaries (Normative)

Workbench MUST NOT redefine Paperhat semantics.

- **Kernel owns** semantic compilation, validation, and deterministic planning.
- **Workbench owns** scaffolding, generators, and developer-facing orchestration.

Workbench MUST treat Kernel as the semantic authority.

---

## 3. Filesystem Contract (Normative)

A Paperhat workspace operated on by Workbench MUST have, at minimum:

- `.paperhat/` — reserved for Workbench configuration and dev-mode runtime artifacts
- `modules/` — the root for authored modules

Rules:

1. Workbench MUST create `.paperhat/` and `modules/` during `paperhat new`.
2. Workbench MUST NOT place authored modules outside `modules/`.
3. `.paperhat/` is a reserved namespace; Workbench MUST NOT treat it as authored module content.

Note (Normative): The Paperhat workspace root specification permits `.paperhat/` to be absent in general. Workbench is allowed to impose a stronger requirement for workspaces it manages.

See also:

- [Workspace Filesystem Root](../workspace-filesystem-root/)
- [Module Filesystem Assembly](../module-filesystem-assembly/)

---

## 4. Determinism and Idempotency (Normative)

Workbench MUST be deterministic and retry-safe.

- Given identical inputs (template, answers/flags, versions), Workbench MUST generate identical file trees.
- Generators MUST be idempotent: re-running the same generation with the same inputs MUST NOT drift or corrupt state.
- All variability MUST come from explicit inputs. Workbench MUST NOT consult ambient time/randomness to decide file contents.

---

## 5. CLI Surface (Normative)

Workbench MUST provide a CLI with commands sufficient to cover:

- `paperhat new <name> ...` — create a new Paperhat workspace from a named template
- `paperhat gen <artifact> ...` — generate authoring boilerplate (Concept, Trait, Assembly, View, etc.)
- `paperhat dev --target <target> ...` — run Kernel builds in watch mode and serve a preview
- `paperhat build --target <target> ...` — produce target outputs deterministically
- `paperhat check ...` — validate filesystem contract and inputs prior to running operations

This spec does not mandate flag names or UX beyond the required capability.

---

## 6. Templates (Normative)

Workbench MUST support multiple templates (for example: "blog", "recipes", etc.).

A template resolution MUST produce a **file plan** that can be:

- previewed (dry-run)
- applied deterministically
- validated against a filesystem contract

---

## 7. Dev Mode (Normative)

Workbench dev mode MUST:

- run in watch mode for a selected target (HTML web app, ebook, PDF, etc.)
- treat all external inputs as explicit (no ambient network/time dependencies introduced by Workbench)
- provide a local preview surface (implementation may be a dev server housed under `.paperhat/`)

---

**End of Workbench Contract v0.1**
