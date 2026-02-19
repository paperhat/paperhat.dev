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
14. `stage-b-vectors/*.cdx` - executable Stage B vectors
15. `stage-c-vectors/*.cdx` - executable Stage C vectors
16. `scripts/compile_adaptive_intent.py` - reference compiler
17. `scripts/emit_adaptive_plan.py` - Stage C plan emission reference
18. `scripts/run_stage_a_e2e_check.py` - compile -> Stage A vector -> evaluator assertion runner
19. `scripts/run_stage_a_e2e_checks.sh` - Stage A end-to-end check entrypoint
20. `scripts/run_stage_b_vectors.py` - Stage B vector evaluator
21. `scripts/run_stage_b_vectors.sh` - Stage B vector check entrypoint
22. `scripts/run_stage_c_vectors.py` - Stage C vector evaluator
23. `scripts/run_stage_c_vectors.sh` - Stage C vector check entrypoint
24. `scripts/run_compiler_mapping_checks.sh` - deterministic fixture + Stage A + Stage B + Stage C runner

Run checks:

```bash
notes/workshop/design/compiler-mapping/scripts/run_compiler_mapping_checks.sh
```
