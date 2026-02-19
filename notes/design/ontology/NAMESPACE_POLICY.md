# Namespace Policy

This policy defines the authoritative namespace rules for the Workshop design ontology and metrics extension.

## Canonical Namespaces

The only production namespaces are:

- `wd:` -> `https://paperhat.dev/ns/wd#`
- `wdm:` -> `https://paperhat.dev/ns/wdm#`

All non-test ontology, SHACL, and fixture files MUST use these namespaces.

## Immutability Rules

1. Term IRIs are immutable after release.
2. Semantic version identifiers MUST NOT be embedded in term IRIs.
3. Versioning metadata, if needed, MUST be expressed at the ontology-document level.
4. Namespace migration requires an explicit, repository-wide rewrite and policy update.

## Runtime and Dereferencing Rules

1. Validation and hashing MUST NOT depend on network dereferencing.
2. Tooling MUST operate correctly in offline mode.
3. Published namespace documents MUST be hosted only for human-readable discovery, and runtime semantics MUST remain local and deterministic.

## Forbidden Namespace Usage

`paperhat.example` is forbidden in non-test files.

Repository checks MUST fail if this legacy namespace appears outside test-only paths.
