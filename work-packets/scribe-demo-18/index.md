# Work Packet — Scribe Demo 18

## Scope: PDF Target via XSL-FO (Essay First, Reuse XML)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Scribe Demo 17 — XML Target with XSL Defaults (Essay) (PROPOSED)

Inputs:

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* The **semantic XML** output produced by Demo 17:

  * `dist/essay/index.xml`
* Architect Presentation Bundle mechanism (Demo 10) extended for FO assets

Outputs:

* `dist/essay/index.fo` (XSL-FO document)
* `dist/essay/index.pdf` (PDF)

---

## Objective

Add a third target that proves “real document publishing” without changing semantics:

1. Produce **semantic XML** (reuse Demo 17 output)
2. Apply **default XSLT** (Architect-owned) to transform XML → **XSL-FO**
3. Run an **FO processor** deterministically to generate **PDF**
4. All default assets and view selection come from Architect bundles (no custom author work)

This is the “serious” target that validates Paperhat’s long-term promise.

---

## Non-Goals (Explicit)

* Do **not** implement full typesetting features (widows/orphans control, floats, complex tables) beyond what the Essay fixture needs.
* Do **not** support every Concept; only those present in the golden Essay fixture.
* Do **not** implement per-page overrides, themes, or user customization.
* Do **not** implement embedded images/audio/video.
* Do **not** implement TOC generation from headings unless trivially required (can be a later packet).

---

## Target Definition

### Target name

* `targetName = "pdf"`

### Asset kinds

* `assetKind = "xsl"` for XML→FO transform (XSLT stylesheet)
* optionally `assetKind = "fo-fragment"` if you want modular FO snippets; but simplest is just XSL assets assembled like Demo 17.

(For determinism and simplicity, prefer the same XSL assembly mechanism as Demo 17.)

---

## Required Behavior (Normative)

### 1) XML is authoritative intermediate

The PDF build MUST consume `dist/essay/index.xml` as its semantic source (not HTML, not ViewModel).

### 2) Default FO transform comes from Architect

Retrieve a Presentation Bundle for `(Essay, pdf)` containing:

* exactly one **root** XSL shell asset (well-formed stylesheet doc)
* one or more template assets inserted deterministically
* explicit dependency edges for deterministic assembly

### 3) Deterministic FO output

The generated `dist/essay/index.fo` MUST be byte-identical for identical inputs (XML + bundle contents).

### 4) Deterministic PDF output (pragmatic)

PDF byte-for-byte determinism is hard across FO engines and timestamps. For this packet:

* We REQUIRE deterministic FO.
* For PDF:

  * Either (A) configure the FO engine to suppress timestamps/metadata so bytes are stable, **or**
  * (B) define determinism as “structurally identical PDF” and compute digest over a normalized representation (e.g., strip metadata) if the engine can’t be made stable.

Pick A if feasible; otherwise do B and make it explicit in the manifest.

### 5) Fail-fast

If XML→FO transform fails or FO→PDF fails, build fails and produces no partial output.

---

## FO Output Contract (Minimum)

The `.fo` MUST be a valid XSL-FO document with:

* `<fo:root>`
* a simple page master (single-column)
* `<fo:flow flow-name="xsl-region-body">`
* block layout for:

  * Title
  * optional subtitle/synopsis
  * sections/headings
  * paragraphs
  * block quotes
  * ordered lists
  * notes / references

No attempt at fancy typography yet—just clean and readable.

---

## XSLT Contract (XML → FO)

### 1) XSLT uses XPath internally (allowed)

XPath use is expected and required; it is not user-authored.

### 2) Notes / references anchors

FO doesn’t use HTML anchors the same way. For this packet:

* Convert `<Ref target="n1"/>` into a **numbered inline** (e.g., `[1]`) in FO output.
* In the Notes section, render notes with matching numbers (based on note order).
* Same for references.

No clickable internal links required yet (can be later).

---

## Required Public API

* `buildEssayPdfDefault(inputPath: string): Result<{ foPath: string; pdfPath: string; digest: string }, BuildError[]>`

Where:

* `foPath` MUST be `dist/essay/index.fo`
* `pdfPath` MUST be `dist/essay/index.pdf`
* `digest` must include:

  * FO digest always
  * PDF digest (raw or normalized; choose and document)

---

## FO Engine Requirement

Choose **one** FO engine for the demo and make it deterministic.

Recommended demo choice (because it’s widely available and scriptable):

* **Apache FOP** (invoked via CLI)

Implementation must treat the engine as a build dependency with deterministic invocation.

If using Apache FOP, invoke like:

* `fop -fo dist/essay/index.fo -pdf dist/essay/index.pdf`

(Exact flags depend on your environment; keep them fixed and documented.)

---

## Architect Presentation Bundle Extensions (Required)

Add a bundle for `(Essay, pdf)` with XSL assets:

Minimum assets:

* `fo.xsl.shell` (root stylesheet skeleton + insertion point)
* `fo.xsl.blocks` (paragraphs, sections, lists, quotes)
* `fo.xsl.frontmatter` (title/subtitle/synopsis)
* `fo.xsl.backmatter` (notes + references rendering)
* `fo.xsl.refs` (Ref → numbering logic)

All dependencies explicit.

Retrieval:

* `getPresentationBundle("Essay", "pdf")`

---

## Assembly Rules (Same as Demo 17)

* Exactly one “root shell” stylesheet.
* Insert template fragments in deterministic topological order (ties by `assetId`).
* Error if:

  * multiple shells
  * missing dependency
  * cycle

---

## Tests

### A) FO generation tests

* `dist/essay/index.fo` exists
* it contains `<fo:root>` and expected basic structure
* determinism: two builds produce identical FO bytes and identical FO digest

### B) PDF generation smoke tests

* `dist/essay/index.pdf` exists
* file size > 0
* optional: extract metadata (if available) and confirm expected title text exists (smoke only)

### C) Failure tests

* Break the FO XSL (intentional) → build fails at stage `TransformFo` (or similar), no PDF written.

---

## Error Model (Stages)

Build errors must include stage:

* `XmlInput`
* `PresentationBundle`
* `AssembleXsl`
* `TransformFo`
* `FoToPdf`
* `Write`

---

## Acceptance Criteria

This packet is DONE when:

* Running `buildEssayPdfDefault(...)` produces:

  * `dist/essay/index.fo`
  * `dist/essay/index.pdf`
* FO is deterministic across runs.
* PDF is generated reliably (and deterministic if engine allows).
* All assets come from Architect defaults (no stubs).
* Tests pass.

---

## Notes

* This packet intentionally makes PDF “look good enough” but not perfect.
* The next follow-up packet after this is obvious and safe:

  * **Recipe → XML → FO → PDF** (same pipeline, different schema)
