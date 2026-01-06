# ViewModel

The **ViewModel** is an internal structure created by the system.

It is **not written by users**, **not edited**, and **not normally seen**.
The ViewModel is produced automatically by **Scribe** by combining:

- **data CDX** (what exists and is true), and
- **view CDX** (what someone wants to see, grouped and ordered).

The ViewModel is the stable contract between authored intent and rendering.

Renderers do not query data and do not interpret meaning.
They receive a ViewModel and decide only:

- how to lay it out,
- how to style it,
- how to make it interactive (if at all).

This separation allows authors to describe systems once, and reuse them everywhere,
without needing to think about technical details.

---

## Example

Below is an example ViewModel produced for the recipe view.

```json
{
  "view": "RecipeView",
  "subject": "recipe:spaghetti-aglio-e-olio",

  "nodes": [
    {
      "type": "Title",
      "text": "Spaghetti Aglio e Olio"
    },
    {
      "type": "Summary",
      "text": "A quick pasta with garlic, olive oil, chili, and parsley."
    },
    {
      "type": "Group",
      "role": "QuickFacts",
      "items": [
        {
          "type": "Fact",
          "label": "Servings",
          "value": "2 persons"
        },
        {
          "type": "Fact",
          "label": "Preparation time",
          "value": "10 minutes"
        },
        {
          "type": "Fact",
          "label": "Cooking time",
          "value": "12 minutes"
        }
      ]
    },
    {
      "type": "Section",
      "title": "Ingredients",
      "content": {
        "type": "List",
        "kind": "unordered",
        "items": [
          {
            "type": "IngredientRow",
            "name": "Spaghetti",
            "quantity": "200 grams"
          },
          {
            "type": "IngredientRow",
            "name": "Extra-virgin olive oil",
            "quantity": "3 tablespoons"
          },
          {
            "type": "IngredientRow",
            "name": "Garlic cloves",
            "quantity": "3 cloves",
            "note": "thinly sliced"
          },
          {
            "type": "IngredientRow",
            "name": "Dried chili flakes",
            "quantity": "0.5 teaspoon",
            "badge": "optional"
          },
          {
            "type": "IngredientRow",
            "name": "Fresh parsley",
            "quantity": "2 tablespoons",
            "note": "finely chopped"
          },
          {
            "type": "IngredientRow",
            "name": "Salt",
            "note": "to taste"
          }
        ]
      }
    },
    {
      "type": "Section",
      "title": "Steps",
      "content": {
        "type": "List",
        "kind": "numbered",
        "items": [
          {
            "type": "StepRow",
            "text": "Bring a large pot of salted water to a boil."
          },
          {
            "type": "StepRow",
            "text": "Cook spaghetti until al dente. Reserve a cup of pasta water, then drain."
          },
          {
            "type": "StepRow",
            "text": "Warm olive oil in a skillet over low heat."
          },
          {
            "type": "StepRow",
            "text": "Add garlic and cook gently until fragrant (do not brown)."
          },
          {
            "type": "StepRow",
            "text": "Stir in chili flakes for 10–20 seconds.",
            "badge": "optional"
          },
          {
            "type": "StepRow",
            "text": "Add pasta and toss. Splash in pasta water until glossy."
          },
          {
            "type": "StepRow",
            "text": "Remove from heat, add parsley, adjust salt to taste."
          },
          {
            "type": "StepRow",
            "text": "Serve immediately."
          }
        ]
      }
    },
    {
      "type": "Tags",
      "values": ["Italian", "Pasta", "Quick", "Vegetarian"]
    },
    {
      "type": "Source",
      "text": "Personal recipe"
    }
  ]
}
````

---

## How to read this (non-technical)

You never write this structure yourself.

The system creates it so that everything you wrote can be shown correctly,
in the right order, every time.

Think of the ViewModel as a **prepared script behind the scenes**:

* you write the content,
* you describe how it should be grouped,
* the system prepares a clean, complete version for presentation.

Because of this, you don’t need to worry about formatting rules,
layout decisions, or technical edge cases.
Those decisions happen later.

---

## For technical readers

The ViewModel is a **target-neutral, policy-free presentation data structure**.

### What the ViewModel is

* created automatically by Scribe
* derived from data CDX + view CDX
* ordered, explicit, and complete
* safe for renderers to consume directly

### What the ViewModel is not

* not authored by users
* not persisted as a source of truth
* not a configuration API
* not responsible for layout, styling, or interaction

---

### View vs ViewModel vs Presentation Plan

This separation is intentional:

* **View (CDX)**
  Declares *what* is conceptually presented and how it is grouped.

* **ViewModel**
  Is the concrete, ordered result of combining a view with data.

* **Presentation Plan**
  Decides *how* that ViewModel should be arranged for a specific medium
  (screen, print, voice, etc.), using Design Policy.

Each step narrows possibilities without mixing concerns.

---

### Why this matters

Because the ViewModel is stable and invisible to authors:

* non-technical users don’t have to think like programmers
* designers can change presentation without touching data
* renderers stay simple and interchangeable
* the system remains explainable end to end

The next page introduces Design Policy — the declarative rules that describe how content should be presented in general, without changing its meaning.

These policies are later applied to a ViewModel and a target context to produce a concrete Presentation Plan.
