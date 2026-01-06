# Presentation Plan

A **Presentation Plan** is a concrete, system-generated result.

It answers this question:

**“Given this ViewModel, this Design Policy, and this target medium, how should this content be presented *here*?”**

A Presentation Plan is **not written by users**.
It is created automatically by the system.

---

## What a Presentation Plan is (and is not)

A Presentation Plan does **not** say:

- what HTML tags to use
- what CSS to write
- how pixels are positioned
- how rendering is implemented

Instead, it expresses decisions such as:

- what is primary vs secondary
- what should be grouped together
- what can be collapsed, skipped, or summarized
- what the reading order is
- how much detail is shown by default

Think of it as **resolved editorial intent**, not visual design.

---

## Where it fits in the pipeline

The Presentation Plan sits between **meaning** and **mechanics**.

```

ViewModel

* Design Policy
* target context
  ────────────────────────
  → Presentation Plan

````

- The **ViewModel** defines *what* exists and in what structure.
- **Design Policy** defines *how content should be communicated in general*.
- The **Presentation Plan** defines _how **this** content will be presented here_.

Only after this step does rendering begin.

---

## Example

Below is an example Presentation Plan generated for a recipe view.

```tsx
<PresentationPlan id="recipe:standard">
	<Emphasis>
		<Primary>Title</Primary>
		<Secondary>QuickFacts</Secondary>
	</Emphasis>

	<Grouping>
		<Group nodes="Title,Summary,QuickFacts" />
		<Group nodes="Ingredients" />
		<Group nodes="Steps" />
	</Grouping>

	<Order>
		<Show>Title</Show>
		<Show>Summary</Show>
		<Show>QuickFacts</Show>
		<Show>Ingredients</Show>
		<Show>Steps</Show>
		<Show>Tags</Show>
	</Order>

	<Density>
		<Default level="normal" />
		<Ingredients level="compact" />
		<Steps level="expanded" />
	</Density>

	<OptionalContent>
		<Badge style="subtle" />
	</OptionalContent>

	<ProgressiveDisclosure>
		<Steps>
			<InitiallyVisible count="3" />
			<Reveal mode="on-demand" />
		</Steps>
	</ProgressiveDisclosure>
</PresentationPlan>
````

---

## How to read this (non-technical)

You never write this.

The system creates it so that:

* your content is presented clearly,
* design rules are applied consistently,
* and the result makes sense for the chosen medium.

Think of the Presentation Plan as the system saying:

> “Given everything we know, this is how this content should be presented *right now*.”

Because this plan is explicit, rendering becomes straightforward and predictable.

The Presentation Plan is expressed in CDX because it represents a real decision made by the system, not an implementation detail. CDX is the system’s language for making those decisions explicit, inspectable, and explainable.

---

## For technical readers

The Presentation Plan is:

* derived, not authored
* specific, not reusable
* target-aware
* fully resolved

It contains **no open design questions**.

### What the Presentation Plan guarantees

* all grouping decisions are finalized
* ordering is explicit
* emphasis is resolved
* density and disclosure are fixed
* renderers do not need to interpret policy

This makes renderers:

* simple
* replaceable
* easy to test

---

### Design Policy vs Presentation Plan (final boundary)

* **Design Policy**
  Reusable, declarative rules about presentation *in general*.

* **Presentation Plan**
  The concrete result of applying those rules to a specific ViewModel
  in a specific context.

Designers author Design Policy.
The system produces Presentation Plans.

---

### Why this matters

By turning presentation into a planned artifact:

* design decisions become visible and explainable
* changes affect only one layer
* new render targets stop being special cases
* rendering becomes a mechanical problem

The next page shows the final step:
**rendering** — where this plan is turned into HTML, text, or speech.
