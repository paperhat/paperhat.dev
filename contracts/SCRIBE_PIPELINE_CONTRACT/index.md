Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.3  
Editor: Charles F. Munat

# Scribe Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Scribe** library.

Scribe is the **authoritative semantic processing pipeline** of the **Paperhat Semantic Authoring System**.

[Contracts Index](../)

---

## 1. Purpose (Hard)

This contract exists to:

* define Scribe’s exclusive ownership of the Paperhat processing pipeline
* enforce strict separation between **semantic truth**, **projection**, and **planning**
* guarantee determinism, inspectability, and round-trippability
* prevent epistemic contamination between authored artifact classes
* ensure that all derived artifacts are reproducible and non-authoritative

Scribe processes authored meaning.
It does not define meaning.

---

## 2. Scope

This contract governs:

* compilation of Codex (`.cdx`) artifacts
* semantic normalization and RDF emission
* interaction with the triple store (via Pathfinder)
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

Scribe exclusively owns the following conceptual pipeline:

1. **Compilation** — CDX → AST → IR → RDF/Turtle (pure)
2. **Storage** — RDF → triple store (IO via Pathfinder)
3. **Query** — SPARQL → results (IO via Pathfinder)
4. **Shaping** — results → ViewModel (pure)
5. **Planning** — ViewModel + Design Policy → Presentation Plan (pure)
6. **Rendering** — Presentation Plan → target output (pure)

No other library may redefine, bypass, or collapse these phases.

---

## 4. Artifact Classes and Epistemic Separation (Hard)

Scribe recognizes three **distinct classes of authored Codex artifacts**:

1. **Domain Data**

   * authored in `data.cdx`
   * asserts semantic truth
   * defines entities, relationships, values, and identity

2. **View Definitions**

   * authored in `view.cdx`
   * define projection, selection, grouping, ordering, and information architecture
   * do **not** assert semantic truth

3. **Design Policy**

   * authored in `design.cdx`
   * defines planning and realization policy
   * does **not** assert semantic truth

These classes are **epistemically distinct** and MUST NOT be conflated.

---

## 5. Multi-Graph Storage Model (Hard)

Scribe MUST store compiled artifacts in **separate graphs**, each with its own ontology and SHACL validation.

At minimum:

* **Domain Graph**

  * populated exclusively from `data.cdx`
  * contains semantic truth

* **View Graph**

  * populated exclusively from `view.cdx`
  * contains projection and information-architecture definitions

* **Design Graph**

  * populated exclusively from `design.cdx`
  * contains planning and realization policy

Graphs MUST NOT be merged.

No graph may depend on another for semantic correctness.

---

## 6. Compilation Responsibilities (Hard)

Scribe exclusively owns:

* Codex grammar and syntax
* lexical validation
* AST node definitions
* IR shape and normalization rules
* canonical formatting rules
* IR → RDF/Turtle emission

No other library may parse CDX or define an alternative CDX compiler.

---

## 7. Canonical Form and Determinism (Hard)

Scribe MUST enforce:

* a single canonical surface form for Codex documents
* deterministic AST, IR, and RDF emission for equivalent inputs
* stable identifiers and ordering for equivalent semantic inputs

Formatting is mandatory and non-optional.

---

## 8. Module Revision Atomicity (Hard)

Scribe processes **Modules atomically**.

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

For each successful Module revision, Scribe MUST establish:

* Module identifier
* Module Revision identifier
* Artifact identifiers for each source document

These identifiers are provenance metadata only and do not affect semantic meaning.

---

## 10. Source Location Policy (Hard)

Scribe MAY track line numbers, columns, and offsets **only** for:

* diagnostics
* Help generation
* tooling feedback

Source-location metadata:

* MUST NOT be stored in any graph
* MUST NOT affect semantic identity
* MUST NOT be required for round-trip reconstruction

---

## 11. Ordering and Structural Preservation (Hard)

To enable structural round-tripping, Scribe MUST emit explicit ordering metadata.

* Ordered collections MUST use an explicit ordering predicate (e.g. `cdx:orderIndex`)
* Ordering metadata is stored **in the graph to which the artifact belongs**

  * Domain ordering → Domain Graph
  * View ordering → View Graph
  * Design ordering → Design Graph

Ordering is structural, not semantic.

---

## 12. Round-Trip Guarantees (Hard)

Scribe defines two round-trip modes:

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

Scribe MUST support both modes.

---

## 13. Query and Shaping (Hard)

Scribe derives a **ViewModel** by:

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

## 14. ViewModel Lifecycle (Hard)

The ViewModel:

* exists only within the pipeline
* is not stored as a persistence boundary
* may be serialized for debugging or testing only
* MUST be fully reproducible from stored graphs

---

## 15. Design Policy Application (Hard)

Scribe exclusively owns application of Design Policy.

Design Policy:

* is declarative
* introduces no semantic facts
* performs no IO
* modifies no domain truth

The result is a **Presentation Plan** that is pure, deterministic, and target-neutral.

---

## 16. Rendering (Hard)

Rendering is a pure function of:

* Presentation Plan
* render target
* render configuration

Rendering invents no structure and asserts no meaning.

---

## 17. Validation and Help (Hard)

Across all phases:

* no exceptions are thrown
* no `null` / `undefined`
* all failures are represented as Help

Scribe validates:

* grammar
* structure
* lexical correctness

Scribe does **not** validate:

* domain semantics (Architect)
* ontology constraints (Warden)
* workflows or behavior

---

## 18. Toolsmith Usage (Hard)

Scribe MUST:

* use Toolsmith monads exclusively
* use Toolsmith newtypes for identifiers
* use Toolsmith Help infrastructure
* never inspect monad internals
* never introduce ad-hoc error handling

Imperative code exists **only inside Toolsmith**.

---

## 19. Non-Ownership (Hard)

Scribe does **not** own:

* semantic meaning (Architect)
* constraint enforcement (Warden)
* tooling or orchestration (Quartermaster)
* application state or workflows

---

## 20. Authority and Precedence

This contract is subordinate to:

1. **Paperhat System Contract**

And authoritative over:

* Scribe implementations
* Scribe-dependent tooling behavior

Higher-authority documents prevail in case of conflict.

---

## 21. Change Control

This document is **LOCKED**.

Changes require:

* explicit version increment
* documented rationale
* review against the Paperhat System Contract and dependent specifications

---

## 22. Summary

Scribe is:

* the authoritative Paperhat processing pipeline
* deterministic and explainable
* multi-graph by design
* atomic at the Module revision level
* explicit about ordering and round-tripping
* hostile to semantic ambiguity

Scribe processes authored meaning.
It does not define it.

---

**End of Scribe Library Contract v0.3**
