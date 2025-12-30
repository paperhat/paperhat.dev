# UI affordances

# 1. UI affordances that sit on top of the protocol

This is **not** “design” in the Dribbble sense. These are **semantic affordances**: what actions are even _possible_ in the system.

The rule of thumb you’re already following (implicitly):

> **Every UI action corresponds to a typed operation in the ontology.**
> No freeform mutation. No invisible effects.

## 1.1 Canonical object states

Every semantic object (Recipe, IngredientUsage, Concept, etc.) is always in **one of these states**:

- **Draft** – editable, private or shared
- **Published** – immutable
- **Forked** – derived from a published object
- **Annotated** – commented on, but unchanged
- **Deprecated** (optional later)

This matters because UI affordances are _state-dependent_.

---

## 1.2 Core affordances (non-negotiable)

These appear everywhere, consistently.

### 🔍 Read

- Default mode
- Zero affordances for mutation
- Shows:
  - lineage
  - forks
  - annotations
  - ontology-backed metadata

> Read is the _safe_ mode.

---

### ✏️ Edit (Draft only)

Appears **only** when:

- object is Draft
- user has permission

**Affordances**

- Structured editors (ingredient picker, quantity widget)
- Validation feedback (SHACL errors inline)
- No “Save” vs “Publish” ambiguity

> Edit does not exist for Published objects.

---

### 🚀 Publish

Single, explicit act.

UI characteristics:

- One-way
- Requires passing validation
- Shows:
  - “This will become immutable”
  - “Future changes require a fork”

> This is the editorial equivalent of “commit”.

---

### 🪓 Fork

Appears **only** on Published objects.

UI copy must be explicit:

> “Create a new version based on this”

Affordances:

- Pre-populated content
- Clear lineage indicator
- Optional fork rationale (quarantined text)

> Fork is _not_ edit. Ever.

---

### 💬 Annotate

Always available.

Annotation types (radio buttons, not free text):

- Question
- Suggestion
- Correction
- Context / Story

Text is allowed **only after** type selection.

> This is where “opinions” go.

---

## 1.3 Progress & confidence indicators

These are subtle but critical.

### Validation status

- ✅ Valid
- ⚠️ Valid with warnings
- ❌ Invalid (draft-only)

This maps **directly** to SHACL results.

---

### Semantic completeness

For Recipes, for example:

- Ingredients defined: ✔️
- Servings defined: ✔️
- Quantities scalable: ⚠️ (freeform unit somewhere)

This is not correctness—it’s **machine usability**.

---

### Lineage indicator

Always visible:

> “Forked from Grandmother’s Apple Pie”

Clickable, graphable, inspectable.

---

## 1.4 What is _not_ an affordance (by design)

Deliberately absent:

- “Edit published content”
- “Resolve conflict”
- “Merge”
- “Neutralize”
- “Auto-fix disagreements”

Those are **Wikipedia pathologies**.

---

# 2. Ingredient identity strategy (formal, scalable)

This is the other keystone. You’re right: naïvely modeling ingredients explodes combinatorially.

So we don’t.

We use **a 3-layer identity stack**.

---

## 2.1 Layer 1: Lexical (what the human types)

This is what appears in TSX:

```tsx
<Ingredient amount="1" unit="cup">
	flour
</Ingredient>
```

Properties:

- Raw string
- Language-tagged
- Authorial intent
- Zero reasoning power

Stored as:

```
lexicalLabel = "flour"
```

This layer is **never deleted**.

---

## 2.2 Layer 2: Canonical ingredient concept

This is where identity stabilizes.

Example:

```
IngredientConcept: WheatFlour
  broader: Flour
  derivedFrom: Wheat
```

Mapping:

- lexical → canonical is **many-to-one**
- done by:
  - author choice
  - AI suggestion
  - later editorial curation

Crucially:

> Lexical text does NOT become canonical automatically.

The UI affordance here is:

> “This looks like _Wheat Flour_. Is that correct?”

---

## 2.3 Layer 3: Nutritional / functional reasoning

This layer is **orthogonal** to culinary naming.

Example:

```
WheatFlour
  macronutrients:
    carbohydrates
    protein
  allergens:
    gluten
  functionalRoles:
    structure
    thickening
```

This is where:

- grocery lists
- dietary filters
- substitutions
- scaling
- allergen warnings

come from.

---

## 2.4 Why this avoids ontology explosion

You do **not** define:

- 100 flours up front
- every regional synonym
- every brand

Instead:

- Lexical layer absorbs mess
- Canonical layer grows _slowly_
- Nutritional layer is reused

You only mint a new canonical concept when:

- reasoning differs
- substitutions differ
- nutrition differs
- constraints differ

Otherwise:

> It’s just another label pointing to the same thing.

---

## 2.5 UI affordances for ingredient identity

Non-dev friendly, but precise:

- Ingredient chip shows:
  - Label: “flour”
  - Canonical: Wheat Flour
  - Confidence indicator

- Click → “Clarify ingredient”
  - Pick existing concept
  - Or leave unresolved

Unresolved is allowed.
It just limits reasoning.

---

# 3. Why these two foundations matter

Once these are locked:

- Recipes become _computable_
- Non-devs can safely contribute
- AI can assist without hallucinating authority
- Disagreement remains structural
- Ontologies grow organically, not explosively

Most importantly:

> **Nothing forces premature formalization.**
> But formalization is always possible later.

That’s the balance almost every system gets wrong.
