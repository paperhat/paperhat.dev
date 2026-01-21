Status: DRAFT
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Predicate, Guard, and Validation Composition Surface Specification

This specification defines the canonical naming conventions, semantic categories, and composition rules for boolean-returning operators in the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

The Behavior Vocabulary contains many operators that return Boolean values. These operators serve different purposes:

- **Type guards** narrow the type of a value
- **Predicates** test properties or relationships
- **Validators** combine predicates for schema validation

Without a unified specification, naming conventions drift, composition rules vary, and the relationship between guards and predicates remains implicit.

This specification exists to:

- establish a taxonomy of boolean-returning operators
- define canonical naming conventions
- specify composition patterns
- clarify the totality policy for each category
- define guard semantics for type narrowing

---

## 2. Taxonomy (Normative)

### 2.1 Type Guards

Type guards test whether a value belongs to a specific type or type family.

Characteristics:

- Always total (return `Valid(false)` for non-matching types)
- Never return `Invalid(...)`
- Enable type narrowing in conditional branches

Examples: `IsInteger`, `IsList`, `IsPlainDate`, `IsColor`, `IsTemporal`

### 2.2 State Predicates

State predicates test intrinsic properties of a value within its type.

Characteristics:

- Assume the value is of an appropriate type
- Return `Valid(false)` for inappropriate types (total) or `Invalid(...)` (partial)
- Do not narrow types

Examples: `IsEmpty`, `IsFinite`, `IsPositive`, `IsZero`, `IsEven`

### 2.3 Relational Predicates

Relational predicates test relationships between two or more values.

Characteristics:

- Compare values for equality, ordering, or other relationships
- May be partial (return `Invalid(...)` for incomparable values)

Examples: `IsEqualTo`, `IsLessThan`, `IsMoreThan`, `IsSameDate`

### 2.4 Membership Predicates

Membership predicates test whether a value exists within a collection.

Characteristics:

- Test containment relationships
- Total over collection types (return `Valid(false)` for non-collections)

Examples: `ContainsElement`, `ContainsKey`, `SetContains`

### 2.5 Shape Predicates

Shape predicates test structural properties of collections.

Characteristics:

- Test size, structure, or content patterns
- Total over collection types

Examples: `HasElementCountEqualTo`, `HasElementCountAtLeast`, `IsSubsetOf`

### 2.6 Quantified Predicates

Quantified predicates apply a predicate expression across collection elements.

Characteristics:

- Higher-order operators (accept predicate expressions)
- Test universal or existential quantification

Examples: `AllElementsSatisfy`, `AnyElementSatisfies`, `NoElementSatisfies`, `AllKeysSatisfy`

---

## 3. Naming Conventions (Normative)

### 3.1 Type Guard Names

Pattern: `Is<TypeName>`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `Is<Type>` | Exact type test | `IsInteger`, `IsFraction`, `IsText` |
| `Is<TypeFamily>` | Type family test | `IsTemporal`, `IsColor`, `IsNumeric` |

### 3.2 State Predicate Names

Pattern: `Is<State>`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `Is<Adjective>` | Boolean state | `IsEmpty`, `IsFinite`, `IsPositive` |
| `Is<Condition>` | Derived state | `IsLeapYear`, `IsWeekend`, `IsPrime` |

### 3.3 Relational Predicate Names

Pattern: `Is<Relation>To` or `Is<Relation>`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `Is<Relation>To` | Binary comparison | `IsEqualTo`, `IsUnequalTo` |
| `Is<Ordering>Than` | Ordering comparison | `IsLessThan`, `IsMoreThan` |
| `IsNo<Ordering>Than` | Inclusive ordering | `IsNoLessThan`, `IsNoMoreThan` |
| `Is<Relation>` | Temporal/domain-specific | `IsAfter`, `IsBefore`, `IsSameDate` |

### 3.4 Membership Predicate Names

