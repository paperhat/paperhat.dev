# Codex System Contract (LOCKED)

This document defines the **global, non-negotiable invariants** of the Sitebender Codex system.

It applies to:

- all Sitebender libraries
- all generated applications
- all tooling
- all LLM implementers

This document is **normative**.

---

**IMPORTANT:**

**Sitebender Codex is not a web framework.**

_It is a declarative language and compilation system for encoding meaning, constraints, behavior, and configuration, with the web as just one possible projection target._

## 1. Core Philosophy (Hard)

### 1.1 Everything Is Data

- All authored meaning is expressed as data.
- Behavior, validation, state transitions, and rendering are described declaratively.
- Code exists only to execute, never to encode meaning.

### 1.2 Single Sources of Truth

- **Applications:** CDX files under version control are the single source of truth.
- **Libraries:** Ontologies, constraints, and semantics live in libraries and are compiled into runtime stores.
- **Runtime stores:** Triple stores are compiled artifacts, never authoritative sources.

### 1.3 Referential Transparency

- All semantic functions are pure.
- Given the same inputs, the same outputs are produced.
- No hidden state, no ambient context, no mutation.

### 1.4 IO Is Isolated

- IO is explicitly separated from pure computation.
- IO boundaries are narrow, explicit, and owned by specific libraries.
- Pure code must never perform IO.

---

## 2. Authoring Surface (Hard)

### 2.1 CDX Is the Only Authoring Language

- Application developers write **only CDX**.
- No imports, no exports, no user-authored functions.
- No JavaScript or TypeScript in applications (except static assets).

### 2.2 Declarative Only

- No imperative control flow in authored content.
- All logic is expressed via composition.

---

## 3. The Canonical Pipeline (Hard)

All meaning flows through the same pipeline:

CDX
→ AST
→ IR
→ RDF / Turtle
→ Triple Store (Oxigraph)
→ SPARQL
→ ViewModel
→ Render Target

- Parsing, compilation, storage, querying, and rendering are distinct phases.
- Short-circuit paths (e.g. Dev modes) must preserve semantic equivalence.

---

## 4. Purity and the Three-Path Rule (Hard)

### 4.1 The Three Paths

Any operation that can fail must return one of:

- **Usable(value)** — successful result
- **Helps([...])** — one or more help messages
- **Pending** — computation not yet complete

Exceptions are forbidden.

### 4.2 Universal Return Shape

At runtime, all evaluatable operations return:

```ts
Future<Validation<Help, A>>;
```

- Async is universal.
- Laziness is preferred.
- Pending is not failure.

---

## 5. Toolsmith as Kernel (Hard)

### 5.1 Shared Foundations

All shared primitives live in **Toolsmith**, including:

- monads
- combinators
- newtype machinery
- BaseHelp
- help construction utilities
- numeric and structural types

No other library may reimplement these.

### 5.2 Extension, Not Duplication

Libraries may:

- extend BaseHelp with local codes
- define library-specific newtypes using Toolsmith primitives

Libraries may not:

- inspect monad internals
- bypass Toolsmith abstractions
- introduce ad-hoc error handling

---

## 6. Folder Structure and Privacy (Hard)

### 6.1 Public vs Private

- Any folder prefixed with `_` is private.
- Private folders are internal implementation details.
- Public API surface must be explicit and minimal.

### 6.2 Lowest Common Ancestor Rule

- Shared internal implementation lives at the lowest common ancestor.
- No junk-drawer folders.
- No “utils”, “misc”, or catch-alls.

---

## 7. Runtime Model (Hard)

### 7.1 Async and Lazy by Default

- All runtime evaluation is async.
- Evaluation is lazy and demand-driven.

### 7.2 Event-Driven Execution

- Runtime execution is driven by events, not direct calls.
- Event delegation is used; per-element handlers are avoided.

(See Engine Contract for details.)

---

## 8. Help System and Pedagogy (Hard)

### 8.1 Errors Become Help

- All failures are represented as Help.
- No error is silent.
- No error is thrown.

### 8.2 Pedagogical Tone

Help messages must:

- use “we”
- be polite and non-blaming
- explain what happened
- explain why
- suggest next steps

The system teaches; it does not scold.

---

## 9. Agile but Disciplined

- Contracts are living documents.
- Changes are allowed, but must be explicit.
- Major semantic changes trigger rewrites and archival of prior versions.
- Implementation follows contracts, never precedes them.

---

## Status

LOCKED.
