# CDL/SDL/PDL Design Decisions Record

## Status

- **Date**: 2026-02-25
- **Status**: Approved (owner decision)
- **Scope**: Workshop §18 (schema families) and §26 (design semantics and adaptive evaluation)
- **Supersedes**: `confidence-shape-decision-record-template/index.md` (all four options rejected; replaced by DEC-07)
- **Companion documents**:
  - `sdl-semdl-pdl-audit-report/index.md` (problem identification)
  - `pdl-workshop-mapping-matrix/index.md` (gap analysis)
  - `index.md` (original PDL theory and discussion)

---

## Non-Negotiable Constraints

Every decision below satisfies all of the following. Any future revision must also satisfy all of the following.

1. Fully deterministic: identical inputs produce identical outputs.
2. Fully declarative: no imperative logic, no runtime inference.
3. Single canonical interpretation: one spec, one meaning, one implementation behavior.
4. Referential transparency: any sub-expression can be replaced by its value.
5. Idempotency: applying the same operation twice produces the same result as once.
6. Round-trippability: Codex surface form and RDF canonical form are losslessly interconvertible.
7. Replayability: any pipeline execution can be replayed from its declared inputs with identical results.

---

## DEC-01: Three-Layer Model — Adopted

The design language system is organized into three layers derived from Morris's semiotic trichotomy:

- **Compositional Design Language (CDL)**: rules governing relationships between elements. Constraints are relations, not values. Eight operators with ordinal levels.
- **Semantic Design Language (SDL)**: rules governing what elements mean. A closed canonical role vocabulary with per-role obligations connecting to CDL constraints, visual encoding channels, and accessibility semantics.
- **Pragmatic Design Language (PDL)**: rules governing how presentation adapts to declared context. Four primitives: intent, confidence, adaptation policy, explanation contract.

### Layer Interaction Contract

This is a normative invariant.

1. CDL constraints define the solution space. Each constraint is a relation between element references with an ordinal level and a weight.
2. SDL roles bind elements to meaning. Each role carries normative obligations (required CDL constraints, encoding compatibility, accessibility binding).
3. PDL rules reweight CDL constraints based on declared context, referencing elements by their SDL roles. PDL's four operations (`weight`, `freeze`, `relax`, `guard`) modify CDL constraint weights.
4. No layer may violate a lower layer's hard constraints. PDL can adjust soft-constraint weights within declared bounds. PDL cannot create new SDL roles or new CDL operators.
5. SDL role obligations are floor constraints. PDL can increase emphasis but cannot reduce below the role's declared obligations.

### Naming

- CDL, not "Syntactic Design Language," to avoid collision with SDL (Semantic Design Language).
- "Compositional" is chosen because the layer governs how elements compose together. It is immediately intuitive to designers and technically accurate.

---

## DEC-02: Schema Family Changes — DesignPolicy and DesignIntent Replaced

DesignPolicy and DesignIntent are replaced by three new schema families aligned with the three-layer model. This changes the schema family count from 9 to 10.

| # | Family | Purpose | Layer |
|---|---|---|---|
| 1 | Domain | Define what exists (ontology) | Upstream of design |
| 2 | View | Define what to show (projection/selection) | Upstream of design |
| 3 | **DesignConstraint** | Declare compositional constraints between elements | CDL |
| 4 | **DesignRole** | Assign semantic roles to elements | SDL |
| 5 | **AdaptiveRule** | Declare pragmatic adaptation rules | PDL |
| 6 | Assembly | Define how it is packaged | Unchanged |
| 7 | Behavior | Define how values are computed | Unchanged |
| 8 | System | Define how packages are organized | Unchanged |
| 9 | Vocabulary | Define standardized reference tokens | Unchanged |
| 10 | Meta | Define what other schemas may declare | Unchanged |

### Design Rationale

