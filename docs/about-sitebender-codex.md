# Sitebender

Sitebender is a Deno TypeScript TSX web framework that uses TSX components as a declarative DSL for constructing powerful, scalable, robust, versatile, standards-compliant, accessible, offline-capable, distributed web sites and applications. The entire application can be constructed in TSX components.

There are 20 libraries in the Sitebender project. Each provides key functionality. These are the current names and simple descriptions:

## Toolsmith

Toolsmith is a strict FP utility function library and more. It provides:

1. Wrappers around all the JS OOP methods (array.map, string.join, map.get, set.add, etc.). These turn them into curried functions for partial application with the data parameter last (array.map(fn) -> map(fn)(monad(array)). The data parameter can be wrapped in one of three monads: Maybe, Result (fail-fast), Validation (accumulate errors). It returns the result in the same type of monad.
2. Wrappers around every other JS function, such as the Math library, also curried and three-path.
3. Tagged types for runtime type checking, including a full set of numeric types: Integer, Fraction, PrecisionNumber, WholeNumber (safe number integer), SafeFloat, and arithmetic operations to perform on them (add, subtract, multiply, divideBy, etc.). Mixed numeric types means the less precise type is "promoted" to the more precise type (e.g., Integer + Fraction means Integer is promoted to a Fraction before the operation). All the Temporal types are also wrapped and turned into a pure FP library with JS Temporal underneath.
4. A help system for use in place of "errors". The philosophy is _do not scold your users_. Provide help and suggestions. If the user fails, it is our fault for not making it obvious what to do.
5. A full set of monads (maybe, either (for branching, not errors), result (catch one error), validation (accumulate errors), future, io, lazy, reader, writer, effect (and schedule).
6. Logic functions such as and, or, xor, not as well as relational operators (greaterThan, equalTo).
7. Guards and predicates of all types (isString, isNotNullish, isEmailAddress, etc.)
8. Conversion functions such as fractionToInteger, toString, toJson, etc.

Much more. This is the most essential library used by all the others.

## Architect

Architect is a semantic component library with thousands of semantic TSX components (e.g., Essay, Poem, Recipe, Tool, Event, Calendar, Schedule, Action), many of them based on the schema.org types (all are represented). The library wraps HTML elements with private wrappers (e.g., <\_A> wraps <a>) and the createFunction compiler automatically replaces every <a> with <\_A>. The wrappers type guard every attribute and element to ensure accessibility to WCAG AAA and WHATWG/W3C standards. And these components can automatically include JSON-LD, RDFa, or microdata (or all three).

The goal here is that you use the **semantic components** exclusively and never have to write any HTML. Our HTML wrappers are context aware, so instead of <h1> or <h2>, you use <Heading> and then createElement (or render) determines the nesting and assigns 1, 2, etc. automatically.

In short, Architect fixes the shortcomings of HTML and allows users to work in a purely intuitive and semantic environment.

Instead of converting the TSX to HTML, the pipeling is:

```
TSX component -> IR -> Turtle triples -> Oxigraph triple store -> SPARQL query -> JSON/TOML/YAML/etc. -> renderToDom/renderToString -> HTML
```

This means that we have an ontology and can use SHACL to enforce our data schema and OWL2 to reason across it.

## Artificer

Artificer extends Architect to provide behaviors by wrapping every Toolsmith function (add, map, reduce, join, lens, etc.) in a TSX component. Over a thousand components, including "injectors" that allow the code to inject values from anywhere: elements, attributes, cookies, the URL, state, localStorage, sessionStorage, API calls, the system clock — everywhere. Lazily and asycnchronously.

The pipeline for Artificer looks like this:

```
TSX component -> IR -> Turtle triples -> Oxigraph triple store -> SPARQL query -> JSON/TOML/YAML/etc. -> compose -> pure JS functions
```

These functions can be attached as properties to HTML elements for validation, conditional display, calculations, formatting, etc. Or use server-side or data-source-side for determining data shape (the schema) and validation. Single source of truth. Same validation everywhere.

There is much more, but that's the essential service that Artifice provides.

## Custodian

Custodian adds state management that respects the web's fundamental architecture. Works without JavaScript, enhances progressively, and treats the server (triple store) as the source of truth.

Custodian rejects the modern antipattern of duplicating server state on the client. Instead, it embraces the web's original design: stateless requests with state encoded in URLs and forms. When JavaScript is available, Custodian intercepts these interactions for optimistic updates and offline support, but the fundamental model remains unchanged.

Every interaction works identically with or without JavaScript:

- **Lynx/IE11**: Form submission → server processes → new page
- **Modern browser (no JS)**: Same as above
- **Modern browser (JS)**: Form submission → preventDefault → local state update → background sync

State isn't something to be "managed" — it's something to be transformed through pure functions, encoded in URLs, and synchronized via idempotent operations. The browser already has a state machine (the history API), a persistence layer (URLs), and a synchronization protocol (HTTP). Custodian orchestrates these existing pieces into a coherent whole.

## Operator

Operator provides a pub/sub event system where events are triples. Publish, subscribe, replay, query. Event sourcing built in. Events are triples. Channels are triples. Projections are triples. Everything that applies to triples applies to events.

## Quartermaster

Quartermaster is the application generator for Sitebender. Like `rails new`, but for the Sitebender ecosystem. It creates a complete, working Sitebender application. Starts the HTTPS dev server. Opens your browser. Opens your editor. All automatically.

Choose from a selection of "blueprints" (templates): blog, dashboard, form-builder, e-commerce, etc. Infinitely configurable (choose your libraries). Works by CLI or plugins to popular IDEs and code editors (VSCode, Zed, etc.)/

## Linguist

Linguist adds i18n. Internationalization as declarative data. Author translations in TSX, store as triples, render anywhere.

Translations are triples. Everything that applies to triples applies to translations.

## Formulator

Formulator works with Artificer to make complex formulas easier. Instead of composing many components to build an equation for, say, validation, you can just do this:

```tsx
<Validation formula="(a² - b) / (c + d)">
	<FromElement name="a" selector="#a" />
	<FromElement name="b" selector="#b" />
	<FromElement name="c" selector="#c" />
	<FromElement name="d" selector="#d" />
</Validation>
```

Formulator is biderctional. Given the full TSX components, it can generate the formula.

## Exchequer

Commerce primitives as declarative data. Type-safe products, orders, payments, returns, and quotes. Zero runtime dependencies.

Exchequer provides **primitives**, not a complete ecommerce platform. Products are triples. Calculations are pure. Payments are data. State machines, events, and sync live in other libraries where they belong.

- **Products are triples** — Stored in Pathfinder, queryable via SPARQL, versioned automatically
- **Calculations are pure** — No mutations, exact decimal arithmetic, currency-safe
- **Payments are data** — Unified model across providers, adapters for Stripe, PayPal, Square
- **State is elsewhere** — Custodian handles order workflows
- **Events are elsewhere** — Operator handles pub/sub
- **Sync is elsewhere** — Agent handles distribution
- **Pricing rules are elsewhere** — Reckoner handles promotions, discounts, refund policies

## Reckoner

Pricing transformations and value operations. Promotions, discounts, refund policies, loyalty programs, credit management. The reckoning.

Exchequer defines what exists. Reckoner calculates what you owe.

Every price transformation is a pure function. Every policy is declarative data.
Every calculation is auditable. Reckoner takes Exchequer entities and applies
rules to determine final prices, refund amounts, loyalty rewards, and credit
positions.

- **Promotions are data** — Rules, eligibility, stacking policies as triples
- **Calculations are pure** — No side effects, deterministic, testable
- **Policies compose** — Stack discounts, layer rules, combine programs
- **Everything auditable** — Every price transformation traceable

## Pathfinder

Triple store integration for Sitebender. SPARQL queries, named graphs, vector similarity search.

Pathfinder is the persistence layer. Every library that needs to store or query data uses Pathfinder. Pathfinder provides both Oxigraph and Qdrant data stores and APIs for creating and querying them. All with TSX components (as with every Sitebender library).

Features:

- Type-safe SPARQL query builder with fluent API
- Oxigraph triple store connection and query execution
- Qdrant vector database integration with semantic similarity search
- Configuration validation with error accumulation
- Result/Validation monads for error handling (no exceptions)
- Pure functions with immutable data structures
- Full TypeScript type safety
- Comprehensive test coverage (85+ tests)

## Orchestrator

Workflow automation as triples. Think n8n, but declarative TSX that compiles to RDF, executes across distributed systems, and integrates with the Sitebender ecosystem.

## Sentinel

> **Authentication and authorization as declarative data, not imperative code**

Sentinel brings authentication, authorization, and security policies into the Sitebender ecosystem. No more auth libraries, no more middleware, no more confusion about who can do what.

**Security is not a feature. It's a property of the data model.**

While traditional auth systems bolt security onto applications as an afterthought, Sentinel makes security policies first-class citizens in your triple store:

- **Authentication** as verifiable credentials
- **Authorization** as SHACL shapes
- **Policies** as declarative rules
- **Sessions** as cryptographic proofs
- **Mocking** as test scenarios

## Agent

> **Distributed, local-first applications through declarative components**

Agent is the bridge between Sitebender's pure functional world and the decentralized web. Write declarative components, get a distributed application. No servers to run, no backends to maintain, no corporate middlemen.

**Everything distributed should be as simple as everything local.**

While Artificer makes calculations and validations declarative, Agent extends this to the distributed web:

- **Distributed state** through CRDTs
- **P2P networking** without central servers
- **Decentralized identity** through DIDs
- **Semantic data** through triple store integration
- **Privacy by default** through encryption

## Arborist

Arborist is a parsing library for Deno TypeScript and TSX. When you need to understand the structure of source code — the functions it contains, where comments appear, what modules it imports — you use Arborist. It returns this information as structured data, leaving interpretation to other libraries.

## Quarrier

Property-based testing with SHACL-aware generation. The same shapes that validate your data also generate your test cases. No manual generator writing for domain types. Define your shape once, get validation AND test generation.

## Auditor

Auditor is a formal verification system that mathematically proves code correctness through theorem proving, property verification, and automated proof generation.

### Formal Verification

- **Z3 Integration** — Automated theorem proving via SMT solving
- **Proof Generation** — Machine-checkable certificates of correctness
- **Counterexamples** — Exact inputs that violate properties

### Property Verification

- **Mathematical Laws** — Associativity, commutativity, distributivity
- **Invariants** — State consistency across transitions
- **Bounds** — Outputs stay within specified ranges
- **Termination** — Functions always complete

### IR Analysis

- **Direct IR verification** — Works with Artificer's IR format
- **AST analysis** — Via Arborist for TypeScript/JSX
- **Branch coverage** — Proves paths reachable or dead
- **Complexity analysis** — Proves Big-O bounds

### Performance Verification

- **Complexity proofs** — Verify O(n), O(log n), O(1) claims
- **Resource bounds** — Prove memory usage limits
- **Termination proofs** — No infinite loops
- **Optimization verification** — Prove optimizations preserve semantics

### Test Generation (When Needed)

When formal proofs aren't feasible, Auditor generates tests:

- **Counterexample tests** — From failed proofs
- **Property-based tests** — For unverifiable properties
- **Coverage completion** — Fill gaps proofs can't reach
- **Regression tests** — Capture fixed bugs

## Envoy

Transforms your codebase into a queryable, navigable knowledge system. The code IS the documentation.

More than a replacement for JSDoc, in Envoy, documentation is not separate from code. It IS the code, understood.

Envoy takes what exists — your actual code, filesystem structure, and git history — and transforms it into:

- **Living documentation** that updates automatically
- **A knowledge graph** queryable with SPARQL
- **Developer experience metrics** with five-smiley feedback
- **Code intelligence** that machines and humans can navigate

All achieved through one principle: **The code is the single source of truth.**

Where traditional tools require developers to annotate code, Envoy derives understanding directly from structure, types, and relationships. The five comment markers exist only for what machines genuinely cannot infer.

### Comment Markers

Five markers for information machines cannot derive. Use sparingly.

| Marker | Purpose                             | Example                                            |
| ------ | ----------------------------------- | -------------------------------------------------- |
| `//++` | Description (mandatory for exports) | `//++ Validates email addresses`                   |
| `//??` | Help, gotchas, examples             | `//?? [GOTCHA] Doesn't validate disposable emails` |
| `//--` | Tech debt with remediation          | `//-- [REFACTOR] Should return Result`             |
| `//!!` | Critical blocking issues            | `//!! [SECURITY] SQL injection vulnerability`      |
| `//>>` | Semantic links                      | `//>> [NEXT] [Session](./session/index.ts)`        |

## Steward

Steward is a deterministic, non-configurable Codex style and structure enforcer. Steward normalizes code shape and folder layout up-front so downstream tools (Envoy, Auditor, Artificer, Warden) operate on a predictable surface. It complements Warden by focusing on mechanical style/shape with safe autofixes; Warden handles import boundary enforcement and SHACL validation.

- **Runtime:** Deno + TypeScript, pure ESM, zero runtime deps (uses Arborist/TS compiler for AST)
- **Policy:** Opinionated, no user overrides. Codex rules only.

### Goals

- Enforce Codex style guide and folder privacy conventions with zero configuration.
- Provide high-quality autofixes where safe; stabilize printing via `deno fmt`.
- Emit machine- and human-friendly diagnostics (JSON + pretty).
- Run fast (repo-wide target ≤ ~2–3s for checks/fixes on typical laptops).
- Reduce Warden false positives by normalizing input shape before governance checks.

## Warden

Import boundary enforcement and SHACL validation. The guard that ensures code stays where it belongs and compositions remain valid.

### Import Guard

Prevents libraries from accessing private (`_`) paths in other libraries.

### Composition Guard

Validates UI compositions against OWL2/SHACL ontology. Invalid structures never save to the triple store.

If it doesn't fit the ontology, it doesn't exist in the triple store.
