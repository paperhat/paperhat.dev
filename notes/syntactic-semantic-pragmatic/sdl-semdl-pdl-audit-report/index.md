# Audit Report: Building the Best Syntactic/Semantic/Pragmatic Design Language System

## Framing

The question is not "can PDL fit into Workshop." The question is: **what is the best unified design language system expressible under deterministic, declarative, single-interpretation constraints** -- and what needs to change in both the PDL notes and the Workshop spec to build it?

The spec is unlocked. Everything is greenfield. The only non-negotiable constraints are: fully deterministic, fully declarative, single canonical interpretation, referential transparency, idempotency, round-trippability, and replayability.

---

## 1. The Three-Layer Model

### Verdict: Sound. Adopt it.

Morris's semiotic trichotomy (syntactics, semantics, pragmatics) applied to design language is a genuine theoretical contribution. It identifies a real hierarchy of abstraction:

- **Syntactic**: rules governing relationships between elements (proximity, contrast, alignment, grouping, separation, foregrounding, negative space)
- **Semantic**: rules governing what elements *mean* (roles, importance, data types, encoding obligations)
- **Pragmatic**: rules governing how presentation adapts to declared context (intent, confidence, bounded adaptation, stability)

This is the right foundation. But three problems need fixing.

### Problem 1: The layers are described but never formally defined

The index.md (lines 86--92) gives pithy one-liners for each layer. The v2 draft (lines 149--174) sharpens them. But nowhere do the documents answer: **what is the formal relationship between the layers?** Specifically:

- Does the pragmatic layer *modify* syntactic constraints, or *replace* them?
- Can a pragmatic rule create new semantic roles, or only reference existing ones?
- Is the semantic layer a dependency of both other layers, or do syntactic and pragmatic layers relate directly to each other?

The v2 draft says "Pragmatic rules operate above semantic roles and components" (line 170), and PDL rules use `weight`, `freeze`, `relax` actions on syntactic constraints (lines 300--305). This implies: **pragmatic rules modify the weights of syntactic constraints, mediated by semantic roles**. That's the right model, but it needs to be stated as a formal invariant, not left implicit.

**What's needed**: A normative layer-interaction contract. Syntactic constraints define the solution space. Semantic roles bind elements to meaning. Pragmatic rules reweight syntactic constraints based on declared context, referencing elements by their semantic roles. No layer may violate a lower layer's hard constraints -- it can only adjust soft-constraint weights within declared bounds.

### Problem 2: Workshop's schema families don't align 1:1

Workshop has nine schema families (S18). The three-layer model cuts across them:

| Layer | Workshop Coverage |
|---|---|
| Syntactic | DesignPolicy (S18.3) -> S26.3--26.4 pattern evaluation |
| Semantic | Domain (S18.1) + View (S18.2) + S26.5--26.6 invariants and encoding |
| Pragmatic | DesignIntent (S18.4) + S26.9--26.10 adaptive compiler + stages |

The misalignment is not fatal, but it's confusing. DesignIntent is named for semantic-level concern ("what it should feel like") but its normative home (S26.9--26.11) is pragmatic-level concern (adaptive compilation, stage evaluation). DesignPolicy sounds pragmatic ("policy") but is actually syntactic (compositional relations).

**What's needed**: The three-layer model should be the organizing principle of S26, not of the schema families. Schema families are authoring concerns -- they structure what authors write. The three layers are evaluation concerns -- they structure how the pipeline processes what was authored. These are orthogonal and should be treated as such. Rename nothing in S18. Restructure S26 into three explicit sub-contracts: Syntactic Evaluation (current S26.3--26.4 + new constraint vocabulary), Semantic Evaluation (current S26.5--26.6 + new role contract), Pragmatic Evaluation (current S26.9--26.10 + new adaptation contracts).

### Problem 3: The PDL documents conflate the model with a runtime engine

The index.md's "Vision" section (lines 95--143) describes a system that infers user goals, detects cognitive states, and adapts in real time. The v3 engineering mapping (lines 465--485) proposes a runtime state machine. These are application-layer behaviors, not design-language semantics.

The three-layer model doesn't require a runtime inference engine. It requires a **declarative constraint system** where:

- Authors declare syntactic constraints (relations between elements)
- Authors declare semantic roles (what elements mean)
- Authors declare pragmatic rules (how constraints change under declared contexts)
- The pipeline compiles these into a deterministic adaptive plan
- The foundry applies the plan given actual context values

