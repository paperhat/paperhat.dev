# Composability of ontological objects (e.g., Recipe)

Yes — **composable in the strong, FP sense**, not just “modular”. And this is exactly the right moment to lock that in _before_ freezing the ontology, because composability determines what the ontology is allowed to look like.

I’ll do this in three layers:

1. **What composability means here (precisely)**
2. **What must be true of the ontology to preserve it**
3. **What you freeze vs what you deliberately leave open**

---

## 1. What “composable” means in Sitebender Codex terms

In FP, composability means:

> You can build larger meaning from smaller meaning **without rewriting either**.

Translated to your system:

> A higher-level concept (Recipe, MealPlan, Cookbook, Curriculum) is constructed by **structural composition** of lower-level concepts, not by inheritance, mutation, or interpretation.

That already rules out a _lot_ of bad ontology design.

### Key composability properties you already have

A `<Recipe>`:

- does not assume where it appears
- does not assume how it’s rendered
- does not assume who uses it
- does not assume why it exists

It is **context-free**.

That’s the content equivalent of a pure function.

---

## 2. The ontology must be algebraic, not taxonomic

This is the crucial distinction.

### ❌ What breaks composability

Traditional ontologies tend to do this:

- Deep inheritance trees
- “Recipe is a type of Document”
- “Ingredient is a subtype of Thing”
- Overloaded properties
- Meaning via position

This leads to:

- tight coupling
- implicit assumptions
- semantic fragility

In FP terms: **action at a distance**.

---

### ✅ What preserves composability

Your ontology must behave like **algebraic data types**.

That means:

- Concepts are **products** (AND)
- Variants are **sums** (OR)
- No semantic inheritance
- No “magic” defaults

#### Example: Recipe as a product type

Conceptually:

```
Recipe =
  Title
  Description?
  Ingredients
  Instructions
  Servings
  Times*
```

Not:

> Recipe extends Content extends Node extends Thing

This matters enormously.

---

## 3. Composition through containment, not specialization

You’re already doing this instinctively with TSX.

This:

```tsx
<Recipe>
	<Ingredients>...</Ingredients>
	<Instructions>...</Instructions>
</Recipe>
```

is **structural composition**, not semantic inheritance.

That gives you:

- reorderability
- reuse
- partial reuse
- projection

Exactly like FP records.

---

## 4. Higher-order composition (this is the good stuff)

Once content is composable, you get **higher-order content**.

### Example: MealPlan

A `MealPlan` is not a new kind of Recipe.

It’s:

```
MealPlan =
  Set<RecipeUsage>
  Timeframe
  ScalingRule
```

Where `RecipeUsage` is:

```
RecipeUsage =
  recipeRef
  servingsOverride?
```

You didn’t invent new semantics.
You _composed existing ones_.

That’s higher-order FP thinking.

---

## 5. Ingredient composition is parametric, not concrete

This is where your ingredient model shines.

A recipe does not require:

> “Wheat flour, brand X”

It requires:

> “Something satisfying the Flour role”

That means recipes are **parametric over ingredient types**.

FP analogy:

```ts
Recipe<F extends Flour>
```

This allows:

- substitution
- filtering
- scaling
- constraint solving

Without rewriting recipes.

That’s _real_ composability.

---

## 6. Serving size is a scaling functor (yes, literally)

Earlier you correctly flagged servings as crucial.

In FP terms:

> Servings is a **mapping over quantities**.

That makes it a **functor**:

```
scale : Recipe → Recipe
```

No mutation.
New value.

Because quantities are explicit and typed, scaling composes cleanly.

This only works because:

- ingredients are structured
- units are explicit
- no freeform math hidden in text

---

## 7. UI composition follows ontology composition

This is why your `<ConceptForm>` idea is so powerful.

The form is not bespoke UI.
It’s a **projection**.

Form composition mirrors ontology composition:

- Include / Exclude → record projection
- Group → structural grouping
- Hidden → partial application
- Ephemeral fields → effect-local state

That’s exactly how FP UIs work when done well.

---

## 8. What freezing the ontology really means

Freezing does **not** mean “complete”.

It means:

### You freeze:

- Core Concepts (Recipe, IngredientUsage, Servings, Quantity)
- Their required properties
- Their algebraic structure
- Validation invariants

### You explicitly do _not_ freeze:

- Lexical labels
- Canonical mappings
- Nutritional expansions
- Domain extensions

This is the FP distinction between:

- **data constructors** (stable)
- **values** (unbounded)

---

## 9. The litmus test for composability

Before freezing anything, ask:

> “Can this concept be reused unchanged in a context I haven’t imagined yet?”

If the answer is “no”:

- it’s too specialized
- or it smuggles context
- or it encodes presentation

Those are the same smells FP devs already know.

---

## 10. Bottom line

Yes — your system is:

- composable
- referentially transparent
- algebraic
- higher-order
- parametric
- immutable

Not because you aimed for FP aesthetics,
but because you enforced **semantic discipline**.
