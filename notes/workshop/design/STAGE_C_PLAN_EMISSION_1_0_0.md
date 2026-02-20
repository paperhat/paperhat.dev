Status: READY
Lock State: LOCKED
Version: 1.0.0

# Stage C Plan Emission 1.0.0

This document defines deterministic Stage C emission semantics for canonical foundry handoff and decision trace reporting.

## 1. Inputs

A conforming Stage C emitter MUST consume:

1. one compiled adaptive request (`CompiledAdaptiveRequest`)
2. one Stage A outcome (`StageAResult`)
3. one Stage B outcome (`StageBResult`)

## 2. Preconditions

Emission MUST terminate with `EVALUATION_ERROR` output if any condition below is true:

1. any input is malformed
2. `CompiledAdaptiveRequest` is missing `intentId`, `targetFoundry`, `policySetRef`, or `StageA.compositionIri`
3. `StageAResult.status` is not `ok` or `error`
4. `StageBResult.status` is not `ok` or `error`
5. `StageBResult.status=ok` and required fields are missing (`selectedCandidate`, `selectedScore`)

No partial output is allowed on precondition failure.

## 3. Error propagation

If Stage A or Stage B reports error status:

1. Stage C MUST NOT emit an `AdaptivePlanPackage`
2. Stage C MUST emit `AdaptiveDecisionReport status="error"`
3. output report MUST include `error="EVALUATION_ERROR"`
4. output report MUST include `failedStage="stageA"` or `failedStage="stageB"`
5. `stageA` failure MUST take precedence over `stageB` failure

## 4. Success emission

If Stage A and Stage B are both `ok`, output MUST be:

1. an `AdaptivePlanPackage` artifact:
   - includes package fields:
     - `workshopVersion`
     - `closureHash`
     - `adaptivePlanProjectionDefinitionClosureHash`
     - `contentHashAlgorithm` (fixed to `SHA-256`)
   - includes ordered `AdaptivePlanPayloadRecord` children with:
     - `projectionIdentifier`
     - `projectionDefinitionClosureHash`
     - `parameterHash`
     - `payloadContentHash`
     - `payloadCanonicalBytes`
2. an `AdaptiveDecisionReport status="ok"` artifact:
   - includes top-level identity fields from `CompiledAdaptiveRequest`:
     - `intentId`
     - `targetFoundry`
     - `policySetRef`
   - includes package linkage:
     - `adaptivePlanPackageContentHash`
   - includes plan scope:
     - `compositionIri` from `CompiledAdaptiveRequest/StageA`
     - optional `viewIri` when present
   - includes Stage A outcome section:
     - ordered `SelectedActions`
     - ordered `Delta Remove/Add` triples
   - includes Stage B outcome section:
     - `selectedCandidate`
     - `selectedScore`
     - ordered `AppliedRelaxation` entries

Every emitted `AdaptivePlanPackage` MUST validate against:

1. `notes/workshop/design/codex/adaptive-plan-package.schema.cdx`

Every emitted `AdaptiveDecisionReport` MUST validate against:

1. `notes/workshop/design/codex/adaptive-decision-report.schema.cdx`

`AdaptivePlanResult` is deprecated for Stage C handoff semantics and MUST NOT be used as the foundry semantic input artifact.

## 5. Determinism requirements

The emitter MUST preserve source order for:

1. selected actions
2. Stage A delta triples
3. Stage B applied relaxations
4. adaptive-plan payload records (ordered by `(projectionIdentifier, projectionDefinitionClosureHash, parameterHash)`)

The emitter MUST NOT inject non-deterministic values (timestamps, random identifiers, host metadata).

## 6. Executable vectors

Executable vectors are defined in:

1. `notes/workshop/design/compiler-mapping/stage-c-vectors/*.cdx`

Run vectors using:

```bash
notes/workshop/design/compiler-mapping/scripts/run_stage_c_vectors.sh
```
