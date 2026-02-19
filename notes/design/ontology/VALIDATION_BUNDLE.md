# Validation Bundle Contract

This document defines the normative SHACL loading contract for the graphic-design ontology.

## Core entrypoint

The canonical validation entrypoint for core composition validity is:

- `gd-all.shacl.ttl`

Validators MUST load `gd-all.shacl.ttl` for conformance decisions.

## Component files

`gd-all.shacl.ttl` is generated from the ordered component list in:

- `shacl-bundle-files.txt`

Current required component set:

1. `gd-core.shacl.ttl`
2. `gd-policy.shacl.ttl`
3. `gd-core-grid.shacl.ttl`
4. `gd-core-figureground.shacl.ttl`
5. `gd-core-closure.shacl.ttl`
6. `gd-core-closure-seal.shacl.ttl`

No subset loading is conformant.

## Build and check commands

Build the bundle:

```bash
notes/design/ontology/scripts/build_shacl_bundle.sh
```

Check bundle sync:

```bash
notes/design/ontology/scripts/check_shacl_bundle.sh
```

Run contract checks (namespaces, bundle sync, traceability, fixture coverage):

```bash
notes/design/ontology/scripts/check_ontology_contract.sh
```

Run SHACL conformance fixtures (requires `pyshacl`):

```bash
notes/design/ontology/scripts/run_conformance_tests.sh
```

Run policy evaluation vectors:

```bash
notes/design/ontology/scripts/run_policy_vectors.sh
```

## Metrics extension

Metrics constraints are an extension layer and are validated separately:

- vocabulary: `notes/workshop/design/gd-metrics.ttl`
- shapes: `notes/workshop/design/gd-metrics.shacl.ttl`

When validating metrics, validators MUST load:

1. `gd-all.shacl.ttl` (core dependency)
2. `notes/workshop/design/gd-metrics.shacl.ttl`

Clause-to-fixture coverage for the core rules is declared in:

- `fixture-coverage.csv`

Coverage semantics:

1. Every SHACL-enforced clause ID MUST have exactly one row in `fixture-coverage.csv`.
2. Each SHACL row MUST reference one positive fixture and one negative fixture file.
3. A negative fixture is required to fail validation for the clause's enforcement layer, but it MAY also violate additional clauses unless otherwise documented.
