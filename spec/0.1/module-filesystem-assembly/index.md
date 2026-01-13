Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Module Filesystem Assembly Specification

This specification defines the canonical filesystem layout for Paperhat applications authored in Codex. It governs how Modules are represented on disk, and how Data, Views, Design Policy, and Assets are organized for deterministic compilation and reasoning.

---

## 1. Purpose

This specification exists to:

* define the canonical **Module-on-disk** structure for Paperhat projects
* separate **packaging and containment** from **semantic meaning**
* prevent implicit semantics from leaking through filesystem paths
* support large-scale modules (including thousands of artifacts) without naming files
* establish stable conventions that tooling and automated systems can rely upon

Filesystem layout is a **normative convention** in Paperhat.

---

## 2. Scope

This specification governs:

* Paperhat projects that store authored content under a top-level `modules/` directory
* the on-disk representation of Paperhat **Modules** and their internal assemblies
* reserved structural directories within a Module root
* the role-based Codex files used for Data, Views, and Design Policy

This specification does **not** govern:

* any particular render target
* URL routing or information architecture
* semantic meaning of domain Concepts (owned by schemas)
* tooling implementation details, except where tooling must rely on this layout

---

## 3. Definitions

* **Module (semantic):** A Codex `<Module>` Concept that assembles heterogeneous artifacts.
* **Module root (filesystem):** A directory representing one Module on disk.
* **Role file:** A `.cdx` file whose name indicates artifact role, not identity.
* **Data Codex:** Codex that asserts semantic facts intended to compile to triples.
* **View Codex:** Codex that defines projections and information architecture, producing ViewModels.
* **DesignPolicy Codex:** Codex that defines declarative planning policy, producing Presentation Plans.
* **Assets:** Non-Codex files not parsed by Kernel.

---

## 4. Top-Level Project Layout (Normative)

A Paperhat project MUST contain a top-level directory:

* `modules/`

The `modules/` directory is the canonical root for authored Modules and replaces any `src/`-style code layout.

---

## 5. Module Root Naming (Normative)

Within `modules/`:

* Each direct child directory that is a Module root MUST be named in **PascalCase**.
* The directory name is the Module’s **filesystem identity**.

Example:

```
modules/
  Recipe/
  MealPlan/
```

Module directory names MUST NOT be interpreted as URL paths or target routing.

---

## 6. Required Module File (Normative)

Every Module root MUST contain:

* `module.cdx`

`module.cdx`:

* defines the Module as a Codex artifact
* establishes the semantic assembly boundary
* declares any Module-level defaults authorized by schema

No other Codex file is required at the Module root.

---

### 6.1 Module Role Declarations (Normative)

A Module MAY declare the following **role marker Concepts** inside `module.cdx`:

* `<Data />`
* `<Views />`
* `<DesignPolicies />`

These Concepts:

* declare which **artifact classes** are present in the Module
* provide a location for **role-specific defaults** (for example `idBase`)
* are **declarative markers**, not structural containers

The <Data />, <Views />, and <DesignPolicies /> Concepts in module.cdx declare role availability and defaults only; they do not wrap or contain artifacts and do not imply structural hierarchy.

Role marker Concepts:

* MUST NOT be interpreted as wrapping, containing, or scoping artifacts
* MUST NOT imply filesystem hierarchy
* MUST NOT replace or duplicate the function of `data/`, `views/`, or `design-policies/` directories

Note (Normative): Role marker Concepts indicate the **dialect** of authored artifacts that will be assembled from the filesystem (Data dialect, View dialect, DesignPolicy dialect). Dialect selection is performed by Kernel based on artifact role and location.

Artifact discovery and assembly remain **filesystem-based**, as defined in §§9–11.

Role marker Concepts exist solely to:

* declare participation
* declare defaults
* make Module intent explicit and machine-inspectable

---

## 7. Reserved Structural Directories (Normative)

A Module root MAY contain the following reserved structural directories:

* `data/`
* `views/`
* `design-policies/`
* `assets/`

If present, each directory has the following meaning:

* `data/` contains Data Codex artifacts only
* `views/` contains View Codex artifacts only
* `design-policies/` contains DesignPolicy Codex artifacts only
* `assets/` contains non-Codex assets only

These directory names are **structural** and have meaning only at the Module root.

---

## 8. Reserved Name Rule (Normative)

Within a Module root, the following names are reserved and MUST NOT be used for any other purpose:

* `data`
* `views`
* `design-policies`
* `assets`

This restriction applies **only** at the Module root level.

