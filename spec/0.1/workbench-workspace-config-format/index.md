Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Workspace Config Format

This specification defines the on-disk configuration format(s) under `.paperhat/` for a Paperhat workspace as used by Workbench.

This document is **Normative**.

---

## 1. Purpose

Workbench needs a deterministic and reviewable way to:

- configure dev/watch behavior (including a local preview surface)
- define and select targets explicitly
- persist tool-owned runtime state without contaminating authored content

This spec exists to:

- define the minimal `.paperhat/` layout for Workbench configuration
- define the canonical **compiled config** JSON format (“Config IR v0.1”)
- define the determinism and idempotency requirements for compiling config sources to Config IR

This spec does not define authored semantics content formats.

---

## 2. Non-negotiables (Normative)

1. The canonical on-disk unit is a **workspace**.
2. `modules/` is the only authoring root.
3. `.paperhat/` is a reserved tooling namespace.
4. Workbench MUST NOT treat `.paperhat/` as an authoring root.
5. All configuration compilation and application MUST be deterministic and idempotent.

See also:

- [Workbench Workspace Filesystem Contract](../workbench-workspace-filesystem-contract/)
- [Workbench Dev Watch and Targets](../workbench-dev-watch-and-targets/)

---

## 3. `.paperhat/` Layout (Normative)

A workspace MAY contain configuration under `.paperhat/`.

If Workbench uses configuration, it MUST separate **user-authored config sources** from **tool-owned runtime artifacts**.

Workbench MUST use the following directories if present:

- `.paperhat/config/` — user-authored configuration sources (inputs)
- `.paperhat/runtime/` — tool-owned runtime artifacts (outputs, caches, state)
- `.paperhat/out/` — tool-owned build outputs (by target)

Workbench MUST NOT place authored Modules under `.paperhat/`.

---

## 4. Config Sources (Normative)

Workbench MUST support configuration being authored in a Paperhat-specified format (for example Codex), and compiled into a JSON Config IR.

This spec does not mandate the source format details. However, if config sources are used, Workbench MUST treat them as explicit inputs and MUST NOT consult ambient time/randomness/network/environment to decide outputs.

Recommended (non-binding) file names:

- `.paperhat/config/config.cdx` — workspace config source
- `.paperhat/config/targets/*.cdx` — target definitions

---

## 5. Compiled Config IR v0.1 (Normative)

Workbench MUST compile config sources into a single JSON document called the **Compiled Config**.

The Compiled Config MUST be written to:

- `.paperhat/runtime/config.json`

The Compiled Config MUST be treated as tool-owned.

Users MUST NOT be required to hand-edit the Compiled Config.

---

## 6. Target IDs (Normative)

Target IDs (the keys under `targets`) MUST be stable identifiers.

For Config IR v0.1, target IDs MUST match:

- `^[a-z][a-z0-9-]*$`

Examples:

- `html`
- `pdf`
- `ebook-mobi`

---

## 7. Deterministic Compilation Contract (Normative)

Compiling configuration sources to the Compiled Config MUST be:

- deterministic
- idempotent
- retry-safe

Rules:

1. Given identical explicit inputs (config source contents, selected target(s), Workbench and Kernel versions), compilation MUST produce identical Compiled Config bytes.
2. Workbench MUST NOT consult ambient time/randomness/network/environment to decide Compiled Config contents.
3. If Workbench writes JSON, it MUST use a canonical serialization (stable key ordering and whitespace policy) to avoid spurious diffs.

---

## 8. Dev/Watch Requirements (Normative)

In dev/watch mode, Workbench MUST support:

- watching authored content under `modules/`
- re-running the appropriate steps deterministically when watched inputs change

If configuration sources under `.paperhat/config/` change, Workbench MUST either:

- recompile config and update dev/watch behavior deterministically, OR
- refuse with a diagnostic that a restart is required

---

## 9. Skipping Persistence in Dev Mode (Normative)

Workbench dev/watch MUST support a mode that disables persistence steps intended for publish/build flows.

For example, in dev/watch mode, Workbench MAY skip writing triples to a persistent graph store.

This behavior MUST be controlled by explicit configuration or explicit CLI flags.

Workbench MUST NOT infer persistence behavior from ambient environment.

---

## 10. Preview Semantics (Normative)

Targets MAY declare a preview.

If a target declares a preview, it MUST be one of:

- `none` — no preview surface
- `http` — preview is served over HTTP
- `file` — preview is a file path

If preview kind is `http` or `file`, the preview MUST include a `path`.

If any selected target uses an `http` preview, Workbench MUST provide a local preview surface.

The default host/port MAY be implementation-defined, but MUST be deterministic.

---

## 11. Diagnostics (Normative)

If config compilation fails, Workbench MUST provide diagnostics that identify:

- the workspace root
- the failing config source path(s)
- the intended output path (`.paperhat/runtime/config.json`)
- the reason compilation could not proceed

Workbench MUST prefer refusal with diagnostics over partial configuration.

---

**End of Workbench Workspace Config Format v0.1**
