# Work Packet — Scribe Demo 03

## Scope: AST → RDF Instance Graph (load into Oxigraph) + Used Concept Set

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs (from Demo 02):

* `DocumentAst` for:

  * `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
  * `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

---

## Objective

Implement the minimal lowering step that converts a parsed Codex AST into an RDF instance graph suitable for:

* SHACL validation later (next packet)
* computing the **Used Concept Set** from the graph (for default assets)
* supporting deterministic ordered-child traversal where required

This packet produces real triples and loads them into Oxigraph.

---

## Non-Goals (Explicit)

* Do **not** implement SHACL validation.
* Do **not** implement schema bundle retrieval.
* Do **not** implement ViewModel projection.
* Do **not** implement Gloss parsing or resolution.
* Do **not** implement inference (OWL reasoning).

---

## Outputs

### A) RDF instance graph loaded into Oxigraph

* For each input document, load triples into a named graph (or separate store instance; either is acceptable if deterministic).

### B) Used Concept Set derived from RDF

* Implement a query/function that returns the set of Concept names used in the document.

### C) Deterministic child ordering encoding

* Encode child order in RDF so it can be reconstructed deterministically later.

---

## RDF Modeling (Normative for this packet)

The exact IRI namespace is implementation-defined, but the structure MUST support the following semantics.

### 1) Document root

Represent the document root element instance as a resource `rootNode`.

You MUST record:

* its Concept name
* its children
* their order

### 2) Concept instance typing

For every element instance node `n`:

* `(n, hasConceptName, "ConceptName")`

Optionally also type it via `rdf:type` to a concept IRI, but `hasConceptName` is mandatory.

### 3) Traits

For each trait on an element instance:

* `(n, hasTraitName, "traitName")` is not required if you model traits as distinct predicates, but you MUST preserve:

  * trait name
  * trait value

Minimum requirement (simple model):

* create a blank/resource `t` representing the trait assertion:

  * `(n, hasTrait, t)`
  * `(t, hasTraitName, "id")`
  * `(t, hasTraitValueString, "spaghetti-aglio-e-olio")` (or number/bool variants)

You may instead map known trait names directly to predicates, but keep it deterministic.

### 4) Children and child order

For each element node `parent` with children elements `c0..ck` in authored order:

* `(parent, hasChild, ci)` for each child element instance
* `(parent, hasChildAtIndex, listNode)` is optional, but you MUST encode order.

Order encoding (minimum deterministic requirement):

* For each child element `ci`:

  * `(ci, hasParent, parent)`
  * `(ci, hasChildIndex, i)` where `i` is a 0-based integer literal

This is sufficient to reconstruct order.

### 5) Text nodes

For text content inside an element, attach as:

* `(parent, hasText, "…")`

If there are multiple text segments, either:

* concatenate deterministically with `\n`, or
* represent multiple `hasText` values with an index similar to children

Either is acceptable as long as deterministic.

### 6) Document identity

Record the source path:

* `(rootNode, hasSourcePath, "paperhat.dev/demo/modules/.../index.cdx")`

This helps debugging and traceability.

---

## Required Public API

### 1) Lowering

* `lowerAstToInstanceGraph(input: { path: string; ast: DocumentAst }, store: OxigraphStore): Result<InstanceGraphInfo, LowerError[]>`

`InstanceGraphInfo` MUST include:

* `rootNodeIri` (or identifier)
* `graphName` (if using named graphs)
* `usedConceptNames: Set<string>`

### 2) Used Concept Set query

Implement a deterministic query or traversal:

* `getUsedConceptNames(store, graph) -> Set<string>`

This MUST be derived from the RDF graph, not the AST, once lowering is done.

---

## Tests

### 1) Golden Essay graph

* Root node has `hasConceptName = "Essay"`.
* Graph contains expected Concept names: `Essay`, `FrontMatter`, `Title`, `Exposition` (or `MainText` depending on fixture), `Section`, `Paragraph`, etc.
* Child ordering:

  * For `Steps` or `Section`-like containers, verify child indices match authored order.

### 2) Golden Recipe graph

* Root node has `hasConceptName = "Recipe"`.
* `Ingredients` has multiple `Ingredient` children with indices 0..n in correct order.
* `Steps` has multiple `Step` children with indices in correct order.

### 3) Determinism

* Lowering the same AST twice produces identical triples (byte-equivalent serialization is not required, but graph isomorphism with identical literal values and indices is required).

### 4) Error case

* If AST contains an impossible structure (e.g., missing root), return deterministic error.

---

## Acceptance Criteria

This packet is DONE when:

* Both golden fixtures lower successfully to RDF and load into Oxigraph.
* Used Concept Set is computed from RDF correctly for each fixture.
* Child order is reconstructable deterministically via `hasChildIndex`.
* Tests pass for expected concepts and ordering.

---

## Notes

* Keep the RDF model minimal; avoid premature generality.
* Do not attempt schema validation here; that’s the next packet.
* Do not parse Gloss here; text remains opaque.