Pattern: `Contains<Thing>` or `<Collection>Contains`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `Contains<Thing>` | Generic containment | `ContainsElement`, `ContainsKey` |
| `<Type>Contains` | Type-specific | `SetContains`, `MapContainsKey` |
| `DoesNotContain<Thing>` | Negated containment | `DoesNotContainElement`, `DoesNotContainKey` |

### 3.5 Shape Predicate Names

Pattern: `Has<Property>` or `Is<Shape>`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `Has<Property><Relation>` | Property test | `HasElementCountEqualTo`, `HasElementCountAtLeast` |
| `Is<SetRelation>Of` | Set relationships | `IsSubsetOf`, `IsSupersetOf`, `IsProperSubsetOf` |
| `<Collections>Are<Relation>` | Collection comparison | `SetsAreDisjoint`, `SetsOverlap` |

### 3.6 Quantified Predicate Names

Pattern: `<Quantifier><Things><Verb>`

| Pattern | Usage | Examples |
|---------|-------|----------|
| `All<Things>Satisfy` | Universal quantification | `AllElementsSatisfy`, `AllKeysSatisfy` |
| `Any<Thing>Satisfies` | Existential quantification | `AnyElementSatisfies` |
| `No<Thing>Satisfies` | Negated existential | `NoElementSatisfies` |

---

## 4. Totality Policy (Normative)

### 4.1 Total Predicates

A predicate is **total** if it returns `Valid(true)` or `Valid(false)` for any input, never `Invalid(...)`.

Total predicates handle out-of-domain inputs by returning `Valid(false)`:

```
IsInteger(<Absent/>) -> Valid(false)
ContainsElement("not a list", 42) -> Valid(false)
HasElementCountEqualTo({ key: "value" }, 5) -> Valid(false)
```

### 4.2 Partial Predicates

A predicate is **partial** if it may return `Invalid(...)` for certain inputs.

Partial predicates return `Invalid(...)` for domain violations:

```
IsLessThan(5, "text") -> Invalid(...) with code IsLessThan::NEED_COMPARABLE_VALUES
AllKeysSatisfy("not a record", pred) -> Invalid(...) with code AllKeysSatisfy::NEED_RECORD
```

### 4.3 Category Defaults

| Category | Default Totality | Rationale |
|----------|------------------|-----------|
| Type Guards | Total | Guards should never fail; they classify |
| State Predicates | Total | State tests on wrong types are simply false |
| Relational Predicates | Partial | Comparing incompatible types is an error |
| Membership Predicates | Total | Membership in non-collection is false |
| Shape Predicates | Total | Shape of non-collection is undefined (false) |
| Quantified Predicates | Partial | Inner predicate errors must propagate |

### 4.4 Totality Declaration

Each predicate specification MUST declare its totality:

- "This predicate is total" — returns `Valid(false)` for out-of-domain inputs
- "This predicate is partial" — returns `Invalid(...)` for out-of-domain inputs

If not declared, the category default applies.

---

## 5. Guard Semantics (Normative)

### 5.1 Type Narrowing

Type guards enable type narrowing in conditional branches. When a guard returns `true`, subsequent code in that branch may assume the narrowed type.

Conceptual model:

```
Ternary(
  IsInteger(x),
  // in this branch, x is known to be Integer
  Add(x, 1),
  // in this branch, x is known to NOT be Integer
  <Absent/>
)
```

### 5.2 Guard Composition

Guards compose under boolean operators:

- `And(IsInteger(x), IsPositive(x))` — both conditions hold
- `Or(IsInteger(x), IsFraction(x))` — either condition holds
- `Not(IsAbsent(x))` — condition does not hold

### 5.3 No Runtime Type Narrowing

Behavior is a pure expression language without mutable bindings. Type narrowing is a **semantic concept** for specification clarity, not a runtime mechanism.

Implementations MUST NOT:

- modify values based on guard results
- cache or memoize type information across expressions

Implementations MAY:

- use guard information for optimization
- skip redundant type checks in nested expressions

---

## 6. Composition Patterns (Normative)

### 6.1 Boolean Composition

Predicates compose using boolean operators defined by the Relational and Predicates family:

