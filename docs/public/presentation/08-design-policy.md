# Design Policy (what CSS was trying to be)

Up to this point, everything has been about **what** should be shown:
- what exists,
- what is true,
- what someone wants to see.

Design Policy is the first place where we talk about **how it should be communicated** —
without committing to any particular layout, styling system, or platform.

Design Policy does not describe *appearance*.
It describes **presentation decisions**.

---

## The problem Design Policy solves

Different mediums require different communication choices.

For example:

- On a small screen, information must be stacked and prioritized.
- On paper, everything should be visible at once.
- In voice, long lists must be summarized or chunked.
- Optional details should never interrupt the main flow.
- Important information should be emphasized consistently.

Today, these decisions are usually:
- scattered across CSS rules,
- duplicated across breakpoints,
- embedded in components,
- reimplemented for each target,
- and hard to reason about globally.

Design Policy pulls these decisions into one place.

---

## What a Design Policy is

A Design Policy is a **set of declarative rules** that describe:

- hierarchy (what matters most),
- grouping (what belongs together),
- density (how compact or spacious something should be),
- emphasis (what should stand out),
- ordering (what comes first),
- disclosure (what can be collapsed or summarized),
- medium-specific behavior (screen, print, voice).

These rules are written **once**, independently of:
- the data,
- the view definition,
- the rendering technology.

---

## Example

Below is a Design Policy authored in CDX.

```tsx
<DesignPolicy id="recipe:standard">

  <Targets>
    <Target>screen</Target>
    <Target>print</Target>
    <Target>voice</Target>
  </Targets>

  <Hierarchy>
    <Primary node="Title" />
    <Secondary node="Section" />
    <Tertiary node="ListItem" />
  </Hierarchy>

  <GroupingRules>
    <Group tightly="true">
      <Member node="Title" />
      <Member node="Summary" />
      <Member node="QuickFacts" />
    </Group>

    <Group>
      <Member node="Ingredients" />
    </Group>

    <Group>
      <Member node="Steps" />
    </Group>
  </GroupingRules>

  <Proximity>
    <Close node="IngredientRow" />
    <Separate node="Section" />
  </Proximity>

  <Contrast>
    <Emphasize node="Title" />
    <Subdue node="OptionalBadge" />
  </Contrast>

  <DensityRules>
    <Compact node="Ingredients" />
    <Comfortable node="Steps" />
  </DensityRules>

  <ResponsiveBehavior>

    <When target="screen" maxWidth="600">
      <Collapse node="QuickFacts" />
      <Move node="QuickFacts" after="Title" />
    </When>

    <When target="print">
      <Expand node="Steps" />
      <DisableProgressiveDisclosure />
    </When>

    <When target="voice">
      <Summarize node="Summary" maxLength="1-sentence" />
      <Enumerate node="Steps" />
      <MarkOptional verbally="true" />
    </When>

  </ResponsiveBehavior>

  <NegativeSpace>
    <AllowBetween node="Section" />
    <AvoidWithin node="IngredientRow" />
  </NegativeSpace>

</DesignPolicy>
````

---

## How to read this (non-technical)

This is **not layout code**.

It doesn’t say:

* where pixels go,
* how wide columns are,
* what font sizes to use.

Instead, it says things like:

* “these belong together”
* “this matters more than that”
* “this should be compact here, but comfortable there”
* “this should be summarized when spoken”

Think of Design Policy as writing down **good communication instincts** —
once — so the system can apply them consistently everywhere.

---

## For technical readers

Design Policy is **authored input**.

It is applied by the system to:

* a ViewModel, and
* a target context,

to produce a **Presentation Plan**.

---

### What Design Policy does *not* do

Design Policy does **not**:

* query data,
* change values,
* invent structure,
* depend on CSS,
* perform rendering.

It expresses **intent and constraints**, not mechanics.

---

### Why this changes the problem

In most systems:

* layout decisions are embedded in components,
* responsiveness is achieved through ad hoc rules,
* consistency is enforced socially, not mechanically.

Here:

* presentation decisions are explicit,
* reusable,
* testable,
* explainable,
* and independent of any rendering technology.

The next page shows what this enables when taken to its logical conclusion.
