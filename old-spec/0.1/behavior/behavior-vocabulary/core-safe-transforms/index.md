Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Core Safe Transforms

This specification defines the v0.1 **Core Safe transform operators**.

This document is **Normative**.

---

## 1. Purpose

These operators provide bounded, deterministic collection and record transforms without introducing eval, dynamic code construction, or ambient dependencies.

---

## 2. Shared Definitions (Normative)

### 2.1 Value model terms

- `List` — an ordered collection value.
- `Record` — a key/value mapping with `Text` keys.
- `<Absent/>` — the canonical missing-value concept.

### 2.2 Evaluation contract

- Each operator takes one or more **expressions** as operands.
- Each operand evaluates to `Validation<Value>`.
- Unless explicitly stated, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)`.

### 2.3 Failure vs missingness

- Operators MUST NOT encode failures as `<Absent/>`.
- If a required domain constraint is violated (wrong type, missing required value, non-comparable keys, duplicates where forbidden), the result MUST be `Invalid(...)`.

Diagnostic code rule (Normative):

- Where this specification requires an `Invalid(...)` produced by the operator itself (not propagated from an operand), the diagnostic code MUST be the corresponding code defined by Behavior Diagnostic Codes.

### 2.4 Determinism

- Output ordering MUST be deterministic.
- Where ordering is defined as “stable”, it MUST preserve relative input order for equal keys.

### 2.5 Resource-boundedness (Normative)

These operators are intended to be safe to evaluate in constrained environments.

Normative rules:

- Evaluators MUST enforce a stable, explicit resource policy for Behavior evaluation.
- In particular, evaluation MUST be bounded by limits that constrain collection size, output size, and join/sort cost.

Policy reference:

- The canonical policy and limit model is defined by `Behavior Program Policy and Resource Limits`.

Failure behavior:

- If a Core Safe Transform would exceed an active limit profile, the result MUST be `Invalid(...)` with code `CoreSafeTransforms::LIMIT_EXCEEDED`.
- Limit failures MUST NOT be encoded as `<Absent/>`.
- Limit failures MUST be deterministic for a fixed Program, input values, and active policy.

---

## 3. Operators (Normative)

### 3.1 `MapElements`

Name: `MapElements`

Arity: 2

Domains:

- `MapElements(listExpr, mapExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`mapExpr` MUST be a Behavior expression that is evaluated once per element, with the following binding rule:

- For each element `e`, `mapExpr` is evaluated with `Argument := e`.

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. For each element of the list in input order:
   - evaluate `mapExpr` with `Argument := element`.
3. If all element evaluations are `Valid(v)`, return `Valid(List(v...))` in the same order.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `MapElements::NEED_LIST`.
- If any element mapping evaluation yields `Invalid(...)`, return `Invalid(...)`.

Observability constraint:

- `mapExpr` MUST be evaluated exactly once per element.

---

### 3.2 `FilterElements`

Name: `FilterElements`

Arity: 2

Domains:

- `FilterElements(listExpr, predicateExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`predicateExpr` MUST be a Behavior expression that is evaluated once per element, with the following binding rule:

- For each element `e`, `predicateExpr` is evaluated with `Argument := e`.

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. For each element of the list in input order:
   - evaluate `predicateExpr` with `Argument := element`.
   - if the result is `Valid(true)`, include the element.
   - if the result is `Valid(false)`, exclude the element.
3. Return the included elements in original order.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `FilterElements::NEED_LIST`.
- If any predicate evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any predicate evaluation yields `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `FilterElements::NEED_BOOLEAN`.

Observability constraint:

- `predicateExpr` MUST be evaluated exactly once per element.

---

### 3.2A `FindAllElements`

Name: `FindAllElements`

Arity: 2

Domains:

- `FindAllElements(listExpr, predicateExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`predicateExpr` MUST be a Behavior expression that is evaluated once per element, with the following binding rule:

- For each element `e`, `predicateExpr` is evaluated with `Argument := e`.

Result:

- `Validation<List>`

Semantics:

- `FindAllElements` is equivalent to `FilterElements`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `FindAllElements::NEED_LIST`.
- If any predicate evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any predicate evaluation yields `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `FindAllElements::NEED_BOOLEAN`.

Observability constraint:

- `predicateExpr` MUST be evaluated exactly once per element.

---

### 3.3 `FindFirstElement`

Name: `FindFirstElement`

Arity: 2

Domains:

- `FindFirstElement(listExpr, predicateExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`predicateExpr` MUST be a Behavior expression evaluated with:

- `Argument := element`

Result:

- `Validation<Value>`

Semantics:

1. Evaluate `listExpr`.
2. Iterate elements in input order; for each element:
   - evaluate `predicateExpr`.
   - on `Valid(true)`, return `Valid(element)`.
   - on `Valid(false)`, continue.
3. If no element matches, return `Valid(<Absent/>)`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `FindFirstElement::NEED_LIST`.
- If any predicate evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any predicate evaluation yields `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `FindFirstElement::NEED_BOOLEAN`.

---

### 3.4 `SortElementsBy`

Name: `SortElementsBy`

Arity: 2

Domains:

- `SortElementsBy(listExpr, keyExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`keyExpr` MUST be a Behavior expression evaluated per element with:

- `Argument := element`

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. For each element in input order, evaluate `keyExpr` once and collect `(element, key)`.
3. Sort elements by `key` with these rules:
   - the sort MUST be stable.
   - elements whose key is `Valid(<Absent/>)` MUST sort last.
   - keys MUST be comparable; if any pair of non-`<Absent/>` keys are not comparable under Value Ordering and Structural Equality, return `Invalid(...)` with code `SortElementsBy::NEED_COMPARABLE_KEYS`.
4. Return the sorted elements.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `SortElementsBy::NEED_LIST`.
- If any key evaluation yields `Invalid(...)`, return `Invalid(...)`.

Observability constraint:

- `keyExpr` MUST be evaluated exactly once per element.

---

### 3.4A `TakeFirstElements`

Name: `TakeFirstElements`

Arity: 2

Domains:

- `TakeFirstElements(listExpr, countExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.
- `countExpr` MUST evaluate to `Valid(Integer)`.

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. Evaluate `countExpr`.
3. If `count` is negative, return `Invalid(...)`.
4. Return a list containing the first `count` elements of the input list (or the entire list if `count` exceeds length), preserving input order.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `TakeFirstElements::NEED_LIST`.
- If `countExpr` is not an `Integer`, return `Invalid(...)` with code `TakeFirstElements::NEED_INTEGER_COUNT`.
- If `count` is negative, return `Invalid(...)` with code `TakeFirstElements::NEED_NONNEGATIVE_COUNT`.

---

### 3.4B `DropFirstElements`

Name: `DropFirstElements`

Arity: 2

Domains:

- `DropFirstElements(listExpr, countExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.
- `countExpr` MUST evaluate to `Valid(Integer)`.

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. Evaluate `countExpr`.
3. If `count` is negative, return `Invalid(...)`.
4. Drop the first `count` elements of the list. If `count` exceeds length, return an empty list.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `DropFirstElements::NEED_LIST`.
- If `countExpr` is not an `Integer`, return `Invalid(...)` with code `DropFirstElements::NEED_INTEGER_COUNT`.
- If `count` is negative, return `Invalid(...)` with code `DropFirstElements::NEED_NONNEGATIVE_COUNT`.

---

### 3.5 `MergeRecords`

Name: `MergeRecords`

Arity: 2 or more

Domains:

- `MergeRecords(recordExpr...)`
- Every `recordExpr` MUST evaluate to `Valid(Record)`.

Result:

- `Validation<Record>`

Semantics:

1. Evaluate operands left-to-right.
2. Construct a new output record.
3. For each input record in order, for each key in that record:
   - if the key is not present in the output record, add it.
   - if the key is already present in the output record, return `Invalid(...)` (InvalidOnCollision).

Error behavior:

- If any operand is not a `Record`, return `Invalid(...)` with code `MergeRecords::NEED_RECORD`.
- On any key collision, return `Invalid(...)` with code `MergeRecords::KEY_COLLISION_HIT_SNAG`.

---

### 3.5A `DistinctElements`

Name: `DistinctElements`

Arity: 1

Domains:

- `DistinctElements(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<List>`

Semantics:

1. Evaluate `listExpr`.
2. Scan elements in input order.
3. Emit each element the first time it appears under structural equality.
4. Preserve input order of first occurrences.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `DistinctElements::NEED_LIST`.

---

### 3.5B `FlattenElements`

Name: `FlattenElements`

Arity: 1

Domains:

- `FlattenElements(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<List>`

Semantics:

This operation flattens exactly one level.

1. Evaluate `listExpr`.
2. For each element in input order:
   - if the element is a `List`, append its elements in order.
   - otherwise return `Invalid(...)`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `FlattenElements::NEED_LIST`.
- If any element is not a `List`, return `Invalid(...)` with code `FlattenElements::NEED_LIST_ELEMENTS`.

---

### 3.5C `CountElements`

Name: `CountElements`

Arity: 1

Domains:

- `CountElements(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<Integer>`

Semantics:

1. Evaluate `listExpr`.
2. Return the element count as an `Integer`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `CountElements::NEED_LIST`.

---

### 3.5D `SumElements`

Name: `SumElements`

Arity: 1

Domains:

- `SumElements(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Clarification (Normative):

- `<Absent/>` is not in `OrderableNumber`. If any element is `<Absent/>`, `SumElements(...)` MUST return `Invalid(...)` with code `SumElements::NEED_ORDERABLE_NUMBER_ELEMENTS`.

Result:

- `Validation<Value>`

Semantics:

1. Evaluate `listExpr`.
2. If the list is empty, return `Valid(0)`.
3. Otherwise, if every element of the list is in `OrderableNumber`, return the arithmetic sum as defined by `Math::Add` applied to the list elements.

Clarification (Normative):

- This specification defines `SumElements` using the semantics of `Math::Add`.
- This definitional reference does not imply that a Behavior Program invokes a Math operation token.
- Allowlisting decisions MUST be made on the operation token present in the Program (`SumElements`), not on definitional references in prose.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `SumElements::NEED_LIST`.
- If any element is not in `OrderableNumber`, return `Invalid(...)` with code `SumElements::NEED_ORDERABLE_NUMBER_ELEMENTS`.

---

### 3.5E `MinimumElement`

Name: `MinimumElement`

Arity: 1

Domains:

- `MinimumElement(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<Value>`

Semantics:

1. Evaluate `listExpr`.
2. If the list is empty, return `Valid(<Absent/>)`.
3. Otherwise, determine the minimum element under the v0.1 ordering rules.
4. If more than one element is equal to the minimum, return the first such element in input order.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `MinimumElement::NEED_LIST`.
- If any element is `<Absent/>`, return `Invalid(...)` with code `MinimumElement::NEED_NONABSENT_ELEMENTS`.
- If any comparison required to determine the minimum is NotComparable under Value Ordering and Structural Equality, return `Invalid(...)` with code `MinimumElement::NEED_MUTUALLY_COMPARABLE_ELEMENTS`.

---

### 3.5F `MaximumElement`

Name: `MaximumElement`

Arity: 1

Domains:

- `MaximumElement(listExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<Value>`

Semantics:

1. Evaluate `listExpr`.
2. If the list is empty, return `Valid(<Absent/>)`.
3. Otherwise, determine the maximum element under the v0.1 ordering rules.
4. If more than one element is equal to the maximum, return the first such element in input order.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `MaximumElement::NEED_LIST`.
- If any element is `<Absent/>`, return `Invalid(...)` with code `MaximumElement::NEED_NONABSENT_ELEMENTS`.
- If any comparison required to determine the maximum is NotComparable under Value Ordering and Structural Equality, return `Invalid(...)` with code `MaximumElement::NEED_MUTUALLY_COMPARABLE_ELEMENTS`.

---

### 3.5G `SelectFields`

Name: `SelectFields`

Arity: 2

Domains:

- `SelectFields(recordExpr, fieldNameListExpr)`
- `recordExpr` MUST evaluate to `Valid(Record)`.
- `fieldNameListExpr` MUST evaluate to `Valid(List)`.

Result:

- `Validation<Record>`

Semantics:

This operator projects a record into a new record using an explicit, ordered list of field names.

1. Evaluate `recordExpr`.
2. Evaluate `fieldNameListExpr`.
3. If any element of `fieldNameListExpr` is not `Text`, return `Invalid(...)`.
4. If `fieldNameListExpr` contains duplicates, return `Invalid(...)`.
5. Construct a new output record whose keys are exactly the names in `fieldNameListExpr`, in list order.
6. For each selected name `k`:
   - If the input record contains key `k`, copy its value.
   - Otherwise set `k` to `<Absent/>` in the output.

Error behavior:

- If `recordExpr` is not a `Record`, return `Invalid(...)` with code `SelectFields::NEED_RECORD`.
- If `fieldNameListExpr` is not a `List`, return `Invalid(...)` with code `SelectFields::NEED_LIST`.
- If any selected field name is not `Text`, return `Invalid(...)` with code `SelectFields::NEED_TEXT_FIELD_NAMES`.
- If `fieldNameListExpr` contains duplicates, return `Invalid(...)` with code `SelectFields::NEED_DISTINCT_FIELD_NAMES`.

---

### 3.5H `SplitString`

Name: `SplitString`

Arity: 2

Domains:

- `SplitString(textExpr, separatorExpr)`
- `textExpr` MUST evaluate to `Valid(Text)`.
- `separatorExpr` MUST evaluate to `Valid(Text)`.

Result:

- `Validation<List>`

Semantics:

This operator splits a string into substrings delimited by an exact separator.

1. Evaluate `textExpr` and `separatorExpr`.
2. If `separator` is the empty string, return `Invalid(...)`.
3. Split `text` on non-overlapping occurrences of `separator`, scanning left-to-right.
4. Return `Valid(List(parts...))` where each part is `Text`.

Empty substrings are permitted.

Error behavior:

- If `textExpr` is not `Text`, return `Invalid(...)` with code `SplitString::NEED_TEXT`.
- If `separatorExpr` is not `Text`, return `Invalid(...)` with code `SplitString::NEED_TEXT_SEPARATOR`.
- If `separator` is empty, return `Invalid(...)` with code `SplitString::NEED_NONEMPTY_SEPARATOR`.

Limit behavior:

- Evaluators MUST enforce `maximumOutputListLength` on the emitted parts list.
- If `maximumStringLength` or `maximumOutputStringLength` are present in the active LimitProfile, evaluators MUST enforce them. Any such limit failure MUST return `Invalid(...)` with code `CoreSafeTransforms::LIMIT_EXCEEDED`.

---

### 3.5I `JoinStrings`

Name: `JoinStrings`

Arity: 2

Domains:

- `JoinStrings(textListExpr, separatorExpr)`
- `textListExpr` MUST evaluate to `Valid(List)`.
- `separatorExpr` MUST evaluate to `Valid(Text)`.

Result:

- `Validation<Text>`

Semantics:

1. Evaluate `textListExpr` and `separatorExpr`.
2. If any element of `textListExpr` is not `Text`, return `Invalid(...)`.
3. Concatenate elements in list order, inserting `separator` between adjacent elements.
4. Return the resulting `Text`.

Error behavior:

- If `textListExpr` is not a `List`, return `Invalid(...)` with code `JoinStrings::NEED_LIST`.
- If `separatorExpr` is not `Text`, return `Invalid(...)` with code `JoinStrings::NEED_TEXT_SEPARATOR`.
- If any element of `textListExpr` is not `Text`, return `Invalid(...)` with code `JoinStrings::NEED_TEXT_ELEMENTS`.

Limit behavior:

- If `maximumStringLength` or `maximumOutputStringLength` are present in the active LimitProfile, evaluators MUST enforce them. Any such limit failure MUST return `Invalid(...)` with code `CoreSafeTransforms::LIMIT_EXCEEDED`.

---

### 3.6 `JoinCollectionsOnKey`

Name: `JoinCollectionsOnKey`

Arity: 4

Domains:

- `JoinCollectionsOnKey(leftListExpr, rightListExpr, leftKeyExpr, rightKeyExpr)`
- `leftListExpr` and `rightListExpr` MUST evaluate to `Valid(List)`.

`leftKeyExpr` is evaluated per left element with:

- `Argument := leftElement`

`rightKeyExpr` is evaluated per right element with:

- `Argument := rightElement`

Result:

- `Validation<List>`

Semantics:

This operator is a keyed **inner join**.

1. Evaluate `leftListExpr` and `rightListExpr`.
2. Compute left keys by evaluating `leftKeyExpr` once per left element.
3. Compute right keys by evaluating `rightKeyExpr` once per right element.
4. Duplicate rejection:
   - if any left key is `<Absent/>`, return `Invalid(...)`.
   - if any right key is `<Absent/>`, return `Invalid(...)`.
   - if the left side contains duplicate keys (under structural equality defined by Value Ordering and Structural Equality), return `Invalid(...)`.
   - if the right side contains duplicate keys (under structural equality defined by Value Ordering and Structural Equality), return `Invalid(...)`.
5. For each left element in left input order:
   - if there exists a right element with the same key, emit a joined record.
6. Join output ordering MUST be deterministic and MUST behave observably as:
   - left-order primary
   - right-order secondary (trivial under RejectDuplicates)

Join output element shape:

- Each joined element MUST be a `Record` with exactly two keys:
  - `left` -> the left element
  - `right` -> the right element

Error behavior:

- If either side is not a `List`, return `Invalid(...)` with code `JoinCollectionsOnKey::NEED_LIST`.
- If any key evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any key is `<Absent/>`, return `Invalid(...)` with code `JoinCollectionsOnKey::NEED_NONABSENT_KEY`.
- If duplicate keys exist on either side, return `Invalid(...)` with code `JoinCollectionsOnKey::DUPLICATE_KEY_HIT_SNAG`.

---

### 3.6A `GroupElementsByKey`

Name: `GroupElementsByKey`

Arity: 2

Domains:

- `GroupElementsByKey(listExpr, keyExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`keyExpr` MUST be a Behavior expression evaluated per element with:

- `Argument := element`

Result:

- `Validation<List>`

Semantics:

This operator partitions a list into groups using structural equality on computed keys.

1. Evaluate `listExpr`.
2. For each element in input order, evaluate `keyExpr` exactly once and collect `(element, key)`.
3. Key validity:
   - if any key is `Valid(<Absent/>)`, return `Invalid(...)`.
4. Grouping:
   - elements are grouped by structural equality of `key`.
   - groups are ordered by the first appearance of their key in the input.
   - within each group, elements preserve their original input order.
5. Emit a list of group records. Each group record MUST be a `Record` with exactly two keys:
   - `key` -> the group key value
   - `elements` -> a `List` of the grouped elements

Limit enforcement (Normative):

- If `maximumGroupCount` is present in the active LimitProfile, evaluation MUST fail (as a limit failure) if the number of distinct group keys would exceed it.
- If `maximumGroupSize` is present in the active LimitProfile, evaluation MUST fail (as a limit failure) if any group’s element count would exceed it.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `GroupElementsByKey::NEED_LIST`.
- If any key evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any key is `<Absent/>`, return `Invalid(...)` with code `GroupElementsByKey::NEED_NONABSENT_KEY`.

Observability constraint:

- `keyExpr` MUST be evaluated exactly once per element.

---

### 3.7 `AnyElementSatisfies`

Name: `AnyElementSatisfies`

Arity: 2

Domains:

- `AnyElementSatisfies(listExpr, predicateExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`predicateExpr` MUST be a Behavior expression evaluated once per element with:

- `Argument := element`

Result:

- `Validation<boolean>`

Semantics:

1. Evaluate `listExpr`.
2. Evaluate `predicateExpr` once per element, in input order.
3. Return `Valid(true)` iff any element yields `Valid(true)`.
4. Otherwise return `Valid(false)`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `AnyElementSatisfies::NEED_LIST`.
- If any predicate evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any predicate evaluation yields `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `AnyElementSatisfies::NEED_BOOLEAN`.

Observability constraint:

- `predicateExpr` MUST be evaluated exactly once per element.

---

### 3.8 `AllElementsSatisfy`

Name: `AllElementsSatisfy`

Arity: 2

Domains:

- `AllElementsSatisfy(listExpr, predicateExpr)`
- `listExpr` MUST evaluate to `Valid(List)`.

`predicateExpr` MUST be a Behavior expression evaluated once per element with:

- `Argument := element`

Result:

- `Validation<boolean>`

Semantics:

1. Evaluate `listExpr`.
2. Evaluate `predicateExpr` once per element, in input order.
3. Return `Valid(false)` iff any element yields `Valid(false)`.
4. Otherwise return `Valid(true)`.

Error behavior:

- If `listExpr` is not a `List`, return `Invalid(...)` with code `AllElementsSatisfy::NEED_LIST`.
- If any predicate evaluation yields `Invalid(...)`, return `Invalid(...)`.
- If any predicate evaluation yields `Valid(x)` where `x` is not `Boolean`, return `Invalid(...)` with code `AllElementsSatisfy::NEED_BOOLEAN`.

Observability constraint:

- `predicateExpr` MUST be evaluated exactly once per element.

---

**End of Behavior Vocabulary — Core Safe Transforms v0.1**
