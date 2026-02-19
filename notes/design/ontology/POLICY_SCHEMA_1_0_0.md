Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Responsive/Adaptive Policy Schema 1.0.0

This document defines the first rules-based policy grammar for responsive/adaptive behavior.

Status:

- Scope: schema only (1.0.0)
- Enforcement: SHACL (`wd-policy.shacl.ttl`)
- Evaluation algorithm: deferred to a separate deterministic execution spec

## Model

Core classes:

1. `wd:Policy`
2. `wd:Condition`
3. `wd:Action`
4. `wd:ConflictStrategy`

Supporting controlled classes:

1. `wd:ContextKey`
2. `wd:ComparisonOperator`
3. `wd:ActionMode`

## Policy structure

A `wd:Policy` MUST define:

1. exactly one `wd:appliesTo` (`wd:Composition` or `wd:View`)
2. one or more `wd:hasCondition`
3. one or more `wd:hasAction`
4. exactly one integer `wd:priority` (`>= 0`)
5. exactly one `wd:conflictStrategy`
6. exactly one boolean `wd:enabled`

`wd:Composition` MUST attach zero or more policies using `wd:hasPolicy`.

## Condition structure

Each `wd:Condition` MUST define:

1. exactly one `wd:contextKey`
2. exactly one `wd:operator`
3. exactly one typed comparison value:
   - `wd:conditionValueDecimal`
   - `wd:conditionValueInteger`
   - `wd:conditionValueString`
   - `wd:conditionValueBoolean`

1.0.0 determinism constraints:

1. numeric operators (`OpLt`, `OpLte`, `OpGt`, `OpGte`) require numeric values
2. boolean/string values are limited to equality operators (`OpEq`, `OpNe`)

## Action structure

Each `wd:Action` MUST define:

1. exactly one `wd:actionMode`
2. exactly one `wd:targetNode` (IRI)
3. exactly one `wd:targetProperty` (IRI)
4. exactly one typed action value:
   - `wd:actionValueDecimal`
   - `wd:actionValueInteger`
   - `wd:actionValueString`
   - `wd:actionValueBoolean`
   - `wd:actionValueIRI`

## Ambiguity Constraints In 1.0.0

To remove ordering ambiguity before execution semantics are specified:

1. policy priorities MUST be unique within the same `wd:appliesTo` scope
2. conflict strategy MUST be uniform within the same `wd:appliesTo` scope

This is enforced in `wd-policy.shacl.ttl`.

Execution semantics are defined in:

- `POLICY_EVALUATION_1_0_0.md`
