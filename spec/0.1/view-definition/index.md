# Codex View Definition Specification

Status: **NORMATIVE**
Lock State: **LOCKED**
Version: **0.2**
Editor: **Charles F. Munat**

---

## 1. Purpose

This specification defines **Views** in Codex: what they are, how they are authored, how they bind to domain data, and how they participate in the Paperhat processing pipeline.

This document governs **View authoring and semantics only**.

It explicitly does **not** define:

* rendering
* layout
* styling
* interaction
* target-specific behavior
* Design Policy

This document is **Normative**.

A View answers one question only:

> **What information is included, in what structure, and in what order?**

---

## 2. Scope

This specification governs:

* the structure of View documents
* allowed Concepts and Traits in a View
* data binding via `source`
* semantic signaling via `Flag`
* compilation of Views into the View Graph and ViewModel

This specification does **not** govern:

* schema or ontology design
* query languages
* rendering targets
* adaptive behavior (Design Policy)
* filesystem layout beyond module scoping

---

## 3. Core Terms (Normative)

### 3.1 View

A **View** is a declarative specification that:

* selects information from domain data
* organizes that information structurally
* defines grouping and ordering
* exposes semantic signals for downstream reasoning

A View expresses **authorial intent**.

A View is **target-independent**.

---

### 3.2 View Graph

The **View Graph** is the semantic graph representation of authored Views.

* It is distinct from the Domain (Data) Graph.
* It is validated using a View ontology and SHACL constraints.
* It is persisted and queryable.

---

### 3.3 ViewModel

The **ViewModel** is a derived, ephemeral structure produced by combining:

* the Domain Graph
* the View Graph
* resolved bindings

The ViewModel is:

* deterministic
* target-neutral
* not persisted
* consumed by Design Policy

---

## 4. Module Scope and Files (Normative)

### 4.1 Module Containment

All Views are **module-scoped**.

A View MUST be authored within a module’s `views/` directory.

Views MUST NOT be global or shared across modules.

---

### 4.2 One View per File (Hard)

Each View document:

* MUST contain exactly one `<View>` root Concept
* MUST reside in its own folder
* MUST be named `view.cdx`

Views MUST NOT be grouped in a single file.

---

### 4.3 Identity

A View MAY declare an `id` Trait.

If present, the View `id` is resolved using the module’s `idBase` per the Codex ID Resolution Specification.

---

## 5. View Root (Normative)

### 5.1 Root Concept

A View document MUST have a single root Concept:

```cdx
<View>
	…
</View>
```

No wrapper Concepts (e.g. `<Views>`) are permitted.

---

## 6. Structural Concepts (Normative)

Structural Concepts define **information architecture only**.

They MUST NOT encode presentation, layout, or target behavior.

---

### 6.1 Section

`<Section>` groups related content.

* Defines hierarchy
* Defines conceptual separation
* Does not imply layout

---

### 6.2 Heading

`<Heading>` provides a human-readable label for a structural region.

* Content only
* No styling or level implied

---

### 6.3 Group

`<Group>` defines a semantic grouping.

Groups exist to support:

* reasoning
* omission
* reordering
* density control

Groups have no visual meaning.

---

### 6.4 OrderedList

`<OrderedList>` asserts that **order is semantically meaningful**.

* Sequence matters
* Rendering style is undefined

---

### 6.5 UnorderedList

`<UnorderedList>` asserts that **order is not semantically meaningful**.

---

### 6.6 Item

`<Item>` defines structure applied to each element of a list.

Rules:

* MUST appear only inside a list
* Establishes a new binding context

---

## 7. Data Binding (Normative)

### 7.1 `source` Trait

The `source` Trait binds a View node to domain data.

Rules:

* `source` values MUST be relative paths
* Paths are schema-governed
* No absolute paths
* No SPARQL, SQL, or expressions
* No filesystem or URL semantics

Example:

```cdx
<Text source="Ingredient.name" />
```

---

### 7.2 Binding Context

Each list `<Item>` establishes a new binding context.

Nested paths are resolved relative to that context.

---

## 8. Text Projection (Normative)

### 8.1 Text

`<Text>` projects opaque content from the domain graph.

* No transformation
* No formatting
* No interpretation

---

## 9. Semantic Signaling (Normative)

### 9.1 Flag

`<Flag>` elevates a boolean domain value to a **semantic signal**.

Traits:

* `name` — semantic signal identifier
* `when` — relative path resolving to a boolean

Rules:

* Flags do NOT prescribe presentation
* Flags exist solely for reasoning by Design Policy
* Flags MUST reference schema-authorized boolean values

Example:

```cdx
<Flag
	name="Optional"
	when="Ingredient.optional"
/>
```

---

## 10. Path Semantics (Normative)

* Paths are declarative references only
* Views MUST NOT:

  * compute
  * filter
  * aggregate
  * invent meaning
* All interpretation is deferred

---

## 11. Non-Goals (Hard)

Views MUST NOT:

* encode target logic
* reference screen, print, voice, etc.
* specify layout, typography, or widgets
* include adaptive rules
* perform computation
* perform IO

If it answers **“how should this adapt?”**, it is not a View.

---

## 12. Compilation and Pipeline Integration (Normative)

### 12.1 Compilation

Views are compiled by Scribe into the View Graph.

* Pure
* Deterministic
* Validated via SHACL

---

### 12.2 ViewModel Creation

At execution time:

1. Domain Graph is queried
2. View Graph is applied
3. A ViewModel is produced

The ViewModel:

* is ephemeral
* is not stored
* is consumed by Design Policy

---

## 13. Error Handling (Normative)

* Invalid paths → Help
* Invalid structure → Help
* Failed View → module execution fails (all-or-nothing)

---

## 14. Relationship to Other Specifications (Normative)

This specification depends on:

* Codex Naming and Value Specification
* Codex ID Resolution Specification
* View and Design Policy Selection Specification

In case of conflict:

* This document governs View semantics
* Naming governs names and literals
* ID Resolution governs identity

---

## 15. Summary

* Views define **structural projection**
* Views express **authorial intent**
* Views are **target-independent**
* One View per file
* `source` binds data
* `Flag` exposes semantic signals
* No rendering, no adaptation, no behavior

---

**End of Codex View Definition Specification v0.2**
