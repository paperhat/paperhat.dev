# Sitebender Studio

A declarative TSX DSL for semantic web applications via a pipeline:

```
TSX → IR → Triples → Oxigraph → SPARQL → JSON → render → HTML
```

## Table of Contents

- [The Paradigm Shift](#the-paradigm-shift)
- [Democratizing Web Development](#democratizing-web-development)
- [Everything Is Data](#everything-is-data)
- [Runtime Types That Actually Work](#runtime-types-that-actually-work)
- [The Three-Path Pattern](#the-three-path-pattern)
- [Schema-Driven Everything](#schema-driven-everything)
- [Structural Validation](#structural-validation)
- [Help, Don't Scold](#help-dont-scold)
- [The Library Ecosystem](#the-library-ecosystem)
  - [Foundation Layer](#foundation-layer)
  - [Rendering Layer](#rendering-layer)
  - [Data Layer](#data-layer)
  - [Application Layer](#application-layer)
  - [Quality Layer](#quality-layer)
  - [Communication Layer](#communication-layer)
  - [Tooling Layer](#tooling-layer)
- [Quality Enforcement Pipeline](#quality-enforcement-pipeline)
- [Three Rendering Modes](#three-rendering-modes)
- [Progressive Enhancement](#progressive-enhancement)
- [High Availability and Disaster Recovery](#high-availability-and-disaster-recovery)
- [What You Actually Write](#what-you-actually-write)
- [Installation](#installation)
- [License](#license)

<a id="the-paradigm-shift"></a>

## The Paradigm Shift

Most web frameworks treat code as code. You write functions, manage state in
closures, and hope your types survive until runtime. Your application exists as
source files that must be parsed, compiled, and executed.

Sitebender inverts this model. **Your entire application — structure, content,
behavior, validation — exists as queryable semantic data in a triple store.**
The rendered interface is just one projection of the underlying knowledge graph.

```
TSX → IR → Turtle Triples → Oxigraph → SPARQL → JSON → render → HTML/DOM
```

This isn't an implementation detail. It's the foundation that enables
capabilities impossible with traditional approaches.

<a id="democratizing-web-development"></a>

## Democratizing Web Development

Sitebender lowers the bar for building powerful, accessible,
standards-compliant, robust, scalable, distributed, and offline-capable web
applications.

**You don't need to understand everything at once.**

| Stage | Libraries                | Skills Required                    | What You Build                |
| ----- | ------------------------ | ---------------------------------- | ----------------------------- |
| 1     | Architect, Quartermaster | Follow templates, domain knowledge | Static sites                  |
| 2     | + Pathfinder, Artificer  | Basic arithmetic, domain logic     | Dynamic sites with validation |
| 3     | + Custodian, Operator    | State and events concepts          | Interactive applications      |
| 4     | + Exchequer, Reckoner    | Commerce understanding             | E-commerce                    |
| 5     | + Agent                  | P2P and CRDT concepts              | Distributed, offline-capable  |

Toolsmith types and functions are used throughout. Sentinel handles security.
You add complexity as you need it.

**Semantic components match domains.** `<Recipe>`, `<Song>`, `<Invoice>` are
self-describing. Understand recipes? Build a recipe site. Domain expertise
matters more than programming skill.

**Templates and tooling smooth the path.** Quartermaster scaffolds working apps.
Tutorials guide progression. Visual editors are coming.

**The audience:**

- Kids with domain expertise building something real
- Designers prototyping without developers
- Small businesses with real e-commerce needs
- Communities wanting privacy-respecting apps
- Anyone not afraid of a little "code" (which is really just semantic
  composition)

**AI makes it even easier** — but it's not the primary story. The same
properties that make Sitebender human-understandable (semantic components,
queryable data, structural validation) also make it AI-friendly. Human-first
with AI compatibility, not AI-first with human readability.

<a id="everything-is-data"></a>

## Everything Is Data

When you write Sitebender components, you're not writing code that executes.
You're declaring data that describes your application:

```tsx
<Essay>
	<Heading>
		<Title>Understanding Semantic Architecture</Title>
		<Author>The Architect</Author>
	</Heading>
	<Section>
		<Heading>
			<Title>Why Data First?</Title>
		</Heading>
		<Paragraph>
			Because data can be queried, reasoned about, and transformed.
		</Paragraph>
	</Section>
</Essay>
```

This compiles to RDF triples, persists in Oxigraph (a high-performance triple
store that runs in browsers via WASM or servers via native Rust), and renders to
semantic HTML with proper heading levels, ARIA attributes, and Schema.org
metadata — all determined automatically by context.

**What this enables:**

- Query your application semantically: "Find all recipes under 30 minutes with
  no dairy" is a SPARQL query, not a text search
- Apply cross-cutting changes via SPARQL UPDATE, not code modifications
- Version content with named graphs — semantic diffs, not text diffs
- Federate data from multiple sources at query time
- Let inference engines derive facts you didn't explicitly program

<a id="runtime-types-that-actually-work"></a>

## Runtime Types That Actually Work

TypeScript provides compile-time safety. But TypeScript types vanish at runtime.
Your carefully typed `EmailAddress` parameter becomes just a string the moment
external data arrives.

Sitebender's Toolsmith library provides **precision types enforced at runtime**:

```typescript
type Integer = Tagged<"Integer"> & {
	readonly value: bigint;
};

type Fraction = Tagged<"Fraction"> & {
	readonly numerator: bigint;
	readonly denominator: bigint;
};

type PrecisionNumber = Tagged<"PrecisionNumber"> & {
	readonly value: bigint;
	readonly decimalPlaces: bigint;
};
```

The `Tagged` pattern provides runtime discrimination via `_tag` for pattern
matching. String newtypes like `EmailAddress` use `Brand` for compile-time-only
safety.

**Two-mechanism safety:**

1. **Tagged types / Brands** prevent bypassing validation in source code
   (compile-time)
2. **Type guards** validate external data at system boundaries (runtime)

**Precision arithmetic means precision arithmetic.** No floating-point errors.
No `0.1 + 0.2 = 0.30000000000000004`. When you need exact calculations —
financial, scientific, or simply correct — you get them.

The numeric type hierarchy provides lossless conversions up and explicit
rounding modes down. Mixed-type operations promote to the appropriate common
type automatically.

<a id="the-three-path-pattern"></a>

## The Three-Path Pattern

Error handling uses three monads, each for a specific purpose:

| Monad          | Success      | Failure             | Use Case                                           |
| -------------- | ------------ | ------------------- | -------------------------------------------------- |
| **Maybe**      | `Just<T>`    | `Nothing`           | Optional values — you don't need error details     |
| **Result**     | `Ok<T>`      | `Help<H>`           | Sequential operations — fail fast on first problem |
| **Validation** | `Success<T>` | `Failure<[H, ...]>` | Parallel/tree operations — accumulate ALL problems |

The critical distinction: **Result** short-circuits (first error stops
everything). **Validation** accumulates (collect every error). Choose
deliberately based on whether you want fail-fast or full feedback.

Smart constructors accept input wrapped in any of these three monads:

```typescript
emailAddress(just("user@example.com")); // → Maybe<EmailAddress>
emailAddress(ok("user@example.com")); // → Result<Help, EmailAddress>
emailAddress(success("user@example.com")); // → Validation<Helps, EmailAddress>
```

Same validation logic, three execution strategies. The constructor validates,
normalizes, brands, and returns the same monad type you provided.

<a id="schema-driven-everything"></a>

## Schema-Driven Everything

Your validation rules ARE your data model.

SHACL shapes in the triple store define types, constraints, and relationships.
The **same definition** drives:

- Form generation — which fields, which widgets
- Client validation — rules execute in the browser
- Server validation — identical rules on the server
- Database constraints — identical rules in storage

```tsx
<ConceptForm of="Person" />
```

This generates a complete form from the `Person` shape. Change the shape once,
everything updates. No duplicate validation logic. No client/server divergence.

Widget selection happens automatically based on type:

- `Integer` → BigInt input (arbitrary precision)
- `Fraction` → Fraction input (configurable display)
- `PrecisionNumber` → Decimal input (exact, currency-ready)
- `Boolean` → Checkbox or toggle
- `Member` → Radio buttons or select (threshold configurable)
- `Subset` → Checkbox buttons or multiselect (threshold configurable)

SHACL constraints (`minInclusive`, `maxInclusive`, `pattern`) become client-side
validation automatically.

<a id="structural-validation"></a>

## Structural Validation

The ontology defines what CAN exist:

- Valid components
- Valid compositions (what can contain what)
- Type constraints
- Accessibility requirements (WCAG as SHACL shapes)

Validation happens at the data layer:

```
Proposed change → SHACL validation → Pass? Save. Fail? Reject.
```

Invalid changes never persist. There's no "invalid state that slipped through."
If it doesn't fit the ontology, it doesn't exist in the triple store.

Everyone makes mistakes — humans forget conventions, AI assistants hallucinate,
copy-paste errors happen. But structural validation at the data layer cannot be
bypassed. The same guardrails protect everyone.

<a id="help-dont-scold"></a>

## Help, Don't Scold

When something goes wrong, it's the system's fault for not making success
obvious. Every Help object:

- Uses friendly language — "hit a snag" not "ERROR"
- Takes responsibility — the system fumbled, not the user
- Provides a path forward — suggestions, not just complaints
- Accumulates all issues — fix everything in one pass

```typescript
SEVERITY.help; // "tip" — suggestion, everything works
SEVERITY.warning; // "heads-up" — may not behave as intended
SEVERITY.critical; // "MAYDAY!" — must fix to proceed
```

Issue codes never blame: `TEXT_NOT_UNDERSTOOD` not `INVALID_TEXT`. The
limitation is ours, not theirs.

<a id="the-library-ecosystem"></a>

## The Library Ecosystem

<a id="foundation-layer"></a>

### Foundation Layer

| Library       | Purpose                                                                                                    |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| **Toolsmith** | Runtime type system, precision arithmetic, monads, Help system, utility functions                          |
| **Arborist**  | The ONLY parser integration — SWC and deno_ast WASM; one parser, many consumers (Envoy, Auditor, Quarrier) |

<a id="rendering-layer"></a>

### Rendering Layer

| Library       | Purpose                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Architect** | Context-aware semantic TSX compiling to HTML via RDF/SPARQL — 1000+ type-safe components with automatic accessibility and guaranteed WHATWG compliance |
| **Artificer** | Reactive behaviors as declarative TSX — calculations, validation, conditional display, schema-driven forms via SHACL                                   |

<a id="data-layer"></a>

### Data Layer

| Library        | Purpose                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| **Pathfinder** | Triple store integration — SPARQL queries, named graphs, vector similarity search                             |
| **Custodian**  | State management respecting web architecture — URL-encoded state, idempotent operations, signed continuations |
| **Quarrier**   | Property-based testing — SHACL-aware generators, metamorphic testing, lazy shrink trees                       |

<a id="application-layer"></a>

### Application Layer

| Library        | Purpose                                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| **Formulator** | Bidirectional formula parsing — human notation to Artificer IR with MathML output                               |
| **Exchequer**  | Commerce primitives: products, orders, payments, returns, gift cards, quotes with exact decimal arithmetic      |
| **Reckoner**   | Pricing transformations: promotions, discounts, refund policies, loyalty programs, credit management            |
| **Linguist**   | Internationalization as declarative data — translations as triples with ICU MessageFormat and RTL support       |
| **Sentinel**   | Security as queryable triples — OAuth2, WebAuthn, DID Auth, RBAC/ABAC, capability tokens, mock auth for testing |

<a id="quality-layer"></a>

### Quality Layer

| Library     | Purpose                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------- |
| **Steward** | Code style enforcement (deterministic, non-configurable)                                                      |
| **Warden**  | Import boundary enforcement and SHACL validation — guards library boundaries and component compositions       |
| **Auditor** | Formal verification via Z3 theorem proving — mathematical proofs of correctness and automated test generation |

<a id="communication-layer"></a>

### Communication Layer

| Library          | Purpose                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| **Operator**     | Pub/sub as triples — channels, transport layers, event sourcing, projections with Warden validation       |
| **Orchestrator** | Workflow automation as triples — n8n-style pipelines with TSX or visual editing, distributed execution    |
| **Agent**        | Local-first P2P sync via CRDTs, DIDs for identity, E2E encryption — no servers to maintain                |
| **Envoy**        | Structured logging and observability — codebase as knowledge graph, SPARQL queries, time-travel debugging |

<a id="tooling-layer"></a>

### Tooling Layer

| Library           | Purpose                                                                 |
| ----------------- | ----------------------------------------------------------------------- |
| **Quartermaster** | Application generator — `bend new` creates working apps from blueprints |

**Available blueprints:** minimal, blog, dashboard, form-builder, e-commerce,
collaborative-doc, knowledge-base.

<a id="quality-enforcement-pipeline"></a>

## Quality Enforcement Pipeline

Code quality is enforced through a strict pipeline:

```
Author writes code → Steward → deno fmt → Warden → Commit
```

1. **Steward** normalizes code shape (formatting, naming, one-function-per-file)
   with safe autofixes
2. **deno fmt** finalizes formatting to canonical form
3. **Warden** validates relationships (import boundaries, SHACL compositions)

Steward answers: "Is this well-formed?" Warden answers: "Is this allowed?"

Invalid code is rejected before it reaches the repository. The pipeline runs on
every commit and in CI.

<a id="three-rendering-modes"></a>

## Three Rendering Modes

**Development** — Fast iteration, skip the triple store:

```
TSX → IR → JSON → render → HTML
```

**Integration** — Full pipeline with ephemeral Oxigraph, verifies invariants:

```
TSX → IR → Triples → Oxigraph → SPARQL → JSON → render → HTML
```

**Production** — Full pipeline with persistent storage:

```
TSX → IR → Triples → Oxigraph → SPARQL → JSON → render → HTML
```

All three modes produce identical JSON. Integration mode catches pipeline bugs
before production.

<a id="progressive-enhancement"></a>

## Progressive Enhancement

Every component functions without JavaScript. This is mandatory.

Three layers compose the experience:

1. **Semantic HTML** — Works everywhere: screen readers, reading modes, minimal
   browsers
2. **CSS Styling** — Visual enhancements with graceful degradation
3. **JavaScript Enhancement** — Opt-in via `data-§-enhance` attributes

Enhancement improves the experience but never enables it.

<a id="high-availability-and-disaster-recovery"></a>

## High Availability and Disaster Recovery

When your entire application lives as queryable RDF triples, HADR stops being a
feature you add and becomes a property you inherit. One source of truth means
one backup strategy. Stateless rendering means instant failover. Named graphs
enable per-category replication policies.

See [docs/hadr.md](./docs/hadr.md) for comprehensive details.

<a id="what-you-actually-write"></a>

## What You Actually Write

The library ecosystem above is **internal infrastructure**. You don't interact
with it directly.

As a Sitebender consumer, you write this:

```tsx
<Recipe>
	<RecipeTitle>Grandmother's Apple Pie</RecipeTitle>
	<PrepTime duration="PT30M" />
	<CookTime duration="PT45M" />
	<Ingredients>
		<Ingredient amount="2" unit="cup">
			flour
		</Ingredient>
		<Ingredient amount="1" unit="cup">
			butter, cold
		</Ingredient>
		<Ingredient amount="6">apples, peeled and sliced</Ingredient>
	</Ingredients>
	<Instructions>
		<Step>Cut butter into flour until crumbly</Step>
		<Step>Press into pie dish</Step>
		<Step>Fill with apples and top with second crust</Step>
		<Step>Bake at 375°F for 45 minutes</Step>
	</Instructions>
</Recipe>
```

Step order is automatic — child position in TSX becomes `schema:position` in
triples. No manual numbering. Reorder by moving elements.

That's it. Semantic TSX with plain English component names and props. No
abbreviations. No framework jargon. No direct interaction with monads, SPARQL,
or triple stores.

**To start a new project:**

```bash
bend new my-recipe-site --template=blog
cd my-recipe-site
bend dev
```

Quartermaster scaffolds a working application. You modify semantic components to
match your domain. The 20 libraries handle type safety, validation, rendering,
state, persistence, and everything else — invisibly.

The complexity documented above exists so yours doesn't have to.

<a id="installation"></a>

## Installation

No barrel files. Import directly from source files. Functions are default
exports; types and constants are named exports.

```typescript
import Essay from "@sitebender/architect/documents/Essay/index.tsx";
import type { EssayProps } from "@sitebender/architect/documents/Essay/index.tsx";
```

<a id="license"></a>

## License

MIT
