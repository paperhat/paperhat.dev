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
6. `scripts/compile_adaptive_intent.py` - reference compiler
7. `scripts/run_stage_a_e2e_check.py` - compile -> Stage A vector -> evaluator assertion runner
8. `scripts/run_stage_a_e2e_checks.sh` - Stage A end-to-end check entrypoint
9. `scripts/run_compiler_mapping_checks.sh` - deterministic fixture + end-to-end check runner

Run checks:

```bash
notes/workshop/design/compiler-mapping/scripts/run_compiler_mapping_checks.sh
```
