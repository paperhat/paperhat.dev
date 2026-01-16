Status: NORMATIVE
Lock State: DRAFT (for now)
Version: 0.1
Editor: Charles F. Munat

# Semantic Display Role Specification

This specification defines **Semantic Display Roles** in Paperhat.

Semantic Display Roles classify the **communicative function** of content so that **design intent, adaptive layout strategy, and target realization** may consistently encode meaning across visual, print, voice, and other modalities.

This document is **Normative**.

---

## 1. Purpose

Semantic Display Roles exist to:

* bind **content meaning** to **design forces** (hierarchy, contrast, proximity, interruption)
* provide a stable bridge between **semantic structure** and **presentation realization**
* prevent misuse of visual signals for inappropriate semantic functions
* enable consistent adaptive behavior across targets
* eliminate ad-hoc renderer interpretation of meaning

A Semantic Display Role answers one question only:

> What communicative function does this content serve for the user?

---

## 2. Position in the System

Semantic Display Roles participate in the pipeline as follows:

```
Domain Data
↓
View (structural projection)
↓
Semantic Display Role assignment
↓
DesignIntent (style ramps)
↓
Adaptive Layout Strategy
↓
Target realization
```

Rules:

* Roles are **semantic**, not visual.
* Roles are **target-independent**.
* Roles constrain but do not prescribe layout or styling.
* Renderers MUST NOT infer or assign roles.

---

## 3. Definition (Normative)

A **Semantic Display Role** is a closed, enumerable classification indicating the **communicative purpose** of a content node.

Roles describe **function**, not appearance.

Examples of function:

* primary narrative
* auxiliary explanation
* procedural instruction
* constraint or warning
* reference material
* call to action

---

## 4. Role Set (Normative, v0.1)

Exactly the following roles are defined in v0.1.
No additional roles may be introduced in v0.1.

### 4.1 Core Narrative Roles

| Role                | Description                                 |
| ------------------- | ------------------------------------------- |
| `primary-content`   | Central content the user is here to consume |
| `secondary-content` | Supporting narrative content                |
| `auxiliary-content` | Optional or skippable elaboration           |

---

### 4.2 Procedural and Logical Roles

| Role              | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| `procedural-step` | Ordered instruction or action                                 |
| `constraint`      | Qualifying or limiting information that must remain proximate |
| `result`          | Outcome, conclusion, or produced result                       |

---

### 4.3 Reference and Metadata Roles

| Role                 | Description                                   |
| -------------------- | --------------------------------------------- |
| `reference-metadata` | Citations, provenance, footnotes, metadata    |
| `indexable-label`    | Tags, facets, categories, navigational labels |

---

### 4.4 Attention and Action Roles

| Role             | Description                              |
| ---------------- | ---------------------------------------- |
| `call-to-action` | Content intended to elicit user action   |
| `notice`         | Informational or contextual interruption |

---

### 4.5 Peripheral Roles

| Role          | Description                                       |
| ------------- | ------------------------------------------------- |
| `decorative`  | Non-informational ornamental content              |
| `promotional` | Advertising, sponsorship, or promotional material |

---

## 5. Assignment Rules (Normative)

Each content node MUST have **at most one** Semantic Display Role.

Roles are assigned through exactly one of the mechanisms below.

---

### 5.1 Implicit Assignment by Structural Kind

Some roles are implicitly assigned based on node kind.

Examples (illustrative):

* `Step` → `procedural-step`
* `Footnote` → `reference-metadata`
* `Constraint` → `constraint`

Rules:

* Implicit mappings are defined centrally by ontology.
* Implicit roles MAY be overridden explicitly.
* Implicit assignment requires no author action.

---

### 5.2 Explicit Assignment by View

A View MAY explicitly assign a Semantic Display Role to a node.

Rules:

* Explicit assignment represents **authorial intent**.
* Explicit assignment overrides implicit assignment.
* Views MUST NOT assign multiple roles to the same node.
* Views MUST NOT assign roles conditionally.

---

### 5.3 Derived Assignment by Adaptive Layout Strategy (Exceptional)

Adaptive Layout Strategy MAY assign roles **only to derived nodes**.

Examples:

* Generated summaries
* Pagination overflow containers
* “Read more” links

Rules:

* Strategy MUST NOT change the role of authored nodes.
* Derived nodes MUST be explicitly marked as derived.
* Derived role assignment MUST be deterministic.

---

### 5.4 Precedence

When multiple assignment mechanisms apply:

```
Derived (strategy, derived nodes only)
> Explicit (View)
> Implicit (by kind)
```

---

## 6. Relationship to DesignIntent (Normative)

Semantic Display Roles:

* DO NOT assign DesignIntent axes
* DO constrain the valid and preferred use of intent signals
* MAY define default **intent biases** (non-binding)

Example:

* `constraint`

  * biases toward strong emphasis
  * resists collapse
  * enforces proximity

DesignIntent sets may override biases subject to Strategy rules.

---

## 7. Relationship to Adaptive Layout Strategy (Normative)

Adaptive Layout Strategy operates **primarily over roles**, not raw node kinds.

Strategy rules MAY:

* prioritize roles under constraint
* determine collapse order by role
* enforce proximity for certain roles
* suppress or defer roles under limited capacity

Strategy MUST NOT reinterpret or invent semantic meaning.

---

## 8. Prohibitions (Normative)

Semantic Display Roles MUST NOT:

* encode layout geometry
* encode typography, color, or styling primitives
* reference target-specific constructs
* vary by context
* be assigned by renderers
* be used as substitutes for domain semantics

---

## 9. Validation Requirements (Normative)

Validation MUST ensure:

* only roles defined in §4 are used
* no node has more than one role
* assignment follows §5 precedence rules
* strategy assigns roles only to derived nodes

Failure is atomic.

---

## 10. Summary

* Semantic Display Roles encode **communicative meaning**
* Roles are finite, stable, and target-independent
* Roles bridge content semantics and design systems
* Roles constrain DesignIntent and Adaptive Layout Strategy
* Roles prevent semantic misuse of visual signals
* Roles are assigned implicitly, explicitly, or derivatively — never inferred

---

**End of Semantic Display Role Specification v0.1**
