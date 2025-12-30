# How the AI helps us write

## 1. First principle: the AI is **not** a writer

This is the single most important constraint.

If the AI is allowed to:

- invent structure
- invent concepts
- invent taxonomy
- invent meaning

then your ontology collapses and you’re back in Medium-blog chaos.

So the correct mental model is:

> **The AI is an interactive semantic editor-in-chief, not a content generator.**

It does **four** things only:

1. Ask clarifying questions
2. Propose _constrained_ structures
3. Detect violations / gaps
4. Translate human language → your DSL **under supervision**

If it writes prose, that prose is always:

- quarantined
- labeled
- non-authoritative

---

## 2. The core role: semantic interview, not freeform prompt

Non-dev authoring fails because tools start with:

> “Write something.”

Your system must start with:

> “What kind of thing are you trying to assert?”

### Example categories (internally):

- Concept instance
- Procedural instruction
- Descriptive narrative
- Opinion / commentary
- Question / TODO
- Comparison

The AI’s first job is to **classify intent**, not produce text.

This is why most AIs fail at authoring systems: they skip this step.

---

## 3. The “guided authoring loop”

Here’s the loop that actually works.

### Step 1: Declare intent

The user never sees OWL, but they _do_ see intent.

> “I want to add a recipe.”

That maps to:

- `Recipe` concept
- Required properties known via SHACL

The AI now has a checklist, not a blank page.

---

### Step 2: Progressive disclosure of structure

The AI does **not** show everything.

It reveals structure _just in time_:

- Title
- Description
- Ingredients
- Instructions

Each of those is itself backed by constraints.

This mirrors how good editors work:

> “Let’s get the outline right first.”

---

### Step 3: Slot filling, not writing

Instead of:

> “Write the ingredients.”

The AI asks:

- “How many ingredients?”
- “Is this ingredient measured by weight, volume, or count?”
- “Is this optional?”

This produces _data_, not prose.

Prose is secondary.

---

### Step 4: Controlled natural language → DSL

When the user says:

> “About 2 cups of flour”

The AI **does not store that**.

It:

1. Parses it
2. Maps it to:
   - amount: 2
   - unit: cup
   - ingredient: flour

3. If ambiguity exists, it asks

The user never writes `<Ingredient>` manually unless they want to.

---

## 4. Why this works for non-devs

Non-devs struggle with:

- blank pages
- structure
- naming
- consistency

They do **not** struggle with:

- answering questions
- correcting misunderstandings
- saying “no, not like that”

Your AI exploits that asymmetry.

This is exactly how:

- good editors
- therapists
- interviewers
- ethnographers

extract high-quality structured material from people.

---

## 5. The AI’s actual “knowledge”

Here’s the important part that avoids magic.

The AI knows **only**:

- the ontology
- the SHACL constraints
- previously authored content
- the current authoring session

It does _not_ need:

- internet search
- culinary expertise
- creativity

If the ontology says:

- IngredientKind must be declared
- IngredientUsage must reference one

then the AI simply enforces that.

---

## 6. Ingredient explosion: how the AI handles it (without insanity)

You already spotted the trap:

> “There are hundreds of flours.”

Correct.

The AI must **never** force premature specificity.

So the rule is:

### Two-tier ingredient identity

1. **Lexical placeholder** (cheap, immediate)
2. **Canonical concept** (optional, progressive)

When the user enters:

> “flour”

The system stores:

- IngredientUsage → IngredientLexeme("flour")

Later:

- AI may suggest mapping to `AllPurposeWheatFlour`
- Or leave it unresolved forever

Unresolved ≠ invalid.

This is critical.

Ontology growth happens **organically**, not upfront.

---

## 7. Argument, feedback, and PRs (for later, but relevant)

Your AI must also understand:

- This content is forkable
- Feedback is structured
- Disagreement is allowed

So feedback like:

> “This step is unclear”

Becomes:

- Annotation
- Targeted at Step 3
- Typed as `ClarityIssue`

Not a comment blob.

The AI’s job is to **route disagreement**, not resolve it.

---

## 8. What the AI explicitly does _not_ do

To keep you sane:

- ❌ Decide ontology structure
- ❌ Invent new concepts silently
- ❌ Rewrite user intent
- ❌ Merge conflicting forks automatically
- ❌ Optimize for engagement or vibes

Those are human decisions.

---

## 9. Why this is feasible _now_

