# Responsive/Adaptive Policy Evaluation v0

This document defines deterministic execution semantics for `gd:Policy` over a validated canonical graph.

Status:

- Scope: execution model (v0)
- Depends on: `POLICY_SCHEMA_V0.md`
- Failure mode: fail-closed

## 1. Inputs

Required inputs:

1. canonical RDF graph `G` for a target `gd:Composition`
2. target scope:
   - composition-only, or
   - composition + specific `gd:View`
3. runtime context map `CTX` keyed by `gd:ContextKey`

`G` MUST pass SHACL validation before evaluation (`gd-all.shacl.ttl`).

## 2. Preconditions

Evaluation MUST terminate with `EVALUATION_ERROR` if any condition below is true:

1. SHACL validation fails
2. a referenced policy/condition/action node is missing from `G`
3. a required context key for an evaluated condition is missing from `CTX`
4. context value type does not match the condition value type
5. matched policies use different `gd:conflictStrategy` values

No partial application is allowed on error.

## 3. Candidate policy set

Given target scope:

1. include enabled policies where `gd:appliesTo` is target composition
2. if target view is provided, also include enabled policies where `gd:appliesTo` is that view

Disabled policies (`gd:enabled false`) are ignored.

## 4. Condition semantics

A policy matches iff all of its conditions are true (`AND` semantics).

Operator semantics:

1. `OpEq`: equal
2. `OpNe`: not equal
3. `OpLt`: strictly less-than (numeric)
4. `OpLte`: less-than-or-equal (numeric)
5. `OpGt`: strictly greater-than (numeric)
6. `OpGte`: greater-than-or-equal (numeric)

Numeric comparison domain:

- integer and decimal are compared in decimal space.

## 5. Deterministic ordering

For matched policies, define deterministic policy order by tuple:

1. descending `gd:priority`
2. scope specificity rank (view-specific before composition-specific)
3. policy IRI ascending (Unicode scalar order)

Within a policy, actions are ordered by action IRI ascending.

## 6. Conflict key

Each action maps to conflict key:

- `(gd:targetNode, gd:targetProperty)`

Actions with different conflict keys do not conflict.

## 7. Conflict resolution

The effective strategy is the shared `gd:conflictStrategy` across matched policies.

If strategies are mixed, result is `EVALUATION_ERROR`.

For each conflict key with multiple actions:

1. `ErrorOnConflict`: `EVALUATION_ERROR`
2. `FirstMatchWins`: select the first action in deterministic order
3. `HigherPriorityWins`: select the highest-priority action
   - tie-breaker 1: view scope over composition scope
   - tie-breaker 2: policy IRI ascending
   - tie-breaker 3: action IRI ascending

## 8. Action semantics

Action execution is pure graph rewrite over the target node/property:

1. `ReplaceAll`: remove all existing values at target property, then insert action value
2. `Add`: insert action value if absent
3. `Remove`: remove action value if present

Action values use the typed value field from schema (`actionValue*`).

## 9. Output

Successful evaluation returns:

1. deterministic ordered list of applied actions
2. resulting graph `G'`

`G'` MUST remain SHACL-valid under `gd-all.shacl.ttl`.

If post-application validation fails, return `EVALUATION_ERROR`.

## 10. Determinism requirement

For identical `(G, scope, CTX)`, implementations MUST produce byte-identical action decision sequences and equivalent resulting triples.

## 11. Executable vectors

Executable test vectors are defined in:

- `notes/design/ontology/policy-vectors/*.json`

Reference graph fixtures for vectors are defined in:

- `notes/design/ontology/fixtures/policy/vector/`

Run vectors using:

```bash
notes/design/ontology/scripts/run_policy_vectors.sh
```
