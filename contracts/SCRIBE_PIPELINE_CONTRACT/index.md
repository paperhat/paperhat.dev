Status: NORMATIVE
Lock State: LOCKED
Version: 0.2
Editor: Charles F. Munat

# Scribe Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Scribe** library.

Scribe is the **authoritative semantic processing pipeline** of the **Paperhat Semantic Authoring System**.

---

## 1. Purpose (Hard)

This contract exists to:

* define Scribe’s **exclusive ownership** of the Paperhat processing pipeline
* formalize strict **phase separation**, **purity**, and **IO boundaries**
* guarantee **determinism**, **explainability**, and **round-trippability**
* prevent semantic drift, partial ingestion, or framework-like behavior

Scribe is authoritative for **processing**, not for **meaning**.

---

## 2. Scope

This contract governs:

* compilation of Codex (`.cdx`) artifacts
* semantic normalization and emission
* interaction with the triple store (via Pathfinder)
* shaping, planning, and rendering phases
* guarantees around determinism and round-trip behavior

This contract does **not** govern:

* semantic meaning or vocabularies (Architect)
* ontology constraints (Warden)
* tooling and orchestration (Quartermaster)
* runtime behavior or workflows

---

## 3. Pipeline Ownership (Exclusive)

Scribe exclusively owns the following pipeline:

1. **Compilation** — CDX → AST → IR → RDF/Turtle (pure)
2. **Storage** — RDF → triple store (IO via Pathfinder)
3. **Query** — SPARQL → results (IO via Pathfinder)
4. **Shaping** — results → ViewModel (pure)
5. **Planning** — ViewModel + Design Policy → Presentation Plan (pure)
6. **Rendering** — Presentation Plan → target output (pure)

No other library may redefine, bypass, or collapse these phases.

---

## 4. Compilation Responsibilities (Hard)

Scribe exclusively owns:

* CDX grammar and syntax
* lexical validation
* AST node definitions
* IR shape and normalization rules
* canonical formatting rules
* IR → RDF/Turtle emission

No other library may parse CDX or define an alternative CDX compiler.

---

## 5. Determinism and Canonical Form (Hard)

Scribe MUST enforce:

* a **single canonical surface form** for Codex documents
* deterministic AST, IR, and RDF emission for equivalent inputs
* stable identifiers and ordering for equivalent semantic inputs

Formatting is **canonical and mandatory**.

---

## 6. Module Ingestion and Atomicity (Hard)

Scribe processes **Modules atomically**.

* A Module MUST either compile and store **in full**, or **not at all**.
* Partial ingestion of a Module is prohibited.
* If any artifact in a Module fails compilation or validation, **no data from that Module revision is stored**.

Scribe MUST treat each successful ingestion as a **module revision**.

---

## 7. Provenance and Revision Identity (Normative)

For each successful Module ingestion, Scribe MUST establish:

* a stable **Module identifier**
* a **Module Revision identifier** (e.g. hash or equivalent)
* identifiers for each source artifact

These identifiers are **provenance metadata**, not source coordinates.

---

## 8. Source Location Policy (Hard)

Scribe MAY track:

* UTF-16 offsets
* line numbers
* column numbers

**Only** for:

* diagnostics
* Help generation
* tooling feedback

Source locations:

* MUST NOT be stored in the triple store
* MUST NOT affect semantic identity
* MUST NOT be required for round-trip reconstruction

---

## 9. Ordering and Structural Preservation (Hard)

To enable structural round-tripping, Scribe MUST emit explicit ordering metadata.

* Ordered collections MUST be represented using an explicit ordering predicate (e.g. `cdx:orderIndex`).
* Ordering applies wherever source order must be preserved, including:

  * sibling Concepts
  * list items
  * artifact ordering within a Module

Ordering metadata is **structural**, not semantic.

---

## 10. Round-Trip Guarantees (Hard)

Scribe defines two round-trip modes:

### 10.1 Semantic Round-Trip

* CDX → RDF → CDX
* Resulting document is **semantically equivalent**
* Canonically formatted
* Ordering MAY differ unless explicitly required by schema

### 10.2 Structural Round-Trip

* CDX → RDF → CDX
* Semantic meaning preserved
* **Lexical ordering preserved** via ordering metadata
* Canonical formatting applied

Scribe MUST support both modes.

---

## 11. Storage and Query (Hard)

Scribe:

* emits RDF/Turtle deterministically
* performs all IO through Pathfinder
* assumes a replaceable triple store backend

Triple store choice is **not normative**, provided the public API contract is honored.

---

## 12. ViewModel Shaping (Hard)

Scribe shapes SPARQL results into a **ViewModel**.

The ViewModel is:

* structural
* deterministic
* target-neutral
* independent of Design Policy and rendering

Scribe shapes **structure only**.
Semantic meaning remains external.

---

## 13. Design Policy Application (Hard)

Scribe exclusively owns **application** of Design Policy.

Design Policy:

* is authored in Codex
* is declarative configuration
* introduces no ontology facts
* performs no IO
* modifies no semantic truth

The result is a **Presentation Plan** that is:

* pure
* deterministic
* target-neutral

---

## 14. Rendering (Hard)

Rendering is:

* a pure function of:

  * Presentation Plan
  * render target
  * render configuration
* deterministic
* non-semantic

Rendering realizes plans; it does not invent structure or meaning.

---

## 15. Validation and Help (Hard)

Across all phases:

* no exceptions are thrown
* no `null` / `undefined`
* all failures are represented as **Help**

Scribe validates:

* grammar
* structure
* lexical correctness

Scribe does **not** validate:

* ontology constraints
* business rules
* workflows

---

## 16. Toolsmith Usage (Hard)

Scribe MUST:

* use Toolsmith monads exclusively
* use Toolsmith newtypes for identifiers
* use Toolsmith Help infrastructure
* never inspect monad internals
* never introduce ad-hoc error handling

Imperative code exists **only inside Toolsmith**.

---

## 17. Non-Ownership (Hard)

Scribe does **not** own:

* semantic meaning (Architect)
* constraints (Warden)
* tooling or orchestration (Quartermaster)
* state, workflows, or execution semantics

Scribe MAY invoke other libraries but MUST NOT subsume their responsibilities.

---

## 18. Authority and Precedence

This contract is subordinate to:

1. **Paperhat System Contract**

And authoritative over:

* Scribe implementations
* Scribe-dependent tooling

In case of conflict, higher-authority documents prevail.

---

## 19. Change Control

This document is **LOCKED**.

Changes require:

* version increment
* documented rationale
* review against System Contract and dependent specs

---

## 20. Summary

Scribe is:

* the authoritative Paperhat processing pipeline
* deterministic, pure where required
* atomic at the Module level
* explicitly ordered for round-trip
* non-semantic by design

Scribe processes authored meaning.
It does not define it.

---

**End of Scribe Library Contract v0.2**
