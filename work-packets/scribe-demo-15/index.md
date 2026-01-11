# Work Packet — Scribe Demo 15

## Scope: Demo Narrative Page (Explains “Defaults” Without Exposing Internals) + Publish-Ready Output

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs:

* Existing demo build outputs (Demo 11–14)

Outputs:

* `dist/about-demo/index.html` (a narrative “what you’re seeing” page)
* Home page updated to link to `/about-demo/`

---

## Objective

You want the demo to prove:

> You can ignore Views/ViewModel/DesignPolicy/Presentation Plan and still get a complete, beautiful site.

But viewers need a short page that frames that claim *without* making them read architecture docs.

This packet adds a single, default-styled page that:

* explains what Paperhat/Codex/Architect/Scribe are in one screen
* highlights the “defaults” claim
* points to proof artifacts (optional link to `/_paperhat/manifest.json` etc.)
* remains fully static and publish-ready

This is the “sales page” for the demo site itself.

---

## Non-Goals (Explicit)

* Do **not** add marketing fluff, pricing, or adoption strategy.
* Do **not** expose internal pipeline steps in detail.
* Do **not** add analytics or tracking.
* Do **not** change schemas.

---

## Required Content (Normative)

The `/about-demo/` page MUST include these sections:

1. **What this site is**

   * “This site is generated from Codex documents using Paperhat defaults.”

2. **What “defaults” means**

   * “No custom Views, no custom CSS, no handcrafted templates.”

3. **What you can edit**

   * “Edit the `.cdx` documents to change content.”
   * “Optionally edit one DesignPolicy token file to theme the site.”

4. **What is enforced**

   * “Schemas validate the structure before rendering.”

5. **Where proof lives** (optional but recommended)

   * Link to:

     * `/_paperhat/manifest.json`
     * `/_paperhat/bundles.json`
     * `/_paperhat/validation-report.json`

Keep it short. One page.

---

## Implementation Requirements

### A) Authoring format

This page MUST be authored as a Codex document (to reinforce the story), e.g.:

* `paperhat.dev/demo/modules/site/data/page/about-demo/index.cdx`

Then rendered using defaults (like the others).

It can use a simple Concept such as:

* `Page` or `Article` or reuse `Essay` if that’s simplest.

### B) Output path

Rendered output MUST be:

* `dist/about-demo/index.html`

### C) Home page link

Home page MUST link to `/about-demo/`.

---

## Required Public API Changes

Extend the site build orchestration to include building this page:

* `buildDemoSite()` now builds:

  * home
  * essays listing (if enabled)
  * recipe page (optional)
  * about-demo page

---

## Tests

### A) Build inclusion

* `dist/about-demo/index.html` exists after build.

### B) Link test

* `dist/index.html` contains a link to `/about-demo/`.

### C) Content smoke

* The about-demo page contains the required headings/phrases.

### D) Determinism

* Build twice yields identical output and manifest digest.

---

## Acceptance Criteria

This packet is DONE when:

* The demo site includes a publish-ready `/about-demo/` page.
* The page explains defaults clearly without internal jargon.
* It is authored in Codex and rendered with defaults.
* The site build remains deterministic.

---

## Notes

* This is the page you show first when someone asks “what am I looking at?”
* It supports your adoption story without requiring a lecture.
