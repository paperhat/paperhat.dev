# A discussion about a cognitive engineering approach to the Workshop UIs

> I am building a rust/cargo codex processor/pipeline with a tauri interface. It will use the Monaco editor and will provide ways to visualise the AST, IR, and triples graph output. I want to discuss how I can apply cognitive engineering principles to it, and any similar approaches to human-centered and semantic design. Thoughts?

Good. This is exactly the kind of system where cognitive engineering actually matters.

You are building a **semantic compiler with a GUI**, not a text editor. That changes everything.

I’ll structure this around:

1. Cognitive engineering principles
2. How they apply specifically to Codex
3. Concrete UI strategies for AST / IR / triples visualization
4. Related human-centered frameworks worth stealing from

---

# 1. Core Cognitive Engineering Principles

## A. Cognitive Load Theory (Sweller)

Three loads:

* **Intrinsic** – inherent complexity of RDF + schema + compilation
* **Extraneous** – UI friction, unclear visualization, noise
* **Germane** – schema understanding, semantic mental models

Your job:

* Reduce extraneous load
* Control intrinsic load
* Increase germane load

For Codex, intrinsic load is non-trivial. So UI discipline is mandatory.

---

## B. External Cognition (Scaife & Rogers)

Good tools:

* Reduce internal memory demand
* Make invisible structure visible
* Offload working memory into spatial layout

AST / IR / triples are *perfect* candidates for external cognition.

---

## C. Progressive Disclosure

Never show full semantic depth by default.

Instead:

* Start with minimal semantic view
* Expand on demand
* Reveal causality when asked

Think “semantic microscope,” not “semantic dump.”

---

## D. Reorientation Penalty (context switching)

You mentioned this before in relation to programming trance.

Your UI must:

* Avoid modal jumps
* Avoid full-screen switches
* Avoid losing cursor context

The editor is the anchor. Everything else orbits it.

---

## E. Representational Alignment

Different representations must:

* Map deterministically
* Maintain identity anchors
* Preserve referential continuity

If a node in the AST corresponds to IR node X and triple Y, the user must *see that continuity*.

No ambiguity.

---

# 2. What Makes Codex Special

Codex is:

* Deterministic
* Schema-first
* Closed-world
* Canonical RDF authority

That gives you huge advantages:

### You can show causality

Example:
User writes block → AST node → IR entity → canonical triples.

This is a pipeline.
You can visualize it as a pipeline.
That’s cognitively powerful.

---

# 3. Concrete UI Strategies

## 3.1 Monaco as Cognitive Anchor

Editor is primary.

Everything else should:

* Highlight corresponding source span
* Never steal focus permanently
* Never obscure primary mental thread

Use:

* Inline semantic lenses
* Hover overlays
* Click-to-expand side panels

Not:

* Separate tool windows
* Full-screen graph dumps

---

# 3.2 AST Visualization

AST is structural, not semantic.

Use:

* Collapsible tree
* Stable node IDs
* Highlight on hover ↔ editor sync

Important:
AST should be boring.
If it’s visually exciting, that’s wrong.

It is a syntax tree, not insight.

---

## 3.3 IR Visualization (This Is Gold)

IR is where semantic meaning crystallizes.

Show:

* EntityTable
* TraitMap
* Identity resolution
* Deterministic expansions

Crucial feature:
**“Why does this exist?” button**

Click IR node → show:

* Source span
* Governing schema rule
* Deterministic transformation step

This increases germane load while reducing confusion.

---

## 3.4 Triple Graph Visualization

Danger zone.

Raw RDF graphs are cognitively hostile.

You must:

* Cluster by subject
* Collapse predicates by default
* Show shapes / constraints visually
* Avoid hairball graphs

Instead of force-directed chaos:
Use structured layout.

Think:

Left: Subjects
Middle: Predicates
Right: Objects

Or:

Schema shape overlay mode.

Make it structural, not decorative.

---

## 3.5 Error Visualization

This is where cognitive engineering shines.

Instead of:

“SHACL violation: property missing”

Do:

* Inline highlight
* Schema rule excerpt
* Deterministic explanation
* Suggested correction (if allowed)

Errors should feel mechanical, not mysterious.

---

