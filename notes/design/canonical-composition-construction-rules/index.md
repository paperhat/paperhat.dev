# Canonical Composition Construction Rules

This document normatively defines how a **canonical** `gd:Composition` graph is constructed, normalized, and sealed for deterministic closed-world validation and downstream projection.

These rules apply to the **canonical RDF graph** for the graphic design ontology.

---

## 1. Definitions

### 1.1 Canonical Composition Graph

A **Canonical Composition Graph** is the RDF subgraph that contains:

* one `gd:Composition` node `C`
* every node **owned by** `C` via `gd:ownedBy`
* every structural edge required by this specification
* no extraneous owned nodes
* no cross-composition references

### 1.2 Structural Nodes

**Structural nodes** are nodes of the following classes:

* `gd:Canvas`, `gd:ElementInstance`, `gd:GroupInstance`
* `gd:Rect`, `gd:Transform`
* `gd:Style`, `gd:Paint`, `gd:Stroke`, `gd:TypographicStyle`
* `gd:GridSystem`, `gd:GridUnit`, `gd:BaselineGrid`
* `gd:PrincipleStatement` (including subclasses)
* `gd:Region`, `gd:Layer`

### 1.3 Ownership

A node `N` is **owned by** `C` iff:

* `N gd:ownedBy C` is present.

Ownership is **exclusive**.

---

## 2. Ownership and Sealing Invariants

### 2.1 Exclusive Ownership

Every Structural Node MUST have exactly one owner:

* For any Structural Node `N`, there MUST exist exactly one triple:

  * `N gd:ownedBy C`

### 2.2 No External Owned Nodes

If a node `N` has `gd:ownedBy C`, then `N` MUST be a Structural Node.

### 2.3 No Cross-Composition References

A Structural Node owned by `C` MUST NOT reference any Structural Node owned by a different `gd:Composition`.

This applies to all properties that link Structural Nodes, including:

* `gd:hasCanvas`, `gd:hasElement`, `gd:frame`, `gd:style`, `gd:transform`
* `gd:fill`, `gd:stroke`, `gd:typeStyle`
* `gd:hasGrid`, `gd:hasUnit`, `gd:baselineGrid`
* `gd:participant`, `gd:foreground`, `gd:background` (when background is an `ElementInstance` or `Region`)
* `gd:hasRegion`, `gd:hasLayer`, `gd:layer`, `gd:group`, `gd:member`
* `gd:expresses`

### 2.4 Reverse Reachability Closure

Every Structural Node owned by `C` MUST be reachable from `C` through at least one allowed structural path:

* `gd:Canvas`: `C gd:hasCanvas Canvas`
* `gd:ElementInstance`: `C gd:hasElement E` or `C gd:hasElement Root ; Root gd:group G ; G gd:member E`
* `gd:Rect`: `E gd:frame R` where `E` is an owned `gd:ElementInstance`
* `gd:Style`: `E gd:style S` where `E` is an owned `gd:ElementInstance`
* `gd:Paint`: `S gd:fill P` where `S` is an owned `gd:Style`
* `gd:Stroke`: `S gd:stroke K` where `S` is an owned `gd:Style`
* `gd:TypographicStyle`: `S gd:typeStyle TS` where `S` is an owned `gd:Style`
* `gd:Transform`: `E gd:transform T` where `E` is an owned `gd:ElementInstance`
* `gd:GroupInstance`: `E gd:group G` where `E` is an owned `gd:ElementInstance`
* `gd:GridSystem`: `C gd:hasGrid G`
* `gd:GridUnit`: `C gd:hasGrid G ; G gd:hasUnit U`
* `gd:BaselineGrid`: `C gd:hasGrid G ; G gd:baselineGrid B`
* `gd:PrincipleStatement`: `C gd:expresses P`
* `gd:Region`: `C gd:hasRegion R` or `C gd:expresses FG ; FG gd:background R` where `FG` is a `gd:FigureGroundStatement`
* `gd:Layer`: `C gd:hasLayer L` or `E gd:layer L` where `E` is an owned `gd:ElementInstance`

---

## 3. Required Construction Rules

Construction rules define which triples MUST exist for a graph to be considered canonical.

### 3.1 Composition Minimum

A canonical composition MUST contain:

* exactly one `gd:hasCanvas` triple
* at least one `gd:hasElement` triple
* exactly one `gd:intent` triple

and ownership:

* `Canvas gd:ownedBy C`

### 3.2 Element Instance Minimum

For each `gd:ElementInstance` `E` owned by `C`, the graph MUST contain:

* `E gd:instanceOf T` exactly once
* `E gd:frame R` exactly once
* `E gd:style S` exactly once
* `E gd:semanticRole Role` exactly once
* `E gd:zIndex Z` exactly once

