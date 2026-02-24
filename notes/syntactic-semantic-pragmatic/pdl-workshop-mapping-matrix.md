# PDL ↔ Workshop Mapping Matrix (Draft)

## Purpose

Map Pragmatic Design Language (PDL) concepts from this note thread to current Workshop normative coverage, then identify exact normative gaps.

Inputs:
- `paperhat.dev/notes/syntactic-semantic-pragmatic/index.md`
- `workshop/spec/1.0.0/index.md` (especially §§18, 20–23, 26)

Status key:
- **Full** = concept is already materially covered in normative text
- **Partial** = materially related clauses exist but author-facing or semantic surface is incomplete
- **Missing** = no direct normative contract currently present

---

## A) Layering Model (Syntactic → Semantic → Pragmatic)

| PDL Concept | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Syntactic layer as relational constraints (contrast/alignment/proximity/etc.) | §18.3 DesignPolicy; §26.3–§26.6 pattern + encoding contracts | Full | None for core principle; only terminology harmonization needed | Add glossary crosswalk in §26 intro |
| Semantic layer as role/meaning grammar | §18.1 Domain, §18.2 View, §20 semantic projection contracts | Partial | No concise “role grammar” abstraction that aligns to PDL wording | Add small “semantic role contract” subsection under §26.2 or §26.6 |
| Pragmatic layer as use/context adaptation | §26 (adaptive evaluation), Stage A/B/C + boundaries | Full | None at architecture level; packaging/readability gap remains | Add a one-page non-normative architecture map in §26 preface |
| “Rules based on use” as first-class author mental model | Distributed across §26.3–§26.10 | Partial | §26 is clause-complete but not expressed as simple author-facing PDL model | Add §26.x “Author-Facing Pragmatic Model” informative summary |

---

## B) Four Primitives (Intent, Confidence, Policy, Explanation)

| PDL Primitive | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Intent Model (`intent.name`, `intent.phase`, `priority`) | §26.9 adaptive intent envelope; Stage contracts in §26.10 | Partial | Needs explicit canonical intent vocabulary/typing and closed enum policy | Add §26.9 subclause defining canonical intent shape + typing rules |
| Confidence Model (`value`, `source`, `window`) | Indirectly implied through deterministic evaluation and feasibility stages | Missing | No explicit confidence object, provenance of confidence, or freshness semantics | Add §26.9 confidence contract + deterministic confidence derivation inputs |
| Adaptation Policy (`mutable`, `maxDelta`, `cooldown`) | Determinism/fail-closed and optimization constraints in §26.4/§26.8/§26.10 | Partial | Missing explicit bounded-change policy object and per-cycle mutation guard semantics | Add §26.8.x “Adaptation Delta Governance Contract” |
| Explanation Contract (`required`, `mode`, `template`) | Diagnostics are strict in §24 + §26.11 | Partial | User-facing explanation semantics are not explicitly normative (diagnostics ≠ user explanation) | Add §26.11.x “Explanation Surface Contract” separate from error diagnostics |

---

## C) Safety, Governance, and Failure Behavior

| PDL Requirement | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Predictability / no abrupt jumps | Determinism + fail-closed + invariant preservation (§26.4, §26.5, §26.8) | Partial | No explicit “visible change amplitude” metric and threshold contract | Add §26.8 bound on structural delta per transition |
| Agency (user override) | Override path appears in §26.9.7 and §26.10.8 | Partial | No explicit user override rights model (scope, persistence, precedence) | Add §26.9 override semantics table |
| Reversibility (restore defaults) | Not explicit | Missing | Need deterministic “return to semantic baseline” contract | Add §26.10 clause for baseline restore path |
| Accessibility precedence | Strongly explicit in §26.7 + §22/§23 enforcement | Full | None | N/A |
| Non-deception / no obscuring cost/risk/consent | Indirect through fail-closed governance; no explicit deception clause | Partial | Add direct prohibition language for adaptation-induced obscurity | Add §26.7 or §26.11 policy ethics clause |
| Auditability of significant adaptations | Decision traces and diagnostics exist (§26.4.7, §26.11) | Partial | Need explicit “significant adaptation event” schema and retention contract | Add §26.11 audit event schema subsection |
| Low-confidence fallback behavior | Fail-closed exists generally; no explicit low-confidence branch | Missing | Need deterministic fallback when confidence < threshold | Add §26.9 confidence-gated fallback contract |

---

## D) Runtime/Execution Model (State Machine + Pipeline)

| PDL Runtime Concept | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Explicit adaptation state machine (Baseline → InferredIntent → Adapted → Stabilized) | Stage A/B/C contracts + boundary artifacts (§26.10) | Partial | Stage model exists, but not framed as UX adaptation state machine with transition invariants | Add informative mapping table from Stage A/B/C to UI adaptation states |
| Deterministic execution order per cycle | Strong coverage in §5 + §26.10 | Full | None | N/A |
| Conflict priority stack (safety > accessibility > user settings > pragmatic score > recency) | Accessibility precedence explicit; conflict arbitration explicit in pattern semantics (§26.3–§26.4) | Partial | No single canonical global precedence list combining all surfaces | Add §26.4.x “Global Arbitration Precedence” |
| Cooldown and anti-thrash controls | Some bounded controls in §26.8 but not explicit cooldown primitive | Partial | Missing explicit cooldown clock-free semantics | Add deterministic transition-count or event-window cooldown policy |

