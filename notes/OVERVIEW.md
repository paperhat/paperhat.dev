# Paperhat: Codex, Gloss, and Workshop

Paperhat has three components. Codex is a markup language for structured semantic data. Gloss is an inline language for binding text spans to semantic references. Workshop is a processing pipeline that consumes Codex and Gloss documents, validates them, computes derived values, and renders output for specific targets (web, PDF, ePub, print, native applications).

Each is an independent, frozen specification with a FOSS Apache 2.0 Rust reference implementation.

## Codex

Codex is a declarative markup language. A Codex document describes structured data — a person, a recipe, an event — using named concepts with typed traits and optional narrative content. File extension: `.cdx`.

### Structure

A document contains one root concept. Concepts have traits (typed name-value pairs) and are in one of two modes: children mode (containing child concepts) or content mode (containing opaque narrative text). The governing schema determines which mode is permitted.

```cdx
<Person id=urn:example:jane key=~jane>
	<PersonName givenName="Jane" familyName="Doe" />
	<ContactPoint kind=$Email value=email("jane@example.com") />
</Person>
```

### Value Types

The type system defines 63 built-in value type tokens. The parser recognizes concrete types by lexical form — no schema is needed for type identification. Union types and constraint tokens provide schema-level type constraints. Collection types are parameterized and can be nested to arbitrary depth.

| Type | Lexical Form |
|------|-------------|
| `$Text` | `"quoted text"` or `` `backtick text` `` |
| `$Character` | `'A'`, `'\n'` |
| `$Boolean` | `true`, `false` |
| `$Number` | union: any numeric type |
| `$Integer` | `42`, `-7` |
| `$Zero` | `0` |
| `$NegativeInteger` | constraint: minus sign, digits not `0` |
| `$NonPositiveInteger` | union: `$Zero` or `$NegativeInteger` |
| `$DecimalNumber` | `3.14`, `-0.5` |
| `$ExponentialNumber` | `6.022e23`, `1.5E-10` |
| `$PrecisionNumber` | `3.14p2` (declared measurement precision) |
| `$Fraction` | `1/3`, `-22/7` (never reduced) |
| `$ImaginaryNumber` | `3i`, `-2.5i` |
| `$ComplexNumber` | `2+3i`, `1.5-2i` |
| `$NonNegativeInteger` | union: `$Zero` or `$PositiveInteger` |
| `$PositiveInteger` | constraint: no minus sign, digits not `0` |
| `$PositiveInfinity` | `Infinity` |
| `$NegativeInfinity` | `-Infinity` |
| `$Infinity` | union: `$PositiveInfinity` or `$NegativeInfinity` |
| `$RealNumber` | union: Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, Fraction, PositiveInfinity, or NegativeInfinity |
| `$FiniteNumber` | union: Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, Fraction, ImaginaryNumber, or ComplexNumber |
| `$FiniteRealNumber` | union: Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, or Fraction |
| `$ExactNumber` | union: Integer or Fraction |
| `$EnumeratedToken` | `$Hardcover`, `$Email` |
| `$IriReference` | `urn:isbn:978-0547928227`, `schema:Person` |
| `$LookupToken` | `~jane`, `~hobbit` |
| `$Uuid` | `550e8400-e29b-41d4-a716-446655440000` |
| `$HostName` | `host("example.com")` |
| `$EmailAddress` | `email("jane@example.com")` |
| `$Url` | `url("https://example.com/path")` |
| `$Ipa` | `ipa/ˈhɒbɪt/` |
| `$Regex` | `regex/[a-z]+/i` (PCRE2 10.47) |
| `$HexColor` | `#FF6633`, `#RGBA`, `#RRGGBBAA` |
| `$NamedColor` | `&crimson`, `&steelblue` |
| `$RgbColor` | `rgb(255, 102, 51)` |
| `$HslColor` | `hsl(20, 100%, 60%)` |
| `$HwbColor` | `hwb(20 20% 0%)` |
| `$LabColor` | `lab(67% 45 30)` |
| `$LchColor` | `lch(67% 54 34)` |
| `$OklabColor` | `oklab(0.7 0.1 0.08)` |
| `$OklchColor` | `oklch(70% 0.15 50)` |
| `$ColorSpaceColor` | `color(display-p3 1 0.5 0)` |
| `$ColorSpaceColorFunction` | union: any function-based color spelling |
| `$ColorMix` | `color-mix(in oklch, #FF0000, #0000FF)` |
| `$DeviceCmyk` | `device-cmyk(0 0.6 1 0)` |
| `$Color` | union: any color type |
| `$PlainDate` | `{2024-03-15}` |
| `$PlainTime` | `{14:30:00}` |
| `$PlainDateTime` | `{2024-03-15T14:30:00}` |
| `$PlainYearMonth` | `{2024-03}` |
| `$PlainMonthDay` | `{03-15}` |
| `$YearWeek` | `{2024-W12}` |
| `$Instant` | `{2024-03-15T14:30:00Z}` |
| `$ZonedDateTime` | `{2024-03-15T14:30:00-05:00[America/New_York]}` |
| `$Duration` | `{P1Y2M3D}`, `{PT1H30M}` |
| `$TemporalKeyword` | `{now}`, `{today}` |
| `$TemporalPoint` | union: any temporal type except Duration and TemporalKeyword |
| `$List` | `[1, 2, 3]` — parameterized: `$List<$Text>` |
| `$Set` | `set[1, 2, 3]` — parameterized: `$Set<$Integer>` |
| `$Map` | `map[key: value]` — parameterized: `$Map<$Text, $Integer>` |
| `$Record` | `record[name: "Jane"]` — parameterized: `$Record<$Text>` |
| `$Tuple` | `(1, "two", true)` — parameterized: `$Tuple<$Integer, $Text, $Boolean>` |
| `$Range` | `1..10`, `1..100s5` — parameterized: `$Range<$Integer>` |