# 4. Human-Centered / Related Frameworks

## A. Norman – Gulf of Execution / Evaluation

User intent:
“I want to define a Recipe.”

System must:

* Make schema affordances visible
* Show what is possible next
* Reduce gulf between schema and expression

You can add:

* Schema introspection sidebar
* “What can go here?” context action

---

## B. Donella Meadows – Systems Thinking

Your pipeline is a system.

Show:

Codex → AST → IR → RDF → Projection

Make it visually linear.
Systems clarity reduces anxiety.

---

## C. Information Foraging Theory

Developers scan for:

* Errors
* Identity anchors
* Structural mismatches

So:

* Use visual salience sparingly
* Don’t overload color
* Reserve strong contrast for violations

---

## D. Semiotics (Very Relevant to You)

You are building a sign system about sign systems.

Maintain:

* Clear type distinctions
* Stable visual grammar
* Consistent iconography

If IR entities and schema shapes look identical, you’ve failed.

---

# 5. Advanced Idea: Cognitive Modes

You could design three modes:

1. Author Mode – minimal noise
2. Structure Mode – AST / outline focus
3. Semantic Mode – IR + triples + schema overlay

Switching modes changes cognitive posture without overwhelming.

This is similar to:

* TeX paragraph-level layout thinking
* IDE debug vs edit mode

---

# 6. The Biggest Mistake to Avoid

Do not treat visualization as a developer toy.

This tool is:

A semantic instrument panel.

It should answer:

* What did I write?
* What does it mean?
* Why does it mean that?
* Where did this triple come from?
* Which schema rule created this?

If you solve those cleanly,
you’ve reduced cognitive footprint massively.

---

# 7. If You Want to Go Deeper

We could:

* Design a formal cognitive architecture for Workshop
* Define “cognitive invariants” parallel to semantic invariants
* Specify visualization rules deterministically like you do schemas

That would be very on-brand for you.

> I am interested in the formal cognitive architecture for Workshop.

Here’s a workable **formal cognitive architecture** for Workshop that fits your existing ethos: **schema-governed, deterministic, closed-world, no vibes**.

## 1) Objective

Define a **normative, testable cognitive layer** that governs how Workshop *presents* the canonical universe (Codex → AST → IR → RDF) to a human, with the explicit goal of minimizing **cognitive footprint** while preserving **traceability** and **semantic certainty**.

This is not “UX guidance.” It’s a **specifiable system**.

## 2) Core Idea

Treat the UI as a **projection system** from the canonical semantic universe to a **Cognitive Projection Graph (CPG)**:

* Inputs: canonical RDF + schema + compilation trace (AST↔IR↔RDF mapping)
* Output: a set of **cognitive artifacts** (panels, views, overlays, summaries, cues)
* Guarantee: deterministic, reproducible, testable

So the cognitive layer is to humans what your render/foundry layer is to targets.

## 3) Objects in the Cognitive Architecture

### 3.1 Cognitive State Model (CSM)

A small, explicit, model of the user’s current cognitive situation:

* `FocusSpan`: the active source range (Monaco selection/cursor)
* `FocusNode`: current AST/IR/RDF node(s) in focus
* `TaskIntent`: author / debug / explore / refactor
* `DepthLevel`: disclosure depth (0..N)
* `WorkingSet`: bounded set of currently relevant entities (IDs)
* `RecentTrail`: last K focus transitions (for reorientation control)

Normative constraint: **state is explicit and serializable** (for repeatability, debugging, and tests).

### 3.2 Cognitive Projection Graph (CPG)

A derived graph whose nodes are **cognitive units** (not semantic units):

* `CPG:Unit` types:

  * `SourceUnit` (span / block / token group)
  * `StructureUnit` (AST region)
  * `MeaningUnit` (IR entity/trait)
  * `EvidenceUnit` (schema rule / validation cause)
  * `ConsequenceUnit` (triple cluster / derived artifact)
  * `IssueUnit` (error/warning)

* `CPG:Edge` types:

  * `correspondsTo` (identity continuity)
  * `explains` (why)
  * `causes` (derivation chain)
  * `violates` (constraint failure)
  * `summarizes` (folding / abstraction)

