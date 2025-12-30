# Scaling the recipe

Great. This is the payoff phase — where the earlier rigor suddenly feels _effortless_ to an observer.

I’ll do this in three tight sections:

1. **Scaling the recipe (servings as a control surface)**
2. **Deriving a grocery list (single + multiple recipes)**
3. **Why this still works for non-devs and doesn’t leak abstraction**

No new ontology unless absolutely necessary.

---

# 1. Scaling the recipe (the “aha” moment)

At this point, the system already has:

- A `Recipe`
- A declared `Servings = 6`
- All `IngredientUsage` amounts defined _relative to that serving size_

Nothing else is needed.

---

## Live interaction: scaling

### USER

> I want to make this for 12 people.

### AI

> Okay.
>
> The recipe currently serves **6**.
> You’re asking to scale it to **12**.
>
> That’s a factor of **2×**.
>
> Would you like me to:
>
> - Update the recipe itself
> - Or just calculate adjusted quantities?

**SYSTEM NOTE**

- AI is not assuming mutation
- Scaling is a _projection choice_

---

### USER

> Just calculate the quantities.

### AI

> Got it.
>
> Here are the adjusted ingredient amounts for **12 servings**:

_(Now the projection kicks in — no data mutation)_

---

### AI (rendered output)

- Flour: **4 cups**
- Butter: **2 cups**
- Apples: **12 medium**
- Sugar: **2 cups**
- Cinnamon: **2 teaspoons**

> The instructions stay the same.

**SYSTEM NOTE**

- This is a pure function:

  ```
  scaledAmount = baseAmount × (targetServings / baseServings)
  ```

- No ontology changes
- No revalidation needed

---

### USER

> Can I save that as a separate version?

### AI

> Yes.
>
> That would create a **fork**:
>
> - Original: serves 6
> - New version: serves 12
>
> Do you want to do that?

_(Notice: no silent overwrite, no “versioning magic”)_

---

## What friends see

They don’t see:

- RDF
- triples
- SPARQL
- IR

They see:

> “Oh. It just knows how much I need.”

That’s the illusion of simplicity earned by semantic discipline.

---

# 2. Grocery list derivation (single recipe)

Now let’s do the thing your friend actually cares about.

---

## Live interaction: grocery list

### USER

> Make me a shopping list for this recipe.

### AI

> For how many servings?
>
> - 6 (original)
> - 12 (scaled)
> - Or another amount?

---

### USER

> 6.

### AI

> Okay.
>
> Here’s the shopping list for **6 servings** of _Grandmother’s Apple Pie_:

---

### AI (rendered output)

**Shopping List**

- Flour — 2 cups
- Butter — 1 cup
- Apples — 6 medium
- Sugar — 1 cup
- Cinnamon — 1 teaspoon

Would you like this:

- Grouped by category (produce, dairy, etc.)?
- Or combined with other recipes?

**SYSTEM NOTE**

- Grouping is a _presentation concern_
- Ingredient identity is still lexical — and that’s fine

---

## Key point: nothing clever happened

No AI reasoning like:

> “People usually buy butter in sticks”

Unless you _explicitly add a module_ for that.

The system is honest.

---

# 3. Grocery list derivation (multiple recipes)

This is where ontology quietly proves its worth.

---

### USER

> Add my lasagna recipe too.

### AI

> Okay.
>
> For how many servings should I calculate each recipe?

---

### USER

> Apple pie for 6, lasagna for 8.

### AI

> Got it.
>
> I’ll combine the ingredients and total them.

**SYSTEM NOTE**

- Cross-recipe aggregation
- Requires:
  - ingredient identity comparison
  - unit normalization (if possible)

- If units conflict, the system **does not guess**

---

### AI (rendered output)

**Combined Shopping List**

**Produce**

- Apples — 6 medium
- Onions — 2
- Garlic — 4 cloves

**Dairy**

- Butter — 1 cup
- Ricotta — 500 g
- Mozzarella — 300 g

**Dry goods**

- Flour — 2 cups
- Sugar — 1 cup
- Lasagna sheets — 1 box

**Spices**

- Cinnamon — 1 teaspoon
- Oregano — 2 teaspoons

> Note: Some ingredients appear in different units across recipes.
> Let me know if you want me to normalize them.

---

## Why this doesn’t collapse

Because:

- Ingredient _usage_ is per-recipe
- Ingredient _identity_ is shared (or at least comparable)
- Units are explicit
- Servings anchor all math

If something can’t be combined safely, the system says so.

No lies.

---

# 4. Why non-devs can use this without understanding it

From the user’s perspective:

- They answered obvious questions
- They never chose a data type
- They never wrote syntax
- They never debugged anything

From the system’s perspective:

- Every quantity is typed
- Every transformation is reversible
- Every projection is explicit
- No information was invented

That’s the balance most systems miss.

---

# 5. Why this generalizes beyond recipes

Replace:

- Recipe → Lesson
- Ingredient → Resource
- Servings → Audience size

And suddenly you can:

- Scale curricula
- Generate reading lists
- Compare workloads
- Plan courses

Same architecture. Different ontology.

---

## Where we are now

At this point, you have:

- A believable non-dev authoring AI
- A complete Recipe flow
- Serving size as a first-class semantic pivot
- Scaling that is mathematically trivial and conceptually powerful
- Grocery lists that fall out naturally

Nothing here required:

- simplifying
- cutting corners
- pretending the AI “understands cooking”

It understands **structure**.

# Disagreement handled

Alright. Let’s do the **forking + disagreement** demo — this is the hardest part conceptually, and the place where Wikipedia, Google Docs, and most “collaborative” systems completely collapse.

