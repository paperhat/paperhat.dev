# Namespace Policy

This policy defines the authoritative namespace rules for the graphic-design ontology and metrics extension.

## Canonical Namespaces

The only production namespaces are:

- `gd:` -> `https://paperhat.dev/ns/gd#`
- `gdm:` -> `https://paperhat.dev/ns/gdm#`

All non-test ontology, SHACL, and fixture files MUST use these namespaces.

## Immutability Rules

1. Term IRIs are immutable after release.
2. Semantic version identifiers MUST NOT be embedded in term IRIs.
3. Versioning metadata, if needed, MUST be expressed at the ontology-document level.
4. Namespace migration requires an explicit, repository-wide rewrite and policy update.

## Runtime and Dereferencing Rules

1. Validation and hashing MUST NOT depend on network dereferencing.
2. Tooling MUST operate correctly in offline mode.
3. Published namespace documents MAY be hosted for human-readable discovery, but runtime semantics MUST remain local and deterministic.

## Forbidden Namespace Usage

`paperhat.example` is forbidden in non-test files.

Repository checks MUST fail if this legacy namespace appears outside test-only paths.
