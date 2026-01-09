# Paperhat Semantic Authoring System

This repository publishes the **canonical system documentation** for **Paperhat**.

Paperhat is a **semantic authoring and processing system** for expressing meaning, structure, and intent independently of runtime, presentation, or delivery target.

This site exists to define:

* what Paperhat **is**
* what compliant systems **must do**
* how authority, contracts, and specifications are structured

It is a reference repository.

---

## What Paperhat Is

**Paperhat is a semantic system**, not an application framework.

It provides:

* a declarative semantic language (**Codex**)
* an inline semantic span-binding language (**Gloss**)
* a set of strictly bounded libraries with defined responsibilities
* a deterministic, inspectable processing pipeline
* a contract-driven architecture for composition and reasoning

Paperhat enables content and systems to be authored once and realized across many targets, including (but not limited to):

* web
* print
* ebooks
* audio and voice
* data export
* knowledge graphs

---

## What Paperhat Is Not

Paperhat is **not**:

* a web framework
* a UI toolkit
* a CMS
* a static site generator
* a templating system
* a runtime environment
* a programming language

Those concerns are intentionally external.

---

## Core Principles

Paperhat is governed by a small number of non-negotiable principles:

* **Meaning is data**
* **Presentation is planned, not embedded**
* **Structure is separate from prose**
* **Semantics precede rendering**
* **Pipelines are explicit**
* **Purity and IO are strictly separated**
* **Everything authoritative is documented**

These principles are enforced through contracts, not convention.

---

## System Structure

Paperhat is composed of:

* **Languages**

  * Codex — declarative semantic authoring
  * Gloss — inline semantic span binding
* **Libraries**

  * Each library owns a single, explicit responsibility
  * Boundaries are contractual and enforced
* **Modules**

  * Semantic assemblies of heterogeneous artifacts
  * The primary unit of composition and reasoning
* **Pipeline**

  * Deterministic compilation, storage, shaping, planning, and rendering

All structure and behavior is defined declaratively.

---

## Documentation Structure

This repository is organized into several top-level areas, including:

* formal specifications
* system and library contracts
* examples
* notes and rationale
* scope and status material

Documents that define required behavior are marked **Normative**.
Documents marked **LOCKED** are authoritative and stable.

Non-normative material is explicitly labeled.

---

## Governance

Paperhat documentation is maintained under a **formal governance model**.

* Authority is explicit and ordered
* Normative documents are binding
* LOCKED documents change only through versioned revision
* Implementations are independent works

See **`GOVERNANCE.md`** for governance rules and authority order.

---

## Relationship to Implementations

This repository defines **intent, architecture, semantics, and invariants**.

It does **not** contain:

* reference implementations
* tooling
* runtimes
* deployment systems

Software implementations may exist elsewhere and are licensed independently.

---

## Licensing and Copyright

All documentation in this repository is licensed under the
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

The license applies to **textual, diagrammatic, and illustrative content only**.

No rights are granted to:

* project, language, or specification names
* trademarks or logos
* software implementations

See:

* **`LICENSE.md`**
* **`COPYRIGHT.md`**

---

## Status

Paperhat is under active development.

The presence of material in this repository establishes **architectural intent and authority**, not finality.

---

*Clarity, determinism, and semantic correctness take precedence over convenience.*
