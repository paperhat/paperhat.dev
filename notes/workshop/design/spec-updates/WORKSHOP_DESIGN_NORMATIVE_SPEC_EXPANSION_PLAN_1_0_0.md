Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Workshop Design Normative Spec Expansion Plan 1.0.0

## 1. Objective

Add full normative design semantics to Workshop core specification so implementers can build conformant behavior without relying on paperhat.dev notes.

Current gap:

1. `§18` has family-level summaries only.
2. `§19` has package-location mapping only.
3. full design rules live outside Workshop core spec in paperhat.dev notes.

Target state:

1. Workshop `spec/1.0.0/index.md` becomes complete for design semantics.
2. paperhat.dev design notes become staging/reference artifacts, not normative dependency for implementers.

Authority policy for this plan:

1. paperhat.dev design notes are the active design-authoring source during this drafting window
2. when paperhat.dev content is more correct, more deterministic, or more complete, Workshop spec is updated to match it
3. existing Workshop wording has no precedence merely because it already exists

## 2. Fixed Recommendation

Use a new top-level normative design section appended after current Workshop sections (provisional: `§26`) instead of inserting in the middle.

Reason:

1. avoids section-number churn while active Workshop edits are ongoing
2. minimizes merge collisions
3. allows direct references from `§18.3` and `§18.4` to the new detailed section
4. preserves existing cross-reference stability in `§20` through `§25`

## 3. Source-to-Target Mapping

Normative content to elevate is sourced from:

1. `notes/design/canonical-composition-construction-rules/index.md`
2. `notes/design/ontology/index.md`
3. `notes/design/ontology/POLICY_SCHEMA_1_0_0.md`
4. `notes/design/ontology/POLICY_EVALUATION_1_0_0.md`
5. `notes/design/ontology/VALIDATION_BUNDLE.md`
6. `notes/design/ontology/CANONICAL_RULE_TRACEABILITY.md`
7. `notes/workshop/design/RESPONSIVE_PROJECTION_SEMANTICS_1_0_0.md`
8. `notes/workshop/design/STAGE_A_EVALUATION_1_0_0.md`
9. `notes/workshop/design/STAGE_B_EVALUATION_1_0_0.md`
10. `notes/workshop/design/STAGE_C_PLAN_EMISSION_1_0_0.md` (aligned with adaptive-plan reconciliation plan)
11. `notes/workshop/design/COMPILER_MAPPING_SPEC_1_0_0.md`

## 4. Proposed Workshop Section Shape

Create one new top-level section with deterministic subsections:

1. `26.1 Purpose and Boundary`
2. `26.2 Canonical Design Semantic Model`
3. `26.3 Canonical Construction and Sealing Invariants`
4. `26.4 DesignPolicy Schema Contract`
5. `26.5 DesignPolicy Evaluation Semantics`
6. `26.6 DesignIntent Contract`
7. `26.7 Adaptive Design Evaluation Stages (A/B/C)`
8. `26.8 Validation Bundle and Enforcement Layers`
9. `26.9 Diagnostics and Failure Model`
10. `26.10 Conformance Vectors and Acceptance`
11. `26.11 Relationship to Semantic Projections and Foundry Boundary`

## 5. Clause Discipline (Mandatory)

Each normative clause introduced into Workshop must include:

1. a stable clause identifier
2. enforcement mapping (`SHACL`, `PROC`, `SPEC`)
3. deterministic pass/fail condition
4. explicit diagnostic behavior on failure where applicable

No prose-only normative obligations are allowed without enforcement mapping.

## 6. Cross-Section Integration Updates

After `§26` is authored, apply targeted link updates in Workshop core:

1. `§18.3` and `§18.4` reference `§26` for full semantics
2. `§19` references design package locations plus `§26` semantics
3. `§20` references `§26` where projection behavior depends on design-policy/design-intent meaning
4. `§22` and `§23` preserve package-only semantic boundary and avoid foundry reinterpretation
5. `§24` includes design-specific conformance profile entries or references

Any older conflicting Workshop wording must be replaced, not retained in parallel.

## 7. Issue 3 Fix: Family/Package Reality Alignment (Mandatory)

Fixed resolution:

1. keep `§19` family coverage for `DesignPolicy`, `DesignIntent`, and `Assembly`
2. create matching family roots in Workshop at:
   - `spec/1.0.0/schemas/design-policy/`
   - `spec/1.0.0/schemas/design-intent/`
   - `spec/1.0.0/schemas/assembly/`
3. add at least one concrete package under each family root with valid package `manifest.cdx`
4. source package contracts from reconciled paperhat.dev design content; do not create placeholder semantics
5. add corresponding `RepositoryPackageEntry` records in Workshop root `manifest.cdx` for every new package
6. ensure each new entry has exact `packageFamily` token alignment (`design-policy`, `design-intent`, `assembly`)
7. remove any phantom location claims: every `§19` family location must resolve to real package directories declared in root manifest

No pending/deferred wording is permitted for these three families once transferred.

## 8. Conformance Artifact Plan

Normative section expansion must be backed by executable checks:

1. policy vectors
2. Stage A/B/C vectors
3. pipeline vectors
4. SHACL bundle checks
5. procedural checks
6. clause-to-fixture traceability checks
7. structural-check declared-family coverage checks (see `WORKSHOP_STRUCTURAL_CHECK_FAMILY_COVERAGE_PLAN_1_0_0.md`)
8. TTL/SHACL asset migration coverage and hash-parity checks (see `WORKSHOP_TTL_SHACL_MIGRATION_PLAN_1_0_0.md`)

If a clause has no vector strategy, it is incomplete.

## 9. Delivery Artifacts in Paperhat.dev Staging

Prepare these artifacts in paperhat.dev first:

1. `§26` draft text blocks (ready to paste into Workshop spec)
2. clause/enforcement mapping table for all imported design clauses
3. unresolved ambiguity list (must be empty before transfer)
4. cross-reference patch list for Workshop `index.md`

## 10. Transfer Strategy to Workshop Repo

Transfer only after active Workshop edits reach a safe sync point.

Transfer execution:

1. apply `§26` from the reconciled paperhat.dev draft in one controlled batch
2. apply cross-reference updates in a second controlled batch
3. run Workshop structural and manifest checks
4. run design conformance suites once integrated
5. verify no conflicting duplicate definitions remain between sections
6. verify no older conflicting normative wording remains active after transfer

## 11. Completion Criteria

This plan is complete only when all are true:

1. Workshop spec contains full normative design semantics (not summary-only)
2. every design clause has enforcement mapping
3. no normative dependency on paperhat.dev notes remains for implementers
4. adaptive-plan/foundry boundary remains unambiguous
5. conformance vectors cover normative design semantics end-to-end
6. package-location statements match actual repository reality
7. root `manifest.cdx` declares concrete `design-policy`, `design-intent`, and `assembly` packages with existing paths
8. migrated TTL/SHACL assets exist in Workshop under explicit target layout with deterministic manifest coverage

## 12. Execution Sequence

Implement in this order:

1. freeze section model and clause ID scheme
2. reconcile terminology with adaptive-plan contract plan
3. draft `§26` prose and tables in paperhat.dev staging
4. prepare Issue 3 package/manifest patch set from reconciled paperhat.dev design artifacts
5. prepare Issue 4 structural-check tooling patch set (family parity and completeness guards)
6. prepare Issue 5 TTL/SHACL migration patch set and verification manifest
7. prepare Workshop cross-reference patch list
8. transfer to Workshop at safe sync point
9. run conformance and finalize

**End of Workshop Design Normative Spec Expansion Plan v1.0.0**
