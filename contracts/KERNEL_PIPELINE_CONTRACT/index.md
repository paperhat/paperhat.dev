Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.3.1  
Editor: Charles F. Munat

# Kernel Pipeline Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Kernel**.

Kernel is the **authoritative semantic processing pipeline** of the **Paperhat system**.

[Contracts Index](../)

---

## 1. Purpose (Normative)

This contract exists to:

* define Kernel’s exclusive ownership of the Paperhat processing pipeline
* enforce strict separation between **semantic truth**, **projection**, and **planning**
* guarantee determinism, inspectability, and round-trippability
* prevent epistemic contamination between authored artifact classes
* ensure that all derived artifacts are reproducible and non-authoritative

Kernel processes authored meaning.
It does not define meaning.

---

## 2. Scope

This contract governs:

* compilation of Codex (`.cdx`) artifacts
* semantic normalization and RDF emission
* interaction with the triple store (via a configured graph store adapter)
* multi-graph storage and querying
* ViewModel derivation
* Design Policy application
* rendering to targets

This contract does **not** govern:

* semantic vocabularies or meaning (Architect)
* ontology constraints (Warden)
* tooling, scaffolding, or orchestration (Quartermaster)
* application workflows or runtime behavior

---

## 3. Kernel Ownership (Exclusive)

Kernel exclusively owns the following conceptual pipeline:

1. **Compilation** — CDX → AST → IR → RDF/Turtle (pure)
2. **Storage** — RDF → triple store (IO via a configured graph store adapter)
3. **Query** — SPARQL → results (IO via a configured graph store adapter)
4. **Shaping** — results → ViewModel (pure)
5. **Planning** — ViewModel + Design Policy → Presentation Plan (pure)
6. **Rendering** — Presentation Plan → target output (pure)

No other library may redefine, bypass, or collapse these phases.

---

## 4. Artifact Classes and Epistemic Separation (Normative)

Kernel recognizes three **distinct classes of authored Codex artifacts**:

1. **Domain Data**

   * authored in `data.cdx`
   * asserts semantic truth
   * defines entities, relationships, values, and identity

2. **View Definitions**

   * authored in `view.cdx`
   * define projection, selection, grouping, ordering, and information architecture
   * do **not** assert semantic truth

3. **Design Policy**

  * authored in `design-policy.cdx`
   * defines planning and realization policy
   * does **not** assert semantic truth

These classes are **epistemically distinct** and MUST NOT be conflated.

---

## 5. Multi-Graph Storage Model (Normative)

Kernel MUST store compiled artifacts in **separate graphs**, each with its own ontology and SHACL validation.

At minimum:

* **Domain Graph**

  * populated exclusively from `data.cdx`
  * contains semantic truth

* **View Graph**

  * populated exclusively from `view.cdx`
  * contains projection and information-architecture definitions

* **Design Graph**

  * populated exclusively from `design-policy.cdx`
  * contains planning and realization policy

Graphs MUST NOT be merged.

No graph may depend on another for semantic correctness.

---

## 6. Compilation Responsibilities (Normative)

Kernel exclusively owns:

* Codex grammar and syntax
* lexical validation
* AST node definitions
* IR shape and normalization rules
* canonical formatting rules
* IR → RDF/Turtle emission

No other library may parse CDX or define an alternative CDX compiler.

---

## 7. Canonical Form and Determinism (Normative)

Kernel MUST enforce:

* a single canonical surface form for Codex documents
* deterministic AST, IR, and RDF emission for equivalent inputs
* stable identifiers and ordering for equivalent semantic inputs

Formatting is mandatory and non-optional.

---

## 8. Module Revision Atomicity (Normative)

Kernel processes **Modules atomically**.

For a given Module revision:

* all Domain, View, and Design artifacts MUST compile successfully
* all corresponding graphs MUST validate successfully
* only then may the Module revision become active

If any required artifact fails:

* **no graph is updated**
* partial ingestion is prohibited

