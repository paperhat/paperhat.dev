# Work Packet — Scribe Demo 09

## Scope: End-to-End Recipe Build Command (Parse → RDF → Validate → ViewModel → HTML + Default Assets)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)

Inputs (golden fixture):

* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

Outputs:

* `dist/recipe/index.html` (complete HTML page with default `<link>` assets)

---

## Objective

Extend the proven pipeline by adding a second, structurally different domain:

**Recipe → HTML**, using Architect defaults.

Kernel (similar to Essay, but with Recipe projection):

1. Parse Codex → AST (Demo 02)
2. Lower AST → RDF instance graph (Demo 03)
3. Retrieve schema bundle and validate with SHACL (Demo 04 + Demo 05)
4. Retrieve presentation bundle for `(Recipe, html)` (Architect defaults)
5. Project RDF → Recipe ViewModel (new in this packet)
6. Compute Used Concept Set and include default assets (Demo 01 asset mechanism)
7. Render HTML (minimal recipe renderer in this packet) and write `dist/recipe/index.html`

Recipe does not require Gloss for the demo unless the fixture includes it; treat text as opaque.

---

## Non-Goals (Explicit)

* Do **not** implement multi-page routing.
* Do **not** implement interactive features (timers, scaling, shopping lists).
* Do **not** implement full bibliographic formatting.
* Do **not** implement CMS authoring UI.
* Do **not** implement theme overrides beyond defaults.

---

## Required Public API

* `buildRecipeHtmlDefault(inputPath: string): Result<{ outputPath: string; digest: string }, BuildError[]>`

Where:

* `outputPath` MUST be `dist/recipe/index.html`
* `digest` is stable hash over output HTML (deterministic)

---

## Recipe ViewModel (Minimum Required)

Define a minimal ViewModel sufficient to render the golden fixture cleanly.

### Root shape

```json
{
  "type": "Recipe",
  "id": "string",
  "title": "string",
  "summary": "string | null",
  "servings": { "amount": "number | string", "unit": "string | null" },
  "times": {
    "preparation": { "duration": "number | string", "unit": "string | null" } | null,
    "cooking": { "duration": "number | string", "unit": "string | null" } | null
  },
  "ingredients": [
    { "name": "string", "amount": "number | string | null", "unit": "string | null", "optional": "boolean", "preparation": "string | null", "toTaste": "boolean" }
  ],
  "equipment": [ "string", ... ],
  "steps": [
    { "text": "string", "optional": "boolean" }
  ],
  "tags": [ "string", ... ],
  "source": "string | null"
}
```

Rules:

* Preserve authored order for `ingredients`, `equipment`, `steps`, and `tags` for determinism.
* Optional fields must be `null` when absent.

---

## Projection Rules (Normative for this packet)

From RDF instance graph:

* Root `Recipe` node:

  * `id` trait → `id`
  * `Title` text → `title`
  * `Summary` text → `summary` (optional)

* `Servings` traits:

  * `amount`, `unit` → `servings`

* `PreparationTime`, `CookingTime` traits:

  * `duration`, `unit` → `times.preparation`, `times.cooking` (optional)

* `Ingredients` container:

  * child `Ingredient` nodes in authored order
  * each `Ingredient`:

    * `name` trait required
    * optional `amount`, `unit`, `optional`, `preparation`, `toTaste`

* `Equipment` container:

  * child `Item` text values in authored order

* `Steps` container:

  * child `Step` text values in authored order
  * `optional` trait allowed

* `Tags` container:

  * child `Tag` text values in authored order

* `Source` text → `source` (optional)

If required data is missing post-validation, treat as projection error.

---

## Recipe HTML Rendering (Minimum Required)

Produce a clean, semantic HTML structure:

* `<article id="recipe-<id>">`
* `<h1>` title
* `<p class="summary">` optional
* sections:

  * servings + times
  * ingredients as `<ul>` with optional annotations
  * equipment as `<ul>`
  * steps as `<ol>` with optional step markers
  * tags as `<ul class="tags">`
  * source as `<p class="source">`

Must include `<head>` stylesheet links via asset inclusion algorithm.

---

## Tests

### A) Golden build test

* Running `buildRecipeHtmlDefault` produces `dist/recipe/index.html`.
* HTML contains:

  * `<head>` with stylesheet links
  * `<article>`
  * `<h1>` title matches fixture
  * ingredients list length matches fixture
  * steps list length matches fixture

### B) Determinism test

* Build twice yields byte-identical output and identical digest.

### C) Negative build test

* Break a required field (e.g., Ingredient missing `name`) → validation fails and build stops.

---

## Acceptance Criteria

This packet is DONE when:

* Recipe builds end-to-end to HTML using defaults.
* Default assets are included deterministically.
* Output is deterministic.
* Tests pass.

---

## Notes

* This packet intentionally defines only the minimum Recipe ViewModel needed for the demo.
* If you want, Recipe can share the same HTML renderer harness as Essay (document wrapper + head links), but keep renderers distinct at first for clarity.
