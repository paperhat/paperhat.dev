Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Kernel Architecture Specification

This specification defines the responsibilities, boundaries, and deterministic execution model of the **Paperhat Kernel**.

The Kernel is the semantic authority for Paperhat in the sense that it validates, enforces, and deterministically derives artifacts from authored meaning; it does **not** invent or infer meaning.

This document is **Normative**.

---

## 1. Scope

This specification governs:

* Kernel responsibilities and non-responsibilities
* Kernel inputs and outputs
* deterministic execution requirements
* dialect selection and ontology pack loading rules

This specification does **not** govern:

* any particular programming language or runtime
* any particular storage backend or network protocol
* any particular developer tooling UX (CLI flag names, editor integrations)

---

## 2. Kernel Responsibilities (Normative)

The Kernel MUST be responsible for:

1. **Compilation** of authored Codex artifacts into canonical internal representations.
2. **Dialect selection** based on explicit artifact role (for example: Data vs View vs DesignIntent vs DesignPolicy).
3. **Validation** against:

   * the relevant dialect ontology expressed as triples, and
   * declarative constraints (for example SHACL or equivalent constraint systems).
4. **Assembly** of Modules from the filesystem according to the Module Filesystem Assembly specification.
5. **Deterministic planning**, including:

   * View Graph application producing a ViewModel,
   * DesignIntent set selection (per Design Policy),
   * Intent resolution (axis-wise merge with precedence rules), and
   * Design Policy application (structural transforms) producing a Presentation Plan.
6. Emission of **diagnostics** sufficient for author correction and tool integration.

---

## 3. Kernel Non-Responsibilities (Normative)

The Kernel MUST NOT:

* infer meaning from filesystem coincidence beyond what Paperhat specifications define
* consult ambient time, randomness, or network access to decide semantic results
* own developer scaffolding, generators, file watching, or preview servers (these are Shell responsibilities)
* require any particular persistence backend (graph store adapters are separately conformable)

---

## 4. Inputs and Outputs (Normative)

### 4.1 Inputs

Kernel inputs MUST be explicit.

At minimum, a Kernel invocation MUST be able to accept:

* a workspace root (or equivalent assembly root)
* an explicit ordered set of ontology pack roots (possibly empty)
* a target context (when producing target-aware derived artifacts such as Presentation Plans)
* context signals (typed, symbolic inputs for adaptive planning)

Target context and context signals are distinct inputs: the former identifies the realization domain, while the latter supplies typed adaptive conditions.

### 4.2 Outputs

Kernel outputs MAY include:

* semantic graphs (for example RDF)
* a ViewModel
* a Presentation Plan
* diagnostics

No Kernel output is itself semantic truth unless it is explicitly defined by specification as semantic truth.

---

## 5. Determinism (Normative)

Given identical explicit inputs (including identical ontology packs and their ordered roots), Kernel MUST produce identical semantic results.

Rules:

1. Kernel MUST NOT use ambient time, randomness, or network access to decide results.
2. Kernel MUST NOT use ambient filesystem iteration order.
3. If Kernel writes JSON outputs, it MUST use a canonical serialization policy to avoid spurious diffs.

---

## 6. Dialects and Ontologies (Normative)

Paperhat uses Codex for multiple distinct purposes. Each such purpose is a **dialect**.

Definitions:

* **Dialect:** A Codex authoring context with its own authorized Concepts, Traits, and structure, governed by a dialect ontology and constraints.
* **Dialect ontology:** A canonical semantic graph (triples) plus declarative constraints that define what is valid for a dialect.

Rules:

1. Dialect meaning MUST be defined by an ontology-as-triples plus declarative constraints.
2. Dialect selection MUST be deterministic and MUST be based on explicit artifact role and/or explicit configuration.
3. Shell tooling MUST NOT guess dialects or reinterpret authored meaning.

Common dialects (non-exhaustive):