- Domain and View are upstream of design. They define what the design has to work with.
- DesignConstraint replaces DesignPolicy. "Policy" sounded pragmatic but was actually compositional. DesignConstraint declares relational constraints authored in Codex, evaluated through §26's pattern machinery.
- DesignRole replaces the semantic portion of DesignIntent. It is the authoring surface for the SDL role vocabulary.
- AdaptiveRule replaces the pragmatic portion of DesignIntent. It is the authoring surface for PDL rules (context predicates + constraint modification actions).
- Theming tokens (t-shirt sizes, color roles, typefaces) move to DesignConstraint. They are encoding constraints, not intent.

---

## DEC-03: CDL — Eight Constraint Operators with Ordinal Levels

### Operators

| Operator | Ordinal Levels | What It Constrains |
|---|---|---|
| `proximity` | `tight`, `near`, `far` | Spatial closeness between elements |
| `contrast` | `soft`, `clear`, `strong` | Perceptual differentiation between elements |
| `alignment` | `loose`, `aligned`, `locked` | Structural alignment between elements |
| `repetition` | `loose`, `cohesive`, `locked` | Consistency/sameness between elements |
| `separation` | `subtle`, `clear`, `strong` | Perceptual distance/boundary between elements |
| `foregrounding` | `subtle`, `prominent`, `dominant` | Visual hierarchy/emphasis of an element |
| `grouping` | `loose`, `cohesive`, `locked` | Perceptual unity of a set of elements |
| `negative_space` | `minimal`, `balanced`, `generous` | Breathing room around/between elements |

### Invariants

1. Ordinal levels define a strict total ordering per operator (e.g., `tight < near < far`).
2. Constraints are relations between element references, not values. `proximity(a, b) = near` declares a relationship, not a measurement.
3. Each constraint has a weight in [0, 1] determining its influence in the solver's badness function. Default weight is 1.0 (full influence).
4. Constraints are soft by default. PDL `guard` promotes a constraint to hard. Hard constraints must be satisfied; soft constraints contribute to badness.
5. Ordinal levels are abstract. Concrete realization (pixels, points, ratios) is foundry business, governed by foundry brand/theme configuration. The spec prescribes ordering invariants and interaction rules, not metric values.
6. Node references in constraints are references to elements in the canonical design graph (§26.2), resolved during sealing. Not arbitrary identifiers.

### No EBNF Grammar

CDL is not a standalone language with its own parser. CDL operators are first-class Workshop concepts with RDF-native shapes. Authors write them in Codex. The EBNF in the original PDL notes is informative-only design sketch material. The normative form is Codex concepts with SHACL shapes.

---

## DEC-04: CDL Constraint Interaction Matrix

When two CDL operators apply to overlapping element sets, three relationships are possible:

- **Orthogonal**: independent properties, no interaction. Both apply independently.
- **Reinforcing**: push in the same direction. Both apply, effects compound.
- **Contradictory**: can push in opposite directions. Creates tension resolved by the solver.

### Matrix

|  | proximity | contrast | alignment | repetition | separation | foregrounding | grouping | negative_space |
|---|---|---|---|---|---|---|---|---|
| **proximity** | — | orth | orth | reinf | **contra** | orth | reinf | **contra** |
| **contrast** |  | — | orth | **contra** | orth | reinf | orth | orth |
| **alignment** |  |  | — | reinf | orth | orth | reinf | orth |
| **repetition** |  |  |  | — | orth | **contra** | reinf | orth |
| **separation** |  |  |  |  | — | orth | **contra** | reinf |
| **foregrounding** |  |  |  |  |  | — | orth | orth |
| **grouping** |  |  |  |  |  |  | — | **contra** |
| **negative_space** |  |  |  |  |  |  |  | — |

### Six Contradictory Pairs

1. **proximity vs. separation**: tight proximity opposes strong separation.
2. **proximity vs. negative_space**: tight proximity opposes generous negative space.
3. **contrast vs. repetition**: strong contrast (differentiation) opposes locked repetition (sameness).
4. **repetition vs. foregrounding**: locked repetition (uniformity) opposes dominant foregrounding (one element stands out).
5. **separation vs. grouping**: strong separation (push apart) opposes cohesive grouping (pull together).
6. **grouping vs. negative_space**: cohesive grouping (minimize internal space) opposes generous negative space (maximize space).

