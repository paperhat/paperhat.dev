Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Dialect — Semantics

This specification defines the **Behavior Dialect** semantic contract for Paperhat.

The Behavior Dialect is authored in Codex and compiles into an executable (pure) function artifact. This spec defines **what Behavior means**, independent of any host language or runtime.

This document is **Normative**.

---

## 1. Purpose

This spec exists to define:

- the canonical evaluation model for Behavior expressions
- purity and determinism rules
- the typed value model (Option B: rich semantic types)
- operator application rules (arity, strictness, evaluation order)
- error and diagnostic rules

This spec does not define:

- the operator vocabulary inventory (see Behavior Vocabulary)
- the surface form / encoding of compiled behavior programs (see Behavior Program Surface Form)
- runtime integration details (owned by target runtimes)

---

## 2. Core Principles (Normative)

1. **Purity:** Behavior evaluation MUST be side-effect free.
2. **Determinism:** Given the same program and explicit inputs, evaluation MUST produce the same result.
3. **No ambient dependencies:** Evaluation MUST NOT consult time, randomness, filesystem, network, or other ambient sources.
4. **Runtime independence:** Semantics MUST NOT depend on any particular host implementation.

Additional safety boundaries (Normative):

5. **No dynamic code construction:** Strings are data, never code. A Behavior Program MUST NOT contain or cause:
	- dynamic operator selection (no “operator name from string”)
	- executable data-as-AST (no “evaluate user-provided graph as code”)
	- query-as-string (no SPARQL embedded as a string literal for execution)

Clarifications (Normative):

- Systems MAY depend on time, randomness, or I/O as system behavior.
- Behavior evaluation MUST remain deterministic; therefore time/randomness/I/O MUST be supplied as explicit inputs.

---

## 3. Evaluation Result Model (Normative)

Behavior evaluation produces a `Validation<Value>`:

- `Valid(value)`
- `Invalid(diagnostics)`

An evaluator MUST NOT throw for user-authored input; it MUST return `Invalid(...)` with diagnostics.

Diagnostics MUST be stable and deterministic (ordering and identity rules defined in §7).

---

## 4. Expressions (Normative)

A Behavior Program is an expression tree.

Every node is one of:

- `Argument` — the primary input value
- `Variable(name)` — environment lookup
- `Constant(value)` — literal constant value
- `Field(name)` — field lookup on a Record-like value (see §5 and §6)
- `Path(steps...)` — bounded path traversal (see §5 and §6)
- `Apply(operator, arguments...)` — operator application

Notes:

- `operator` is a reference to a Behavior Vocabulary Concept.
- This spec defines evaluation; the concrete Codex surface form is defined elsewhere.

Path and missingness (Normative):

- `Field(name)` and `Path(...)` MUST be total and deterministic.
- If a referenced field/path location is missing, the result MUST be the canonical `<Absent/>` value.
- Operators that require presence or a specific domain MUST return `Invalid(...)` rather than silently accepting `<Absent/>`.

---

## 5. Value Model (Option B: Rich Semantic Types) (Normative)

Behavior Values are **Codex values** constrained by the Behavior Dialect type system.

### 5.1 Scalar types

- `Boolean`
- `Text`

### 5.1.1 Canonical Absent value

Behavior defines a canonical missing-value concept:

- `<Absent/>`

Normative rules:

1. `<Absent/>` represents “no value exists here” (missing field, missing path location, missing optional trait value).
2. `<Absent/>` is distinct from empty text, empty list, and empty record; those are present values.
3. Implementations MUST NOT introduce any separate “Null” semantic value in v0.1.

### 5.2 Numeric types

This dialect defines distinct semantic numeric domains. All numeric operators MUST specify which domains they accept and what they return.

Initial v0.1 numeric domains:

- `Integer`
- `Fraction` (rational)
- `PrecisionNumber` (explicit precision-carrying decimal)
- `RealNumber` (approximate real)

Rules (Normative):

1. Numeric domains MUST NOT be collapsed into a single host “number” type in the semantic contract.
2. Conversions MUST be explicit and defined by vocabulary Concepts (e.g., `ConvertToInteger`, `ConvertToPrecisionNumber`), or by explicit coercion rules defined in §6.
3. Where an operator admits multiple domains, the result domain MUST be defined and deterministic.