I’ll show:

1. **What disagreement actually is in your system**
2. **How a non-dev expresses it**
3. **How forks preserve coherence**
4. **How the original stays stable**
5. **Why this doesn’t devolve into chaos**

All with the Recipe.

---

# 1. First: what disagreement is (and is not)

In your system, disagreement is **never**:

- editing someone else’s content silently
- overwriting facts
- arguing in comment blobs
- “improving” by stealth

Instead, disagreement is one of three _typed acts_:

1. **Annotation** – “I think this is wrong / unclear”
2. **Alternative** – “I do it differently”
3. **Fork** – “This is a different recipe now”

This is straight editorial discipline, mechanized.

---

# 2. The scenario

We have a **stable recipe**:

> _Grandmother’s Apple Pie_
> Serves 6
> Sugar: **1 cup**

Now enter a family member.

---

## 3. Non-dev disagreement: annotation first

### USER (mum)

> This is too sweet. Grandma used less sugar.

### AI

> Thanks — I won’t change the recipe itself.
>
> How would you like to record this?
>
> - A comment for the author
> - A suggested change
> - Or an alternative version of the recipe

**SYSTEM NOTE**

- The AI refuses to mutate canonical content
- Presents _editorial options_, not technical ones

---

### USER

> A suggested change.

### AI

> Okay.
>
> What part of the recipe does this apply to?

_(Notice: disagreement must be **targeted**, not vague)_

---

### USER

> The sugar amount.

### AI

> Got it.
>
> What amount do you suggest instead?

---

### USER

> Half a cup.

### AI

> I’ll record a suggestion:
>
> - Original: 1 cup sugar
> - Suggested: ½ cup sugar
>
> With the note:
> _“Grandma used less sugar.”_
>
> Is that correct?

### USER

> Yes.

---

### What the system now has

- The **original recipe is unchanged**
- A **typed suggestion** exists:
  - Target: IngredientUsage(sugar)
  - Type: QuantityAlternative
  - Author: mum
  - Rationale: textual, quarantined

No chaos.
No edit wars.

---

# 4. Escalation: fork instead of argument

Now suppose the author responds.

---

### USER (author)

> This isn’t the same recipe. Grandma’s version really was different.

### AI

> In that case, the cleanest option is to create a **fork**.
>
> The fork will:
>
> - Start from the current recipe
> - Change only what you decide
> - Remain linked to the original
>
> Do you want to do that?

---

### USER

> Yes.

---

## 5. Fork creation (explicit, visible)

### AI

> Okay.
>
> We’re creating a fork:
>
> **“Grandmother’s Apple Pie (Less Sugar)”**
>
> The original recipe will stay unchanged.

**SYSTEM NOTE**

- New Recipe node
- `forkOf` relationship recorded
- All content copied structurally

---

### AI

> What should the sugar amount be in this version?

### USER

> Half a cup.

### AI

> Done.
>
> Everything else remains the same.

---

## 6. What the fork looks like semantically

Now you have:

- **Recipe A**
  _Grandmother’s Apple Pie_
  Sugar: 1 cup
  Status: Stable Canonical

- **Recipe B**
  _Grandmother’s Apple Pie (Less Sugar)_
  Sugar: ½ cup
  Relationship: `forkOf → Recipe A`

This is not duplication.
This is **lineage**.

---

# 7. How coherence is preserved

Here’s why this doesn’t explode:

### 7.1 Search results

When someone searches for:

> “apple pie”

They see:

- The canonical recipe
- Plus a visible indicator:

  > “This recipe has 1 alternative version”

No opinion blending.
No silent averaging.

---

### 7.2 Grocery lists

If a user selects:

- Recipe A → they get 1 cup sugar
- Recipe B → they get ½ cup sugar

If they select both:

- The system does **not** merge sugar amounts
- It flags a conflict:

  > “Two versions of the same recipe selected”

Honesty over cleverness.

---

### 7.3 Future disagreement

If someone says:

> “Even half a cup is too sweet”

They fork **the fork**.

This creates a _tree_, not a mess.

---

# 8. How this differs from Wikipedia (the key point)

Wikipedia enforces:

- Single mutable artifact
- Illusion of neutrality
- Power struggles
- Edit wars

Your system enforces:

- Immutable published artifacts
- Explicit alternatives
- Lineage, not dominance
- No pretense of neutrality

That’s why you called it **neutrality theater** — correctly.

---

# 9. Why non-devs understand this intuitively

Because it matches real life:

- “That’s not how _I_ do it”
- “That’s a different version”
- “Here’s my take”
- “Use whichever you like”

The system doesn’t force consensus.
It forces **clarity**.

---

# 10. The killer demo moment

When you demo this to friends, this is the moment that lands:

> “We didn’t argue.
> We didn’t overwrite.
> We didn’t comment-fight.
> We just… branched reality.”

And then you show:

- Both recipes
- Both grocery lists
- Both serving scalings
- The explicit relationship

That’s when people realize this isn’t a CMS.

It’s an **editorial system**.

---

## Where you are now (take stock)

You now have, end-to-end:

- Non-dev authoring
- Semantic structure
- Serving-aware quantities
- Scaling
- Grocery lists
- Forking without collapse
- Disagreement without warfare

All without:

- simplifying
- handwaving
- AI “creativity”
- magic knowledge

Everything is traceable.

---

If you want to keep pushing, the next _really_ interesting stress test is:

> **Two forks that partially disagree**
> (e.g. less sugar _and_ different apples)

Or:

> **Re-merging ideas without merging data**
> (editorial synthesis instead of Git merge)

Or:

> **Applying this exact machinery to curricula or docs**
