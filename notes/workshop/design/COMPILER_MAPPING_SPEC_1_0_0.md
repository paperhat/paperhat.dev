Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Compiler Mapping Spec 1.0.0

Status:

- scope: `1.0.0` internal compiler contract
- purpose: deterministic mapping from adaptive Codex authoring artifacts to executable evaluation requests
- failure mode: fail-closed

## 1. Input and output

Input (authoring layer):

1. `AdaptiveContextProfile`
2. `AdaptiveObjectiveProfile`
3. `AdaptiveOptimizationProfile`
4. `AdaptiveOverrideSet` (optional)
5. `AdaptiveIntent`

Output (runtime layer):

1. Stage A request (`gd:Policy` evaluator request)
2. Stage B request (optimization/override request)

The compiler output is a normalized Codex envelope.

## 2. Canonical output envelope

```cdx
<CompiledAdaptiveRequest intentId="IriRef" targetFoundry="web|app|pdf|epub|print" policySetRef="IriRef">
	<StageA compositionIri="IriRef" viewIri="IriRef">
		<ContextEntry key="ContextKeyIRI" type="integer|decimal|string|boolean" value="..." />
	</StageA>

	<StageB>
		<ContextExtEntry key="..." value="..." />
		<ObjectiveProfile profileId="..." primaryObjective="..." />
		<OptimizationProfile profileId="..." />
		<OverrideSet overrideSetId="..." />
	</StageB>
</CompiledAdaptiveRequest>
```

## 3. Normalization rules

The compiler MUST apply these rules:

1. token normalization:
   - enumerated token values are authored as `$token`
   - compiled value is `"token"` (leading `$` removed)
2. decimal quantization:
   - derived decimal values use scale 6 and round half-even
3. booleans:
   - preserve native boolean values only
4. sorting:
   - object keys sorted lexicographically in serialized output
   - list entries sorted by deterministic tuples (defined below)

## 4. Stage A mapping (`gd` policy evaluator)

`gd` context key mapping:

1. `viewportWidthPx` -> `https://paperhat.dev/ns/gd#ViewportWidthPx` as `integer`
2. `viewportHeightPx` -> `https://paperhat.dev/ns/gd#ViewportHeightPx` as `integer`
3. `deviceClass` -> `https://paperhat.dev/ns/gd#DeviceClass` as `string`
4. `motionPreference` -> `https://paperhat.dev/ns/gd#ReducedMotionPreference` as `boolean`
   - `$reduce` -> `true`
   - `$noPreference` -> `false`

Derived keys:

1. `ViewportAspectRatio`:
   - if width and height exist and `height > 0`
   - value = `width / height` quantized to 6 decimals
2. `ViewportOrientation`:
   - `"portrait"` if `height > width`
   - `"landscape"` if `width > height`
   - `"square"` if equal

Intent fields:

1. `AdaptiveIntent.compositionRef` -> `stage_a.composition_iri`
2. `AdaptiveIntent.viewRef` -> `stage_a.view_iri` (nullable)

## 5. Stage B mapping (optimization/override evaluator)

`context_ext` includes normalized context profile traits not consumed by Stage A:

1. `zoomLevel`
2. `inputModality`
3. `contrastPreference`
4. `colorSchemePreference`
5. `language`
6. `region`
7. `scriptDirection`
8. `networkClass`
9. `interactionMode`

### 5.1 Objective profile mapping

Direct token fields are normalized and copied.

Priority token -> numeric weight mapping:

1. `must` -> `1.0`
2. `prefer` -> `0.7`
3. `neutral` -> `0.4`

Compiled field:

1. `objective_profile.priority_weights`

### 5.2 Optimization profile mapping

Profile fields:

1. `solverMode`
2. `quantizationMode`
3. `reflowMode`
4. `satisficeThreshold`
5. `relaxationStrategy`

`OptimizationHardConstraint` compilation:

1. fields: `constraintKey`, `constraintScope`, `targetRef`, `constraintValue`
2. sort tuple: `(constraintKey, constraintScope, targetRef, constraintValue)`

`OptimizationSoftTerm` compilation:

1. fields: `termKey`, `weightClass`, `termScope`, `targetRef`, `minimumSatisfaction`
2. derived `weight`:
   - `critical=1.0`
   - `high=0.75`
   - `medium=0.5`
   - `low=0.25`
3. sort tuple: `(termKey, termScope, targetRef, weightClass)`

`RelaxationRule` compilation:

1. fields: `relaxOrder`, `relaxWeightClass`, `relaxationAction`
2. sort tuple: `(relaxOrder, relaxWeightClass, relaxationAction)`

