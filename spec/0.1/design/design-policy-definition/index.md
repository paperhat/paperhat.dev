Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Design Policy Definition Specification

This specification defines **Design Policy** in Paperhat: what it is, what it may contain, and how it deterministically maps a **ViewModel** into a **Presentation Plan**.

Design Policy handles **intent selection**, **context-aware adaptation**, and **structural transforms**.

This document governs **policy authoring and semantics only**.
It does not define rendering, layout engines, styling systems, or target APIs.

This document is **Normative**.

---

## 1. Purpose

Design Policy exists to:

* separate **information architecture** (Views) from **presentation decisions**
* select and layer **DesignIntent sets**
* consume **context signals** for adaptive behavior
* apply **structural transforms** (move, collapse, group, summarize, etc.)
* ensure presentation decisions are **target-aware** while remaining **target-neutral**
* produce a **deterministic Presentation Plan** from a ViewModel and target context

**Target-aware** means policy MAY branch on target medium and context signals.
**Target-neutral** means policy produces a Presentation Plan expressed only in Paperhat plan semantics, not target APIs or layout primitives.

A Design Policy answers one question only:

> Given this ViewModel, these intent sets, and this context, what should be realized?

---

## 2. Position in the Pipeline

Design Policy is applied by Kernel during the planning phase:

```
Data (pure semantics)
↓
ViewModel (pure structure, with node kinds, flags, slots)
↓
DesignIntent sets (inert assignments) + DesignPolicy (selection + rules)
↓
Presentation Plan (resolved, target-neutral)
↓
Renderers
```

Rules:

* Policy application is **pure** and **deterministic**.
* Policies do **not** modify semantic truth or domain meaning.
* Policies select intent sets; they do not define or assign intent axes.
* Renderers MUST NOT re-run policy logic.

---

## 3. Core Terms (Normative)

### 3.1 Design Policy

A **Design Policy** is a declarative policy document that:

* targets one or more render targets (e.g., screen, print, voice)
* selects and layers DesignIntent sets
* consumes context signals for adaptive behavior
* declares structural transform rules over ViewModel nodes
* produces a Presentation Plan with explicit plan-level intent metadata and derived nodes

---

### 3.2 ViewModel Node

A **ViewModel Node** is a structural node derived from a View applied to domain data.

Nodes have:

* a **kind** (structural type, e.g., `Section`, `Heading`, `Item`)
* zero or more **flags** (semantic signals declared by the View)
* zero or one **slot** identity (if filling a composition slot)

---

### 3.3 Context Signal

A **Context Signal** is structured, typed, symbolic input provided to DesignPolicy for adaptive behavior.

Context signals are external to DesignPolicy; Policy consumes but does not produce them.

Context signals are **not raw measurements** and do not carry implicit units.

---

## 4. Scope and Non-Goals (Normative)

Design Policy MUST NOT:

* encode layout geometry (columns, grids, coordinates)
* encode typography, colors, or styling primitives
* reference CSS/HTML/PDF constructs
* encode interaction, navigation, or behavior
* embed executable logic or queries
* introduce new domain semantics or ontology facts
* define or assign **DesignIntent axes** (size, emphasis, density, role)
* infer or fabricate context signals

Design Policy MAY:

* select and layer DesignIntent sets
* consume context signals for conditional behavior
* suppress, collapse, expand, reorder, summarize, enumerate
* assign grouping, ordering, and structural transforms
* attach derived nodes (explicitly marked) in the Presentation Plan
* emit **Presentation Plan intent metadata** (proximity, visibility, ordering, enumeration, spacing, flagTreatment, etc.)

### 4.1 DesignIntent Axes vs Plan Intent Metadata

This specification distinguishes two categories of intent:

| Category                 | Examples                                                             | Defined By        | Assigned By       |
| ------------------------ | -------------------------------------------------------------------- | ----------------- | ----------------- |
| **DesignIntent axes**    | size, emphasis, density, role                                        | DesignIntent spec | DesignIntent sets |
| **Plan intent metadata** | proximity, visibility, ordering, enumeration, spacing, flagTreatment | This spec         | DesignPolicy      |

Rules:

* DesignPolicy MUST NOT assign DesignIntent axes.
* DesignPolicy MAY emit Plan intent metadata.
* These namespaces are distinct and MUST NOT overlap.

