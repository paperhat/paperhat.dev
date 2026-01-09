# AST (Abstract Syntax Tree)

Once a Codex (`.cdx`) file is read, the first thing Paperhat does is **parse it into an Abstract Syntax Tree (AST)**.

The AST is not a new interpretation of your data.
It is the **same information**, rewritten into a precise, unambiguous structure that a computer can work with safely.

At this stage:
- nothing is inferred
- nothing is validated beyond structure
- nothing is “understood” semantically yet

The AST exists so that the rest of the pipeline can operate on **structure**, not text.

---

## Example

Below is a simplified AST representation corresponding to parts of the recipe CDX.
Each node records:
- the concept type (`t`)
- its traits (`a`)
- its children (`c`)

```ts
{ t: "Servings", a: { amount: "2", unit: "persons" }, c: [] },
{ t: "PreparationTime", a: { duration: "10", unit: "minutes" }, c: [] },
{ t: "CookingTime", a: { duration: "12", unit: "minutes" }, c: [] },

{
  t: "Ingredients",
  a: {},
  c: [
    { t: "Ingredient", a: { name: "Spaghetti", amount: "200", unit: "grams" }, c: [] },
    { t: "Ingredient", a: { name: "Extra-virgin olive oil", amount: "3", unit: "tablespoons" }, c: [] },
    { t: "Ingredient", a: { name: "Garlic cloves", amount: "3", unit: "cloves", preparation: "thinly sliced" }, c: [] },
    { t: "Ingredient", a: { name: "Dried chili flakes", amount: "0.5", unit: "teaspoon", optional: "true" }, c: [] },
    { t: "Ingredient", a: { name: "Fresh parsley", amount: "2", unit: "tablespoons", preparation: "finely chopped" }, c: [] },
    { t: "Ingredient", a: { name: "Salt", toTaste: "true" }, c: [] }
  ]
},

{
  t: "Equipment",
  a: {},
  c: [
    { t: "Item", a: {}, c: ["Large pot"] },
    { t: "Item", a: {}, c: ["Skillet"] },
    { t: "Item", a: {}, c: ["Colander"] }
  ]
},

{
  t: "Steps",
  a: {},
  c: [
    { t: "Step", a: {}, c: ["Bring a large pot of salted water to a boil."] },
    { t: "Step", a: {}, c: ["Cook spaghetti until al dente. Reserve a cup of pasta water, then drain."] },
    { t: "Step", a: {}, c: ["Warm olive oil in a skillet over low heat."] },
    { t: "Step", a: {}, c: ["Add garlic and cook gently until fragrant (do not brown)."] },
    { t: "Step", a: { optional: "true" }, c: ["Stir in chili flakes for 10–20 seconds."] },
    { t: "Step", a: {}, c: ["Add pasta and toss. Splash in pasta water until glossy."] },
    { t: "Step", a: {}, c: ["Remove from heat, add parsley, adjust salt to taste."] },
    { t: "Step", a: {}, c: ["Serve immediately."] }
  ]
},

{
  t: "Tags",
  a: {},
  c: [
    { t: "Tag", a: {}, c: ["Italian"] },
    { t: "Tag", a: {}, c: ["Pasta"] },
    { t: "Tag", a: {}, c: ["Quick"] },
    { t: "Tag", a: {}, c: ["Vegetarian"] }
  ]
},

{ t: "Source", a: {}, c: ["Personal recipe"] }
````

---

## How to read this (non-technical)

This is still *your recipe* — just written in a way that removes ambiguity.

* Every concept becomes a node.
* Every trait is captured exactly.
* Every piece of text is preserved.
* The nesting structure is made explicit.

Nothing has been interpreted yet.
This step exists so the system cannot “misread” what you wrote.

Think of the AST as a **faithful transcript** of the CDX file, prepared for further processing.

---

## For technical readers

The AST is a **lossless structural representation** of the authored CDX.

### Why an AST exists at all

Working directly on source text is fragile:

* whitespace matters accidentally
* ordering is ambiguous
* errors are hard to localize
* transformations become ad hoc

The AST solves this by:

* making structure explicit
* separating parsing from interpretation
* providing stable node shapes for downstream phases

Every later step in the pipeline depends on this discipline.

---

### What the AST does *not* do

At this stage, the AST:

* does **not** normalize structure
* does **not** resolve identity
* does **not** validate against ontology
* does **not** attach meaning
* does **not** infer relationships

It reflects *author intent*, not semantic truth.

This is why AST is distinct from the next phase (IR).

---

### Provenance and source location

In the real system, AST nodes also carry:

* source file identity
* character offsets
* line and column numbers

This information is preserved so that:

* diagnostics can point back to authored CDX
* later transformations remain explainable
* round-tripping is possible

Nothing downstream is allowed to “forget where it came from”.

---

### Why this separation matters

By isolating parsing into a dedicated AST phase, Paperhat ensures that:

* syntax errors are caught early
* semantics are applied consistently
* later transformations are deterministic
* rendering never depends on string tricks

This strict separation is what makes the rest of the pipeline predictable.

The next step builds on this structure to create a **canonical internal representation**.
