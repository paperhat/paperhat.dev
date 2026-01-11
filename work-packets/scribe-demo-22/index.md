# Work Packet — Scribe Demo 22

## Scope: Tables + Figures (Image) Across HTML + XML/XSL + PDF/FO (Essay First)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)
* Scribe Demo 17 — XML Target with XSL Defaults (Essay) (PROPOSED)
* Scribe Demo 18 — PDF Target via XSL-FO (Essay) (PROPOSED)

Inputs:

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx` *(updated to include at least one Table and one Figure)*
* Existing pipeline: parse → RDF → validate → ViewModel → render (HTML/XML/FO)

Outputs:

* HTML: `dist/essay/index.html` renders Table + Figure using defaults
* XML: `dist/essay/index.xml` contains semantic `<Table>` + `<Figure>`
* XSL: `dist/essay/index.xsl` renders those to HTML when opening XML
* FO: `dist/essay/index.fo` renders those
* PDF: `dist/essay/index.pdf` includes those (per PDF policy)

---

## Objective

Add two high-value scholarly constructs—**Table** and **Figure**—end-to-end across targets using defaults only:

* Conceptual structure is validated (SHACL)
* Projections are semantic (XML)
* Presentations are default assets (CSS/XSL/FO)
* Deterministic output is preserved

This is the minimum set that makes essays feel “real” for consulting briefs/tutorials/cheat-sheets.

---

## Non-Goals (Explicit)

* Do **not** implement complex table features (rowspan/colspan) unless required by fixture.
* Do **not** implement charts/plots generation.
* Do **not** implement image embedding from arbitrary sources beyond a simple locator.
* Do **not** implement captions/numbering beyond minimal deterministic numbering.
* Do **not** implement TableOfContents/TableOfFigures derivation (later packet if desired).

---

## Concepts and Traits (Locked for this packet)

### New Concepts (Essay content blocks)

* `Figure` *(ordered container)*
* `Image` *(entity or not; your choice, but must have stable locator)*
* `Caption` *(text-bearing)*
* `Table` *(ordered container)*
* `TableHeader` *(ordered container)*
* `TableBody` *(ordered container)*
* `Row` *(ordered container)*
* `Cell` *(text-bearing; may later support richer content)*

### Required Traits

* `Figure`: optional `id`
* `Image`: `src` (string locator), optional `alt`
* `Table`: optional `id`
* `Cell`: optional `align` (string enum: `"left"|"center"|"right"`), optional `role` (e.g. `"header"`)

*(Keep traits minimal. No abbreviations.)*

---

## Schema Requirements (Demo 04 Compilation)

Update Codex-authored schemas so SHACL enforces:

### Figure

* `Figure` may contain:

  * exactly 1 `Image`
  * optional 1 `Caption`
* `Image` MUST have `src` trait

### Table

* `Table` must contain exactly:

  * optional `Caption`
  * exactly 1 `TableHeader`
  * exactly 1 `TableBody`
* `TableHeader` contains 1+ `Row`
* `TableBody` contains 1+ `Row`
* each `Row` contains 1+ `Cell`
* optional rule (recommended): all rows have the same number of cells as the first header row

  * If you can’t express this cleanly in SHACL without SPARQL constraints, skip it in v0.1 (don’t half-implement).

All these concepts that represent ordered content MUST be marked `isOrderedContainerConcept=true` in schema metadata (consistent with your “least surprise” rule).

---

## HTML Target (Defaults)

### ViewModel additions (Demo 06)

Extend Essay ViewModel to include two new block types:

#### Figure

```json
{
  "type": "Figure",
  "id": "string|null",
  "image": { "src": "string", "alt": "string|null" },
  "caption": "string|null"
}
```

#### Table

```json
{
  "type": "Table",
  "id": "string|null",
  "caption": "string|null",
  "header": [ ["cell", ...], ... ],
  "body": [ ["cell", ...], ... ]
}
```

Cells are plain text strings for v0.1.

### HTML rendering rules (Demo 01 renderer)

* `Figure` → `<figure>` containing `<img src alt>` and optional `<figcaption>`
* `Table` → `<table>` with `<caption>` optional, `<thead>` and `<tbody>`
* preserve authored order of rows/cells

### CSS defaults (Demo 10)

Add concept-attached CSS assets for:

* `Figure`, `Table`, `Caption`, `Row`, `Cell` *(or just `Figure` + `Table` if you keep it simple)*

Minimal styling:

* figure centered, caption muted
* table with readable spacing, borders, zebra striping optional, responsive overflow

---

## XML Target (Demo 17)

### XML projection rules

Emit semantic XML:

```xml
<Figure id="...">
  <Image src="..." alt="..." />
  <Caption>...</Caption>
