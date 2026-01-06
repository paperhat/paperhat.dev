# SPARQL queries (system-owned retrieval)

At this point we have:

- **data** stored as an RDF graph
- a **view definition** that declares what should be presented

Now Scribe retrieves the required facts from the triple store.

End users do **not** write SPARQL.
These queries are part of the Paperhat/Scribe system (generated, templated, or selected),
so that non-technical authors only need to write:

- data CDX
- view CDX

SPARQL is shown here to make the pipeline explainable: it is the concrete mechanism
used to retrieve graph data for shaping into a ViewModel.

---

## Set the ontology prefixes

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>
````

## Choose the recipe

```sparql
BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)
```

---

## Query A: Header (Title, Summary, Source)

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT ?title ?summary ?source
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)

  ?recipe ex:title ?title .
  OPTIONAL { ?recipe ex:summary ?summary . }
  OPTIONAL { ?recipe ex:source ?source . }
}
LIMIT 1
```

View nodes filled: `Title`, `Summary`, `Source`.

Shaping rule: `single row -> direct fields`.

---

## Query B: QuickFacts (Servings, PreparationTime, CookingTime)

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT ?servingsAmount ?servingsUnit ?prepMinutes ?cookMinutes
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)

  OPTIONAL { ?recipe ex:servingsAmount ?servingsAmount . }
  OPTIONAL { ?recipe ex:servingsUnit ?servingsUnit . }

  OPTIONAL { ?recipe ex:preparationTimeMinutes ?prepMinutes . }
  OPTIONAL { ?recipe ex:cookingTimeMinutes ?cookMinutes . }
}
LIMIT 1
```

View nodes filled: `QuickFacts/Servings`, `QuickFacts/PreparationTime`, `QuickFacts/CookingTime`.

Shaping rule: `single row -> create a QuickFacts group with label/value entries`.

---

## Query C: Ingredients list

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT
  ?ingredient
  ?name
  ?amount
  ?unit
  ?preparation
  ?optional
  ?toTaste
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)

  ?recipe ex:hasIngredient ?ingredient .
  OPTIONAL { ?ingredient ex:name ?name . }

  OPTIONAL {
    ?ingredient ex:quantity ?q .
    OPTIONAL { ?q ex:amount ?amount . }
    OPTIONAL { ?q ex:unit ?unit . }
  }

  OPTIONAL { ?ingredient ex:preparation ?preparation . }
  OPTIONAL { ?ingredient ex:optional ?optional . }
  OPTIONAL { ?ingredient ex:toTaste ?toTaste . }
}
ORDER BY LCASE(STR(?name))
```

View nodes filled: `Ingredients/List/IngredientName`, `IngredientQuantity`, `IngredientPreparationNote`, `IngredientOptionalBadge`.

Shaping rule: `each row → one IngredientRow in the ViewModel list`:

* `name → IngredientRow.name`
* `(amount + unit) → IngredientRow.quantity (string formatting)`
* `preparation → IngredientRow.note`
* `optional = true → IngredientRow.badge = "optional"`
* `toTaste = true → IngredientRow.note = "to taste" if no quantity (or append)`

---

## Query D: Equipment list

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT ?equipmentItem
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)

  ?recipe ex:requiresEquipment ?equipmentItem .
}
ORDER BY LCASE(STR(?equipmentItem))
```

View nodes filled: `Equipment/List/EquipmentItem` (one item per row).

Shaping rule: `ordered rows -> list of strings`.

---

## Query E: Steps list

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT ?tag
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)
  ?recipe ex:tag ?tag .
}
ORDER BY LCASE(STR(?tag))
```

View nodes filled: `Steps/NumberedList/StepText`, `StepOptionalBadge`.

Shaping rule: `ordered rows → numbered list items`:

* `text → StepRow.text`
* `optional = true → badge optional`

(If index is missing, Scribe can fall back to document order provenance.)

---

## Query F: Tags

```sparql
PREFIX ex:     <https://sitebender.example/demo/>
PREFIX recipe: <https://sitebender.example/demo/recipe/>

SELECT ?tag
WHERE {
  BIND(recipe:spaghetti-aglio-e-olio AS ?recipe)
  ?recipe ex:tag ?tag .
}
ORDER BY LCASE(STR(?tag))
```

View nodes filled: `Tags`.

Shaping rule: collect into list of strings.

---

## Wiring summary

How these queries wire up the ViewModel:

* `<Title />` → Query A → `Title.text`
* `<Summary />` → Query A → `Summary.text`
* `<QuickFacts>` → Query B → three `Fact` entries
* `<List source="Ingredients">` → Query C → list of `IngredientRow`
* `<List source="Equipment">` → Query D → list of strings
* `<NumberedList source="Steps">` → Query E → list of `StepRow` ordered by index
* `<Tags />` → Query F → list of strings
* `<Source />` → Query A → `Source.text`

---

## For technical readers

These queries are intentionally **boring**.

They avoid:

* inference
* hidden joins
* “smart” reconstruction logic

because the stability guarantee lives in the pipeline:

* **IR** produces deterministic identities and structure
* **RDF** persists that structure as a graph
* **SPARQL** retrieves facts
* **shaping rules** convert results into a stable ViewModel

This keeps each phase single-purpose and explainable.

The next page shows the resulting **ViewModel**: a target-neutral data structure
that presentation planning and rendering can consume without knowing SPARQL.