---

## 5. Document Form (Normative)

### 5.1 Root Concept

A Design Policy document MUST have exactly one root Concept:

```cdx
<DesignPolicy id=policy:example>
	...
</DesignPolicy>
```

### 5.2 Identity

A Design Policy MUST declare an `id` Trait.

The `id` is resolved via the active module’s applicable `idBase` according to the Codex ID Resolution Specification.

### 5.3 Location

Design Policy documents are located at:

```
modules/{ModuleName}/design/policies/{PolicyName}/policy.cdx
```

Rules:

* `{PolicyName}` folder carries the identifier (names on folders).
* File MUST be named `policy.cdx` (canonical filename).

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
* Target Context selection is performed by Kernel (not by renderers).

---

## 7. Intent Selection (Normative)

### 7.1 The UseIntent Concept

The `<UseIntent>` Concept selects a DesignIntent set to be applied.

```cdx
<UseIntent intent="recipe:base" />
```

Traits:

* `intent` — required; references a DesignIntent set by `id`

Rules:

* `<UseIntent>` MUST NOT assign axes or target nodes directly.
* `<UseIntent>` selects only; assignment is defined in the referenced intent set.
* The referenced intent set MUST exist and be valid.
* Unknown intent set reference is a **compile-time error**.

---

### 7.2 Intent Layering

Multiple `<UseIntent>` declarations layer intent sets.

```cdx
<UseIntent intent="base:typography" />
<UseIntent intent="brand:emphasis" />
```

Rules:

* All selected intent sets contribute assignments into **one resolution pool**.
* Layering does NOT create a new precedence tier.
* Resolution follows the DesignIntent precedence rules.
* Same-precedence conflicts across sets are **compile-time errors** unless resolved by higher-precedence targeting.
* Document order does not override precedence or resolve conflicts.

---

### 7.3 The When Concept

The `<When>` Concept expresses a condition over typed context signals.

`<When>` MAY be used for:

* Conditional intent selection
* Conditional structural transforms

```cdx
<When targetMedium=$Screen viewportClass=$Compact>
	<UseIntent intent="recipe:compact" />
	<Collapse slot="sidebar" />
</When>
```

Rules:

* `<When>` MUST use **typed context signal traits**, not raw numeric thresholds.
* `<When>` MUST NOT include pixel values, breakpoints, or unit-bearing numbers.
* Context signals are consumed, not fabricated.
* Unknown context signal values are **compile-time errors**.
* Multiple conditions on a single `<When>` are AND-combined.

---

## 8. Node Addressing (Normative)

Policies apply structural rules to ViewModel nodes addressed by:

* **kind** — structural node kind
* **flag** — semantic signal declared by the View
* **slot** — composition slot name
* **nodeId** — exceptional explicit identity

### 8.1 Addressing Constraints

Rules:

* All addressing MUST use typed references validated at compile time.
* Unknown kind, flag, slot, or nodeId is a **compile-time error**.
* No selector syntax, string-based paths, or wildcards are permitted.
* Policies MUST NOT rely on renderer-inferred structure.

### 8.2 NodeId Override (Exceptional)

For rare one-off cases, policies MAY address a specific node by `nodeId`.

Rules:

* `nodeId` addressing is **exceptional** and MUST NOT be the default pattern.
* Unknown `nodeId` is a **compile-time error**.

### 8.3 Addressing Precedence

When multiple address forms match the same node, the more specific address has higher precedence:

```
nodeId > slot > flag > kind
```

Rules:

* Addressing precedence is used only for resolving **same-family structural transform conflicts** (see §9.11).
* Addressing precedence does not modify DesignIntent axis precedence.

---

## 9. Structural Transform Vocabulary (Normative)

Every construct in this section maps to explicit Presentation Plan structure and/or plan-level intent metadata.
No construct in this section assigns DesignIntent axes.

### 9.1 Grouping

`<Grouping>` creates derived group nodes with proximity intent.

```cdx
<Grouping>
	<Group tightly=true>
		<Member kind="Heading" />
		<Member kind="Text" />
	</Group>
</Grouping>
```

---

### 9.2 Ordering

```cdx
<Ordering>
	<PreserveOrder kind="OrderedList" />
</Ordering>
```

---

### 9.3 Proximity

