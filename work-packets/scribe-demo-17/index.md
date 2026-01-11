# Work Packet — Scribe Demo 17

## Scope: XML Target with XSL Defaults (Essay First)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT) *(for semantic parity)*

Inputs:

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* Validated Essay instance graph + ViewModel pipeline (Demo 05–08)
* Architect presentation bundle mechanism (Demo 10)

Outputs:

* `dist/essay/index.xml` (XML document)
* `dist/essay/index.xsl` (XSL stylesheet, default)
* `dist/essay/index.html` (optional, produced by browser XSL transform; not required as build output)

---

## Objective

Add a second target to prove the “independent targets” claim:

* Produce **semantic XML** for `Essay` by default
* Attach **default XSL** (as a concept-attached target asset) that transforms the XML into attractive HTML when opened in a browser (or via XSLT processor)
* Use the *same* “accept defaults” story:

  * no custom view authoring
  * no custom XSL required
  * defaults come from Architect

This packet focuses on `Essay` only. Recipe XML can be a follow-up packet.

---

## Non-Goals (Explicit)

* Do **not** implement generalized XML for all concepts.
* Do **not** implement full XSLT 3.0 features (keep it basic XSLT 1.0/2.0 compatible).
* Do **not** implement XML schema (XSD).
* Do **not** implement multiple XSL themes or overrides.
* Do **not** implement embedded images/audio/video.

---

## Required Behavior (Normative)

### 1) XML output is semantic, not HTML-in-XML

The produced `index.xml` MUST represent the Essay’s Concepts as XML elements.

No `<div>`, `<span>`, or CSS-class-driven markup in the XML.

### 2) XSL association

The XML MUST reference the default XSL via an XML stylesheet processing instruction:

```xml
<?xml-stylesheet type="text/xsl" href="index.xsl"?>
```

This must be emitted deterministically.

### 3) Default XSL comes from Architect

The XSL file MUST be sourced via the Architect Presentation Bundle for `(Essay, xml)`:

* concept-attached `xsl` assets
* dependency closure + dedupe + deterministic order (same mechanism as CSS)

For this packet, it is acceptable to output a single final `index.xsl` file that is assembled from ordered XSL fragments, as long as the fragments are defined as assets with dependencies.

### 4) Determinism

For identical inputs, the XML and XSL outputs must be byte-identical.

---

## XML Shape Contract (Minimum)

Root element:

```xml
<Essay id="...">
  <FrontMatter>
    <Title>...</Title>
    <Subtitle>...</Subtitle> (optional)
    <Synopsis>...</Synopsis> (optional)
    <Tags>
      <Tag>...</Tag>
      ...
    </Tags>
  </FrontMatter>

  <MainContent>
    ... blocks ...
  </MainContent>

  <BackMatter>
    <Notes>
      <Note id="n1">
        <Paragraph>...</Paragraph>
        ...
      </Note>
      ...
    </Notes>

    <References>
      <Reference id="r1">
        <Title>...</Title>
        <Authors>
          <Author>...</Author>
          ...
        </Authors>
      </Reference>
      ...
    </References>
  </BackMatter>
</Essay>
```

MainContent blocks (minimum supported in this packet):

* `Section` (nested)
* `Paragraph`
* `Quote`
* `PullQuote`
* `OrderedList` with `Item`

Ordered containers must appear in authored order.

Gloss markers:

* Do not inject HTML into XML.
* Represent `{#id}` markers as semantic XML nodes:

Option A (recommended for simplicity and clarity):

* In paragraph text, replace `{#id}` with:

  ```xml
  <Ref target="id"/>
  ```

and keep the rest as text.

This requires splitting paragraph text into mixed content; do it deterministically.

If you choose not to split, you may leave markers as literal text for this packet, but then the XSL must not claim resolved links. (I recommend splitting now; it’s a clean proof.)

---

## XSL Output Contract (Minimum)

`index.xsl` MUST transform the XML into an HTML page that is comparable in structure to the HTML default rendering:

* `<article id="essay-...">`
* `<h1>`, `<section>`, `<p>`, `<blockquote>`, `<ol>`
* Notes and references sections at end
* Anchor links:

  * `<Ref target="n1"/>` becomes a link to `#note-n1` with deterministic label `[k]`
  * `<Ref target="r1"/>` becomes a link to `#ref-r1` with deterministic label `[k]`

The XSL must be deterministic and must not depend on external network resources.

---

## Required Public API

* `buildEssayXmlDefault(inputPath: string): Result<{ xmlPath: string; xslPath: string; digest: string }, BuildError[]>`

Where:

* `xmlPath` MUST be `dist/essay/index.xml`
* `xslPath` MUST be `dist/essay/index.xsl`
* `digest` is stable hash over both outputs (manifest-style)

---

## Architect Presentation Bundle Extensions (Required)

Add target support for:

* `targetName = "xml"`
* assets with `assetKind = "xsl"`

Provide a Presentation Bundle for:

* `(Essay, xml)` including:

  * a default view id (can be a symbolic `"default-xsl"`)
  * XSL assets, at minimum:

    * `xsl.base` (root stylesheet skeleton)
    * `xsl.blocks` (templates for Paragraph/Section/Quote/List)
    * `xsl.refs` (Ref → anchors, notes, references numbering)
  * explicit dependencies so assembly order is deterministic

Retrieval API stays the same:

* `getPresentationBundle("Essay", "xml")`

---

## Assembly Rules for XSL Assets (Normative for this packet)

Because XSL must be a single well-formed stylesheet document, define:

* One asset is the **root shell** containing:

  * `<xsl:stylesheet ...>`
  * `<xsl:output ...>`
  * a placeholder marker like `<!-- ASSET_INSERTION_POINT -->`
  * closing `</xsl:stylesheet>`

All other XSL assets contribute one or more `<xsl:template>` blocks (and optional `<xsl:key>` declarations), inserted at the insertion point in deterministic order.

If more than one asset claims to be the root shell, that is an error.

---

## Tests

### A) Build outputs

* `dist/essay/index.xml` exists and is well-formed XML.
* `dist/essay/index.xsl` exists and is well-formed XSL.

### B) Determinism

* Build twice → byte-identical XML + XSL, identical digest.

### C) Shape checks

* XML contains `<Essay id="...">` and expected child elements.
* XML contains blocks in correct order.

### D) XSL transform smoke test (optional but recommended)

* Run an XSLT processor in tests (or a minimal library call) to transform XML → HTML string.
* Verify output contains `<article>`, `<h1>`, and at least one `<p>`.

### E) Ref links

* If XML includes `<Ref target="..."/>`, transformed HTML includes anchor links.

---

## Acceptance Criteria

This packet is DONE when:

* The Essay builds to semantic XML with an attached default XSL.
* Opening `dist/essay/index.xml` in a browser produces a readable HTML page via XSL (manual check).
* The XSL is delivered via Architect defaults and assembled deterministically.
* Output is deterministic and tests pass.

---

## Notes

* This is the best “second target” because it demonstrates:

  * semantic separation
  * default presentation assets
  * target independence
  * inspectable intermediates