and ownership:

* `E gd:ownedBy C`
* `R gd:ownedBy C`
* `S gd:ownedBy C`

If `E gd:transform T` is present:

* `T gd:ownedBy C`

### 3.3 Rect Minimum

For each `gd:Rect` `R` owned by `C`, the graph MUST contain exactly once each:

* `R gd:x _`
* `R gd:y _`
* `R gd:w _` where `w > 0`
* `R gd:h _` where `h > 0`

### 3.4 Style Minimum

For each `gd:Style` `S` owned by `C`, the graph MUST contain exactly once:

* `S gd:opacity O` where `0 ≤ O ≤ 1`

Fill and stroke are optional but constrained:

* `S gd:fill P` at most once
* `S gd:stroke K` at most once

If `S gd:fill P` is present:

* `P gd:ownedBy C`
* `P` MUST have exactly one `gd:paintKind` and one `gd:paintValue`

If `S gd:stroke K` is present:

* `K gd:ownedBy C`
* `K` MUST have exactly one `gd:strokeWidth` where `strokeWidth ≥ 0`

If `S gd:typeStyle TS` is present:

* `TS gd:ownedBy C`
* `TS` MUST satisfy Typography Minimum (3.5)

### 3.5 Typography Minimum

For each `gd:TypographicStyle` `TS` owned by `C`, the graph MUST contain exactly once each:

* `TS gd:typeface TF`
* `TS gd:fontSize _` where `fontSize > 0`
* `TS gd:fontWeight _` where `fontWeight ≥ 1`
* `TS gd:leading _` where `leading > 0`

`gd:tracking` is optional (at most once).

### 3.6 Grid Minimum

If `C gd:hasGrid G` is present:

* `G gd:ownedBy C`
* `G gd:columnCount n` exactly once where `n ≥ 1`
* `G gd:rowCount m` exactly once where `m ≥ 1`

Grid units:

* zero or more `G gd:hasUnit U` triples are permitted.
* If `G gd:hasUnit U` appears then:

  * `U gd:ownedBy C`
  * `U` MUST be exactly one of: `gd:ColumnUnit`, `gd:RowUnit`, `gd:GutterUnit`

Baseline grid:

* `G gd:baselineGrid B` at most once
* If present:

  * `B gd:ownedBy C`
  * `B gd:baselineStep s` exactly once where `s > 0`

### 3.7 Principle Statement Minimum

For each `gd:PrincipleStatement` `P` owned by `C`, the graph MUST contain:

* `P gd:principleType PT` exactly once
* `P gd:scope Scope` exactly once
* `P gd:participant E` one or more times
* `P gd:ownedBy C`

Every participant `E` MUST be:

* a `gd:ElementInstance`
* owned by `C`

Every owned `gd:PrincipleStatement` MUST be linked from the composition:

* `C gd:expresses P`

### 3.8 Figure–Ground Specialization

For each `gd:FigureGroundStatement` `FG` owned by `C`:

* `FG gd:principleType gd:FigureGround` MUST hold
* `FG gd:foreground E` one or more times
* `FG gd:background X` one or more times

Each `foreground` element MUST be a participant:

* if `FG gd:foreground E` then `FG gd:participant E`

Each `background` value MUST be either:

* an `gd:ElementInstance` owned by `C`, or
* a `gd:Region` owned by `C`

---

## 4. Canonical Normalization Rules

Normalization rules specify when multiple equivalent authoring states are disallowed.

### 4.1 Explicit Ownership Materialization

Ownership MUST be explicit.

Implementations MUST NOT infer ownership via reachability.
If a node is part of the composition structure, it MUST declare `gd:ownedBy C`.

### 4.2 No Implicit Cascading Semantics

No semantic interpretation is permitted that depends on:

* inherited style
* implicit group defaults
* implicit z-order
* implicit grid snapping

Any such information, if used, MUST be materialized into explicit triples on the owning nodes.

### 4.3 Deterministic Defaults

If an implementation provides defaults (e.g., missing `gd:strokeWidth`), defaults MUST be applied by deterministic rule and MUST be materialized into the canonical graph before hashing or validation.

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

The hash input MUST be exactly the canonical composition graph for the specified `gd:Composition` node and MUST NOT include triples outside that subgraph.

---

## 6. Validation Contract

A `gd:Composition` is **valid** iff:

1. It satisfies all construction rules in §3.
2. It satisfies all ownership and sealing invariants in §2.
3. It satisfies all normalization rules in §4.
4. It satisfies the full SHACL validation bundle (`gd-all.shacl.ttl`).

If any rule fails, the composition MUST be rejected as invalid.