### Resolution Rule

Contradictions are not errors. They are **tension**. Good design often involves deliberate tension (tight grouping with strong internal contrast).

1. Both contradictory constraints enter the solver as soft terms with their respective weights.
2. The badness function accumulates penalty from both.
3. The solver finds the least-bad tradeoff.
4. If one is `guard`-promoted to hard, it wins absolutely.
5. If both are hard, it is an author error. Fail closed with a diagnostic code.
6. The solver reports which contradictory pairs were active and how they were resolved in the decision trace.

---

## DEC-05: SDL — Semantic Role Vocabulary Structure

### Per-Role Entry Fields

Each semantic role in the closed vocabulary defines:

1. **Role ID**: canonical identifier (e.g., `primary_action`, `cost_disclosure`).
2. **Category**: one of Content, Structure, Interactive, Status, or Disclosure.
3. **CDL obligations**: required compositional constraints (e.g., a `primary_action` MUST have `foregrounding >= prominent` relative to peer actions).
4. **Encoding compatibility**: which §26.6 visual encoding channels are valid for this role.
5. **Accessibility binding**: the ARIA role or landmark this maps to (connecting to §26.7).
6. **Non-deception protection level**: whether this role is adaptation-protected.

### Non-Deception Contract

- All roles in the **Disclosure** category have their CDL constraints floor-locked.
- PDL rules cannot `relax` or `weight` Disclosure-role constraints below their authored values.
- `guard` is implicit for Disclosure roles. Their constraints are always hard.
- Machine-testable predicate: adaptation MUST NOT reduce the visibility rank of elements with Disclosure-category roles.

### Closure

The role vocabulary is a closed, enumerable set for 1.0.0. Extension happens through spec revision only, not through author declaration. This ensures single-interpretation determinism.

### Draft Status

The specific roles have not yet been enumerated. A draft will be produced as a separate deliverable, structured into the five categories (Content, Structure, Interactive, Status, Disclosure), grounded in ARIA roles for accessibility mapping and established design system patterns for the other categories.

---

## DEC-06: PDL — Four Primitives, Rearchitected for Determinism

### 6a. Intent

Intent is the **declared purpose** of the current composition. It is not inferred.

- Intent is a context variable (`intent`) supplied by the application layer at evaluation time.
- The author writes pragmatic rules with conditions referencing intent values: `when intent = checkout, guard(cost_disclosure)`.
- Intent values are author-declared enum members (e.g., `browse`, `checkout`, `configure`, `compose`).
- The adaptive plan contains conditional branches gated on intent predicates. The foundry evaluates predicates mechanically.

### 6b. Confidence

Confidence is a **deterministic function of context completeness**. This replaces all four options in the original decision record template.

- Each pragmatic rule declares its required context keys.
- Confidence for a rule = `|valid_present_keys| / |required_keys|`.
- The function is **linear**. Each context key contributes equally.
- Effect on reweighting is linear: `effective_weight = base_weight * confidence`.
- Optional **hard floor threshold** per rule (author-declared, or spec-wide default). Below the floor, the rule does not fire and the output is baseline.
- Confidence is derived by the pipeline, not authored or supplied externally.
- A rule that requires many context keys adapts only when rich context is available. A rule requiring one key adapts readily. This is the correct incentive structure.

### 6c. Adaptation Policy (Four Operations)

PDL provides four action types that modify CDL constraints:

| Operation | Effect |
|---|---|
| `weight <constraint> = <level>` | Change a CDL constraint's weight |
| `freeze <constraint>` | Lock a CDL constraint at current weight (immune to further reweighting) |
| `relax <constraint> [by <amount>]` | Widen a CDL constraint's acceptable range |
| `guard <constraint>` | Promote a soft CDL constraint to hard for this context |

These are first-class action types in Workshop's pattern evaluation machinery (§26.4), authored in Codex. They are not a separate grammar. The PrDL EBNF from the original notes is informative-only.

### 6d. Explanation Contract

Users have a right to understand why the interface changed. Explanation is a first-class primitive.