The "intelligence" is in the authored rules, not in a runtime engine. This is the same insight that makes CSS powerful: media queries are declarative adaptation rules, not an inference engine.

**What's needed**: Strip the runtime inference framing from the PDL model entirely. Replace it with: the pragmatic layer is a declarative rule system over a closed set of typed context variables. The pipeline compiles all declared rules. The foundry evaluates typed predicates mechanically.

---

## 2. The Syntactic Design Language

### Verdict: The constraint vocabulary is excellent. The EBNF grammar is premature.

PDL's SDL (index.md, lines 245--277) defines eight relational constraint operators: `proximity`, `contrast`/`importance`, `alignment`, `repetition`, `separation`, `foregrounding`, `grouping`, `negative_space`. Each operates over named nodes with ordinal values (e.g., `tight | near | far`).

This is **better than what Workshop currently has**. Workshop's DesignPolicy (S18.3) names the same five design principles (Contrast, Repetition, Alignment, Proximity, Negative Space) but S26.3's pattern network expresses them as conditional rewrite rules with conditions and actions, not as direct relational declarations. The pattern network is the evaluation mechanism, not the constraint vocabulary.

### What SDL gets right

1. **Constraints are relations, not values.** `proximity(a, b) = near` declares a relationship, not `margin: 8px`. This is exactly the right level of abstraction for a deterministic design language -- it separates intent from realization.

2. **The operator set is grounded.** The eight operators map directly to established design principles (Gestalt proximity, visual hierarchy via contrast/foregrounding, structural coherence via alignment/repetition/grouping, breathing room via negative space/separation). This isn't arbitrary.

3. **Ordinal levels, not continuous values.** `tight | near | far`, `soft | clear | strong`, `loose | cohesive | locked`. This gives renderers bounded, enumerable solution spaces while maintaining relational semantics. Good for determinism -- a finite number of ordinal levels means a finite constraint space.

### What SDL gets wrong or leaves unfinished

**Problem 1: The EBNF grammar (lines 245--277) is a surface syntax, not a semantic contract.**

Workshop doesn't need a parser grammar for SDL -- it uses Codex as its surface form and RDF as its semantic representation. An EBNF grammar for a standalone SDL language creates a parallel authoring surface that would need its own parser, its own error model, and its own compilation path into Workshop's pipeline. This contradicts Workshop's single-surface-form architecture (S1.1 property 9, S11).

**What's needed**: Define the eight constraint operators as first-class Workshop concepts with RDF-native shapes, not as a standalone grammar. Authors write them in Codex. The pipeline evaluates them through S26's pattern evaluation machinery. The EBNF in the notes is useful as a *design sketch* for understanding the operators, but the normative form should be Codex concepts with SHACL shapes.

**Problem 2: The operators lack formal semantics.**

SDL declares `proximity(order_total, shipping_cost) = near`. But what does `near` *mean*? Not in pixels -- in constraint-satisfaction terms. The ordinal levels need formal definitions:

- What ordering relationship holds? (`tight < near < far` -- is this stated?)
- What is the interaction between operators? (If `proximity(a, b) = tight` and `separation(a, b) = strong`, is that a contradiction? Always? Sometimes?)
- How do operators compose? (If `group(a, b, c) = cohesive` and `proximity(a, b) = far`, which wins?)

Workshop's S26.5 (perceptual invariants) partially addresses this -- D26-5-2 requires "tighter intra-group than inter-group separation" -- but doesn't define the full interaction semantics for all eight operators.

**What's needed**: A constraint interaction matrix. For each pair of operators that can apply to overlapping node sets, define whether they are orthogonal, reinforcing, or potentially contradictory. For contradictory pairs, define the resolution rule. This is a significant piece of new design work.

**Problem 3: Node identity is undefined.**

SDL constraints reference nodes by `Identifier` (e.g., `order_total`, `place_order`). But what are these identifiers? Are they:

- Semantic role names?
- Element instance IRIs?
- Authored labels?
- View projection nodes?

The relationship between SDL node identifiers and Workshop's canonical design graph (S26.2) is not specified. S26.2 requires "complete element instance semantic bindings" (D26-2-3) and single-owner structural ownership (D26-2-2), but SDL nodes aren't anchored to this structure.

**What's needed**: SDL nodes must be defined as references to elements in the canonical design graph, resolved during S26.2's sealing phase. Each constraint operator takes element references, not arbitrary identifiers.

