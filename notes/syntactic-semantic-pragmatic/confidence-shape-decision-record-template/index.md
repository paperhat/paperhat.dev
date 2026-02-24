# Confidence Shape Decision Record (Template)

## Purpose

Record and approve the canonical Workshop confidence-shape decision for §26 drafting.

This template is intentionally decision-first.

---

## 1) Decision Metadata

- **Decision ID**: `DEC-26-CONFIDENCE-SHAPE-____`
- **Date**: `YYYY-MM-DD`
- **Status**: `Proposed | Approved | Rejected | Superseded`
- **Scope**: `Workshop §26.9 / §26.10`
- **Owners**: `__________`
- **Reviewers**: `__________`
- **Related Notes**:
  - `paperhat.dev/notes/syntactic-semantic-pragmatic/index.md`
  - `paperhat.dev/notes/syntactic-semantic-pragmatic/pdl-workshop-mapping-matrix/index.md`

---

## 2) Problem Statement

We must define confidence as a first-class adaptive input without violating Workshop invariants:

- deterministic replay,
- fail-closed behavior,
- no ambient dependencies,
- canonical package/boundary contracts.

Open question: What is the canonical confidence shape and derivation model?

---

## 3) Non-Negotiable Constraints

Any approved option MUST satisfy all of the following:

1. Confidence is deterministic for identical explicit inputs.
2. No wall-clock dependency (no freshness-in-seconds semantics).
3. No implicit runtime/ambient history reads.
4. Foundry does not recompute confidence semantics.
5. Conformance vectors can test confidence behavior deterministically.
6. Freshness concern is addressed in deterministic form: confidence inputs MUST come from current declared inputs/canonical state for the current execution, not implicit carry-forward from prior executions.

---

## 4) Candidate Options

### Option A — Authored Scalar

- **Shape**: confidence is provided as a scalar field on adaptive intent.
- **Computation**: none (author-supplied only).
- **Pros**: simplest; lowest implementation risk.
- **Cons**: weak semantics; limited explainability of source/provenance.
- **Conformance impact**: low.

### Option B — Deterministic Function over Explicit Context Inputs

- **Shape**: confidence is computed from a closed, typed context key set.
- **Computation**: spec-defined deterministic function over spec-defined input keys (not author-configurable per deployment).
- **Pros**: useful confidence semantics while preserving determinism.
- **Cons**: requires normative signal set and function contract; changes may require spec revision.
- **Conformance impact**: medium.

### Option C — Declared Signal Weights + Deterministic Aggregation

- **Shape**: author declares signal sources and weights; pipeline computes composite confidence.
- **Computation**: spec-defined deterministic aggregation over author-declared, schema-validated signal inputs/weights.
- **Pros**: closest to PDL `confidence.source` model.
- **Cons**: highest schema and vector complexity.
- **Conformance impact**: high.

### Option D — Hybrid (A Base + C Optional Derivation)

- **Shape**: canonical boundary value is always a scalar confidence; authors may either supply scalar directly (A path) or declare signals+weights for deterministic derivation (C path).
- **Computation**: scalar passthrough or deterministic aggregation, normalized to one canonical scalar output.
- **Pros**: boundary simplicity with opt-in provenance/expressiveness.
- **Cons**: dual-path validation complexity.
- **Conflict rule**: if both direct scalar and derivation inputs are present, fail closed. Exactly one path must be declared per adaptive intent. Final diagnostic code must conform to §26/§24 taxonomy rules (likely `AdaptivePipeline::*` family).
- **Conformance impact**: medium-high.

---

## 5) Evaluation Matrix

Score each option 1–5 (5 = best). Rows with pre-filled values are expected invariants under the non-negotiable constraints.

| Criterion | A | B | C | D | Notes |
|---|---:|---:|---:|---:|---|
| Determinism assurance | 5 | 5 | 5 | 5 | Must be true for any admissible option.
| Conformance testability | 5 | 5 | 5 | 5 | Must be vector-testable or option is non-conformant.
| Boundary compatibility (§22/§23) | 5 | 5 | 5 | 5 | Pipeline computes scalar before package assembly; foundry consumes canonical scalar only in all options.
| Author usability |  |  |  |  |  |
| Explainability/provenance |  |  |  |  |  |
| Spec complexity |  |  |  |  |  |
| Implementation risk |  |  |  |  |  |
| Extensibility (post-1.0 evolution cost) |  |  |  |  |  |

---

## 6) Selected Option

- **Chosen Option**: `A | B | C | D`
- **Rationale (2–5 bullets)**:
  - `...`
  - `...`

- **Rejected Option Notes**:
  - `A:`
  - `B:`
  - `C:`
  - `D:`

---

## 7) Normative Drafting Targets (Post-Approval)

If approved, drafting MUST update:

1. `§26.9` — confidence field/shape and deterministic input contract.
2. `§26.10` — confidence interaction with fallback/reweighting semantics.
3. `§26.11` — diagnostics and conformance vectors for confidence failure modes.

Optional (if payload fields change):

4. `§20.10` adaptive-plan payload/package structure.
5. `§22`/`§23` interface expectations for confidence-derived payloads.

---

## 8) Test Vector Requirements

Minimum vectors to add:

1. Positive deterministic replay (`same inputs => same confidence`).
2. Missing required confidence inputs fails closed.
3. Invalid confidence shape/type fails closed.
4. Confidence fallback threshold behavior (if enabled).
5. Confidence-reweighting behavior (if enabled).
6. Freshness translation rule: confidence uses only current declared inputs/state (no implicit prior-run carry-forward).
7. Hybrid-only (if D selected): deterministic conflict handling when both direct scalar and derivation inputs are provided.

---

## 9) Approval

- **Approved by**: `__________`
- **Approval date**: `YYYY-MM-DD`
- **Effective in spec version**: `__________`
- **Follow-up ticket IDs**: `__________`
