Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# `paperhat check` Contract

This specification defines the required behavior of `paperhat check`.

This document is **Normative**.

---

## 1. Purpose

`paperhat check` exists to validate that inputs and on-disk state satisfy the minimum requirements needed to safely invoke Kernel and Workbench operations.

This spec exists to:

- define the minimum checks Workbench MUST perform
- define required diagnostic behavior
- establish refusal semantics (fail fast, do not partially proceed)

---

## 2. Scope

This specification governs:

- workspace root validation
- filesystem contract validation
- target selection input validation
- preflight checks for deterministic/safe execution

This specification does not govern Kernel internals.

---

## 3. Inputs (Normative)

`paperhat check` MUST accept inputs sufficient to:

- select a workspace root (explicit path or current working directory)
- optionally select a target (when checking for dev/build readiness)

This spec does not mandate flag names.

---

## 4. Workspace Root Detection (Hard)

`paperhat check` MUST locate a workspace root.

A directory is a valid workspace root for Workbench if it contains:

- `modules/`
- `.paperhat/`

If either directory is missing, Workbench MUST fail with a diagnostic.

---

## 5. Filesystem Contract Validation (Hard)

`paperhat check` MUST validate the Workbench Workspace Filesystem Contract.

At minimum:

1. `modules/` MUST exist and MUST be treated as the only authoring root.
2. `.paperhat/` MUST exist and MUST be treated as a reserved namespace.
3. Workbench MUST NOT treat `.paperhat/` as an authoring module root.

See also:

- [Workbench Workspace Filesystem Contract](../workbench-workspace-filesystem-contract/)

---

## 6. Target Selection Validation (Normative)

If `paperhat check` is invoked in a mode that requires a target, then:

1. Target selection MUST be explicit.
2. Workbench MUST refuse ambiguous or missing target selection.
3. Workbench MUST NOT silently change targets based on environment.

See also:

- [Workbench Dev Watch and Targets](../workbench-dev-watch-and-targets/)

---

## 7. Safety and Hygiene (Normative)

If `paperhat check` is invoked as a prerequisite for an operation that would modify many files, Workbench MUST ensure that:

- a dry-run mode is available for preview
- conflicts that would overwrite unexpected existing files are detected

On conflict, Workbench MUST either:

- refuse with a diagnostic, OR
- require an explicit override flag

See also:

- [Workbench Templates and File Plans](../workbench-templates-and-file-plans/)

---

## 8. Diagnostics Contract (Hard)

When `paperhat check` fails, Workbench MUST provide diagnostics that, at minimum:

- identify the workspace root that was checked
- identify each failed rule
- provide a human-readable explanation for each failure

Workbench MUST prefer refusal with diagnostics over partial execution.

---

**End of `paperhat check` Contract v0.1**
