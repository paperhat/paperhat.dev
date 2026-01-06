# Putting it all together

At a high level, Paperhat follows a single, consistent idea:

> **Describe meaning, intent, and communication rules —  
> then let the system do the mechanics.**

Everything in the pipeline exists to support that idea.

---

## The full pipeline

From start to finish, the system moves through these stages:

```

Authored CDX
↓
AST
↓
IR
↓
RDF (semantic graph)
↓
View (CDX)
↓
ViewModel
↓
Design Policy (CDX)
↓
Presentation Plan
↓
Rendering (HTML / print / voice / etc.)

```

Each step has one responsibility.
No step tries to do another step’s job.

---

## Who does what

### Authors

- write **data CDX**
- write **view CDX**
- focus on meaning and structure
- never write queries, layout rules, or rendering code

---

### Designers

- write **Design Policy**
- encode communication principles
- decide hierarchy, grouping, emphasis, density, and adaptation
- do this once, reuse everywhere

---

### The system (the Scribe library + planners)

- parses and normalizes input
- stores semantic truth
- retrieves required facts
- builds ViewModels
- applies Design Policy
- produces Presentation Plans

All of this is deterministic and explainable.

---

### Renderers

- take a Presentation Plan
- produce concrete output for a target
- make no semantic or design decisions

Rendering is mechanical by design.

---

## What never changes

Across all targets:

- the **data** stays the same
- the **meaning** stays the same
- the **view definition** stays the same
- the **design policy** stays the same

Only the final realization changes.

---

## Why this matters

Because meaning, intent, and policy are explicit:

- content is written once
- presentation is consistent
- design decisions are visible
- behavior is predictable
- new targets stop being special cases

The system can explain itself.

---

## The quiet shift

This approach does not optimize for:
- quick hacks
- clever CSS
- one-off layouts

It optimizes for:
- clarity
- reuse
- longevity
- scale across media

Instead of tuning outputs,
the system **reasons about presentation**.

---

## The result

Authors write meaning.  
Designers write principles.  
The system plans.  
Renderers execute.

Everything else follows.