Within these directories, folder names are unrestricted unless governed by other specifications.

---

## 9. Data Assembly (Normative)

If a Module contains a `data/` directory:

* Each data artifact MUST be stored in its own directory.
* Each such directory MUST contain exactly one file:

  * `data.cdx`

Example:

```
modules/
  Recipe/
    module.cdx
    data/
      bobs-apple-pie/
        data.cdx
      bettys-birthday-cake/
        data.cdx
```

The semantic identity of a data artifact is declared **inside** `data.cdx` (via Traits such as `id`), not inferred from folder names.

Folder names under `data/` are organizational only.

---

## 10. View Assembly (Normative)

If a Module contains a `views/` directory:

* The default view for the Module MUST be located at:

  * `views/view.cdx`
* Additional view variants MUST be stored in subdirectories under `views/`.
* Each variant directory MUST contain exactly one file:

  * `view.cdx`

Example:

```
modules/
  Recipe/
    views/
      view.cdx
      card/
        view.cdx
      short/
        view.cdx
```

View Codex is the **exclusive location** for:

* information architecture
* projection and selection rules
* structural organization of domain data

Filesystem paths MUST NOT imply information architecture.

---

## 11. Design Policy Assembly (Normative)

If a Module contains a `design-policies/` directory:

* The default Design Policy MUST be located at:

  * `design-policies/design-policy.cdx`
* Additional Design Policy variants MUST be stored in subdirectories.
* Each variant directory MUST contain exactly one file:

  * `design-policy.cdx`

Example:

```
modules/
  Recipe/
    design-policies/
      design-policy.cdx
      voice/
        design-policy.cdx
```

Design Policy:

* is authored in Codex
* configures planning, not semantic meaning
* introduces no ontology facts
* is applied by Kernel as a pure phase

---

## 12. Assets (Normative)

If a Module contains an `assets/` directory:

* It MUST contain only non-Codex files.
* Assets MUST NOT be parsed as Codex and MUST NOT affect semantic truth.

Assets may include images, fonts, stylesheets, scripts, or other target-specific resources.

---

## 13. Nested Modules (Normative)

Modules MAY be nested.

A Module MAY contain additional Module roots as subdirectories, provided:

* each nested Module root is a PascalCase directory
* each contains its own `module.cdx`
* nested Modules remain independent semantic assemblies

Example:

```
modules/
  MealPlan/
    module.cdx
    Recipe/
      module.cdx
```

Nesting expresses **packaging and ownership**, not information architecture.

---

## 14. Linking and Overrides (Normative)

Data artifacts MUST NOT embed per-target information architecture.

Custom Views or Design Policies that apply to specific data artifacts MUST be expressed in:

* View Codex (under `views/`)
* DesignPolicy Codex (under `design-policies/`)

Applicability MUST be established through **explicit semantic linkage** declared in Codex content.

Filesystem coincidence MUST NOT be the sole determinant of applicability.

---

## 15. Determinism and Inference Rules (Normative)

The filesystem layout MUST support deterministic compilation.

* `module.cdx` establishes the assembly boundary.
* Artifact role is determined by file name (`data.cdx`, `view.cdx`, `design-policy.cdx`).

No tool MAY infer semantic meaning from:

* folder names under `data/`, `views/`, or `design-policies/`
* folder ordering
* filesystem timestamps

---

## 16. Documentation File Convention (Normative)

All Paperhat **documentation** (including specifications and contracts):

* uses **folder-based identity**
* stores content in `index.md`
* encodes page identity in the **folder name**, not the file name

Example:

```
spec/
  0.1/
    module-filesystem-assembly/
      index.md
```

This convention applies to documentation only and does not affect Codex artifact naming.

---

## 17. Non-Goals

This specification does not:

* define URL routing behavior
* define target-specific pipelines
* define schema-level meaning
* replace the semantic Module definition in Codex
* define tooling behavior beyond layout reliance

---

## 18. Summary

A Paperhat project:

* stores authored Modules under `modules/`
* represents Modules as PascalCase directories with `module.cdx`
* uses `<Data />`, `<Views />`, and `<DesignPolicies />` as declarative role markers
* separates concerns via reserved directories:

  * `data/` → `data.cdx`
  * `views/` → `view.cdx`
  * `design-policies/` → `design-policy.cdx`
  * `assets/` → non-Codex files
* treats filesystem structure as packaging, not meaning
* requires explicit semantic linkage for overrides
* uses folder-named documentation pages with `index.md`

---

**End of Paperhat Module Filesystem Assembly Specification v0.1**
