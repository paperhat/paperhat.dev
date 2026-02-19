Status: WORKING
Lock State: LOCKED
Version: 1.0.0

# Stage A Evaluation 1.0.0

This document defines deterministic Stage A policy evaluation semantics for adaptive intent execution.

## 1. Inputs

A conforming Stage A evaluator MUST consume:

1. one compiled adaptive request (`CompiledAdaptiveRequest`)
2. one policy graph
3. one SHACL bundle (`gd-all.shacl.ttl`)
4. one ontology graph (`gd-core.ttl`)

## 2. Preconditions

Evaluation MUST terminate with `EVALUATION_ERROR` if any condition below is true:

1. compiled request is malformed
2. policy graph is malformed
3. SHACL pre-evaluation validation fails
4. Stage A composition IRI is missing or not typed `gd:Composition`
5. Stage A view IRI is supplied and not typed `gd:View`
6. a required context key is missing
7. condition typing or operator semantics are invalid
8. matched policies contain mixed conflict strategies

No partial output is allowed on error.

## 3. Candidate selection and ordering

Policy matching and action selection MUST follow deterministic ordering:

1. candidate policy order:
   - higher `gd:priority` first
   - view scope before composition scope
   - lexical policy IRI tie-break
2. action order within policy:
   - lexical action IRI order
3. conflict handling:
   - strategy semantics from `gd:conflictStrategy`
   - deterministic first-selected action per `(targetNode, targetProperty)` key when required

## 4. Output

Successful evaluation MUST emit `StageAResult status="ok"` with:

1. ordered `SelectedActions`
2. `Delta` containing:
   - ordered `Remove` triples
   - ordered `Add` triples

Failure MUST emit `StageAResult status="error" error="EVALUATION_ERROR"`.

Every emitted `StageAResult` MUST validate against:

1. `notes/workshop/design/codex/stage-a-result.schema.cdx`

## 5. Executable vectors

Executable vectors for Stage A semantics are defined in:

1. `notes/design/ontology/policy-vectors/*.cdx`

Executable compile->Stage A output assertions are defined in:

1. `notes/workshop/design/compiler-mapping/fixtures/adaptive-intent-stage-a-e2e.*.cdx`

Run Stage A checks using:

```bash
notes/workshop/design/compiler-mapping/scripts/run_stage_a_e2e_checks.sh
```
