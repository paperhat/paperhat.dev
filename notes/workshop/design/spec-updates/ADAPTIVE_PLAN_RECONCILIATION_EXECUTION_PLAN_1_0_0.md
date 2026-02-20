Status: READY
Lock State: LOCKED
Version: 1.0.0

# Adaptive Plan Reconciliation Execution Plan 1.0.0

## 0. Execution State (2026-02-20)

Decision state:

1. terminology is fixed: `AdaptiveDecisionReport` is the only report term
2. `AdaptivePlanPackage` is fixed as the sole foundry semantic input artifact
3. `AdaptivePlanResult` is deprecated for foundry handoff semantics

Workstream state:

1. Workstream A: COMPLETE in paperhat.dev notes and schema staging artifacts
2. Workstream B: COMPLETE
3. Workstream C: COMPLETE
4. Workstream D: PENDING (transfer gate)

This document is now decision-resolved. Remaining items are execution tasks, not open architectural decisions.
Four previously identified external audit issues remain deferred outside Workstreams A-C and are still pending follow-up.

## 1. Objective

Resolve the current contract split between:

1. current Workshop core specification text (`§20.10`, `§22`, `§23`, `§25`)
2. newer adaptive-plan/report semantics in paperhat.dev design notes and compiler-mapping artifacts

Authority policy for this plan:

1. correctness, determinism, and completeness decide the winning model
2. when paperhat.dev design content is better/newer, Workshop spec is updated to match it
3. current Workshop text has no precedence merely because it is already in the spec

Outcome: one unambiguous model where the canonical adaptive-plan package is the only foundry semantic input, and Stage A/B/C internals are represented as a separate execution report artifact.

## 2. Architectural Decision (Fixed)

The better specification model is:

1. `AdaptivePlanPackage` (canonical package) is the only artifact called "adaptive plan".
2. Stage C emits a separate report artifact for decision traceability.
3. Foundries consume package bytes only, never the decision report.

This plan executes that decision and then updates Workshop to the reconciled model.

## 3. Terminology Contract

The following names are authoritative after reconciliation:

1. `AdaptivePlanPackage`
2. `AdaptivePlanPayloadRecord`
3. `AdaptiveDecisionReport`
4. `StageAResult` and `StageBResult` as internal stage outputs, not foundry input artifacts

Deprecated terms to remove from normative usage:

1. "AdaptivePlanResult" when used to mean foundry handoff
2. any sentence implying Stage C report == adaptive plan

## 4. Scope

In scope:

1. design notes/spec text in paperhat.dev
2. Codex schemas used by compiler-mapping vectors
3. compiler-mapping fixtures, vectors, and scripts
4. conformance expectations and deterministic checks
5. follow-up transfer into Workshop repo after current external Workshop editing pass is complete

Out of scope:

1. changing Codex language semantics
2. changing Behavior semantics
3. changing foundry implementation internals outside interface contract alignment

## 5. Workstream A: Paperhat.dev Authoritative Drafting and Validation

Status: COMPLETE

All changes in this workstream stay in paperhat.dev first because paperhat.dev is the active design-authoring source during this reconciliation window.

### A1. Update normative design notes

Status: COMPLETE

Update:

1. `notes/workshop/design/STAGE_C_PLAN_EMISSION_1_0_0.md`
2. `notes/workshop/design/COMPILER_MAPPING_SPEC_1_0_0.md`
3. `notes/workshop/design/RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md`
4. `notes/workshop/design/index.md`

Required text outcomes:

1. Stage C success emits canonical package plus decision report.
2. Error propagation remains deterministic and fail-closed.
3. decision report is explicitly non-authoritative for foundry semantics.
4. foundry handoff points only to package artifact.

### A2. Rename/replace Stage C output schema

Status: COMPLETE

Current schema to retire from handoff semantics:

1. `notes/workshop/design/codex/adaptive-plan-result.schema.cdx`

Create replacement schema for report semantics:

1. `notes/workshop/design/codex/adaptive-decision-report.schema.cdx`

Schema requirements:

1. report carries stage status, selected actions, deltas, candidate/score/relaxation trace
2. report includes explicit linkage to package hash and/or package identity fields
3. report does not define package payload bytes

### A3. Keep Stage A/B schemas as stage artifacts

Status: COMPLETE

Review and tighten:

1. `notes/workshop/design/codex/stage-a-result.schema.cdx`
2. `notes/workshop/design/codex/stage-b-result.schema.cdx`

Required outcome:

1. no wording that implies these are foundry semantic inputs

### A4. Add/align canonical package schema artifact in paperhat.dev staging set

Status: COMPLETE

Add schema representing package contract for the reconciled model; update Workshop `§20.10` to match this model during transfer.

Suggested path:

