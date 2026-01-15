Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex View Definition Specification

This specification defines **Views** in Codex: what they are, what they may contain, how they bind to domain data, and how they participate in the Paperhat processing pipeline.

This document governs **View authoring and semantics only**.
It does not define rendering, layout, styling, interactivity, or target-specific behavior.

This document is **Normative**.

---

## 1. Purpose

Views define:

* **what information** is included from domain data
* **how that information is structurally organized**
* **the meaningful order** of included information

Views exist to separate:

* **information architecture** (Views)
  from
* **realization decisions** (Design Policy + renderers)

A View answers one question only:

> **What information is included, in what structure, and in what order?**

---

## 2. Scope

This specification governs:

* View documents authored in Codex
* the allowed View Concepts and Traits
* how Views bind to domain data
* how `source` paths are interpreted
* how Views compile into the View Graph and contribute to ViewModel creation

This specification does **not** govern:

* presentation, layout, typography, styling
* behavior or interaction
* target selection
* Design Policy
* rendering

This specification also does **not** govern View composition and override constructs such as Slots, Fills, and Use.
Those semantics are defined by the View Composition specification.

---

## 2.1 Dialect and Ontology (Normative)

Views are authored in Codex under the **View dialect**.

Rules:

- The View dialect is governed by a **View ontology** expressed as triples plus declarative constraints.
- The View ontology is authored in Codex using the **Schema Dialect** and compiled by Kernel.
- Kernel selects the View dialect based on artifact role during module assembly; shell tooling MUST NOT reinterpret view semantics.

---

## 3. Core Terms (Normative)

### 3.1 View

A **View** is a declarative specification that:

* selects information from the Domain Graph
* organizes that information structurally
* is target-independent

A View is authored in Codex and compiled into a **View Graph**.

---

### 3.2 View Graph

The **View Graph** is the semantic graph representation of authored Views.

* It is distinct from the Domain (Data) Graph.
* It is validated using a View ontology and SHACL constraints.
* It is stored and queryable.

---

### 3.3 ViewModel

The **ViewModel** is a derived, ephemeral structure produced by combining:

* the Domain Graph
* the View Graph
* resolved selection bindings

The ViewModel is:

* deterministic
* target-neutral
* not persisted

---

## 4. Module Scope (Normative)

### 4.1 Containment

All Views are **module-scoped**.

A View MUST be authored within a module’s `views/` folder as `view.cdx`.

Views MUST NOT be global.

---

### 4.2 Identity

A View MUST declare an `id` Trait.

The View `id` is resolved using the module’s active `idBase` according to the Codex ID Resolution Specification.

Example (Illustrative):

```cdx
<View id=recipe:default>
	...
</View>
```

---

## 5. View Root and Binding (Normative)

### 5.1 Root Concept

A View document MUST have exactly one root Concept: `<View>`.

---

### 5.2 Binding Context

A View is evaluated against a **current binding context**.

* At the top level, the binding context is the **bound domain entity** selected by Kernel (selection rules are governed elsewhere).
* Certain View constructs change the binding context (notably lists and items).

---

## 6. Allowed View Concepts (Normative)

A View MAY contain the following structural concepts.

These concepts express **structure only**.

Additional constructs MAY be permitted by other normative Paperhat specifications.
If present, they MUST be validated and applied according to those specifications.
In particular, Slots/Fills/Use are governed by the View Composition specification.

### 6.1 Section

`<Section>` groups related material.

Traits:

* `name` — optional string token used for deterministic node addressing by Design Policy

Rules:

* If `name` is present, it MUST be unique within the View.

---

### 6.2 Heading

`<Heading>` is a structural label for a section.

* Heading Content is opaque text Content.
* Heading does not prescribe typography, size, or styling.

---

### 6.3 Group

`<Group>` groups a set of sibling elements as a logical unit.

Traits:

* `name` — optional string token used for deterministic node addressing by Design Policy

Rules:

* If `name` is present, it MUST be unique within the View.

---

### 6.4 OrderedList

`<OrderedList>` asserts that sequence is semantically meaningful.

Traits:

* `source` — required relative path selecting a collection from the current binding context
* `name` — optional string token for policy addressing

---

### 6.5 UnorderedList

