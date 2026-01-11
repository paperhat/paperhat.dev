# Work Packet — Scribe Demo 05

## Scope: SHACL Validation of Instance Graphs (Essay + Recipe) + Deterministic Validation Report

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)

Inputs:

* Instance graphs produced by Demo 03 for:

  * `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
  * `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`
* Schema bundles produced by Demo 04 for:

  * `Essay`
  * `Recipe`

---

## Objective

Implement deterministic SHACL validation:

1. Load the Schema Bundle (SHACL shapes + metadata) for the document’s root concept.
2. Validate the instance graph against the SHACL shapes using Oxigraph’s SHACL engine (or the chosen deterministic SHACL engine).
3. Produce a machine-consumable validation report that:

   * is deterministic for identical inputs
   * references failing nodes and constraints
   * provides Concept and Trait names where applicable

This packet gives the pipeline “teeth” and blocks invalid content from rendering.

---

## Non-Goals (Explicit)

* Do **not** implement ViewModel projection.
* Do **not** implement rendering.
* Do **not** implement Gloss resolution.
* Do **not** implement bundle caching strategies beyond basic memoization.
* Do **not** implement inference (OWL reasoning).

---

## Required Public API

### 1) Validate a document graph

* `validateInstanceGraph(input: { rootConceptName: string; instanceGraph: GraphRef }, schemaBundle: SchemaBundle): Result<ValidationOk, ValidationFail>`

Where:

* `ValidationOk` includes:

  * `conforms: true`
  * `reportDigest: string` (stable hash over canonical report form)

* `ValidationFail` includes:

  * `conforms: false`
  * `violations: Violation[]`
  * `reportDigest: string`

### 2) Validate by root concept name

* `validateByRootConceptName(input: { rootConceptName: string; instanceGraph: GraphRef }): Result<ValidationOk, ValidationFail | ValidationSystemError>`

This function retrieves the schema bundle deterministically (using Demo 04 retrieval API).

---

## Validation Report Model (Normative for this packet)

Each `Violation` MUST include:

* `nodeId: string`
  A stable identifier for the failing instance node (IRI or internal id).

* `conceptName: string | null`
  Derived from `(node, hasConceptName, ...)` when available.

* `path: string | null`
  A predicate or trait path if available (e.g., `hasTraitValue`, `hasChild`, etc.).

* `message: string`
  Short, deterministic message. Avoid engine-specific verbosity.

* `severity: "Violation" | "Warning"`
  For this demo, treat all failures as `"Violation"`.

* `constraintId: string | null`
  Identifier for the failing constraint or SHACL shape.

`violations` array order MUST be deterministic:

* primary sort: `nodeId` ascending
* secondary sort: `constraintId` ascending (null last)
* tertiary sort: `message` ascending

---

## Required Behavior

### 1) Golden fixtures must validate

* Golden Essay instance graph MUST conform to `Essay` schema bundle.
* Golden Recipe instance graph MUST conform to `Recipe` schema bundle.

### 2) At least two intentional failing fixtures

Create two small negative documents (inline or files) and run them through AST → RDF (Demo 03) and validation:

* **Failing Essay**: missing required discourse container / missing required child per schema
* **Failing Entity**: missing required `id` trait where schema marks concept as entity

Each MUST produce deterministic violations.

### 3) Fail-fast semantics

Rendering is out of scope, but validation must clearly signal:

* conforming vs non-conforming
* violations list (possibly empty)

---

## Implementation Requirements

* Use the SHACL shapes emitted by Demo 04.
* Do not hand-write SHACL in code.
* Do not silently “fix up” instance graphs.

If the SHACL engine returns additional fields, you may ignore them, but your report MUST be stable and derived deterministically.

---

## Tests

### A) Conformance tests

1. Golden Essay conforms.
2. Golden Recipe conforms.

### B) Negative tests

3. Failing Essay does not conform; violations include the expected missing structure.
4. Missing entity id does not conform; violations identify the relevant node and mention `id`.

### C) Determinism tests

5. Validating the same graph twice yields identical `reportDigest` and identical `violations` order/content.

---

## Acceptance Criteria

This packet is DONE when:

* Validation succeeds for both golden fixtures.
* Validation fails deterministically for at least two negative fixtures.
* The produced validation report model is stable and sorted deterministically.
* All tests pass.

---

## Notes

* Keep the report minimal; focus on reliability and determinism.
* Do not expose raw SHACL engine strings unless you normalize them.
* Use `hasConceptName` on failing nodes to provide meaningful `conceptName`.
