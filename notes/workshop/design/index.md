Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Workshop Design Notes

This directory holds Workshop-level design modeling notes that sit above the core `gd` ontology.

Current artifacts:

1. `gd-metrics.ttl` - derived metrics vocabulary
2. `gd-metrics.shacl.ttl` - SHACL constraints for metrics graphs
3. `RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md` - deterministic adaptive projection model (human-first)
4. `DESIGN_POLICY_PRECEDENTS_1_0_0.md` - Knuth-Plass + Muller-Brockmann precedents translated into requirements
5. `COMPILER_MAPPING_SPEC_1_0_0.md` - deterministic compiler mapping contract from adaptive Codex artifacts to runtime requests
6. `STAGE_B_EVALUATION_1_0_0.md` - deterministic Stage B evaluation contract and vector semantics
7. `STAGE_C_PLAN_EMISSION_1_0_0.md` - deterministic Stage C foundry handoff plan emission contract
8. `compiler-mapping/index.md` - executable mapping fixtures and check runner
9. `codex/adaptive-context-profile.schema.cdx` - context taxonomy for adaptive evaluation inputs
10. `codex/adaptive-objective-profile.schema.cdx` - objective taxonomy for adaptive intent
11. `codex/adaptive-optimization-profile.schema.cdx` - cost-function and relaxation controls
12. `codex/adaptive-override-set.schema.cdx` - explicit human override constraints
13. `codex/adaptive-intent.schema.cdx` - binding model linking context + objectives + optimization + overrides + policy set + target
14. `codex/examples/adaptive-intent-article-homepage.example.cdx` - worked authoring example
