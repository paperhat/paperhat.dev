Status: NORMATIVE  
Lock State: DRAFT (candidate for LOCKED)  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Program Policy and Resource Limits

This specification defines the canonical safety policy model for evaluating a Behavior Program as data.

This document is **Normative**.

---

## 1. Purpose (Normative)

Paperhat Behavior is intentionally not a general-purpose programming language.

This spec exists to ensure that Behavior remains:

- pure (no I/O, no ambient dependencies)
- closed-world (only approved operations)
- bounded (no unbounded iteration, recursion, or uncontrolled growth)
- safe to compile into constrained execution plans (including triple-store queries)

This specification complements:

- `Behavior Dialect` (purity and safety boundary)
- `Behavior Vocabulary — Core Safe Transforms` (collection/record transform algebra)

---

## 2. Policy Model (Normative)

A runtime that evaluates Behavior MUST apply a **Policy**.

A Policy has two independent parts:

1. **Surface allowance**: which operations are allowed at all.
2. **Resource limits**: what structural or metered bounds apply during evaluation.

A backend MAY support multiple named policies (for example, “strict”, “trusted author”, “preview”), but for any given evaluation the active policy MUST be explicit and stable.

---

## 3. Surface Allowance (Normative)

### 3.1 Closed-world operator allowlist

A Policy MUST define an allowlist of operation tokens.

- If the Behavior Program uses an operation token not in the allowlist, evaluation MUST return `Invalid(...)`.
- Tooling SHOULD reject disallowed programs before evaluation.

### 3.2 Expression surface allowance

A Policy MAY further restrict which operation families may appear inside other operators.

Example (Informative):

- allow `MapElements` only when its mapper expression uses:
  - `Argument`, `Field`, `Path`, `Constant`
  - and a bounded set of pure transforms

### 3.3 No query-as-string execution

A Policy MUST NOT permit any construct that causes a string literal (or other value) to be interpreted as executable query text.

This rule is a restatement of the Behavior Dialect safety boundary.

---

## 4. Resource Limits (Normative)

### 4.1 Limit profile

A Policy MUST include a **LimitProfile**.

A LimitProfile is an evaluation parameter set that bounds computation.

Required limits:

- `maximumExpressionDepth`
- `maximumListLength`
- `maximumRecordFieldCount`
- `maximumOutputListLength`
- `maximumJoinInputListLength`

Optional limits (recommended):

- `maximumIntermediateListLength`
- `maximumSortKeyEvaluationCount`

Optional limits (recommended for relational transforms):

- `maximumGroupCount`
- `maximumGroupSize`

Optional limits (recommended for string transforms):

- `maximumStringLength`
- `maximumOutputStringLength`

All limits are non-negative integers.

### 4.2 Determinism and stability

- For a fixed Program, input data, and active Policy (including limits), evaluation MUST be deterministic.
- If a limit is exceeded, evaluation MUST return `Invalid(...)` and MUST NOT partially return results.

### 4.3 Enforcement points

A runtime MUST enforce limits at observable boundaries:

- before iterating a list, validate `maximumListLength`
- before allocating or emitting an output list, validate `maximumOutputListLength`
- before joining two lists, validate `maximumJoinInputListLength`
- during grouping, validate `maximumGroupCount` and `maximumGroupSize` if present
- before scanning or splitting a string, validate `maximumStringLength` if present
- before emitting a string result, validate `maximumOutputStringLength` if present
- before emitting or merging records, validate `maximumRecordFieldCount`

---

## 6. Canonical Policy Encoding (Normative)

Policies MAY be represented as Codex values for portability and static validation.

### 6.1 Policy record shape

A Policy value MUST be a Codex `Record` with these keys:

- `allowedOperations` (List of `Text`) — an allowlist of Behavior operation tokens.
- `limits` (Record) — the LimitProfile.

No other keys are permitted.

`allowedOperations` rules (Normative):

- The list MUST be interpreted as a set; ordering is not semantically significant.
- The list MUST NOT contain duplicates.
- Each element MUST be a known v0.1 Behavior operation token.
- If any element is unknown for v0.1, the Policy value is invalid and MUST be rejected.

Example:

```codex
{
  "allowedOperations": [
    "Argument",
    "Field",
    "Path",
    "Constant",
    "MapElements",
    "FilterElements",
    "SortElementsBy",
    "MergeRecords"
  ],
  "limits": {
    "maximumExpressionDepth": 64,
    "maximumListLength": 10000,
    "maximumRecordFieldCount": 200,
    "maximumOutputListLength": 10000,
    "maximumJoinInputListLength": 5000,
    "maximumIntermediateListLength": 20000,
    "maximumSortKeyEvaluationCount": 10000,
    "maximumGroupCount": 1000,
    "maximumGroupSize": 10000,
    "maximumStringLength": 20000,
    "maximumOutputStringLength": 20000
  }
}
```

### 6.2 LimitProfile record shape

`limits` MUST be a Codex `Record` that contains:

Required keys:

- `maximumExpressionDepth`
- `maximumListLength`
- `maximumRecordFieldCount`
- `maximumOutputListLength`
- `maximumJoinInputListLength`

Optional keys:

- `maximumIntermediateListLength`
- `maximumSortKeyEvaluationCount`
- `maximumGroupCount`
- `maximumGroupSize`
- `maximumStringLength`
- `maximumOutputStringLength`

All limit values MUST be `Integer` and MUST be non-negative.

Missing optional keys MUST be treated as “no additional restriction beyond required limits”.

---

## 5. Capability and Applicability (Informative)

A Policy can be treated as a capability set.

This enables:

- static rejection of forbidden surfaces
- safe subset selection per target
- declarative applicability reasoning

This spec does not mandate a particular triple representation, but it is designed to be enforceable by structural constraints.

---

**End of Behavior Program Policy and Resource Limits v0.1**