| Operator | Semantics |
|----------|-----------|
| `Not(p)` | Logical negation |
| `And(p, q, ...)` | Logical conjunction (all must be true) |
| `Or(p, q, ...)` | Logical disjunction (at least one must be true) |

### 6.2 Short-Circuit Evaluation

Boolean composition follows short-circuit semantics:

- `And` stops at the first `false` (left-to-right)
- `Or` stops at the first `true` (left-to-right)

However, diagnostic ordering MUST remain deterministic as specified by Behavior Dialect Semantics Section 8.

### 6.3 Higher-Order Composition

Quantified predicates enable composition over collections:

```
AllElementsSatisfy(list, IsInteger)  // all elements are integers
AnyElementSatisfies(list, IsPositive)  // at least one is positive
AllKeysSatisfy(record, StartsWithSubstring("_"))  // all keys start with underscore
```

### 6.4 Predicate Pipelines

Complex validations compose as nested expressions:

```
And(
  IsList(x),
  HasElementCountAtLeast(x, 1),
  AllElementsSatisfy(x, IsInteger),
  AllElementsSatisfy(x, IsPositive)
)
```

---

## 7. Determinism Requirements (Normative)

### 7.1 Deterministic Results

All predicates MUST be deterministic:

- Given the same inputs, a predicate MUST return the same result.
- No ambient dependencies (time, randomness, external state).

### 7.2 Stable Diagnostics

When a predicate returns `Invalid(...)`:

- Diagnostic codes MUST be stable across evaluations.
- Diagnostic ordering MUST follow Behavior Dialect Semantics Section 8.

### 7.3 Evaluation Independence

Predicate evaluation MUST NOT depend on:

- previous predicate evaluations
- evaluation order optimizations
- runtime caching strategies

---

## 8. Relationship to Validation Surface (Informative)

### 8.1 Schema Validation

Predicates form the foundation of schema validation. A schema constraint is conceptually a predicate applied to instance data:

```
// Schema constraint: "list must have 1-10 elements"
HasElementCountBetweenInclusive(instance.items, 1, 10)
```

### 8.2 Adaptive Layout Integration

Adaptive Layouts use predicates for conditional rendering and validation:

- `ShowIf` — display element when predicate is true
- `Validate` — mark field invalid when predicate is false

### 8.3 Diagnostic Integration

When validation predicates return `Invalid(...)`, the diagnostic codes integrate with:

- Behavior Diagnostic Codes (code registry)
- Diagnostic Messaging and Help (user-facing messages)

---

## 9. Summary Tables

### 9.1 Naming Pattern Quick Reference

| Category | Pattern | Example |
|----------|---------|---------|
| Type Guard | `Is<Type>` | `IsInteger` |
| State Predicate | `Is<State>` | `IsEmpty` |
| Equality | `Is<Relation>To` | `IsEqualTo` |
| Ordering | `Is<Ordering>Than` | `IsLessThan` |
| Membership | `Contains<Thing>` | `ContainsElement` |
| Shape | `Has<Property><Relation>` | `HasElementCountAtLeast` |
| Universal | `All<Things>Satisfy` | `AllElementsSatisfy` |
| Existential | `Any<Thing>Satisfies` | `AnyElementSatisfies` |

### 9.2 Totality Quick Reference

| Returns | Meaning |
|---------|---------|
| `Valid(true)` | Predicate holds |
| `Valid(false)` | Predicate does not hold (or out-of-domain for total predicates) |
| `Invalid(...)` | Domain violation (partial predicates only) |

---

## 10. Relationship to Other Specifications

- Evaluation model and diagnostics ordering: Behavior Dialect Semantics
- Boolean operators (Not, And, Or): Behavior Vocabulary — Relational and Predicates
- Collection predicates: Behavior Vocabulary — Data Shapes and Validation
- Type guards: Behavior Dialect (Section 11), individual vocabulary families
- Diagnostic codes: Behavior Diagnostic Codes

---

**End of Predicate, Guard, and Validation Composition Surface Specification v0.1**