`<UnorderedList>` asserts that order is not semantically meaningful.

Traits:

* `source` — required relative path selecting a collection from the current binding context
* `name` — optional string token for policy addressing

---

### 6.6 Item

`<Item>` defines the structure applied to each element of a list.

Traits:

* `name` — optional string token for policy addressing

Rules:

* `<Item>` MUST appear only as a direct child of `OrderedList` or `UnorderedList`.
* `<Item>` establishes a new binding context: the current list element.

---

### 6.7 Text

`<Text>` projects a value from the current binding context into the ViewModel.

Traits:

* `source` — required relative path selecting a value or concept from the current binding context

Rules:

* `<Text>` performs no transformation.
* `<Text>` does not interpret Content.
* If the selected value is absent, handling is Help-driven (see §10).

---

### 6.8 Flag

`<Flag>` elevates a boolean value to a semantic signal for policy reasoning.

Traits:

* `name` — required string token naming the signal (example: `"Optional"`)
* `when` — required relative path selecting a boolean value from the current binding context

Rules:

* `when` MUST resolve to a boolean.
* `<Flag>` does not prescribe presentation.
* Flags are emitted into the ViewModel as structural signals.

Example (Illustrative):

```cdx
<Flag name="Optional" when="optional" />
```

---

### 6.9 Tags

`<Tags>` is a structural projection for tag collections.

Traits:

* `source` — required relative path selecting the tags collection

(Exact tag structure is schema-defined; Views do not define tag semantics.)

---

## 7. Path Semantics (Normative)

### 7.1 Relative only

All `source` and `when` values MUST be **relative paths**.

Forbidden:

* absolute IRIs
* filesystem paths
* URLs
* SPARQL, SQL, or embedded query languages
* computed expressions

---

### 7.2 Binding-relative resolution

Paths are resolved relative to the current binding context.

* At top level: relative to the bound domain entity.
* Inside `<Item>`: relative to the list element.

---

### 7.3 Schema-governed meaning

Path validity and meaning are governed by the domain schema/ontology.

Views do not invent semantics.

---

## 8. Design Policy Addressability (Normative)

Design Policy operates on ViewModel structure.
To enable deterministic policy application, Views MAY name structural nodes using `name`.

Rules:

* `name` is structural only.
* `name` must not encode target behavior.
* Policies MUST reference node names that exist in the ViewModel derived from the View.

---

## 9. Non-Goals (Normative)

Views MUST NOT:

* reference targets (`screen`, `print`, `voice`, etc.)
* encode presentation (layout, typography, styling)
* encode interaction or behavior
* perform computation
* perform IO
* embed executable logic or queries

---

## 10. Errors and Help (Normative)

* Invalid View structure MUST produce Help and invalidate the View.
* Invalid paths MUST produce Help.
* A module run MUST fail (all-or-nothing) if a required View fails validation or compilation.

---

## 11. Compilation and Kernel Integration (Normative)

### 11.1 Compilation

View documents are compiled by Kernel into the View Graph.

* Compilation is pure and deterministic.
* Validation occurs against a View ontology and SHACL constraints.

### 11.2 ViewModel Creation

During execution:

* Views are selected (selection rules governed elsewhere).
* Domain Graph + View Graph are combined to produce a ViewModel.

The ViewModel is ephemeral and feeds Design Policy application.

---

## 12. Anti-Examples (Normative)

Invalid (target reference):

```cdx
<View id=x>
	<When target=voice>
		...
	</When>
</View>
```

Invalid (embedded query):

```cdx
<Text source="SELECT ?x WHERE { ... }" />
```

Invalid (computed expression):

```cdx
<Text source="amount * 2" />
```

Invalid (absolute URL as a path):

```cdx
<Text source="https://example.test/title" />
```

---

## 13. Summary

* Views define inclusion, structure, and meaningful order.
* Views are module-scoped and stored as a separate View Graph.
* ViewModel is derived and ephemeral.
* `source` and `when` are relative, binding-context paths.
* `Text` projects values; `Flag` elevates booleans to signals.
* Structural nodes may be named for deterministic Design Policy addressing.
* Views contain no targets, no layout, no behavior.

---

**End of Codex View Definition Specification v0.1**
