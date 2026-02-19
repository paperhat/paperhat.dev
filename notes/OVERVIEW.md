# The Paperhat System: Codex, Gloss, and Workshop

## What This Is

Paperhat is a semantic document authoring and processing system. It captures structured meaning in documents, validates that meaning against schemas, computes derived values, applies design constraints, and produces finished output for multiple targets — web, PDF, ePub, print, applications.

The system has three layers, each an independent specification with a FOSS Apache 2.0 Rust reference implementation:

- **Codex** — a declarative markup language for structured semantic data
- **Gloss** — an inline annotation language that binds spans of text to semantic references
- **Workshop** — a deterministic processing pipeline that consumes Codex and Gloss documents and produces finished artifacts

Each layer does one thing. Each refuses to do anything else. The boundaries are enforced by specification, not convention.

## The Core Thesis

Most document systems treat formatting as the primary concern. You write content, then you style it. The styling is tightly coupled to the output format — CSS for the web, LaTeX for print, platform-specific code for apps. Change the target and you redo the work.

Paperhat inverts this. Documents carry meaning, not formatting. A document declares that something is a person's name, a recipe ingredient, a warning — not that it's bold, red, or 16 pixels tall. Schemas define what kinds of things exist and what properties they have. The system validates documents against these schemas, computes derived values, and only at the very end translates everything into format-specific output through target-specific renderers called Foundries.

The entire pipeline is deterministic. Same inputs, same outputs, always, provably. Content-addressed imports, Merkle hash trees, canonical byte sequences, checkpointed pipeline state. The semantic universe for a repository can be rebuilt from scratch and proven identical to a previous build.

## Codex

Codex is a markup language for capturing what things are — a person, a recipe, an event, a book — along with their properties, relationships, and content. It uses angle-bracket syntax that superficially resembles XML but has fundamentally different semantics.

### The Problem It Solves

Existing data formats force tradeoffs. JSON has six types — everything else is convention. YAML infers types in ways that routinely cause bugs (`no` becomes `false`, `3.10` becomes `3.1`). XML is verbose and conflates structure with presentation. Markdown is for prose, not data. HTML mixes meaning with appearance at every level.

None of them produce a single canonical byte sequence for the same information. None of them round-trip losslessly through a semantic database and back. None of them have a type system rich enough to distinguish a fraction from a decimal, a date from a timestamp, or a color in one color space from the same color in another.

### What Codex Does

**One canonical form.** Every valid Codex document has exactly one correct byte sequence — tabs for indentation, alphabetical trait ordering, deterministic line-wrapping at 100 characters. Two people writing the same information produce the same file. No style arguments.

**Rich value types determined by lexical form.** Codex has over 30 value types recognized purely by how you write them — no schema needed for the parser to identify the type:

- Text: `"The Hobbit"` or `` `The Hobbit` ``
- Numbers: `42` (integer), `3.14` (decimal), `1/3` (fraction — never reduced, author's spelling preserved), `3.14p2` (precision number with declared measurement precision), `2+3i` (complex number)
- Temporal: `{2024-03-15}` (date), `{2024-03-15T14:30:00Z}` (instant), `{P1Y2M3D}` (duration) — 10 temporal types aligned with the TC39 Temporal proposal
- Color: `#FF6633`, `rgb(255, 102, 51)`, `oklch(70% 0.15 50)`, `color-mix(in oklch, red 40%, blue)` — 12 color syntaxes with deterministic conversion math at 256-bit precision
- Identity: `550e8400-e29b-41d4-a716-446655440000` (UUID), `urn:isbn:978-0-618-26030-2` (IRI reference)
- Tokens: `$Hardcover` (enumerated value from a schema-defined closed set), `~hobbit` (document-scoped lookup key)
- Collections: lists, sets, maps, records, tuples, and ranges — all as literals with parameterized type constraints
- Pattern: `regex/[a-z]+/` (pinned to PCRE2 version 10.47)
- Phonetic: `ipa/ˈhɒbɪt/` (IPA transcription)

There is no NaN. There is no null. Fractions are never normalized.

**Schema-first validation.** A Codex document is validated against a governing schema (which is itself a Codex document). Schemas declare what concepts exist, what traits they have, what values are allowed, and what structural rules apply. The constraint system is expressive — conditional rules, path-based validation, cardinality checks, uniqueness constraints, cross-reference validation — and maps deterministically to SHACL for machine enforcement. The schema system is self-hosting: the bootstrap schema that defines what a valid schema looks like is itself a Codex document that validates itself.

**Round-trip through RDF.** A Codex document can be transformed into RDF triples, stored in a triple store, queried via SPARQL, and reconstructed back to a byte-identical Codex document. No sidecar files, no metadata loss, no semantic drift.

**Content as a first-class concept.** A Codex element is in either children mode (containing other structured elements) or content mode (containing opaque narrative text). Content is preserved verbatim as authored prose. Semantic annotations within content are written in Gloss.

**Multiple output formats.** The Codex processor outputs canonicalized Codex, Turtle triples (RDF), or CBOR. Converting CBOR to JSON, TOML, YAML, or any other format is a straightforward boundary adapter — a separate crate, not a core concern.

### What Makes Codex Distinctive

The type system stands out. Thirty-plus value types with unambiguous lexical recognition is a hard design problem. The precedence rules and disambiguation are carefully specified. The color system alone — 12 syntaxes with exact matrix constants for color space conversions computed at 256-bit precision, mandated dot-product procedures, and specific gamut-checking tolerances — is unusually rigorous for a data format.

The canonical form requirement means every conforming tool must agree on formatting down to the byte. This is a strict demand, but it eliminates an entire class of problems: merge conflicts from formatting differences, identity disagreements between systems, and the "same data, different bytes" ambiguity that plagues looser formats.

## Gloss

Gloss is an inline annotation language. It binds spans of text to semantic references — connecting a piece of prose to the thing it's talking about. It does exactly one thing, and the specification constitutionally prohibits it from doing anything else.

### The Problem It Solves

When you write "The Hobbit" in a document, a human knows you mean Tolkien's novel. A machine doesn't. Traditional solutions — HTML links, Markdown links, wiki syntax — all conflate meaning with presentation. An HTML anchor tag is simultaneously a semantic reference, a navigation target, and a visual styling trigger. Change the rendering target (screen reader, PDF, braille display, semantic analysis tool) and the link metaphor breaks or carries unwanted baggage.

Gloss separates the question "what does this text refer to?" from every other concern.

### How It Works

The entire language is four syntactic forms:

```
{@iri}                     reference by global identifier, no label
{@iri | label text}        reference by global identifier, with label
{~token}                   reference by local lookup key, no label
{~token | label text}      reference by local lookup key, with label
```

Inside a Codex content block:

```
I first read {@book:hobbit | The Hobbit} when I was ten.
```

This binds the text "The Hobbit" to the entity identified by `book:hobbit`. Workshop resolves that identifier against its semantic model.

The `@` form references entities by global IRI. The `~` form references entities by document-scoped lookup key. These represent genuinely different kinds of reference and are handled differently in the output model.

### What Gloss Does Not Do

Gloss is constitutionally prohibited from defining layout, typography, styling, behavior, evaluation, or execution. It is prohibited from introducing new semantic entities. It is prohibited from resolving references — that is the consuming system's job. Gloss parses text into segments (literal text and span bindings) and stops.

### What Makes Gloss Distinctive

**Two-phase recognition.** A `{` character only begins a Gloss binding when immediately followed by `@` or `~`. Otherwise it's a literal brace. This means Gloss can be embedded in JSON, code, math notation, or any other text that uses braces without requiring escaping. Only the specific sequences `{@` and `{~` trigger parsing.

**Extreme precision.** The label separator must be exactly ` | ` — one space, pipe, one space. No variation. Sixteen distinct diagnostic codes cover every possible whitespace and separator violation. Every valid Gloss string parses to exactly one interpretation. There is no style variation to argue about.

**Deterministic error recovery.** When a binding fails to parse, the processor emits the opening `{` as literal text and resumes scanning from the next character. No backtracking, no buffering, no ambiguity.

**Target independence.** A Gloss binding could become a hyperlink, a tooltip, a citation, a spoken annotation, an attributed string, a braille annotation, or something not yet invented. The same annotated text works against different semantic models and different rendering targets without modification.

## Workshop

Workshop is the processing pipeline. It consumes Codex and Gloss documents, validates them against schemas, computes derived values, applies design constraints, and produces finished output for specific targets.

### The Pipeline

Workshop processes documents through eight phases:

1. **Resolve** — find all referenced schemas and dependencies using cryptographic content hashes (no "latest version" ambiguity — imports use SHA-256 content-address URNs)
2. **Plan** — build an execution plan
3. **Load** — establish the baseline semantic state
4. **Validate** — check everything against schemas
5. **Derive** — compute calculated values using the Behavior expression language
6. **Verify** — confirm derivations are consistent
7. **Project** — determine what each output target needs via semantic projections
8. **Render** — Foundries produce final artifacts

The pipeline is deterministic, checkpointed, resumable, and incrementally re-executable. The output is a Semantic Universe — the complete set of RDF triples derived from a repository at a given commit under a given Workshop version. The triple store is a rebuildable cache, not the source of truth.

### The Expression Language (Behavior)

Workshop includes a built-in language for computations. It derives values, validates constraints, and transforms collections. It is deliberately limited: no side effects, no network access, no file I/O, no randomness. Every computation either succeeds with a value or fails with a diagnostic. There is no concept of crashing or undefined behavior.

The language covers ten operator families: math (including complex numbers, statistics, linear algebra, combinatorics, numerical calculus), text manipulation, date/time operations, color space conversions, collection transforms (map, filter, sort, reduce), relational predicates, identity operations, structural validation, presence testing, and formatting boundaries. It compiles to SPARQL (always), TypeScript (for browsers), and Rust/WebAssembly (for native).

NaN is banned — any operation that would produce NaN instead produces a diagnostic explaining what went wrong.

### Semantic Projections and Foundries

Between the canonical semantic universe and the final output sits a projection layer. A semantic projection is a pure function that derives a non-authoritative view of the data — selecting, pruning, collapsing, and annotating the canonical graph into what a specific output target needs.

Foundries consume the projected adaptive plan and produce target artifacts. A Foundry is strictly forbidden from querying the canonical universe, executing Behavior expressions, or applying semantic transforms. It receives a fully resolved description of what to render and renders it. This separation means adding a new output format (PDF, ePub, native app) requires only a new Foundry, not changes to the pipeline.

### Error Handling

Workshop's error messages are specified to be humane. The specification states: "When something goes wrong, it is Workshop's failure, not the user's." Diagnostics must be specific, must suggest fixes, must not use jargon, must not blame the user, and must say please. Every error has a stable code, a location, expected versus received values, and a suggestion. This is a normative requirement.

## The Design System

Workshop includes a formal graphic design ontology and adaptive layout system. This is the most ambitious component and the one with the longest gestation — 25 years of thinking about how to formalize visual design as a constraint satisfaction problem.

### The Ontology

Rather than CSS-style styling rules, Workshop uses a machine-readable vocabulary that models visual design the way a trained designer thinks about it. The ontology is grounded in established design theory (the framework draws on Richard Poulin's *The Language of Graphic Design*) and organizes visual communication into three layers:

- **Elements** — the perceptual primitives: geometry, color, texture, scale, space
- **Principles** — the relational grammar: balance, contrast, figure-ground, proportion, hierarchy, rhythm, tension, closure
- **Structure** — the realization systems: typography and grid

Compositions contain elements. Elements have geometry, style, and semantic roles. Design principles (balance, contrast, figure-ground, proportion, hierarchy) are declared as explicit, first-class statements about relationships between elements — reified as RDF nodes, validated by SHACL constraints, not implied by pixel values.

The ontology is enforced at three levels: RDF vocabulary (what terms exist), SHACL constraints (what structural rules apply), and canonical construction rules (what makes a composition graph valid, sealed, and deterministically hashable). Every normative clause is traced to its enforcement mechanism and tested with positive and negative fixture files.

### Adaptive Layout

Responsive behavior — adapting to different screens, devices, and user preferences — is handled through constraint-based optimization rather than hand-authored breakpoints. The approach draws explicitly on two precedents:

- **Knuth-Plass line-breaking (1981)** — reframed line breaking as global optimization over a cost function. The insight: the algorithm matters less than the cost function. Define the cost function well and good results follow.
- **Muller-Brockmann grid systems (1981)** — formalized proportional grid systems where proportional relationships are more stable than absolute positions. A grid is a set of constraints that produces layouts, not a fixed layout itself.

Authors declare context (device, viewport, accessibility preferences), objectives (readability-first, performance-first, accessibility requirements), constraints (hard rules like "elements must not overlap" and soft preferences like "readability is critical, brand expression is low priority" with explicit weights), and overrides (human-authored exceptions that flow through the same solver).

A solver evaluates all of this against the composition, resolves conflicts deterministically, and emits an adaptive plan. Breakpoints are not hand-coded — they emerge naturally from when constraints become infeasible at certain viewport sizes. Overrides are first-class constraints re-run through the solver, preserving human authority, determinism, and auditability.

This either works or it doesn't. The idea is sound, the precedents are established, and the specification is thorough. Testing and adjustment will determine whether the generalization from one-dimensional line-breaking to two-dimensional page layout holds at production scale.

### Computed Metrics

A separate metrics vocabulary supports quality analysis of compositions. Eleven closed metric types — salience score, hierarchy rank, balance deviation, contrast luminance, whitespace ratio, alignment error, typographic rhythm score, and others — can be computed from geometry and style and attached to compositions. Each metric has deterministic replay identity via algorithm identifier and input hash.

## The Schema Ecosystem

Workshop ships with 40 domain schemas as a starting point, with plans to scale to 1,000 or more. Each schema is a complete package: schema definition, English localization baseline, examples, and templates.

The domain schemas draw on schema.org for conceptual coverage — the same real-world domains (Person, Recipe, Event, Organization, Product, and so on). But the approach differs in two fundamental ways.

First, Codex schemas use **composition, not inheritance**. Schema.org's type hierarchy (Thing > CreativeWork > Article > NewsArticle) creates deep inheritance chains where properties are inherited from ancestors and meaning depends on position in the tree. Codex schemas compose independent, well-defined packages. A Person schema imports a PersonName schema and a ContactPoint schema. The relationships are explicit, not inherited.

Second, Codex schemas have **better types**. Schema.org properties accept loose types — a date might be a Text or a Date or a DateTime, a price might be a Number or a Text. Codex schemas use the full Codex type system: temporal types with proper semantics, monetary amounts with currency codes, fractions, precision numbers, enumerated tokens from closed sets. The ambiguity that schema.org tolerates by design, Codex eliminates by design.

Localization is built in at the foundation. No language is structurally privileged — even English labels come from external localization bundles. The schema itself is language-neutral. Pluralization follows CLDR categories. Grammatical gender is supported. The localization model is clean enough to serve as a reference for how multilingual schema systems should work.

The goal is to provide a schema ecosystem that is cleaner, more precise, and more composable than schema.org — one that could eventually serve as an alternative for applications that need stronger typing and structural guarantees than schema.org provides.

## Implementation Strategy

Each of the three specifications has a FOSS Apache 2.0 Rust reference implementation:

- **Codex processor** — parsing, validation, canonicalization, RDF projection, CBOR serialization
- **Gloss parser** — recognition, parsing, segment output
- **Workshop** — pipeline orchestration, Behavior compilation and evaluation, schema validation, semantic projection, Foundry interface

Workshop depends on the Codex and Gloss crates as Rust dependencies. It does not reimplement their functionality.

The specifications are extremely strict by design. Every requirement uses MUST or MUST NOT — no MAY, no SHOULD. Every valid document has one canonical byte sequence. Every error has one correct diagnostic. Every pipeline execution has one deterministic output.

This strictness serves three purposes. First, it ensures that no implementation claiming conformance can deviate from the specification in any way — the kind of "almost compatible" fragmentation that plagued XML, Markdown, and YAML cannot happen. Second, it strongly discourages others from creating competing implementations when a fully conforming, well-tested, FOSS reference implementation already exists. Use the reference implementation. The conformance problem is already solved.

Third, and perhaps most practically: people are not going to write Codex, Gloss, or schema packages by hand. LLMs will write them. When the primary author is a machine, ambiguity is the enemy. One canonical form means the LLM never has to choose between equivalent representations, never drifts across a codebase, and every output is mechanically verifiable against the specification. Strictness that would be burdensome for human authors is a feature for machine authors — one right way saves a lot of pain.

## What This Is Not

This is not a content management system, a static site generator, a web framework, or a design tool. It is a semantic processing pipeline: documents go in, validated and enriched semantic data comes out, and target-specific renderers produce finished artifacts. The system owns the pipeline from parsing through rendering but does not prescribe how documents are authored, stored, or managed.

This is a work in progress. The specifications are substantial and largely locked. The reference implementations are underway. The design system is specified but unimplemented. The schema ecosystem is established at 40 packages and growing. The ambition is large; the execution is methodical.