Normative constraint: CPG must be **deterministically derivable** from canonical inputs + user cognitive state.

### 3.3 Cognitive Operators (CO)

Small set of actions the UI can perform, defined formally:

* `Focus(x)` — set focus to node/unit x
* `Reveal(x, depth)` — increase disclosure depth for x
* `Fold(x)` — collapse x into summary unit
* `Trace(x, targetLayer)` — show mapping: source→AST→IR→RDF or inverse
* `Explain(x)` — show governing schema rule(s) + transformation steps
* `Compare(x, y)` — diff between two versions / two nodes
* `Filter(predicate)` — constrain working set
* `Pin(x)` — keep unit visible across focus changes

Key: operators have **preconditions, postconditions, and invariants**.

## 4) Cognitive Invariants (Normative)

These are the “semantic invariants” analog for cognition. They should be spec-level.

### I1. Identity Continuity

For any focused semantic entity, the UI MUST provide a stable mapping across layers:
`SourceSpan ↔ AST node ↔ IR node ↔ Triple cluster`.

No “similar,” no heuristics.

### I2. Reorientation Bound

Any state transition must preserve at least one of:

* focus anchor (cursor/span)
* pinned units
* trail breadcrumb

This bounds reorientation penalty.

### I3. Progressive Disclosure

Default views MUST show only DepthLevel 0.
Higher depths are explicit user actions.
No surprise explosions.

### I4. Causal Explainability

Every displayed error/derived triple MUST be explainable via:

* governing schema rule
* transformation step(s)
* source evidence

### I5. Bounded Working Set

At any moment, the UI MUST maintain a bounded set of “active” units (the rest are summarized/folded). The bound is a policy parameter.

### I6. Layer Honesty

AST view shows structure only.
IR view shows semantics only.
RDF view shows canonical consequences only.
No mixing unless explicitly in Trace/Explain mode.

## 5) Cognitive Policies (Configurable, Still Deterministic)

Policies are like “design rules,” but formal:

* `MaxWorkingSetSize`
* `DefaultDepthLevel`
* `AutoFoldThreshold` (e.g., triple clusters > N fold)
* `HighlightBudget` (max simultaneous emphasis marks)
* `TrailLength`

Policies can be expressed as a small schema-governed config (and tested).

## 6) The Three Canonical Cognitive Views

Define three primary projections (each is a deterministic projection from CPG):

1. **Authoring View**

   * Monaco primary
   * minimal overlays
   * only local structure + local issues

2. **Trace View**

   * synchronized cross-layer mapping
   * “what does this become?”
   * bidirectional trace

3. **Explanation View**

   * schema rule(s) + evidence + consequence
   * “why is this true/invalid?”

Everything else is derived compositionally.

## 7) Conformance Tests for the Cognitive Layer

You can test cognition like you test semantics:

* Given input doc + schema:

  * focus span S
  * operator sequence O1..Ok
* Assert:

  * which units appear
  * what edges exist
  * what is folded/revealed
  * that invariants hold

This means the cognitive architecture is **not subjective**.
It becomes *part of Workshop’s determinism story*.

## 8) Practical Next Step

If you want to make this real, the minimal spec you need is:

1. A formal definition of **Compilation Trace** (span↔AST↔IR↔RDF identity links)
2. A small schema for **Cognitive State Model**
3. A deterministic mapping function: `(CanonicalRDF, Schema, Trace, CSM) -> CPG`
4. Rules for **three canonical views** as projections of CPG

> How do we prevent graph-view cognitive collapse?

Good.
This is the right question.

**Graph-view cognitive collapse** happens when the representation exceeds working memory capacity and loses structural intelligibility. RDF hairballs are a classic failure case.

You prevent collapse the same way you prevent semantic ambiguity in Codex:

* Constrain it.
* Define invariants.
* Make collapse impossible by specification.

Below is a **formal anti-collapse strategy** tailored to Workshop.

---

# 1. Define What “Collapse” Means (Formally)

Graph-view collapse occurs when any of the following thresholds are violated:

1. **Node Overload** – Too many visible units (> working memory capacity).
2. **Edge Density Saturation** – Cross-links obscure topology.
3. **Loss of Hierarchy** – No perceivable structural layering.
4. **Identity Drift** – User cannot track which node corresponds to source focus.
5. **Causal Opacity** – Cannot see why an edge exists.

