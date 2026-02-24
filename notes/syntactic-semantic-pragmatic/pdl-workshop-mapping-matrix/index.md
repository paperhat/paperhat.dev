# PDL ↔ Workshop Mapping Matrix (v2)

## Purpose

Map Pragmatic Design Language (PDL) concepts to Workshop coverage with explicit separation between:

1. true normative gaps,
2. distributed-but-complete normative coverage,
3. vocabulary/framing gaps,
4. semantic translation gaps where PDL cannot map 1:1.

Inputs:
- `paperhat.dev/notes/syntactic-semantic-pragmatic/index.md`
- `workshop/spec/1.0.0/index.md` (especially §§18, 20–23, 26)

Status key:
- **Full** = concept is materially covered in normative text
- **Partial** = concept is covered but distributed/underspecified for direct conformance use
- **Missing** = no direct normative contract present

Gap type key:
- **Normative** = contract missing or under-specified
- **Distributed** = contract exists across multiple clauses; consolidation may help
- **Vocabulary** = concept exists but terminology differs
- **Translation** = PDL concept requires Workshop-native reinterpretation

Blocking decision key:
- **Blocker** = must be resolved before normative drafting

---

## A) Layering Model (Syntactic → Semantic → Pragmatic)

| PDL Concept | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Syntactic layer as relational constraints | §18.3 DesignPolicy; §26.3–§26.6 | Full | Vocabulary | None at contract level | Add glossary crosswalk (informative) |
| Semantic layer as role/meaning grammar | §18.1 + §18.2 + §26.2 + §20 | Full | Vocabulary | Covered but not labeled “role grammar” | Add term crosswalk, not new normative clause |
| Pragmatic layer as use/context adaptation | §26 Stage A/B/C and boundary contracts | Full | Vocabulary | No architecture defect | Add concise companion architecture map |
| “Rules based on use” as author mental model | Distributed across §26.3–§26.10 | Partial | Distributed | Needs synthesis for readability | Add informative synthesis table |

---

## B) Four Primitives (Intent, Confidence, Policy, Explanation)

| PDL Primitive | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Intent Model | §26.9 adaptive intent envelope; §26.10 stage contracts | Partial | Normative | Canonical intent field/typing vocabulary should be explicit | Add compact §26.9 intent-shape contract |
| Confidence Model | Not explicitly modeled; deterministic machinery exists | Missing | Translation **(Blocker)** | PDL confidence is probabilistic/time-freshness flavored; Workshop forbids ambient/time semantics | Resolve architecture decision first: confidence must be deterministic from explicit inputs only |
| Adaptation Policy (`maxDelta`, `cooldown`) | Determinism/fail-closed and bounded controls exist | Partial | Normative + Translation | Need explicit policy object; cooldown must be clock-free reinterpretation | Add bounded delta + clock-free cooldown semantics |
| Explanation Contract | Diagnostics are strict (§24, §26.11) | Partial | Translation | UX presentation mode is foundry concern | Specify explanation payload semantics only; keep presentation non-normative |

---

## C) Safety and Failure Behavior (Spec Scope)

| PDL Requirement | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Predictability / no abrupt jumps | §26.4/§26.5/§26.8 | Partial | Normative | No explicit adaptation-amplitude bounds | Add explicit bounded structural delta contract |
| Agency (user override) | §26.9.7 and §26.10.8 | Partial | Distributed | Mechanism exists; rights/precedence expression is diffuse | Add consolidation clause/table |
| Reversibility (restore defaults) | Not explicit | Missing | Normative | Baseline-restore contract absent | Add deterministic baseline-restore path |
| Accessibility precedence | §26.7 + §22/§23 | Full | Normative | None | None |
| Non-deception / non-obscurity | Indirect only | Partial | Normative | Add testable prohibition predicates for adaptation-induced demotion of cost/risk/consent elements | Add machine-testable adaptation honesty clause (per K.2) |
| Auditability | Decision traces exist | Partial | Normative | Need canonical event shape for adaptation audit | Add adaptation event schema |
| Low-confidence fallback | Not explicit | Missing | Normative | Fallback branch missing | Add confidence-gated fallback contract |

---

## D) Runtime/Execution Model (State Machine + Pipeline)

