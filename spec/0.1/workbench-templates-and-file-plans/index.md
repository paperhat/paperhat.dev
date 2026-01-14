Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Workbench Templates and File Plans

This specification defines Workbench’s template system at the level necessary to guarantee determinism, reviewability, and idempotency.

This document is **Normative**.

---

## 1. Definitions

- **Template**: a named, versioned recipe for producing a workspace file tree.
- **File Plan**: a deterministic plan that describes which files will be created/updated and with what contents.

---

## 2. Deterministic Resolution (Normative)

Given identical inputs (template identity, template content, explicit user inputs, and versions), template resolution MUST produce an identical File Plan.

Workbench MUST NOT consult ambient time, randomness, network, or environment to decide file contents.

---

## 3. Dry Run (Normative)

Workbench MUST support previewing a File Plan without applying it.

A dry run MUST be sufficient for review by showing:

- which files will be created
- which files will be modified
- which files will be left untouched

This spec does not mandate a particular diff format.

---

## 4. Apply (Normative)

Applying a File Plan MUST be:

- deterministic
- idempotent
- safe by default

If application encounters unexpected existing files that would be overwritten, Workbench MUST either:

- refuse with a diagnostic, OR
- require an explicit override flag

---

**End of Workbench Templates and File Plans v0.1**
