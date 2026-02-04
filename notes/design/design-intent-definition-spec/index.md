Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Design Intent Definition Specification

This specification defines the **DesignIntent dialect** and the **DesignIntent artifact model** in Paperhat.

DesignIntent enables authors to express **semantic differentiation** — what should differ — without encoding presentation, layout, or styling.

This document establishes **prior art** for intent-based visual differentiation in semantic publishing systems.

This document is **Normative**.

---

## 1. Purpose

DesignIntent exists to:

* enable non-CSS authors to express visual differentiation
* provide a closed-world vocabulary of discrete, enumerable axes
* maintain strict separation between intent and presentation
* remain target-independent and context-agnostic at authoring time
* produce deterministic intent metadata consumed by DesignPolicy and Kernel

DesignIntent answers one question only:

> What should differ, and by how much?

---

## 2. Scope

### 2.1 In Scope

This specification governs:

* the DesignIntent dialect (language definition)
* the DesignIntent artifact model (authored intent sets)
* the closed set of intent axes for v0.1
* attachment mechanisms for intent assignments
* static validation requirements
* the relationship between DesignIntent and DesignPolicy

### 2.2 Explicitly Deferred

The following are explicitly out of scope for v0.1 but MUST NOT be blocked by this specification:

* theme realization (mapping intent to presentation primitives)
* numeric modeling and distance calculations
* cultural adaptation
* emotional or environmental context
* personalization signals

---

## 3. Position in the Pipeline

DesignIntent participates in the Kernel pipeline as follows:

```
Data (pure semantics)
↓
ViewModel (pure structure, with node kinds, flags, slots)
↓
DesignIntent assignments + DesignPolicy rules
↓
Presentation Plan (resolved, target-neutral intent metadata)
↓
Renderer / Runtime (HTML, PDF, Voice, etc.)
```

Rules:

* DesignIntent sets are **inert** until selected by DesignPolicy.
* DesignPolicy selects, layers, and applies intent sets.
* Kernel resolves intent assignments into the Presentation Plan.
* Renderers consume resolved intent; they do not re-run intent logic.

---

## 4. Core Terms (Normative)

### 4.1 DesignIntent Dialect

The **DesignIntent dialect** is a Codex dialect that defines:

* the allowed intent axes
* the allowed values for each axis
* the grammar for intent assignment

The DesignIntent dialect is governed by a DesignIntent ontology expressed as triples plus declarative constraints, authored in Codex using the Schema Dialect.

---

### 4.2 DesignIntent Set

A **DesignIntent set** is an authored artifact written in the DesignIntent dialect.

A DesignIntent set:

* assigns intent axes to structural nodes
* contains **no rules**
* contains **no context conditions**
* performs **no structural transforms**
* is **inert** unless selected by DesignPolicy

---

### 4.3 Intent Axis

An **Intent Axis** is a closed enumeration of values expressing one dimension of visual differentiation.

All axes in v0.1 have exactly three values representing a spectrum from background to prominent.

---

### 4.4 ViewModel Node Kind

A **Node Kind** is the structural type of a ViewModel node (e.g., `Section`, `Group`, `Heading`, `Item`, `Text`).

Node Kinds are defined by the View ontology. They are structural classifications, not domain-specific types.

---

## 5. Intent Axes (Normative)

DesignIntent v0.1 defines exactly four axes. No additional axes may be defined in v0.1.

### 5.1 SizeIntent

`SizeIntent` expresses relative scale differentiation.

Values:

* `$Small` — reduced scale
* `$Medium` — default scale
* `$Large` — increased scale

Trait name: `size`

---

### 5.2 EmphasisIntent

`EmphasisIntent` expresses relative prominence differentiation.

Values:

* `$Subtle` — reduced prominence
* `$Normal` — default prominence
* `$Strong` — increased prominence

Trait name: `emphasis`

---

### 5.3 DensityIntent

`DensityIntent` expresses relative spacing differentiation.

Values:

* `$Compact` — reduced spacing
* `$Comfortable` — default spacing
* `$Spacious` — increased spacing

