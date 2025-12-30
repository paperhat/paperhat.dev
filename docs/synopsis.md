# Sitebender Codex Synopsis

A comprehensive analysis based on reading all 20 library READMEs line by line.

## The 20 Libraries

### Foundation Layer

1. **Toolsmith** - Runtime type system, precision arithmetic (Integer, Fraction,
   PrecisionNumber using bigint), monads (Maybe, Result, Validation, Either, IO,
   Reader, Writer, Lazy, Future), Help system with never-blame philosophy, pure
   functions, curried, no exceptions

2. **Arborist** - TypeScript/TSX parsing via SWC WASM (fast, 20-50x faster than
   tsc) and deno_ast WASM (semantic analysis). Provides structural data for
   Envoy, Auditor, and Quarrier. The ONLY library that imports parser WASM
   packages. One parser, many consumers.

### Rendering Layer

3. **Architect** - Semantic TSX compiling to HTML via RDF/SPARQL. Pipeline:
   `TSX → createElement → IR → Turtle → Oxigraph → SPARQL → JSON → render/renderToString → HTML`.
   Context-aware compilation, route-based page promotion, 1000+ components,
   progressive enhancement, accessibility by default, OWL ontology-driven.

4. **Artificer** - Reactive behaviors as declarative data. Injectors (data
   sources), Operators (lift Toolsmith functions), Comparators, Logical
   Operators, Formatters, Display Components. ConceptForm for SHACL-driven
   forms. AI-safe via ontology validation through Warden.

### Data Layer

5. **Pathfinder** - Oxigraph triple store + Qdrant vector database. SPARQL query
   builder. Type-safe, immutable. Where ALL triples live. The persistence layer
   for everything.

6. **Custodian** - State management respecting web architecture. URL as state
   container, idempotent operations via UUIDs, signed continuations for
   multi-step flows. Works without JavaScript.

7. **Quarrier** - Property-based testing with SHACL-aware generation. The same
   shapes that validate data also generate test cases. Lazy shrink trees,
   bidirectional generators, metamorphic testing.

### Application Layer

8. **Formulator** - Bidirectional formula parsing. `(a² - b) / (c + d)` parses
   to nested Artificer IR and back. MathML output. Infix, prefix, postfix
   notation. Symbol recognition (alpha → α, sqrt → √).

9. **Exchequer** - Commerce primitives (products, orders, carts, payments,
   subscriptions, returns, gift cards, backorders, preorders, quotes). Products
   as triples. Pure calculations. SHACL constraints.

10. **Reckoner** - Pricing transformations. Promotions, discounts, refund
    policies, loyalty programs, credit management. Exchequer defines what
    exists; Reckoner calculates what you owe.

11. **Linguist** - Internationalization as triples. TSX authoring, ICU
    MessageFormat (full pluralization including Arabic's six forms), Intl API
    wrappers, locale detection, RTL support. Translations queryable via SPARQL.

12. **Sentinel** - Authentication/authorization as declarative data. OAuth2,
    WebAuthn, DID Auth, Magic Links. RBAC/ABAC/capability-based security. Mock
    auth for testing. TSX component API.

### Quality Layer

13. **Steward** - Deterministic, non-configurable code style enforcement. Runs
    BEFORE deno fmt and Warden. Safe autofixes. JSON diagnostics.

14. **Warden** - Import boundary enforcement (no cross-library underscore
    paths) + SHACL composition validation. Runs AFTER Steward. Invalid
    compositions never save to the triple store.

15. **Auditor** - Formal verification via Z3 theorem proving. Property
    verification, branch coverage proofs, complexity proofs, termination proofs.
    Test generation when proofs aren't feasible.

### Communication Layer

16. **Operator** - Pub/sub events as triples. Channels with scopes
    (local/broadcast/network/distributed). Event sourcing, CQRS. Progressive
    enhancement (forms work without JS). Warden validates all events.

17. **Orchestrator** - Workflow automation as triples. n8n-style but TSX or
    visual (bidirectional). Triggers (events, schedules, webhooks), stage
    dependencies, error handling, checkpoints, recovery. Distributed execution
    via Agent.

18. **Agent** - Local-first P2P via CRDTs, DIDs, E2E encryption. No servers
    required. Works offline. Declarative components for distributed state.

19. **Envoy** - Codebase as knowledge graph. Five comment markers for what
    machines can't derive: `//++` (description), `//??` (gotchas), `//--` (tech
    debt), `//!!` (critical), `//>>` (links). Automated code intelligence from
    Arborist/Auditor/Quarrier. SPARQL queries. Five-smiley feedback.

