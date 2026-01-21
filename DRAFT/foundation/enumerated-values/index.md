Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Enumerated Values Specification

This specification defines how schemas declare enumerated value sets and how instances reference enumerated values.

This document is **Normative**.

---

## 1. Purpose

Many domains require closed sets of values: difficulty levels, status codes, measurement units, days of the week. These are not free-form text; they are constrained to a known, finite set.

This specification defines:

- how schemas declare enumerated value sets
- how instances reference enumerated values
- how Behavior operates on enumerated values
- the relationship to OWL2/SHACL semantic primitives

---

## 2. Terminology

- **Enumerated Value Set** — a named, finite, closed set of valid values
- **Enumerated Token** — a single value from an enumerated set, written `$Identifier`
- **Member** — an individual value within an enumerated set

---

## 3. Schema Declaration (Normative)

### 3.1 Defining an Enumerated Value Set

Domain schemas declare enumerated value sets using `EnumeratedValueSet`:

```cdx
<EnumeratedValueSet name="DifficultyLevel">
  <Member value="easy" />
  <Member value="medium" />
  <Member value="hard" />
</EnumeratedValueSet>
```

Rules:

1. The `name` MUST be unique within the schema.
2. Each `Member` MUST have a unique `value` within the set.
3. Member values MUST be valid identifiers (alphanumeric, hyphens, underscores).
4. The set MUST contain at least one member.

### 3.2 Optional Properties

Members MAY carry additional properties:

```cdx
<EnumeratedValueSet name="DifficultyLevel" ordered="true">
  <Member value="easy" ordinal="1" label="Easy" description="Suitable for beginners" />
  <Member value="medium" ordinal="2" label="Medium" description="Some experience required" />
  <Member value="hard" ordinal="3" label="Hard" description="For experts only" />
</EnumeratedValueSet>
```

Optional properties:

| Property | Meaning |
|----------|---------|
| `ordered` | If `true`, members have a defined ordering (default: `false`) |
| `ordinal` | Numeric position for ordered sets |
| `label` | Human-readable display label |
| `description` | Documentation for the member |
| `deprecated` | If `true`, member is deprecated but still valid |

### 3.3 Default Value

A set MAY declare a default member:

```cdx
<EnumeratedValueSet name="Calendar" default="iso8601">
  <Member value="iso8601" label="ISO 8601" />
  <Member value="gregorian" label="Gregorian" />
  <Member value="julian" label="Julian" />
  ...
</EnumeratedValueSet>
```

The default is used when:
- A trait with this enumerated type is absent and a default is needed
- An operation requires a value but none was specified

### 3.4 Constraining Traits

To constrain a trait to an enumerated set:

```cdx
<TraitDefinition name="difficulty">
  <EnumeratedConstraint set="DifficultyLevel" />
</TraitDefinition>
```

Or inline for simple cases:

```cdx
<TraitDefinition name="status" enumeration="pending,active,completed,archived" />
```

---

## 4. Instance Usage (Normative)

### 4.1 Syntax

Enumerated values are written with a `$` prefix:

```cdx
<Recipe difficulty=$medium>
  ...
</Recipe>
```

### 4.2 Validation

When a document is validated:

1. The trait's enumerated constraint is identified.
2. The token (without `$`) is checked against the set's members.
3. If the token is not a member, validation fails with diagnostic `EnumeratedValue::INVALID_MEMBER`.

### 4.3 Case Sensitivity

Enumerated tokens are **case-sensitive**:

- `$Medium` is NOT equal to `$medium`
- Schemas SHOULD use lowercase with hyphens for consistency

---

## 5. Built-in Enumerated Sets (Normative)

Certain enumerated sets are defined at the foundation level and available to all schemas.

### 5.1 Calendar

The `Calendar` enumerated set defines supported calendar systems.

Default: `iso8601`

Members:

| Value | Description |
|-------|-------------|
| `iso8601` | ISO 8601 calendar (default) |
| `gregorian` | Gregorian calendar |
| `julian` | Julian calendar |
| `hebrew` | Hebrew calendar |
| `islamic` | Islamic (Hijri) calendar |
| `islamic-umalqura` | Islamic (Umm al-Qura) calendar |
| `islamic-civil` | Islamic (civil) calendar |
| `islamic-tbla` | Islamic (tabular) calendar |
| `persian` | Persian (Solar Hijri) calendar |
| `indian` | Indian National calendar |
| `buddhist` | Buddhist calendar |
| `chinese` | Chinese calendar |
| `japanese` | Japanese Imperial calendar |
| `coptic` | Coptic calendar |
| `ethiopic` | Ethiopic calendar |
| `ethiopic-amete-alem` | Ethiopic (Amete Alem) calendar |
| `roc` | Republic of China calendar |