- The adaptive plan includes a deterministic explanation payload for every pragmatic modification.
- The payload is semantic only: which rules fired, which constraints were modified, which context keys were present/absent, what the confidence was.
- Presentation modality (toast, panel, tooltip, etc.) is foundry business, not spec business.
- Explanation payload links to canonical diagnostic codes per §26/§24 taxonomy.

---

## DEC-07: Confidence Shape — Context Completeness (Supersedes Decision Record Template)

This decision supersedes the confidence-shape decision record template and its four candidate options (A, B, C, D). All four are rejected.

- **Option A (authored scalar)**: Rejected. No derivation semantics. Magic number.
- **Option B (deterministic function)**: Right foundation, but a single spec-defined function for all contexts is too rigid.
- **Option C (declared signal weights)**: Author-invented confidence models are fragile and arbitrary.
- **Option D (hybrid A+C)**: Adds complexity without clarifying semantics.

**Selected approach**: Confidence is `|valid_present_keys| / |required_keys|` per rule. See DEC-06b for full specification.

---

## DEC-08: Adaptation Result Classes — Replace State Machine

The PDL state machine (`Baseline -> InferredIntent -> Adapted -> Stabilized -> Baseline`) is rejected. It models runtime behavior that does not exist in a declarative compile-time pipeline.

The states it identifies are real but are reclassified as **solver output classes**:

| Class | Meaning |
|---|---|
| `baseline` | No pragmatic reweighting applied. Either confidence was below the floor, or no pragmatic rules matched. |
| `adapted` | Pragmatic reweighting applied within all bounds (confidence, structural delta). |
| `constrained` | Pragmatic reweighting was requested but bounded by delta or confidence constraints. Partial adaptation applied. |

Every pragmatic evaluation produces exactly one class. The class is recorded in the `AdaptiveDecisionReport` and is part of the decision trace. This is auditable and deterministic.

---

## DEC-09: Structural Delta — Chebyshev over Four Axes

### Axes

| Axis | What It Captures | Why It Matters |
|---|---|---|
| Element ordering | Rearrangement of elements | Most disorienting perceptual change |
| Constraint weights | Shift in CDL constraint weights | Drives solver output; changes element relationships |
| Visibility state | Elements appearing or disappearing | High-impact binary change |
| Guard promotions | Soft constraints promoted to hard | Feasibility boundary shift; cascade risk |

### Rejected Axes

- **Encoding channel changes**: downstream of constraint weight changes. Measuring both double-counts.
- **Role reassignment**: should not happen through adaptation. Pragmatic rules do not change what an element means.
- **Absolute position/size**: foundry business. Adaptive plan does not specify pixels.

### Metric

Chebyshev distance (L-infinity norm): `structuralDelta = max(ordering_delta, weight_delta, visibility_delta, guard_delta)`.

Each axis is normalized to [0, 1]. The bound constrains the worst-case single-axis change.

### Bound Model

- `maxStructuralDelta`: overall bound. Applies as default to all axes.
- Per-axis overrides: `maxOrderingDelta`, `maxWeightDelta`, `maxVisibilityDelta`, `maxGuardDelta`.
- Resolution: explicit per-axis bound wins. If no per-axis bound declared, overall bound applies.
- If any axis exceeds its effective bound, the adaptation is rejected and falls back to the nearest valid adaptation within bounds.

---

## DEC-10: Pragmatic Context Variable Set

### Variables

| Variable | Type | Sourced By | Required? |
|---|---|---|---|
| `viewportClass` | enum: `compact`, `standard`, `expanded` | Platform/foundry | Yes |
| `inputMode` | enum: `touch`, `pointer`, `keyboard`, `voice` | Platform/foundry | Yes |
| `accessibilityProfile` | flags: `reducedMotion`, `highContrast`, `screenReader`, `magnification` | Platform/OS | Yes (empty set if none) |
| `locale` | BCP-47 tag | Platform/OS | Yes |
| `intent` | enum: author-declared IDs | Application | No |
| `phase` | enum: `discover`, `decide`, `commit`, `recover` | Application | No |
| `density` | enum: `compact`, `comfortable`, `spacious` | Application (user pref) | No |
| `confidence` | scalar [0, 1] | Derived by pipeline | N/A (always computed) |