Every type is an independent, first-class type. Union types like `$Color`, `$Number`, and `$TemporalPoint` are schema-level constraint tokens that accept multiple concrete types — they are not parent types. Collection types accept type parameters with no limit on nesting depth (for example, `$List<$List<$Map<$Text, $Set<$Integer>>>>`).

There is no NaN and no null.

### Schemas

Schemas are Codex documents that define what concepts exist, what traits they have, what values are permitted, and what structural rules apply. The constraint system includes conditional rules, path-based validation, cardinality checks, uniqueness constraints, and cross-reference validation. All constraints map deterministically to SHACL for machine enforcement. The bootstrap schema (the schema that governs schemas) is itself a Codex document.

### Canonical Form

Every valid Codex document has exactly one byte-level representation: tabs for indentation, alphabetical trait ordering, deterministic line-wrapping at 100 characters. This canonical form enables byte-identical round-tripping through RDF triple stores and content-addressed identity via SHA-256 hash.

### Output Formats

The Codex processor outputs canonicalized Codex, RDF (Turtle triples), or CBOR. Conversion from CBOR to other formats (JSON, TOML, YAML) is a boundary concern handled by separate adapters.

## Gloss

Gloss binds spans of text to semantic references. It appears inside Codex content blocks. The specification prohibits Gloss from defining layout, styling, behavior, or any other concern beyond span-to-reference binding.

### Syntax

Four forms:

```
{@iri}                     identifier reference, no label
{@iri | label text}        identifier reference, with label
{~token}                   lookup reference, no label
{~token | label text}      lookup reference, with label
```

Example in a Codex content block:

```
I first read {@book:hobbit | The Hobbit} when I was ten.
```

This binds "The Hobbit" to the entity `book:hobbit`. The `@` form uses global IRIs. The `~` form uses document-scoped lookup keys. Resolution against the semantic model is the consuming system's responsibility, not Gloss's.

### Recognition

A `{` character triggers Gloss parsing only when immediately followed by `@` or `~`. All other braces are literal. This allows Gloss to appear inside JSON, code, or any brace-using text without escaping.

### Precision

The label separator is exactly ` | ` (space, pipe, space). No variation is permitted. Sixteen diagnostic codes cover specific whitespace and separator violations. Every valid Gloss string has exactly one parse. Error recovery is deterministic: on failure, emit `{` as literal text and resume from the next character.

## Workshop

Workshop consumes Codex and Gloss documents and produces rendered output. It is a deterministic pipeline: the same inputs always produce the same outputs, provably, via content-addressed imports and Merkle hash trees.

### Pipeline

Eight phases:

1. **Resolution** — resolve schema imports by SHA-256 content-hash URN
2. **Plan compilation** — build the execution plan
3. **Load** — establish the baseline semantic state
4. **Validation** — check all documents against governing schemas
5. **Derivation** — compute derived values using the Behavior expression language
6. **Verification** — confirm derived values are consistent
7. **Projection** — compute what each output target needs
8. **Rendering** — Foundries produce target-specific artifacts

The pipeline is checkpointed and resumable. The output of phases 1-6 is a Semantic Universe: the complete RDF graph for a repository at a given commit under a given Workshop version. The triple store is a rebuildable cache. The Codex documents in Git are the source of truth.

### Behavior

Behavior is Workshop's expression language for derived values and validation. It is pure (no side effects), total (every evaluation terminates), and deterministic (no ambient state). Every evaluation produces either a valid result or a diagnostic. NaN does not exist; operations that would produce NaN produce diagnostics instead.

Ten operator families: math (arithmetic, complex numbers, statistics, linear algebra, combinatorics, calculus), text, temporal, color, collection transforms (map, filter, sort, reduce), relational predicates, identity, structural validation, presence testing, and formatting boundaries. Behavior compiles to SPARQL, TypeScript, and Rust/WebAssembly.

