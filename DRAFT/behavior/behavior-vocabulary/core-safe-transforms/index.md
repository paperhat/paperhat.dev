Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Vocabulary — Core Safe Transforms

This specification defines the **Core Safe transform operators** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

These operators provide bounded, deterministic collection and record transforms. They enable practical functional programming patterns (map, filter, reduce, etc.) while remaining closed-world, bounded, and deterministic.

---

## 2. Shared Definitions (Normative)

### 2.1 Value Model Terms

- `List` — ordered collection, may contain duplicates
- `Set` — unordered collection, unique elements
- `Tuple` — ordered, fixed-length, positional semantics
- `Map` — key-value collection with unique keys
- `Record` — key-value structure with Text keys
- `Range` — declarative interval with start, end, optional step
- `<Absent/>` — canonical missing-value concept

### 2.2 Evaluation Contract

- Each operator takes one or more **expressions** as operands.
- Each operand evaluates to `Validation<Value>`.
- Unless explicitly stated, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)`.

### 2.3 Failure vs Missingness

- Operators MUST NOT encode failures as `<Absent/>`.
- If a required domain constraint is violated, the result MUST be `Invalid(...)`.

Diagnostic code rule:
- Where this specification requires an `Invalid(...)`, it MUST use the corresponding code defined by Behavior Diagnostic Codes.

### 2.4 Determinism

- Output ordering MUST be deterministic.
- Where ordering is defined as "stable", it MUST preserve relative input order for equal keys.

### 2.5 Resource Boundedness

Evaluators MUST enforce limits to prevent resource exhaustion:
- Maximum collection length
- Maximum output size
- Maximum iteration count

If a transform exceeds limits, the result MUST be `Invalid(...)` with code `CoreSafeTransforms::LIMIT_EXCEEDED`.

---

## 3. List Operations (Normative)

### 3.1 `MapElements`

Arity: 2

```
MapElements(list, mapExpr) -> List
```

Semantics:
1. Evaluate `list`.
2. For each element in order, evaluate `mapExpr` with `Argument := element`.
3. Return a new List of results in the same order.

Error behavior:
- If `list` is not a List: `Invalid(...)` with code `MapElements::NEED_LIST`.
- If any mapping yields `Invalid(...)`: propagate.

### 3.2 `FilterElements`

Arity: 2

```
FilterElements(list, predicateExpr) -> List
```

Semantics:
1. For each element, evaluate `predicateExpr` with `Argument := element`.
2. Include elements where predicate returns `Valid(true)`.
3. Preserve original order.

Error behavior:
- If `list` is not a List: `Invalid(...)` with code `FilterElements::NEED_LIST`.
- If predicate returns non-Boolean: `Invalid(...)` with code `FilterElements::NEED_BOOLEAN`.

### 3.3 `ReduceElements`

Arity: 3

```
ReduceElements(list, initialValue, reduceExpr) -> Value
```

Semantics:
1. Start with `accumulator := initialValue`.
2. For each element in order:
   - Evaluate `reduceExpr` with environment `{ accumulator, element }`.
   - Set `accumulator := result`.
3. Return final accumulator.

Error behavior:
- If `list` is not a List: `Invalid(...)` with code `ReduceElements::NEED_LIST`.

### 3.4 `ReduceElementsRight`

Arity: 3

```
ReduceElementsRight(list, initialValue, reduceExpr) -> Value
```

Semantics:
- Same as `ReduceElements` but processes elements right-to-left.

### 3.5 `FoldElements`

Arity: 2

```
FoldElements(list, foldExpr) -> Value
```

Semantics:
1. If list is empty, return `Invalid(...)`.
2. Start with `accumulator := first element`.
3. For remaining elements, evaluate `foldExpr` with `{ accumulator, element }`.
4. Return final accumulator.

Error behavior:
- If `list` is empty: `Invalid(...)` with code `FoldElements::NEED_NONEMPTY_LIST`.

### 3.6 `FindFirstElement`

Arity: 2

```
FindFirstElement(list, predicateExpr) -> Value
```

Semantics:
1. Iterate in order, evaluate predicate for each element.
2. Return first element where predicate is `Valid(true)`.
3. If none match, return `Valid(<Absent/>)`.

### 3.7 `FindLastElement`

Arity: 2

```
FindLastElement(list, predicateExpr) -> Value
```

Semantics:
- Return last element where predicate is true.

### 3.8 `FindAllElements`

Arity: 2

```
FindAllElements(list, predicateExpr) -> List
```

Semantics:
- Equivalent to `FilterElements`.

### 3.9 `SortElements`

Arity: 1

```
SortElements(list) -> List
```

Semantics:
- Sort elements using natural ordering.
- Elements must be mutually comparable.

Error behavior:
- If elements are not comparable: `Invalid(...)` with code `SortElements::NEED_COMPARABLE_ELEMENTS`.

### 3.10 `SortElementsBy`

Arity: 2

```
SortElementsBy(list, keyExpr) -> List
```

Semantics:
1. For each element, evaluate `keyExpr` with `Argument := element`.
2. Sort by keys (stable sort).
3. Elements with `<Absent/>` keys sort last.

Error behavior:
- If keys are not comparable: `Invalid(...)` with code `SortElementsBy::NEED_COMPARABLE_KEYS`.

### 3.11 `SortElementsDescending`

Arity: 1

```
SortElementsDescending(list) -> List
```

### 3.12 `SortElementsByDescending`

Arity: 2

```
SortElementsByDescending(list, keyExpr) -> List
```

### 3.13 `ReverseElements`

Arity: 1

```
ReverseElements(list) -> List
```

### 3.14 `TakeFirstElements`

Arity: 2

```
TakeFirstElements(list, count) -> List
```

Semantics:
- Return first `count` elements.
- If count > length, return entire list.

### 3.15 `TakeLastElements`

Arity: 2

```
TakeLastElements(list, count) -> List
```

### 3.16 `TakeWhile`

Arity: 2

```
TakeWhile(list, predicateExpr) -> List
```

Semantics:
- Take elements from start while predicate is true.
- Stop at first false.

### 3.17 `DropFirstElements`

Arity: 2

```
DropFirstElements(list, count) -> List
```

### 3.18 `DropLastElements`

Arity: 2

```
DropLastElements(list, count) -> List
```

### 3.19 `DropWhile`

Arity: 2

```
DropWhile(list, predicateExpr) -> List
```

### 3.20 `SliceElements`

Arity: 3

```
SliceElements(list, startIndex, endIndex) -> List
```

Semantics:
- Return elements from startIndex (inclusive) to endIndex (exclusive).
- Indices are zero-based.
- Negative indices count from end.

### 3.21 `ChunkElements`

Arity: 2

```
ChunkElements(list, size) -> List<List>
```

Semantics:
- Split into chunks of specified size.
- Last chunk may be smaller.

### 3.22 `WindowElements`

Arity: 2

```
WindowElements(list, size) -> List<List>
```

Semantics:
- Sliding window of specified size.
- Returns List of overlapping windows.

### 3.23 `DistinctElements`

Arity: 1

```
DistinctElements(list) -> List
```

Semantics:
- Remove duplicates (first occurrence wins).
- Preserve order of first occurrences.

### 3.24 `DistinctElementsBy`

Arity: 2

```
DistinctElementsBy(list, keyExpr) -> List
```

Semantics:
- Remove duplicates by key.

### 3.25 `FlattenElements`

Arity: 1

```
FlattenElements(list) -> List
```

Semantics:
- Flatten one level (List of Lists -> List).

Error behavior:
- If any element is not a List: `Invalid(...)` with code `FlattenElements::NEED_LIST_ELEMENTS`.

### 3.26 `FlatMapElements`

Arity: 2

```
FlatMapElements(list, mapExpr) -> List
```

Semantics:
- Map then flatten.
- `mapExpr` must return Lists.

### 3.27 `ZipElements`

Arity: 2

```
ZipElements(list1, list2) -> List<Tuple>
```

Semantics:
- Combine element-wise into Tuples.
- Length is minimum of inputs.

### 3.28 `ZipElementsWith`

Arity: 3

```
ZipElementsWith(list1, list2, combineExpr) -> List
```

Semantics:
- Combine using custom expression.
- `combineExpr` receives `{ first, second }`.

### 3.29 `UnzipElements`

Arity: 1

```
UnzipElements(listOfTuples) -> Tuple<List, List>
```

Semantics:
- Inverse of zip.

### 3.30 `ConcatenateElements`

Arity: 2 or more

```
ConcatenateElements(list1, list2, ...) -> List
```

### 3.31 `InterleaveLists`

Arity: 2

```
InterleaveLists(list1, list2) -> List
```

Semantics:
- Alternate elements from each list.

### 3.32 `PartitionElements`

Arity: 2

```
PartitionElements(list, predicateExpr) -> Record { passing, failing }
```

Semantics:
- Split into two lists based on predicate.

### 3.33 `GroupElementsByKey`

Arity: 2

```
GroupElementsByKey(list, keyExpr) -> List<Record { key, elements }>
```

Semantics:
- Group elements by computed key.
- Groups ordered by first appearance.
- Elements within groups preserve original order.

Error behavior:
- If any key is `<Absent/>`: `Invalid(...)` with code `GroupElementsByKey::NEED_NONABSENT_KEY`.

### 3.34 `IndexElements`

Arity: 1

```
IndexElements(list) -> List<Tuple<Integer, Value>>
```

Semantics:
- Pair each element with its index.

---

## 4. Aggregation (Normative)

### 4.1 `CountElements`

Arity: 1

```
CountElements(list) -> Integer
```

### 4.2 `CountElementsWhere`

Arity: 2

```
CountElementsWhere(list, predicateExpr) -> Integer
```

### 4.3 `SumElements`

Arity: 1

```
SumElements(list) -> Number
```

Error behavior:
- If any element is not numeric: `Invalid(...)` with code `SumElements::NEED_NUMERIC_ELEMENTS`.

### 4.4 `ProductElements`

Arity: 1

```
ProductElements(list) -> Number
```

### 4.5 `MinimumElement`

Arity: 1

```
MinimumElement(list) -> Value
```

Semantics:
- If empty, return `<Absent/>`.
- If multiple equal minimum, return first.

### 4.6 `MaximumElement`

Arity: 1

```
MaximumElement(list) -> Value
```

### 4.7 `MinimumElementBy`

Arity: 2

```
MinimumElementBy(list, keyExpr) -> Value
```

### 4.8 `MaximumElementBy`

Arity: 2

```
MaximumElementBy(list, keyExpr) -> Value
```

### 4.9 `AverageElements`

Arity: 1

```
AverageElements(list) -> Number
```

Semantics:
- Arithmetic mean.
- Empty list returns `Invalid(...)`.

---

## 5. Predicates (Normative)

### 5.1 `AnyElementSatisfies`

Arity: 2

```
AnyElementSatisfies(list, predicateExpr) -> Boolean
```

### 5.2 `AllElementsSatisfy`

Arity: 2

```
AllElementsSatisfy(list, predicateExpr) -> Boolean
```

### 5.3 `NoElementSatisfies`

Arity: 2

```
NoElementSatisfies(list, predicateExpr) -> Boolean
```

### 5.4 `ContainsElement`

Arity: 2

```
ContainsElement(list, element) -> Boolean
```

### 5.5 `IsEmpty`

Arity: 1

```
IsEmpty(collection) -> Boolean
```

Works on List, Set, Map, Record.

### 5.6 `IsNotEmpty`

Arity: 1

```
IsNotEmpty(collection) -> Boolean
```

---

## 6. Set Operations (Normative)

### 6.1 `SetUnion`

Arity: 2

```
SetUnion(set1, set2) -> Set
```

### 6.2 `SetIntersection`

Arity: 2

```
SetIntersection(set1, set2) -> Set
```

### 6.3 `SetDifference`

Arity: 2

```
SetDifference(set1, set2) -> Set
```

Semantics:
- Elements in set1 but not in set2.

### 6.4 `SetSymmetricDifference`

Arity: 2

```
SetSymmetricDifference(set1, set2) -> Set
```

Semantics:
- Elements in either but not both.

### 6.5 `IsSubsetOf`

Arity: 2

```
IsSubsetOf(set1, set2) -> Boolean
```

### 6.6 `IsSupersetOf`

Arity: 2

```
IsSupersetOf(set1, set2) -> Boolean
```

### 6.7 `IsProperSubsetOf`

Arity: 2

```
IsProperSubsetOf(set1, set2) -> Boolean
```

### 6.8 `IsProperSupersetOf`

Arity: 2

```
IsProperSupersetOf(set1, set2) -> Boolean
```

### 6.9 `SetsAreDisjoint`

Arity: 2

```
SetsAreDisjoint(set1, set2) -> Boolean
```

### 6.10 `SetsOverlap`

Arity: 2

```
SetsOverlap(set1, set2) -> Boolean
```

### 6.11 `SetContains`

Arity: 2

```
SetContains(set, element) -> Boolean
```

### 6.12 `SetAdd`

Arity: 2

```
SetAdd(set, element) -> Set
```

Semantics:
- Returns new Set with element added (no-op if already present).

### 6.13 `SetRemove`

Arity: 2

```
SetRemove(set, element) -> Set
```

### 6.14 `SetSize`

Arity: 1

```
SetSize(set) -> Integer
```

### 6.15 `ListToSet`

Arity: 1

```
ListToSet(list) -> Set
```

### 6.16 `SetToList`

Arity: 1

```
SetToList(set) -> List
```

Semantics:
- Order is deterministic but unspecified.

---

## 7. Map Operations (Normative)

### 7.1 `MapGet`

Arity: 2

```
MapGet(map, key) -> Value
```

Semantics:
- Returns value for key, or `<Absent/>` if not present.

### 7.2 `MapGetOrDefault`

Arity: 3

```
MapGetOrDefault(map, key, defaultValue) -> Value
```

### 7.3 `MapContainsKey`

Arity: 2

```
MapContainsKey(map, key) -> Boolean
```

### 7.4 `MapContainsValue`

Arity: 2

```
MapContainsValue(map, value) -> Boolean
```

### 7.5 `MapKeys`

Arity: 1

```
MapKeys(map) -> Set
```

### 7.6 `MapValues`

Arity: 1

```
MapValues(map) -> List
```

### 7.7 `MapEntries`

Arity: 1

```
MapEntries(map) -> List<Record { key, value }>
```

### 7.8 `MapSet`

Arity: 3

```
MapSet(map, key, value) -> Map
```

Semantics:
- Returns new Map with key set to value (insert or update).

### 7.9 `MapRemove`

Arity: 2

```
MapRemove(map, key) -> Map
```

### 7.10 `MapMerge`

Arity: 2

```
MapMerge(map1, map2) -> Map
```

Semantics:
- Merge maps. map2 values win on collision.

### 7.11 `MapMergeWith`

Arity: 3

```
MapMergeWith(map1, map2, resolveExpr) -> Map
```

Semantics:
- On collision, evaluate `resolveExpr` with `{ key, value1, value2 }`.

### 7.12 `MapMapValues`

Arity: 2

```
MapMapValues(map, mapExpr) -> Map
```

Semantics:
- Transform values, keep keys.
- `mapExpr` receives `{ key, value }`.

### 7.13 `MapFilterEntries`

Arity: 2

```
MapFilterEntries(map, predicateExpr) -> Map
```

Semantics:
- Filter by predicate on entries.
- `predicateExpr` receives `{ key, value }`.

### 7.14 `MapSize`

Arity: 1

```
MapSize(map) -> Integer
```

### 7.15 `MapFromEntries`

Arity: 1

```
MapFromEntries(list) -> Map
```

Semantics:
- Build Map from List of `{ key, value }` records.

Error behavior:
- If duplicate keys: `Invalid(...)` with code `MapFromEntries::DUPLICATE_KEY`.

### 7.16 `MapFromLists`

Arity: 2

```
MapFromLists(keys, values) -> Map
```

Error behavior:
- If lists have different lengths: `Invalid(...)`.
- If duplicate keys: `Invalid(...)`.

---

## 8. Record Operations (Normative)

### 8.1 `RecordGet`

Arity: 2

```
RecordGet(record, fieldName) -> Value
```

### 8.2 `RecordSet`

Arity: 3

```
RecordSet(record, fieldName, value) -> Record
```

### 8.3 `RecordRemove`

Arity: 2

```
RecordRemove(record, fieldName) -> Record
```

### 8.4 `RecordMerge`

Arity: 2

```
RecordMerge(record1, record2) -> Record
```

Semantics:
- record2 fields win on collision.

### 8.5 `RecordKeys`

Arity: 1

```
RecordKeys(record) -> Set<Text>
```

### 8.6 `RecordValues`

Arity: 1

```
RecordValues(record) -> List
```

### 8.7 `RecordEntries`

Arity: 1

```
RecordEntries(record) -> List<Record { key, value }>
```

### 8.8 `RecordHasField`

Arity: 2

```
RecordHasField(record, fieldName) -> Boolean
```

### 8.9 `SelectFields`

Arity: 2

```
SelectFields(record, fieldNames) -> Record
```

Semantics:
- Project to specified fields.
- Missing fields become `<Absent/>`.

### 8.10 `OmitFields`

Arity: 2

```
OmitFields(record, fieldNames) -> Record
```

### 8.11 `RenameField`

Arity: 3

```
RenameField(record, oldName, newName) -> Record
```

### 8.12 `RecordFromMap`

Arity: 1

```
RecordFromMap(map) -> Record
```

Error behavior:
- If any key is not Text: `Invalid(...)`.

### 8.13 `RecordToMap`

Arity: 1

```
RecordToMap(record) -> Map
```

---

## 9. Tuple Operations (Normative)

### 9.1 `TupleGet`

Arity: 2

```
TupleGet(tuple, index) -> Value
```

### 9.2 `TupleFirst`

Arity: 1

```
TupleFirst(tuple) -> Value
```

### 9.3 `TupleSecond`

Arity: 1

```
TupleSecond(tuple) -> Value
```

### 9.4 `TupleLast`

Arity: 1

```
TupleLast(tuple) -> Value
```

### 9.5 `TupleLength`

Arity: 1

```
TupleLength(tuple) -> Integer
```

### 9.6 `TupleToList`

Arity: 1

```
TupleToList(tuple) -> List
```

### 9.7 `ListToTuple`

Arity: 1

```
ListToTuple(list) -> Tuple
```

### 9.8 `MakeTuple`

Arity: 2 or more

```
MakeTuple(a, b, ...) -> Tuple
```

---

## 10. Range Operations (Normative)

### 10.1 `RangeToList`

Arity: 1

```
RangeToList(range) -> List
```

Semantics:
- Expand range to list of elements.

Error behavior:
- If expansion exceeds limits: `Invalid(...)` with code `CoreSafeTransforms::LIMIT_EXCEEDED`.

### 10.2 `RangeContains`

Arity: 2

```
RangeContains(range, value) -> Boolean
```

### 10.3 `RangeStart`

Arity: 1

```
RangeStart(range) -> Value
```

### 10.4 `RangeEnd`

Arity: 1

```
RangeEnd(range) -> Value
```

### 10.5 `RangeStep`

Arity: 1

```
RangeStep(range) -> Value
```

Semantics:
- Returns step or `<Absent/>` if none.

### 10.6 `RangeLength`

Arity: 1

```
RangeLength(range) -> Integer
```

Semantics:
- Number of elements when expanded.

### 10.7 `MakeRange`

Arity: 2 or 3

```
MakeRange(start, end) -> Range
MakeRange(start, end, step) -> Range
```

---

## 11. Join Operations (Normative)

### 11.1 `JoinCollectionsOnKey`

Arity: 4

```
JoinCollectionsOnKey(left, right, leftKeyExpr, rightKeyExpr) -> List<Record { left, right }>
```

Semantics:
- Inner join on computed keys.
- Output ordered by left, then right.

Error behavior:
- If duplicate keys on either side: `Invalid(...)` with code `JoinCollectionsOnKey::DUPLICATE_KEY`.
- If any key is `<Absent/>`: `Invalid(...)` with code `JoinCollectionsOnKey::NEED_NONABSENT_KEY`.

### 11.2 `LeftJoinCollectionsOnKey`

Arity: 4

```
LeftJoinCollectionsOnKey(left, right, leftKeyExpr, rightKeyExpr) -> List<Record { left, right }>
```

Semantics:
- Left outer join.
- Right is `<Absent/>` for non-matching left elements.

### 11.3 `RightJoinCollectionsOnKey`

Arity: 4

```
RightJoinCollectionsOnKey(left, right, leftKeyExpr, rightKeyExpr) -> List<Record { left, right }>
```

### 11.4 `FullJoinCollectionsOnKey`

Arity: 4

```
FullJoinCollectionsOnKey(left, right, leftKeyExpr, rightKeyExpr) -> List<Record { left, right }>
```

Semantics:
- Full outer join.

### 11.5 `CrossJoinCollections`

Arity: 2

```
CrossJoinCollections(left, right) -> List<Record { left, right }>
```

Semantics:
- Cartesian product.

---

## 12. String Operations (Normative)

### 12.1 `SplitString`

Arity: 2

```
SplitString(text, separator) -> List<Text>
```

Error behavior:
- If separator is empty: `Invalid(...)` with code `SplitString::NEED_NONEMPTY_SEPARATOR`.

### 12.2 `JoinStrings`

Arity: 2

```
JoinStrings(list, separator) -> Text
```

Error behavior:
- If any element is not Text: `Invalid(...)` with code `JoinStrings::NEED_TEXT_ELEMENTS`.

### 12.3 `SplitStringByLength`

Arity: 2

```
SplitStringByLength(text, length) -> List<Text>
```

### 12.4 `SplitStringByPattern`

Arity: 2

```
SplitStringByPattern(text, pattern) -> List<Text>
```

Semantics:
- Split by regex pattern.

---

## 13. Collection Creation (Normative)

### 13.1 `RepeatElement`

Arity: 2

```
RepeatElement(element, count) -> List
```

### 13.2 `GenerateElements`

Arity: 2

```
GenerateElements(count, generatorExpr) -> List
```

Semantics:
- Generate `count` elements.
- `generatorExpr` receives `{ index }`.

### 13.3 `EmptyList`

Arity: 0

```
EmptyList() -> List
```

### 13.4 `EmptySet`

Arity: 0

```
EmptySet() -> Set
```

### 13.5 `EmptyMap`

Arity: 0

```
EmptyMap() -> Map
```

### 13.6 `EmptyRecord`

Arity: 0

```
EmptyRecord() -> Record
```

### 13.7 `SingletonList`

Arity: 1

```
SingletonList(element) -> List
```

### 13.8 `SingletonSet`

Arity: 1

```
SingletonSet(element) -> Set
```

---

**End of Behavior Vocabulary — Core Safe Transforms v0.1**