* **Data dialect** — domain facts intended to compile to the Domain Graph.
* **View dialect** — view definitions intended to compile to the View Graph.
* **DesignIntent dialect** — intent axis assignments intended to be selected by DesignPolicy and resolved into Presentation Plans.
* **DesignPolicy dialect** — declarative planning policy (intent selection, context conditions, structural transforms) intended to produce Presentation Plans.
* **Behavior dialect** — behavior expressions intended to compile to Behavior Programs.
* **Schema Dialect** — meta-dialect used to author dialect ontologies themselves.

---

## 7. Schema Dialect (Normative)

Dialect ontologies MUST be authored in Codex.

The **Schema Dialect** is the meta-dialect used to author dialect ontologies.

Rules:

1. Kernel MUST own the Schema Dialect.
2. Kernel MUST ship with a minimal built-in bootstrap for the Schema Dialect sufficient to validate and compile Schema Dialect documents deterministically.
3. All other dialect ontologies and domain schemas MUST be loadable inputs and MUST NOT require a Kernel rebuild to update.

---

## 8. Ontology Packs (Normative)

An **ontology pack** is a versioned directory of Codex artifacts authored in the Schema Dialect.

Ontology packs exist to define and distribute dialect ontologies and domain schemas without baking them into the Kernel.

### 8.1 Pack Identity (Normative)

Each ontology pack MUST declare, as authored Codex:

* a stable pack identifier
* an explicit pack version
* the dialect ontology(ies) and/or schema(s) it provides
* any dependencies on other packs (by identifier and version)

### 8.2 Pack Roots (Normative)

Kernel MUST treat ontology packs as explicit inputs.

Rules:

1. Kernel MUST accept an explicit ordered list of pack roots (directories) as input.
2. Kernel MUST NOT rely on ambient filesystem iteration order to determine which packs are loaded.
3. If a pack root is present on disk but not provided as an explicit input, it MUST NOT affect outputs.

### 8.3 Deterministic Resolution (Normative)

Given identical explicit inputs, including the same ordered pack roots, Kernel MUST resolve the same pack set.

Rules:

1. Pack discovery within a root MUST use a deterministic ordering (for example: lexicographic path order).
2. If multiple packs provide the same pack identifier and version, Kernel MUST fail with a diagnostic.
3. If multiple versions of the same pack identifier are present, selection MUST be explicit; Kernel MUST NOT choose “latest” implicitly.
4. Dependency resolution MUST be deterministic and MUST fail on missing or incompatible dependencies.

---

## 9. Compiled Projections and Caching (Normative)

Kernel MAY compile loaded ontology packs into a canonical internal form for efficient validation and compilation.

Kernel MAY persist such compiled projections as caches.

Rules:

1. Compiled projections are non-authoritative and MUST be fully regenerable from authored Codex.
2. Cache keys MUST be derived from explicit inputs (including pack contents and selected pack set) and MUST be stable across machines.
3. Presence or absence of caches MUST NOT change semantic results.

---

## 10. Relationship to Shell Tooling (Normative)

A Shell (such as Workbench) MAY provide:

* workspace scaffolding and generators
* file watching and incremental rebuild orchestration
* running the Kernel and capturing diagnostics
* invoking renderers and writing outputs
* providing a local preview surface

Shell tooling MUST treat the Kernel as the semantic authority.

Shell tooling MUST NOT perform its own semantic compilation.

---

## 11. Relationship to Other Specifications (Normative)

This specification MUST be read in conjunction with:

* [Design Intent Definition Specification](../design-intent-definition/)
* [Design Policy Definition Specification](../design-policy-definition/)
* [Presentation Plan Definition Specification](../presentation-plan-definition/)
* [View Definition Specification](../view-definition/)
* [View Composition Specification](../view-composition-slots-fills-and-use/)

---

**End of Paperhat Kernel Architecture Specification v0.1**
(Normative)
