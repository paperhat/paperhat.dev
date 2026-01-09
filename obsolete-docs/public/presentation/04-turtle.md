# Turtle (RDF Triples)

After the data has been normalized into IR, Paperhat converts it into
**RDF triples**, expressed here using **Turtle** syntax.

This is the point where the data stops being a tree and becomes a **graph**.

Nothing new is added.
Nothing is lost.
The same information is now expressed in a form that can be:
- stored independently
- shared across systems
- queried flexibly
- validated against formal constraints

Turtle is just a readable way to write down that graph.

---

## Example

Below is the same recipe, now expressed as an RDF graph using Turtle.

```turtle
@prefix ex:    <https://paperhat.example/demo/> .
@prefix recipe:<https://paperhat.example/demo/recipe/> .
@prefix ing:   <https://paperhat.example/demo/ingredient/> .
@prefix step:  <https://paperhat.example/demo/step/> .
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
````

---

## How to read this (non-technical)

This is the same recipe again — but now it is no longer “inside” a document.

Each thing:

* the recipe
* each ingredient
* each step

exists as its **own identifiable object**, connected to others by named relationships.

Think of this as turning a written recipe into a **network of facts** that other systems
can understand, share, and ask questions about.

---

## For technical readers

This step converts the canonical IR into a **semantic graph**.

### From trees to graphs

Up to this point, all representations have been tree-shaped:

* CDX is nested
* AST is hierarchical
* IR is structured

RDF removes the tree constraint.

In a graph:

* nodes can have many parents
* relationships are first-class
* order is explicit, not implied
* identity is global

This is why RDF is the persistence and query boundary.

---

### What becomes explicit here

In RDF:

* identity is expressed as IRIs
* class membership is explicit (`a ex:Recipe`)
* relationships are named predicates
* literals are typed
* derived facts are preserved with provenance

Nothing depends on document structure anymore.

---

### Why not stay in IR?

IR is application-internal.
RDF is **interoperable and durable**.

Using RDF allows:

* storage independent of application code
* formal constraint checking (via SHACL)
* flexible querying (via SPARQL)
* cross-domain linking
* long-term stability

IR exists to *produce* this graph cleanly.
The graph exists so the data can live on its own.

---

### Turtle is not the point

Turtle is just one syntax for RDF.

It is used here because:

* it is compact
* it is readable
* it maps directly to triples

The important thing is the **graph**, not the notation.

---

### Why this matters

Once the data is a graph:

* it can be validated independently
* queried in many ways
* projected into different views
* rendered for different targets

The next page shows how we declare what should be presented from this graph, without committing to any particular output or platform.
