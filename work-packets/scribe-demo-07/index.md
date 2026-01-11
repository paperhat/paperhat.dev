# Work Packet — Scribe Demo 07

## Scope: Gloss Resolution for `{#id}` References in ViewModel Text (Notes + References)

Status: PROPOSED  
Governing Docs:

* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)
* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)

Inputs:

* Essay ViewModel produced by Demo 06
* Validated Essay instance graph (Demo 05), for reference existence checks

Output:

* Essay ViewModel with Gloss references resolved to HTML anchors in text fields

---

## Objective

Implement the minimal Gloss feature required for the demo:

* recognize `{#id}` markers embedded in paragraph text
* verify that `id` resolves to an existing Note or Reference entity in the document
* replace markers with deterministic HTML anchor links

This packet makes the demo feel “real”: citations and notes work without any inline concepts.

---

## Non-Goals (Explicit)

* Do **not** implement full Gloss language.
* Do **not** implement rich inline styling or spans.
* Do **not** implement bibliography formatting rules.
* Do **not** implement cross-document resolution.
* Do **not** implement `{today}`, `{now}`, or other special forms.

Only `{#id}`.

---

## Gloss Marker Definition (Normative for this packet)

A Gloss reference marker is:

* literal `{#`
* followed by one or more characters forming `id`
* followed by `}`

Example:

* `{#n1}`
* `{#ref-foo}`

`id` MUST match the identifier rules already used for Entities (treat as a raw token for now).

Markers MUST NOT be nested.

---

## Resolution Rules (Normative)

### 1) Identify resolvable targets

A marker `{#id}` is resolvable if `id` refers to:

* a Note entry in `viewModel.backMatter.notes[*].id`, OR
* a Reference entry in `viewModel.backMatter.references[*].id`

For this packet, these are the only resolvable target sets.

### 2) Link targets

Replace `{#id}` with an `<a>` element with:

* `href="#note-<id>"` if it resolves to a Note
* `href="#ref-<id>"` if it resolves to a Reference

Anchor **text** MUST be deterministic:

* Notes: `"[<k>]"` where `k` is the 1-based position of the note in the rendered Notes list order.
* References: `"(…)"` is not allowed (too style-like). Use `"[<k>]"` as well, where `k` is 1-based position of the reference in the rendered References list order.

If Notes/References are considered unordered semantically, the renderer still needs deterministic order. For this packet:

* Preserve authored order as present in the ViewModel arrays.

### 3) Multiple references

Text may contain multiple markers. Each must be resolved independently.

### 4) Unknown id

If `{#id}` does not resolve:

* This MUST be an error, and rendering MUST NOT proceed.
* Provide a deterministic error including `id` and a small snippet of surrounding text.

### 5) Escaping

Do not attempt to escape HTML in this packet beyond what is necessary to avoid breaking output:

* The anchor HTML you inject MUST be valid.
* The surrounding text is treated as already-safe for the demo pipeline (full HTML escaping policy can be a later contract).

---

## Required Public API

* `resolveGlossReferencesInEssayViewModel(input: EssayViewModel): Result<EssayViewModel, GlossError[]>`

Where `GlossError` includes:

* `code`
* `id` (the unresolved id)
* `message`

---

## Implementation Requirements

### 1) Pure transformation

This function MUST be pure:

* It takes a ViewModel
* Returns a modified ViewModel (or errors)
* No I/O

### 2) Where to apply replacements

Apply replacement to all `text` fields in:

* `Paragraph` blocks throughout `mainContent`
* `Paragraph` blocks inside `Section.content`
* Quote/PullQuote paragraph blocks
* OrderedList item paragraph blocks
* Note content paragraph blocks
* Reference fields may be left untouched unless they contain markers (rare)

### 3) Replacement strategy

Use a deterministic scan:

* find all `{#...}` markers
* replace with computed anchor HTML string

Do not use regexes that may behave differently across engines unless tested.

---

## Tests

### A) Golden Essay reference resolution

* The golden essay contains at least one `{#...}` marker.
* After resolution:

  * marker is replaced with `<a href="#note-...">[k]</a>` or `<a href="#ref-...">[k]</a>`
  * all markers are resolved
  * output is deterministic

### B) Multiple markers in one paragraph

* A paragraph with two markers results in two anchors.

### C) Unknown id failure

* A paragraph containing `{#does-not-exist}` fails with deterministic error.

### D) Determinism

* Running resolution twice yields identical output (canonical stringify).

---

## Acceptance Criteria

This packet is DONE when:

* The golden Essay ViewModel is transformed with working anchor links for all `{#id}` markers.
* Unknown ids are rejected deterministically.
* Output is deterministic across runs.
* Tests pass.

---

## Notes

* This packet purposely uses ViewModel arrays for determining `[k]` numbering.
* Later versions may introduce formatting policies; do not pre-empt them here.
