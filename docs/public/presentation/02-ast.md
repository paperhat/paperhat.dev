# AST

The Codex (.cdx) files are parsed into an Abstract Syntax Tree (AST) to facilitate further processing and rendering. The AST represents the hierarchical structure of the data, making it easier to manipulate and transform.

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

```
