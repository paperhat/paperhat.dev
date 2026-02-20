# Workshop Design Ontology

This document specifies the intended ontology for **Workshop design as a compositional language**. It formalizes the structural primitives of design artifacts (compositions, elements, geometry, style, and structural systems) and the critique/analysis layer (principle statements) in a way that is **queryable, validatable, and deterministic**.

This is a **greenfield** specification: there is exactly **one** evolving spec state. The canonical truth is the current content of the RDF vocabulary and SHACL constraint sets defined by this document set.

---

# 1. Purpose

Workshop design is treated as a **compositional language**:

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

A `wd:Composition` is a bounded design artifact (page, poster, screen, card, spread, etc.).

A composition contains:

* a canvas (`wd:hasCanvas`)
* element instances (`wd:hasElement`)
* optional grid system (`wd:hasGrid`)
* optional regions (`wd:hasRegion`)
* optional layers (`wd:hasLayer`)
* exactly one declared communicative intent (`wd:intent`)

A composition also links to its declared principle statements:

* `wd:expresses` links a `wd:Composition` to the `wd:PrincipleStatement` nodes it asserts.

## 2.2 ElementType vs ElementInstance

The ontology distinguishes:

* `wd:ElementType`: reusable conceptual type/template (“headline text”, “photo”, “circle mark”).
* `wd:ElementInstance`: an actual placed instance inside a composition.

Each `wd:ElementInstance` MUST specify:

* `wd:instanceOf` → `wd:ElementType`
* `wd:frame` → `wd:Rect`
* `wd:style` → `wd:Style`
* `wd:semanticRole` → `wd:Role`
* `wd:zIndex` → integer

This separation supports reuse, clarity, and deterministic composition graphs.

## 2.3 Principles as first-class statements

Design principles are not represented as informal tags. Instead, each design claim is reified as a node:

* `wd:PrincipleStatement`

Each `wd:PrincipleStatement` MUST specify:

* `wd:principleType` → a controlled term (`wd:Principle`)
* `wd:scope` → the scope of the claim (composition, region, etc.)
* one or more `wd:participant` → `wd:ElementInstance`

This makes critiques and structural claims queryable and validatable, e.g.:

* “This composition expresses contrast between these two elements”
* “These elements participate in a balance relationship”

## 2.4 Controlled vocabularies

The ontology includes controlled terms for:

* `wd:Principle` (e.g., `wd:Balance`, `wd:FigureGround`, `wd:Contrast`, etc.)
* `wd:Role` (e.g., `wd:Title`, `wd:Caption`, `wd:Decoration`, etc.)
* `wd:CommunicativeIntent` (e.g., `wd:Inform`, `wd:Brand`, etc.)

These are represented as **instances** of the respective class, not subclasses, to preserve deterministic behavior and avoid inference dependencies.

---

# 3. Structural primitives

## 3.1 Geometry

Each `wd:ElementInstance` has a `wd:frame` of type `wd:Rect` with:

* `wd:x`, `wd:y`, `wd:w`, `wd:h` (decimals)
* `w > 0` and `h > 0`

An optional `wd:transform` may be supplied as a `wd:Transform` node.

`wd:Transform` supports minimal affine parameters:

* `wd:tx`, `wd:ty`, `wd:sx`, `wd:sy`, `wd:rotationDeg`

Transform semantics are purely declarative: the graph does not rely on implicit transform defaults.

## 3.2 Style

Each `wd:ElementInstance` has a `wd:style` of type `wd:Style`.

`wd:Style` MUST specify:

* `wd:opacity` exactly once, range `[0..1]`

`wd:Style` MUST specify zero or one of each optional style refinement:

* `wd:fill` → `wd:Paint` (at most one)
* `wd:stroke` → `wd:Stroke` (at most one)
* `wd:typeStyle` → `wd:TypographicStyle` (at most one)

`wd:Paint` MUST specify:

* `wd:paintKind` exactly once (string)
* `wd:paintValue` exactly once (string)

`wd:Stroke` MUST specify:

* `wd:strokeWidth` exactly once (decimal, `>= 0`)

`wd:TypographicStyle` MUST specify:

* `wd:typeface` exactly once → `wd:Typeface`
* `wd:fontSize` exactly once (`> 0`)
* `wd:fontWeight` exactly once (`>= 1`)
* `wd:leading` exactly once (`> 0`)
* `wd:tracking` optional (at most one)

No implicit cascading semantics are permitted. If any style inheritance is used by tooling, it MUST be materialized into explicit triples in the canonical graph.

