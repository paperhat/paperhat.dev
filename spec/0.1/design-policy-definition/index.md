Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Design Policy Definition Specification

This specification defines **Design Policy** in Paperhat: what it is, what it may contain, and how it deterministically maps a **ViewModel** into a **Presentation Plan**.

This document governs **policy authoring and semantics only**.
It does not define rendering, layout engines, styling systems, or target APIs.

This document is **Normative**.

---

## 1. Purpose

Design Policy exists to:

- separate **information architecture** (Views) from **presentation decisions**
- ensure presentation decisions are **target-aware** while remaining **target-neutral**
- produce a **deterministic Presentation Plan** from a ViewModel and target context
- enable reasoning about presentation intent without embedding rendering logic

A Design Policy answers one question only:

> Given this ViewModel and target context, what presentation intent should be applied?

---

## 2. Position in the Pipeline

Design Policy is applied by Scribe during the pure planning phase:

```
Domain Graph + View Graph
↓
ViewModel
↓
Design Policy
↓
Presentation Plan
↓
Renderers
```

Rules:

- Policy application is **pure** and **deterministic**.
- Policies do **not** modify semantic truth or domain meaning.
- Renderers MUST NOT re-run policy logic.

---

## 3. Core Terms (Normative)

### 3.1 Design Policy

A **Design Policy** is a declarative policy document that:

- targets one or more render targets (e.g. screen/print/voice)
- declares presentation intent rules over ViewModel nodes and flags
- produces a Presentation Plan with explicit intent metadata and derived nodes

---

### 3.2 ViewModel Node

A **ViewModel Node** is a structural node derived from a View applied to domain data.
Nodes may be addressable by **name** as defined by the View Definition Specification.

---

### 3.3 Presentation Plan Intent

A **Presentation Plan Intent** is declarative metadata attached to Presentation Plan nodes,
as defined by the Presentation Plan Definition Specification.

Design Policy exists to map ViewModel structure into Presentation Plan structure + intent.

---

## 4. Scope and Non-Goals (Normative)

Design Policy MUST NOT:

- encode layout geometry (columns, grids, coordinates)
- encode typography, colors, or styling primitives
- reference CSS/HTML/PDF constructs
- encode interaction, navigation, or behavior
- embed executable logic or queries
- introduce new domain semantics or ontology facts

Design Policy MAY:

- suppress, collapse, expand, reorder, summarize, enumerate
- assign importance, density, proximity, emphasis
- attach intent to flags and named nodes
- introduce derived nodes (explicitly marked) in the Presentation Plan

---

## 5. Document Form (Normative)

### 5.1 Root Concept

A Design Policy document MUST have exactly one root Concept:

```cdx
<DesignPolicy id="...">
	...
</DesignPolicy>
```

### 5.2 Identity

A Design Policy MUST declare an `id` Trait.

The `id` is resolved via the active module’s applicable `idBase` according to the Codex ID Resolution Specification.

---

## 6. Targeting (Normative)

### 6.1 Targets

A policy MUST declare its supported targets:

```cdx
<Targets>
	<Target>screen</Target>
	<Target>print</Target>
	<Target>voice</Target>
</Targets>
```

Rules:

* Target identifiers are opaque tokens.
* A policy MAY support multiple targets.
* Target Context selection is performed by Scribe (not by renderers).

---

## 7. Node Addressing (Normative)

Policies apply rules to ViewModel nodes addressed by:

* structural concept class (e.g., `Section`, `Group`, `Item`)
* explicit View node `name` values (recommended)
* flags by `name`

Rules:

* If a policy references a node name, that name MUST exist in the ViewModel for the selected View.
* If a policy references a concept class, it applies to all nodes of that class in scope.
* Policies MUST NOT rely on renderer-inferred structure.

---

## 8. Policy Vocabulary and Presentation Plan Mapping (Normative)

This section is the **authoritative mapping**: every policy construct MUST map to an explicit Presentation Plan intent and/or an explicit derived node.

### 8.1 Importance → Presentation Plan Importance intent

```cdx
<Importance>
	<Primary node="..." />
	<Secondary node="..." />
	<Tertiary node="..." />
</Importance>
```

Mapping:

* Produces `importance=primary|secondary|tertiary` intent on matched nodes.

Rules:

* Importance is relative; ties are allowed.
* Importance MUST NOT imply suppression by itself.

---

### 8.2 Grouping → Presentation Plan Grouping intent and derived group nodes

```cdx
<Grouping>
	<Group tightly=true>
		<Member node="A" />
		<Member node="B" />
	</Group>
</Grouping>
```

Mapping:

* Produces `grouping=tight|loose` intent on a derived **group wrapper node** containing the members in order.
* The derived node MUST reference its member source nodes.

Rules:

* Grouping MUST NOT reorder members unless an Ordering rule also applies.
* Grouping is structural; it does not prescribe visual layout.

---

### 8.3 Ordering → Presentation Plan Ordering intent

```cdx
<Ordering>
	<PreserveOrder node="StepsList" />
</Ordering>
```

Mapping:

* Produces `ordering=preserve` intent on matched nodes.

Rules:

* Ordering rules MAY apply to lists, sections, groups, or any named node.
* Ordering does not prescribe enumeration style.

---

### 8.4 Density → Presentation Plan Density intent

```cdx
<Density>
	<Compact node="Ingredients" />
	<Comfortable node="Steps" />
</Density>
```

Mapping:

* Produces `density=compact|comfortable|spacious` intent on matched nodes.

Rules:

* Density is a planning hint; realization is renderer-specific.

---

### 8.5 Proximity → Presentation Plan Proximity intent

```cdx
<Proximity>
	<Close node="IngredientsItem" />
	<Separate node="Section" />
</Proximity>
```

Mapping:

