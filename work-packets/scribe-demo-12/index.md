# Work Packet — Scribe Demo 12

## Scope: “Drop-in CMS” Demo for Partner Site (Essays Collection) with Defaults Only

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs:

* A folder of Essay Codex documents (multiple essays) under the demo module, e.g.

  * `paperhat.dev/demo/modules/essay/data/essay/` containing:

    * `index.cdx` (existing golden essay)
    * `how-to-run-a-workshop/index.cdx`
    * `brief-on-risk/index.cdx`
    * `newsletter-2026-01/index.cdx`
      (exact names are illustrative; any subfolders with `index.cdx` count as essays)

Outputs:

* `dist/index.html` (home)
* `dist/essays/index.html` (essays listing)
* `dist/essays/<id>/index.html` (one page per essay)
* plus existing `dist/recipe/index.html` if you keep it in the demo

---

## Objective

Demonstrate the “CMS with defaults” story:

* author multiple essays as plain Codex files
* run a single build
* get a complete, attractive site:

  * an essays listing page
  * stable URLs per essay
  * default styling, chrome, and links
* with **no custom views and no custom CSS**

This is the first demo that looks like a real consulting/newsletter site.

---

## Non-Goals (Explicit)

* Do **not** implement tagging pages, search, RSS, sitemap.
* Do **not** implement pagination.
* Do **not** implement drafts/publishing workflow.
* Do **not** implement CMS editing UI.
* Do **not** implement image assets or embeds beyond what the current schema supports.

---

## Required Behavior (Normative)

### 1) Discover essays deterministically

Scan the essays data directory and discover all essay documents:

* Any directory containing `index.cdx` under `.../data/essay/` is an essay item.
* The stable URL segment for each essay is the Essay’s `id` trait, not the folder name.
* If two essays share an id, build MUST fail deterministically.

Discovery order MUST be deterministic:

* sort by filesystem path ascending *only for discovery stability*
* final listing order is defined below.

### 2) Build all essays

For each discovered essay:

* run the full pipeline (parse → RDF → validate → ViewModel → gloss → render → assets)
* output to:

  * `dist/essays/<essayId>/index.html`

### 3) Build essays listing page (defaults)

Generate:

* `dist/essays/index.html`

Listing includes for each essay:

* title
* optional synopsis
* link to the essay page

Listing order MUST be deterministic and default-friendly:

* primary: title ascending (case-insensitive)
* secondary: essay id ascending

(If you later add publish dates, you can change ordering by version.)

### 4) Home page links

`dist/index.html` MUST include:

* link to `/essays/`
* link to `/recipe/` may remain optional

### 5) Defaults only

No custom views or CSS are allowed in this packet.

* Use Architect default presentation bundles only.

---

## Required Public API

* `buildEssayCollectionSite(inputRootDir: string): Result<{ outputDir: string; digest: string }, BuildError[]>`

Where:

* `inputRootDir` points at `paperhat.dev/demo/modules/essay/data/essay/`
* `outputDir` is `dist/`
* `digest` is stable hash over manifest of outputs

---

## Required Data Extraction for Listing

From each essay’s validated ViewModel, extract:

* `id`
* `frontMatter.title`
* `frontMatter.synopsis` (nullable)

Do not attempt to infer author/date.

---

## Error Handling (Normative)

Build MUST fail if:

* any essay fails parse/validate/projection
* duplicate essay ids
* missing required title
* listing generation encounters missing fields

Errors must include:

* stage (Discover, Parse, Validate, Project, Render, Write)
* path
* essay id when known

Ordering of errors must be deterministic (by stage order then path).

---

## Tests

### A) Discovery tests

* With a directory containing 3 essays, discovery finds exactly 3.
* Duplicate id causes deterministic failure.

### B) Build tests

* `dist/essays/index.html` exists.
* Each essay outputs to `dist/essays/<id>/index.html`.

### C) Listing content tests

* Listing includes links for each essay id.
* Titles appear as rendered text.

### D) Determinism

* Build twice → identical manifest digest.

---

## Acceptance Criteria

This packet is DONE when:

* You can drop multiple Essay documents into the essays data folder.
* A single build generates a multi-page site with an essays index and stable URLs.
* Everything uses defaults only.
* Output is deterministic.
* Tests pass.

---

## Notes

* This is the demo you show your partner: “write newsletters/briefs/essays in Codex; get a real site.”
* Once this exists, adding About/Contact/Policies is just “more content types,” not a different architecture.