</Figure>

<Table id="...">
  <Caption>...</Caption>
  <TableHeader>
    <Row><Cell>...</Cell>...</Row>
  </TableHeader>
  <TableBody>
    <Row>...</Row>
  </TableBody>
</Table>
```

No HTML-ish tags in XML.

### XSLT defaults (Architect bundle for `Essay, xml`)

Add templates for:

* `Figure` → HTML `<figure>` structure
* `Table` → HTML `<table>` structure

Deterministic numbering (optional but recommended):

* If you want “Figure 1” / “Table 1”:

  * In XSLT: use `xsl:number` over `Figure` and `Table` elements in document order
  * Keep it simple: “Figure 1”, “Table 1”

If you don’t number, that’s fine—just render captions.

---

## FO/PDF Target (Demo 18)

### FO transform (Architect bundle for `Essay, pdf`)

Add templates for:

* `Figure`

  * render image only if your FO engine supports external-graphics reliably
  * else render a placeholder block with the image src (acceptable for v0.1 demo if needed)
* `Table`

  * use `<fo:table>`, `<fo:table-header>`, `<fo:table-body>`, `<fo:table-row>`, `<fo:table-cell>`

Caption rendering:

* as italic/muted block above figure/table (or below figure, above table—choose one and be consistent)

Image handling policy (normative decision for v0.1)
Choose one:

**Option A (preferred):** Support external graphics in FO

* `Image src` is a file path or URL that the FO engine can load deterministically
* Demo assets are local under `dist/assets/images/...` to avoid network variability

**Option B:** Placeholder-only in PDF

* Render a box with the image filename/src and caption
* (Still proves the pipeline across targets without fighting FO image handling.)

Pick one and lock it for demo v0.1.

---

## Asset/Bundles Updates (Architect)

You must add presentation bundle assets for:

* `(Essay, html)` CSS: table/figure styles (concept-attached)
* `(Essay, xml)` XSL: templates for table/figure
* `(Essay, pdf)` XSL: FO templates for table/figure

Dependencies explicit, no cycles.

---

## Required Public APIs (minimal changes)

* Extend `projectEssayViewModel(...)` to support Figure/Table nodes
* Extend HTML renderer to handle new block types
* Extend XML emitter to include semantic nodes
* Extend XSLT/FO assets to transform/render them

No changes to core pipeline stages.

---

## Tests

### A) Schema validation

* Updated Essay fixture with Figure/Table validates successfully.
* Negative fixture:

  * Figure missing Image src → fails validation deterministically
  * Table missing TableHeader or TableBody → fails deterministically

### B) HTML output smoke

* Generated HTML contains:

  * `<figure>` with `<img>`
  * `<table>` with `<thead>` and `<tbody>`

### C) XML output smoke

* Generated XML contains `<Figure>` and `<Table>` elements.

### D) XSL transform smoke (optional)

* Transform XML→HTML and confirm `<figure>` and `<table>` exist.

### E) FO output smoke

* FO contains `<fo:table>` at least once.
* If Option A for images: FO contains `<fo:external-graphic>` with correct src.

### F) Determinism

* Build twice → FO byte-identical; HTML/XML/XSL byte-identical.
* PDF per Demo 19 policy (Tier A or Tier B) remains stable.

---

## Acceptance Criteria

This packet is DONE when:

* Essay can include Table and Figure content in Codex.
* SHACL enforces minimum structure.
* HTML, XML+XSL, and PDF/FO all render them using defaults.
* Outputs remain deterministic under your demo determinism policy.
* Tests pass.
