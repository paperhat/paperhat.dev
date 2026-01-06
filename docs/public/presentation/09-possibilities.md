# What this makes possible

If we step back, something unusual has happened.

We have separated three things that are usually tangled together:

- **what something *is***  
- **what someone wants to *show***  
- **how it should be *communicated***  

…and we have made each of them explicit, declarative, and independent.

---

## The traditional web stack

Most web systems collapse these concerns:

- HTML mixes meaning with presentation structure
- CSS mixes design principles with layout mechanics
- JavaScript mixes behavior intent with wiring and state management

As a result:
- content is rewritten to fit layouts
- layouts are rewritten to fit screens
- behavior is tightly coupled to components
- changing one concern often breaks the others

Responsiveness, accessibility, and consistency become *ongoing battles*.

---

## The Paperhat pipeline

Paperhat takes a different approach.

Each concern lives at its own level:

- **CDX (data)** describes *what exists and is true*
- **CDX (views)** describes *what should be presented*
- **Design Policy** describes *how information should be communicated*
- **Presentation Plans** are generated for specific targets
- **Rendering** is mechanical and replaceable

No single layer needs to know about the others’ implementation details.

---

## A useful way to think about it

HTML, CSS, and JavaScript still exist.

But they are no longer the **authoring languages**.

They become **output formats**.

In the same way that:
- people do not write assembly,
- but computers still run it,

authors and designers no longer write:
- HTML to express meaning,
- CSS to encode design philosophy,
- JavaScript to wire behavior imperatively.

Those concerns are expressed declaratively —
and compiled.

---

## What changes for authors

Authors:
- write content once
- describe meaning, not layout
- never touch queries, layout code, or rendering logic

The same content can:
- appear as a web page,
- be printed,
- be read aloud,
- be reused in other contexts,

without being rewritten.

---

## What changes for designers

Designers:
- write communication rules, not CSS tricks
- encode hierarchy, grouping, emphasis, and density
- define how content adapts to different media

They do this once —
and the system applies it consistently.

Design decisions stop being scattered across files and breakpoints.
They become explicit and reviewable.

---

## What changes for developers

Developers:
- stop hand-wiring presentation logic
- stop duplicating layout behavior
- stop rebuilding the same responsiveness rules

They work on:
- compilers,
- planners,
- renderers,
- and behavior systems,

with clear contracts between them.

---

## The quiet consequence

When meaning, presentation intent, and communication policy are all explicit:

- presentation becomes predictable
- changes become localized
- explanations become possible
- new targets stop being special cases

The system is no longer *tuned*.
It is *reasoned about*.

---

## Where this leads

This approach does not optimize for:
- short-term convenience,
- quick demos,
- or familiar patterns.

It optimizes for:
- reuse,
- clarity,
- longevity,
- and scale across media.

Everything that follows — rendering, interaction, behavior —
is built on that foundation.
