# Canonical Composition Construction Rules

This document normatively defines how a **canonical** `wd:Composition` graph is constructed, normalized, and sealed for deterministic closed-world validation and downstream projection.

These rules apply to the **canonical RDF graph** for the Workshop design ontology.

---

## 1. Definitions

### 1.1 Canonical Composition Graph

A **Canonical Composition Graph** is the RDF subgraph that contains:

* one `wd:Composition` node `C`
* every node **owned by** `C` via `wd:ownedBy`
* every structural edge required by this specification
* no extraneous owned nodes
* no cross-composition references

### 1.2 Structural Nodes

**Structural nodes** are nodes of the following classes:

* `wd:Canvas`, `wd:ElementInstance`, `wd:GroupInstance`
* `wd:Rect`, `wd:Transform`
* `wd:Style`, `wd:Paint`, `wd:Stroke`, `wd:TypographicStyle`
* `wd:GridSystem`, `wd:GridUnit`, `wd:BaselineGrid`
* `wd:PrincipleStatement` (including subclasses)
* `wd:Region`, `wd:Layer`

### 1.3 Ownership

A node `N` is **owned by** `C` iff:

* `N wd:ownedBy C` is present.

Ownership is **exclusive**.

---

## 2. Ownership and Sealing Invariants

### 2.1 Exclusive Ownership

Every Structural Node MUST have exactly one owner:

* For any Structural Node `N`, there MUST exist exactly one triple:

  * `N wd:ownedBy C`

### 2.2 No External Owned Nodes

If a node `N` has `wd:ownedBy C`, then `N` MUST be a Structural Node.

### 2.3 No Cross-Composition References

A Structural Node owned by `C` MUST NOT reference any Structural Node owned by a different `wd:Composition`.

This applies to all properties that link Structural Nodes, including:

* `wd:hasCanvas`, `wd:hasElement`, `wd:frame`, `wd:style`, `wd:transform`
* `wd:fill`, `wd:stroke`, `wd:typeStyle`
* `wd:hasGrid`, `wd:hasUnit`, `wd:baselineGrid`
* `wd:participant`, `wd:foreground`, `wd:background` (when background is an `ElementInstance` or `Region`)
* `wd:hasRegion`, `wd:hasLayer`, `wd:layer`, `wd:group`, `wd:member`
* `wd:expresses`

### 2.4 Reverse Reachability Closure

Every Structural Node owned by `C` MUST be reachable from `C` through at least one allowed structural path:

* `wd:Canvas`: `C wd:hasCanvas Canvas`
* `wd:ElementInstance`: `C wd:hasElement E` or `C wd:hasElement Root ; Root wd:group G ; G wd:member E`
* `wd:Rect`: `E wd:frame R` where `E` is an owned `wd:ElementInstance`
* `wd:Style`: `E wd:style S` where `E` is an owned `wd:ElementInstance`
* `wd:Paint`: `S wd:fill P` where `S` is an owned `wd:Style`
* `wd:Stroke`: `S wd:stroke K` where `S` is an owned `wd:Style`
* `wd:TypographicStyle`: `S wd:typeStyle TS` where `S` is an owned `wd:Style`
* `wd:Transform`: `E wd:transform T` where `E` is an owned `wd:ElementInstance`
* `wd:GroupInstance`: `E wd:group G` where `E` is an owned `wd:ElementInstance`
* `wd:GridSystem`: `C wd:hasGrid G`
* `wd:GridUnit`: `C wd:hasGrid G ; G wd:hasUnit U`
* `wd:BaselineGrid`: `C wd:hasGrid G ; G wd:baselineGrid B`
* `wd:PrincipleStatement`: `C wd:expresses P`
* `wd:Region`: `C wd:hasRegion R` or `C wd:expresses FG ; FG wd:background R` where `FG` is a `wd:FigureGroundStatement`
* `wd:Layer`: `C wd:hasLayer L` or `E wd:layer L` where `E` is an owned `wd:ElementInstance`

---

## 3. Required Construction Rules

Construction rules define which triples MUST exist for a graph to be considered canonical.

### 3.1 Composition Minimum

A canonical composition MUST contain:

* exactly one `wd:hasCanvas` triple
* at least one `wd:hasElement` triple
* exactly one `wd:intent` triple

and ownership:

* `Canvas wd:ownedBy C`

### 3.2 Element Instance Minimum

For each `wd:ElementInstance` `E` owned by `C`, the graph MUST contain:

* `E wd:instanceOf T` exactly once
* `E wd:frame R` exactly once
* `E wd:style S` exactly once
* `E wd:semanticRole Role` exactly once
* `E wd:zIndex Z` exactly once

and ownership:

* `E wd:ownedBy C`
* `R wd:ownedBy C`
* `S wd:ownedBy C`

If `E wd:transform T` is present:

* `T wd:ownedBy C`

### 3.3 Rect Minimum

For each `wd:Rect` `R` owned by `C`, the graph MUST contain exactly once each:

* `R wd:x _`
* `R wd:y _`
* `R wd:w _` where `w > 0`
* `R wd:h _` where `h > 0`

### 3.4 Style Minimum

For each `wd:Style` `S` owned by `C`, the graph MUST contain exactly once:

* `S wd:opacity O` where `0 ≤ O ≤ 1`

Fill and stroke are optional but constrained:

* `S wd:fill P` at most once
* `S wd:stroke K` at most once

