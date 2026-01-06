# Recipe content model

Recipes are _deceptively_ hard — they look like “content,” but they’re actually **procedures with structured resources, variants, and constraints**. Which makes them ideal for Paperhat + filesystem pedagogy.

We'll use the same three-layer way:

1. **Content primitives for recipes (what exists)**
2. **Filesystem + routing (how Paperhat sees it)**
3. **Non-developer contribution, shopping lists, feedback**

And keep it concrete and boring-on-purpose.

---

# I. Recipe content model (editorial primitives)

Forget “recipe pages.” They’re a trap.

A recipe site consists of **five primitives**:

---

## 1. Ingredient (canonical, reusable)

```
/_ingredient
  /onion.ts
  /olive-oil.ts
```

```ts
export const ingredient = {
	id: "onion",
	name: "Onion",
	forms: ["red", "white", "brown"],
	unitDefaults: ["g", "each"],
	tags: ["vegetable", "aromatic"],
} as const;
```

Why this matters:

- Normalizes naming
- Enables aggregation
- Prevents “1 onion” vs “one onion” vs “onions”

This is **where Wikipedia-style mess usually starts**. You prevent it upfront.

---

## 2. Recipe (procedure, not prose)

```
/recipe
  /pasta-alla-norma.ts
```

```ts
import { onion } from "_ingredient/onion.ts";
import { eggplant } from "_ingredient/eggplant.ts";

export const recipe = {
	id: "pasta-alla-norma",
	title: "Pasta alla Norma",
	serves: 4,
	tags: ["italian", "vegetarian", "pasta"],

	ingredients: [
		{ item: onion, amount: 1 },
		{ item: eggplant, amount: 2 },
		{ item: oliveOil, amount: "3 tbsp" },
	],

	steps: [
		"Salt and roast the eggplant.",
		"Sweat the onion in olive oil.",
		"Combine with tomato sauce and pasta.",
	],
} as const;
```

No layout. No markdown. No fluff.

This is **machine-readable first**, human-readable second.

---

## 3. Tags (derived, not authored)

Tags are **not freeform strings**.

```
/_tag
  /italian.ts
  /vegetarian.ts
```

Each tag file:

```ts
export const tag = {
	id: "vegetarian",
	description: "Contains no meat or fish",
};
```

Recipes reference tags by ID.
Tags can evolve _without touching recipes_.

---

## 4. Pantry state (per user, ephemeral)

```
/pantry/chas.json
```

```json
{
	"onion": true,
	"eggplant": false,
	"olive-oil": true
}
```

This is not content. It’s **state**.

---

## 5. Feedback (structured, forkable)

```
/feedback
  /pasta-alla-norma
    /mum.md
```

```md
---
type: suggestion
tone: friendly
---

Took longer than expected. Maybe warn about roasting time.
```

No comments embedded in canon.

---

# II. Paperhat routing & features

Now the fun part: what this enables _automatically_.

---

## 1. String search

Because recipes are structured:

- Title
- Ingredient names
- Tags
- Step text

You can index fields separately.

Examples:

- `"eggplant"`
- `"vegetarian pasta"`
- `"under 30 minutes"`

No NLP required.

---

## 2. Tag filtering

Routes:

```
/recipes
/recipes/tag/vegetarian
/recipes/tag/italian
```

Multi-tag:

```
/recipes?tags=vegetarian,pasta
```

Since tags are normalized, filtering is exact, not fuzzy.

---

## 3. Ingredient-based search (killer feature)

Routes:

```
/recipes/with/onion
/recipes/with/onion,eggplant
```

Computed by:

- Recipe ingredient lists
- Pantry state

You get:

> “You can cook 7 recipes right now.”

---

## 4. Shopping list generation (this is huge)

Given:

- Selected recipes
- Pantry state

The system computes:

```json
{
	"eggplant": 2,
	"tomato": "400g",
	"basil": "1 bunch"
}
```

Grouped by:

- Ingredient category
- Store section (optional metadata)

This alone makes the site _useful_, not just pretty.

---

# III. Non-developer contribution (this matters)

Here’s where Paperhat + filesystem shine.

---

## 1. “My sister adds a recipe”

She does **not** write TypeScript.

She fills a form:

- Title
- Ingredients (autocomplete from canonical list)
- Amounts
- Steps
- Tags (checkboxes)

The system:

- Generates the `.ts` file
- Validates constraints
- Opens a PR automatically

She never sees Git.

---

## 2. Ingredient governance (lightweight)

If she needs a new ingredient:

- She proposes it
- The system:
  - Suggests merges (“Shallot” vs “Onion”)
  - Requires a category
  - Prevents duplicates

You approve once.

---

## 3. “My mum leaves feedback via PR”

She clicks:

> “Suggest an improvement”

She writes text.

Under the hood:

- A markdown file is created in `/feedback`
- A PR is opened

She doesn’t know what a PR is.
You do.

---

## 4. Forking recipes (safe experimentation)

```
/forks/mum/recipe/pasta-alla-norma.less-oil.ts
```

Marked as:

- Variant
- Non-canonical

Readers can toggle:

> “Show variants”

Canon remains clean.

---

# IV. Why this works better than every recipe site

Because:

- Ingredients are _entities_, not strings
- Recipes are procedures, not stories
- Tags are curated, not polluted
- Feedback is separated from canon
- Shopping lists fall out _for free_

Most recipe sites are blogs pretending to be tools.

This is a **tool that happens to be readable**.

---

# V. Pedagogy (yes, even here)

The site can say:

> “Recipes are procedures. Ingredients are shared resources. Variants are forks.”

You’re teaching users _how to think about cooking_, not just what to cook.

---

## Final thought

If this works for recipes — a domain with:

- Ambiguity
- Variants
- Opinions
- Personal habits

— then it will work for almost anything.
