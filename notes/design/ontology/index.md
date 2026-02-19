# Graphic Design Ontology

This document specifies the intended ontology for **graphic design as a compositional language**. It formalizes the structural primitives of design artifacts (compositions, elements, geometry, style, and structural systems) and the critique/analysis layer (principle statements) in a way that is **queryable, validatable, and deterministic**.

This is a **greenfield** specification: there is exactly **one** evolving spec state. The canonical truth is the current content of the RDF vocabulary and SHACL constraint sets defined by this document set.

---

# 1. Purpose

Graphic design is treated as a **compositional language**:

* **Elements** provide vocabulary (what exists in the visual field).
* **Principles** provide grammar (relationships and structural claims about elements).
* **Structure systems** (typography, grid, layers) provide composition mechanics.

The ontology models:

1. **What is in a composition** (instances, types, geometry, style, structure).
2. **What design principles are claimed to be present** (reified statements).
3. **Closed-world sealing** for deterministic validation and projection.

This ontology is intended to support:

* semantic authoring and analysis
* deterministic validation
* deterministic downstream projections/renderings
* stable internal composition graphs suitable for hashing/caching

---

# 2. Canonical modeling pattern

## 2.1 Composition as the root scope

A `gd:Composition` is a bounded design artifact (page, poster, screen, card, spread, etc.).

A composition contains:

* a canvas (`gd:hasCanvas`)
* element instances (`gd:hasElement`)
* optional grid system (`gd:hasGrid`)
* optional regions (`gd:hasRegion`)
* optional layers (`gd:hasLayer`)
* exactly one declared communicative intent (`gd:intent`)

A composition also links to its declared principle statements:

* `gd:expresses` links a `gd:Composition` to the `gd:PrincipleStatement` nodes it asserts.

## 2.2 ElementType vs ElementInstance

The ontology distinguishes:

* `gd:ElementType`: reusable conceptual type/template (“headline text”, “photo”, “circle mark”).
* `gd:ElementInstance`: an actual placed instance inside a composition.

Each `gd:ElementInstance` MUST specify:

* `gd:instanceOf` → `gd:ElementType`
* `gd:frame` → `gd:Rect`
* `gd:style` → `gd:Style`
* `gd:semanticRole` → `gd:Role`
* `gd:zIndex` → integer

This separation supports reuse, clarity, and deterministic composition graphs.

## 2.3 Principles as first-class statements

Design principles are not represented as informal tags. Instead, each design claim is reified as a node:

* `gd:PrincipleStatement`

Each `gd:PrincipleStatement` MUST specify:

* `gd:principleType` → a controlled term (`gd:Principle`)
* `gd:scope` → the scope of the claim (composition, region, etc.)
* one or more `gd:participant` → `gd:ElementInstance`

This makes critiques and structural claims queryable and validatable, e.g.:

* “This composition expresses contrast between these two elements”
* “These elements participate in a balance relationship”

## 2.4 Controlled vocabularies

The ontology includes controlled terms for:

* `gd:Principle` (e.g., `gd:Balance`, `gd:FigureGround`, `gd:Contrast`, etc.)
* `gd:Role` (e.g., `gd:Title`, `gd:Caption`, `gd:Decoration`, etc.)
* `gd:CommunicativeIntent` (e.g., `gd:Inform`, `gd:Brand`, etc.)

These are represented as **instances** of the respective class, not subclasses, to preserve deterministic behavior and avoid inference dependencies.

---

# 3. Structural primitives

## 3.1 Geometry

Each `gd:ElementInstance` has a `gd:frame` of type `gd:Rect` with:

* `gd:x`, `gd:y`, `gd:w`, `gd:h` (decimals)
* `w > 0` and `h > 0`

An optional `gd:transform` may be supplied as a `gd:Transform` node.

`gd:Transform` supports minimal affine parameters:

* `gd:tx`, `gd:ty`, `gd:sx`, `gd:sy`, `gd:rotationDeg`

Transform semantics are purely declarative: the graph does not rely on implicit transform defaults.

## 3.2 Style

Each `gd:ElementInstance` has a `gd:style` of type `gd:Style`.

`gd:Style` MUST specify:

* `gd:opacity` exactly once, range `[0..1]`

`gd:Style` MUST specify zero or one of each optional style refinement:

* `gd:fill` → `gd:Paint` (at most one)
* `gd:stroke` → `gd:Stroke` (at most one)
* `gd:typeStyle` → `gd:TypographicStyle` (at most one)

`gd:Paint` MUST specify:

* `gd:paintKind` exactly once (string)
* `gd:paintValue` exactly once (string)

`gd:Stroke` MUST specify:

* `gd:strokeWidth` exactly once (decimal, `>= 0`)

`gd:TypographicStyle` MUST specify:

* `gd:typeface` exactly once → `gd:Typeface`
* `gd:fontSize` exactly once (`> 0`)
* `gd:fontWeight` exactly once (`>= 1`)
* `gd:leading` exactly once (`> 0`)
* `gd:tracking` optional (at most one)

No implicit cascading semantics are permitted. If any style inheritance is used by tooling, it MUST be materialized into explicit triples in the canonical graph.

---

# 4. Structural systems

## 4.1 Grid system

A composition MUST declare zero or one grid system:

* `gd:hasGrid` → `gd:GridSystem`