Module revisions are all-or-nothing.

---

## 9. Provenance and Revision Identity (Normative)

For each successful Module revision, Kernel MUST establish:

* Module identifier
* Module Revision identifier
* Artifact identifiers for each source document

These identifiers are provenance metadata only and do not affect semantic meaning.

---

## 10. Source Location Policy (Normative)

Kernel MAY track line numbers, columns, and offsets **only** for:

* diagnostics
* Help generation
* tooling feedback

Source-location metadata:

* MUST NOT be stored in any graph
* MUST NOT affect semantic identity
* MUST NOT be required for round-trip reconstruction

---

## 11. Ordering and Structural Preservation (Normative)

To enable structural round-tripping, Kernel MUST emit explicit ordering metadata.

* Ordered collections MUST use an explicit ordering predicate (e.g. `cdx:orderIndex`)
* Ordering metadata is stored **in the graph to which the artifact belongs**

  * Domain ordering → Domain Graph
  * View ordering → View Graph
  * Design ordering → Design Graph

Ordering is structural, not semantic.

---

## 12. Round-Trip Guarantees (Normative)

Kernel defines two round-trip modes:

### 12.1 Semantic Round-Trip

* CDX → RDF → CDX
* semantic meaning preserved
* canonical formatting applied
* ordering preserved only where semantically required

### 12.2 Structural Round-Trip

* CDX → RDF → CDX
* semantic meaning preserved
* lexical ordering preserved via ordering metadata
* canonical formatting applied

Kernel MUST support both modes.

---

## 13. Query and Shaping (Normative)

Kernel derives a **ViewModel** by:

* interpreting View definitions from the **View Graph**
* querying the **Domain Graph**
* combining results deterministically

The ViewModel is:

* derived
* structural
* target-neutral
* deterministic
* non-authoritative

---

## 14. ViewModel Lifecycle (Normative)

The ViewModel:

* exists only within the pipeline
* is not stored as a persistence boundary
* may be serialized for debugging or testing only
* MUST be fully reproducible from stored graphs

---

## 15. Design Policy Application (Normative)

Kernel exclusively owns application of Design Policy.

Design Policy:

* is declarative
* introduces no semantic facts
* performs no IO
* modifies no domain truth

The result is a **Presentation Plan** that is pure, deterministic, and target-neutral.

---

## 16. Rendering (Normative)

Rendering is a pure function of:

* Presentation Plan
* render target
* render configuration

Rendering invents no structure and asserts no meaning.

---

## 17. Validation and Help (Normative)

Across all phases:

* no exceptions are thrown
* no `null` / `undefined`
* all failures are represented as structured diagnostics

Kernel validates:

* grammar
* structure
* lexical correctness

Kernel does **not** validate:

* domain semantics (Architect)
* ontology constraints (Warden)
* workflows or behavior

---

## 18. Implementation Neutrality (Normative)

Kernel MUST NOT embed implementation-specific library requirements into normative pipeline behavior.

---

## 19. Non-Ownership (Normative)

Kernel does **not** own:

* semantic meaning (Architect)
* constraint enforcement (Warden)
* tooling or orchestration (Quartermaster)
* application state or workflows

---

## 20. Authority and Precedence

This contract is subordinate to:

1. **Paperhat System Contract**

And authoritative over:

* Kernel pipeline implementations
* Kernel-dependent tooling behavior

Higher-authority documents prevail in case of conflict.

---

## 21. Change Control

This document is **UNLOCKED**.

Rationale (v0.3.1): Align contract language with Kernel ownership and remove previous implementation-specific references.

---

## 22. Summary

Kernel is:

* the authoritative Paperhat processing pipeline
* deterministic and explainable
* multi-graph by design
* atomic at the Module revision level
* explicit about ordering and round-tripping
* hostile to semantic ambiguity

Kernel processes authored meaning.
It does not define it.

---

**End of Kernel Pipeline Contract v0.3.1**