Trait name: `density`

---

### 5.4 RoleIntent

`RoleIntent` expresses semantic prominence and functional role differentiation.

This is often realized through color in visual targets, but MAY be realized through other modality-appropriate cues (e.g., voice emphasis, interaction priority, tactile indicators).

Values:

* `$Neutral` — structural/background role
* `$Muted` — de-emphasized role
* `$Primary` — brand/action role

Trait name: `role`

---

## 6. Artifact Model (Normative)

### 6.1 Location

DesignIntent sets are located at:

```
modules/{ModuleName}/design/intents/{IntentName}/intent.cdx
```

Rules:

* `{IntentName}` folder carries the identifier (names on folders).
* File MUST be named `intent.cdx` (canonical filename).

---

### 6.2 Root Concept

A DesignIntent set document MUST have exactly one root Concept:

```cdx
<DesignIntent id=intent:example>
	...
</DesignIntent>
```

---

### 6.3 Identity

A DesignIntent set MUST declare an `id` Trait.

The `id` is resolved via the active module's applicable `idBase` according to the Codex ID Resolution Specification.

---

## 7. The IntentAssignment Concept (Normative)

The `<IntentAssignment>` Concept assigns axis values to targeted structural nodes.

### 7.1 Targeting Mechanisms

An `<IntentAssignment>` MUST declare exactly one targeting mechanism:

| Trait   | Targets                                | Validated Against        |
| ------- | -------------------------------------- | ------------------------ |
| `kind`  | All nodes of a structural kind         | View ontology node kinds |
| `flag`  | All nodes carrying a single named flag | View-declared Flag names |
| `flags` | All nodes carrying *all* listed flags  | View-declared Flag names |
| `slot`  | All nodes filling a named slot         | View-declared Slot names |

Rules:

* Exactly one of `kind`, `flag`, `flags`, or `slot` MUST be present.
* The value(s) MUST reference valid kinds, flags, or slots in the resolved View.
* Unknown kind, flag, or slot is a **compile-time error**.
* No selector syntax, string-based paths, or wildcards are permitted.
* `flags` (plural) has higher precedence than `flag` (singular) — see §8.2.

---

### 7.2 NodeId Override (Exceptional)

For rare one-off overrides, an `<IntentAssignment>` MAY use `nodeId` targeting:

| Trait    | Targets                     | Validated Against         |
| -------- | --------------------------- | ------------------------- |
| `nodeId` | A specific node by identity | ViewModel node identities |

Rules:

* `nodeId` targeting is **exceptional** and MUST NOT be the default pattern.
* `nodeId` MUST reference a valid node identity in the ViewModel.
* Unknown `nodeId` is a **compile-time error**.
* `nodeId` has **highest precedence**, above Slot.

---

### 7.3 Axis Traits

An `<IntentAssignment>` MUST declare at least one axis trait.

Allowed axis traits:

* `size` — `$Small` | `$Medium` | `$Large`
* `emphasis` — `$Subtle` | `$Normal` | `$Strong`
* `density` — `$Compact` | `$Comfortable` | `$Spacious`
* `role` — `$Neutral` | `$Muted` | `$Primary`

Rules:

* Omitted axes receive no assignment from this rule (they inherit from lower-precedence rules or system defaults).
* An assignment with no axis traits is invalid.

---

### 7.4 Example

```cdx
<DesignIntent id=recipe:base>
	<IntentAssignment kind="Heading" size=$Large emphasis=$Strong />
	<IntentAssignment kind="Text" size=$Medium emphasis=$Normal />
	<IntentAssignment kind="Item" density=$Comfortable />
	<IntentAssignment flag="Optional" emphasis=$Subtle role=$Muted />
	<IntentAssignment flag="Important" emphasis=$Strong role=$Primary />
	<IntentAssignment slot="sidebar" density=$Compact size=$Small />
</DesignIntent>
```

---

## 8. Resolution and Merge (Normative)

### 8.1 Axis-Wise Merge

Intent resolution operates **per-axis**.