| PDL Runtime Concept | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| UX adaptation state machine metaphor | §26 Stage A/B/C contracts | Full | Vocabulary | Different framing, not missing mechanism | Add informative mapping only |
| Deterministic execution order | §5 + §26.10 | Full | Normative | None | None |
| Global precedence stack | Accessibility + arbitration + hard-feasibility semantics are distributed | Partial | Distributed | Consolidation may improve conformance clarity | Add single precedence consolidation table |
| Cooldown / anti-thrash | Some bounded controls in §26.8 | Partial | Translation | `cooldownMs` is temporal; Workshop must stay clock-free | Define Workshop-native cooldown and note behavioral non-equivalence |

---

## E) Solver Semantics

| PDL Solver Requirement | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Hard vs soft classes | Hard-feasibility-first and accessibility constitutional semantics exist | Partial | Distributed | Unify terminology for conformance readability | Add minimal consolidation |
| Explicit objective function | Optimization semantics exist | Partial | Translation | Fixed formula may overconstrain implementations | Keep formula informative; keep tie-break/precedence normative |
| Deterministic tie-break chain | Present but distributed | Partial | Distributed | Consolidate into one canonical chain | Add tie-break canonical table |
| Confidence-gated reweighting | Not explicit | Missing | Normative | Requires confidence decision first | Add only after blocker resolution |
| Timeout fallback | Fail-closed exists; timeout path not explicit | Partial | Normative | Need deterministic timeout fallback | Add timeout/fallback contract |

---

## F) Explanation, Telemetry, and Diagnostics

| PDL Requirement | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| User-facing explanation on adaptation | Diagnostics strict but UX explanation not modeled | Partial | Translation | Keep foundry boundary intact | Add deterministic explanation payload contract only |
| “Why this changed” trace view | Traces exist; no user-oriented projection | Partial | Normative | Need deterministic subset for explanation consumers | Add trace projection contract |
| Adaptation telemetry minimum schema | Diagnostic taxonomy exists | Partial | Normative | Need pipeline adaptation decision event schema (per K.3: pipeline decisions only, not task outcomes) | Add canonical pipeline telemetry event contract |
| Code vs explanatory text distinction | §26.11.7 explicit | Full | Normative | None | None |

---

## G) Component/Renderer Contract Mapping

| PDL Engineering Mapping | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Component-level API shape | Out-of-scope by current boundary design | Partial | Vocabulary | Should remain non-normative | Keep in companion implementation guide |
| Renderer capability profile facets | §22 has target profile and capability declarations | Partial | Distributed | Add fields only if parity requirements justify it | Optional §22.5 extension |
| Renderer solves constraints; semantics precomputed | §22–§23 + §5.9.4 explicit | Full | Normative | None | None |

---

## H) Governance and Ship Gate (Companion-Doc Scope)

These are process/governance policy unless machine-verifiable mechanism contracts are introduced.

| PDL Governance Check | Current Workshop Coverage | Status | Gap Type | Gap to Close | Suggested Action |
|---|---|---|---|---|---|
| Rule owner + measurable hypothesis | Not in spec | Missing | Vocabulary/process | Process policy, not semantic mechanism | Move to governance companion |
| Fallback defined before enablement | Not explicit as checklist | Partial | Vocabulary/process | Deployment process concern | Move to governance companion |
| Explanation copy approval workflow | Not in spec | Partial | Vocabulary/process | Workflow concern | Move to governance companion |
| Rollback switch exists | Not explicit | Missing | Normative | Mechanism-level activation/deactivation is missing | Keep as spec candidate (§26.9) |

Machine-verifiable metadata exception:
- Only manifest metadata that is machine-validated should be normative in §17.

---

## I) High-Value Priorities

0. **Blocker: confidence under determinism**
   - Decide between deterministic explicit-input confidence vs probabilistic ambient inference.
   - Recommended: deterministic explicit-input confidence only.
1. Confidence as first-class normative object (post-decision).
2. Bounded delta + Workshop-native clock-free cooldown.
3. Precedence consolidation for conformance clarity.
4. Explanation payload contract (semantic only).
5. Adaptation telemetry event schema.

---

## J) Minimal Additions Package (Scoped)

Precondition:
- Resolve the confidence blocker in Section I(0).