1. `notes/workshop/design/codex/adaptive-plan-package.schema.cdx`

Required fields to encode:

1. workshopVersion
2. closureHash
3. adaptivePlanProjectionDefinitionClosureHash
4. contentHashAlgorithm
5. ordered payload records
6. payload uniqueness and hash validation constraints where expressible

## 6. Workstream B: Fixtures and Vectors

Status: COMPLETE

### B1. Replace Stage C fixture contract

Status: COMPLETE

Current fixture family that assumes plan == report must be split:

1. package fixtures (canonical package bytes and hashes)
2. decision-report fixtures

Update paths under:

1. `notes/workshop/design/compiler-mapping/fixtures/`
2. `notes/workshop/design/compiler-mapping/stage-c-vectors/`
3. `notes/workshop/design/compiler-mapping/pipeline-vectors/`

### B2. Update vector semantics

Status: COMPLETE

Stage C and pipeline vectors must assert:

1. package emission correctness and determinism
2. report emission correctness and determinism
3. explicit package/report linkage integrity

### B3. Remove ambiguous expected outputs

Status: COMPLETE

Retire expected fixtures that encode report-only as adaptive plan handoff.

## 7. Workstream C: Script and Validator Refactor

Status: COMPLETE

### C1. Stage C emitter and orchestration scripts

Status: COMPLETE

Refactor:

1. `notes/workshop/design/compiler-mapping/scripts/emit_adaptive_plan.py`
2. `notes/workshop/design/compiler-mapping/scripts/run_stage_c_vectors.py`
3. `notes/workshop/design/compiler-mapping/scripts/run_adaptive_pipeline_e2e_check.py`

Required behavior:

1. emit package artifact
2. emit decision report artifact
3. validate each against its schema
4. enforce deterministic ordering and no ambient data injection

### C2. Output schema validator updates

Status: COMPLETE

Update:

1. `notes/workshop/design/compiler-mapping/scripts/validate_output_schema.py`
2. `notes/workshop/design/compiler-mapping/scripts/run_output_schema_checks.py`

Required checks:

1. package schema conformance
2. decision report schema conformance
3. package/report linkage conformance

### C3. Aggregate check runner updates

Status: COMPLETE

Update:

1. `notes/workshop/design/compiler-mapping/scripts/run_compiler_mapping_checks.sh`

Runner must fail if any package/report deterministic comparison fails.

## 8. Workstream D: Workshop Spec Update Transfer Plan (Deferred Until Active Workshop Edit Window Closes)

Status: PENDING

After current Workshop editing activity reaches a safe sync point, port the reconciled contract into Workshop and replace conflicting older wording.

Target files in Workshop:

1. `spec/1.0.0/index.md` (`§20`, `§22`, `§23`, `§24`, `§25` normative updates as required for full semantic alignment)
2. `spec/1.0.0/schemas/view/semantic-projection/*` only if schema surface changes are required
3. `tools/*` and tests where artifact assumptions must be updated

Transfer rule:

1. no mixed terminology survives ("AdaptivePlanResult" as handoff must not remain)
2. no conflicting Workshop normative text survives once reconciliation is transferred

## 9. Conformance and Determinism Gate

Reconciliation is complete only if all checks below pass:

1. package canonical bytes are deterministic for identical inputs
2. package content hash checks pass
3. payload record ordering and uniqueness checks pass
4. decision report bytes are deterministic for identical inputs
5. Stage A/B/C and pipeline vectors all pass with updated semantics
6. foundry input contract tests assert package-only semantic input
7. no normative text still equates decision report with adaptive plan

## 10. Cleanup Rules

Before marking reconciliation COMPLETE:

1. remove obsolete fixtures/scripts/schemas that preserve old plan==report semantics
2. remove stale references in index files and note cross-links
3. remove dead compatibility wording

No dual-contract coexistence is allowed in the final state.

## 11. Execution Sequence

Implement in this exact dependency order:

1. terminology freeze and note updates (A1)
2. schema split and additions (A2, A4, A3)
3. fixture/vector migration (B1, B2, B3)
4. script/validator refactor (C1, C2, C3)
5. conformance gate run and cleanup (Sections 9 and 10)
6. controlled transfer into Workshop repo (Workstream D)

## 12. Deliverables

Required deliverables from this plan:

1. updated Stage C and mapping notes in paperhat.dev
2. package schema + decision report schema
3. migrated fixtures/vectors
4. updated script/tooling path and schema checks
5. explicit transfer checklist for Workshop adoption

Current completion snapshot:

1. deliverables (1) and (2): COMPLETE
2. deliverables (3) and (4): COMPLETE
3. deliverable (5): PENDING

**End of Adaptive Plan Reconciliation Execution Plan v1.0.0**
