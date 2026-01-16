Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Template Format

This specification defines the concrete artifact format(s) for Workbench templates.

This document is **Normative**.

---

## 1. Purpose

Workbench templates exist to produce a deterministic Paperhat **workspace** scaffold.

This spec exists to:

- define what a template is on disk
- define how template identity and versioning work
- define how templates compose (overlays)
- ensure template resolution produces a deterministic **File Plan**

This spec does not define the internal semantics of Codex artifacts.

---

## 2. Definitions

- **Template**: a named, versioned recipe for producing a workspace file tree.
- **Template Manifest**: the canonical metadata file that describes a template.
- **Template Overlay**: an optional template that is applied on top of a base template.
- **File Plan**: a deterministic plan describing which files will be created/updated and with what contents.

---

## 3. Template Layout (Normative)

A template MUST be a directory.

A template directory MUST contain exactly one Template Manifest file:

- `template.cdx`

All other files within the template directory are template inputs.

---

## 4. Template Manifest (Normative)

The Template Manifest MUST be valid Codex.

The manifest MUST contain:

- `id` (string) — template identifier
- `name` (string) — display name
- `version` (string)
- `description` (string)

The manifest MAY contain:

- `overlays` (array of template identifiers)
- `inputs` (object describing explicit user inputs)
- `compatibility` (object describing compatible Workbench and Kernel versions)
- `modules` (array of module scaffolds to create)
- `targets` (array of default target configurations)

Workbench MUST refuse templates that do not conform.

---

## 5. Template Identity and Versioning (Normative)

Template identity MUST be defined by the tuple:

- `name`
- `version`

Workbench MUST treat template `version` as an opaque string for selection and reporting.

Workbench MUST NOT infer template selection from ambient environment.

---

## 6. Template Resolution (Normative)

Template resolution MUST:

1. Load the base template manifest.
2. Collect all explicit user inputs (flags/answers).
3. Apply overlays (if any) in a deterministic order.
4. Produce a single **File Plan**.

Given identical inputs (template identity, template contents, explicit inputs, and versions), resolution MUST produce an identical File Plan.

Workbench MUST NOT consult ambient time, randomness, network, or environment to decide file contents.

---

## 7. Overlays (Normative)

If overlays are used, Workbench MUST apply them deterministically.

Rules:

1. Overlay order MUST be explicit and stable.
2. If two overlays propose conflicting edits to the same destination path, Workbench MUST either:
   - refuse with a diagnostic, OR
   - require an explicit override input that resolves the conflict

---

## 8. Output Requirements (Normative)

A template intended to create a workspace MUST produce a File Plan that creates, at minimum:

- `modules/`
- `.paperhat/`

See also:

- [Workbench Workspace Filesystem Contract](../workbench-workspace-filesystem-contract/)

---

## 9. Safety and Reviewability (Normative)

Workbench MUST support previewing the File Plan without applying it.

Dry-run output MUST be sufficient to review:

- which files will be created
- which files will be modified
- which files will be left untouched

Applying a File Plan MUST be safe by default.

---

**End of Workbench Template Format v0.1**