So collapse is not “looks messy.”
It is **violation of cognitive invariants**.

---

# 2. Core Anti-Collapse Invariants

## I1 — Bounded Visible Node Count

At any time:

```
|VisibleUnits| ≤ MaxWorkingSetSize
```

This is non-negotiable.

Everything else must be folded or summarized.

---

## I2 — Single Anchor Guarantee

There must always be:

* One primary focus node
* With visual dominance
* With identity continuity across layers

No multi-anchor chaos.

---

## I3 — No Free-Form Layout

Force-directed layouts are illegal by default.

They are:

* Non-deterministic
* Spatially unstable
* Visually chaotic

Layout must be:

* Layered (Source → IR → RDF)
* Or subject-clustered
* Or schema-shaped

Structured, not decorative.

---

# 3. Structural Solutions

## 3.1 Replace Graph with Structured Graph

Do not show a raw triple network.

Instead:

### Subject-Centric Column Layout

```
[Subject]
    ├── predicate → object
    ├── predicate → object
```

Objects that are IR entities become expandable nodes.

This preserves:

* Tree-like mental parsing
* Reduced cross-link noise
* Visual grammar consistency

---

## 3.2 Triple Clustering

Instead of:

```
50 triples visible
```

Show:

```
Entity: Recipe#42
  17 properties (collapsed)
```

Expand only when user requests.

Clustering rule:

* Cluster by subject
* Cluster by predicate family
* Cluster by schema shape

---

## 3.3 Layer Separation

Never intermix:

* AST nodes
* IR entities
* RDF triples

Unless explicitly in Trace mode.

Default:
Single layer at a time.

Layer mixing causes collapse.

---

# 4. Cognitive Throttling

Introduce formal throttling policies.

### 4.1 Edge Visibility Budget

Only show:

* Edges touching focused unit
* Edges within N-hop radius

Everything else summarized.

### 4.2 Progressive Radius Expansion

User action required to expand:

* 1-hop → 2-hop → 3-hop

Never auto-expand full graph.

---

# 5. Causal Mode Instead of Topology Mode

Most users do not want topology.

They want:

* “Why is this triple here?”
* “Where did this come from?”

So default graph mode should be:

**Causal Trace Mode**, not Network Mode.

Example:

```
Triple:
  ex:recipe42 ex:hasIngredient ex:flour

Derived from:
  Schema rule: IngredientPropertyShape
  Source span: line 12–18
```

Linear causality > spatial topology.

---

# 6. Semantic Compression

Define **Cognitive Compression Rules**:

If N triples share:

* Same subject
* Same predicate
* Same shape

Compress into:

```
hasIngredient → 5 values
```

Expansion reveals items.

Compression reduces extraneous load without losing truth.

---

# 7. Visual Grammar Discipline

You must maintain:

* Stable icon for IR entity
* Stable icon for schema rule
* Stable icon for literal
* Stable edge style per relation type

Never improvise visuals.

Graph collapse often happens because visual grammar collapses.

---

# 8. Deterministic Layout Algorithm

Layout must be:

* Stable across renders
* Determined by canonical identity (e.g., sorted by IRI)

If layout moves every time, cognitive map resets → collapse.

---

# 9. Hard Rule: No Hairball Mode

If:

```
VisibleNodes > Threshold
```

Switch to:

* Summary View
* Or Subject Filter View

Never allow visual explosion.

Better to refuse than to overwhelm.

---

# 10. Advanced Strategy: Schema-Projected Graphs

Instead of graph-of-triples:

Project graph onto schema shape.

Example:

```
Recipe
 ├── title
 ├── difficulty
 ├── ingredient*
 └── instruction*
```

Populate slots with values.

This is:

* Structurally constrained
* Familiar
* Cognitively bounded

Schema projection is safer than network projection.

---

# 11. The Real Insight

Raw RDF topology is rarely cognitively useful.

Workshop is schema-first.

So show:

Schema-governed structure first.
Network topology only when explicitly requested.

---

# 12. If You Want to Formalize This

You could define:

### Anti-Collapse Policy Schema

