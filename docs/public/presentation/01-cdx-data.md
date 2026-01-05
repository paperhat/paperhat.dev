# Codex

All data is captured in Codex (.cdx) files in the application, organized by module in a `modules` folder. Folders that do not participate in the routing have a prepended underscore.

Example:

In `/modules/recipes/_data/spaghetti-aglio-e-olio.cdx`:

```tsx
<Recipe title="Spaghetti Aglio e Olio">
  <Summary>A quick pasta with garlic, olive oil, chili, and parsley.</Summary>

  <Servings amount="2" unit="persons" />
  <PreparationTime duration="10" unit="minutes" />
  <CookingTime duration="12" unit="minutes" />

  <Ingredients>
    <Ingredient name="Spaghetti" amount="200" unit="grams" />
    <Ingredient name="Extra-virgin olive oil" amount="3" unit="tablespoons" />
    <Ingredient name="Garlic cloves" amount="3" unit="cloves" preparation="thinly sliced" />
    <Ingredient name="Dried chili flakes" amount="0.5" unit="teaspoon" optional="true" />
    <Ingredient name="Fresh parsley" amount="2" unit="tablespoons" preparation="finely chopped" />
    <Ingredient name="Salt" toTaste="true" />
  </Ingredients>

  <Equipment>
    <Item>Large pot</Item>
    <Item>Skillet</Item>
    <Item>Colander</Item>
  </Equipment>

  <Steps>
    <Step>Bring a large pot of salted water to a boil.</Step>
    <Step>Cook spaghetti until al dente. Reserve a cup of pasta water, then drain.</Step>
    <Step>Warm olive oil in a skillet over low heat.</Step>
    <Step>Add garlic and cook gently until fragrant (do not brown).</Step>
    <Step optional="true">Stir in chili flakes for 10–20 seconds.</Step>
    <Step>Add pasta and toss. Splash in pasta water until glossy.</Step>
    <Step>Remove from heat, add parsley, adjust salt to taste.</Step>
    <Step>Serve immediately.</Step>
  </Steps>

  <Tags>
    <Tag>Italian</Tag>
    <Tag>Pasta</Tag>
    <Tag>Quick</Tag>
    <Tag>Vegetarian</Tag>
  </Tags>

  <Source>Personal recipe</Source>
</Recipe>

```
