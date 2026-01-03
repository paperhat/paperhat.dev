# Planning issues

One of the biggest problems with making web site/application development possible for the average person has nothing to do with the code. It's the content.

Hiding the code is not difficult, and many sites have done so. Many have visual tools for building pages or sites. But this does not address the main problem facing most users. That problem is this: they are not good at organizing their thoughts, creating taxonomies (information architectures), creating content, etc.

Even if someone is a good writer, they need a good editor, and the two skills are rarely found in the same person. And if a person is a good editor, that does not mean they are a good writer. And good technical writers, curricula developers, and teachers are hard to find.

So creating a tool that makes it easy to build, for example, a "book site" or a "magazine site" solves only the smallest part of the problem. The real problem is getting the user to both create sufficient (and sufficient quality) content, and to **organize** that content in a comprehensible and **searchable/browsable** way.

AIs may assist, but most AIs are not very good at this either.

So the question is — the billion dollar question — how can we make it easy for the user, with or without AI assistance, to both create content and to organize it into a reasonably good architecture? There is a similar issue with design and layout, but there are plenty of design systems/templates that can help with this. For content, not so much.

## An Editorial Operating System

The bottleneck is **sense-making**: deciding _what belongs_, _where it goes_, _how it connects_, and _when it’s good enough_. That’s an editor’s job, an information architect’s job, and often a teacher’s job — not a developer’s.

The solution is almost certainly **not one thing**, but a stack of constraints, workflows, and **affordances** that _force_ coherence to emerge.

---

## 1. Reframe the problem: people don’t fail at writing, they fail at _editorial closure_

Most tools assume:

> “If we help you write, organization will follow.”

In reality, people fail because they:

- Don’t know **what the finished shape should be**
- Don’t know **when something is done**
- Don’t know **what level of detail belongs where**
- Don’t know **how to revise without destroying motivation**

Editors solve this by:

- Enforcing structure _before_ content
- Forcing tradeoffs
- Saying “no” more than “write more”

So the tool must behave less like a word processor and more like an **opinionated editor-in-chief**.

---

## 2. The core idea: _progressive commitment under constraint_

The single most important design principle:

> **Users should never face an unstructured blank space.**

Instead:

- They make _small, reversible commitments_
- The system hardens those commitments over time
- Structure emerges _before_ prose

Think: **taxonomies first, sentences last**

---

## 3. Architecture-first authoring (without calling it IA)

Most users shut down when you say “information architecture.”
But they _can_ answer questions like:

- “What kind of thing is this?”
- “Who is this for?”
- “What problem does this solve?”
- “What should someone be able to do after reading this?”

### Replace freeform pages with _content types that encode intent_

Not “pages,” but **editorial primitives**, for example:

- Concept
- How-to
- Reference
- Argument
- Story
- FAQ
- Example
- Glossary entry

Each type:

- Has **required fields**
- Has **size limits**
- Has **expected relationships**
- Has **automatic placement rules**

> A Concept _must_ explain a term and link to at least one How-to.
> A How-to _must_ reference exactly one Concept it teaches.
> A Reference cannot contain narrative prose.

This is how good documentation systems work internally—but exposed gently.

---

## 4. Organization by _forced relationships_, not folders

Folders are a lie. They postpone thinking.

Instead, require **explicit semantic links**:

- “Explains”
- “Depends on”
- “Expands”
- “Contrasts with”
- “Prerequisite for”

The UI should _not_ allow content to exist unlinked.

> If something cannot be connected, it cannot be saved.

Navigation, browsing, and search are then **derived**, not authored.

This turns IA from:

> “Where should this go?”

into:

> “What is this _in relation to_ other things?”

Which humans are much better at answering.

---

## 5. Bounded writing: length limits as editorial discipline

One of the biggest helpss of amateur content is _overwriting_.

Editors impose:

- Word limits
- Section caps
- Progressive disclosure

Your tool should enforce things like:

- Concepts: 150–300 words
- How-tos: 5–9 steps max
- Arguments: claim → evidence → counterpoint → resolution
- Examples: code + explanation only

You don’t _suggest_ limits.
You **hard-stop**.

This alone massively improves clarity.

---

## 6. AI’s real role: adversarial editor, not ghostwriter

You’re right: AI is bad at _creating good IA_ if asked to “organize this.”
But it’s excellent at **critique under constraints**.

The AI should:

- Reject vague titles
- Flag duplicate concepts
- Detect scope creep
- Identify missing prerequisites
- Ask annoying editor questions

Examples:

> “You’ve introduced a new term here. Should it be a Concept?”
>
> “This How-to references three Concepts. Pick one or split it.”
>
> “This page is doing two jobs. Which one matters more?”

AI as **hostile but fair editor**, not co-author.

---

## 7. Scaffolded growth: start with a _minimum viable canon_

Instead of:

> “Build your site.”

Start with:

> “Create **five** things.”

Hard limit:

- 5 Concepts
- 5 How-tos
- 10 total items

Only after those exist can new ones be added.

This mirrors:

- Books (outline first)
- Courses (learning objectives first)
- Encyclopedias (seed articles)

Abundance is the enemy of coherence.

---

## 8. Searchability via _semantic guarantees_

Search sucks when content is sloppy.

But if:

- Every item has a type
- Every term has a definition
- Every relationship is explicit
- Every page has an audience and intent

Then search becomes trivial:

- Filter by type
- Traverse graph edges
- Rank by conceptual centrality

Browsing becomes:

- “Show me prerequisites”
- “Show me advanced topics”
- “Show me unresolved concepts”

No tagging UI required.

---

## 9. Editorial states: draft → review → canon

Most amateur content never improves because it’s all “published.”

Introduce states:

- Draft (private, messy)
- Review (AI + rules enforced)
- Canon (frozen, linkable)

Canon content:

- Cannot change arbitrarily
- Requires justification to revise
- Preserves stable URLs

This creates **psychological weight**, which improves quality.

---

## 10. The uncomfortable truth (and opportunity)

Here’s the part most tools avoid:

> **You cannot make everyone good at content creation.**

But you _can_:

- Prevent them from making incoherent messes
- Make bad structure impossible
- Make “good enough” the default outcome

The billion-dollar insight is not:

> “Empower creativity”

It’s:

> **“Constrain chaos until meaning emerges.”**

---

## 11. If I had to name the product philosophy

Not:

- Website builder
- CMS
- No-code tool
- AI writer

But:

> **Editorial Operating System**

Where:

- Content is data with intent
- Structure precedes expression
- Organization is unavoidable
- AI enforces standards, not vibes