Each axis is resolved independently. A node's final intent is the combination of resolved values across all four axes.

Example:

```
kind="Section":    size=$Medium  density=$Comfortable
flag="Important":  emphasis=$Strong
─────────────────────────────────────────────────────
Result:            size=$Medium  density=$Comfortable  emphasis=$Strong
```

---

### 8.2 Precedence

When multiple assignments match a node, precedence determines which value wins **per axis**:

```
NodeId > Slot > flags (plural) > flag (singular) > Kind > System Default
```

Rules:

* Higher precedence wins.
* If a higher-precedence assignment does not specify an axis, the next lower precedence applies.
* System defaults apply when no assignment specifies an axis.
* `flags` (plural) has higher precedence than `flag` (singular) because it is more specific.

---

### 8.3 System Defaults

If no assignment specifies an axis value for a node, the system default applies:

* `size` → `$Medium`
* `emphasis` → `$Normal`
* `density` → `$Comfortable`
* `role` → `$Neutral`

---

### 8.4 Same-Precedence Conflicts

If two assignments at the **same precedence level** specify **different values** for the **same axis** on the **same node**, this is a **compile-time error**.

Example (error):

```cdx
<IntentAssignment flag="Important" emphasis=$Strong />
<IntentAssignment flag="Featured" emphasis=$Subtle />
```

A node with both `Important` and `Featured` flags has conflicting `emphasis` values at the same precedence level. This MUST fail compilation.

---

### 8.5 Explicit Conflict Resolution

To resolve same-precedence conflicts, authors MUST provide an explicit combined assignment using the `flags` (plural) targeting mechanism (see §7.1):

```cdx
<IntentAssignment flag="Important" emphasis=$Strong />
<IntentAssignment flag="Featured" emphasis=$Subtle />
<IntentAssignment flags=["Important", "Featured"] emphasis=$Strong />
```

Rules:

* The `flags` trait (plural) matches nodes carrying **all** listed flags.
* The combined-flag assignment explicitly resolves the conflict for nodes with both flags.
* See §8.2 for the full precedence order.

---

## 9. Relationship to DesignPolicy (Normative)

### 9.1 Selection

DesignIntent sets are **inert** until selected by DesignPolicy.

DesignPolicy selects intent sets using the `<UseIntent>` mechanism (defined in the Design Policy Definition Specification).

### 9.2 Separation of Concerns

| Concern                              | Owner                |
| ------------------------------------ | -------------------- |
| Intent axis definitions              | DesignIntent dialect |
| Intent assignments to nodes          | DesignIntent sets    |
| Selection of which intent sets apply | DesignPolicy         |
| Layering and override of intent sets | DesignPolicy         |
| Context-aware switching              | DesignPolicy         |
| Structural transforms                | DesignPolicy         |
| Resolution into Presentation Plan    | Kernel               |

### 9.3 What DesignIntent MUST NOT Do

DesignIntent sets MUST NOT:

* select themselves
* consume or reference context signals
* perform structural transforms (move, collapse, group, etc.)
* contain conditional rules
* reference other intent sets

---

## 10. Context Awareness (Normative)

### 10.1 Context Signals

DesignPolicy consumes **context signals** as structured input to inform intent selection and structural adaptation.

Context signals MAY include (non-exhaustive):

* target size and medium (screen, print, voice)
* accessibility preferences
* cultural context
* environmental conditions (lighting, motion preferences)
* personalization signals
* emotional or cognitive state indicators

### 10.2 DesignIntent and Context

DesignIntent MUST NOT:

* reference context signals
* consume context as input
* vary based on context

DesignPolicy MUST NOT:

* infer context from unstructured sources
* fabricate context signals

The **production** of context signals is out of scope for v0.1.

### 10.3 Rationale

This separation ensures that:

* Intent sets remain pure, deterministic, and reusable
* Context-aware behavior is centralized in Policy
* Future context mechanisms can be introduced without modifying intent sets

---

## 11. DesignVector (Normative)

### 11.1 Internal Representation