---

# 4. Structural systems

## 4.1 Grid system

A composition MUST declare zero or one grid system:

* `wd:hasGrid` → `wd:GridSystem`

A `wd:GridSystem` MUST specify:

* `wd:columnCount` exactly once (`>= 1`)
* `wd:rowCount` exactly once (`>= 1`)

A `wd:GridSystem` MUST specify optional extensions with explicit cardinality:

* `wd:hasUnit` → one or more `wd:GridUnit`
* `wd:baselineGrid` → `wd:BaselineGrid` (at most one)

`wd:GridUnit` is specialized into:

* `wd:ColumnUnit`
* `wd:RowUnit`
* `wd:GutterUnit`

A `wd:BaselineGrid` MUST specify:

* `wd:baselineStep` exactly once (`> 0`)

Grid semantics are declarative: no implicit snapping rules exist in the ontology; snapping, if used, must be materialized.

## 4.2 Regions and layers

A composition MUST declare zero or more structural scopes:

* `wd:hasRegion` → `wd:Region`
* `wd:hasLayer` → `wd:Layer`

`wd:Region` and `wd:Layer` are structural primitives used for scoping (principles, grouping, layout management). Ordering rules are expressed through explicit properties (e.g., `wd:zIndex` on elements and explicit layer linkages when defined).

---

# 5. Principle specializations

## 5.1 Figure–Ground statement

`wd:FigureGroundStatement` is a specialization of `wd:PrincipleStatement`.

It MUST satisfy all `wd:PrincipleStatement` requirements, plus:

* `wd:principleType` MUST be `wd:FigureGround`
* one or more `wd:foreground` → `wd:ElementInstance`
* one or more `wd:background` → (`wd:ElementInstance` or `wd:Region`)

A Figure–Ground statement’s `foreground` elements are required to also be `participant` elements (enforced normatively in the canonical rules and in SHACL constraints).

Background values are restricted to:

* a `wd:Region` owned by the same composition
* an `wd:ElementInstance` owned by the same composition

---

# 6. Closure and sealing

The ontology uses explicit ownership to support closed-world sealing.

## 6.1 Ownership

* `wd:ownedBy` links a structural node to exactly one `wd:Composition`
* `wd:owns` is a forward link from `wd:Composition` to owned nodes and MUST be used with explicit triples when present

All structural nodes that participate in the canonical composition graph MUST declare `wd:ownedBy` explicitly.

## 6.2 Same-owner sealing

A canonical composition graph MUST have no cross-composition structural references.

In other words:

* any structural node referenced by `wd:Composition` content MUST be owned by that same `wd:Composition`.

This sealing is enforced by:

* explicit ownership constraints (SHACL)
* composition seal constraints (SHACL-SPARQL)
* the canonical construction rules (normative prose)

---

# 7. Normativity and enforcement layers

This specification is enforced by a combination of:

1. **RDF vocabulary** (`wd-core.ttl`) — defines classes and properties
2. **SHACL constraints** — validate well-formedness, ownership rules, and reachability closure
3. **Canonical composition construction rules** — define the normative meaning of “canonical” and prohibit implicit semantics

Normative clauses are split across two enforcement layers:

- SHACL-enforceable graph constraints (bundle: `wd-all.shacl.ttl`)
- deterministic procedural constraints (canonical serialization, hashing, and validation orchestration)

A normative clause without an assigned enforcement mechanism in `CANONICAL_RULE_TRACEABILITY.md` is non-conformant.

Validation MUST load the full SHACL bundle entrypoint:

- `wd-all.shacl.ttl` (component files and loading contract are defined in `VALIDATION_BUNDLE.md`)

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

- `wd:` -> `https://paperhat.dev/ns/wd#`
- `wdm:` -> `https://paperhat.dev/ns/wdm#`

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

Workshop-level (Codex authoring) specifications for context/objective profiling and adaptive intent binding are defined in:

- `../../workshop/design/RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md`
- `../../workshop/design/DESIGN_POLICY_PRECEDENTS_1_0_0.md`
- `../../workshop/design/COMPILER_MAPPING_SPEC_1_0_0.md`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/design-intent/adaptive-context-profile/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/design-intent/adaptive-objective-profile/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/design-policy/adaptive-optimization-profile/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/design-policy/adaptive-override-set/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/design-intent/adaptive-intent/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/assembly/stage-a-result/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/assembly/stage-b-result/schema.cdx`
- `../../workshop/design/codex-packages/spec/1.0.0/schemas/assembly/adaptive-plan-result/schema.cdx`
