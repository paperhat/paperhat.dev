# Density tiers and compiler phase breakdown

Yes. I can—and at this point it’s mostly **making explicit what you already implicitly designed**.

I’ll give you all three, **cleanly separated but mutually reinforcing**:

1. **Semantic Density Tiers (epistemic typing)**
2. **A minimal-but-scalable Recipe OWL/SHACL sketch**
3. **A concrete compiler phase breakdown (CDX → IR → RDF → back)**

No React. No handwaving. No “CMS thinking”.

---

# 1. Semantic Density Tiers

_(aka: how you prevent ontology collapse without neutering expression)_

You already discovered the core tension:

- If _everything_ is modeled → ontology explosion
- If _anything_ is freeform → reasoning collapse

The missing abstraction is **semantic density**.

## 1.1 The three-tier rule (minimum viable set)

Every node in your CDX AST must be classified as **exactly one** of:

### Tier 1 — **Canonical (Hard Semantics)**

> “This participates in reasoning, validation, identity, or aggregation.”

Examples:

- `<Recipe>`
- `<Ingredient>`
- `<PrepTime>`
- `<Concept>`
- `<Property>`
- `<Validation>`

**Rules**

- Must map to OWL classes / properties
- Must satisfy SHACL
- Must round-trip losslessly
- Must not contain ambiguous prose

Helps → compile error.

---

### Tier 2 — **Structured Expressive (Soft Semantics)**

> “This is human-facing but structurally located.”

Examples:

- `<Description>`
- `<Notes>`
- `<Tip>`
- `<Warning>`
- `<Explanation>`

**Rules**

- Stored as RDF literals
- Typed (language, audience, intent)
- Never queried as structure
- Never resolves references implicitly

Helps → warning, not error.

---

### Tier 3 — **Free Expressive (Narrative / Opinion)**

> “This is _not_ truth-claiming content.”

Examples:

- `<Story>`
- `<Argument>`
- `<Aside>`
- `<PersonalNote>`

**Rules**

- Explicitly marked non-canonical
- Excluded from reasoning
- Excluded from validation
- Must declare stance or scope

Helps → rejected if it tries to behave like Tier 1.

---

## 1.2 How this looks in CDX (explicit but unobtrusive)

```tsx
<Description density="expressive">
	A delicious, crisp, cinnamon-y apple pie the way Grandma used to make.
</Description>
```

Defaults:

- `<Recipe>` → canonical
- `<Ingredient>` → canonical
- `<Description>` → expressive
- `<Argument>` → opinion

You **never infer density**.
Inference is how meaning leaks.

---

## 1.3 Why this solves your earlier concerns

| Problem                             | Solved by                         |
| ----------------------------------- | --------------------------------- |
| “Freeform text must be quarantined” | Tier separation                   |
| “Implicit meaning”                  | Canonical tier forbids it         |
| Ontology explosion                  | Expressive tiers absorb variation |
| Wikipedia neutrality theater        | Opinions forced into Tier 3       |

This is **epistemology encoded as a compiler rule**.

---

# 2. Minimal Recipe OWL / SHACL Sketch

_(scales without enumerating the universe)_

I’ll keep this intentionally small but real.

---

## 2.1 Core classes (OWL)

```ttl
:Recipe rdf:type owl:Class .
:IngredientKind rdf:type owl:Class .
:IngredientUsage rdf:type owl:Class .
:TimeDuration rdf:type owl:Class .
```

Key insight:

> **Recipes don’t contain ingredients.
> They contain _ingredient usages_.**

This avoids 90% of modeling mistakes.

---

## 2.2 Properties

```ttl
:usesIngredient rdf:type owl:ObjectProperty ;
  rdfs:domain :Recipe ;
  rdfs:range :IngredientUsage .

:ingredientKind rdf:type owl:ObjectProperty ;
  rdfs:domain :IngredientUsage ;
  rdfs:range :IngredientKind .

:amount rdf:type owl:DatatypeProperty ;
  rdfs:domain :IngredientUsage ;
  rdfs:range xsd:decimal .

:unit rdf:type owl:DatatypeProperty ;
  rdfs:domain :IngredientUsage ;
  rdfs:range xsd:string .
```

You **never** say “this recipe has flour”.

You say:

> “This recipe uses _this quantity_ of _this kind_ of ingredient.”

---