```cdx
<Proximity>
	<Close kind="Item" />
	<Separate kind="Section" />
</Proximity>
```

---

### 9.4 NegativeSpace

```cdx
<NegativeSpace>
	<AllowBetween kind="Section" />
	<AvoidWithin kind="Item" />
</NegativeSpace>
```

---

### 9.5 Collapse / Expand

```cdx
<Collapse slot="sidebar" />
<Expand kind="Section" />
```

---

### 9.6 Move

```cdx
<Move slot="quickFacts" after="title" />
```

---

### 9.7 Summarize

```cdx
<Summarize kind="Section" strategy=$Sentence maxLength=1 />
```

Rules:

* Summary MUST be deterministic.
* MUST NOT call external services or models.

---

### 9.8 Enumerate

```cdx
<Enumerate kind="OrderedList" />
```

---

### 9.9 Mark

```cdx
<Mark flag="Optional" verbally=true />
```

---

### 9.10 DisallowProgressiveDisclosure

```cdx
<DisallowProgressiveDisclosure />
```

---

### 9.11 Transform Resolution and Conflicts

Structural transforms are applied after evaluating all `<When>` conditions against the provided context signals.

Rules:

* Policy application MUST be deterministic; transform outcomes MUST NOT depend on evaluation order, traversal order, or renderer behavior.
* Some transforms are **exclusive**: multiple exclusive transforms from the same family MUST NOT apply to the same addressed node.

Exclusive families in v0.1:

* **Collapse/Expand family**: `<Collapse ... />` and `<Expand ... />` are mutually exclusive for the same addressed node.
* **Move family**: multiple `<Move ... />` transforms that relocate the same addressed node are mutually exclusive.

Conflict rules:

* If two transforms in the same exclusive family apply to the same addressed node and are in conflict, this is a **compile-time error**, unless a higher-precedence address form explicitly overrides the lower-precedence transform according to §8.3.
* If a higher-precedence transform applies, lower-precedence conflicting transforms in the same family are ignored for that addressed node.

Examples (error):

```cdx
<Collapse kind="Section" />
<Expand kind="Section" />
```

Example (resolved by precedence):

```cdx
<Collapse kind="Section" />
<Expand flag="AlwaysExpanded" />
```

A `Section` with the `AlwaysExpanded` flag MUST be expanded; other `Section` nodes MUST be collapsed.

Document order rules:

* Document order MUST NOT be used to resolve conflicts in an exclusive family.
* Multiple non-conflicting transforms MAY accumulate when they affect distinct plan metadata and do not produce contradictory structural outcomes.

---

## 10. Context Awareness (Normative)

### 10.1 Context Signals

DesignPolicy consumes **typed, symbolic context signals** as structured input.

### 10.2 Policy and Context

DesignPolicy:

* MAY branch on context signals using `<When>`
* MUST NOT infer context
* MUST NOT fabricate context signals

The production of context signals is out of scope.

---

## 11. Determinism Requirements (Normative)

Policy application MUST be deterministic with respect to:

* ViewModel structure
* Selected DesignIntent sets
* Design Policy document
* Context signals
* Target medium

---

## 12. Validation Requirements (Normative)

Validation MUST ensure:

* referenced intent sets exist and validate
* referenced kinds, flags, slots, and nodeIds are valid
* context conditions reference valid signal types
* no forbidden constructs are used
* no unresolved exclusive-family transform conflicts exist (see §9.11)

Failure is atomic.

---

## 13. Anti-Examples (Normative)

```cdx
<Columns count=2 />
<Color value="#ff0000" />
<Intent kind="Heading" size=$Large />
<Collapse node="section.sidebar.title" />
<When target=screen maxWidth=600>
```

---

## 14. Relationship to Other Specifications (Normative)

This specification MUST be read in conjunction with:

* Design Intent Definition Specification
* Presentation Plan Definition Specification
* Kernel Architecture Specification
* View Definition Specification
* View Composition Specification

---

## 15. Summary

* Design Policy is declarative, deterministic, and target-aware.
* Policy selects DesignIntent sets; it does not define or assign axes.
* Policy consumes typed context signals.
* Policy applies structural transforms only.
* All addressing is typed and statically validated.
* Renderers consume the Presentation Plan and do not re-run policy logic.

---

**End of Design Policy Definition Specification v0.1**
