# Defining the view

Now that the data exists as a semantic graph, we define a **view**.

A view describes **what should be presented** to a human and **how that information is
structured**, without saying anything about layout, styling, or platform.

Views are authored in CDX, just like data.
They are **not rendering instructions**.
They are **projections** over semantic data.

The same data can have many views.

---

## Example

Below is a view definition for presenting a recipe.

```tsx
<RecipeView id="view:recipe-default" for="Recipe">
  <Title />
  <Summary />

  <QuickFacts>
    <Servings />
    <PreparationTime />
    <CookingTime />
  </QuickFacts>

  <Section title="Ingredients">
    <List source="Ingredients">
      <Item>
        <IngredientName />
        <IngredientQuantity />
        <IngredientPreparationNote />
        <IngredientOptionalBadge />
      </Item>
    </List>
  </Section>

  <Section title="Equipment">
    <List source="Equipment">
      <Item><EquipmentItem /></Item>
    </List>
  </Section>

  <Section title="Steps">
    <NumberedList source="Steps">
      <Item>
        <StepText />
        <StepOptionalBadge />
      </Item>
    </NumberedList>
  </Section>

  <Tags />
  <Source />
</RecipeView>
````

---

## How to read this (non-technical)

This view says:

* which parts of the recipe matter
* how they are grouped
* what order they appear in
* which details are included

It does **not** say:

* what it looks like
* how it is styled
* whether it’s a web page, a card, or a voice response

Think of a view as the **outline of a presentation**, not the presentation itself.

The same recipe can be shown in many different ways by using different views.

---

## For technical readers

A view is a **declarative projection specification**.

### What a view does

A view:

* selects semantic concepts (e.g. Ingredients, Steps)
* defines structural grouping
* introduces symbolic presentation slots
* establishes a stable shape for retrieval and shaping

It is authored independently of:

* storage
* queries
* layout
* target platform

---

### Views vs queries

Views are **author intent**. Queries are **retrieval mechanics**.

The system uses the view definition to determine:

* what data must be retrieved
* how query results should be shaped

SPARQL queries are generated or selected by the system. End users do not write them.

---

### Views vs Presentation Plans

This boundary is critical:

* **View** answers: *what is presented?*
* **Presentation Plan** answers: *how is it presented here?*

A single view may feed:

* a web presentation plan
* a print presentation plan
* a voice presentation plan

Design Policy is applied **after** the ViewModel is constructed, not at view definition time.

---

### Why this matters

Because views are:

* semantic
* reusable
* target-neutral

…the same underlying data can support many interfaces without being rewritten, and without embedding presentation decisions into the data itself.

The next step shows how the system retrieves the data required by a view using graph queries.
