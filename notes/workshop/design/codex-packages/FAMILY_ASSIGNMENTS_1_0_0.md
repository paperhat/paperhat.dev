Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Codex Design Schema Family Assignments 1.0.0

This document resolves family assignment decisions for normalized Codex design schemas prior to Workshop adoption.

## Assignment table

| Source schema | Assigned family | Package name | Staged package path |
|---|---|---|---|
| `adaptive-context-profile.schema.cdx` | `design-intent` | `workshop-design-intent-adaptive-context-profile` | `spec/1.0.0/schemas/design-intent/adaptive-context-profile/` |
| `adaptive-objective-profile.schema.cdx` | `design-intent` | `workshop-design-intent-adaptive-objective-profile` | `spec/1.0.0/schemas/design-intent/adaptive-objective-profile/` |
| `adaptive-intent.schema.cdx` | `design-intent` | `workshop-design-intent-adaptive-intent` | `spec/1.0.0/schemas/design-intent/adaptive-intent/` |
| `adaptive-optimization-profile.schema.cdx` | `design-policy` | `workshop-design-policy-adaptive-optimization-profile` | `spec/1.0.0/schemas/design-policy/adaptive-optimization-profile/` |
| `adaptive-override-set.schema.cdx` | `design-policy` | `workshop-design-policy-adaptive-override-set` | `spec/1.0.0/schemas/design-policy/adaptive-override-set/` |
| `stage-a-result.schema.cdx` | `assembly` | `workshop-assembly-stage-a-result` | `spec/1.0.0/schemas/assembly/stage-a-result/` |
| `stage-b-result.schema.cdx` | `assembly` | `workshop-assembly-stage-b-result` | `spec/1.0.0/schemas/assembly/stage-b-result/` |
| `adaptive-plan-result.schema.cdx` | `assembly` | `workshop-assembly-adaptive-plan-result` | `spec/1.0.0/schemas/assembly/adaptive-plan-result/` |

## Rationale

1. `design-intent` receives authoring artifacts that declare adaptation intent and objective posture (`AdaptiveContextProfile`, `AdaptiveObjectiveProfile`, `AdaptiveIntent`).
2. `design-policy` receives deterministic constraint/optimization policy artifacts (`AdaptiveOptimizationProfile`, `AdaptiveOverrideSet`).
3. `assembly` receives stage output envelope artifacts for deterministic internal stage exchange (`StageAResult`, `StageBResult`); `AdaptivePlanResult` is retained only as a legacy transitional schema during contract migration.

## Normalization rules applied

1. Package structure normalized to Workshop schema package contract shape:
   - `manifest.cdx`
   - `schema.cdx`
   - `README.md`
   - `localizations/en.cdx`
   - `examples/default/example.cdx`
   - `templates/basic/template.cdx`
2. In staged package `schema.cdx` copies, schema ID prefix is normalized to the assigned family namespace:
   - `codex:design-intent:*`
   - `codex:design-policy:*`
   - `codex:assembly:*`
3. Source files under `notes/workshop/design/codex/` are retained as legacy staging inputs until Workshop transfer is executed.
4. Canonical Stage C handoff semantics are now split in `notes/workshop/design/codex/` as:
   - `adaptive-plan-package.schema.cdx` (foundry semantic input)
   - `adaptive-decision-report.schema.cdx` (decision trace, non-authoritative)
