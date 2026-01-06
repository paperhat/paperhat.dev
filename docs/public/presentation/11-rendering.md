# Rendering

Rendering is the final step in the pipeline.

At this point:
- all meaning is resolved,
- all presentation decisions have been made,
- and nothing remains ambiguous.

Rendering takes a **Presentation Plan** and produces a concrete output for a specific target:
HTML, print, voice, or any other medium.

Renderers do not make decisions.
They execute them.

---

## What rendering does (and does not do)

Rendering does **not**:
- decide what is important
- decide what should be grouped
- decide how much detail to show
- apply design rules
- interpret meaning

All of that has already happened.

Rendering **only** translates a finalized plan into a target-specific form.

---

## Example: Web (HTML)

Below is one possible rendering of the same Presentation Plan as HTML.

```html
<h1>Spaghetti Aglio e Olio</h1>

<p class="summary">A quick pasta with garlic, olive oil, chili, and parsley.</p>

<div class="quick-facts">
  <span>Serves: 2 persons</span>
  <span>Prep: 10 minutes</span>
  <span>Cook: 12 minutes</span>
</div>

<section>
  <h2>Ingredients</h2>

  <ul class="ingredients compact">
    <li>200 grams spaghetti</li>
    <li>3 tablespoons olive oil</li>
    <li>3 cloves garlic (thinly sliced)</li>
    <li>0.5 teaspoon chili flakes <em>(optional)</em></li>
    <li>2 tablespoons parsley (finely chopped)</li>
    <li>Salt to taste</li>
  </ul>
</section>

<section>
  <h2>Steps</h2>

  <ol class="steps">
    <li>Bring a large pot of salted water to a boil.</li>
    <li>Cook spaghetti until al dente. Reserve pasta water, then drain.</li>
    <li>Warm olive oil in a skillet over low heat.</li>
  </ol>

  <button>Show remaining steps</button>
</section>
````

What the renderer decided (based on the Presentation Plan):

* Title → large heading
* QuickFacts → horizontal grouping
* Ingredients → compact list
* Steps → numbered list
* Only the first three steps visible initially

No CDX changed.
No data changed.
No view changed.
No design policy changed.

Only the **target-specific realization** changed.

---

## Example: Voice

Here is another rendering of the **same Presentation Plan**, this time for a voice interface.

This is spoken aloud to the user.

```plaintext
“Spaghetti Aglio e Olio.”

A quick pasta with garlic, olive oil, chili, and parsley.

This recipe serves two people.
Preparation time: ten minutes.
Cooking time: twelve minutes.

Ingredients:
Two hundred grams of spaghetti.
Three tablespoons of olive oil.
Three cloves of garlic, thinly sliced.
Half a teaspoon of chili flakes — optional.
Two tablespoons of finely chopped parsley.
Salt to taste.

Step one:
Bring a large pot of salted water to a boil.

Step two:
Cook the spaghetti until al dente. Reserve pasta water, then drain.

Step three:
Warm olive oil in a skillet over low heat.
```

What changed here:

* lists are read sequentially
* optional items are announced verbally
* only a small number of steps are read at once
* ordering and emphasis follow the same plan

What did **not** change:

* the data
* the view
* the design policy
* the presentation plan

---

## How to read this (non-technical)

Rendering is where the system finally “speaks.”

Everything you wrote earlier has already been understood and organized.
Rendering is just how that understanding is expressed in a particular medium.

This is why the same content can appear on a screen, on paper, or spoken aloud —
without rewriting anything.

---

## For technical readers

Renderers are:

* target-specific
* deterministic
* replaceable
* easy to test

They consume a fully resolved Presentation Plan and produce output.

Because all decisions are upstream:

* renderers contain no business logic
* no layout policy
* no inference
* no special cases

Rendering becomes a mechanical transformation.

---

## Why this matters

When rendering is boring:

* adding new targets is straightforward
* bugs are easier to localize
* presentation behavior is explainable
* the system scales across media

The next page steps back and shows the **entire pipeline at once** —
from authored meaning to rendered output.