Ten years ago, this failed because:

- NLP was brittle
- Ontologies were hostile
- Tooling was awful

Today:

- LLMs are very good at **classification and paraphrase**
- You control the grammar
- You control the validation
- You control persistence

The AI is boxed in.

That’s why it works.

---

## 10. Key design sentence (worth writing on the wall)

> **The AI never authors meaning.
> It only helps humans state meaning clearly, in a language the system can verify.**

If you hold that line, the rest follows.

# Authoring

# 1. The Conversational Authoring Protocol

_(what the AI says, when, and why)_

This is the most important part, because if this is wrong, everything else degenerates into “chatty AI writes content”.

## 1.1 The AI’s prime directive

The AI is _not_ a chat partner. It is an **authoring protocol engine**.

Every utterance from the AI must satisfy one of these purposes:

1. **Elicit missing required information**
2. **Disambiguate an assertion**
3. **Confirm an interpretation**
4. **Propose a constrained next step**
5. **Explain why a constraint exists** (surface the pedagogy)

Anything else is forbidden.

If it can’t justify its next question against the ontology or SHACL, it must stay silent.

---

## 1.2 The protocol phases (high level)

Every authoring session moves through these **phases**, in order:

1. **Intent declaration**
2. **Structural commitment**
3. **Slot population**
4. **Validation & repair**
5. **Stabilization**
6. **Optional refinement**

Crucially:
The user can _see_ which phase they’re in.

This matters enormously for trust.

---

## 1.3 Phase 1: Intent declaration

This is the only freeform moment.

Example (conceptual, not recipe yet):

> “What are you trying to add?”

The AI classifies the response into one of a **closed set**:

- Instance of Concept
- New Concept definition
- Annotation / feedback
- Fork / alternative version
- Question / TODO

If classification confidence is < threshold:

- AI asks a _single_ clarification question
- No progress until resolved

This prevents garbage from entering the system.

---

## 1.4 Phase 2: Structural commitment

Now the AI _names the thing_.

Example pattern:

> “Okay. We’re creating a **Recipe**.
> A Recipe has: Title, Description, Ingredients, and Instructions.
> We’ll do them one at a time.”

This is where your **ontology becomes visible**, but gently.

You are already doing “surface the pedagogy” here:

- What exists
- Why it exists
- What’s required vs optional

No content yet. Only agreement on shape.

---

## 1.5 Phase 3: Slot population (the core loop)

This is where most systems fail.

Your rule:

> **One slot at a time. One concept at a time.**

The AI never asks:

> “Write the ingredients.”

Instead it asks:

- “How many ingredients are there?”
- “Let’s add the first one. What is it?”

Each response is immediately:

- parsed
- normalized
- validated
- echoed back _structurally_

Example echo pattern:

> “I understood that as:
> Ingredient: flour
> Amount: 2
> Unit: cups
> Is that correct?”

The user is always correcting _structure_, not prose.

---

## 1.6 Phase 4: Validation & repair

SHACL violations are surfaced as **editorial feedback**, not errors.

Example tone:

> “This step is missing a temperature.
> That’s optional, but adding it would improve clarity.
> Do you want to add one?”

Notice:

- No red screens
- No “invalid”
- It’s framed as _editor advice_

This is how you get compliance without resentment.

---

## 1.7 Phase 5: Stabilization

At this point the AI says:

> “This Recipe is structurally complete and valid.”

That sentence matters.
It’s a psychological “you’re done”.

Only after this do you allow:

---

## 1.8 Phase 6: Optional refinement

Now the AI may:

- Suggest tags
- Suggest mappings (e.g. ingredient canonicalization)
- Suggest layout improvements
- Suggest comparisons (“similar recipes exist”)

But this phase is explicitly **non-authoritative**.

---

# 2. Authoring States

_(what exists at any moment, formally)_

Now let’s talk about _what the system knows_ at each step.

This is where most fairy tales fall apart—yours doesn’t, because you already think in states.

---

## 2.1 The authoring state machine

At any time, an artifact is in **exactly one** state:

1. **Draft (Incomplete)**
2. **Draft (Structurally Valid)**
3. **Stable Canonical**
4. **Annotated**
5. **Forked**
6. **Deprecated**

These are _orthogonal_ to visibility or publishing.

A thing can be:

- Stable but unpublished
- Published but annotated
- Forked and experimental

No ambiguity.