### Tooling Layer

20. **Quartermaster** - `bend new` application generator. Blueprints: minimal,
    blog, dashboard, form-builder, e-commerce, collaborative-doc,
    knowledge-base. HTTPS dev server. Editor integration.

## What Sitebender Actually Is

Sitebender is a deeply opinionated, radically ambitious attempt to rebuild web
development from first principles. The core insight is genuine: if your entire
application exists as semantic data (RDF triples) in a queryable store
(Oxigraph), capabilities emerge that are impossible with traditional approaches:

- Query your application semantically (SPARQL over your UI)
- Apply changes via data updates, not code changes
- Version via named graphs, not text diffs
- Federate data from multiple sources at query time
- Let inference engines derive facts you didn't program
- Validate compositions structurally, not procedurally

### The Technical Foundation Is Coherent

1. **Toolsmith** provides mathematical rigor: exact arithmetic, monadic error
   handling, no exceptions, pure functions
2. **Arborist** centralizes parsing: one parser, many consumers
3. **Pathfinder** centralizes persistence: one store, everything is triples
4. **Warden** gates validity: invalid compositions never persist

### The Layering Is Well-Designed

- Foundation: Toolsmith (types/monads), Arborist (parsing)
- Rendering: Architect (structure), Artificer (behavior)
- Data: Pathfinder (storage), Custodian (state), Quarrier (testing)
- Application: Formulator, Exchequer, Reckoner, Linguist, Sentinel
- Quality: Steward → deno fmt → Warden → Auditor
- Communication: Operator (events), Orchestrator (workflows), Agent
  (distribution)
- Developer: Envoy (docs), Quartermaster (generation)

### The Philosophy Is Consistent Across All Libraries

- Everything is data, queryable, versionable
- Pure functions, no mutations, no exceptions
- Help, not scold (never blame the user)
- Progressive enhancement (works without JavaScript)
- 100% test coverage, no unreachable code
- One function per file, curried, no classes

### The Ambition Is Extraordinary

This aims to make building distributed, offline-capable, accessible,
standards-compliant web applications as simple as writing semantic TSX. If it
works, it democratizes capabilities currently requiring large teams.

## Codex README Audit Findings

### What Is Correct

1. **The paradigm shift is accurately conveyed** - the triple store foundation
   and its implications are well explained
2. **All 20 library descriptions are accurate** - verified each against the
   library README; no factual errors
3. **The three monads table is correct** - Maybe/Result/Validation with their
   use cases matches Toolsmith exactly
4. **The Help philosophy is accurately conveyed** - never scold, never blame,
   provide path forward
5. **The pipeline diagram is essentially correct** - minor omission of
   `createElement` step
6. **Progressive enhancement is well covered** - three layers, mandatory
   accessibility
7. **Schema-driven forms via SHACL is accurate** - ConceptForm, automatic widget
   selection
8. **The rendering modes are correct** - Development, Integration, Production
   match Architect

### What Was Missing (Now Corrected)

1. **The quality enforcement pipeline** - Steward → deno fmt → Warden was not
   mentioned. Now added.

2. **Arborist's foundational role was underemphasized** - Envoy, Auditor, and
   Quarrier all depend on Arborist. Now clarified.

3. **Quartermaster's blueprints** - Now listed: minimal, blog, dashboard,
   form-builder, e-commerce, collaborative-doc, knowledge-base.

### What Was Potentially Misleading (Now Corrected)

1. **"Toolsmith runs in the background"** - Toolsmith doesn't "run" anywhere.
   It's a library of pure functions. Corrected to clarify.

2. **Agent: "(Plain English interface TBD)"** - Agent's README has nothing about
   natural language interfaces. Removed until documented.

3. **The HADR section** - While the architecture enables these properties, it
   read as more speculative than the rest. Moved to separate document.

---

_Synopsis created December 2024 based on thorough line-by-line review of all 20
library READMEs._
