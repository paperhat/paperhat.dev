Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Stage C Plan Emission 1.0.0

This document defines deterministic Stage C plan emission semantics for foundry handoff.

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

1. output MUST be `AdaptivePlanResult status="error"`
2. output MUST include `error="EVALUATION_ERROR"`
3. output MUST include `failedStage="stageA"` or `failedStage="stageB"`
4. `stageA` failure MUST take precedence over `stageB` failure

## 4. Success emission

If Stage A and Stage B are both `ok`, output MUST be:

1. `AdaptivePlanResult status="ok"`
2. include top-level identity fields from `CompiledAdaptiveRequest`:
   - `intentId`
   - `targetFoundry`
   - `policySetRef`
3. include plan scope:
   - `compositionIri` from `CompiledAdaptiveRequest/StageA`
   - optional `viewIri` when present
4. include Stage A outcome section:
   - ordered `SelectedActions`
   - ordered `Delta Remove/Add` triples
5. include Stage B outcome section:
   - `selectedCandidate`
   - `selectedScore`
   - ordered `AppliedRelaxation` entries

## 5. Determinism requirements

The emitter MUST preserve source order for:

1. selected actions
2. Stage A delta triples
3. Stage B applied relaxations

The emitter MUST NOT inject non-deterministic values (timestamps, random identifiers, host metadata).

## 6. Executable vectors

Executable vectors are defined in:

1. `notes/workshop/design/compiler-mapping/stage-c-vectors/*.cdx`

Run vectors using:

```bash
notes/workshop/design/compiler-mapping/scripts/run_stage_c_vectors.sh
```
