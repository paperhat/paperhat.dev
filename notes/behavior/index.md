# Codex, Gloss, Workshop, and Behavior Integration Model

## Purpose

This document defines how **Codex**, **Gloss**, **Behavior**, and the **Paperhat Workshop Semantic Authoring System** integrate into a single deterministic authoring, storage, validation, and rendering pipeline.

It establishes clear boundaries of responsibility, formal pipeline stages, the role of schemas in controlling data, projection, semantic composition, adaptive realization, and the normative role of **Behavior** in validation and derivation.

---

## Core Principles

The system is designed around the following invariants:

* **Schema authority**: All meaning, validity, identity, and behavior are schema-defined.
* **Closed-world semantics**: Nothing is inferred from omission.
* **Determinism**: Identical inputs produce identical outputs at every stage.
* **Strict separation of concerns**: Data, behavior, projection, composition, and realization are isolated.
* **Target independence**: No renderer assumptions are encoded upstream.
* **Lossless preservation**: Authored meaning, behavior, and narrative text are never discarded.

---

## Roles of the Core Languages

### Codex

Codex is the **authoritative semantic authoring language**.

It is used to:

* Define schemas (meta and domain)
* Define **ValueShape Concepts** and built-in value semantics
* Author structured semantic data
* Define **Behavior programs** (Constraint and Derivation)
* Express semantic composition artifacts
* Produce canonical semantic representations (Semantic IR and RDF)

Codex is responsible for:

* Parsing
* Canonicalization
* Schema loading
* Semantic validation
* Behavior attachment to ValueShapes
* Deterministic IR and RDF generation

Codex **does not**:

* Perform inference
* Interpret narrative text
* Parse or resolve Gloss
* Execute rendering or layout
* Apply target-specific realization

---

### Gloss

Gloss is an **inline semantic span-binding language** embedded inside Codex `Content`.

Gloss:

* Binds semantic meaning to spans of free text
* References Concepts by identity (`@id`) or lookup (`~key`)
* Is preserved verbatim by Codex
* Is resolved only by downstream consumers

Gloss **never**:

* Affects Codex validity
* Introduces structure
* Influences schema validation or Behavior evaluation
* Prescribes presentation

Gloss resolution occurs **after semantic meaning and behavior semantics exist**, not during Codex parsing.

---

## ValueShapes and Behavior

### ValueShape Concepts

Codex defines **ValueShape Concepts** as first-class schema constructs.

A ValueShape Concept represents the complete semantic definition of a value, including:

* structure
* validity constraints
* derivation semantics

ValueShapes include:

* built-in primitive and structural value forms
* parameterized value forms (e.g. collections)
* record values
* entity node values (EntityShapes)

Only ValueShape Concepts may carry Behavior.

Traits:

* reference exactly one ValueShape Concept
* do not define Behavior
* do not define validity or derivation semantics

---

## Behavior

Behavior is a **declarative semantic expression language** authored in Codex and governed by schemas.

Behavior programs are:

* **Pure** (no side effects)
* **Deterministic**
* **Runtime-neutral**
* **Total**: evaluation never throws; it yields either a valid result or diagnostics

Behavior provides:

* Typed value computation aligned with Codex values (including `<Absent/>`)
* Precisely defined equality, ordering, and comparison semantics
* Deterministic diagnostics (stable codes, ordering, and locations)

Behavior semantics are authoritative and shared across:

* Triple store validation and rule execution
* Server-side validation
* Browser/runtime validation
* Form validation and computed fields
* Semantic composition
* Downstream realization

---

## Constraint vs Derivation Behavior

Behavior is divided into two **non-overlapping, mandatory roles**.

### Constraint Behavior

Constraint Behavior answers:

> “Is this value valid under the schema?”

Characteristics:

* Produces a validation judgment
* Does not create new values or RDF facts
* Is part of schema validity
* Powers authoritative correctness and form validation
* Is evaluated solely over the value and its internal structure

Constraint Behavior MUST lower to **SHACL Core constraints** and/or **SHACL-SPARQL constraints** in the triple store.

---

### Derivation Behavior

Derivation Behavior answers:

> “Given a value, compute another value or fact.”

Characteristics:

* Produces derived values and/or derived RDF facts
* Remains pure and deterministic
* Does not affect schema validity unless explicitly paired with Constraint Behavior

Each Derivation Behavior MUST declare:

* an **output ValueShape**
* a **derivation class**:

  * **ephemeral** (used only for composition and rendering)
  * **materialize** (lowered to RDF triples)
* an integer **derivation phase**

Derivation Behavior MUST lower to **SHACL Rules** or equivalent deterministic SHACL-SPARQL rule constructs.

---

## EntityShape ValueShapes