If `S wd:fill P` is present:

* `P wd:ownedBy C`
* `P` MUST have exactly one `wd:paintKind` and one `wd:paintValue`

If `S wd:stroke K` is present:

* `K wd:ownedBy C`
* `K` MUST have exactly one `wd:strokeWidth` where `strokeWidth ≥ 0`

If `S wd:typeStyle TS` is present:

* `TS wd:ownedBy C`
* `TS` MUST satisfy Typography Minimum (3.5)

### 3.5 Typography Minimum

For each `wd:TypographicStyle` `TS` owned by `C`, the graph MUST contain exactly once each:

* `TS wd:typeface TF`
* `TS wd:fontSize _` where `fontSize > 0`
* `TS wd:fontWeight _` where `fontWeight ≥ 1`
* `TS wd:leading _` where `leading > 0`

`wd:tracking` is optional (at most once).

### 3.6 Grid Minimum

If `C wd:hasGrid G` is present:

* `G wd:ownedBy C`
* `G wd:columnCount n` exactly once where `n ≥ 1`
* `G wd:rowCount m` exactly once where `m ≥ 1`

Grid units:

* zero or more `G wd:hasUnit U` triples are permitted.
* If `G wd:hasUnit U` appears then:

  * `U wd:ownedBy C`
  * `U` MUST be exactly one of: `wd:ColumnUnit`, `wd:RowUnit`, `wd:GutterUnit`

Baseline grid:

* `G wd:baselineGrid B` at most once
* If present:

  * `B wd:ownedBy C`
  * `B wd:baselineStep s` exactly once where `s > 0`

### 3.7 Principle Statement Minimum

For each `wd:PrincipleStatement` `P` owned by `C`, the graph MUST contain:

* `P wd:principleType PT` exactly once
* `P wd:scope Scope` exactly once
* `P wd:participant E` one or more times
* `P wd:ownedBy C`

Every participant `E` MUST be:

* a `wd:ElementInstance`
* owned by `C`

Every owned `wd:PrincipleStatement` MUST be linked from the composition:

* `C wd:expresses P`

### 3.8 Figure–Ground Specialization

For each `wd:FigureGroundStatement` `FG` owned by `C`:

* `FG wd:principleType wd:FigureGround` MUST hold
* `FG wd:foreground E` one or more times
* `FG wd:background X` one or more times

Each `foreground` element MUST be a participant:

* if `FG wd:foreground E` then `FG wd:participant E`

Each `background` value MUST be either:

* an `wd:ElementInstance` owned by `C`, or
* a `wd:Region` owned by `C`

---

## 4. Canonical Normalization Rules

Normalization rules specify when multiple equivalent authoring states are disallowed.

### 4.1 Explicit Ownership Materialization

Ownership MUST be explicit.

Implementations MUST NOT infer ownership via reachability.
If a node is part of the composition structure, it MUST declare `wd:ownedBy C`.

### 4.2 No Implicit Cascading Semantics

No semantic interpretation is permitted that depends on:

* inherited style
* implicit group defaults
* implicit z-order
* implicit grid snapping

Any such information, if used, MUST be materialized into explicit triples on the owning nodes.

### 4.3 Deterministic Defaults

If an implementation provides defaults (e.g., missing `wd:strokeWidth`), defaults MUST be applied by deterministic rule and MUST be materialized into the canonical graph before hashing or validation.

---

## 5. Canonical Serialization and Hashing

### 5.1 Canonical Graph Preconditions

Before canonical serialization:

1. All IRIs and string literals MUST be normalized to Unicode NFC.
2. Blank nodes MUST NOT appear in the canonical composition graph.
3. Every triple in the canonical composition graph MUST satisfy §2–§4.

### 5.2 Canonical Serialization Algorithm

The canonical composition graph MUST be serialized as RDF 1.1 N-Triples with these deterministic rules:

1. Each triple is serialized as exactly one N-Triples line terminated by `\n` (U+000A).
2. No comments and no blank lines are permitted.
3. Literal lexical forms MUST use canonical lexical representation for their datatype.
4. Triple ordering MUST be:
   - primary key: subject IRI (Unicode scalar value order)
   - secondary key: predicate IRI (Unicode scalar value order)
   - tertiary key: object with type precedence:
     - IRI objects sort before literal objects
     - IRI object key: IRI (Unicode scalar value order)
     - literal object key: lexical form, then datatype IRI, then language tag (all Unicode scalar value order; empty language tag sorts first)
5. The sorted N-Triples stream MUST be UTF-8 encoded. The resulting byte sequence is the canonical byte form.

### 5.3 Hashing Algorithm

The canonical hash MUST be computed as:

1. Input bytes: canonical byte form from §5.2.
2. Algorithm: SHA-256.
3. Output format: 64-character lowercase hexadecimal string.

### 5.4 Hash Input Scope

The hash input MUST be exactly the canonical composition graph for the specified `wd:Composition` node and MUST NOT include triples outside that subgraph.

---

## 6. Validation Contract

A `wd:Composition` is **valid** iff:

1. It satisfies all construction rules in §3.
2. It satisfies all ownership and sealing invariants in §2.
3. It satisfies all normalization rules in §4.
4. It satisfies the full SHACL validation bundle (`wd-all.shacl.ttl`).

If any rule fails, the composition MUST be rejected as invalid.
