# Work Packet — Scribe Demo 11

## Scope: Demo Site Build (Two Pages) + Minimal Site Chrome (Defaults) + Reproducible Build Command

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs (golden fixtures):

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

Outputs:

* `dist/index.html` (home page)
* `dist/essay/index.html`
* `dist/recipe/index.html`
* `dist/assets/...` (copied/served CSS assets referenced by `<link>`)

---

## Objective

Produce a *complete demo site* that shows the selling point:

* author Codex
* accept defaults
* get a complete, beautiful site

This packet adds only what is necessary to demo “site/app” rather than “single page”:

* a home page with links to Essay and Recipe pages
* minimal site chrome (header/footer) applied by defaults
* a single reproducible build command that generates all pages deterministically

---

## Non-Goals (Explicit)

* Do **not** implement navigation trees, tag indexes, search.
* Do **not** implement content collections or routing beyond fixed paths.
* Do **not** implement RSS, sitemap, robots.txt.
* Do **not** implement CMS UI or editing UI.
* Do **not** implement pagination or multiple essays/recipes.

This is a two-page demo + home page only.

---

## Required Behavior (Normative)

### 1) Deterministic build

A single command/function builds the entire demo site and produces byte-identical output for identical inputs.

### 2) Home page

Generate `dist/index.html` with:

* site title
* two links:

  * `/essay/`
  * `/recipe/`

The home page may be authored as a tiny Codex doc or generated; for this packet, generation is acceptable if deterministic.

### 3) Site chrome via defaults

Apply minimal header/footer markup around page bodies for both Essay and Recipe pages.

Chrome must be implemented as *defaults*, not per-page custom logic.

Minimum structure:

* `<header>` containing site title and nav links
* `<footer>` containing a small attribution line

Chrome styling must come from Architect default assets (site base CSS), not ad hoc inline styles.

### 4) Asset path correctness

All `<link href="...">` references in generated HTML must resolve to real files present under `dist/assets/` (or a deterministic equivalent).

---

## Required Public API

* `buildDemoSite(): Result<{ outputDir: string; digest: string }, BuildError[]>`

Where:

* `outputDir` is `dist/`
* `digest` is stable hash over a canonical manifest of outputs (paths + file hashes)

---

## Implementation Requirements

### A) Build orchestration

The build function MUST:

1. Build Essay page (Demo 08)
2. Build Recipe page (Demo 09)
3. Build home page
4. Copy/emit required CSS assets into `dist/assets/`
5. Ensure all link locators used in bundles point to the copied asset paths

### B) Minimal asset manifest

Compute a deterministic manifest:

* list of output files
* sha256 of each file content

Sort manifest by path.

Digest = sha256 of the manifest text.

### C) Chrome integration

Implement chrome in the HTML rendering stage (shared document wrapper), not in the ViewModel:

* `renderHtmlDocument` takes:

  * `siteTitle`
  * `navLinks`
  * `headLinks`
  * `mainHtml`
  * and wraps with `<header>`, `<main>`, `<footer>`

Chrome HTML must be identical for Essay and Recipe pages (only the `mainHtml` differs).

---

## Tests

### A) Build test

* Running `buildDemoSite()` produces:

  * `dist/index.html`
  * `dist/essay/index.html`
  * `dist/recipe/index.html`
  * `dist/assets/...` with required CSS

### B) Link integrity test

* Parse generated HTML files and verify each `<link href="...">` points to an existing file in `dist/`.

### C) Determinism test

* Run build twice → identical manifest digest.

### D) Smoke render test

* `dist/index.html` includes links to `/essay/` and `/recipe/`.

---

## Acceptance Criteria

This packet is DONE when:

* `dist/` contains a tiny but complete site with home + two pages.
* Pages include consistent chrome and styling using defaults only.
* Asset links resolve to real files under `dist/assets/`.
* Build is deterministic with stable digest.
* Tests pass.

---

## Notes

* This is intentionally the smallest “site” that still feels like a site.
* Once this is done, you can replace the fixtures with your partner’s real content and still demo the same story.
