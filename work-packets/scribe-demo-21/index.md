# Work Packet — Scribe Demo 21

## Scope: Recipe → PDF Target via XSL-FO (Reuse Recipe XML + FO Engine + PDF Policy)

Status: PROPOSED  
Governing Docs:

* Scribe Demo 18 — PDF Target via XSL-FO (Essay) (PROPOSED)
* Scribe Demo 19 — PDF Determinism / Metadata Policy (PROPOSED)
* Scribe Demo 20 — Recipe → XML Target with XSL Defaults (PROPOSED)
* Architect Runtime Contract — Default Presentation Bundles (v0.1)

Inputs:

* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`
* Recipe XML output (from Demo 20):

  * `dist/recipe/index.xml`
* PDF determinism policy implementation (from Demo 19)
* FO processor (same as Demo 18, e.g., Apache FOP)

Outputs:

* `dist/recipe/index.fo`
* `dist/recipe/index.pdf`
* PDF digest records integrated into:

  * `dist/_paperhat/pdf-policy.json` (shared; may already exist)
  * `dist/_paperhat/pdf-digests.json` (add recipe entry)
  * manifest rules per Demo 19

---

## Objective

Complete the “real publishing” proof for the second domain:

1. Build semantic XML for Recipe (Demo 20)
2. Apply Architect default XSLT to transform Recipe XML → XSL-FO
3. Run FO processor to generate Recipe PDF
4. Apply the same determinism policy logic as Essay (Demo 19)

This proves the FO/PDF target is **domain-general**, not bespoke to Essay.

---

## Non-Goals (Explicit)

* Do **not** improve page design beyond “clean and readable.”
* Do **not** implement advanced FO features (tables, floats, multi-column).
* Do **not** implement images or media embeds.
* Do **not** implement scaling servings, timers, or interactive features.
* Do **not** add new schema constraints or new Recipe concepts.

---

## Required Behavior (Normative)

### 1) XML is authoritative intermediate

The PDF build MUST consume `dist/recipe/index.xml` as its semantic source.

### 2) Defaults come from Architect

Retrieve a Presentation Bundle for `(Recipe, pdf)` that contains XSLT assets to produce FO.

### 3) Deterministic FO

`dist/recipe/index.fo` MUST be byte-identical across runs for identical inputs.

### 4) PDF determinism policy

PDF output MUST follow Demo 19 tier rules:

* Tier A (byte-identical PDF) if achievable, else Tier B (normalized digest)
* manifest stability MUST be maintained

### 5) Fail-fast

If XML→FO transform fails or FO→PDF fails, build fails and produces no partial output.

---

## Recipe FO Output Contract (Minimum)

The `.fo` MUST be valid XSL-FO with a single-page-master layout and a readable structure:

* Title as large block
* Summary (optional) as smaller block
* Key facts (servings, times) as a compact block list
* Ingredients as a bulleted or labeled list
* Equipment as a short list
* Steps as a numbered list (ordered)
* Tags optional
* Source optional

No fancy styling required; the point is correctness and repeatability.

---

## Architect Presentation Bundle Requirements

Add a Presentation Bundle for `(Recipe, pdf)` with XSL assets.

Minimum assets (stable `assetId`s):

* `recipe.fo.xsl.shell` (root stylesheet shell + insertion point)
* `recipe.fo.xsl.front` (title/summary/facts)
* `recipe.fo.xsl.ingredients` (ingredients rendering)
* `recipe.fo.xsl.steps` (steps rendering)
* `recipe.fo.xsl.misc` (equipment/tags/source)

Dependencies explicit and acyclic.

Assembly rules identical to Demo 18:

* exactly one shell
* insert templates deterministically via topo-sort (ties by `assetId`)
* missing deps / cycles are errors

---

## Required Public API

* `buildRecipePdfDefault(inputPath: string): Result<{ foPath: string; pdfPath: string; digest: string }, BuildError[]>`

Where:

* `foPath` MUST be `dist/recipe/index.fo`
* `pdfPath` MUST be `dist/recipe/index.pdf`
* `digest` computed per Demo 19 (FO digest + PDF raw/normalized as policy dictates)

Stages in errors MUST include:

* `XmlInput`
* `PresentationBundle`
* `AssembleXsl`
* `TransformFo`
* `FoToPdf`
* `Write`
* `PdfDigest`

---

## Integration Requirements (Site Build)

Update the demo runner (Demo 14/11/12 orchestration) so that a “full demo build” can optionally include PDFs:

* `dist/essay/index.pdf`
* `dist/recipe/index.pdf`

PDF inclusion must not break determinism of the overall build digest (Demo 19 rules apply).

---

## Tests

### A) Output existence + well-formedness

* `dist/recipe/index.fo` exists and contains `<fo:root>`
* `dist/recipe/index.pdf` exists and size > 0

### B) Determinism

* Build twice:

  * FO byte-identical
  * PDF Tier A: byte-identical OR Tier B: normalized digest identical

### C) Content smoke

* FO contains the recipe title text
* FO contains at least one ingredient name
* FO contains at least one step text

### D) Failure test

* Introduce a deliberate bundle dependency error → build fails deterministically at `PresentationBundle` or `AssembleXsl`.

---

## Acceptance Criteria

This packet is DONE when:

* Recipe builds to FO and PDF using defaults only.
* FO is deterministic.
* PDF determinism policy is correctly applied and recorded.
* Manifest stability is preserved.
* Tests pass.