### 5.2 Extending Built-in Sets

Built-in enumerated sets MUST NOT be extended or modified by domain schemas. They are closed sets defined by the foundation.

---

## 6. Behavior Operations (Normative)

### 6.1 Type Guard

```
IsEnumeratedToken(value) -> Boolean
```

Returns `true` if the value is an enumerated token.

### 6.2 Equality

Enumerated tokens are compared by structural equality:

- Two tokens are equal iff they have the same identifier string.
- Tokens from different enumerated sets with the same identifier are NOT equal (they carry set context).

### 6.3 Ordering

By default, enumerated tokens are NOT orderable.

If a set is declared with `ordered="true"`:
- Tokens are orderable by their `ordinal` values.
- Tokens without explicit ordinals are ordered by declaration order.

### 6.4 Set Membership

```
IsValidMember(token, setName) -> Boolean
```

Returns `true` if the token is a valid member of the named set.

### 6.5 Enumeration

```
EnumerateMembers(setName) -> List<EnumeratedToken>
```

Returns all members of the set in declaration order.

---

## 7. Semantic Mapping (Normative)

Enumerated value sets map to OWL2/SHACL constructs:

| Codex Construct | Semantic Web Equivalent |
|-----------------|------------------------|
| `EnumeratedValueSet` | `owl:oneOf` enumeration or SKOS ConceptScheme |
| `Member` | Named individual in the enumeration |
| `EnumeratedConstraint` on trait | `sh:in` constraint in SHACL |
| Ordered set | `rdf:List` ordering |

Example OWL2 equivalent:

```turtle
:DifficultyLevel a owl:Class ;
    owl:oneOf ( :easy :medium :hard ) .

:easy a :DifficultyLevel .
:medium a :DifficultyLevel .
:hard a :DifficultyLevel .
```

---

## 8. Diagnostic Codes (Normative)

| Code | Meaning |
|------|---------|
| `EnumeratedValue::INVALID_MEMBER` | Token is not a member of the constrained set |
| `EnumeratedValue::EMPTY_SET` | Enumerated set has no members |
| `EnumeratedValue::DUPLICATE_MEMBER` | Set contains duplicate member values |
| `EnumeratedValue::INVALID_IDENTIFIER` | Member value is not a valid identifier |
| `EnumeratedValue::MISSING_ORDINAL` | Ordered set has members without ordinals |

---

## 9. Examples

### 9.1 Domain Schema with Enumeration

```cdx
<Schema id=codex:domain:recipe>
  <EnumeratedValueSets>
    <EnumeratedValueSet name="DifficultyLevel" ordered="true">
      <Member value="easy" ordinal="1" />
      <Member value="medium" ordinal="2" />
      <Member value="hard" ordinal="3" />
    </EnumeratedValueSet>
    
    <EnumeratedValueSet name="MealType">
      <Member value="breakfast" />
      <Member value="lunch" />
      <Member value="dinner" />
      <Member value="snack" />
      <Member value="dessert" />
    </EnumeratedValueSet>
  </EnumeratedValueSets>
  
  <TraitDefinitions>
    <TraitDefinition name="difficulty">
      <EnumeratedConstraint set="DifficultyLevel" />
    </TraitDefinition>
    
    <TraitDefinition name="mealType">
      <EnumeratedConstraint set="MealType" />
    </TraitDefinition>
  </TraitDefinitions>
  
  <ConceptDefinitions>
    <ConceptDefinition name="Recipe" entityEligibility=$MustBeEntity>
      <TraitRules>
        <AllowsTrait name="difficulty" />
        <AllowsTrait name="mealType" />
      </TraitRules>
    </ConceptDefinition>
  </ConceptDefinitions>
</Schema>
```

### 9.2 Data File Using Enumerated Values

```cdx
<Recipe id=recipe:pancakes difficulty=$easy mealType=$breakfast>
  <Title>Fluffy Pancakes</Title>
  ...
</Recipe>
```

### 9.3 Behavior Expression Using Enumerated Value

```cdx
<Behavior>
  <Ternary>
    <IsEqualTo>
      <Field name="difficulty" />
      <Constant value=$hard />
    </IsEqualTo>
    <Constant value="This recipe requires advanced skills." />
    <Constant value="This recipe is approachable." />
  </Ternary>
</Behavior>
```

---

**End of Enumerated Values Specification v0.1**