Codex defines **EntityShape** as a ValueShape category representing the value semantics of entity nodes.

EntityShape ValueShapes:

* define node structure
* carry cross-trait Constraint Behavior
* carry entity-level Derivation Behavior

This preserves the invariant that **all Behavior attaches only to ValueShapes**.

---

## Workshop as the Integrating System

The **Paperhat Workshop Semantic Authoring System** is the primary consumer of Codex, Behavior, and Gloss.

Workshop:

* Owns the semantic execution pipeline
* Executes SHACL validation and rules
* Enforces derivation phase ordering and fixpoint semantics
* Owns SPARQL querying
* Owns adaptive semantic composition
* Emits Codex artifacts to renderers

Renderers never query the triple store, never execute Behavior, and never perform SPARQL.

---

## Schema Families and Their Roles

Workshop operates over multiple **schema families**, each with a distinct responsibility.

### 1. Data Schemas

Data schemas define **domain meaning and validity**.

They specify:

* Concepts and Traits
* ValueShape references
* Constraint Behavior on ValueShapes and EntityShapes
* Canonical RDF shapes

Characteristics:

* Broad, expressive, high-fidelity
* SHACL-validated
* Behavior-governed
* Stored fully in the triple store
* Optimized for correctness and completeness, not display

---

### 2. View Schemas

View schemas define **projection and selection**.

They specify:

* Which Concepts are selected
* Which Traits are exposed
* Which Derivation Behaviors are applied
* How data is grouped into semantic views

View schemas:

* Do not mutate underlying data
* Do not prescribe layout
* Produce deterministic semantic projections

---

### 3. DesignPolicy Schemas

DesignPolicy defines **semantic composition rules**.

It controls:

* Ordering
* Grouping
* Priority
* Containment
* Fallbacks
* Overflow and collapse rules

DesignPolicy may reference derived values but does not introduce new derivation semantics.

---

### 4. DesignIntent Schemas

DesignIntent defines **semantic intent and emphasis**, not styling.

It expresses:

* Relative importance
* Hierarchy
* Emphasis
* Affordance classes

DesignIntent may reference derived values and classifications, but never presentation metrics.

---

### 5. Assembly Schemas

Assembly schemas define **structural composition**.

They organize:

* Collections
* Sequences
* Hierarchies
* Publications

Assembly governs containment and order, not behavior execution.

---

## The Semantic Composition Artifact

Between stored data and rendering, Workshop produces a **semantic composition artifact**.

This artifact:

* Is authored in Codex
* Is schema- and behavior-governed
* Is deterministic
* Is target-independent

Acceptable names include:

* **Composition Graph**
* **Semantic Composition Graph**
* **Presentation Graph**
* **Realization Graph**

This artifact is the *sole* input to renderers.

---

## End-to-End Pipeline

### Authoring and Storage

```
data / view / policy / intent / assembly schemas
        ↓
Codex parse
        ↓
AST
        ↓
Semantic IR
        ↓
Canonical RDF (Turtle)
        ↓
Triple Store
(SHACL constraints, SHACL rules, SHACL-SPARQL)
```

---

### Rendering

```
SPARQL (Workshop-owned)
        ↓
Semantic Composition Graph (Codex)
        ↓
Codex parse (IR / JSON)
        ↓
Derivation Behavior (ephemeral values)
        ↓
Gloss resolution
        ↓
Target renderer (HTML, PDF, audio, etc.)
        ↓
Rendered output
```

Renderers:

* Never run SPARQL
* Never interpret schemas
* Never execute Behavior
* Only realize meaning already composed

---

## Gloss Resolution Phase

Gloss is resolved:

* After Constraint Behavior validation
* After materialized Derivation Behavior execution
* After View selection and DesignPolicy application
* Before target-specific realization

Gloss diagnostics are isolated from Codex and Behavior diagnostics.

---

## Diagnostics Stratification

Diagnostics are strictly layered:

1. Codex well-formedness
2. Codex semantic validation (schemas + Constraint Behavior)
3. Derivation Behavior diagnostics
4. Gloss parsing and resolution
5. Semantic composition and policy feasibility
6. Target realization constraints

Failures at one layer never contaminate another.

---

## SPARQL Ownership

SPARQL:

* Is part of the Workshop pipeline
* Is not exposed to renderers
* May be schema-defined, hardcoded, or both

Schema-defined SPARQL is preferred where determinism, governance, and certification are required.

---

## Summary

* Codex defines **what exists**
* ValueShapes define **what values mean**
* Behavior defines **what is valid and what is computed**
* Gloss annotates **what narrative spans mean**
* Workshop composes **what is shown**
* Renderers decide **how it appears**

Each stage is isolated, deterministic, schema-governed, and normatively specified.

This separation is intentional, required, and foundational.
