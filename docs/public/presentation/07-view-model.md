# ViewModel

The ViewModel is the stable contract between the language (CDX) and all renderers.

Renderers take a ViewModel and decide:

- how to lay it out,
- how to style it,
- how to make it interactive (if at all).

This keeps meaning, structure, and presentation cleanly separated — and lets non-technical authors describe systems once, then reuse them everywhere.

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

```

It is created by Scribe by combining:

- data (what exists and is true), and
- a view definition (what someone wants to see, grouped and ordered in a certain way).

The ViewModel answers the question:

“What should be shown, in what order, with what values?” — but it does not answer how it should look on screen, in print, or when spoken aloud.

Because the ViewModel is target-neutral, the same ViewModel can be rendered to a web page, a PDF, a voice interface, or any other output without changing the original data or view definition.
