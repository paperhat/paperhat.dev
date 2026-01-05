# Sitebender Codex & Scribe

## Canonical Architecture, Routing, and Source-of-Truth Contract (LOCKED)

This document defines the **end-to-end architectural contract** for:

- Codex (`.cdx`) as the authoring surface
- Scribe as the semantic pipeline
- Quartermaster as the scaffolder and runtime orchestrator
- Routing, modularity, reuse, and data scoping
- Sources of truth and the role of the triple store

This document is **normative**.

---

## 1. Core Goals

Sitebender exists to:

1. **Minimize cognitive load** for application developers
2. Make the **human-authored artifacts** the source of truth
3. Enforce correctness via **formal semantics**, not conventions
4. Enable **fast, safe development** and **sound production behavior**
5. Keep architecture **simple, explicit, and deletable**

---

## 2. Codex (`.cdx`) Is the Authoring Surface

### 2.1 What Codex Is

Codex is a **declarative, semantic DSL** used to author:

- Application data (domain facts)
- Concepts / schemas
- UI projections (views, forms, cards, etc.)
- Composition and configuration

Codex is:

- CDX-like in syntax
- **Not JavaScript**
- **No expressions**
- **No imports / exports**
- **No imperative logic**

Codex is what the developer **sees, edits, diffs, and reasons about**.

---

### 2.2 Codex as Source of Truth (App Level)

For an application:

- **The CDX files in the app repo are the single source of truth for app-authored data**
- They are versioned in git
- They are human-readable
- They are reviewable

The developer never authors application data by editing triples.

---

## 3. Libraries as Sources of Truth (Semantic Level)

Sitebender libraries (Architect, Artificer, Custodian, Operator, Exchequer, etc.) are **also sources of truth**, but for a different class of knowledge:

- Ontologies (OWL2)
- Constraints (SHACL)
- Reference vocabularies
- Accessibility and compliance rules
- Semantic contracts for components and systems

These are:

- Authored by humans
- Versioned in library repos
- Distributed as triples
- **Not edited in the app**

---

## 4. The Triple Store Is a Compiled Runtime Image

### 4.1 What the Triple Store Is

The Oxigraph triple store is:

- **Derived**
- **Generated**
- **Queryable**
- **Replaceable**

It is built from:

```
compile(app CDX)
∪ load(library ontologies & constraints)
∪ load(reference datasets)
```

### 4.2 What the Triple Store Is Not

The triple store is **not**:

- The authoring surface
- The primary source of truth
- Something developers edit directly

It is a **materialized semantic index**.

---

## 5. Scribe: The Semantic Pipeline (One Library)

Scribe is a **single library** that owns the entire pipeline.

### 5.1 Pure Compilation Pipeline (Referentially Transparent)

```
CDX text
 → AST
 → IR
 → RDF Dataset (triples)
```

Properties:

- Pure
- Deterministic
- No IO
- Testable
- Cacheable

This is exposed as **compile**.

---

### 5.2 IO Boundary (Explicit and Isolated)

```
RDF Dataset
 → Oxigraph (load / commit)
 → SPARQL
 → QueryResult
```

Properties:

- Only place with side effects
- Config-driven (dev / test / prod)
- Same code path for test and prod

---

### 5.3 Pure Rendering Pipeline

Two equivalent pure inputs:

```
IR → ViewModel            (Dev preview)
QueryResult → ViewModel   (Store-backed)
```

Rendering is always pure:

```
ViewModel → DOM
ViewModel → HTML string
AST → CDX text (round-trip)
```

---

## 6. Execution Environments and Paths

### 6.1 Environments (Externally Visible)

Quartermaster selects one of:

1. **Dev**
2. **Test**
3. **Prod**

---

### 6.2 Dev Execution Paths (Internal to Dev)

#### Dev-A: Preview (Default)

```
CDX
 → AST
 → IR
 → ViewModel
 → DOM / HTML / CDX
```

- Fully pure
- No triple store
- Instant reload
- Honest because CDX is the source of truth

---

#### Dev-B: Store-Validated (Opt-in)

```
CDX
 → AST
 → IR
 → RDF
 → Oxigraph (in-memory)
 → SPARQL
 → QueryResult
 → ViewModel
 → Render
```

- Exercises full semantics
- Uses ephemeral store
- Slower, but safe

---

### 6.3 Test Mode

- Same as Dev-B
- Isolated store
- Used for assertions and fixtures

---

### 6.4 Prod Mode

- Same pipeline as Test
- Production store config
- Only configuration differs

---

## 7. Quartermaster vs Scribe

### Quartermaster Owns:

- Project scaffolding
- `modules/` layout
- File watching
- Dev server
- Routing
- Environment selection
- Store configuration

### Scribe Owns:

- Codex parsing and compilation
- Semantic lowering
- RDF generation
- Store IO adapters
- ViewModel generation
- Rendering

Scribe never watches files.
Quartermaster never compiles semantics.

---

## 8. Modules, Routing, and Reuse

### 8.1 Modules Are Folders

**A module is a folder.**
Everything related to that module lives inside it.

---

### 8.2 Primary Entry File

Each module may expose a primary public surface:

```
entry.cdx
```

This file is:

- The module’s public interface
- Rendered as a **Document** when routed
- Rendered as a **Fragment** when embedded

The render context is **explicit**.

---

### 8.3 Routing Rules

- Everything under `modules/` is a candidate
- Anything starting with `_` is **non-routable**
- Routes nest by folder hierarchy
- Dynamic segments may use `[param]`

Routing is a Quartermaster concern.

---

## 9. Data, Concepts, and Reuse (Option A, LOCKED)

### 9.1 Single Module Universe

There is **one module tree**: `modules/`.

Different kinds of modules are distinguished by **location and naming**, not roots.

---

### 9.2 `_data` and `_concepts`

- `_data/` contains **application-authored domain instances**
- `_concepts/` contains **schemas / concepts**

Both are:

- Non-routable
- Compiled by Scribe
- Loaded into the triple store

---

### 9.3 LCA (Lowest Common Ancestor) Rule

A `_data` or `_concepts` folder applies to **all modules beneath it**.

Therefore:

- Data used only by `a/b/c/**` → `a/b/c/_data`
- Data used by `a/b/c/**` and `a/b/e/f/**` → `a/b/_data`

**A module may only consume data defined at or above it in the hierarchy.**

This enables:

- Safe deletion
- Clean reuse
- Predictable scoping

---

## 10. Views vs Data

- Data modules define **what exists**
- View modules define **how it is projected**

Examples:

- `<Recipe>` → data (triples)
- `<RecipeCard of="iri:…">` → view
- `<Concept name="Person">` → schema
- `<ConceptForm of="Person">` → projection

Views never _contain_ data; they _reference_ it by identity.

---

## 11. Injectors (No Expressions)

Codex remains declarative.

Runtime values are introduced via **injector elements**, e.g.:

```
<FromSentinel name="userId" />
<FromQueryString name="email" />
<FromSystemClock />
```

No JavaScript.
No inline expressions.

---

## 12. Architectural Guarantees

- CDX is always human-authored truth
- Libraries are semantic authorities
- Store is always derived
- Dev preview is honest, not fake
- Full semantics are always available
- Modules are deletable units
- No page metaphor leakage
- No library explosion

---

## 13. Status

All of the following are **locked**:

- CDX as source of truth
- Library ontologies as source of truth
- Store as compiled runtime image
- Scribe pipeline structure
- Dev/Test/Prod semantics
- Dev-A / Dev-B split
- Module + `_data` + LCA model
- `entry.cdx` promotion/embedding rule

**This document is authoritative.**
