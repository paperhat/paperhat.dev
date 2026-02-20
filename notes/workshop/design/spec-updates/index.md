Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Workshop Design Spec Updates Index

This folder contains execution plans for Workshop design-spec consolidation and contract reconciliation.

Policy alignment for this folder:

1. during this drafting window, paperhat.dev design material is the active source for design corrections
2. when paperhat.dev content is better/newer, Workshop specification text is updated to match it
3. final state remains Workshop spec as normative, deterministic, sole source of truth

## Plans

1. `ADAPTIVE_PLAN_RECONCILIATION_EXECUTION_PLAN_1_0_0.md`
2. `WORKSHOP_DESIGN_NORMATIVE_SPEC_EXPANSION_PLAN_1_0_0.md`
3. `WORKSHOP_STRUCTURAL_CHECK_FAMILY_COVERAGE_PLAN_1_0_0.md`
4. `WORKSHOP_TTL_SHACL_MIGRATION_PLAN_1_0_0.md`
5. `WORKSHOP_DESIGN_PATH_REWRITE_PLAN_1_0_0.md`

Issue coverage note:

1. Issue 3 (family/package reality mismatch) is fixed by mandatory steps in `WORKSHOP_DESIGN_NORMATIVE_SPEC_EXPANSION_PLAN_1_0_0.md` section `7`.
2. Issue 4 (structural checker family coverage gap) is fixed by `WORKSHOP_STRUCTURAL_CHECK_FAMILY_COVERAGE_PLAN_1_0_0.md`.
3. Issue 5 (TTL/SHACL migration with explicit target layout) is fixed by `WORKSHOP_TTL_SHACL_MIGRATION_PLAN_1_0_0.md`.
4. Issue 6 (hardcoded legacy design-note paths in scripts/vectors/coverage) is fixed by `WORKSHOP_DESIGN_PATH_REWRITE_PLAN_1_0_0.md`.
5. Issue 7 (Codex design schemas not package-structured and missing family assignment decisions) is fixed by staged packages under `notes/workshop/design/codex-packages/spec/1.0.0/schemas/` and `notes/workshop/design/codex-packages/FAMILY_ASSIGNMENTS_1_0_0.md`.

## Recommended Execution Order

1. Execute adaptive-plan/report contract reconciliation plan.
2. Execute normative design section expansion plan.
3. Execute structural-check family coverage plan.
4. Execute TTL/SHACL migration plan.
5. Execute design path rewrite plan.
6. Transfer reconciled content into Workshop repo after current Workshop editing window reaches a safe merge point.

**End of Workshop Design Spec Updates Index v1.0.0**
