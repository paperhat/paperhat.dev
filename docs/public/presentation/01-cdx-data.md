# Codex (CDX Data)

All application data in Paperhat is authored in **Codex (`.cdx`) files**.

A CDX file does not describe *how* something should be stored, queried, or displayed.
It describes **what exists** — using a shared, well-defined vocabulary.

In other words: CDX is how you *state facts* about the world your application knows about.

CDX files live alongside your application code, typically organized by domain or feature
inside a `modules` folder. Folders that do not participate in routing or navigation are
prefixed with an underscore.

You do not invent structure in CDX. You **use documented concepts and traits** that are already defined by Paperhat (or by a domain library your application depends on).

---

## Example

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
````

---

## How to read this (non-technical)

* `<Recipe>` says *what kind of thing this is*.
* Traits like `title`, `amount`, or `unit` capture **specific facts** the system understands.
* Text inside concepts (like steps or summaries) is **descriptive**, written for people.
* The structure comes from Paperhat — you are **filling it in**, not designing it.

Think of this as *adding a recipe to a shared cookbook*:
the format already exists, and your job is to provide the content.

You cannot make up new tags or traits here.
If something is not documented, it is not valid CDX and will be rejected.

---

## For technical readers

CDX is a **declarative semantic authoring language**, not a markup language and not a UI
component system.

### Concepts, not components

CDX uses the term **concept** deliberately.

Although `<Recipe>` corresponds to an ontological *class* and each instance represents an
*individual*, CDX itself is not an object system and does not model behavior.

At different layers, the same thing is described differently:

* In CDX: `<Recipe>` is an **concept**
* In ontology terms: `Recipe` is a **class**
* In RDF: an instance has `rdf:type Recipe`

Each term is correct in its own layer. CDX stays intentionally surface-level and structural.

---

### Semantic density: why traits vs concept content

CDX distinguishes between **high-density** and **low-density** semantics.

* **Concept names and traits** carry high semantic density:

  * they are structured
  * validated
  * queryable
  * suitable for inference
* **Concept content (text)** carries low semantic density:

  * descriptive
  * opinionated
  * human-oriented
  * not relied on for semantic reasoning

For example:

* `amount="200"` and `unit="grams"` are facts the system can reason about.
* “Cook spaghetti until al dente” is meaningful to humans, but not treated as a formal claim.

This separation prevents accidental inference from prose while preserving rich description.

---

### Vocabulary and schema ownership

You cannot invent new concepts or traits in CDX.

Every concept and trait comes from a **defined schema**:

* core schemas are provided by Paperhat
* additional schemas may come from domain libraries
* schemas are documented, versioned, and validated

CDX files **use schemas**; they do not define them.

This guarantees that:

* data is structurally valid
* queries are stable
* renderers and tools agree on meaning

---

### Why this matters

Because CDX data is:

* constrained
* deterministic
* structurally meaningful

…it can be safely compiled, validated, stored as a graph, queried, and rendered in
many different ways — without rewriting or reinterpreting the original data.

Later stages in the pipeline depend on these guarantees.
