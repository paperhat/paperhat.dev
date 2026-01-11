# Work Packet — Scribe Demo 02

## Scope: Codex Parse → AST (Essay + Recipe fixtures only)

Status: PROPOSED  
Governing Docs:

* Codex Language Specification (v0.1)
* Architect Essay Schema Specification (v0.1)
* Architect Recipe Schema (v0.1) (as applicable)

Golden fixtures (inputs):

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

---

## Objective

Implement a deterministic Codex parser that can parse the two golden fixture documents into a canonical AST suitable for subsequent lowering to RDF.

This packet proves that:

* the language can be parsed reliably
* comments are ignored correctly
* text content is preserved correctly
* ordering is preserved (as authored)
* errors are precise and deterministic

This packet authorizes **parsing only**. No RDF, no validation, no rendering.

---

## Non-Goals (Explicit)

* Do **not** implement schema validation (SHACL or otherwise).
* Do **not** lower to RDF.
* Do **not** interpret Gloss beyond treating it as opaque text.
* Do **not** implement identifier resolution.
* Do **not** implement any “reformat” or “pretty print” output.

---

## Inputs

Codex source files:

* `paperhat.dev/demo/modules/essay/data/essay/index.cdx`
* `paperhat.dev/demo/modules/recipe/data/recipe/index.cdx`

---

## Outputs

### A) In-memory AST

A deterministic AST representing the document.

### B) Parse diagnostics

On failure, return deterministic diagnostics with:

* filename
* 1-based line number
* a short error code (string)
* a human-readable message

Diagnostics MUST NOT be verbose.

---

## AST Data Model (Normative for this packet)

### Node kinds

#### 1) `Document`

* `kind: "Document"`
* `root: ElementNode`

#### 2) `Element`

* `kind: "Element"`
* `name: string` (e.g. `"Essay"`, `"Section"`)
* `traits: Trait[]`
* `children: ChildNode[]`

#### 3) `Trait`

* `name: string`
* `value: TraitValue`

`TraitValue` is one of:

* `StringValue` (raw string with escapes resolved according to the Codex string rules)
* `NumberValue` (string form preserved OR parsed numeric; choose one and be consistent)
* `BooleanValue` (`true`/`false`)
* `IdentifierValue` (unquoted token form, if your spec distinguishes it)
* `ListValue` (for `[...]` lists if present in your v0.1; if not, omit)

#### 4) `Text`

* `kind: "Text"`
* `text: string`

Text nodes are used only for the **opaque content inside multi-line text-bearing Concepts**.

#### 5) `Comment` (discarded)

Comments of the form `[ ... ]` MUST be ignored completely and MUST NOT appear in the AST.

---

## Parsing Rules (Minimum Required)

These rules are the minimum needed to parse the two fixtures correctly.

### 1) Exactly one root Concept

A document MUST contain exactly one top-level Element (the root).

### 2) Element syntax

Support these forms:

* **Open/close pair**

  * `<Concept ...>`
  * children
  * `</Concept>`

* **Self-closing**

  * `<Concept ... />`

### 3) Traits / attributes

Support:

* `name="string"` (quoted string)
* `name=number` (unquoted numeric)
* `name=true|false` (unquoted boolean)
* Mixed trait ordering and multi-line trait blocks as in the Recipe fixture.

Trait parsing MUST preserve:

* trait names
* trait values

Whitespace/newlines between traits are insignificant.

### 4) Indentation

Indentation MUST be accepted as in the fixtures (tabs used).

The parser MUST NOT infer semantics from indentation, but it MAY use indentation to improve error messages.

### 5) Text content

Inside a non-self-closing element, text may appear as lines between child elements.

For this packet:

* Preserve text content for:

  * `Title`, `Subtitle`, `Synopsis`, `Summary`, `Paragraph`, `Heading`, `Item` content blocks, etc., as they appear in fixtures
* Preserve internal newlines as `\n` where they occur between text lines.
* Trim only the leading/trailing blank lines that are purely structural indentation, if necessary for cleanliness—but be deterministic.
  (If unsure, preserve exactly and deal with normalization later.)

### 6) Comments

Lines of the form:

* `[This is a comment.]`

MUST be ignored entirely.

They may appear:

* between elements
* adjacent to elements
* inside containers

### 7) Error handling

The parser MUST detect:

* unterminated tag
* mismatched closing tag name
* invalid trait syntax
* multiple roots
* unexpected EOF (unclosed element)

And return deterministic diagnostics.

---

## Required Public API (for this packet)

Define one function:

* `parseCodexDocument(input: { path: string; text: string }): Result<DocumentAst, ParseError[]>`

Where:

* `DocumentAst` matches the model above
* `ParseError` includes `path`, `line`, `code`, `message`

If you already have Toolsmith `Result`, use it. Otherwise return a simple discriminated union, but keep it minimal.

---

## Tests

### Golden fixture tests (mandatory)

1. `Essay` parses successfully and produces:

* root element name `Essay`
* presence of expected child Concepts (FrontMatter, Exposition/MainText, BackMatter)
* ordered child preservation for known ordered containers (verify order matches the file)

2. `Recipe` parses successfully and produces:

* root element name `Recipe`
* `Ingredients` contains expected sequence of `Ingredient` children in order
* `Steps` contains expected sequence of `Step` children in order

### Negative tests (mandatory)

Create small inline test strings:

* mismatched close tag
* missing `>`
* unterminated quoted string trait
* duplicate root elements

Each must produce a deterministic error with correct line.

---

## Acceptance Criteria

This packet is DONE when:

* Both golden fixtures parse into AST successfully.
* Comments are ignored (not present in AST).
* Text blocks are preserved deterministically.
* The AST preserves authored order of element children.
* Required negative tests produce deterministic diagnostics.

---

## Notes

* Treat Gloss markup inside text as opaque. Do not parse it.
* Do not attempt to “validate” Concept names or traits against schemas here.
* Keep the parser strict. If something isn’t in the fixtures or spec, error out.