Additions:
- §26.9:
  - Canonical `AdaptiveIntent` field/typing contract.
  - `AdaptiveConfidence` contract constrained to deterministic explicit inputs.
  - Deterministic low-confidence fallback branch.
- §26.10:
  - Consolidated hard/soft terminology.
  - Consolidated precedence table and consolidated tie-break table (separate contracts per K.4).
  - Bounded delta + clock-free cooldown semantics.
- §26.11:
  - Explanation payload contract (semantic payload only; no UI mode requirements).
  - Adaptation telemetry minimum schema.
  - Deterministic linkage to canonical diagnostic codes.

Non-goal:
- Do not normatively specify foundry UX presentation modality.

This preserves Workshop architecture while cleanly separating normative gaps, vocabulary gaps, and translation decisions.

---

## K) Reviewer Clarifications to Carry Forward

These clarifications are accepted and should be treated as drafting constraints for any §26 edits.

### K.1 Confidence Blocker: Candidate Shape Sketches (for Decision Record)

The blocker is not only deterministic-vs-probabilistic; it is also input-shape architecture. Candidate deterministic shapes:

1. **Authored scalar on AdaptiveIntent**
  - Example: `confidence = 0.8` supplied in compiled adaptive request.
  - Pros: simplest, deterministic.
  - Tradeoff: little/no derivation semantics.

2. **Deterministic function over explicit context inputs**
  - Confidence computed from declared, typed context keys only.
  - Pros: useful and still deterministic.
  - Tradeoff: requires normative signal-set and function definition.

3. **Declared per-signal weight table + deterministic aggregation**
  - Author declares signal sources and weights; pipeline computes composite confidence.
  - Pros: closest to PDL `confidence.source` intent while deterministic.
  - Tradeoff: higher schema and conformance complexity.

4. **Hybrid (A base + C optional derivation)**
  - Canonical boundary value is always a scalar; authors supply directly or declare signals+weights for deterministic derivation.
  - Pros: boundary simplicity with opt-in provenance.
  - Tradeoff: dual-path validation; must fail closed if both paths declared.

See confidence-shape decision record for full option set and evaluation matrix.

Decision requirement:
- Choose one canonical shape (or strict profile set) before normative clause drafting.

### K.2 Non-Deception Clause Must Be Machine-Testable

Any adaptation-honesty contract must be encoded as deterministic, vector-testable predicates.

Acceptable formulation style examples:
- Adaptation MUST NOT reduce visibility rank of elements with declared `cost/risk/consent` semantic roles.
- Elements with declared consent-gate semantics MUST NOT be demoted below declared presentation thresholds (position/contrast constraints defined in canonical metrics).

Metric anchors: "visibility rank" and "presentation thresholds" must be defined in terms of existing §26.5 perceptual invariant and §26.6 visual encoding contracts.

Drafting rule:
- Do not add a principle-only “non-deception” clause without explicit measurable predicates.

### K.3 Telemetry Boundary Split (Normative vs Non-Normative)

Telemetry must be split by deterministic boundary:

1. **Normative pipeline telemetry (spec-able)**
  - Inputs used, rules fired, constraints selected/relaxed, confidence value, deterministic decision trace IDs.
  - Emitted by adaptive pipeline pre-foundry or at boundary artifacts.

2. **Outcome telemetry (non-normative / implementation policy)**
  - Task completion, user error count, elapsed task time, behavioral analytics.
  - Uses ambient post-render interaction state; not suitable as deterministic normative contract.

Drafting rule:
- §26 normative schema should cover pipeline decision telemetry only.

### K.4 Keep Precedence and Tie-Break as Separate Contracts

Do not conflate:

- **Precedence table**: category-level conflict resolution order (which constraint class wins).
- **Tie-break table**: candidate-selection order when equivalent feasible candidates remain.

Drafting rule:
- Maintain two independent normative tables with distinct conformance vectors.

### K.5 Separate Mechanisms: Low-Confidence Fallback vs Confidence-Gated Reweighting

These are related but distinct:

1. **Low-confidence fallback (binary gate)**
  - Below threshold: freeze or revert adaptation path per contract.

2. **Confidence-gated reweighting (continuous scaling)**
  - At/above threshold: soft-constraint weighting scales with confidence.

Drafting relationship rule:
- Specify interaction explicitly (e.g., fallback gate evaluated first; reweighting applies only when gate passes).
