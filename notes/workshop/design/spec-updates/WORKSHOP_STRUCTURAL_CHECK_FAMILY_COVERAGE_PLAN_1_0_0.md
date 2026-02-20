Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Workshop Structural Check Family Coverage Plan 1.0.0

## 1. Objective

Fix Issue 4 by updating Workshop structural validation tooling so it supports all declared package families and performs completeness checks for `design-policy`, `design-intent`, and `assembly`.

Target state:

1. `tools/structural_check.py` accepts all nine package families declared by Workshop spec.
2. structural checks discover and validate design-family packages with the same rigor as existing schema families.
3. test coverage proves acceptance and rejection behavior for the full family set.

## 2. Authority Policy

Policy for this plan:

1. paperhat.dev design content is the active drafting source during the current correction window
2. Workshop tooling and specification are updated to the better reconciled model; existing code has no precedence by age
3. final merged state remains Workshop spec + Workshop tooling as normative, deterministic implementation authority

## 3. Confirmed Defect

Current `tools/structural_check.py` behavior is incomplete:

1. `VALID_PACKAGE_FAMILIES` only allows `{domain, behavior, view, system, meta, vocabulary}`
2. no discovery paths exist for `schemas/design-policy/`, `schemas/design-intent/`, `schemas/assembly/`
3. no completeness checks run for packages in those families
4. no manifest-root contract checks run for `DesignPolicyPackageManifest`, `DesignIntentPackageManifest`, `AssemblyPackageManifest`
5. tests do not cover acceptance of those family tokens or family-specific completeness behavior

## 4. Fixed Recommendation

Use strict family parity in tooling:

1. every family declared in Workshop `§18`/`§19` must be accepted by repository manifest validation
2. every declared schema family must have package discovery + completeness + manifest-root checks
3. tooling must fail deterministically when any declared family support is missing

No partial support is allowed.

## 5. Workstream A: Tooling Changes (`tools/structural_check.py`)

### A1. Family Constants and Discovery

Add family roots:

1. `DESIGN_POLICY_DIR = SCHEMA_ROOT / "design-policy"`
2. `DESIGN_INTENT_DIR = SCHEMA_ROOT / "design-intent"`
3. `ASSEMBLY_DIR = SCHEMA_ROOT / "assembly"`

Add discovery functions:

1. `discover_design_policy_packages(...)`
2. `discover_design_intent_packages(...)`
3. `discover_assembly_packages(...)`

Each discovery function must use deterministic sorted traversal consistent with existing family discovery behavior.

### A2. Valid Package Families

Expand `VALID_PACKAGE_FAMILIES` to the full set:

1. `domain`
2. `view`
3. `design-policy`
4. `design-intent`
5. `assembly`
6. `behavior`
7. `system`
8. `vocabulary`
9. `meta`

### A3. Design-Family Completeness Rules

Add completeness checks for the three design families.

Minimum required package files:

1. `manifest.cdx`
2. `schema.cdx`
3. `README.md`
4. `localizations/en.cdx`
5. `examples/*/example.cdx`
6. `templates/*/template.cdx`

Implement via dedicated functions:

1. `check_design_policy_completeness(...)`
2. `check_design_intent_completeness(...)`
3. `check_assembly_completeness(...)`

### A4. Manifest Contract Coverage

Apply `check_package_manifest_contract(...)` with expected roots:

1. `DesignPolicyPackageManifest`
2. `DesignIntentPackageManifest`
3. `AssemblyPackageManifest`

Add package-name consistency checks for design families, aligned with existing domain-family naming expectations where applicable.

### A5. Main Pipeline Integration

Update `main()` so design families are first-class participants:

1. discover these packages
2. include them in `all_packages`
3. print grouped package inventory
4. run completeness, naming, and manifest checks for each package

## 6. Workstream B: Repository Completeness Guard

Add a deterministic family-support guard in repository-manifest validation:

1. define a `DECLARED_PACKAGE_FAMILIES` constant equal to the nine-family set in Workshop spec
2. ensure root `manifest.cdx` entries collectively cover every declared family
3. emit deterministic failures naming missing families

This guard prevents future regressions where a declared family is silently unsupported in tooling.

## 7. Workstream C: Test Updates (`tests/test_structural_check.py`)

Add tests for Issue 4 coverage:

1. repository manifest accepts `design-policy`, `design-intent`, and `assembly` family tokens
2. each new family completeness check fails without required files and passes when complete
3. manifest-root validation enforces the expected design-family manifest concepts
4. unknown packageFamily values are still rejected
5. repository family-support guard fails when any declared family is absent

## 8. Acceptance Criteria

Issue 4 is resolved only when all are true:

1. structural checker accepts all declared families and rejects unknown tokens
2. design-family packages are discovered and validated in `main()`
3. design-family completeness and manifest-root checks run and fail deterministically on violation
4. repository-manifest family-support guard enforces declared-family coverage
5. updated structural checker tests pass

## 9. Execution Sequence

Implement in this order:

1. extend family constants, valid-family set, and discovery wiring
2. add design-family completeness and manifest-root checks
3. add repository family-support guard
4. add/update tests
5. run `python3 -m unittest tests/test_structural_check.py`
6. run `python3 tools/structural_check.py --root .`

## 10. Deliverables

Required deliverables:

1. updated `tools/structural_check.py`
2. updated `tests/test_structural_check.py`
3. deterministic failure messages for missing family support
4. passing test evidence for full declared-family coverage

**End of Workshop Structural Check Family Coverage Plan v1.0.0**
