Status: NORMATIVE
Lock State: LOCKED
Version: 0.1.1
Editor: Charles F. Munat

# Quartermaster Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Quartermaster** library.

Quartermaster is the **developer tooling and orchestration layer** for Paperhat.

It is **non-authoritative** and **non-semantic**.

[Contracts Index](../)

---

## 1. Purpose

This contract exists to:

* define Quartermaster’s role as **tooling**, not system authority
* prevent Quartermaster from acquiring semantic or runtime ownership
* formalize the boundary between **authoring semantics** and **developer ergonomics**
* ensure Quartermaster remains replaceable without invalidating Paperhat artifacts

Quartermaster exists to make Paperhat **usable**, not to define what Paperhat **means**.

---

## 2. Scope

This contract governs:

* the Quartermaster library
* its CLI, dev server, and orchestration behavior
* its interaction with the filesystem and other Paperhat libraries

This contract does **not** govern:

* the Paperhat system itself
* Codex or Gloss semantics
* pipeline phase definitions
* render target semantics
* production deployment requirements

---

## 3. Non-Authority Declaration (Normative)

Quartermaster is **not authoritative**.

Specifically:

* Quartermaster does not define semantic meaning
* Quartermaster does not define structure
* Quartermaster does not define information architecture
* Quartermaster does not define pipeline phases
* Quartermaster does not define execution semantics

Removing Quartermaster MUST NOT invalidate any authored Paperhat artifact.

Any behavior that makes Quartermaster required for correctness is a violation of this contract.

---

## 4. Relationship to Higher-Authority Documents (Normative)

Quartermaster is subordinate to, and MUST conform to:

1. **Paperhat System Contract**
2. **Paperhat Module Filesystem Assembly Specification**
3. **Relevant Library Contracts**

In the event of conflict, higher-authority documents prevail.

---

## 5. Core Responsibilities (Exclusive)

Quartermaster exclusively owns:

### 5.1 Project Scaffolding

Quartermaster MAY:

* create new Paperhat projects
* scaffold directory structures
* generate placeholder files
* apply canonical filesystem conventions

Scaffolding MUST conform to the **Module Filesystem Assembly Specification**.

Scaffolding MUST NOT introduce semantic defaults beyond what is explicitly declared in generated Codex.

---

### 5.2 Development Orchestration

Quartermaster MAY:

* watch the filesystem for changes
* trigger pipeline runs
* coordinate rebuilds and re-renders
* cache intermediate results for ergonomics

All orchestration is **convenience only**.

Quartermaster MUST NOT alter pipeline semantics.

---

### 5.3 CLI Interface

Quartermaster MAY provide a CLI that includes commands such as:

* project creation
* validation
* build
* render
* watch
* format
* lint

CLI commands:

* are optional
* are not part of the Paperhat specification
* MUST map to documented pipeline behavior
* MUST NOT introduce undocumented side effects

---

### 5.4 Development Server

Quartermaster MAY provide a development server to:

* host rendered outputs
* refresh outputs on change
* preview targets (HTML, PDF, audio, etc.)

The development server:

* is not a runtime
* is not authoritative
* is not required for correctness
* MUST NOT introduce behavior unavailable in non-server contexts

---

## 6. What Quartermaster Does NOT Own (Normative)

Quartermaster does **not** own:

* Codex parsing or compilation
* AST, IR, or RDF generation
* triple-store IO
* SPARQL query semantics
* ViewModel shaping
* Design Policy application
* Presentation Plan generation
* rendering semantics
* target definitions
* semantic validation
* ontology constraints

Those responsibilities are owned by other components (e.g. Kernel, Architect, Warden).

---

## 7. Filesystem Interaction (Normative)

Quartermaster:

* reads the filesystem as **packaging**
* relies on reserved structural directories as defined by specification
* MUST NOT infer semantic meaning from:

  * folder names
  * directory depth
  * file ordering
  * timestamps

Quartermaster MUST treat the filesystem as **input**, not authority.

---

## 8. Determinism and Purity (Normative)

Quartermaster MAY invoke impure operations (IO, watching, serving).

Quartermaster MUST NOT:

* introduce non-determinism into pure pipeline phases
* cache results in a way that alters correctness
* mask semantic errors

All semantic determinism is owned by higher-authority libraries.

---

## 9. Extensibility and Replacement (Normative)

Quartermaster MUST be replaceable.

It MUST be possible to:

* implement alternative tooling
* invoke Paperhat libraries directly
* integrate Paperhat into other systems
* run pipelines without Quartermaster

No Paperhat specification may assume Quartermaster’s presence.

---

## 10. Compliance and Misuse

A Quartermaster implementation is **non-compliant** if it:

* embeds semantic meaning
* redefines pipeline phases
* imposes runtime semantics
* requires itself for correctness
* diverges from filesystem specification

Compliance is measured against **behavior**, not feature set.

---

## 11. Change Control

This document is **LOCKED**.

Rationale (v0.1.1): Remove previous library naming that could misstate authority ownership.

Changes require:

* an explicit version increment
* documented rationale
* review against the System Contract and dependent specifications

---

## 12. Summary

Quartermaster is:

* developer tooling
* orchestration and ergonomics
* optional and replaceable
* explicitly non-authoritative

Quartermaster serves the Paperhat system.
The Paperhat system does not serve Quartermaster.

---

**End of Quartermaster Library Contract v0.1.1**
