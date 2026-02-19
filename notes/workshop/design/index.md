Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Workshop Design Notes

This directory holds Workshop-level design modeling notes that sit above the core `wd` ontology.

Current artifacts:

1. `wd-metrics.ttl` - derived metrics vocabulary
2. `wd-metrics.shacl.ttl` - SHACL constraints for metrics graphs
3. `RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md` - deterministic adaptive projection model (human-first)
4. `DESIGN_POLICY_PRECEDENTS_1_0_0.md` - Knuth-Plass + Muller-Brockmann precedents translated into requirements
5. `COMPILER_MAPPING_SPEC_1_0_0.md` - deterministic compiler mapping contract from adaptive Codex artifacts to runtime requests
6. `STAGE_A_EVALUATION_1_0_0.md` - deterministic Stage A evaluation contract and output envelope
7. `STAGE_B_EVALUATION_1_0_0.md` - deterministic Stage B evaluation contract and vector semantics
8. `STAGE_C_PLAN_EMISSION_1_0_0.md` - deterministic Stage C foundry handoff plan emission contract
9. `compiler-mapping/index.md` - executable mapping fixtures and check runner
10. `codex/adaptive-context-profile.schema.cdx` - context taxonomy for adaptive evaluation inputs
11. `codex/adaptive-objective-profile.schema.cdx` - objective taxonomy for adaptive intent
12. `codex/adaptive-optimization-profile.schema.cdx` - cost-function and relaxation controls
13. `codex/adaptive-override-set.schema.cdx` - explicit human override constraints
14. `codex/adaptive-intent.schema.cdx` - binding model linking context + objectives + optimization + overrides + policy set + target
15. `codex/stage-a-result.schema.cdx` - Stage A result envelope schema
16. `codex/stage-b-result.schema.cdx` - Stage B result envelope schema
17. `codex/adaptive-plan-result.schema.cdx` - Stage C adaptive plan envelope schema
18. `codex/examples/adaptive-intent-article-homepage.example.cdx` - worked authoring example