Kernel MAY compute internal numeric representations of resolved intent (e.g., vectors, distance metrics) for purposes including:

* validation and diagnostics
* conflict detection
* hierarchy analysis
* rule resolution optimization

### 11.2 Constraints

DesignVector representations:

* are **non-semantic** — they carry no meaning beyond internal processing
* are **not authored** — authors never write or see them
* MUST NOT appear in Codex — no dialect may expose numeric intent representations
* are **implementation details** — they may change without spec revision

### 11.3 Rationale

This establishes prior art for numeric modeling while keeping the authoring surface clean and semantic.

---

## 12. Validation (Normative)

DesignIntent sets MUST be validated against the DesignIntent ontology.

Validation MUST ensure:

* `kind` values reference valid View ontology node kinds
* `flag` values reference Flags declared in the active View
* `slot` values reference Slots declared in the active View
* `nodeId` values reference valid ViewModel node identities
* axis values are from the closed enumeration
* no same-precedence conflicts exist (unless explicitly resolved)
* exactly one targeting mechanism is present per assignment

If validation fails, the module run fails atomically.

---

## 13. Scope and Non-Goals (Normative)

DesignIntent MUST NOT:

* encode colors, fonts, sizes, spacing, or any presentation primitives
* encode layout geometry, coordinates, or breakpoints
* reference CSS, HTML, PDF, or target-specific constructs
* encode behavior, interaction, or navigation
* contain numeric values
* modify semantic truth or domain meaning
* perform computation or IO
* reference device or environmental assumptions

DesignIntent MAY:

* differentiate visual hierarchy through closed axes
* target nodes by structural kind, semantic flag, composition slot, or (exceptionally) node identity
* produce deterministic intent metadata for the Presentation Plan

---

## 14. Future Extensions (Non-Normative)

### 14.1 Adding New Axes

Future versions MAY introduce additional intent axes.

New axes:

* MUST be closed enumerations with discrete values
* MUST have a defined system default
* MUST integrate with the existing precedence model
* MUST NOT invalidate existing intent sets that omit the new axis

Existing intent sets that do not specify a new axis will receive the system default for that axis.

### 14.2 Extending Existing Axes

Future versions MAY add values to existing axes.

New values:

* MUST NOT change the meaning of existing values
* MUST integrate into the existing spectrum logically

### 14.3 Additional Targeting Mechanisms

Future versions MAY introduce additional targeting mechanisms.

New mechanisms:

* MUST integrate into the precedence hierarchy
* MUST be statically validated at compile time
* MUST NOT introduce selector syntax, paths, or wildcards

---

## 15. Relationship to Other Specifications (Normative)

This specification MUST be read in conjunction with:

* [Design Policy Definition Specification](../design-policy-definition/)
* [Presentation Plan Definition Specification](../presentation-plan-definition/)
* [Kernel Architecture Specification](../kernel-architecture/)
* [View Definition Specification](../view-definition/)
* [View Composition Specification](../view-composition-slots-fills-and-use/)

Authority:

* View Definition governs node kinds and Flag declarations.
* View Composition governs Slot declarations.
* Design Policy governs intent selection, context consumption, and structural transforms.
* This specification governs intent axes, assignments, and resolution semantics.
* Presentation Plan Definition governs the output format.

---

## 16. Summary

* **DesignIntent dialect** defines the vocabulary: four axes, each with three values.
* **DesignIntent sets** are authored artifacts containing intent assignments.
* Intent sets are **inert** until selected by DesignPolicy.
* Assignments target nodes via **kind**, **flag**, **flags** (plural), **slot**, or (exceptionally) **nodeId**.
* Resolution is **axis-wise** with precedence: NodeId > Slot > flags > flag > Kind > Default.
* Same-precedence conflicts are **compile-time errors** unless explicitly resolved.
* Intent sets contain **no rules, no context, no structural transforms**.
* DesignPolicy handles selection, layering, context, and structure.
* Kernel MAY use internal numeric representations (DesignVector) for processing.
* All references are **statically validated** at compile time.

---

**End of Design Intent Definition Specification v0.1**
