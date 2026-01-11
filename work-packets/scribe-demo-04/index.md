# Work Packet — Scribe Demo 04

## Scope: Codex-Authored Schemas → Compile to SHACL + Schema Bundle Retrieval (Essay + Recipe)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Schema Authoring in Codex (v0.1, WORKING DRAFT)

Inputs (authoritative Codex schema sources):

* Architect schema-definition Codex documents for:

  * Essay schema family
  * Recipe schema family

Outputs (compiled artifacts):

* Schema Bundle for `Essay`
* Schema Bundle for `Recipe`

---

## Objective

Implement the minimum viable “schemas are authored in Codex” loop:

1. Define the **Schema Authoring meta-vocabulary** required for schema-definition documents.
2. Parse schema-definition Codex documents using the existing parser (Demo 02).
3. Lower them to an RDF schema graph (similar lowering as Demo 03, but into a schema graph).
4. Compile schema-definition intent into:

   * required schema metadata predicates
   * SHACL NodeShapes / PropertyShapes sufficient to validate the golden Essay and Recipe instance graphs
5. Provide a deterministic **Schema Bundle retrieval** API by `rootConceptName`.

This packet makes Architect real: the schema bundle must be produced from Codex source, not hand-written Turtle.

---

## Non-Goals (Explicit)

* Do **not** implement OWL reasoning.
* Do **not** implement full SHACL expressiveness beyond what Essay/Recipe require.
* Do **not** implement presentation bundles (CSS/views); that comes after validation.
* Do **not** implement version discovery across multiple spec versions; assume v0.1 only.

---

## Required Inputs (Concrete)

### A) Schema-definition documents

Create schema-definition Codex documents (authoritative) for:

* `Essay` family
* `Recipe` family

They MUST use the authoring model from “Schema Authoring in Codex” (draft), at minimum:

* `<Schema id="...">`

  * `<ConceptDefinition name="..." entity=true|false orderedContainer=true|false> ...`
  * `<TraitDefinition ... />`
  * `<TraitUsage ... />`
  * `<ChildConstraint ... />`
  * `<ChoiceConstraint ...> <ChoiceOption .../> ... </ChoiceConstraint>`

---

## Outputs

### A) Schema Graph (RDF) containing:

* Concept resources with:

  * `hasConceptName`
  * `isOrderedContainerConcept` boolean
  * `isEntityConcept` boolean

* SHACL NodeShapes and property constraints sufficient for validation (see below)

### B) Schema Bundle metadata:

* `bundleRootConceptName`
* `bundleVersion` (e.g., `"0.1"`)
* `bundleLockState` (e.g., `"LOCKED"` or `"UNLOCKED"`—must be deterministic)
* `bundleDigest` (stable hash over canonical serialization of the bundle)

### C) Bundle retrieval API:

* `getSchemaBundle(rootConceptName: string): Result<SchemaBundle, SchemaBundleError>`

---

## Compilation Requirements (Minimum SHACL Feature Set)

Support only what is required to validate the golden fixtures.

### 1) Required Traits (Entity id)

If `isEntityConcept = true`, then:

* the node MUST have an `id` trait present

This MUST be expressed as a SHACL constraint.

### 2) Allowed children and cardinalities

From `ChildConstraint`:

* Allowed child concept types under a parent concept
* Optional `min` and `max` constraints

This MUST be enforced by SHACL.

### 3) Exclusive choice groups

From `ChoiceConstraint`:

* Enforce “exactly one of these concepts appears” where `min=1 max=1`

Support only `min/max` where used by the Essay schema (most likely `1..1`).

### 4) Closed-world containment

Containment MUST be closed-world for Concepts in scope:

* Any child element instance not permitted by constraints MUST be invalid.

Implementation may express this using:

* `sh:closed true` with `sh:ignoredProperties`, or
* explicit SPARQL-based SHACL constraints, or
* any deterministic equivalent

---

## Schema-to-Instance Compatibility Rules

The schema graph and instance graph must share Concept naming semantics:

* instance nodes identify Concept by `hasConceptName`
* schema bundle identifies Concepts by `hasConceptName`

SHACL constraints must be authored to match this representation.

No reliance on RDF class typing is required (allowed if present, but not required).

---

## Required Public API

### 1) Compile schema bundle from Codex sources

* `compileSchemaBundleFromCodexSources(rootConceptName: string): Result<SchemaBundle, CompileError[]>`

### 2) Retrieve schema bundle

* `getSchemaBundle(rootConceptName: string): Result<SchemaBundle, SchemaBundleError>`

For this packet, retrieval may be in-memory, but must be deterministic and keyed by `rootConceptName`.

---

## Tests

### A) Compilation tests

1. Compiling `Essay` schema bundle succeeds deterministically.
2. Compiling `Recipe` schema bundle succeeds deterministically.
3. Compiling twice produces identical `bundleDigest`.

### B) Bundle content tests

For `Essay` bundle:

* `Essay` concept resource exists and has required metadata predicates.
* Key ordered container concepts have `isOrderedContainerConcept=true` (e.g., `Section`, `Quote`, `Item`, plus your discourse container concept).

For `Recipe` bundle:

* `Steps` (or equivalent) is marked ordered if schema declares it.
* `Step` concept exists.

### C) Negative compilation tests

* Missing required fields in schema-definition doc produce deterministic errors (line + code).

---

## Acceptance Criteria

This packet is DONE when:

* Schema-definition Codex sources produce Schema Bundles for `Essay` and `Recipe`.
* Each bundle includes:

  * Concept metadata predicates
  * SHACL shapes sufficient to validate the golden fixtures
  * deterministic digest
* Bundle retrieval by root Concept name works deterministically.

---

## Notes

* Keep SHACL generation minimal and explicit.
* Prefer boolean predicates (`isOrderedContainerConcept`, `isEntityConcept`) exactly as in the Architect Runtime Contract.
* This packet intentionally does not validate instance graphs yet; Demo 05 will do that.
