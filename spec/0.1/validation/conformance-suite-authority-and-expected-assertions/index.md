Status: NORMATIVE  
Lock State: DRAFT (candidate for LOCKED)  
Version: 0.1  
Editor: Charles F. Munat

# Conformance Suite Authority and Expected Assertions

This document locks core governance decisions for conformance suites, especially suites that validate numeric semantics across backends.

This document is **Normative**.

---

## 1. Canonical Authority Boundary (Normative)

For a given domain (for example, Math) and spec version:

- There MUST be exactly one blessed conformance suite per version.
- Backend mapping tables and implementation notes are never authoritative; they are claims that must survive the suite.

### 1.1 Normative artifacts

For a surface with both prose semantics and a conformance suite:

1. Prose semantics define meaning (formulas, ranges, tie-breaking, invariants) and are human-reviewable.
2. The single blessed Codex conformance suite is the enforcement mechanism.

Conflict rule (Normative):

- The prose semantics and the Codex conformance suite are both Normative.
- Any disagreement between them constitutes a specification defect and MUST be resolved explicitly.

Operational guidance (Informative):

- Implementations are typically validated against the conformance suite.
- Resolution of a defect may involve correcting the suite, the prose, or both, but never by silent precedence.

---

## 2. Canonical Special-Value Concepts (Normative)

Where applicable, special values MUST be represented as first-class Concepts:

- `<NotANumber />`
- `<PositiveInfinity />`
- `<NegativeInfinity />`
- `<NegativeZero />`

Negative zero representation rule (Normative):

- Any numeric literal representation of negative zero is FORBIDDEN.
- Negative zero MUST be represented only as `<NegativeZero />`.

Rationale (Informative):

- Literal negative zero is not round-trip safe across languages, runtimes, and graph serializations.
- Signed zero is semantic, not magnitude.

---

## 3. Numeric Domains and Coercion (Normative)

- `Integer` and `RealNumber` are distinct Concepts.
- No implicit coercion occurs at the semantic level.
- Each operation MUST declare (or imply via its definition) the required operand domains and result domain.

Examples (Informative):

- `Remainder(Integer, Integer) → Integer`
- `FloatingRemainder(RealNumber, RealNumber) → RealNumber`
- `RoundTowardZero(RealNumber) → Integer`

If a backend coerces internally, that is an implementation detail, not semantic meaning.

---

## 4. Expected Outcomes: Value Equality vs Property Assertions (Normative)

Some expectations are values. Others are properties that cannot be expressed as plain equality.

The conformance suite MUST support both:

### 4.1 Value equality

An expected value is compared using the value equality rules for the relevant domain.

### 4.2 Property assertions

An expected outcome can assert a property of the observed value.

The following assertion Concepts are REQUIRED when those properties are tested:

- `<AssertNegativeZero />`
- `<AssertIsNotANumber />`
- `<AssertIsPositiveInfinity />`
- `<AssertIsNegativeInfinity />`
- `<AssertIsFinite />`

Applicability note (Normative):

- If a test’s expected outcome includes `<AssertNegativeZero />`, the backend MUST declare a capability equivalent to “supports signed zero” for the test to be applicable.

---

## 5. Reasoning Layer (Informative)

Suites MAY be authored as Concepts + Traits that compile deterministically into triples, enabling:

- SHACL validation of structure and completeness
- inference of applicability (skip logic becomes declarative)
- querying results, regressions, and mapping mismatches

See `Conformance Suite Ontology and Reasoning` for the recommended pattern.

---

**End of Conformance Suite Authority and Expected Assertions v0.1**
