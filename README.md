# Sitebender Studio

A declarative DSL for building enterprise applications using only TSX/JSX.

## The Paradigm Shift

Most web frameworks treat code as code. You write functions, manage state in
closures, and hope your types survive until runtime. Your application exists as
source files that must be parsed, compiled, and executed.

Sitebender inverts this model. **Your entire application — structure, content,
behavior, validation — exists as queryable semantic data in a triple store.**
The rendered interface is just one projection of the underlying knowledge graph.

```
TSX/JSX → IR → Turtle Triples → Oxigraph → SPARQL → JSON → render → HTML/DOM
```

This isn't an implementation detail. It's the foundation that enables
capabilities impossible with traditional approaches.

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

## AI-Safe Architecture

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

This matters because AI systems (and humans) make mistakes. Documentation gets
ignored. Conventions get forgotten. But structural validation at the data layer
cannot be bypassed.

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

## The Library Ecosystem

### Foundation Layer

| Library       | Purpose                                                        |
| ------------- | -------------------------------------------------------------- |
| **Toolsmith** | Runtime type system, precision arithmetic, monads, Help system |
| **Arborist**  | SWC-based AST parsing for JSX transformation                   |

### Rendering Layer

| Library       | Purpose                                                                         |
| ------------- | ------------------------------------------------------------------------------- |
| **Architect** | Semantic authoring language that compiles to HTML via the triple store pipeline |
| **Artificer** | Reactive behaviors as data: calculations, validation, conditional display       |

### Data Layer

| Library        | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| **Pathfinder** | Triple store integration, SPARQL queries, named graphs |
| **Custodian**  | State management that respects web architecture        |
| **Quarrier**   | Test data generation respecting validation constraints |

### Application Layer

| Library        | Purpose                                                             |
| -------------- | ------------------------------------------------------------------- |
| **Formulator** | Expression parsing and evaluation                                   |
| **Exchequer**  | Commerce primitives: products, orders, payments as declarative data |
| **Linguist**   | Internationalization where translations are RDF triples             |
| **Sentinel**   | Authentication, authorization, security policies as data            |

### Quality Layer

| Library     | Purpose                                                  |
| ----------- | -------------------------------------------------------- |
| **Steward** | Code style enforcement (deterministic, non-configurable) |
| **Warden**  | Architectural governance via ontology validation         |
| **Auditor** | Formal verification of validation logic                  |

### Communication Layer

| Library          | Purpose                                                           |
| ---------------- | ----------------------------------------------------------------- |
| **Operator**     | Pub/sub event system scaling from local DOM to distributed global |
| **Orchestrator** | Workflow coordination                                             |
| **Agent**        | Distributed data synchronization via CRDTs                        |
| **Envoy**        | Structured logging and observability                              |

### Tooling Layer

| Library           | Purpose                               |
| ----------------- | ------------------------------------- |
| **Quartermaster** | Application scaffolding and templates |

## Three Rendering Modes

**Development** — Fast iteration, skip the triple store:

```
JSX → IR → JSON → render → HTML
```

**Integration** — Full pipeline with ephemeral Oxigraph, verifies invariants:

```
JSX → IR → Triples → Oxigraph → SPARQL → JSON → render → HTML
```

**Production** — Full pipeline with persistent storage:

```
JSX → IR → Triples → Oxigraph → SPARQL → JSON → render → HTML
```

All three modes produce identical JSON. Integration mode catches pipeline bugs
before production.

## Progressive Enhancement

Every component functions without JavaScript. This is mandatory.

Three layers compose the experience:

1. **Semantic HTML** — Works everywhere: screen readers, reading modes, minimal
   browsers
2. **CSS Styling** — Visual enhancements with graceful degradation
3. **JavaScript Enhancement** — Opt-in via `data-§-enhance` attributes

Enhancement improves the experience but never enables it.

## High Availability and Disaster Recovery

An unexpected consequence of "everything is data": enterprise-grade resilience
emerges naturally from the architecture.

Traditional applications scatter state across application memory, database rows,
file systems, caches, and browser storage. Recovering from failure means
coordinating N different backup strategies, hoping nothing falls through the
cracks. Teams bolt on HADR as an afterthought, fighting their own architecture
every step of the way.

Sitebender's triple store foundation inverts this. When your entire
application—structure, content, behavior, state—lives as queryable RDF triples,
HADR stops being a feature you add and becomes a property you inherit:

- **One source of truth** → one backup strategy, one recovery procedure
- **Stateless rendering pipeline** → any node can serve any request, instant
  failover
- **Named graphs** → per-category replication policies without multiple
  databases
- **Browser-side Oxigraph** → offline operation with automatic conflict
  resolution
- **Immutable event log** → point-in-time recovery with complete audit trail
- **SHACL validation** → automatic integrity verification after restoration

The architecture doesn't _support_ HADR. It _embodies_ it.

See [HADR.md](./HADR.md) for comprehensive details.

## Getting Started

```bash
deno add @sitebender/architect @sitebender/artificer @sitebender/toolsmith
```

```tsx
import Essay from "@sitebender/architect/documents/Essay/index.tsx";
import Heading from "@sitebender/architect/documents/Heading/index.tsx";
import Title from "@sitebender/architect/documents/Title/index.tsx";

<Essay>
	<Heading>
		<Title>My First Sitebender Application</Title>
	</Heading>
</Essay>;
```

Direct imports. No barrel files. The path IS the documentation.

## License

MIT