```
MaxWorkingSetSize: 25
MaxVisibleEdges: 40
DefaultHopRadius: 1
AutoFoldThreshold: 5
LayoutMode: subject-column | schema-projection
```

And make graph-view conformance testable.

---

# 13. The Principle

Graph-view collapse is not a rendering problem.

It is a violation of:

* Working memory limits
* Identity continuity
* Progressive disclosure
* Causal traceability

Design so collapse is structurally impossible.

---

If you'd like, next we can:

* Design a concrete triple view for Recipe schema
* Or define a deterministic layout algorithm
* Or define a “Trace-first” visualization spec

> Define a deterministic layout algorithm.

Here’s a **deterministic layout algorithm** you can spec and implement (Rust) that avoids hairballs by construction. It’s not “graph drawing” in the force-directed sense; it’s a **canonical, schema-governed structured layout** with stable coordinates.

I’ll define one primary algorithm (recommended) and one optional fallback.

# Deterministic Subject-Column Layout (DSCL)

## Inputs

* Canonical RDF graph `G` (triples)
* Governing schema `S` (SHACL shapes / Codex schema model)
* Focus set `F` (one focused subject IRI, plus optional pinned subjects)
* Policy `P` (bounds + display settings)
* Canonical ordering function `ord(x)` (bytewise order of canonical IRI/blank-id/literal canonical forms)

## Output

A layout `L`:

* For each visible node `n`: `(x, y, w, h)`
* For each visible edge `e`: routed polyline segments (deterministic)

## Core idea

You never place the full RDF network. You lay out **subject panels** in columns, and inside each panel you lay out **predicate rows** and **object items**. Cross-links are shown only for the bounded working set (and routed deterministically).

This prevents cognitive collapse because the topology is expressed as **structured lists**, not a free-form web.

---

## Policy (minimal)

* `MaxSubjects` (e.g. 7)
* `MaxPredicatesPerSubject` (e.g. 12)
* `MaxObjectsPerPredicate` (e.g. 8; remainder collapsed)
* `MaxCrossLinks` (e.g. 25)
* `HopRadius` (default 1)
* `ColumnWidth`, `RowHeight`, `Gutters` (constants; or derived from font metrics)
* `CollapseThreshold` (counts beyond which you summarize)

All policy values are part of determinism: given the same `P`, same output.

---

## Step 0 — Canonical keys

Define canonical string keys:

* `key(iri) = canonical_iri_string(iri)` (normalized form you already use)
* `key(blank) = "_:" + stable_blank_id` (must be stable within canonicalization)
* `key(lit) = canonical_literal_form(lit)` (datatype + lexical normalized as you define)

Then ordering is `ord(a,b) = lex(key(a))`.

---

## Step 1 — Choose the visible working set (deterministic)

### 1.1 Seed subjects

Start with `focusSubject = f0` (exactly one primary anchor). Add pinned subjects in stable order.

`Seeds = [f0] + sort(pinnedSubjects, ord)`

### 1.2 Expand by bounded hop radius

Compute candidate subjects from triples touching the seeds out to `HopRadius`, but **only via subject/object links where object is IRI/blank and passes a schema relevance test**.

Deterministic BFS:

* frontier queue ordered by `ord(subject)`
* when visiting subject `s`, consider outgoing triples `(s,p,o)` sorted by `(ord(p), ord(o))`
* add `o` as a subject candidate if it’s IRI/blank
* stop once `|Subjects| = MaxSubjects`

This yields `VisibleSubjects` in a stable order:

1. `f0`
2. pinned (sorted)
3. BFS-added candidates in discovery order (which is deterministic due to sorted processing)

---

## Step 2 — Lay out subject panels (columns)

Let `k = |VisibleSubjects|`.

Place panels left-to-right:

* `x_i = X0 + i*(ColumnWidth + GutterX)`
* `y_i = Y0`
* `w_i = ColumnWidth`
* `h_i = computed from rows but clamped to viewport; overflow scroll allowed (scroll is deterministic, too: start at top)`

This alone guarantees *spatial stability*: same subject list → same panel positions.

---

## Step 3 — Inside each subject panel: predicate rows

For each subject `s`:

### 3.1 Collect outgoing predicate groups

