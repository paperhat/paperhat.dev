## How Semantic Display Roles are assigned

You want **power without author pain** and **escape hatches without chaos**.
That means **three assignment paths**, with strict precedence.

---

## 1. Implicit by structural kind (default, zero effort)

Some meanings are obvious and should require **no author action**.

Examples:

* `Step` → `procedural-step`
* `Warning` / `Constraint` → `constraint`
* `Footnote`, `Citation` → `reference-metadata`
* `Figure` marked decorative → `decorative`

**Rules**

* Defined centrally (ontology-level)
* Stable
* Overrideable, but not silently

This covers 60–70% of cases automatically.

---

## 2. Explicit in the View (authorial intent)

When the author *means* something specific.

Examples:

* “This Section is auxiliary, even though it’s long”
* “This block is a CTA”
* “This sidebar is promotional”

This belongs in **View**, because it is **intent**, not adaptation.

**Rules**

* Views may assign a Semantic Display Role explicitly
* This overrides implicit-by-kind
* Views may NOT assign multiple roles to the same node

This is where meaning is *declared*, not guessed.

---

## 3. Derived or substituted by Adaptive Layout Strategy (exceptional)

Only when structure is **derived**, not authored.

Examples:

* A collapsed summary → `auxiliary-content`
* A generated “Read more” link → `call-to-action`
* Paginated overflow → `reference-metadata`

**Rules**

* Strategy may assign roles **only to derived nodes**
* Strategy MUST NOT change the role of an authored node
* Derived roles MUST be explicit and marked as such

This prevents strategy from rewriting meaning.

---

## Precedence (lock this)

```
Derived (strategy, derived nodes only)
> Explicit (View)
> Implicit (by kind)
```

No ambiguity. No guessing.

---

## What this gives you immediately

* Authors express **meaning**, not layout
* Designers get **semantic leverage**
* Strategy operates on **roles, not guesses**
* Runtime has a clean contract
* Copilot has nowhere to get confused

---

## One-sentence lock (important)

> **Semantic Display Roles classify the communicative function of content and are assigned implicitly by structure, explicitly by Views, or derivatively by Adaptive Layout Strategy—never by renderers.**

If you agree, the *next* step is obvious and small:

➡️ **Write the Semantic Display Role Specification (v0.1)**
(very short, mostly rules and tables)

Say the word again when ready.
