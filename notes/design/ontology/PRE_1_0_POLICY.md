# Pre-1.0 Working Policy

This policy defines how ontology/spec changes are handled before the first public `v1.0.0` release.

## Status

- Repository status: private
- Contributor model: internal (you + Codex)
- Release status: pre-`1.0.0`

## Core Rule

Before `v1.0.0`, this project runs in a single-track working mode:

1. Breaking changes are allowed.
2. Semantic versioning, release manifests, and formal governance workflows are deferred.
3. Git history is the authoritative change history for pre-`1.0.0`.

## Required Discipline (Pre-1.0)

Every accepted normative change MUST:

1. keep namespace policy intact (`NAMESPACE_POLICY.md`)
2. keep traceability and fixture coverage artifacts current
3. pass ontology contract checks:
   - `notes/design/ontology/scripts/check_ontology_contract.sh`
4. pass conformance fixtures:
   - `notes/design/ontology/scripts/run_conformance_tests.sh`

If checks fail, the change is not accepted.

## Decision Log (Lightweight)

Major normative shifts SHOULD be recorded briefly in commit messages or PR notes with:

1. what changed
2. why it changed
3. which constraints/fixtures were updated

No separate changelog process is required pre-`1.0.0`.

## Trigger To Enable Full Governance

Full governance/versioning is activated when any one of these becomes true:

1. first external consumer depends on this spec
2. first public release candidate is prepared
3. explicit owner decision to freeze compatibility guarantees

At that point, adopt a formal SemVer/governance model.