### 5.3 Structural types

- `List<T>`
- `Record` (key/value structure)

`Record` keys are `Text`.

Record key collision policy (Normative):

- Where a Behavior operator merges or combines Records, key collisions MUST be handled deterministically.
- In v0.1, the default merge policy for `MergeRecords` is **InvalidOnCollision** (see §9 and Behavior Vocabulary).

---

## 6. Type Checking and Coercion (Normative)

This spec uses three related ideas:

- **Type checking:** rejecting invalid inputs to an operator.
- **Normalization:** producing a canonical value representation.
- **Coercion:** converting between domains.

Rules (Normative):

1. If an operator receives values outside its domain, evaluation MUST return `Invalid([...])`.
2. Coercion MUST be explicit (via vocabulary Concepts) unless a specific operator family defines a fixed coercion rule.
3. Any implicit coercion rules that do exist MUST be minimal, deterministic, and specified by this document.

(TBD: final coercion lattice and promotion rules. Coordinate with the mapping tables work.)

---

## 7. Diagnostics (Normative)

A diagnostic MUST include:

- a stable code (token)
- an optional human-readable message
- a stable location reference to the originating expression node (program-local)

Code structure (Normative):

- Codes MUST follow the pattern `<surfaceName>::<ISSUE_DESCRIPTION>`.
- Where a v0.1 Behavior diagnostic code is required, it MUST use the corresponding code defined by Behavior Diagnostic Codes.

Diagnostics ordering MUST be deterministic. (TBD: ordering key.)

---

## 8. Evaluation Order and Strictness (Normative)

Implementations MAY evaluate operands using any strategy (including reordering, parallelism, or short-circuiting) provided that:

1. the final `Valid(...)` / `Invalid(...)` outcome is identical to the reference evaluation defined by this specification, and
2. the ordered list of produced diagnostics is identical to the reference ordering rules.

Unless explicitly stated otherwise, evaluation MUST behave observably as if:

- argument expressions were evaluated left-to-right, and
- diagnostics were accumulated and emitted in authored operand order.

Operators MAY be implemented as curried and/or higher-order functions internally, but the observable semantics MUST match this specification.

---

## 9. Core Safe Behavior Profile (0.1) (Normative)

This section defines the v0.1 “Core Safe” profile for Behavior transforms. The purpose is to enable practical map/filter/sort/join transforms while remaining closed-world, bounded, and deterministic.

### 9.1 Failure channel

Behavior evaluation already returns `Validation<Value>`.

Normative rule:

- Behavior transform operators that can fail MUST return `Invalid(...)` rather than encoding failure as `<Absent/>`.

### 9.2 Collection transforms

For `MapElements` and `FilterElements`:

- output order MUST preserve input order.

For `FindFirstElement`:

- it MUST select the first matching element in input order.

### 9.3 Sort determinism

For `SortElementsBy`:

- sorting MUST be stable.
- elements whose sort-key is `<Absent/>` MUST sort last.
- if two keys are not comparable under the specified ordering, the result MUST be `Invalid(...)`.

### 9.4 Record merge determinism

For `MergeRecords`:

- key collisions MUST produce `Invalid(...)`.

### 9.5 Join determinism

If `JoinCollectionsOnKey` is supported in v0.1 Core Safe:

- it MUST be a keyed inner join.
- duplicate keys on either side MUST produce `Invalid(...)` (RejectDuplicates).
- output ordering MUST be deterministic and MUST behave observably as left-order primary, right-order secondary.

### 9.6 Boundedness

An implementation MUST enforce policy-bounded limits sufficient to prevent resource exhaustion.

At minimum, limits MUST be enforceable for:

- maximum program depth
- maximum expression depth
- maximum collection length processed per operator
- maximum output size
- maximum join output size

---

## 9. Relationship to Other Specifications

This specification works in conjunction with:

- Behavior Vocabulary (operator inventory and semantics per operator)
- Behavior Program Surface Form (Codex surface form / encoding for compiled programs)
- Target runtimes (HTML runtime, native runtime, etc.)

---

**End of Behavior Dialect — Semantics v0.1**