### 5.3 Override set mapping

`AdaptiveOverrideSet`:

1. compile `overrideMode`
2. compile child `OverrideConstraint[]`

Constraint fields:

1. `overrideKind`
2. `targetRef`
3. `targetProperty`
4. `overrideValue`
5. `overridePriority`
6. `expiresAt`

Derived `priority_rank`:

1. `critical=4`
2. `high=3`
3. `medium=2`
4. `low=1`

Sort tuple:

1. descending `priority_rank`
2. `targetRef`
3. `overrideKind`

## 6. Stage C mapping (plan emission)

Stage C emits the foundry handoff envelope from:

1. one `CompiledAdaptiveRequest`
2. one `StageAResult`
3. one `StageBResult`

Success output:

1. root `AdaptivePlanResult status="ok"`
2. copy:
   - `intentId`
   - `targetFoundry`
   - `policySetRef`
3. emit plan scope:
   - `compositionIri` from `CompiledAdaptiveRequest/StageA`
   - `viewIri` when present
4. emit Stage A outcome:
   - ordered `SelectedActions`
   - ordered `Delta Remove/Add` triples
5. emit Stage B outcome:
   - `selectedCandidate`
   - `selectedScore`
   - ordered `AppliedRelaxation`

Error propagation:

1. if `StageAResult.status=error`, emit:
   - `AdaptivePlanResult status="error" error="EVALUATION_ERROR" failedStage="stageA"`
2. else if `StageBResult.status=error`, emit:
   - `AdaptivePlanResult status="error" error="EVALUATION_ERROR" failedStage="stageB"`
3. no success output is allowed when either upstream stage reports error

## 7. Compiler errors

Compilation MUST fail if:

1. any required concept is missing (`AdaptiveIntent`, context/objective/optimization profile)
2. `AdaptiveIntent` is missing required refs (`intentId`, `compositionRef`, `policySetRef`, `targetFoundry`)
3. `viewportHeightPx <= 0` when aspect ratio derivation is attempted
4. unknown priority token is supplied for objective or override weight mapping
5. unknown relaxation or weight class token is supplied where required

No partial output is allowed on compile failure.

## 8. Executable reference

Reference files:

1. input fixture:
   - `compiler-mapping/fixtures/adaptive-intent-article-homepage.input.cdx`
2. expected compiled output:
   - `compiler-mapping/fixtures/adaptive-intent-article-homepage.compiled.cdx`
3. Stage A end-to-end fixture:
   - `compiler-mapping/fixtures/adaptive-intent-stage-a-e2e.input.cdx`
4. Stage A end-to-end expectation:
   - `compiler-mapping/fixtures/adaptive-intent-stage-a-e2e.expect.cdx`
5. Stage B fixture (allow group split):
   - `compiler-mapping/fixtures/adaptive-intent-stage-b-allow-group-split.compiled.cdx`
6. Stage B fixture (widen threshold):
   - `compiler-mapping/fixtures/adaptive-intent-stage-b-widen-threshold.compiled.cdx`
7. Stage B malformed fixture:
   - `compiler-mapping/fixtures/adaptive-intent-stage-b-malformed.compiled.cdx`
8. Stage C Stage A result fixture:
   - `compiler-mapping/fixtures/stage-a-result-empty-ok.cdx`
9. Stage C Stage B result fixture (ok):
   - `compiler-mapping/fixtures/stage-b-result-widen-threshold-ok.cdx`
10. Stage C Stage B result fixture (error):
    - `compiler-mapping/fixtures/stage-b-result-error.cdx`
11. Stage C expected plan fixture (ok):
    - `compiler-mapping/fixtures/adaptive-plan-widen-threshold.expect.cdx`
12. Stage C expected plan fixture (error):
    - `compiler-mapping/fixtures/adaptive-plan-error-stage-b.expect.cdx`
13. Stage B vectors:
   - `compiler-mapping/stage-b-vectors/*.cdx`
14. Stage C vectors:
    - `compiler-mapping/stage-c-vectors/*.cdx`
15. compiler script:
   - `compiler-mapping/scripts/compile_adaptive_intent.py`
16. Stage C emitter script:
    - `compiler-mapping/scripts/emit_adaptive_plan.py`
17. Stage A end-to-end runner:
   - `compiler-mapping/scripts/run_stage_a_e2e_checks.sh`
18. Stage B vector runner:
   - `compiler-mapping/scripts/run_stage_b_vectors.sh`
19. Stage C vector runner:
    - `compiler-mapping/scripts/run_stage_c_vectors.sh`
20. check runner:
   - `compiler-mapping/scripts/run_compiler_mapping_checks.sh`