Group triples by predicate:

`Group[s][p] = [o1, o2, ...]`

Order predicates:

1. If schema `S` provides a preferred property order for the shape governing `s`, use that order (deterministic list).
2. Then append remaining predicates sorted by `ord(p)`.
3. Truncate to `MaxPredicatesPerSubject`; remainder becomes a single collapsed row: “+ N more predicates”.

### 3.2 For each predicate row, order objects

Objects for `(s,p,*)` are sorted by:

1. schema-informed class/type priority (optional but deterministic):

* IRIs/blank that are instances of “primary classes” for the shape first (you can define this explicitly)

2. then `ord(o)`

Truncate to `MaxObjectsPerPredicate`; remainder collapsed: “+ N more values”.

### 3.3 Row geometry

Within the panel:

* Subject header occupies fixed height `HeaderH`
* Each predicate row occupies `RowHeight`
* Objects are laid out as a vertical list inside the row area *or* as chips with deterministic wrap:

  * For chips: order is fixed; wrapping is done by width; ties resolved by the same order, so chip positions are deterministic.

So for predicate row `j`:

* `rowTop = HeaderH + j*RowHeight`
* Predicate label at `(x+PadL, y+rowTop)`
* Object list starts at `(x+PredLabelW, y+rowTop)` with deterministic item offsets

---

## Step 4 — Cross-links (edges between panels)

You only draw cross-links between visible subjects (bounded).

### 4.1 Select candidate cross-links

A cross-link exists if there’s a triple `(s,p,o)` where both `s` and `o` are in `VisibleSubjects` and `o` is IRI/blank.

Candidate edges are sorted by `(ord(s), ord(p), ord(o))`.

Take first `MaxCrossLinks`. Remainder suppressed (but you can show a deterministic counter: “+N hidden links”).

### 4.2 Edge routing (deterministic, non-overlapping bias)

Each cross-link is routed as an orthogonal polyline:

From:

* the anchor point of the object item inside subject panel `s` (you know its y-coordinate)
  To:
* the subject header anchor point of panel `o`

Routing:

* If `panelIndex(o) > panelIndex(s)`: route to the right; else to the left.
* Use a per-edge “track” number to separate overlaps:

  * `track(e) = rank(e)` in the sorted edge list (0..)
  * The bend x-coordinate is `bendX = midX + track(e)*TrackSpacing` (bounded; if exceeds policy, collapse more edges)

This yields stable edges that don’t jump around.

---

## Step 5 — Labels, summarization, and determinism guarantees

Every collapsed group (extra predicates, extra objects, extra edges) is represented by a **summary node** with a canonical label derived from counts and keys (never from incidental ordering).

Example:

* “+ 14 more values” (the 14 is deterministic)
* Optionally, you can include the first hidden item key as a hint, but it must be derived deterministically from sorted hidden items.

---

# Optional: Deterministic Schema-Projection Layout (DSPL)

When schema provides a strong shape for `s`, you can replace the predicate list with a **shape slot layout**:

* Slots are ordered exactly as declared by the schema (plus deterministic append of unknown predicates).
* Each slot is a “field” with values displayed in the same truncation rules.

This is even more cognitively stable because it’s a form-like layout rather than raw predicates.

---

# Complexity

Let `T` be number of triples inspected within hop radius bounds.

* Working set selection: `O(T log T)` due to sorting triples by predicate/object for deterministic traversal (or pre-index + stable iteration).
* Grouping per subject: `O(T)` grouping + `O(P log P)` sorting predicates.
* Layout: linear in visible elements.
* Cross-links: `O(E log E)` for edge sorting (E bounded by inspected triples).

All bounded by policy; UI stays fast.

---

# What you can put in the spec as “hard requirements”

1. Layout must be fully determined by `(G, S, F, P)` and canonical ordering.
2. No physics / force-directed / randomized layout in default mode.
3. Node positions must be stable under:

   * re-render
   * pan/zoom
   * incremental edits that do not change the working set membership/order

---

If you want, next we can define the **canonical ordering** precisely for your IR entities vs RDF terms (so AST/IR/RDF selections land on the same anchors), and the exact structure of the **summary nodes** so they’re also traceable and explainable.
