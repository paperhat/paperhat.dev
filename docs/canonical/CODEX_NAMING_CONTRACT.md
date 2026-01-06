# Codex Naming Contract — Core Vocabulary (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex documentation, tooling, and error messages

---

## 1. Purpose

This contract defines the **core naming vocabulary** used to describe Codex constructs.

Its goals are to:

- eliminate HTML / XML / UI / OO confusion
- keep terminology **semantic, declarative, and human-readable**
- support correct reasoning by humans, tools, and LLMs
- prevent ontology leakage into surface language

---

## 2. Core Terms (Normative)

### 2.1 Concept

A **Concept** is the primary surface construct in Codex.

A Concept is:

- a named declarative unit
- composed of **Traits** and child Concepts
- optionally identified with an `id`
- purely declarative (never imperative)

Examples:

- `<Recipe>`
- `<Step>`
- `<Policy>`
- `<Module>`

Notes:

- “Concept” refers to the _surface construct_, not a philosophical abstraction.
- Not all Concepts are entities.

---

### 2.2 Trait

A **Trait** is a named characteristic of a Concept.

A Trait:

- binds a **name** to a **Value**
- is declared inline on a Concept
- is schema-defined
- has no independent identity

Examples:

- `name="Bob"`
- `amount=200`
- `optional=false`

Traits are **not**:

- props
- traits
- fields
- parameters

---

### 2.3 Value

A **Value** is a literal or structured datum.

Values include:

- strings
- numbers
- booleans

Values are:

- immutable
- schema-typed
- never narrative

Example:

- `"Bob"`
- `200`
- `true`

---

### 2.4 Content

**Content** is opaque narrative data.

Content:

- is not interpreted by Codex
- may contain prose, code, poetry, or markup
- is always carried inside a Concept

Example:

```xml
<Description>
	A cool dude.
</Description>
```

---

### 2.5 Entity

An **Entity** is a Concept that has identity.

- A Concept **is an Entity iff it has an `id`**
- Entity identity is semantic and graph-addressable
- Identity rules are defined by schema, not syntax

Examples:

- `<Recipe id="recipe:spaghetti">` → Entity
- `<Step>` → not an Entity

---

## 3. Structural vs Semantic Concepts

This distinction is **terminological only** (no syntax difference):

- **Semantic Concepts** express domain meaning
  (`<Recipe>`, `<Person>`, `<Policy>`)

- **Structural Concepts** organize or group meaning
  (`<Steps>`, `<Data>`, `<Policies>`)

Authors do **not** need to reason about this distinction while writing Codex.

---

## 4. Forbidden Vocabulary (Normative)

The following terms MUST NOT be used to describe Codex constructs:

- concept
- component
- tag
- node
- class
- prop / property
- trait
- field
- parameter

---

## 5. Summary

- Codex is written in **Concepts**
- Concepts declare **Traits**
- Traits bind names to **Values**
- Concepts may carry **Content**
- Some Concepts are **Entities**

This vocabulary is mandatory and foundational.
