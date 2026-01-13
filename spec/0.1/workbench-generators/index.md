Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Generators

This specification defines Workbench generator behavior for authoring artifacts such as Concepts, Traits, Assemblies, and Views.

This document is **Normative**.

---

## 1. Scope

This spec governs:

- required generator properties (determinism, idempotency)
- minimum CLI capabilities
- filesystem placement rules for generated artifacts

It does not define the internal formats of authored semantics artifacts.

---

## 2. Determinism and Idempotency (Hard)

All generators MUST be deterministic and idempotent.

Rules:

1. Given identical explicit inputs, generator output MUST be identical.
2. Generators MUST NOT consult ambient time/randomness/network to decide output contents.
3. Re-running the same generator command with the same inputs MUST NOT produce drift.
4. If a requested artifact already exists, Workbench MUST either:
   - refuse with a diagnostic, OR
   - require an explicit override flag

---

## 3. Filesystem Placement (Hard)

Generators MUST place authored artifacts under `modules/`.

Rules:

1. Workbench MUST NOT generate authored artifacts under `.paperhat/`.
2. Workbench MUST NOT generate authored artifacts outside `modules/`.
3. Workbench MUST treat `modules/` as the only authoring root.

---

## 4. Generator CLI Surface (Normative)

Workbench MUST provide a generator command family:

- `paperhat gen <artifactKind> ...`

At minimum, Workbench MUST support artifact kinds sufficient to bootstrap a workspace:

- `concept`
- `trait`
- `assembly`
- `view`

This spec does not mandate flag names. However, Workbench MUST support explicit naming inputs such that the output path and contents are fully determined by the provided inputs.

---

## 5. Diagnostics (Normative)

When generation fails, Workbench MUST provide diagnostics that:

- identify which artifact was requested
- identify the intended destination path
- explain why generation could not proceed (e.g., conflict, invalid name, workspace contract violation)

Workbench MUST prefer refusal with diagnostics over partial generation.

---

**End of Workbench Generators v0.1**