### Sourcing Model

- **Platform-sourced** (viewportClass, inputMode, accessibilityProfile, locale): always present. Foundries must supply these.
- **Application-sourced** (intent, phase, density): optional. May be absent.
- **Derived** (confidence): computed per-rule from presence/validity of other variables.

### Graceful Degradation

Rules referencing absent optional variables get proportionally reduced confidence. If confidence drops below the rule's floor threshold, the rule does not fire. A simple static site that never supplies `intent` or `phase` gets baseline output from all rules that require them. A rich interactive application that supplies full context gets full adaptation. This is the correct incentive structure.

### View Projections vs. Pragmatic Rules

If a context variable (e.g., `density`) affects **what data to show**, the author creates different View projections. If it affects **how the same data is laid out**, the author writes pragmatic rules. These are different operations at different layers. The author may use both for the same context variable.

---

## DEC-11: Solver Specification — Single Normative Badness Function

### Architecture

The solver follows the Knuth-Plass precedent: global optimization against a defined badness function. This is not limited to paragraph layout. It is the general quality metric for any adaptive plan.

### Integration with Three-Layer Model

- **CDL defines the badness terms.** Each compositional constraint contributes a term. Violating a soft constraint increases badness.
- **SDL defines role obligations.** Role obligations are additional badness terms (or hard constraints). Failing to meet a role's CDL obligation increases badness.
- **PDL modifies term weights.** Confidence-proportional reweighting changes coefficients. `weight` changes a term's coefficient. `guard` promotes a term to hard. `freeze` locks a coefficient. `relax` widens acceptable ranges.
- **The solver minimizes total weighted badness under hard constraints.**

### Badness Function

Single normative formula: `B = sum(weight_i * violation_i)` where:

- `weight_i` is the effective weight of constraint_i after pragmatic reweighting (base weight * confidence scaling).
- `violation_i` is a normalized [0, 1] measure of how much constraint_i is violated. Each CDL operator defines its own violation metric.

### Evaluation Order

1. **Hard feasibility first.** All hard constraints (guard-promoted, accessibility constitutional, Disclosure floor-locks) must be satisfied. If no feasible solution exists, proceed to relaxation.
2. **Soft optimization.** Minimize total weighted badness across all soft constraints.
3. **Relaxation.** If no feasible solution exists under hard constraints, relax lowest-weighted soft constraints first, with lexical tie-break on constraint ID. Relaxation converts the lowest-weighted hard constraint back to soft, then re-optimizes. Repeat until feasible.
4. **Tie-break.** If multiple feasible solutions have equal badness, select by lexical ordering on the content-addressed serialized plan (deterministic).

### Structural Delta as Hard Constraint

The solver MUST NOT produce a solution whose structural delta (DEC-09) exceeds the declared bounds. Structural delta bounds are hard constraints in the solver, evaluated after soft optimization.

---

## DEC-12: Conditional Adaptive Plan Structure

### Decision

The adaptive plan uses **conditional branches** (not enumerated plans).

### Structure

The `AdaptivePlanPackage` contains:

1. A **base constraint set**: the CDL constraints and SDL role obligations as authored, with no pragmatic modifications.
2. An **ordered list of conditional modifications**: each entry contains:
   - A **typed predicate** over the context variable set (e.g., `intent = checkout AND phase = commit`).
   - A **set of CDL constraint modifications** (weight, freeze, relax, guard actions).
3. An **adaptation result class** per conditional path (baseline, adapted, constrained).
4. An **explanation payload** per conditional path.

### Evaluation by Foundry

The foundry evaluates predicates top-to-bottom against actual context values. All matching modifications are applied in order. The result is fed to the foundry's solver. This is deterministic because predicate evaluation order is fixed and modifications compose deterministically.

### Analogy

This is analogous to CSS media queries: a base stylesheet plus conditional overrides. The browser evaluates conditions and applies matching rules. Workshop does the same with typed context predicates instead of `@media` blocks.

