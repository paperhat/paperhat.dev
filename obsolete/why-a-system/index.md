# Why Paperhat Is a System (Not a Framework)

This document explains **why Paperhat is classified as a system rather than a framework**, and why that distinction is intentional and important.

It exists to prevent recurring confusion and incorrect assumptions.

---

## The Question

Paperhat includes:

* languages (Codex, Gloss)
* a deterministic processing pipeline
* multiple bounded libraries
* developer tooling (CLI, scaffolding, watchers, servers)
* build, lint, and format tasks

Given that, it is reasonable to ask:

> *Why is this not a framework?*

The answer depends on **what defines a framework**, not on surface features like tooling.

---

## The Defining Difference

The decisive distinction is this:

> **A framework imposes an execution model.
> A system defines meaning, contracts, and transformations.**

Tooling is not the differentiator.
**Control and authority are.**

---

## What a Framework Is

A framework:

* owns **runtime control flow**
* defines a **lifecycle** you must participate in
* provides **hooks, callbacks, or extension points**
* assumes a **canonical execution environment**
* treats authored material as subordinate to execution

In a framework:

* your work *runs inside* the framework
* structure is shaped by runtime needs
* behavior is primary
* meaning is often implicit or emergent

Frameworks answer:

> **“How does this application run?”**

---

## What a System Is

A system:

* defines **meaning, structure, and invariants**
* is governed by **specifications and contracts**
* separates **authoring, planning, and realization**
* does **not require execution** to be meaningful
* allows multiple independent implementations
* treats execution as **optional and external**

In a system:

* authored artifacts are authoritative
* execution is an interpretation, not the source of truth
* behavior is derived, not embedded
* meaning is explicit and inspectable

Systems answer:

> **“What exists, what does it mean, and what must be true?”**

---

## Why Paperhat Is a System

Paperhat is a system because:

* **Codex and Gloss are languages**, not APIs
* meaning is authored **as data**
* presentation is **planned**, not embedded
* rendering is **pure realization**
* the pipeline is **specified**, not implicit
* there is **no required runtime**
* authoritative behavior is documented, not encoded

Paperhat artifacts remain valid and meaningful:

* without a server
* without a CLI
* without a dev environment
* without execution

That is incompatible with a framework classification.

---

## The Role of Tooling (Workbench)

Paperhat includes tooling such as **Workbench**, which provides:

* project scaffolding
* file watching
* pipeline orchestration
* target execution
* development servers
* build and formatting tasks

This tooling exists for **ergonomics**, not authority.

Critically:

* Workbench does **not define meaning**
* Workbench does **not define structure**
* Workbench does **not define lifecycle semantics**
* Workbench does **not own execution**
* Workbench can be replaced without affecting Paperhat

Paperhat remains intact if Workbench is removed.

That alone disqualifies “framework”.

---

## A Useful Analogy

Paperhat relates to its tooling the way:

* SQL relates to database clients
* TeX relates to build tools
* RDF relates to triple-store CLIs
* Unicode relates to rendering engines

These ecosystems have:

* servers
* CLIs
* watchers
* build pipelines

Yet they are **systems**, not frameworks.

The presence of tooling does not redefine the core.

---

## Why the Distinction Matters

Calling Paperhat a framework would imply:

* a required runtime
* implicit lifecycle behavior
* component-based execution
* routing or control flow semantics
* behavior-first design

Those implications are **incorrect** and would lead to:

* wrong implementations
* wrong tooling assumptions
* wrong AI-generated output
* pressure to violate locked contracts

The classification is not cosmetic.
It protects the architecture.

---

## The Correct Classification

The correct and stable description is:

> **Paperhat is a semantic authoring and processing system,
> consisting of languages, specifications, bounded libraries,
> and optional tooling for development and realization.**

Tooling serves the system.
The system does not serve tooling.

---

## Summary

* Frameworks impose execution
* Systems define meaning and constraints
* Paperhat defines meaning, not runtime
* Tooling is optional and replaceable
* Therefore, Paperhat is a **system**

This distinction is intentional and should be treated as settled.

---

**End of document**
