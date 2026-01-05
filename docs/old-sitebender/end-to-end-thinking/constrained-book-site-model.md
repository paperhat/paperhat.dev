# A Constrained "Book Site" Model

A **book site** that is _editorially constrained by design_. Not a CMS, not pages, not chapters in the usual sense. Think of it as a system that _forces a book to behave like a book_, even when written by someone who has never edited anything.

---

# A Constrained “Book Site” Model

## 1. What this _is_ and _is not_

**It is:**

- A finite, opinionated knowledge artifact
- With a spine, prerequisites, and closure
- Designed to be _read end-to-end_ but also _navigable_

**It is not:**

- A wiki
- A blog
- A document dump
- A tree of folders

No infinite growth. No “just add another page.”

---

## 2. The canonical object model (hard limits)

A book consists of **exactly four content primitives**:

### 1. Concept

> “What is this thing?”

- 150–300 words
- Defines one term
- No procedures
- No history
- No opinions
- Must link to:
  - ≥1 Example
  - ≥1 Chapter section that uses it

If it can’t be defined cleanly, it doesn’t exist yet.

---

### 2. Example

> “What does this look like in reality?”

- Concrete
- Minimal explanation
- No abstraction
- No generalization
- Must reference exactly **one** Concept

Examples prevent hand-wavy theory.

---

### 3. Chapter Section

> “What do I do with these ideas?”

- 5–9 sections per chapter
- Each section:
  - Uses 1–3 Concepts
  - Solves exactly one problem

- No new Concepts allowed here

This forces Concept creation _before_ instruction.

---

### 4. Argument (optional, capped)

> “Why this approach?”

- Max 5 total in the entire book
- Explicitly marked as opinion
- Cannot introduce Concepts
- Cannot be prerequisite for anything

Arguments are quarantined so they don’t poison the core.

---

## 3. The book spine (this is the key)

Before _any content_ is written, the author must create:

### The Spine

A linear list of **Learning States**:

> After Chapter 1, the reader can…
> After Chapter 2, the reader can…

Each state:

- Is testable
- Is cumulative
- References Concepts by name

Example:

```
State 3:
The reader can explain:
- Event propagation
- Stateless rendering

And can implement:
- A minimal reactive loop
```

No state → no chapter.

This alone eliminates 80% of bad books.

---

## 4. Chapter construction is backward

You do **not** write chapters directly.

You must:

1. Define a Learning State
2. Identify Concepts needed
3. Write Concepts
4. Write Examples
5. Assemble Chapter Sections from those

The UI literally prevents skipping steps.

---

## 5. Navigation emerges, not authored

The book site automatically generates:

### Linear reading

- Canonical chapter order
- No branching

### Concept index

- Alphabetical
- With usage heatmap (where concepts are used most)

### Dependency graph

- “You are here”
- What you already know
- What this depends on

### Example gallery

- Browse-only
- No reading order

### Prerequisite warnings

> “This section assumes knowledge of X and Y.”

No hand-written TOC pages.

---

## 6. Search works because content is typed

Search is not full-text first.

Primary filters:

- Concepts
- Chapters
- Examples
- Arguments

Secondary:

- Used in Chapter N
- Introduced before/after X
- Central vs peripheral

This avoids Wikipedia’s “keyword soup.”

---

## 7. Editorial enforcement (this is where Wikipedia fails)

The system **rejects** content when:

- A Concept exceeds its word cap
- A Chapter Section introduces a new term
- A Concept is never used
- Two Concepts overlap semantically
- An Example references multiple Concepts
- A Chapter has more than 9 sections

Rejection, not suggestion.

---

## 8. AI’s role (precise and limited)

AI is allowed to:

- Detect concept leakage
- Propose splits or merges
- Flag circular dependencies
- Identify missing examples
- Ask:

  > “What misconception does this address?”

AI is **not allowed** to:

- Invent structure
- Rewrite prose unless asked
- Add content without a slot

---

## 9. What the reader experiences

The reader sees:

- A clear progression
- Stable definitions
- No sudden abstraction jumps
- Examples exactly when needed
- Opinions clearly marked and rare

They _feel_ like:

> “Someone actually thought this through.”

---

## 10. Why this avoids Wikipedia and MDN helps modes

### Wikipedia problems

- No closure
- Infinite scope
- No pedagogical spine
- Neutrality destroys narrative

### MDN problems

- Hybrid reference/tutorial confusion
- Concepts buried in guides
- Examples too large or too small
- Inconsistent depth

This model:

- Separates **what**, **how**, and **why**
- Forces order
- Caps growth
- Makes pedagogy explicit

---

## 11. The uncomfortable but important conclusion

This system will:

- Reject a lot of user input
- Feel “hostile” at first
- Slow authors down

But the output will be:

- Coherent
- Navigable
- Searchable
- Actually readable

Which is the entire point.
