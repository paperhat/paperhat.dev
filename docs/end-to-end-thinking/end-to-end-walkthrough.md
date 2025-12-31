# End-to-end Recipe walkthrough

# End-to-End Recipe Demo (Sitebender Codex)

We will walk **one recipe** through the full pipeline:

> Author → File → IR → Triple Store → Query → UI → Fork → Grocery List

---

## Phase 0 — Preconditions (what already exists)

Frozen and assumed:

- Recipe Ontology v1 (just frozen)
- Ingredient identity stack (lexical → canonical → nutritional)
- Closed world
- Publish = immutable value
- Fork = new value

No UI yet. Just meaning.

---

## Phase 1 — Authoring (non-dev, human-legible)

This is **the entire authoring artifact**.
No imports. No helpers. No runtime code.

### 📄 `modules/recipes/grandmas-apple-pie/content.bend`

```tsx
<Recipe>
	<Title>Grandmother's Apple Pie</Title>

	<Description>
		A crisp, cinnamon-forward apple pie passed down in our family.
	</Description>

	<Servings amount={6} unit="servings" />

	<Ingredients>
		<Ingredient amount={2} unit="cup">
			flour
		</Ingredient>
		<Ingredient amount={1} unit="cup">
			butter
		</Ingredient>
		<Ingredient amount={6} unit="each">
			apples
		</Ingredient>
		<Ingredient amount={0.75} unit="cup">
			sugar
		</Ingredient>
		<Ingredient amount={1} unit="tsp">
			cinnamon
		</Ingredient>
	</Ingredients>

	<Instructions>
		<Step>Cut butter into flour until crumbly.</Step>
		<Step>Mix in sugar and cinnamon.</Step>
		<Step>Fold in apples.</Step>
		<Step>Bake at 375°F for 45 minutes.</Step>
	</Instructions>
</Recipe>
```

### What this is (formally)

- A **pure declarative value**
- No presentation semantics
- No implicit defaults
- No side effects
- Referentially transparent

At this point:

> This is just _structured meaning_, not a page.

---

## Phase 2 — Parse → IR (internal, deterministic)

The compiler does **one thing**:

> Parse TSX → validate against ontology → emit IR

### Example IR (conceptual, abbreviated)

```json
{
	"type": "Recipe",
	"id": "recipe:grandmas-apple-pie@v1",
	"title": "Grandmother's Apple Pie",
	"description": "A crisp, cinnamon-forward apple pie passed down in our family.",
	"servings": { "amount": 6, "unit": "servings" },
	"ingredients": [
		{
			"quantity": { "amount": 2, "unit": "cup" },
			"lexicalLabel": "flour"
		},
		{
			"quantity": { "amount": 1, "unit": "cup" },
			"lexicalLabel": "butter"
		},
		{
			"quantity": { "amount": 6, "unit": "each" },
			"lexicalLabel": "apples"
		}
	],
	"instructions": [
		{ "text": "Cut butter into flour until crumbly." },
		{ "text": "Mix in sugar and cinnamon." },
		{ "text": "Fold in apples." },
		{ "text": "Bake at 375°F for 45 minutes." }
	]
}
```

### Important

- No guessing
- No enrichment
- No ingredient inference
- Free text remains quarantined

If this fails SHACL → **cannot publish**.

---

## Phase 3 — IR → RDF → Oxigraph

The IR is serialized into triples.

Example (conceptual):

```
:recipe123 a :Recipe ;
  :hasTitle "Grandmother's Apple Pie" ;
  :hasServings [
    :amount 6 ;
    :unit :Serving
  ] ;
  :hasIngredientUsage [
    :usesIngredient :IngredientUsage1
  ] .
```

Ingredient identity at this point:

```
:IngredientUsage1
  :lexicalLabel "flour" .
```

Still **no canonical ingredient yet**.
That is deliberate.

---

## Phase 4 — Ingredient clarification (optional, incremental)

Now the system can offer an affordance:

> “Clarify ingredients?”

### UI affordance

For each ingredient chip:

```
flour  ⚠️  (unresolved)
```

Click → suggestion panel:

- Wheat flour (common)
- All-purpose flour
- Leave unresolved

If the author selects:

```
canonicalIngredient = WheatFlour
```

A new triple is added.
The recipe itself is unchanged **unless republished**.

---

## Phase 5 — Publish (commit the value)

User clicks **Publish**.

What happens:

- Validation re-run
- Immutable ID minted
- Version hash sealed
- Lineage recorded

Now:

> This recipe is a **value in the knowledge graph**.

---

## Phase 6 — Query → Projection (this is where magic _isn’t_)

### Example: recipe page query

SPARQL:

```sparql
SELECT ?title ?description ?ingredients ?steps WHERE {
  ?r a :Recipe ;
     :hasTitle ?title ;
     :hasIngredientUsage ?ingredients ;
     :hasInstructionStep ?steps .
}
```

Result → JSON → renderer.

### Renderer choice

- `renderToDOM` → interactive site
- `renderToString` → SSG
- `renderToTSX` → editable fork
- `renderToPDF` → printable

Same value. Different projection.

---

## Phase 7 — Grocery list (pure function)

User selects:

> “I want to cook this for **12 servings**”

This triggers:

```
scaleRecipe(recipe, factor = 2)
```

No mutation.

### Derived grocery list

```
flour: 4 cups
butter: 2 cups
apples: 12
sugar: 1.5 cups
cinnamon: 2 tsp
```

This works because:

- Servings are explicit
- Quantities are structured
- Ingredients are identity-stable

---

## Phase 8 — Fork & disagreement (no collapse)

User’s mum clicks:

> “This uses too much sugar”

She **cannot edit**.

She can:

### Option A — Annotate

```text
Suggestion:
I usually use half the sugar and add lemon zest.
```

### Option B — Fork

Creates:

```
Grandmother's Apple Pie (Less Sweet)
forkedFrom → original
```

New value. Coherence preserved.

---

## Phase 9 — Non-dev AI assistance (safely)

AI is allowed to:

- Draft a recipe (unpublished)
- Suggest canonical ingredients
- Flag missing servings
- Propose forks

AI is **never allowed to**:

- Mutate published values
- Resolve disputes
- Invent ontology terms
- Assert authority

The AI is a **junior assistant**, not an editor.

---

## Phase 10 — What you can demo to friends

You can now demo:

1. Write recipe in 1 file
2. Publish → immutable
3. Scale servings → grocery list
4. Fork → variation
5. Annotate → discussion
6. No conflicts
7. No CMS
8. No React
9. No magic

---

## The key point (the one to emphasize)

> **Everything is a value. Everything else is a projection.**

That’s why this works.
That’s why it scales.
That’s why it doesn’t rot.