* Produces `proximity=close|separate` intent on matched nodes or boundaries.

Rules:

* Proximity never encodes measurements.
* Proximity may influence derived grouping boundaries.

---

### 8.6 Emphasis → Presentation Plan Emphasis intent (nodes) and Flag handling intent (flags)

```cdx
<Emphasis>
	<Emphasize node="Title" />
	<Subdue flag="Optional" />
</Emphasis>
```

Mapping:

* `Emphasize node=...` → `emphasis=emphasize` intent on matched nodes.
* `Subdue flag=...` → `flagTreatment=subdue` intent for that flag name.

Rules:

* Emphasis MUST NOT prescribe typography, decoration, or styling.

---

### 8.7 Negative Space → Presentation Plan spacing intent

```cdx
<NegativeSpace>
	<AllowBetween node="Section" />
	<AvoidWithin node="IngredientsItem" />
</NegativeSpace>
```

Mapping:

* Produces `spacingBetween=allow|avoid` / `spacingWithin=allow|avoid` intent.

Rules:

* This is intent only; renderers interpret it per target.

---

### 8.8 Responsive → Target-conditional rule application and derived node transforms

```cdx
<Responsive>
	<When target="screen" maxWidth=600>
		<Collapse node="QuickFacts" />
		<Move node="QuickFacts" after="Title" />
	</When>
</Responsive>
```

`<When ...>` mapping:

* Selects a rule block based on Target Context.
* Produces target-specific Presentation Plan structure and intent.

#### 8.8.1 Collapse / Expand → Presentation Plan visibility intent and derived summary nodes

```cdx
<Collapse node="QuickFacts" />
<Expand node="Steps" />
```

Mapping:

* `Collapse` → `visibility=collapsed` intent; MAY introduce a derived collapsed representation node if needed.
* `Expand` → `visibility=expanded` intent; ensures no collapse is applied.

Rules:

* Collapse MUST be reversible and traceable.
* Collapse MUST NOT delete semantic content; it may suppress presentation.

#### 8.8.2 Move → Presentation Plan structural reorder

```cdx
<Move node="QuickFacts" after="Title" />
```

Mapping:

* Produces a reorder transform in the Presentation Plan structure for the affected siblings.

Rules:

* Move MUST preserve internal subtree order unless separately overridden.
* Move applies only within a well-defined parent scope (the smallest common ancestor in the ViewModel).

#### 8.8.3 DisallowProgressiveDisclosure → Presentation Plan constraint intent

```cdx
<DisallowProgressiveDisclosure />
```

Mapping:

* Produces `progressiveDisclosure=disallowed` intent at policy scope (or within the active When block).

Rules:

* This is a constraint for renderers; it is not UI behavior.

---

### 8.9 Summarize → Presentation Plan summarization intent and derived summary nodes

```cdx
<Summarize node="Summary" strategy=$Sentence maxLength=1 />
```

Mapping:

* Produces `summarize=true`, `summaryStrategy=...`, `summaryMaxLength=...` intent on the matched node,
  and MAY produce a derived summary node if the summarized representation differs structurally.

Rules:

* Summarize MUST NOT call external services.
* Summarize intent does not mandate a specific algorithm; it mandates that a summary representation is produced deterministically by the pipeline.

---

### 8.10 Enumerate → Presentation Plan enumeration intent

```cdx
<Enumerate node="StepsList" />
```

Mapping:

* Produces `enumeration=required` intent on the matched node.

Rules:

* Enumeration does not specify numbering style.
* Enumeration indicates that the renderer MUST provide an explicit enumeration affordance for the target (including voice).

---

### 8.11 Mark (Flag handling) → Presentation Plan flag treatment intent

```cdx
<Mark flag="Optional" verbally=true />
```

Mapping:

* Produces `flagTreatment=mark` intent for the flag name, with parameters (e.g., `verbal=true`).

Rules:

* Mark never specifies the symbol or wording; it specifies that the flag must be expressed for that target.

---

## 9. Determinism Requirements (Normative)

Policy application MUST be deterministic with respect to:

* ViewModel content and structure
* Design Policy document
* Target Context

No randomization. No time dependence. No external IO.

---

## 10. Validation Requirements (Normative)

A Design Policy MUST be validated against a Design Policy ontology + SHACL.

Validation MUST ensure:

* required structure exists (Targets, etc.)
* referenced node names are well-formed
* referenced flags are well-formed
* enumerated tokens (e.g., strategies) are schema-authorized where applicable

If a policy fails validation, the module run fails atomically (all-or-nothing).

---

## 11. Anti-Examples (Normative)

Invalid (layout geometry):

```cdx
<Columns count=2 />
```

Invalid (styling primitive):

```cdx
<Color value="#ff0000" />
```

Invalid (behavior):

```cdx
<OnClick node="Title" action="..." />
```

Invalid (renderer API reference):

```cdx
<HtmlTag name="h1" />
```

Invalid (embedded executable logic):

```cdx
<If expression="amount > 3"> ... </If>
```

---

## 12. Relationship to Other Specifications (Normative)

This specification must be read in conjunction with:

* Codex View Definition Specification
* Presentation Plan Definition Specification
* Kernel Architecture Specification

In case of conflict:

* View structure and selection are governed by the View Definition Specification
* Presentation intent and plan constraints are governed by the Presentation Plan Definition Specification
* Policy-to-plan mapping is governed by this specification

---

## 13. Summary

* Design Policy is declarative, deterministic, and target-aware.
* It maps ViewModel structure + flags into a Presentation Plan with explicit intent.
* It never encodes layout, styling, behavior, or target APIs.
* Every policy construct maps to a defined Presentation Plan intent and/or derived node.
* Renderers consume the plan; they do not re-run policy logic.

---

**End of Design Policy Definition Specification v0.1**
