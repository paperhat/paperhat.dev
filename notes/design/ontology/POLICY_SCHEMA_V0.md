# Responsive/Adaptive Policy Schema v0

This document defines the first rules-based policy grammar for responsive/adaptive behavior.

Status:

- Scope: schema only (v0)
- Enforcement: SHACL (`gd-policy.shacl.ttl`)
- Evaluation algorithm: deferred to a separate deterministic execution spec

## Model

Core classes:

1. `gd:Policy`
2. `gd:Condition`
3. `gd:Action`
4. `gd:ConflictStrategy`

Supporting controlled classes:

1. `gd:ContextKey`
2. `gd:ComparisonOperator`
3. `gd:ActionMode`

## Policy structure

A `gd:Policy` MUST define:

1. exactly one `gd:appliesTo` (`gd:Composition` or `gd:View`)
2. one or more `gd:hasCondition`
3. one or more `gd:hasAction`
4. exactly one integer `gd:priority` (`>= 0`)
5. exactly one `gd:conflictStrategy`
6. exactly one boolean `gd:enabled`

`gd:Composition` MAY attach policies using `gd:hasPolicy`.

## Condition structure

Each `gd:Condition` MUST define:

1. exactly one `gd:contextKey`
2. exactly one `gd:operator`
3. exactly one typed comparison value:
   - `gd:conditionValueDecimal`
   - `gd:conditionValueInteger`
   - `gd:conditionValueString`
   - `gd:conditionValueBoolean`

v0 determinism constraints:

1. numeric operators (`OpLt`, `OpLte`, `OpGt`, `OpGte`) require numeric values
2. boolean/string values are limited to equality operators (`OpEq`, `OpNe`)

## Action structure

Each `gd:Action` MUST define:

1. exactly one `gd:actionMode`
2. exactly one `gd:targetNode` (IRI)
3. exactly one `gd:targetProperty` (IRI)
4. exactly one typed action value:
   - `gd:actionValueDecimal`
   - `gd:actionValueInteger`
   - `gd:actionValueString`
   - `gd:actionValueBoolean`
   - `gd:actionValueIRI`

## Ambiguity constraints in v0

To remove ordering ambiguity before execution semantics are specified:

1. policy priorities MUST be unique within the same `gd:appliesTo` scope
2. conflict strategy MUST be uniform within the same `gd:appliesTo` scope

This is enforced in `gd-policy.shacl.ttl`.

Execution semantics are defined in:

- `POLICY_EVALUATION_V0.md`