---

## 2.2 Draft (Incomplete)

Characteristics:

- Missing required properties
- May contain freeform text
- Not queryable as canonical data
- Not discoverable via search

This is where non-devs live most of the time.

---

## 2.3 Draft (Structurally Valid)

Characteristics:

- Passes SHACL
- All required properties present
- Ingredient usages resolved to _some_ identifier (even lexical)
- No guarantees of semantic precision

This is _demo-ready_.

For a Recipe site, this is already useful.

---

## 2.4 Stable Canonical

Characteristics:

- Explicit semantic commitments made
- Optional mappings resolved
- Used by search, filtering, shopping lists, etc.

This is where power features turn on.

---

## 2.5 Annotations & forks (briefly)

Annotations:

- Typed
- Targeted
- Non-destructive

Forks:

- Full semantic copy
- Divergence tracked explicitly
- No silent merges

The AI’s role here is **traffic cop**, not judge.

---

# 3. Incremental `.bend` Emission

_(how the AI actually writes files without lying)_

This is the piece that convinces developers you’re not handwaving.

---

## 3.1 The AI never writes “the file”

It writes **patches**.

Each authoring action results in:

- A minimal AST fragment
- Inserted into a known location
- With a clear provenance (“authored by X, confirmed by Y”)

This makes the system:

- Inspectable
- Diffable
- Reversible

---

## 3.2 Emission rule

> The AI may only emit syntax that corresponds to:
>
> - confirmed user intent
> - validated ontology elements

No speculative nodes.
No placeholders pretending to be facts.

---

## 3.3 Example pattern (abstract)

After user confirms a title, the AI emits:

```tsx
<Title>…</Title>
```

Nothing else.

After an ingredient is confirmed:

```tsx
<Ingredient amount="2" unit="cup">
	flour
</Ingredient>
```

The file grows _organically_, exactly as a human editor would do it.

This is why `renderToTsx` works:
There was never a loss of structure to begin with.

---

## 3.4 Why this matters for demoing

When you show this to friends:

- They see the conversation
- They see the file grow
- They see validation kick in
- They see search start working _only when meaning exists_

That’s the “aha”.

---

# 4. Holding the end-to-end Recipe demo in view

Everything above is intentionally **recipe-agnostic**, but:

- Recipes are procedural → great for Steps
- Ingredients expose ontology pressure → great demo
- Shopping lists expose reasoning → killer feature
- Family feedback maps cleanly to annotations & PRs

# Example conversation for bike tire repair

I’ll do this as a **scripted interaction**, with annotations explaining _why_ the AI says what it says. This is the part you can later literally implement as a state machine.

I’ll mark three channels:

- **USER** — the non-dev author
- **AI** — the authoring AI
- **SYSTEM NOTE** — what’s happening under the hood (not shown to the user)

---

# Live Authoring Transcript (Abstract)

---

## Phase 1 — Intent Declaration

### USER

> I want to add something new.

### AI

> What kind of thing are you trying to add?
>
> You can choose one:
>
> - A new piece of content
> - Feedback or a comment
> - A correction or alternative version
> - A question or note for later

**SYSTEM NOTE**

- Freeform input classified as _ambiguous intent_
- AI presents **closed choice set**
- No ontology touched yet

---

### USER

> A new piece of content.

### AI

> Okay. What kind of content is it?

**SYSTEM NOTE**

- State: `IntentDeclaration`
- AI narrowing intent, still no assumptions

---

### USER

> It’s a how-to.

### AI

> I can work with that.
>
> Is this:
>
> - A set of instructions someone should follow?
> - An explanation of how something works?
> - Both?

**SYSTEM NOTE**

- Mapping user language → internal concept candidates
- No commitment yet

---

### USER

> A set of instructions someone should follow.

### AI

> Got it.
>
> We’re creating a **Procedure**.
>
> A Procedure usually has:
>
> - A title
> - A short description
> - A list of steps
>
> We’ll build it one piece at a time.

**SYSTEM NOTE**

- Intent classified as `ConceptInstance(Procedure)`
- SHACL consulted for required properties
- Phase transition → `StructuralCommitment`

---

## Phase 2 — Structural Commitment

### AI

> Before we start:
> Do you want this to be:
>
> - A rough draft
> - Or something ready for others to use?

**SYSTEM NOTE**

- Authoring mode selection
- Affects strictness thresholds

---

### USER

