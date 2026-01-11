# Work Packet — Scribe Demo 06

## Scope: RDF Instance Graph → Essay ViewModel (Defaults) per Rendering Contract

Status: PROPOSED  
Governing Docs:

* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)
* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)

Inputs:

* Validated Essay instance graph (Demo 03 + Demo 05) for:

  * `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* Essay schema bundle metadata (for concept naming and ordered container flags)

Output:

* `EssayViewModel` JSON object exactly matching the rendering contract

---

## Objective

Implement the deterministic projection from a validated RDF instance graph of an `Essay` into the ViewModel required by the **Essay → HTML Default Rendering Contract**.

This packet creates the semantic-to-render boundary needed to render HTML using defaults.

---

## Non-Goals (Explicit)

* Do **not** render HTML (already covered by Demo 01).
* Do **not** include CSS assets or `<link>` injection (Demo 01).
* Do **not** parse or resolve Gloss markers (Demo 07).
* Do **not** implement Recipe ViewModel (separate packet).
* Do **not** implement alternate Views or customization.

---

## Required ViewModel Output (Normative)

The output MUST match the contract’s root shape:

```json
{
  "type": "Essay",
  "id": "string",
  "frontMatter": {
    "title": "string",
    "subtitle": "string | null",
    "synopsis": "string | null",
    "tags": [ "string", ... ]
  },
  "mainContent": [ ... ],
  "backMatter": {
    "notes": [ ... ],
    "references": [ ... ]
  }
}
```

All ordered containers MUST be represented as arrays in authored order.

---

## Projection Rules (Normative for this packet)

### 1) Identify root essay node

* Find the single node with `hasConceptName = "Essay"`.
* Extract its `id` trait value as `viewModel.id`.

If missing, this is an error (but should not occur after validation).

### 2) FrontMatter extraction

From the Essay’s `FrontMatter` child (by concept name):

* `Title` → text content → `frontMatter.title` (required)
* `Subtitle` → text → `frontMatter.subtitle` (optional)
* `Synopsis` (or `Summary`, whichever is in your schema) → text → `frontMatter.synopsis` (optional)
* `Tags` → sequence of `Tag` children text values → `frontMatter.tags` array (unordered semantics allowed, but preserve authored order for determinism)

If an optional concept is absent, set corresponding field to `null` (or empty array for tags).

### 3) MainContent extraction

Determine which discourse container exists (exactly one per schema choice constraint), e.g.:

* `MainText` OR `Exposition` OR `Narrative` OR `Discourse`

Find that node and project its direct children as the `mainContent` array in authored order.

Supported content blocks (minimum):

* `Section`
* `Paragraph`
* `Quote`
* `PullQuote`
* `OrderedList`

If unexpected content appears, return deterministic projection error (do not silently drop).

### 4) Section projection (recursive)

For each `Section` node:

* `id` trait (if present) → `id` field, else `null`
* `Heading` child text (if present) → `heading`, else `null`
* Remaining content children (in order) → `content` array

Nested `Section` nodes are projected recursively.

### 5) Paragraph projection

A `Paragraph` node becomes:

```json
{ "type": "Paragraph", "text": "..." }
```

Text is the opaque content of the Paragraph node (no Gloss processing in this packet).

### 6) Quote / PullQuote projection

A `Quote` or `PullQuote` node becomes:

```json
{
  "type": "Quote",
  "content": [ { "type": "Paragraph", "text": "..." }, ... ]
}
```

Quote content MUST be projected as an ordered list of Paragraph blocks (or other allowed text blocks if present in your schema, but keep minimal).

### 7) OrderedList projection

An `OrderedList` node becomes:

```json
{
  "type": "OrderedList",
  "items": [
    { "content": [ ... ] },
    ...
  ]
}
```

Each `Item` node projects to:

```json
{ "content": [ { "type": "Paragraph", "text": "..." }, ... ] }
```

Items are ordered.

### 8) BackMatter extraction

From `BackMatter` child:

* `Notes` → list of `Note` (or `Reference`-style note) entries
* `References` → list of `Reference` entries

Minimum required fields:

Notes:

* `id` from trait `id` or equivalent entity id
* `content` as array of Paragraph blocks (ordered for determinism even if notes are unordered)

References:

* `id`
* `title` (text)
* `authors` (if present; else empty array)

If absent, return empty arrays.

---

## Required Graph Access Helpers

Implement pure helper functions to query the instance graph deterministically:

* `getConceptChildren(node, conceptName) -> Node[]`
  Children filtered by concept name, ordered by `hasChildIndex`.

* `getAllChildren(node) -> Node[]`
  Ordered by `hasChildIndex`.

* `getText(node) -> string`
  Deterministic retrieval of `hasText` (or concatenation order if multiple).

* `getTrait(node, traitName) -> TraitValue | null`

These helpers should be usable by future packets (Recipe ViewModel, Gloss resolution).

---

## Required Public API

* `projectEssayViewModel(input: { store: OxigraphStore; graph: GraphRef }): Result<EssayViewModel, ProjectionError[]>`

`ProjectionError` MUST include:

* `code` (short string)
* `nodeId` when applicable
* `message`

Errors MUST be deterministic and minimal.

---

## Tests

### A) Golden Essay projection

* Produces a ViewModel matching the required JSON shape.
* `type` is `"Essay"`.
* `frontMatter.title` matches the fixture.
* `mainContent` block count and ordering match authored order.
* Nested sections preserved.
* Quotes and lists preserved.

### B) Determinism

* Project twice → identical JSON output (byte-equivalent when serialized with canonical stable stringify).

### C) Error case

* If the discourse container is missing (simulate by removing it), projection fails deterministically with a clear error code.

---

## Acceptance Criteria

This packet is DONE when:

* Golden Essay instance graph projects to ViewModel per contract.
* Ordering is correct everywhere (sections, quote paragraphs, list items).
* Output is deterministic across runs.
* Tests pass.

---

## Notes

* Do not parse Gloss markers yet; treat paragraph text as opaque.
* Do not interpret “unordered” semantics as permission to reorder; preserve authored order for deterministic output.
* Keep projection minimal: only support the Concepts needed by the golden Essay fixture.
