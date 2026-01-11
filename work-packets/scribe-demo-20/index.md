# Work Packet — Scribe Demo 20

## Scope: Recipe → XML Target with XSL Defaults (Reuse XML+XSL Mechanism)

Status: PROPOSED  
Governing Docs:

* Scribe Demo 17 — XML Target with XSL Defaults (Essay) (PROPOSED)
* Architect Runtime Contract — Default Presentation Bundles (v0.1)

Inputs:

* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`
* Validated Recipe instance graph pipeline (Demo 03–05)
* Architect Presentation Bundle system extended for `target="xml"` and `assetKind="xsl"` (Demo 17)

Outputs:

* `dist/recipe/index.xml`
* `dist/recipe/index.xsl`

---

## Objective

Add XML+XSL output for Recipe, proving the target system is domain-general:

* same deterministic XML output principle
* same XSL assembly and concept-attached assets
* same “open XML in browser → see rendered HTML” experience

This packet does not produce PDF. It is the XML counterpart only.

---

## Non-Goals (Explicit)

* Do **not** implement Recipe → PDF (that will be Demo 21).
* Do **not** implement advanced XML mixed-content splitting for Recipe unless needed.
* Do **not** implement tables, images, audio/video.

---

## XML Shape Contract (Minimum)

Output must be semantic XML:

```xml
<Recipe id="...">
  <Title>...</Title>
  <Summary>...</Summary> (optional)

  <Servings amount="..." unit="..." />
  <PreparationTime duration="..." unit="..." /> (optional)
  <CookingTime duration="..." unit="..." /> (optional)

  <Ingredients>
    <Ingredient name="..." amount="..." unit="..." optional="true|false" preparation="..." toTaste="true|false" />
    ...
  </Ingredients>

  <Equipment>
    <Item>...</Item>
    ...
  </Equipment>

  <Steps>
    <Step optional="true|false">...</Step>
    ...
  </Steps>

  <Tags>
    <Tag>...</Tag>
    ...
  </Tags>

  <Source>...</Source> (optional)
</Recipe>
```

Ordering:

* Ingredients, Equipment items, Steps, Tags MUST appear in authored order.

---

## XSL Contract (Recipe XML → HTML)

`dist/recipe/index.xsl` MUST:

* render to an HTML page with:

  * `<article id="recipe-...">`
  * `<h1>` title
  * ingredients list
  * steps list
  * optional summary/source
  * simple layout sections
* be deterministic and self-contained

The XML MUST include:

```xml
<?xml-stylesheet type="text/xsl" href="index.xsl"?>
```

---

## Architect Bundle Requirement

Provide a Presentation Bundle for `(Recipe, xml)` containing XSL assets:

Minimum assets:

* `recipe.xml.xsl.shell`
* `recipe.xml.xsl.blocks` (templates for Ingredient/Step/Item etc.)
* `recipe.xml.xsl.layout` (overall HTML skeleton)

Dependencies explicit.

Assembly rules same as Demo 17:

* exactly one root shell
* insert templates deterministically

---

## Required Public API

* `buildRecipeXmlDefault(inputPath: string): Result<{ xmlPath: string; xslPath: string; digest: string }, BuildError[]>`

Where:

* `xmlPath` MUST be `dist/recipe/index.xml`
* `xslPath` MUST be `dist/recipe/index.xsl`
* `digest` is stable over both outputs

---

## Tests

### A) Output existence + well-formedness

* XML is well-formed and contains expected elements.
* XSL is well-formed.

### B) Determinism

* Build twice → byte-identical XML + XSL.

### C) Transform smoke test (optional)

* Apply XSLT to XML and verify:

  * output contains `<h1>` with recipe title
  * output contains at least one ingredient and one step

---

## Acceptance Criteria

This packet is DONE when:

* Recipe builds to `index.xml` + `index.xsl` deterministically.
* Default XSL comes from Architect bundle assembly.
* Opening `index.xml` in a browser produces a readable page (manual check).
* Tests pass.

---