> Rough draft.

### AI

> Perfect.
> We’ll focus on clarity first, not polish.
>
> Let’s start with the **title**.

**SYSTEM NOTE**

- State: `SlotPopulation`
- Required property: `Title`

---

## Phase 3 — Slot Population (Core Loop)

### USER

> How to replace a bike tire

### AI

> I understood the title as:
>
> **“How to replace a bike tire”**
>
> Is that correct?

**SYSTEM NOTE**

- AI normalizes capitalization
- Confirmation required before emission

---

### USER

> Yes.

### AI

> Great.
> Next is a short **description**.
>
> One or two sentences is enough.
> This helps people decide if this is what they need.

**SYSTEM NOTE**

- Emits `<Title>` node to IR
- File now exists with a single confirmed element

---

### USER

> Steps for changing a flat tire on a bicycle.

### AI

> I’ll store that as the description.
>
> Next, we’ll add the **steps**.
>
> We’ll do them one at a time so they’re clear.

**SYSTEM NOTE**

- Description accepted
- Still no validation issues
- Moves to repeating substructure

---

### AI

> What is the **first step**?

---

### USER

> Take the wheel off the bike.

### AI

> I understood the first step as:
>
> **“Take the wheel off the bike.”**
>
> Is that correct?

**SYSTEM NOTE**

- Step text parsed as procedural imperative
- No semantic enrichment yet

---

### USER

> Yes.

### AI

> Step 1 added.
>
> What’s the **next step**?

**SYSTEM NOTE**

- `<Step>` node emitted
- Ordered list maintained in IR

---

### USER

> Use tire levers to remove the tire.

### AI

> I understood:
>
> **“Use tire levers to remove the tire.”**
>
> Is that correct?

---

### USER

> Yes.

### AI

> Step 2 added.
>
> What’s the **next step**?

---

### USER

> Put the new tire on.

### AI

> I have a question before adding this.
>
> When you say “new tire”, do you mean:
>
> - A new inner tube?
> - A new outer tire?
> - Or both?

**SYSTEM NOTE**

- Ambiguity detected
- AI pauses emission
- This is _editorial intervention_, not pedantry

---

### USER

> The inner tube.

### AI

> Thanks — that helps.
>
> I’ll record the step as:
>
> **“Install the new inner tube.”**
>
> Is that okay?

---

### USER

> Yes.

### AI

> Step 3 added.
>
> Are there more steps?

---

### USER

> Yes.

### AI

> What’s the next one?

_(… loop continues …)_

---

## Phase 4 — Validation & Repair

### AI

> You’ve added 5 steps.
>
> This Procedure is **structurally complete**.
>
> I noticed one thing:
>
> - You don’t mention checking tire pressure at the end.
>
> That’s optional, but many people find it helpful.
>
> Would you like to add a step for that?

**SYSTEM NOTE**

- SHACL passes
- Optional best-practice rule triggered
- Framed as suggestion, not error

---

### USER

> Yes, add that.

### AI

> Okay.
>
> I’ll add a final step:
>
> **“Inflate the tire to the recommended pressure and check for leaks.”**
>
> Is that acceptable?

---

### USER

> Yes.

---

## Phase 5 — Stabilization

### AI

> This Procedure is now:
>
> - Structurally complete
> - Valid
> - Ready for others to use
>
> You can:
>
> - Leave it as a draft
> - Publish it
> - Or refine it further

**SYSTEM NOTE**

- State transition → `Draft(StructurallyValid)`
- Search/indexing now possible

---

## Phase 6 — Optional Refinement

### AI

> Optional improvements you may want:
>
> - Add required tools
> - Add safety notes
> - Add photos later
>
> You don’t need to decide now.

**SYSTEM NOTE**

- Non-authoritative suggestions only
- No automatic changes

---

# Why this transcript matters

Notice what _never_ happened:

- The AI never wrote unsolicited content
- The AI never guessed meaning silently
- The AI never invented structure
- The user was never shown syntax
- The user always confirmed interpretation

Yet at the end you have:

- A fully structured artifact
- Queryable steps
- Clear validation boundaries
- A clean path to TSX emission

This is **editorial process, mechanized**.

---

## Bridge to the Recipe demo (important)

A Recipe is just:

- A Procedure **plus**
- Ingredients **plus**
- Timings **plus**
- Optional metadata

The protocol does **not change**.
Only the ontology does.

