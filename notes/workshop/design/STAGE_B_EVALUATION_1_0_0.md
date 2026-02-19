Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Stage B Evaluation 1.0.0

This document defines deterministic Stage B evaluation semantics for adaptive optimization and overrides.

## 1. Inputs

A conforming Stage B evaluator MUST consume:

1. one compiled adaptive request (`CompiledAdaptiveRequest`)
2. one candidate set

The candidate set MUST include explicit outcomes for:

1. hard constraints
2. soft term scores
3. override constraints

## 2. Preconditions

Evaluation MUST terminate with `EVALUATION_ERROR` if any condition below is true:

1. compiled request is malformed
2. candidate set is empty
3. a required hard constraint result is missing for any candidate
4. a required soft term score is missing for any candidate
5. a required strict override result is missing for any candidate
6. a soft term score is outside `[0, 1]`
7. a required numeric value cannot be parsed as decimal

No partial output is allowed on error.

## 3. Hard feasibility

A candidate is hard-feasible iff:

1. every required hard constraint result is `satisfied=true`
2. when override mode is `strict`, every override result is `satisfied=true`

Candidates that are not hard-feasible MUST be excluded before soft scoring.

If no hard-feasible candidates remain, result MUST be `EVALUATION_ERROR`.

## 4. Soft scoring

Stage B MUST compute weighted mean score over active soft terms:

1. `score = sum(weight * termScore) / sum(weight)`
2. weights MUST be positive decimals
3. score comparison MUST use decimal arithmetic

Deterministic tie-break order for equal scores:

1. candidate ID ascending (Unicode scalar order)

## 5. Satisficing and relaxation

If `satisficeThreshold` is defined:

1. only candidates with `score >= satisficeThreshold` are eligible
2. if no eligible candidates exist, evaluator MUST apply relaxation rules in deterministic order

Relaxation rules MUST be applied by ascending `relaxOrder`.

Supported actions in 1.0.0:

1. `dropTerm`:
   - remove active soft terms whose `weightClass == relaxWeightClass`
2. `widenThreshold`:
   - reduce threshold by `0.1`, floor at `0.0`
3. `allowGroupSplit`:
   - remove hard constraint key `preserveGroupCohesion` from active hard constraints

If all relaxation rules are exhausted and no candidate qualifies, result MUST be `EVALUATION_ERROR`.

## 6. Output

Successful evaluation MUST return:

1. `status=ok`
2. `selectedCandidate`
3. final `selectedScore`
4. ordered list of `appliedRelaxations`

Failure MUST return:

1. `status=error`
2. `error=EVALUATION_ERROR`

## 7. Executable vectors

Executable vectors are defined in:

1. `notes/workshop/design/compiler-mapping/stage-b-vectors/*.cdx`

Run vectors using:

```bash
notes/workshop/design/compiler-mapping/scripts/run_stage_b_vectors.sh
```
