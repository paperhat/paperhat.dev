# Presentation Plan

A Presentation Plan answers this question:

“Given this ViewModel, what kind of presentation are we aiming for?”

It does not say:

- what HTML tags to use
- what CSS to write
- what the screen size is

Instead, it says things like:

- what is important vs secondary
- what should be grouped together
- what can be collapsed, skipped, or summarized
- what the reading order is
- how much detail to show by default

Think of it as editorial intent, not visual design.

The Presentation Plan sits between the ViewModel and the renderer.

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
```