---

## DEC-13: §26 Restructuring

### Current Structure (11 subsections)

| # | Content |
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

### Proposed Structure (15 subsections)

| # | Content | Source |
|---|---|---|
| 26.1 | Purpose, boundary, and layer model | Updated. Adds formal three-layer interaction contract (DEC-01). |
| 26.2 | Canonical design graph and sealing | Updated. Role vocabulary anchoring added. |
| 26.3 | CDL constraint vocabulary | **New.** Eight operators, ordinal levels, interaction matrix (DEC-03, DEC-04). |
| 26.4 | CDL constraint evaluation | Refactored from existing §26.3/26.4. |
| 26.5 | SDL role vocabulary | **New.** Closed role set with obligations (DEC-05). |
| 26.6 | Perceptual invariant contract | Existing §26.5. |
| 26.7 | Visual encoding contract | Existing §26.6. |
| 26.8 | PDL context and confidence contract | **New.** Context variables, confidence derivation (DEC-10, DEC-06b). |
| 26.9 | PDL rule evaluation | **New.** Four operations, confidence-gated reweighting (DEC-06c). |
| 26.10 | PDL safety contract | **New.** Bounded delta, non-deception, explanation, baseline-restore (DEC-09, DEC-05 non-deception, DEC-06d). |
| 26.11 | Accessibility constitutional layer | Existing §26.7. |
| 26.12 | Cognitive footprint contract | Existing §26.8. |
| 26.13 | Solver specification | **New.** Normative badness function, evaluation order, relaxation, tie-break (DEC-11). |
| 26.14 | Adaptive compiler and stage integration | Merged/updated from existing §26.9/26.10. Incorporates conditional plan structure (DEC-12). |
| 26.15 | Validation, diagnostics, conformance | Existing §26.11, extended for new contracts. |

---

## DEC-14: Branding, Theming, and Foundry Configuration

CDL declares abstract ordinal relations. The foundry's brand/theme configuration maps ordinals to concrete values.

- Two recipe sites can share identical CDL constraints but look different because their foundry configurations interpret `near`, `soft contrast`, and `prominent` differently.
- The design (CDL + SDL + PDL) is the same. The expression differs.
- Ratio relationships between ordinal levels (golden ratio, geometric progression, etc.) are foundry configuration, not spec business.
- The spec prescribes ordering invariants (`tight < near < far`) and interaction rules. The foundry prescribes metric realization.

---

## DEC-15: Redundancies Eliminated

The following items from the original PDL notes are not carried forward into normative drafting:

1. PDL index.md v1 discussion (historical motivation) — companion essay, not spec input.
2. TypeScript interfaces in v3 — implementation artifacts for companion implementation guide.
3. Telemetry schema in v3 — split per K.3. Only normative pipeline decision telemetry enters the spec.
4. v3 "Reference Implementation Slice" — test plan for conformance test design, not spec.
5. EBNF grammars for SDL and PrDL — informative-only if preserved. Normative form is Codex concepts with SHACL shapes.
6. The PDL state machine — replaced by solver output classes (DEC-08).
7. The confidence-shape decision record's four options — superseded by context-completeness derivation (DEC-07).
8. `cooldownMs` and all temporal semantics — replaced by bounded structural delta (DEC-09).
9. All runtime inference / cognitive state detection framing — replaced by declarative context variables (DEC-10).

---

## Next Steps

1. **Draft the SDL semantic role vocabulary.** Enumerate the closed role set across five categories (Content, Structure, Interactive, Status, Disclosure) with per-role obligation tables.
2. **Begin §26 restructuring.** Apply DEC-13 to the Workshop spec.
3. **Write normative CDL operator contracts.** Codex concept definitions and SHACL shapes for the eight operators.
4. **Write normative PDL contracts.** Context variable schema, confidence derivation, four operations, conditional plan structure.
5. **Write the solver specification.** Single normative badness function with evaluation order.
6. **Update §18.** Apply DEC-02 schema family changes.
7. **Extend §26.15 diagnostics.** New diagnostic codes for CDL/SDL/PDL contract violations.