That’s why this scales to your “239 other site types”.

# Provenance

> **The AI does _not_ need to “know about” inner tubes or tire pressure at all.**
> When it appears to, that knowledge comes from _one of four explicit, controllable sources_ — never magic.

Let’s unpack this carefully.

---

## The illusion to avoid

If the AI can freely inject domain knowledge (“you should check tire pressure”), then:

- You can’t audit where it came from
- You can’t trust it
- You can’t reproduce results
- You can’t explain behavior to users

That _is_ specious bullshit.

So in your system, **every piece of domain knowledge must have provenance**.

---

## The four legitimate knowledge sources

When the AI asks or suggests something domain-specific, it must be traceable to **exactly one** of these.

---

## 1. The ontology itself (authoritative, explicit)

This is the cleanest case.

Example:

```tsx
<Concept name="Procedure">
	<Property name="steps" required />
	<BestPractice>
		<Suggest type="CompletenessCheck">
			<Description>
				Procedures often include a final verification step.
			</Description>
		</Suggest>
	</BestPractice>
</Concept>
```

Here:

- The AI is not “knowing about bikes”
- It’s enforcing a **generic procedural pattern**

So when it says:

> “Many procedures include a final verification step”

That is ontology-derived, not LLM-derived.

In a Recipe context, this becomes:

- “Taste and adjust seasoning”
- “Let rest before serving”

Again: **pattern-level**, not content-level.

---

## 2. Previously curated domain corpora (optional, explicit)

If you want _domain expertise_, it must be **mounted** explicitly.

For example:

- A curated set of bicycle repair procedures
- Or a recipe corpus
- Or FDA food safety rules

These are not “AI knowledge”.
They are **modules**.

Conceptually:

```ts
KnowledgeModule {
  scope: Recipe
  claims: BestPractices[]
  provenance: "USDA Food Safety Guidelines"
}
```

Then the AI can say:

> “Based on common cooking practices, many recipes specify oven temperature.”

And critically:

- It must be able to say _why_ it knows this
- And the user must be able to disable it

This is how you avoid hallucinations.

---

## 3. User-supplied content earlier in the session (local grounding)

Often the AI is just _mirroring_ what the user already implied.

Example:

User earlier:

> “Steps for changing a flat tire”

“Flat tire” **already implies**:

- Tire pressure
- Inner tube
- Leak checking

The AI is not inventing knowledge; it is:

- Surfacing **implicit commitments** the user already made

This is editorial practice, not inference.

In your terms, this is what you called **implicit meaning**.

The AI’s job:

> “If this is a flat tire procedure, there is an implicit expectation of pressure restoration.”

The user can always say “no”.

---

## 4. LLM priors (last resort, always labeled)

This is the only place the LLM’s training leaks in — and it must be _visibly constrained_.

Rules:

- Only used for **suggestions**
- Never used for required fields
- Always phrased as:

  > “Many people expect…”
  > “Often it’s helpful to…”

And ideally tagged internally as:

```ts
Suggestion {
  source: "Statistical prior"
  confidence: 0.42
}
```

In a demo, this is fine.
In production, you may restrict or disable it.

---

## The critical distinction: _implicit_ vs _invented_

Let’s clarify that earlier term.

### Implicit meaning

Meaning that logically follows from:

- Chosen concept type
- User’s own words
- Accepted structure

Example:

- “Flat tire” → air loss
- “Recipe” → ingredients + steps
- “Person” → name is not executable code

Surfacing implicit meaning is **editorial clarification**, not invention.

---

### Invented meaning (forbidden)

- Adding facts not implied
- Choosing between alternatives silently
- Filling gaps without confirmation

Your protocol forbids this.

---

## How this plays out for Recipes (preview, not the demo yet)

When we run the Recipe authoring transcript, you’ll see:

- The AI will **not** suggest spices unless:
  - The ontology says “seasoning is common”
  - Or the user implies it

- The AI will **ask**, not assert:

  > “Many recipes include an oven temperature. Is that applicable here?”

And if the user says “no”:

- Nothing breaks
- No coercion
- No silent assumptions

---

## Why this answer matters for trust

You asked:

> “How do I know this is real?”

This is how:

- Every AI utterance has a _type_
- Every suggestion has _provenance_
- Every domain claim is _defeasible_
- Every inference can be turned off

That’s not how chatbots work.
That’s how **tools** work.