### Projections and Foundries

A semantic projection is a function that derives a target-specific view from the canonical graph using four operations: select, prune, collapse, and annotate. The result is an adaptive plan.

Foundries consume the adaptive plan and produce output (HTML bundles, PDFs, etc.). A Foundry cannot access the canonical graph, execute Behavior expressions, or apply semantic transforms. It receives a fully resolved description and renders it. Adding a new output target requires a new Foundry, not pipeline changes.

### Diagnostics

Diagnostics are normatively required to be specific, actionable, and non-blaming. Every diagnostic has a stable code, source location, expected and received values, and a suggestion. The specification states: "When something goes wrong, it is Workshop's failure, not the user's."

## Adaptive Rendering

Workshop adapts output to different targets, devices, user preferences, and cultural contexts through a two-stage adaptive system.

### Context

Authors declare rendering context as structured Codex data: viewport dimensions, device class (handset, tablet, laptop, desktop, television, kiosk, watch, automotive), input modality (touch, pointer, keyboard, voice, stylus), accessibility preferences (reduced motion, high contrast, color scheme), network class (offline, constrained, standard, high bandwidth), interaction mode (scan, read, edit, immerse), language, region, and script direction (LTR, RTL, top-to-bottom).

### Objectives and Constraints

Authors declare objectives with explicit priorities: readability, accessibility, performance, task completion, conversion, trust, brand expression, delight, localization. Each objective has a priority level (must, prefer, neutral) that maps to a numeric weight.

Hard constraints are pass/fail: elements must not overlap, minimum readable font size, preserve reading order, respect reduced motion. Soft constraints are weighted preferences: readability (critical), performance (high), brand expression (low). When the full constraint set is infeasible, relaxation rules specify what to relax first.

Overrides are explicit human-authored exceptions — pin this element visible, hide that element on constrained networks — that run through the same solver as all other constraints.

### Two-Stage Evaluation

Stage A evaluates hard policy rules against the runtime context. Policies are condition-action pairs: if viewport width exceeds 1024 pixels, apply these graph changes. Policies have priorities and deterministic conflict resolution (three strategies: error on conflict, first match wins, higher priority wins).

Stage B runs a constraint-based optimization solver. It balances weighted soft constraints, applies hard constraint boundaries, uses relaxation rules when constraints conflict, and produces the final adaptive plan. Breakpoints are not hand-authored; they emerge from when constraints become infeasible at specific context values.

Both stages are fully specified with deterministic ordering, conflict resolution, and end-to-end executable tests from authored Codex through evaluated output.

### Design Ontology

The visual constraint vocabulary is a formal RDF ontology under the `gd:` namespace. It models compositions as graphs of elements with geometry, style, and semantic roles. Design principles (balance, contrast, figure-ground, proportion, hierarchy, rhythm) are first-class nodes — explicit statements about relationships between elements, validated by SHACL constraints.

The ontology draws on Knuth-Plass line-breaking (global cost-function optimization) and Muller-Brockmann grid systems (proportional constraints that survive format changes) as architectural precedents for the solver.

Eleven computed metrics (salience, hierarchy rank, balance deviation, contrast, whitespace ratio, alignment error, typographic rhythm, and others) can be attached to compositions for quality analysis. Each metric has deterministic replay identity.

## Schema Ecosystem

Workshop ships with 40 domain schemas (Person, Recipe, Event, Organization, Product, and others) as a starting point, with plans to scale to 1,000 or more. Each schema is a package containing a schema definition, an English localization baseline, examples, and templates.

The domain coverage draws on schema.org, but the structural approach differs. Codex schemas use composition (a Person imports PersonName and ContactPoint as independent packages) rather than schema.org's inheritance hierarchies (Thing > Person). Codex schemas use the full Codex type system (temporal types, monetary amounts with currency codes, enumerated tokens, precision numbers) rather than schema.org's loose typing (where a date might be Text, Date, or DateTime).

Localization is built in. No language is structurally privileged. Even English labels are external localization bundles. Pluralization uses CLDR categories. Grammatical gender is supported.

## Implementation

Three FOSS Apache 2.0 Rust crates: Codex processor, Gloss parser, Workshop pipeline. Workshop depends on the Codex and Gloss crates.

All specifications use only MUST and MUST NOT. Every valid document has one canonical byte sequence. Every error has one correct diagnostic. Every pipeline execution has one deterministic output. This strictness prevents the kind of "almost compatible" fragmentation that occurred with XML, Markdown, and YAML, and it strongly discourages competing implementations when the reference implementation already exists.

The primary authoring tool for Codex documents and schema packages is LLMs. One canonical form means the LLM never chooses between equivalent representations, never drifts across a codebase, and every output is mechanically verifiable. Strictness that would burden human authors is an advantage for machine authors.
