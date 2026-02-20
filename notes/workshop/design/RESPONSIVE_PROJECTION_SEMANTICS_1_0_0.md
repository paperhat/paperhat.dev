Status: READY
Lock State: LOCKED
Version: 1.0.0

# Responsive Projection Semantics 1.0.0

Status:

- scope: Workshop design architecture specification
- maturity: publication-ready
- audience: human authors and implementers

## 1. Intent

`wd` started as graphic design modeling, but Workshop needs a broader contract:

1. many foundries (`web`, `app`, `pdf`, `book`, etc.)
2. dynamic targets (zoom, motion, interaction, state)
3. internationalization and cultural adaptation
4. deterministic, declarative behavior

This document defines that contract at a system level.

## 2. Core contract

Adaptive behavior in Workshop is:

1. declarative (rules and profiles, not imperative renderer code)
2. deterministic (same inputs -> same adaptive plan)
3. human-authored (AI may assist authoring only)
4. auditable (all decisions trace to explicit inputs and rules)

No autonomous "AI design" is assumed.

## 3. Precedent-driven model

Workshop adopts two explicit precedents:

1. Knuth-Plass: global optimization against a defined badness function is better than greedy local decisions.
2. Muller-Brockmann grid systems: proportional constraints are more stable across target changes than absolute placement.

Resulting architecture rule:

1. policy evaluation is deterministic and declarative
2. layout choice is evaluated globally (not greedy)
3. breakpoint behavior is derived from constraints/objectives, not hand-authored switches

## 4. End-to-end flow

1. Authoring
   - human writes Codex artifacts for:
     - context profile
     - objective profile
     - optimization profile
     - override set (optional)
     - policy set
     - target projection intent (must include `compositionRef`; may include `viewRef`)
2. Compilation
   - Codex is compiled to canonical RDF graph(s)
   - policy nodes map to `wd:Policy` / `wd:Condition` / `wd:Action`
3. Validation
   - Codex schema validation
   - SHACL validation (`wd-all.shacl.ttl`)
4. Stage A evaluation (hard policy semantics)
   - evaluate enabled `wd:Policy` against context
   - resolve action conflicts deterministically
5. Stage B evaluation (optimization semantics)
   - score candidate realizations against weighted badness terms
   - enforce hard constraints
   - if needed, apply deterministic relaxation policy
6. Plan emission
   - emit ordered adaptive plan plus score/explanation metadata
7. Foundry realization
   - foundry consumes the plan and renders target output
   - foundry internals may use local solvers, but cannot violate plan constraints

## 5. Determinism invariants

To keep adaptivity deterministic across implementations:

1. context keys and objective axes use controlled taxonomies
2. condition value types are explicit
3. ordering is explicit (priority, scope rank, stable lexical tie-breakers)
4. conflict strategy is explicit and uniform per scope
5. hard constraints are evaluated before soft objectives
6. soft objective aggregation mode is explicit
7. relaxation order is explicit and deterministic
8. failure mode is fail-closed (`EVALUATION_ERROR`)

## 6. Optimization semantics

Optimization in 1.0.0 is constrained by declarative profiles:

1. hard constraints
   - examples: no overlap, readable minimum text size, reduced-motion compliance
2. soft weighted terms
   - examples: proximity, contrast, readability, performance, density, localization fidelity
3. aggregation mode
   - weighted mean (`weightedSum`) in 1.0.0
4. satisfice threshold
   - target minimum score before accepting a plan
5. relaxation policy
   - deterministic rule for which low-priority terms may relax when no feasible plan exists

This follows the "least-bad valid layout" principle used by paragraph optimization systems.

## 7. Derived breakpoints and continuous adaptation

Workshop does not treat breakpoints as author-authored layout branches by default.

Instead:

1. profile constraints determine when a current layout family becomes infeasible
2. reflow is a re-optimization event
3. optional quantization bands can stabilize output for practical rendering

This keeps responsiveness tied to semantic constraints instead of fixed pixel breakpoints.

## 8. Override model

Professional overrides are first-class constraints, not imperative side channels.

Rules:

1. overrides are explicit artifacts
2. overrides are applied as additional hard constraints
3. solver re-optimizes with overrides in scope
4. every override must remain auditable in plan metadata

## 9. Context and objective taxonomies

Codex artifacts:

1. `codex-packages/spec/1.0.0/schemas/design-intent/adaptive-context-profile/schema.cdx`
2. `codex-packages/spec/1.0.0/schemas/design-intent/adaptive-objective-profile/schema.cdx`
3. `codex-packages/spec/1.0.0/schemas/design-policy/adaptive-optimization-profile/schema.cdx`
4. `codex-packages/spec/1.0.0/schemas/design-policy/adaptive-override-set/schema.cdx`
5. `codex-packages/spec/1.0.0/schemas/design-intent/adaptive-intent/schema.cdx`
6. `codex-packages/spec/1.0.0/schemas/assembly/stage-a-result/schema.cdx`
7. `codex-packages/spec/1.0.0/schemas/assembly/stage-b-result/schema.cdx`
8. `codex-packages/spec/1.0.0/schemas/assembly/adaptive-plan-result/schema.cdx`

Example authoring package:

1. `codex-packages/spec/1.0.0/schemas/design-intent/adaptive-intent/examples/default/example.cdx`

## 10. Cultural and individual adaptation model

Culture and preference are represented as explicit, typed signals:

1. language, region, script direction
2. motion/contrast/color preferences
3. input modality and device class
4. objective priorities (readability, accessibility, performance, brand expression, localization)

Because these are explicit profile fields, adaptation decisions are inspectable and repeatable.
