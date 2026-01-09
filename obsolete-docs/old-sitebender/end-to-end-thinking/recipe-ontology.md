# Recipe conversation from the ontology

Serving size is not a “nice to have”; it’s a **semantic fulcrum**:

- ingredient quantities are meaningless without it
- grocery lists can’t aggregate
- scaling (×2, ×½) is impossible
- nutritional reasoning is impossible
- meal planning collapses

We’ll do two things:

1. **Acknowledge serving size as a first-class concept**
2. **Run the full Recipe authoring transcript with it integrated from the start**

I’ll also explicitly show:

- where the AI is constrained
- where it asks instead of assumes
- how `.pph` grows incrementally

No React. No magic. No silent knowledge.

---

# 0. Minimal Recipe ontology (just enough to run the demo)

This is _not_ exhaustive — just the commitments needed to make the transcript honest.

Conceptually (not syntax yet):

**Recipe**

- title (required)
- description (optional)
- servings (required)
- ingredients (required, ≥1)
- instructions (required, ≥1)
- prepTime (optional)
- cookTime (optional)

**Serving**

- quantity (number)
- unit (e.g. servings, people)

**IngredientUsage**

- ingredientRef (lexical or canonical)
- amount (number)
- unit (optional, contextual)
- per (Serving) ← _this is the key link_

Important:

> Ingredient amounts are **defined relative to the declared serving size**, not absolute.

That’s the invariant that makes everything downstream work.

---

# 1. Live authoring transcript — Recipe

Same protocol as before. Different ontology.

---

## Phase 1 — Intent Declaration

### USER

> I want to add a recipe.

### AI

> Got it.
>
> We’re creating a **Recipe**.
>
> A Recipe describes:
>
> - How many people it serves
> - What ingredients are needed
> - What steps to follow
>
> We’ll build it one piece at a time.

**SYSTEM NOTE**

- Intent classified: `ConceptInstance(Recipe)`
- SHACL loaded
- Required properties known, but not yet enforced

---

## Phase 2 — Structural Commitment

### AI

> Before we start:
>
> Is this:
>
> - A rough personal recipe
> - Or something you want others to cook from?

### USER

> Others should be able to cook it.

### AI

> Great.
>
> That means we’ll need clear quantities and serving size.
>
> Let’s start with the **title**.

---

## Phase 3 — Slot Population

### USER

> Grandmother’s apple pie

### AI

> I understood the title as:
>
> **“Grandmother’s Apple Pie”**
>
> Is that correct?

### USER

> Yes.

**SYSTEM NOTE**

- Emit `<Title>`
- File created with one node

---

### AI

> Next is the **serving size**.
>
> This tells people how much the recipe makes.
>
> For example:
>
> - “Serves 4”
> - “Serves 8”
>
> How many servings is this recipe?

---

### USER

> About 6 people.

### AI

> I’ll record that as:
>
> **Serves 6**
>
> Is that okay?

### USER

> Yes.

**SYSTEM NOTE**

- Emit `<Servings quantity={6} unit="people" />`
- This unlocks scaling later

---

### AI

> Next is a short **description**.
>
> One or two sentences is enough.

---

### USER

> A classic apple pie with a flaky crust and cinnamon filling.

### AI

> Description added.
>
> Now we’ll add the **ingredients**.
>
> We’ll do them one at a time.

---

## Ingredients loop (this is where the system shines)

### AI

> What’s the **first ingredient**?

### USER

> Flour.

### AI

> How much flour is used **for 6 servings**?

_(Notice: the AI explicitly anchors quantities to servings — no implicit math)_

---

### USER

> Two cups.

### AI

> I understood:
>
> - Ingredient: flour
> - Amount: 2
> - Unit: cups
> - For: 6 servings
>
> Is that correct?

### USER

> Yes.

**SYSTEM NOTE**

- Emit `<Ingredient amount="2" unit="cup">flour</Ingredient>`
- IngredientRef stored as lexical placeholder
- Valid because servings exist

---

### AI

> Next ingredient?

---

### USER

> Butter.

### AI

> How much butter for 6 servings?

---

### USER

> One cup, cold.

### AI

> I’ll record:
>
> - Ingredient: butter
> - Amount: 1 cup
> - Preparation note: cold
>
> Is that correct?

### USER

> Yes.

---

### AI

> Next ingredient?

---

### USER

> Apples.

### AI

> How many apples for 6 servings?

---

### USER

> Six medium apples.

### AI

> I’ll record:
>
> - Ingredient: apples
> - Amount: 6
> - Size: medium
>
> Is that correct?

### USER

> Yes.

---

### AI

> Are there more ingredients?

### USER

> Cinnamon and sugar.

### AI

> Let’s add them one at a time.
>
> How much cinnamon?

_(The AI refuses to bundle — structure over convenience)_

---

_(loop continues until user says “no more ingredients”)_

---

## Instructions loop

### AI

> Now let’s add the **instructions**.
>
> We’ll do them one step at a time.

---

### USER

> Cut butter into flour until crumbly.

### AI

> Step 1:
>
> **“Cut butter into flour until crumbly.”**
>
> Is that correct?

### USER

> Yes.

_(steps continue)_

---

## Phase 4 — Validation & Repair

### AI

> This Recipe is structurally complete.
>
> I noticed two optional things you may want to add:
>
> - Prep time
> - Bake temperature
>
> These aren’t required, but many cooks find them helpful.
>
> Would you like to add either?

**SYSTEM NOTE**

- These suggestions come from:
  - Recipe ontology best-practices
  - Not LLM free association

---

### USER

> Add bake temperature.

### AI

> What temperature should the oven be set to?

---

### USER

> 375 Fahrenheit.

### AI

> I’ll record:
>
> **Bake at 375°F**
>
> Is that correct?

---

## Phase 5 — Stabilization

### AI

> Your recipe:
>
> - Serves 6
> - Has ingredients tied to that serving size
> - Has complete instructions
>
> It’s now **valid and usable**.
>
> You can:
>
> - Publish it
> - Scale it (e.g. for 12 people)
> - Or refine it later

**SYSTEM NOTE**

- State → `Draft(StructurallyValid)`
- Grocery list derivation now possible

---

# 2. Why serving size unlocked everything

Because servings were declared **before** ingredients:

You can now:

- Scale the recipe deterministically
- Generate grocery lists across recipes
- Ask: “What do I need for 18 people?”
- Compare recipes meaningfully
- Attach nutrition later without rewriting data

If servings had been optional or late:

- You’d be guessing
- Or normalizing retroactively
- Or breaking invariants

You did the right thing by stopping us.

---

# 3. What friends will _see_ in a demo

When you demo this:

- The AI asks obvious, human questions
- Nothing feels technical
- The file grows visibly
- Scaling feels like magic — but isn’t
- Grocery list generation is trivial and impressive

And if someone says:

> “Why is it asking me that?”

You can answer honestly:

> “Because otherwise the system wouldn’t actually understand what you meant.”

That’s pedagogy surfaced.
