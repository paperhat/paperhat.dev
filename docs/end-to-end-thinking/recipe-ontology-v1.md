# Recipe ontology v1

This is **Recipe Ontology v1**, frozen in the _FP / algebraic_ sense we’ve been circling around.

This is the **minimum complete, composable core**.

---

# 📘 Sitebender Codex — Recipe Ontology v1 (Frozen Core)

This is a **closed-world, algebraic ontology** designed for:

- referential transparency
- composability
- scaling
- reasoning
- non-dev authoring
- long-term evolution via _extension, not mutation_

---

## 0. Design constraints (non-negotiable)

1. **No inheritance for meaning**
2. **No presentation semantics**
3. **No implicit defaults**
4. **No mutation of published values**
5. **All quantities explicit**
6. **Free text is always quarantined**

If a concept violates one of these, it does not belong in v1.

---

## 1. Core Concepts (the algebra)

### 1.1 `Recipe` (product type)

A `Recipe` is a **pure value** defined as:

```
Recipe =
  Identity
  Title
  Description?
  Servings
  IngredientList
  InstructionList
  TimeInfo?
```

Nothing more. Nothing less.

---

### 1.2 `RecipeIdentity`

```
RecipeIdentity =
  canonicalId
  createdBy
  createdAt
  forkedFrom?
```

- Immutable
- Used for lineage
- Never user-edited

---

### 1.3 `Title`

```
Title =
  PlainText
```

Constraints:

- language-tagged
- max length enforced
- no formatting
- no semantics beyond human readability

---

### 1.4 `Description` (quarantined text)

```
Description =
  PlainText
```

Rules:

- Optional
- Never parsed
- Never reasoned over
- Never used for search except full-text

This is **editorial prose**, explicitly marked as such.

---

## 2. Servings (the scaling anchor)

### 2.1 `Servings` (required)

```
Servings =
  quantity : PositiveInteger
  unit     : ServingUnit
```

Example:

- `4 servings`
- `2 people`

Rules:

- Always required
- No “to taste”
- This is the **referential anchor for scaling**

> Without this, the recipe is incomplete.

---

## 3. Ingredients (parametric, not concrete)

### 3.1 `IngredientList`

```
IngredientList =
  NonEmptyList<IngredientUsage>
```

Order is preserved **only** for authorial readability.

---

### 3.2 `IngredientUsage`

This is the key abstraction.

```
IngredientUsage =
  Quantity
  IngredientReference
  Preparation?
```

It is **not** an ingredient.
It is a _use of an ingredient_.

---

### 3.3 `Quantity`

```
Quantity =
  amount : Decimal
  unit   : Unit
```

Rules:

- No ranges
- No “some”
- No embedded math
- Units must be canonical

---

### 3.4 `IngredientReference` (3-layer identity)

```
IngredientReference =
  lexicalLabel
  canonicalIngredient?
```

- `lexicalLabel` is required
- `canonicalIngredient` is optional

This preserves:

- human intent
- machine reasoning
- future refinement

---

### 3.5 `Preparation` (optional, controlled)

```
Preparation =
  PreparationMethod*
```

Examples:

- chopped
- peeled
- melted

Controlled vocabulary, **not free text**.

---

## 4. Instructions (procedural, but pure)

### 4.1 `InstructionList`

```
InstructionList =
  OrderedList<InstructionStep>
```

Order **matters** here.

---

### 4.2 `InstructionStep`

```
InstructionStep =
  StepText
  Duration?
```

---

### 4.3 `StepText` (quarantined text)

```
StepText =
  PlainText
```

Rules:

- Human-readable only
- No embedded quantities relied on for reasoning
- Machines never infer ingredients from here

This prevents **implicit meaning leakage**.

---

## 5. Time (orthogonal metadata)

### 5.1 `TimeInfo`

```
TimeInfo =
  prepTime?
  cookTime?
  totalTime?
```

Each is:

```
Duration =
  amount
  unit (minutes | hours)
```

No assumptions. No derivations required.

---

## 6. Validation invariants (SHACL-level)

A Recipe is **valid** iff:

- exactly one `Title`
- exactly one `Servings`
- at least one `IngredientUsage`
- at least one `InstructionStep`
- all quantities are numeric + unitized
- no ingredient quantity depends on prose
- no instruction mutates ingredients implicitly

---

## 7. What is deliberately NOT in v1

Explicit exclusions:

- Nutritional data
- Substitutions
- Allergens
- Scaling rules
- Equipment
- Temperature modeling
- Cuisine taxonomy
- Difficulty
- Ratings
- Comments
- Media
- Layout

All of these compose **on top**, not inside.

---

## 8. FP correspondence (sanity check)

| FP concept               | Recipe ontology      |
| ------------------------ | -------------------- |
| Value                    | Published Recipe     |
| Record                   | Product concepts     |
| Functor                  | Scaling by servings  |
| Parametric polymorphism  | IngredientReference  |
| Purity                   | No hidden inputs     |
| Immutability             | Publish / fork       |
| Referential transparency | Identity + structure |

This passes the test.

---

## 9. TSX surface (canonical)

Your example already fits with _zero changes_ except Servings:

```tsx
<Recipe>
	<Title>Grandmother's Apple Pie</Title>

	<Description>
		A delicious, crisp, cinnamon-y apple pie the way Grandma used to make.
	</Description>

	<Servings amount={6} unit="servings" />

	<Ingredients>
		<Ingredient amount="2" unit="cup">
			flour
		</Ingredient>
		<Ingredient amount="1" unit="cup">
			butter
		</Ingredient>
		<Ingredient amount="6" unit="each">
			apples
		</Ingredient>
	</Ingredients>

	<Instructions>
		<Step>Cut butter into flour until crumbly</Step>
		<Step>Press into pie dish</Step>
		<Step>Bake at 375°F for 45 minutes</Step>
	</Instructions>
</Recipe>
```

This is now **definitionally complete**.

---

## 10. Why this is safe to freeze

Because:

- It is algebraic
- It is minimal
- It is orthogonal
- It is extensible
- It does not smuggle assumptions
- It composes upward cleanly

You will not regret freezing this.