---

## 3. The Semantic Design Language

### Verdict: Underspecified. The PDL documents treat it as a pass-through between syntactic and pragmatic. It needs its own contract.

The semantic layer appears in the index.md (lines 89--90) as "rules based on the function or significance of an element" and in the v2 scope boundary (line 173) as "role grammar (`primary_action`, `warning`, `identity_chip`) and role obligations." The v3 engineering mapping defines a TypeScript type (lines 418--423):

```ts
type SemanticRole =
    | "primary_action"
    | "secondary_action"
    | "destructive_action"
    | "status_info"
    | "help_entry";
```

This is thin. Five roles is not a design language -- it is a proof of concept.

### What's needed

**A canonical semantic role vocabulary** that:

1. **Covers the full design space.** Not just actions -- also content roles (heading, body, caption, annotation), structural roles (container, group, separator, landmark), interactive roles (navigation, input, control, feedback), and status roles (success, warning, error, info, progress).

2. **Defines obligations per role.** Each role carries normative obligations: what syntactic constraints it requires, what visual encoding channels it's compatible with (connecting to S26.6), what accessibility semantics it implies (connecting to S26.7). A `destructive_action` role might carry obligations like "must use a selective channel for categorical distinction from `primary_action`" and "must not be the default focus target."

3. **Is closed for 1.0.0.** Like the visual encoding matrix (S26.6 D26-6-1), the role vocabulary should be a closed, enumerable set. Extension happens through spec revision, not through author declaration. This ensures single-interpretation determinism.

4. **Connects to the non-deception contract.** The mapping matrix's K.2 correctly demands machine-testable non-deception predicates. These must be anchored to semantic roles: "adaptation MUST NOT reduce the visibility rank of elements with `cost`, `risk`, or `consent` semantic roles." This requires the role vocabulary to include these categories.

### Workshop's current state

Workshop has the architectural hooks but not the vocabulary:

- S26.2 D26-2-3 requires "complete element instance semantic bindings" -- but doesn't define what bindings are available.
- S26.5 D26-5-3 requires "stable role-to-encoding mapping across contexts" -- but doesn't enumerate the roles.
- S26.6 defines visual encoding channels and a compatibility matrix -- but the matrix maps data types to channels, not semantic roles to channels.

**The semantic layer is the connective tissue between syntactic and pragmatic. Without a formal role vocabulary, the other two layers have nothing to bind to.**

---

## 4. The Pragmatic Design Language

### Verdict: The best ideas in the PDL documents, but almost everything needs rearchitecting for determinism.

### 4.1 What's Genuinely Valuable

**The four primitives** (Intent, Confidence, Adaptation Policy, Explanation) are the right decomposition of pragmatic concern. They answer: What is the user trying to do? How certain are we? What are we allowed to change? How do we explain what changed? Every adaptation system needs answers to these four questions.

**Confidence-proportional adaptation** is a real insight. The idea that adaptation should scale with certainty -- high confidence enables larger changes, low confidence constrains to baseline -- is sound design theory. It prevents the system from making dramatic changes on weak signals.

**Bounded adaptation delta** is critical. The idea that adaptation should never produce "abrupt, high-amplitude UI jumps" (line 213) is a genuine safety requirement. It prevents adaptation from destroying user orientation.

**The explanation contract** is necessary. Users have a right to understand why the interface changed. Making explanation a first-class primitive (not an afterthought) is correct.

### 4.2 What Needs Fundamental Rethinking

**Problem 1: Intent is not inferred -- it's declared.**

PDL's operational model (lines 339--342) says: "1. infer intent, 2. compute confidence." Workshop cannot infer. Intent must be a **declared input** -- either authored statically (this view serves the `checkout` intent) or supplied as a typed context variable by the application layer.

This changes what "intent" means. It's not a model of what the user is thinking. It's a **declared purpose** for the current view/composition. The author declares: "this composition serves the `checkout` intent in the `commit` phase." The pragmatic rules reference this declaration.

This is actually *better* than inference. It's explicit, deterministic, and auditable. And it's what good designers do anyway -- they design for specific intents, not for guessed ones.

