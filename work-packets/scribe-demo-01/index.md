# Work Packet — Scribe Demo 01

## Scope: Default HTML Asset Inclusion + `<link>` Emission (Concept-attached assets)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs (golden fixtures):

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

---

## Objective

Implement the deterministic default-asset path for the HTML demo:

1. Determine the **Used Concept Set** for a page (for this packet: sourced from a provided list or a temporary ViewModel stub; *not* from RDF yet).
2. Retrieve a **Presentation Bundle** for `(rootConceptName, targetName="html")` (for this packet: stubbed in-process bundle is allowed).
3. Select assets for the Used Concept Set, compute **dependency closure**, **dedupe**, and a **deterministic order**.
4. Emit `<link rel="stylesheet" ...>` elements in `<head>` in the correct order.
5. Produce one HTML file for Essay and one for Recipe, proving “accept defaults → nice page” plumbing exists.

This packet authorizes implementation of the asset selection/closure/dedupe/order algorithm and the head injection plumbing only.

---

## Non-Goals (Explicit)

* Do **not** implement Codex parsing.
* Do **not** implement RDF lowering.
* Do **not** implement SHACL validation.
* Do **not** implement real bundle retrieval from a store.
* Do **not** implement full ViewModel projection.

This packet is about the **default asset mechanism**, not the pipeline.

---

## Deliverables

### A) Core pure functions

1. `computeUsedConceptSetFromStub(...) -> Set<ConceptName>`

   * Input may be a hardcoded list for now.
   * Must be deterministic.

2. `selectHtmlAssetsForConcepts(bundle, usedConcepts) -> AssetSelection`

   * Implements:

     * initial selection: assets where `appliesToTarget=html` and `appliesToConcept ∈ usedConcepts`
     * dependency closure via `dependsOnAsset` (transitive)
     * dedup by `assetId`
     * deterministic ordering:

       * dependencies before dependents
       * stable tie-breaking for independent assets

3. `renderHeadStylesheetLinks(orderedAssets) -> string`

   * Produces `<link rel="stylesheet" href="...">` tags in order.
   * No duplicates.

### B) Minimal HTML renderer hook

4. `renderHtmlDocument({ title, headLinks, bodyHtml }) -> string`

   * Must include `<head>` and `<body>`.
   * Head must include the generated stylesheet links.

### C) Demo outputs

* `dist/essay/index.html`
* `dist/recipe/index.html`

These pages can have placeholder body content for now, but **must** show:

* correct `<link>` emission
* deterministic, dependency-respecting ordering
* deduplication

---

## Definitions

### ConceptName

A plain string, e.g. `"Essay"`, `"Section"`, `"Paragraph"`.

### Asset

An object with:

* `assetId: string` (stable id; dedupe key)
* `targetName: "html"` (for this packet)
* `kind: "css"` (for this packet)
* `appliesToConceptName: string`
* `locator: string` (emitted into `href`)
* `dependsOnAssetIds: string[]` (dependency edges)

### PresentationBundle (stub form for this packet)

* `rootConceptName: string`
* `targetName: "html"`
* `bundleDigest: string` (stable; can be placeholder but deterministic)
* `assets: Asset[]`

---

## Algorithm Requirements (Normative for this packet)

### 1) Initial selection

Select all assets where:

* `targetName == "html"`, AND
* `appliesToConceptName ∈ usedConcepts`

### 2) Dependency closure

Let `selected` be the initial set by `assetId`.

Repeatedly add any asset whose `assetId` appears in `dependsOnAssetIds` of an asset already in `selected`, until no more assets can be added.

If a dependency id is referenced but missing from `bundle.assets`, this MUST be an error.

### 3) Dedup

After closure, dedupe by `assetId`. (There must be exactly one asset object per `assetId`.)

### 4) Deterministic order

Produce a deterministic order that satisfies:

* For any edge `A dependsOn B`, asset `B` must appear **before** asset `A`.

Tie-breaking rule (mandatory):

* When multiple assets are eligible at the same time, order by `assetId` ascending (string compare).

Cycle handling:

* If dependencies contain a cycle, this MUST be an error with the cycle’s asset ids included.

This is essentially a stable topological sort.

---

## Test Requirements

### Unit tests

1. **Closure**

* Given a used concept set that selects asset `section.css` which depends on `base.css`,
  the output must include both assets.

2. **Dedup**

* If two used concepts both select the same `base.css`, output includes it once.

3. **Ordering**

* Dependencies appear before dependents.
* Independent assets sorted by `assetId`.

4. **Missing dependency error**

* If `dependsOnAssetIds` references an absent asset, fail deterministically.

5. **Cycle error**

* If cycle exists, fail deterministically.

### Snapshot tests (recommended)

* Snapshot the generated `<head>` link block for Essay and Recipe.

---

## Demo Bundle Stub (Minimum Content)

### Essay bundle stub

Must include at least these assets (ids illustrative but must be stable):

* `essay.base` → appliesTo `Essay`, locator like `/assets/essay/base.css`
* `text.block` → appliesTo `Paragraph`, dependsOn `essay.base`
* `section.block` → appliesTo `Section`, dependsOn `essay.base`
* `quote.block` → appliesTo `Quote`, dependsOn `text.block`
* `list.block` → appliesTo `OrderedList`, dependsOn `text.block`
* `item.block` → appliesTo `Item`, dependsOn `list.block`

### Recipe bundle stub

Similar minimal set:

* `recipe.base` → appliesTo `Recipe`
* `ingredient.block` → appliesTo `Ingredient`, dependsOn `recipe.base`
* `step.block` → appliesTo `Step`, dependsOn `recipe.base`

It is acceptable for the locator paths to be placeholders for now; they must be consistent and deterministic.

---

## Acceptance Criteria

This packet is DONE when:

* Running the demo build produces:

  * `dist/essay/index.html`
  * `dist/recipe/index.html`

* Each output HTML contains:

  * `<head>` with `<link rel="stylesheet" ...>` entries
  * no duplicate assets
  * dependency-respecting order
  * stable ordering across repeated runs

And the unit tests for closure/dedupe/order/errors pass.

---

## Notes

* This packet intentionally does not bind to the final RDF-backed “Used Concept Set.”
  That will come later; this packet locks the *asset mechanism* independently.

* Keep the implementation surface minimal and functional. No framework required.
