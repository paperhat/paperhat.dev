# Work Packet — Scribe Demo 08

## Scope: End-to-End Essay Build Command (Parse → RDF → Validate → ViewModel → Gloss → HTML + Default Assets)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs (golden fixture):

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`

Outputs:

* `dist/essay/index.html` (complete HTML page with default `<link>` assets)

---

## Objective

Wire all prior demo stages into a single deterministic end-to-end build for **Essay → HTML**, using **Architect defaults**.

Kernel:

1. Parse Codex → AST (Demo 02)
2. Lower AST → RDF instance graph (Demo 03)
3. Retrieve schema bundle and validate with SHACL (Demo 04 + Demo 05)
4. Retrieve presentation bundle for `(Essay, html)` (from Architect; stub acceptable if already implemented)
5. Project RDF → Essay ViewModel (Demo 06)
6. Resolve Gloss `{#id}` markers (Demo 07)
7. Compute Used Concept Set and include default assets (Demo 01 asset mechanism)
8. Render HTML (Demo 01 renderer) and write `dist/essay/index.html`

This packet produces the demo artifact that proves the system is real.

---

## Non-Goals (Explicit)

* Do **not** implement multi-page routing.
* Do **not** implement navigation, tags index, search.
* Do **not** implement Recipe end-to-end (next packet).
* Do **not** implement theming beyond using defaults.
* Do **not** implement incremental builds or watch mode.

---

## Required Public API

Implement a single entry point:

* `buildEssayHtmlDefault(inputPath: string): Result<{ outputPath: string; digest: string }, BuildError[]>`

Where:

* `inputPath` is the canonical fixture path
* `outputPath` MUST be `dist/essay/index.html`
* `digest` is a stable hash over the output HTML (canonicalized or raw, but deterministic)

---

## Required Build Behavior (Normative)

### 1) Deterministic output

For identical inputs (including bundle contents), the produced HTML must be byte-identical.

### 2) Fail-fast on invalid input

If parsing, lowering, schema compilation, bundle retrieval, validation, projection, gloss resolution, or rendering fails:

* the build MUST fail
* MUST return deterministic errors
* MUST NOT emit partial HTML output

### 3) Default assets included

The resulting HTML MUST include `<link rel="stylesheet" ...>` entries in `<head>` as computed by the default asset inclusion algorithm:

* based on Used Concept Set derived from RDF (preferred) or ViewModel (acceptable if deterministic)
* dependency closure
* dedupe
* deterministic order

### 4) HTML structure

The output must include the required structure from the rendering contract:

* `<article id="essay-...">`
* front matter elements (`<h1>`, etc.)
* sections, paragraphs, quotes, lists
* notes and references sections (if present)

### 5) Gloss anchors work

All `{#id}` markers must be replaced with working anchor links that match note/reference ids.

---

## Error Model (Normative)

Each `BuildError` MUST include:

* `stage` (one of: `Parse`, `Lower`, `SchemaBundle`, `Validate`, `PresentationBundle`, `Project`, `Gloss`, `Render`, `Write`)
* `code` (short stable string)
* `message`

Optional:

* `path`, `line`, `nodeId`, `id` (when relevant)

Errors MUST be deterministic in ordering (sort by stage order then code then message).

---

## Tests

### A) Golden build test

* Running `buildEssayHtmlDefault` produces `dist/essay/index.html`.
* HTML contains:

  * `<head>` with at least one stylesheet link
  * `<article>`
  * `<h1>` title
  * at least one `<section>` or `<p>`
* Links for notes/references exist if markers exist.

### B) Determinism test

* Run build twice with same inputs:

  * output HTML byte-identical
  * `digest` identical

### C) Negative build test

* Mutate fixture (or use a failing fixture) to break schema rule:

  * build fails at `Validate`
  * no output file emitted

---

## Acceptance Criteria

This packet is DONE when:

* A single command/function builds the Essay HTML page end-to-end.
* Output includes default assets and deterministic structure.
* The build is deterministic.
* Failures are deterministic and fail-fast.
* Tests pass.

---

## Notes

* Bundle retrieval may initially be in-memory stubs, but must conform to the Architect runtime contract’s semantics.
* Prefer Used Concept Set derived from RDF to align with the contract and reduce future refactors.
* Keep the build function small; delegate each stage to the prior packet’s functions.
