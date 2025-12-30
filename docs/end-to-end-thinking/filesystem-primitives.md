# Filesystem primitives and generalization

_Surface the pedagogy_ is the missing half of most systems. Once you say it out loud, you can’t unsee how much damage “invisible teaching” does. We teach _as if_ structure is incidental, when it’s the actual lesson.

We'll tackle this in two passes:

1. **Filesystem primitives** — concrete, mechanical, boring (in the good way)
2. **Generalization** — how this becomes a universal content OS, not just “book sites”

---

## Part I — Filesystem primitives (structure you can’t lie to)

The filesystem is powerful because it:

- Forces explicit naming
- Makes absence visible
- Is hostile to ambiguity
- Is trivially diffable, cacheable, versionable

The trick is to **encode pedagogy in the directory layout**, not just content.

---

### 1. No “pages” directory. Ever.

Pages are a lie. They smuggle structure.

Instead, top-level primitives:

```
book/
  spine/
  concepts/
  examples/
  chapters/
  arguments/
```

Each directory corresponds to a _pedagogical role_, not a visual one.

---

### 2. The spine is first-class and mandatory

```
spine/
  01-learning-state.md
  02-learning-state.md
  03-learning-state.md
```

Each file contains:

- Learning outcomes
- Concepts required
- Capabilities gained

No spine → build fails.

This forces authors to think like teachers _before_ writers.

---

### 3. Concepts are atomic, named, and scarce

```
concepts/
  event-propagation.md
  stateless-rendering.md
```

Rules enforced by tooling:

- One file = one concept
- Filename = canonical term
- Word count enforced
- No code blocks allowed (that’s examples’ job)

A concept file is _definition, not discourse_.

This alone kills Wikipedia-style sprawl.

---

### 4. Examples are brutally constrained

```
examples/
  event-propagation/
    basic-loop.ts
    annotated.md
```

Rules:

- Exactly one concept per example directory
- Code + minimal explanation
- No abstraction language (“in general”, “typically”)

Examples are _evidence_, not teaching vehicles.

---

### 5. Chapters are assemblies, not writing spaces

```
chapters/
  01-reactive-loop/
    section-01.md
    section-02.md
```

Each section file:

- Declares:
  - Concepts used
  - Learning state advanced

- Cannot define new terms
- Must reference at least one example

Chapters are _compositions_ of prior work.

---

### 6. Arguments quarantined

```
arguments/
  why-not-mvc.md
```

Explicit metadata:

- Opinion
- Non-canonical
- Optional

Arguments cannot be prerequisites. They cannot block understanding.

This prevents ideology leakage into fundamentals.

---

### 7. Pedagogy is surfaced _in the files themselves_

Every file begins with something like:

```yaml
pedagogy:
  role: concept
  purpose: definition
  constraints:
    - no procedures
    - no opinions
```

Learners see this.

Authors can’t pretend they’re “just writing.”

---

## Part II — Generalization: from book to _sensemaking engine_

Here’s the key insight:

> **Books, courses, docs, magazines, and reference manuals are not different things.**
>
> They are different _projections_ of the same underlying structure.

Once content is typed and linked, the “site type” becomes a _view_.

---

## 1. The universal primitives (reduced)

Across all formats, you only need:

- **Concept** — definition
- **Procedure** — steps
- **Example** — concrete instance
- **Claim** — opinion
- **Question** — uncertainty
- **State** — learner capability

Everything else is composition.

---

## 2. Different products = different constraints

### Book

- Linear spine
- Hard prerequisites
- Strong closure

### Course

- Time-based pacing
- Assessments tied to states
- Exercises derived from procedures

### Reference manual

- No spine
- Concepts only
- Zero pedagogy narrative

### Magazine

- Weak spine
- High argument density
- Concepts assumed, not taught

Same content. Different rule sets.

---

## 3. “Surface the pedagogy” as a UI principle

Every rendered page shows:

- What kind of thing this is
- Why it exists
- How to read it
- What it assumes
- What it enables next

This teaches _how to learn_, not just content.

---

## 4. Why AI finally makes sense here

AI is bad at creation.
AI is good at **rule enforcement and critique**.

Given this structure, AI can:

- Explain _why_ a constraint exists
- Reflect pedagogy back to the learner
- Say:

  > “You are encountering this concept earlier than most learners struggle with it.”

AI becomes a _teaching assistant_, not an author.

---

## 5. The philosophical through-line

What you’re really building is not a site builder.

It’s a system that enforces this truth:

> **Meaning precedes expression.
> Structure precedes content.
> Pedagogy precedes prose.**

Wikipedia pretends none of that is true.
MDN half-admits it.
Most tools actively obscure it.

You’re proposing a system that refuses to lie.

---

## 6. Where this gets dangerous (in a good way)

This kind of system:

- Makes power visible
- Makes assumptions explicit
- Makes ideology locatable
- Makes disagreement _structural_, not rhetorical

Which is why it will feel “hostile,” “elitist,” or “opinionated.”

That’s fine. Editors are opinionated. Teachers must be.
