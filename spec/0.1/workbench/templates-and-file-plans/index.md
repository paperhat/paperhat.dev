Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Templates and File Plans Contract

---

## 1. Purpose

This specification defines Workbench’s template system at the level necessary to guarantee:

* determinism
* reviewability
* idempotency
* refusal-by-default safety

Templates exist to produce deterministic workspace scaffolds and authored boilerplate through **File Plans**.

This document is **Normative**.

---

## 2. Definitions

* **Template**: a named, versioned recipe for producing a workspace file tree.
* **File Plan**: a deterministic plan describing which files will be created/updated and with what contents.

---

## 3. Deterministic Resolution (Normative)

Given identical inputs (template identity, template content, explicit user inputs, and versions), template resolution MUST produce an identical File Plan.

Workbench MUST NOT consult ambient time, randomness, network, or environment to decide file contents.

---

## 4. Dry Run (Normative)

Workbench MUST support previewing a File Plan without applying it.

A dry run MUST be sufficient for review by showing:

* which files will be created
* which files will be modified
* which files will be left untouched

This specification does not mandate a particular diff format.

---

## 5. Apply (Normative)

Applying a File Plan MUST be:

* deterministic
* idempotent
* safe by default

If application encounters unexpected existing files that would be overwritten, Workbench MUST either:

* refuse with Diagnostics, OR
* require an explicit override

---

## 6. Generator Behavior as File Plans (Normative)

All Workbench “generators” are expressed exclusively as File Plans.

Rules:

1. Workbench MUST NOT perform ad-hoc generation writes outside of applying a File Plan.
2. Workbench MUST ensure generator output is reviewable via dry-run.
3. Re-running the same generation with identical inputs MUST NOT drift.

---

## 7. Filesystem Placement Rules (Normative)

Templates and generators MUST obey the Workbench Workspace Filesystem Contract.

Rules:

1. Workbench MUST NOT generate authored artifacts under `.paperhat/`.
2. Workbench MUST NOT generate authored artifacts outside `modules/`.
3. Workbench MUST treat `modules/` as the only authoring root.

Tool-owned artifacts MAY be written under `.paperhat/` only when explicitly specified as tool-owned.

---

## 8. Minimum Generator Capabilities (Normative)

Workbench MUST support creating boilerplate sufficient to bootstrap a workspace.

This capability MAY be provided through templates, overlays, or explicit generator commands, but MUST be expressible as File Plans.

At minimum, Workbench MUST support generating scaffolds for:

* Concept
* Trait
* Assembly
* View

This specification does not mandate flag names or UX.

---

## 9. Idempotency and Conflict Semantics (Normative)

If a requested artifact already exists, Workbench MUST either:

* refuse with Diagnostics, OR
* require an explicit override input

Workbench MUST prefer refusal over partial generation.

---

## 10. Diagnostics (Normative)

When generation (template resolution or application) cannot proceed, Workbench MUST provide Diagnostics that:

* identify the requested template/generator intent
* identify intended destination paths
* explain why the operation could not proceed (conflict, invalid inputs, contract violation)

Workbench MUST prefer refusal with Diagnostics over partial filesystem modification.

---

## 11. Reality Rule (Normative)

This specification defines templates and file plans **as they are**.

There is no legacy generator behavior.
There are no ad-hoc write modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
