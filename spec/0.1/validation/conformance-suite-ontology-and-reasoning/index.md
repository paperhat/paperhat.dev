Status: INFORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Conformance Suite Ontology and Reasoning

This document records an Informative design pattern for expressing Paperhat conformance suites (tests, applicability, mappings, and results) as **Concepts + Traits** that compile into RDF triples.

The motivation is practical:

- make test suites structurally valid before execution
- make applicability (“skip logic”) declarative
- make conformance results queryable and reasoned over
- detect semantic mapping mistakes (for example, confusing Euclidean modulus with truncation remainder)

This document is **Informative**. It does not change any operator semantics.

---

## 1. Model Overview

A conformance suite can be modeled as an ontology of:

- **Test intent** (what is being asserted)
- **Test structure** (operation, arguments, expected value, preconditions)
- **Backend capability** (supports signed zero, supports IEEE remainder variants, supports next-representable)
- **Backend mapping claims** (direct/emulated/library + target symbol)
- **Execution outcomes** (pass/fail/not-applicable + observed values + environment metadata)

When expressed as triples, OWL2/SHACL + SPARQL provides three superpowers:

1. Structural validation and completeness checking (SHACL)
2. Inference of derived facts (OWL2 rules / SHACL rules / SPARQL CONSTRUCT)
3. Querying conformance, gaps, regressions, and semantic mismatches (SPARQL)

---

## 2. Recommended Core Concepts (Informative)

The following Concept categories are typical:

- `ConformanceSuite`
- `TestSection`
- `TestCase`
- `Operation`
- `ExpectedValue`
- `ObservedValue`
- `BackendImplementation`
- `ExecutionRun`
- `ExecutionResult`
- `Outcome` (Pass / Fail / NotApplicable)
- `Capability`
- `CapabilitySet`
- `FunctionMapping`

Recommended Traits:

- `TestCase`:
  - `name`
  - `inSection`
  - `testsFunction`
  - `coversClause`
  - `hasOperation`
  - `hasExpectedValue`
  - `requiresCapabilitySet`
  - `isCritical`
- `Operation`:
  - `functionIri` (stable identifier)
  - `operandValues` (ordered)
  - `preconditions`
- `BackendImplementation`:
  - `supportsCapabilitySet`
  - `hasMapping`
- `ExecutionRun`:
  - `forBackend`
  - `backendVersion`
  - `runTimestamp`
  - `environmentMetadata`
  - `hasResult`
- `ExecutionResult`:
  - `forTestCase`
  - `outcome`
  - `observedValue`

---

## 3. Structural Validation with SHACL (Informative)

Because Codex → triples is deterministic, SHACL can validate authored test vectors before any backend runs them.

Examples of constraints worth locking:

- Every `TestCase` MUST have exactly one `Operation` and exactly one `ExpectedValue`.
- Every `Operation` MUST have exactly one canonical function identifier (stable IRI).
- The `ExpectedValue` type MUST be compatible with the function’s return type.
- If an expected value is `NegativeZero`, the backend MUST declare `SupportsSignedZero = true` for the test to be applicable.
- `Modulus` tests MUST have a non-zero divisor precondition.

This provides authoring-time correctness and machine-checkable governance.

---

## 4. Reasoning and Inference (Informative)

### 4.1 Applicability inference

A test’s applicability to a backend can be inferred from capability triples.

Examples:

- A test asserting `NegativeZero` is `NotApplicable` to a backend that lacks signed zero.
- Tests for `IeeeRemainder` are `NotApplicable` unless the backend can implement `IeeeRemainder` (direct or emulated).

This enables a data-driven runner: it asks the graph “which tests are applicable?” and executes only those.

### 4.2 Conformance level inference

Define classes such as:

- `FullyConformantBackend`
- `ConformantExceptSignedZero`
- `NonConformantForEuclideanModulus`

Membership can be inferred from results:

- If a backend passes all applicable tests in required sections → `FullyConformantBackend`.
- If it fails any `CriticalTestCase` → `NonConformantBackend`.

### 4.3 Semantic mismatch inference

Record semantic facts about target-language operators to detect mapping mistakes.

Example:

- Python `%` for negatives aligns with Euclidean modulus (for positive divisors), not truncation remainder.
- If an implementation claims it used “Direct mapping” of `%` for `Remainder`, infer `MappingSemanticMismatch`.

This catches mistakes before runtime.

---

## 5. SPARQL Query Patterns (Informative)

The query examples below are illustrative. They are not intended as query strings embedded for execution.

### 5.1 Which tests are failing on backend X?

```sparql
SELECT ?testName ?sectionName ?functionName ?expected ?observed
WHERE {
  ?run a :ExecutionRun ;
       :forBackend :Backend_X ;
       :hasResult ?result .

  ?result :forTestCase ?test ;
          :outcome :Fail ;
          :observedValue ?observed .

  ?test :name ?testName ;
        :inSection ?section ;
        :testsFunction ?function ;
        :expectedValue ?expected .

  ?section :name ?sectionName .
  ?function :name ?functionName .
}
ORDER BY ?sectionName ?testName
```

### 5.2 Show only critical failures

```sparql
SELECT ?testName ?functionName
WHERE {
  ?result :outcome :Fail ;
          :forTestCase ?test .
  ?test a :CriticalTestCase ;
        :name ?testName ;
        :testsFunction ?function .
  ?function :name ?functionName .
}
```

### 5.3 Detect semantic mapping mistakes

If mapping claims are stored as:

- `mapsCanonicalFunction`
- `mappingMode` (Direct / Emulate / Library)
- `usesTargetSymbol`

and semantic facts classify target symbols:

- `EuclideanModulusOperator`
- `TruncationRemainderFunction`

then mismatches can be queried:

```sparql
SELECT ?backend ?canonicalName ?targetSymbol
WHERE {
  ?mapping a :FunctionMapping ;
           :forBackend ?backend ;
           :mapsCanonicalFunction ?canonical ;
           :mappingMode :Direct ;
           :usesTargetSymbol ?targetSymbol .

  ?canonical a :TruncationRemainderFunction ;
            :name ?canonicalName .

  ?targetSymbol a :EuclideanModulusOperator .
}
```

---

## 6. Stable Identifiers (Informative)

This approach benefits from stable identifiers:

- Every canonical function and semantic rule SHOULD have a stable IRI.
- Tests SHOULD link to functions and clauses by IRI:
  - `TestCase testsFunction CanonicalFunctionIRI`
  - `TestCase coversClause NormativeClauseIRI`

This makes provenance, traceability, and impact analysis straightforward.

---

## 7. Relationship to Math Conformance

The Math surface defines a conformance appendix with normative test vectors.

This document describes an optional *representation strategy* for those vectors and their outcomes:

- author tests as Concepts + Traits
- compile deterministically to triples
- validate structure with SHACL
- infer applicability with rules
- query outcomes with SPARQL

No non-Codex artifacts are required.

---

**End of Conformance Suite Ontology and Reasoning v0.1**
