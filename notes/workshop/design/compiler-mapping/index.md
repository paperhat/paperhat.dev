Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Compiler Mapping

This directory contains the executable reference package for adaptive compiler mapping 1.0.0.

Artifacts:

1. `../COMPILER_MAPPING_SPEC_1_0_0.md` - normative mapping rules
2. `fixtures/adaptive-intent-article-homepage.input.cdx` - source fixture
3. `fixtures/adaptive-intent-article-homepage.compiled.cdx` - expected compiled output
4. `fixtures/adaptive-intent-stage-a-e2e.input.cdx` - Stage A end-to-end fixture source
5. `fixtures/adaptive-intent-stage-a-e2e.expect.cdx` - expected Stage A evaluator assertion
6. `fixtures/adaptive-intent-stage-b-allow-group-split.compiled.cdx` - Stage B fixture for allow-group-split relaxation
7. `fixtures/adaptive-intent-stage-b-widen-threshold.compiled.cdx` - Stage B fixture for widen-threshold relaxation
8. `fixtures/adaptive-intent-stage-b-malformed.compiled.cdx` - malformed Stage B fixture for evaluator precondition coverage
9. `fixtures/stage-a-result-empty-ok.cdx` - Stage C Stage A result fixture (success)
10. `fixtures/stage-b-result-widen-threshold-ok.cdx` - Stage C Stage B result fixture (success)
11. `fixtures/stage-b-result-error.cdx` - Stage C Stage B result fixture (error)
12. `fixtures/adaptive-plan-widen-threshold.expect.cdx` - expected Stage C emitted plan (success)
13. `fixtures/adaptive-plan-error-stage-b.expect.cdx` - expected Stage C emitted plan (error)
14. `fixtures/stage-b-candidates-stage-a-e2e.cdx` - Stage B candidates fixture for compile -> Stage A -> Stage B -> Stage C e2e
15. `fixtures/stage-a-result-stage-a-e2e.expect.cdx` - expected emitted Stage A result for e2e
16. `fixtures/stage-b-result-stage-a-e2e.expect.cdx` - expected emitted Stage B result for e2e
17. `fixtures/adaptive-plan-stage-a-e2e.expect.cdx` - expected emitted adaptive plan for e2e
18. `fixtures/adaptive-intent-stage-a-error.input.cdx` - Stage A error-propagation fixture source
19. `fixtures/stage-b-candidates-stage-a-error.cdx` - Stage B candidates fixture for Stage A error-propagation e2e
20. `fixtures/stage-b-candidates-malformed.cdx` - malformed Stage B candidates fixture for fail-closed propagation
21. `fixtures/stage-a-result-stage-a-error.expect.cdx` - expected emitted Stage A error result for e2e
22. `fixtures/stage-b-result-stage-a-error.expect.cdx` - expected emitted Stage B result for Stage A error-propagation e2e
23. `fixtures/adaptive-plan-error-stage-a.expect.cdx` - expected emitted adaptive plan for Stage A error propagation
24. `stage-b-vectors/*.cdx` - executable Stage B vectors
25. `stage-c-vectors/*.cdx` - executable Stage C vectors
26. `pipeline-vectors/*.cdx` - executable compile -> Stage A -> Stage B -> Stage C vectors
27. `scripts/compile_adaptive_intent.py` - reference compiler
28. `scripts/evaluate_stage_a.py` - Stage A evaluator and StageAResult emitter
29. `scripts/evaluate_stage_b.py` - Stage B evaluator and StageBResult emitter
30. `scripts/emit_adaptive_plan.py` - Stage C plan emission reference
31. `scripts/validate_output_schema.py` - output envelope schema validator
32. `scripts/run_output_schema_checks.py` - validates Stage A/B/Plan output fixtures against Codex schemas
33. `scripts/run_output_schema_checks.sh` - output schema check entrypoint
34. `scripts/run_stage_a_e2e_check.py` - compile -> Stage A vector -> evaluator assertion runner
35. `scripts/run_stage_a_e2e_checks.sh` - Stage A end-to-end check entrypoint
36. `scripts/run_stage_b_vectors.py` - Stage B vector evaluator
37. `scripts/run_stage_b_vectors.sh` - Stage B vector check entrypoint
38. `scripts/run_stage_c_vectors.py` - Stage C vector evaluator
39. `scripts/run_stage_c_vectors.sh` - Stage C vector check entrypoint
40. `scripts/run_adaptive_pipeline_e2e_check.py` - compile -> Stage A -> Stage B -> Stage C e2e vector runner
41. `scripts/run_adaptive_pipeline_e2e_checks.sh` - compile -> Stage A -> Stage B -> Stage C e2e check entrypoint
42. `scripts/run_compiler_mapping_checks.sh` - deterministic fixture + output schemas + Stage A + Stage B + Stage C + pipeline e2e runner

Run checks:

```bash
notes/workshop/design/compiler-mapping/scripts/run_compiler_mapping_checks.sh
```
