# Defining the view

We use CDX now to define the view for our application. The view is responsible for rendering the user interface and displaying data to the user. It is used to create the ViewModel, which will be used by the rendering system to display the data _depending on the target platform_.

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
```
