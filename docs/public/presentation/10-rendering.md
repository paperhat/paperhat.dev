# Rendering

Rendering is the process of taking a ViewModel and transforming it into a specific output format, such as HTML for web pages, PDF for print, or audio for voice interfaces.

Here are two different target-specific renderings of the same ViewModel:

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

```

What the renderer decides (examples):

- Title = large heading
- QuickFacts = horizontal row
- Ingredients = compact bullet list
- Steps = numbered list
- First 3 steps visible, rest behind “Show more”

No CDX changed.  
No data changed.  
Only the renderer’s interpretation changed.

Here is another rendering of the same ViewModel, this time for a voice interface. This is spoken aloud to the user:

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
Cook the spaghetti until al dente…
``
```
