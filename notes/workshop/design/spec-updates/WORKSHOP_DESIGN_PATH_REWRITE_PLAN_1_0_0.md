Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Workshop Design Path Rewrite Plan 1.0.0

## 1. Objective

Fix Issue 6 by removing hardcoded legacy design-note paths from executable tooling and validation artifacts so design assets remain runnable after migration into Workshop.

Target state:

1. no executable `.py`/`.sh` tooling or vector/coverage `.cdx`/`.csv` assets depend on literal `notes/design/ontology/...` or `notes/workshop/design/...` paths
2. canonical Workshop design-validation prefixes are primary: `spec/1.0.0/validation/design/ontology/...` and `spec/1.0.0/validation/design/workshop/...`
3. path resolution works in both transition staging (paperhat.dev) and final Workshop location

## 2. Authority Policy

Policy for this plan:

1. paperhat.dev design artifacts are the active correction source during migration drafting
2. when paperhat.dev path contracts are better/newer, Workshop spec/tooling is updated to match them
3. final normative authority remains Workshop specification + Workshop repository artifacts

## 3. Confirmed Defect

Current state contained migration-breaking assumptions:

1. hardcoded legacy literals in scripts and validation data (`notes/design/ontology/...`, `notes/workshop/design/...`)
2. fixed-depth repo-root assumptions (`parents[4|5]`, `../../../..`) that fail after relocation
3. mixed canonical/legacy fixture resolution behavior causing inconsistent execution across locations

## 4. Canonical Path Contract

The only normative design-validation prefixes are:

1. `spec/1.0.0/validation/design/ontology/`
2. `spec/1.0.0/validation/design/workshop/`

All vector and coverage references MUST use those prefixes.

## 5. Workstream A: Rewrite Data Path References

Apply deterministic rewrites:

1. vector `.cdx` files: rewrite legacy design-note prefixes to canonical Workshop prefixes
2. `fixture-coverage.csv`: rewrite positive/negative fixture paths to canonical Workshop prefixes
3. reject any residual legacy-prefix rows in executable validation data

## 6. Workstream B: Rewrite Script Resolution Rules

For all design validation scripts:

1. use canonical Workshop paths as primary targets
2. use transition-safe local fallback derived from script location, not hardcoded legacy path strings
3. discover repository root by ancestor search (`.git`), not fixed parent-depth assumptions
4. keep deterministic failure messages when no valid path can be resolved

## 7. Workstream C: Verification Gates

Issue 6 is complete only if all are true:

1. `rg` scan over relevant `.py/.sh/.cdx/.csv` returns zero matches for `notes/design/ontology/` and `notes/workshop/design/`
2. shell scripts pass `bash -n`
3. Python scripts pass `python3 -m py_compile`
4. representative design runners resolve canonical paths correctly in transition staging and canonical Workshop layout

## 8. Execution Sequence

Implement in this order:

1. rewrite vector/coverage data path literals
2. rewrite shell tooling path and root discovery logic
3. rewrite Python tooling resolvers and root discovery logic
4. run static syntax checks (`bash -n`, `python3 -m py_compile`)
5. run residual legacy-path scans and record zero-match evidence
6. update `spec-updates/index.md` issue coverage list

## 9. Deliverables

Required deliverables:

1. updated design tooling scripts with canonical-first resolution
2. updated vector/coverage artifacts using canonical Workshop prefixes
3. zero-match residual scan results for legacy design-note path literals
4. syntax-check evidence for modified shell and Python tooling

**End of Workshop Design Path Rewrite Plan v1.0.0**
