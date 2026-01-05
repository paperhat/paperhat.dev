# Turtle

Turtle (Terse RDF Triple Language) is a syntax for expressing data in the Resource Description Framework (RDF) format. It is designed to be a more human-readable and compact way to represent RDF graphs compared to other formats like RDF/XML.

In the context of our recipe application, we use Turtle to represent recipes and their components in a structured way that can be easily shared and understood by other systems.

```turtle
@prefix ex:    <https://sitebender.example/demo/> .
@prefix recipe:<https://sitebender.example/demo/recipe/> .
@prefix ing:   <https://sitebender.example/demo/ingredient/> .
@prefix step:  <https://sitebender.example/demo/step/> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

# --- Recipe (subject) ---

recipe:spaghetti-aglio-e-olio
  a ex:Recipe ;
  ex:title "Spaghetti Aglio e Olio" ;
  ex:summary "A quick pasta with garlic, olive oil, chili, and parsley." ;

  ex:servingsAmount 2 ;
  ex:servingsUnit ex:Persons ;

  ex:preparationTimeMinutes 10 ;
  ex:cookingTimeMinutes 12 ;
  ex:totalTimeMinutes 22 ;

  ex:hasIngredient ing:spaghetti ;
  ex:hasIngredient ing:extra-virgin-olive-oil ;
  ex:hasIngredient ing:garlic-cloves ;
  ex:hasIngredient ing:dried-chili-flakes ;
  ex:hasIngredient ing:fresh-parsley ;
  ex:hasIngredient ing:salt ;

  ex:requiresEquipment "Large pot" ;
  ex:requiresEquipment "Skillet" ;
  ex:requiresEquipment "Colander" ;

  ex:hasStep step:1 ;
  ex:hasStep step:2 ;
  ex:hasStep step:3 ;
  ex:hasStep step:4 ;
  ex:hasStep step:5 ;
  ex:hasStep step:6 ;
  ex:hasStep step:7 ;
  ex:hasStep step:8 ;

  ex:tag "Italian" ;
  ex:tag "Pasta" ;
  ex:tag "Quick" ;
  ex:tag "Vegetarian" ;

  ex:source "Personal recipe" ;

  ex:provenance [
    ex:stepOrderingPolicy ex:DocumentOrder ;
    ex:derivedIds true ;
    ex:derivedTotalTime true
  ] .

# --- Ingredients ---

ing:spaghetti
  a ex:Ingredient ;
  ex:name "Spaghetti" ;
  ex:quantity [
    ex:amount "200"^^xsd:decimal ;
    ex:unit "grams"
  ] ;
  ex:optional false .

ing:extra-virgin-olive-oil
  a ex:Ingredient ;
  ex:name "Extra-virgin olive oil" ;
  ex:quantity [
    ex:amount "3"^^xsd:decimal ;
    ex:unit "tablespoons"
  ] ;
  ex:optional false .

ing:garlic-cloves
  a ex:Ingredient ;
  ex:name "Garlic cloves" ;
  ex:preparation "thinly sliced" ;
  ex:quantity [
    ex:amount "3"^^xsd:decimal ;
    ex:unit "cloves"
  ] ;
  ex:optional false .

ing:dried-chili-flakes
  a ex:Ingredient ;
  ex:name "Dried chili flakes" ;
  ex:quantity [
    ex:amount "0.5"^^xsd:decimal ;
    ex:unit "teaspoon"
  ] ;
  ex:optional true .

ing:fresh-parsley
  a ex:Ingredient ;
  ex:name "Fresh parsley" ;
  ex:preparation "finely chopped" ;
  ex:quantity [
    ex:amount "2"^^xsd:decimal ;
    ex:unit "tablespoons"
  ] ;
  ex:optional false .

ing:salt
  a ex:Ingredient ;
  ex:name "Salt" ;
  ex:toTaste true ;
  ex:optional false .

# --- Steps (order derived from document; idx included for convenience) ---

step:1
  a ex:Step ;
  ex:index 1 ;
  ex:text "Bring a large pot of salted water to a boil." ;
  ex:optional false .

step:2
  a ex:Step ;
  ex:index 2 ;
  ex:text "Cook spaghetti until al dente. Reserve a cup of pasta water, then drain." ;
  ex:optional false .

step:3
  a ex:Step ;
  ex:index 3 ;
  ex:text "Warm olive oil in a skillet over low heat." ;
  ex:optional false .

step:4
  a ex:Step ;
  ex:index 4 ;
  ex:text "Add garlic and cook gently until fragrant (do not brown)." ;
  ex:optional false .

step:5
  a ex:Step ;
  ex:index 5 ;
  ex:text "Stir in chili flakes for 10–20 seconds." ;
  ex:optional true .

step:6
  a ex:Step ;
  ex:index 6 ;
  ex:text "Add pasta and toss. Splash in pasta water until glossy." ;
  ex:optional false .

step:7
  a ex:Step ;
  ex:index 7 ;
  ex:text "Remove from heat, add parsley, adjust salt to taste." ;
  ex:optional false .

step:8
  a ex:Step ;
  ex:index 8 ;
  ex:text "Serve immediately." ;
  ex:optional false .

```
