# Work Packet — Scribe Demo 10

## Scope: Presentation Bundle Retrieval (Architect Defaults) + Real CSS Assets for Beautiful Demo

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs:

* Architect Codex-authored presentation-definition sources for:

  * `Essay` + `html`
  * `Recipe` + `html`

Outputs:

* Presentation Bundle for `(Essay, html)` with:

  * default view id(s)
  * default CSS assets attached to Concepts + dependency graph
  * stable digest
* Presentation Bundle for `(Recipe, html)` with same
* Real CSS files (or generated CSS text) that make the demo page look complete and attractive

---

## Objective

Replace stubs with real Architect-owned defaults so the demo proves the key selling point:

> You can ignore Views/ViewModel/DesignPolicy and still get a beautiful, functional site by accepting defaults.

This packet makes Architect the canonical home for:

* default View selection
* default concept-attached CSS assets
* dependency layering and deduped inclusion

And it provides the actual CSS that makes the pages feel production-ready.

---

## Non-Goals (Explicit)

* Do **not** build a full theming system (token overrides can be minimal).
* Do **not** implement alternate Views or templates.
* Do **not** implement PDF/XSL targets.
* Do **not** implement site navigation or page layout beyond what CSS provides.
* Do **not** implement asset minification or bundling; links are fine.

---

## Required Authoritative Inputs (Codex)

Define a small Concept vocabulary in Architect for presentation resources (v0.1), sufficient to author:

* a PresentationBundle definition
* CSS assets bound to Concepts
* dependency relations

Minimum required Concepts (names are normative here):

* `PresentationBundle`
* `DefaultView`
* `TargetAsset`
* `AssetDependency`
* `AppliesTo` (or use traits; choose one pattern and be consistent)

Minimum required Traits:

* `id` (entity id for bundles/assets)
* `rootConcept` (e.g. `"Essay"`)
* `target` (e.g. `"html"`)
* `assetKind` (e.g. `"css"`)
* `locator` (href string)
* `appliesToConcept` (e.g. `"Section"`)
* `dependsOn` (asset id)

These are authored in Codex and compiled into RDF presentation metadata predicates required by the Architect Runtime Contract.

---

## Presentation Bundle Compilation (Normative)

From Codex presentation-definition documents, compile RDF that includes:

For each asset:

* `hasAssetId`
* `appliesToTarget`
* `appliesToConcept`
* `hasAssetKind`
* `hasAssetLocator`
* `dependsOnAsset` edges (from `dependsOn`)

For each bundle:

* `bundleRootConceptName`
* `bundleTarget`
* `bundleVersion`
* `bundleLockState`
* `bundleDigest`
* default view resource(s) for the bundle’s root concept and target

---

## Bundle Retrieval API (Required)

* `getPresentationBundle(rootConceptName: string, targetName: string): Result<PresentationBundle, PresentationBundleError>`

Must be deterministic and versioned (v0.1 only is fine).

---

## Real CSS Assets (Demo Quality Requirements)

Provide a small set of CSS files (or emitted CSS strings) that make both pages look “complete”:

### Minimum qualities

* pleasant typography defaults
* readable line length and spacing for essays
* clear hierarchy for headings/sections
* blockquote styling that looks intentional
* list styling that is clean
* notes/references section styling that reads well
* recipe layout that is scannable: ingredients, steps, equipment
* consistent spacing scale

### Strong constraint

CSS must be:

* concept-attached (e.g., `Section.css`, `Paragraph.css`, etc.)
* layered via explicit dependencies
* includable via `<link>` tags (no bundling required)

### Token minimalism (optional but recommended)

Define a tiny token file (e.g., `base.css`) that sets CSS variables:

* font family
* base text size/line height
* spacing scale
* max content width

Concept CSS should depend on base.

---

## Required Asset Set (Minimum)

### Essay (html)

At minimum assets for:

* `Essay` (base layout + tokens)
* `FrontMatter`
* `Section`
* `Paragraph`
* `Quote`
* `PullQuote`
* `OrderedList`
* `Item`
* `Notes`
* `References`

With explicit dependencies, e.g.:

* `Paragraph` depends on `EssayBase`
* `Section` depends on `EssayBase`
* `Quote` depends on `Paragraph`
* `Item` depends on `OrderedList`

### Recipe (html)

At minimum assets for:

* `Recipe` (base layout + tokens)
* `Ingredients`
* `Ingredient`
* `Equipment`
* `Steps`
* `Step`
* `Tags`

---

## Tests

### A) Bundle retrieval tests

* `getPresentationBundle("Essay","html")` succeeds and returns assets + dependencies.
* `getPresentationBundle("Recipe","html")` succeeds.

### B) Asset graph correctness

* All `dependsOn` references resolve.
* No cycles (cycle should fail deterministically).

### C) Demo output verification

* End-to-end Essay build includes expected `<link>` tags matching bundle assets.
* End-to-end Recipe build includes expected `<link>` tags.

### D) Visual sanity checks (manual)

* Open `dist/essay/index.html` and `dist/recipe/index.html`:

  * both look complete and intentional using defaults alone.

---

## Acceptance Criteria

This packet is DONE when:

* Presentation bundles are authored in Codex and compiled deterministically.
* Scribe retrieves real presentation bundles (no stubs).
* Both Essay and Recipe builds include the correct linked CSS assets by concept usage.
* The resulting pages look complete and attractive with zero customization.

---

## Notes

* This packet is the demo’s “wow moment.” Keep it small but polished.
* Avoid “framework CSS.” Defaults should read as Paperhat’s canonical baseline.
