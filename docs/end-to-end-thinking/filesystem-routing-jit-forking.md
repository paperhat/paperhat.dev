# Filesystem routing, JIT, and forking without collapsing coherence

**Three passes that interlock**:

1. **Map to your filesystem-driven routing (Sitebender-style)**
2. **Embed just-in-time learning without breaking the spine**
3. **Enable forking, remixing, and argument _without entropy_**

---

# I. Mapping directly onto filesystem routing

You already have:

- Modules = folders
- Filesystem → routes
- No interfaces, FP bias, explicit composition

So: **content primitives _are_ modules**.

---

## 1. Canonical directory layout

```
/book
  /_spine
  /_concept
  /_example
  /_procedure
  /_argument
  /_view
```

Leading `_` = non-routable primitives. Views generate routes.

This mirrors how you likely separate internal vs public modules.

---

## 2. Primitives as pure data modules

Each file exports **data, not markup**.

Example: `_concept/event-propagation.ts`

```ts
export const concept = {
	id: "event-propagation",
	term: "Event Propagation",
	definition: `
    Event propagation describes how changes in one part
    of a system trigger updates in other parts.
  `,
	constraints: {
		minWords: 150,
		maxWords: 300,
	},
} as const;
```

No JSX. No layout. No opinion.

This is FP-friendly and composable.

---

## 3. Chapters as compositions (pure functions)

`/_view/chapter/02-reactive-loop.tsx`

```ts
import { concept as propagation } from "_concept/event-propagation.ts";
import { example as loop } from "_example/event-propagation/basic-loop.ts";
import { procedure } from "_procedure/build-loop.ts";

export default Chapter(uses(propagation), shows(loop), teaches(procedure));
```

Routing is automatic:

```
/chapter/02-reactive-loop
```

The chapter has _no authority_ to invent structure.

---

## 4. Spine as a compile-time dependency graph

`/_spine/02.ts`

```ts
export const learningState = {
	id: "reactive-loop",
	requires: ["event-propagation", "stateless-rendering"],
	enables: ["build-reactive-loop"],
};
```

Build fails if:

- A chapter doesn’t advance a spine state
- A spine state references missing concepts
- A concept isn’t used

This is pedagogy as type system.

---

# II. Just-in-time learning (without destroying linearity)

JIT learning usually degenerates into:

> “Here’s a sidebar you didn’t know you needed.”

We avoid that by making **ignorance explicit and bounded**.

---

## 1. JIT slots are declared, not emergent

Chapter sections may declare:

```ts
jit: {
  concept: "event-queue",
  reason: "needed to understand async propagation",
  maxDepth: 1
}
```

Rules:

- JIT cannot introduce a brand-new dependency chain
- JIT content must already exist
- Depth is capped (no rabbit holes)

---

## 2. Reader experience

When hitting JIT:

- Reader sees:

  > “We need one idea _now_. Full treatment comes later.”

Options:

- Inline micro-definition (≤50 words)
- Jump to concept
- Defer

The system **tracks deferred concepts**.

---

## 3. JIT debt must be repaid

The spine enforces:

> Any JIT concept must appear formally in a later learning state.

Unpaid JIT → build fails.

This preserves narrative honesty.

---

## 4. Pedagogy is surfaced explicitly

The UI literally says:

> “This is a just-in-time detour. We’re optimizing momentum, not completeness.”

Learners learn _why_ they’re confused.

That matters.

---

# III. Forking, remixing, and arguing without collapse

This is the hardest part. And the most important.

---

## 1. Canon vs branches (Git, but semantic)

There is **one canon**:

```
/book
```

Learners fork into:

```
/forks/chas/
```

Forks can:

- Add arguments
- Add alternative procedures
- Propose concept modifications

But cannot:

- Mutate canon directly
- Break spine constraints

---

## 2. Arguments as first-class dissent

```
/forks/chas/_argument/why-stateless-fails.md
```

Arguments must declare:

```yaml
targets:
  - concept: stateless-rendering
stance: dispute
scope: advanced
```

The system renders:

- Canon content unchanged
- Forked arguments as overlays

Readers can toggle:

> “Show dissenting views”

No edit wars. No neutrality theater.

---

## 3. Remixing without incoherence

A remix is a **new spine** using existing primitives.

```
/forks/chas/_spine/alt-sequence.ts
```

Rules:

- All constraints still apply
- Missing prerequisites are surfaced
- Concept definitions remain canonical unless explicitly overridden

You can reorder learning _without redefining reality_.

---

## 4. Concept overrides are surgical and explicit

If a learner wants to redefine a concept:

```
/forks/chas/_concept/event-propagation.override.ts
```

Metadata:

```yaml
overrides: event-propagation
justification: "Distributed systems require causal framing"
```

UI shows:

> “You are reading a forked definition.”

No silent drift.

---

## 5. Merging is editorial, not democratic

To merge into canon:

- Constraints must pass
- Spine coherence must improve
- Conflicts must be resolved explicitly

No “consensus.” Only justification.

This mirrors how good editors actually work.

---

# IV. Why this all holds together

Because:

- **Filesystem enforces honesty**
- **Routing is derived, not authored**
- **Pedagogy is executable**
- **JIT is tracked as debt**
- **Disagreement is localized**
- **Remix happens at the spine, not the prose**

Nothing is implicit.
Nothing is hidden.
Nothing is infinite.

---

# V. The meta-insight (this is the payoff)

What you’re really doing is this:

> Turning learning, writing, and disagreement into _composable, typed operations_.

Most systems collapse because they confuse:

- Expression with structure
- Opinion with definition
- Exploration with canon

You’re separating them _mechanically_.