**What's needed**: `AdaptiveIntent` as a first-class concept in the canonical design graph (S26.2), with required fields: `intentId` (already in S26.9 D26-9-1), `intentPhase` (new -- from PDL's `discover | decide | commit | recover`), and `intentPriority` (new -- from PDL's `low | medium | high`). All declared by the author, not inferred.

**Problem 2: Confidence must be deterministic from explicit inputs.**

The decision record template provides four options. Given the new framing (best system, no legacy), here's the assessment:

- **Option A (authored scalar)**: Too weak. An author-supplied `0.8` has no derivation semantics. You can't tell why confidence is 0.8 or what would make it higher. It's a magic number.
- **Option B (deterministic function over explicit inputs)**: The right foundation, but "spec-defined deterministic function" is a single function for all contexts, which is too rigid.
- **Option C (declared signal weights + aggregation)**: Closest to the right answer, but "per-signal weights" implies the author is inventing a confidence model, which is fragile.
- **Option D (hybrid A+C)**: Adds complexity without clarifying semantics.

**The best answer is none of these.** Confidence should be computed as a **deterministic function of context completeness**:

1. Each pragmatic rule declares its required context keys (e.g., `intent`, `phase`, `viewportClass`, `accessibilityProfile`).
2. Each context key is either present+well-typed, present+malformed, or absent.
3. Confidence for a rule = the proportion of its required context keys that are present and well-typed.
4. This is deterministic, requires no author-supplied weights, and has clear derivation semantics.

A rule that requires 4 context keys and gets 3 valid ones has confidence 0.75. The pipeline evaluates this deterministically. The pragmatic reweighting scales with this value. No inference. No magic numbers. No temporal freshness.

The rule author controls confidence *indirectly* by declaring required context keys. A rule that requires many signals adapts only when much context is available. A rule that requires one signal adapts readily. This is the right incentive structure.

**What's needed**: Define confidence as `|valid_present_keys| / |required_keys|` per rule. This is deterministic, composable, and self-documenting. It replaces all four options in the decision record.

**Problem 3: Cooldown must be structural, not temporal.**

PDL's `cooldownMs` (line 201) and temporal stability rules (lines 665--670) are wall-clock mechanisms. The best deterministic replacement:

**Bounded structural delta.** Define a deterministic metric for "how much the layout changed" between two adaptive plan outputs (e.g., edit distance over the ordered node sequence, or count of reordered/resized/reweighted elements). Declare a maximum delta per adaptation. If a candidate adaptation exceeds the delta bound, reject it and fall back to the nearest valid adaptation within bounds.

This is already partially present in S26.8 (cognitive footprint, D26-8-6: "structural reorientation cost"). What's needed is to formalize this as a constraint on the solver, not just a cognitive metric: the solver MUST NOT produce a solution whose structural delta from the baseline exceeds the declared bound.

**What's needed**: Add `maxStructuralDelta` as a declared constraint on pragmatic rules, defined in terms of a normative metric over the canonical design graph's element ordering and constraint weights. The solver treats this as a hard constraint.

**Problem 4: The state machine is the wrong metaphor.**

PDL's `Baseline -> InferredIntent -> Adapted -> Stabilized -> Baseline` state machine (lines 468--485) models runtime behavior that doesn't exist in Workshop's compile-time pipeline. But the *states* it identifies are real:

- **Baseline**: no pragmatic adaptation active (confidence too low, or no pragmatic rules apply).
- **Adapted**: pragmatic rules have modified syntactic constraint weights.
- **Stabilized**: adaptation is active but frozen (delta bound reached, or cooldown equivalent).

These aren't runtime states -- they're **solver output classes**. The solver produces a result that is classifiable as baseline, adapted, or stabilized, and this classification is part of the decision trace. This is auditable and deterministic without being a state machine.

**What's needed**: Define three adaptation result classes as part of the `AdaptiveDecisionReport` (S26.10 D26-10-9). Each pragmatic evaluation produces exactly one of: `baseline` (no reweighting applied), `adapted` (reweighting applied within bounds), `constrained` (reweighting was requested but bounded by delta/confidence constraints). This replaces the state machine.

**Problem 5: The PrDL grammar has the same surface-syntax problem as SDL.**

The PrDL EBNF (lines 279--315) defines a standalone language with `rule`, `when`, `apply`, `weight`, `freeze`, `relax`, `guard` constructs. As with SDL, this should not become a parallel authoring surface. It should inform the design of Codex concepts.

But the *operations* PrDL defines are exactly right:

- `weight <constraint> = <level>`: change a syntactic constraint's weight
- `freeze <constraint>`: lock a syntactic constraint at current weight
- `relax <constraint> [by <amount>]`: widen a constraint's acceptable range
- `guard <constraint>`: promote a soft constraint to hard for this context

These four operations are the pragmatic layer's vocabulary. They should be first-class action types in Workshop's pattern evaluation (S26.4), not a separate grammar.

**What's needed**: Add `weight`, `freeze`, `relax`, and `guard` as pragmatic action types in the pattern network (S26.3), alongside the existing condition/action system. Pragmatic rules are patterns whose conditions reference context variables and whose actions modify syntactic constraint weights.

---

## 5. Workshop Spec Changes Required

### 5.1 S26 Restructuring

Current S26 subsections:

| Current | Content |
|---|---|
| 26.1 | Purpose and boundary |
| 26.2 | Canonical design graph and sealing |
| 26.3 | Pattern network schema |
| 26.4 | Pattern evaluation semantics |
| 26.5 | Perceptual invariants |
| 26.6 | Visual encoding |
| 26.7 | Accessibility constitutional layer |
| 26.8 | Cognitive footprint |
| 26.9 | Adaptive compiler and context |
| 26.10 | Stage A/B/C integration |
| 26.11 | Validation, diagnostics, conformance |

Proposed restructuring to make the three-layer model explicit:

| Proposed | Content |
|---|---|
| 26.1 | Purpose, boundary, and layer model (NEW: formal three-layer interaction contract) |
| 26.2 | Canonical design graph and sealing (EXISTING, updated for role vocabulary anchoring) |
| 26.3 | **Syntactic constraint vocabulary** (NEW: the eight operators with formal interaction semantics) |
| 26.4 | Syntactic constraint evaluation (EXISTING S26.3--26.4, refactored) |
| 26.5 | **Semantic role vocabulary** (NEW: closed role set with obligations) |
| 26.6 | Perceptual invariant contract (EXISTING S26.5) |
| 26.7 | Visual encoding contract (EXISTING S26.6) |
| 26.8 | **Pragmatic context and confidence contract** (NEW: context variables, confidence derivation) |
| 26.9 | **Pragmatic rule evaluation** (NEW: weight/freeze/relax/guard actions, confidence-gated reweighting) |
| 26.10 | **Pragmatic safety contract** (NEW: bounded delta, non-deception, explanation, baseline-restore) |
| 26.11 | Accessibility constitutional layer (EXISTING S26.7) |
| 26.12 | Cognitive footprint contract (EXISTING S26.8) |
| 26.13 | Adaptive compiler and context (EXISTING S26.9, updated for new inputs) |
| 26.14 | Stage A/B/C integration (EXISTING S26.10, updated for new artifacts) |
| 26.15 | Validation, diagnostics, conformance (EXISTING S26.11, extended) |

### 5.2 New Normative Concepts Required

1. **Syntactic constraint operators** (8 operators with ordinal levels and formal interaction semantics)
2. **Semantic role vocabulary** (closed set with per-role obligations)
3. **Pragmatic context variable schema** (closed set of typed context keys)
4. **Confidence derivation contract** (deterministic function of context completeness)
5. **Pragmatic action types** (`weight`, `freeze`, `relax`, `guard`)
6. **Bounded structural delta** (normative metric and hard constraint)
7. **Non-deception predicates** (machine-testable, anchored to semantic roles)
8. **Explanation payload contract** (deterministic, semantic-only)
9. **Baseline-restore contract** (pipeline produces valid output with all pragmatic inputs absent)
10. **Adaptation result classification** (`baseline`, `adapted`, `constrained`)

### 5.3 Existing Contracts That Need Updating

1. **S26.2 (Sealing)**: D26-2-3 "complete element instance semantic bindings" must reference the new role vocabulary.
2. **S26.3/26.4 (Patterns)**: Must accommodate pragmatic action types alongside existing condition/action system.
3. **S26.5 (Perceptual invariants)**: D26-5-6 "explicit precedence rules" must be defined concretely, not just required to exist.
4. **S26.9 (Adaptive compiler)**: D26-9-1 must accept the new context variable schema. D26-9-5 and D26-9-6 must integrate pragmatic context.
5. **S26.10 (Stage B)**: D26-10-2 must incorporate confidence-gated reweighting and bounded delta as hard constraints in the solver.
6. **S26.11 (Diagnostics)**: New diagnostic codes for pragmatic contract violations.

---

## 6. Remaining Gaps Requiring New Design Work

These are items neither the PDL documents nor the Workshop spec currently address, and which are required for a complete system.

### Gap 1: The constraint interaction matrix

For eight syntactic operators that can apply to overlapping node sets, what are the pairwise interaction semantics? Which pairs reinforce, which are orthogonal, which can contradict? What are the resolution rules for contradictions? This is a combinatorial problem (28 pairs) that requires careful design grounded in design theory.

### Gap 2: The semantic role obligation table

For each role in the closed vocabulary, what syntactic constraints does it require? What visual encoding channels is it compatible with? What accessibility obligations does it carry? This is a substantial table that connects all three layers.

### Gap 3: The pragmatic context variable set

What are the canonical context variables? The PDL documents suggest `intent`, `phase`, `confidence`, `viewportClass`, `inputMode`, `accessibilityProfile`. Are there others? What are their types? What are their legal values? This must be a closed, typed set for determinism.

### Gap 4: The structural delta metric

How do you measure "how much the layout changed" deterministically? You need a formal metric over the canonical design graph that produces a deterministic scalar distance between two adaptive plan outputs. This must be defined precisely enough that all implementations compute the same distance for the same inputs.

### Gap 5: Solver specification under the new constraint types

Stage B (S26.10 D26-10-2) does "hard-feasibility-first deterministic optimization and relaxation." With the addition of pragmatic reweighting, confidence-gated scaling, bounded delta constraints, and guard promotions, the solver's specification becomes significantly more complex. The PDL v3's solver semantics (index.md lines 597--712) provide a starting sketch, but the objective function and precedence order need to be defined in Workshop-native terms, with a single normative specification -- not an informative formula that implementations may interpret differently.

### Gap 6: Conditional adaptive plan structure

If pragmatic rules produce context-dependent adaptations, the `AdaptivePlanPackage` (S26.10 D26-10-9) must either contain conditional branches or the pipeline must enumerate all context configurations. The former is more practical but requires defining the conditional structure. The latter is simpler but may be combinatorially explosive. This is an architectural decision that affects the foundry boundary contract (S22).

---

## 7. Redundancies to Eliminate

1. **The PDL index.md v1 discussion (lines 1--78)** is historical motivation. Valuable as a companion essay but not as spec input. Don't carry it forward.
2. **The TypeScript interfaces in v3 (lines 406--463)** are implementation artifacts. They informed the design but belong in a companion implementation guide, not in spec drafting materials.
3. **The telemetry schema in v3 (lines 518--552)** mixes normative and non-normative data. Split per K.3 and define only the normative pipeline schema.
4. **The v3 "Reference Implementation Slice" (lines 567--595)** is a test plan, not a spec artifact. Move to conformance test design.
5. **The mapping matrix's informative-only suggestions** (vocabulary crosswalks, companion architecture maps) are good ideas for companion documents but should not enter the normative drafting process.

---

## 8. Summary

| Aspect | Status |
|---|---|
| Three-layer model | Sound. Needs formal layer-interaction contract. |
| Syntactic constraint vocabulary | Excellent starting point. Needs formal interaction semantics, Workshop-native representation, node identity anchoring. |
| Semantic role vocabulary | Critically underspecified. Needs full design from near-scratch. |
| Pragmatic primitives (intent, confidence, policy, explanation) | Right decomposition. Every primitive needs rearchitecting for determinism. |
| Confidence model | Decision record's four options are all wrong. Propose context-completeness derivation. |
| Adaptation stability | Temporal cooldown -> bounded structural delta. Needs formal metric. |
| Safety invariants | Mostly right. Non-deception needs metric anchors. Baseline-restore needs formal contract. |
| Workshop S26 readiness | Strong architectural foundation. Needs restructuring and significant additions. |
| SDL/PrDL grammars | Useful as design sketches. Must not become parallel authoring surfaces. Operators and actions should become Workshop-native concepts. |
| Solver specification | Partially addressed by both PDL and Workshop. Needs unified, precise normative specification. |

**The system is buildable.** The theoretical foundation is sound, the architectural invariants are clear, and the Workshop spec provides a rigorous framework to build within. The main work is: (1) defining the three new vocabularies (syntactic operators, semantic roles, pragmatic context variables), (2) formalizing their interaction semantics, (3) rearchitecting confidence and stability for determinism, and (4) extending S26 with the new contracts while preserving its existing strengths.
