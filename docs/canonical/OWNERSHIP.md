# Ownership and Responsibility Map (LOCKED)

This document defines **hard ownership boundaries** between Paperhat libraries.

Each responsibility has exactly one owner.

This document is **normative**.

---

## 1. Core Rule (Hard)

- Every responsibility has one owner.
- No responsibility is shared implicitly.
- Cross-library interaction happens only through defined interfaces.

---

## 2. Library Ownership

### Toolsmith

**Owns:**

- monads and combinators
- newtype framework
- BaseHelp and help utilities
- numeric and structural runtime types

**Does not own:**

- parsing
- rendering
- IO
- application semantics

---

### Scribe

**Owns:**

- CDX parsing
- AST construction
- IR generation
- RDF/Turtle emission
- round-trip fidelity

**Does not own:**

- validation semantics
- rendering
- runtime execution
- triple store lifecycle

---

### Pathfinder

**Owns:**

- triple store access
- SPARQL querying
- query result shaping

**Does not own:**

- ontology definition
- validation rules
- rendering

---

### Warden

**Owns:**

- validation enforcement
- SHACL contract checking
- rejection of invalid structures

**Does not own:**

- data storage
- rendering
- business logic

---

### Artificer

**Owns:**

- declarative behavior composition
- reactive calculations
- validation composition
- conditional display logic

**Does not own:**

- parsing
- storage
- UI primitives

---

### Architect

**Owns:**

- semantic UI components
- accessibility-correct markup
- presentational structure

**Does not own:**

- behavior logic
- validation
- state management

---

### Operator

**Owns:**

- pub/sub event system
- event sourcing
- event transport selection
- projections from events

**Does not own:**

- business logic
- rendering
- persistence of non-event data

---

### Custodian

**Owns:**

- application state containers
- derived state
- state invalidation

**Does not own:**

- event transport
- validation
- rendering

---

### Quartermaster

**Owns:**

- application scaffolding
- project structure generation
- dev server orchestration
- file watching and reload

**Does not own:**

- application semantics
- runtime execution
- library internals

---

## 3. Generated Applications

Generated applications:

- author CDX only
- do not own parsing, storage, or runtime machinery
- consume libraries declaratively

---

## 4. Conflict Resolution (Hard)

If two libraries appear to overlap:

1. Ownership is resolved by this document.
2. The document is amended explicitly if needed.
3. Code is changed to comply.

No “pragmatic exceptions.”

---

## Status

LOCKED.