A `gd:GridSystem` MUST specify:

* `gd:columnCount` exactly once (`>= 1`)
* `gd:rowCount` exactly once (`>= 1`)

A `gd:GridSystem` MUST specify optional extensions with explicit cardinality:

* `gd:hasUnit` → one or more `gd:GridUnit`
* `gd:baselineGrid` → `gd:BaselineGrid` (at most one)

`gd:GridUnit` is specialized into:

* `gd:ColumnUnit`
* `gd:RowUnit`
* `gd:GutterUnit`

A `gd:BaselineGrid` MUST specify:

* `gd:baselineStep` exactly once (`> 0`)

Grid semantics are declarative: no implicit snapping rules exist in the ontology; snapping, if used, must be materialized.

## 4.2 Regions and layers

A composition MUST declare zero or more structural scopes:

* `gd:hasRegion` → `gd:Region`
* `gd:hasLayer` → `gd:Layer`

`gd:Region` and `gd:Layer` are structural primitives used for scoping (principles, grouping, layout management). Ordering rules are expressed through explicit properties (e.g., `gd:zIndex` on elements and explicit layer linkages when defined).

---

# 5. Principle specializations

## 5.1 Figure–Ground statement

`gd:FigureGroundStatement` is a specialization of `gd:PrincipleStatement`.

It MUST satisfy all `gd:PrincipleStatement` requirements, plus:

* `gd:principleType` MUST be `gd:FigureGround`
* one or more `gd:foreground` → `gd:ElementInstance`
* one or more `gd:background` → (`gd:ElementInstance` or `gd:Region`)

A Figure–Ground statement’s `foreground` elements are required to also be `participant` elements (enforced normatively in the canonical rules and in SHACL constraints).

Background values are restricted to:

* a `gd:Region` owned by the same composition
* an `gd:ElementInstance` owned by the same composition

---

# 6. Closure and sealing

The ontology uses explicit ownership to support closed-world sealing.

## 6.1 Ownership

* `gd:ownedBy` links a structural node to exactly one `gd:Composition`
* `gd:owns` is a forward link from `gd:Composition` to owned nodes and MUST be used with explicit triples when present

All structural nodes that participate in the canonical composition graph MUST declare `gd:ownedBy` explicitly.

## 6.2 Same-owner sealing

A canonical composition graph MUST have no cross-composition structural references.

In other words:

* any structural node referenced by `gd:Composition` content MUST be owned by that same `gd:Composition`.

This sealing is enforced by:

* explicit ownership constraints (SHACL)
* composition seal constraints (SHACL-SPARQL)
* the canonical construction rules (normative prose)

---

# 7. Normativity and enforcement layers

This specification is enforced by a combination of:

1. **RDF vocabulary** (`gd-core.ttl`) — defines classes and properties
2. **SHACL constraints** — validate well-formedness, ownership rules, and reachability closure
3. **Canonical composition construction rules** — define the normative meaning of “canonical” and prohibit implicit semantics

Normative clauses are split across two enforcement layers:

- SHACL-enforceable graph constraints (bundle: `gd-all.shacl.ttl`)
- deterministic procedural constraints (canonical serialization, hashing, and validation orchestration)

A normative clause without an assigned enforcement mechanism in `CANONICAL_RULE_TRACEABILITY.md` is non-conformant.

Validation MUST load the full SHACL bundle entrypoint:

- `gd-all.shacl.ttl` (component files and loading contract are defined in `VALIDATION_BUNDLE.md`)

Normative coverage mapping from prose clauses to concrete constraints is defined in:

- `CANONICAL_RULE_TRACEABILITY.md`
- `fixture-coverage.csv`

---

# 8. Non-goals

This ontology does not define:

* rendering behavior
* layout heuristics
* perception/psychophysics inference
* “best design” judgments

It defines only:

* compositional structure
* explicit declared principle statements
* sealed, deterministic composition graphs suitable for validation and projection

---

# 9. Namespace policy

Namespace authority and immutability rules are defined in:

- `NAMESPACE_POLICY.md`

The canonical production namespaces are:

- `gd:` -> `https://paperhat.dev/ns/gd#`
- `gdm:` -> `https://paperhat.dev/ns/gdm#`

---

# 10. Pre-1.0 working mode

Pre-`1.0.0` change handling and governance deferral rules are defined in:

- `PRE_1_0_POLICY.md`

---

# 11. Responsive/adaptive policy schema

The 1.0.0 rules-based policy grammar is defined in:

- `POLICY_SCHEMA_1_0_0.md`
- `POLICY_EVALUATION_1_0_0.md`

---

# 12. Workshop-level adaptive projection notes

Workshop-level (Codex authoring) drafts for context/objective profiling and adaptive intent binding are defined in:

- `../../workshop/design/RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md`
- `../../workshop/design/DESIGN_POLICY_PRECEDENTS_1_0_0.md`
- `../../workshop/design/COMPILER_MAPPING_SPEC_1_0_0.md`
- `../../workshop/design/codex/adaptive-context-profile.schema.cdx`
- `../../workshop/design/codex/adaptive-objective-profile.schema.cdx`
- `../../workshop/design/codex/adaptive-optimization-profile.schema.cdx`
- `../../workshop/design/codex/adaptive-override-set.schema.cdx`
- `../../workshop/design/codex/adaptive-intent.schema.cdx`