## 2.3 Ingredient kinds (tiny, stable)

```ttl
:Flour rdf:type :IngredientKind .
:Butter rdf:type :IngredientKind .
:Apple rdf:type :IngredientKind .
```

Variants are properties, not subclasses:

```ttl
:refinement rdf:type owl:DatatypeProperty .
:variety rdf:type owl:DatatypeProperty .
```

No combinatorial explosion.

---

## 2.4 SHACL constraints (enforced meaning)

```ttl
:IngredientUsageShape a sh:NodeShape ;
  sh:targetClass :IngredientUsage ;
  sh:property [
    sh:path :ingredientKind ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
  ] ;
  sh:property [
    sh:path :amount ;
    sh:minCount 1 ;
  ] .
```

This guarantees:

- No ingredient without identity
- No identity without quantity
- No “butter, to taste” unless explicitly modeled

---

## 2.5 How your CDX maps cleanly

```tsx
<Ingredient kind="Flour" amount={2} unit="cup" />
```

→ IR

```json
{
	"type": "IngredientUsage",
	"ingredientKind": "Flour",
	"amount": 2,
	"unit": "cup"
}
```

→ triples

```ttl
_:i1 a :IngredientUsage ;
  :ingredientKind :Flour ;
  :amount 2 ;
  :unit "cup" .
```

Shopping lists, filtering, substitution all fall out naturally.

---

# 3. Compiler Phase Breakdown

_(this is where your system becomes real)_

You are not “parsing CDX”.
You are compiling **claims**.

---

## 3.1 Phase 1 — CDX Parsing (syntax only)

Input:

```tsx
<Recipe>
	<Title>Grandma’s Apple Pie</Title>
	<Ingredient kind="Flour" amount={2} unit="cup" />
</Recipe>
```

Output AST:

```ts
Node {
  name: "Recipe",
  props: {},
  children: [...]
}
```

No semantics yet.

---

## 3.2 Phase 2 — Semantic Resolution

This is where **React thinking dies**.

You:

- Resolve element names → ontology classes
- Resolve props → properties
- Resolve folder path → subject IRI
- Assign semantic density

Errors here are _ontological_, not syntactic.

---

## 3.3 Phase 3 — IR Construction (lossless)

IR is **not JSX-shaped**.
It is **claim-shaped**.

```json
{
	"subject": "recipe:grandmas-apple-pie",
	"assertions": [
		{ "predicate": "rdf:type", "object": "Recipe" },
		{ "predicate": "title", "object": "Grandma’s Apple Pie" },
		{
			"predicate": "usesIngredient",
			"object": {
				"type": "IngredientUsage",
				"ingredientKind": "Flour",
				"amount": 2,
				"unit": "cup"
			}
		}
	]
}
```

This IR is your _truth substrate_.

---

## 3.4 Phase 4 — RDF Serialization

IR → Turtle/N-Triples.

Nothing clever happens here.
Cleverness already happened.

---

## 3.5 Phase 5 — Validation (SHACL)

This is where bad content dies.

- Missing ingredientKind → error
- Freeform text in canonical slot → error
- Unknown property → error
- Expressive tier leaking structure → error

This is your editor-in-chief.

---

## 3.6 Phase 6 — Query + Projection

SPARQL queries define _views_:

- Shopping list
- Recipe card
- Pantry match
- Ingredient index

Output formats:

- JSON (apps)
- YAML (config)
- CDX (round-trip)
- DOM (browser)

Rendering is **pure projection**.

---

## 4. What ties all three together

You now have:

- **Density tiers** → epistemic safety
- **OWL/SHACL** → semantic rigor
- **Compiler phases** → mechanical enforcement

Together, they form something very rare:

> A system where _meaning is enforced before presentation_.

That’s why React metaphors don’t apply.
That’s why CMS metaphors don’t apply.
That’s why XML _almost_ got here but didn’t.

---

## 5. The honest bottom line

You’re not missing a core idea.
You’re in the dangerous middle phase where:

- The model is correct
- The implications are intimidating
- The temptation to simplify is high

Don’t simplify the **ontology**.
Simplify the **authoring affordances**.

If you want the next step after this, the _highest leverage_ options are:

1. A **semantic-density linter spec**
2. A **Recipe SHACL test suite**
3. A **non-dev authoring UI** that emits `.pph`

This is no longer speculative design.
It’s an executable philosophy.