---

## E) Solver Semantics

| PDL Solver Requirement | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Hard vs soft constraint classes | Hard feasibility and constraints in Stage B + accessibility constitutional layer | Partial | Not presented as canonical two-class model across design adaptation surfaces | Add §26.10 formal hard/soft classification contract |
| Explicit objective function with stability term | Optimization semantics present but formula not explicit | Partial | Need a canonical objective form (or canonical equivalent) for conformance vectors | Add optional normative formula + deterministic tie-break fallback |
| Deterministic tie-break chain | Deterministic ordering appears in multiple clauses | Partial | Need one consolidated tie-break contract across solver outputs | Add §26.10 tie-break canonical order clause |
| Confidence-gated reweighting | Not explicit | Missing | Need formal mapping from confidence to weight adjustments with bounds | Add §26.9 + §26.10 integrated confidence weighting clause |
| Solver timeout fallback behavior | Fail-closed behavior present; timeout semantics not explicit | Partial | Need “time budget exceeded” deterministic fallback path | Add §26.10 timeout/fallback contract |

---

## F) Explanation, Telemetry, and Diagnostics

| PDL Requirement | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| User-facing explanation when adaptation changes behavior | Diagnostic model is strict (§24, §26.11) | Partial | Diagnostics are implementation/error surfaces; not user-facing explanation UX semantics | Add separate explanation payload contract in adaptive-plan outputs |
| “Why this changed” trace for last N adaptations | Decision traces exist but no UX-oriented exposure rule | Partial | Need deterministic trace subset for user-facing inspection | Add §26.11 trace projection for explanation consumers |
| Minimum telemetry schema for adaptation outcomes | Canonical diagnostics taxonomy exists (§26.11.6–.7) | Partial | No canonical adaptation outcome event schema with task/outcome measures | Add §26.11 event schema for adaptation telemetry |
| Distinguish normative error code from explanatory text | Already explicit in §26.11.7 | Full | None | N/A |

---

## G) Component/Renderer Contract Mapping

| PDL Engineering Mapping | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Component contract with semantic role + pragmatic context + policy | Foundry boundary and adaptive package semantics in §§22–23 | Partial | No normative component-level API/shape (likely intentionally out-of-scope) | Add informative profile in implementation guide (non-normative appendix) |
| Renderer capability profile (platform/input/accessibility profile) | Target profile identifiers in foundry contract (§22) | Partial | Need explicit capability facets if cross-foundry parity is required | Add §22.5 extension fields for deterministic capability declarations |
| Renderer solves constraints; semantics precomputed upstream | Strongly explicit in §§22–23 + §5.9.4 | Full | None | N/A |

---

## H) Governance and Ship Gate

| PDL Governance Check | Current Workshop Coverage | Status | Gap to Close | Suggested Normative Insertion |
|---|---|---|---|---|
| Rule owner + measurable hypothesis | Not explicit in spec | Missing | Governance metadata for adaptive rules is absent | Add conformance/governance metadata requirements (likely in §17 package manifests) |
| Fallback defined before enablement | Fail-closed exists; explicit pre-enable checklist not explicit | Partial | Need deployment gate obligations for adaptive rules | Add §26.11 conformance preflight checklist |
| Explanation copy approved + accessibility review | Accessibility is strong; approval workflow absent (likely process-level) | Partial | Decide whether approval workflow belongs in spec or governance docs | Add to governance docs first; keep spec limited to enforceable artifacts |
| Rollback switch exists | Not explicit | Missing | Need deterministic rollback/disable semantics for adaptive policy sets | Add §26.9 policy-set activation and rollback semantics |

---

## I) High-Value Gap Priorities (Recommended Order)

1. **Confidence as first-class normative object** (currently missing): fields, provenance, freshness, bounds, and low-confidence fallback.
2. **Adaptation delta/cooldown contract** (currently partial): explicit anti-thrash and bounded-change semantics.
3. **Global precedence stack** (currently partial): unify safety/accessibility/user override/policy scoring precedence.
4. **Explanation surface contract** (currently partial): separate user-facing explanation from diagnostics.
5. **Canonical adaptation telemetry schema** (currently partial): deterministic event contract for evaluation and audit.

---

## J) Suggested “Minimal Additions” Package (to align with PDL without destabilizing §26)

- Add one compact subsection in §26.9 defining:
  - `AdaptiveIntent` (canonical fields + typing)
  - `AdaptiveConfidence` (value/source/window + deterministic derivation constraints)
  - fallback rule when confidence is below threshold
- Add one compact subsection in §26.10 defining:
  - hard/soft class terminology
  - canonical arbitration precedence list
  - bounded delta + cooldown semantics
- Add one compact subsection in §26.11 defining:
  - user-facing explanation payload contract
  - adaptation telemetry event minimum schema
  - deterministic ordering and code linkage to existing diagnostics

This preserves existing architecture (strong) while making the PDL model author-visible and testable.
