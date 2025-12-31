# Recipe UI design sketch

A **minimal UI sketch**. That means:

- concrete screens
- concrete widgets
- concrete affordances
- **no React assumptions**
- no “designer fluff”
- no ontology leakage into the UI

I’ll give you the **smallest UI surface that makes the system usable**, nothing more.

---

# Minimal UI for Sitebender Codex (Recipes)

This is not a CMS.
This is a **value editor + value browser**.

---

## 0. Global invariants (UI rules)

These are enforced everywhere:

1. **Read is default**
2. **Edit is explicit**
3. **Publish is irreversible**
4. **Fork instead of mutate**
5. **Validation is visible**
6. **Ontology errors block publishing**

If a UI violates one of these, it is wrong.

---

## 1. App layout (one screen model)

No dashboards. No sidebars full of noise.

```
┌──────────────────────────────────────────┐
│ Sitebender Codex                         │
│ Recipes / Grandmother's Apple Pie        │
├──────────────────────────────────────────┤
│ [Read] [Edit] [Fork] [Annotate]          │
│ Status: Published ✓   Version: v1        │
├──────────────────────────────────────────┤
│                                          │
│              CONTENT AREA                │
│                                          │
├──────────────────────────────────────────┤
│ Lineage | Ingredients | Annotations      │
└──────────────────────────────────────────┘
```

Tabs are **projections**, not modes.

---

## 2. Read View (default)

This is what **everyone** sees.

### Title & metadata

```
Grandmother's Apple Pie
6 servings
Prep: 30 min   Cook: 45 min
```

### Ingredients

Each ingredient is a **chip with state**:

```
• 2 cups flour     ⚠ unresolved
• 1 cup butter     ✓ Wheat Butter
• 6 apples         ✓ Apple (generic)
```

Hover tooltip:

- lexical label
- canonical mapping (if any)
- confidence

---

### Instructions

Plain numbered list.
No interactivity. No parsing.

---

### Bottom affordances

```
[ Scale servings ]   [ Make shopping list ]
```

Clicking **never mutates** the recipe.

---

## 3. Edit View (draft only)

Only visible if:

- recipe is Draft
- user has permission

### Edit is **structured**, not freeform

#### Ingredients editor

Each row:

```
[ 2.00 ] [ cup ▼ ] [ flour __________ ]  [ ⚠ clarify ]
```

Clarify opens:

```
Did you mean:
○ Wheat flour
○ All-purpose flour
○ Leave unresolved
```

No autocomplete that invents ontology.

---

#### Servings editor

```
Servings: [ 6 ] [ servings ▼ ]
```

This field is **required**.
UI does not allow empty.

---

#### Validation panel (always visible)

```
Validation
✓ Servings defined
✓ Ingredients quantified
⚠ Ingredient "flour" unresolved
✗ Instruction references temperature not modeled
```

Publish button is disabled until ❌ is gone.

---

## 4. Publish affordance (critical)

This is a **modal**, not a button.

```
Publish Recipe?

• This recipe will become immutable
• Future changes require a fork
• Annotations remain possible

[ Cancel ]   [ Publish ]
```

No auto-publish. Ever.

---

## 5. Fork UI (one click, explicit)

From Read view:

```
[ Fork Recipe ]
```

Dialog:

```
Create a fork of:
Grandmother's Apple Pie (v1)

Reason (optional):
[ __________________________ ]

[ Cancel ]   [ Create Fork ]
```

Result:

- new Draft
- lineage shown immediately

---

## 6. Annotation UI (controlled discourse)

No comment box until type is selected.

```
Add Annotation

Type:
○ Question
○ Suggestion
○ Correction
○ Context

[ Text area appears after selection ]
```

Annotations never alter the recipe.

---

## 7. Grocery List UI (pure projection)

Triggered by:

```
[ Make shopping list ]
```

Dialog:

```
For how many servings?
[ 12 ]

[ Generate ]
```

Result:

```
Shopping List
• Flour — 4 cups
• Butter — 2 cups
• Apples — 12
• Sugar — 1.5 cups
```

Options:

- export
- print
- save as list

No write-back.

---

## 8. Ingredient clarification UI (the subtle killer feature)

Accessible from:

- ingredient chip
- validation warning
- AI suggestion (later)

Always shows:

```
Original text: "flour"
Current mapping: none

Select canonical ingredient:
[ searchable list ]

Or:
[ Leave unresolved ]
```

No silent changes.

---

## 9. What is deliberately missing

On purpose:

- WYSIWYG
- drag-and-drop
- live preview while typing
- auto-fix buttons
- merge tools
- ratings
- likes
- “neutrality” controls

Those come _later_, if ever.

---

## 10. Why this UI is minimal but sufficient

Because:

- every button maps to a semantic operation
- every state transition is explicit
- nothing relies on hidden inference
- non-devs can reason about consequences

This is the **smallest surface** that preserves:

- FP properties
- ontology integrity
- social coherence
- future extensibility

---

## About your code concern (briefly, honestly)

You’re right to be cautious.

What we’ve done so far is:

- specify invariants
- specify data shapes
- specify state transitions
- specify UI affordances

That is the **correct order** if you don’t want to paint yourself into a corner.
