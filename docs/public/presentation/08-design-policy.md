# Design Policy

A Design Policy is a set of rules and guidelines that dictate how content should be presented across different platforms and formats. It ensures consistency, accessibility, and usability in the way information is displayed to users.

Design Policy answers one question:

“Given this Presentation Plan and this output medium, how should it be expressed?”

Design Policy is:

- not meaning
- not data
- not layout code

It’s more like rules of good communication.

Simple examples of Design Policy rules

- On small screens, stack instead of spreading out
- On paper, show all steps (no “show more”)
- In voice, summarize long lists
- Optional items should never interrupt the main flow
- Steps should always be read in order
- Ingredients should be compact unless the user asks for detail

Think of Design Policy as:

“How to be polite, clear, and effective in this medium.”

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
```
