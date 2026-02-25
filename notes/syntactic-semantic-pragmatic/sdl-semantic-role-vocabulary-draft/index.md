# SDL Semantic Role Vocabulary — Draft v1

## Status

- **Date**: 2026-02-25
- **Status**: Draft for review
- **Implements**: DEC-05 (CDL/SDL/PDL Decisions Record)
- **Scope**: Workshop §26.5 (new)
- **Dependencies**:
  - CDL constraint operators (DEC-03)
  - Visual encoding channels (§26.6 D26-6-1)
  - Accessibility constitutional layer (§26.7)

---

## 1. Design Principles

### 1.1 What Roles Are

A semantic role declares **what an element means in the design**, not what it looks like or how it is implemented. Roles are the connective tissue between the Compositional Design Language (CDL) and the Pragmatic Design Language (PDL):

- CDL constraints reference elements by their roles.
- PDL rules target elements by their roles.
- The solver evaluates CDL obligations attached to roles.
- The non-deception contract uses role categories to floor-lock constraints.

### 1.2 Closure

This vocabulary is a **closed set for 1.0.0**. Authors assign roles from this set. They do not declare new roles. Extension happens through spec revision only. This ensures single-interpretation determinism: every conforming implementation knows exactly what every role means and what obligations it carries.

### 1.3 Assignment Rules

1. Every element in the canonical design graph (§26.2) MUST be assigned exactly one semantic role.
2. Role assignment is authored (in Codex via the DesignRole schema family), not inferred.
3. Role assignment is stable across adaptive contexts (per D26-5-3: "preserve stable role-to-encoding mapping across contexts"). PDL rules cannot reassign roles.
4. An element's role determines its CDL obligations, encoding compatibility, and accessibility binding.

### 1.4 Encoding Compatibility Notation

Each role declares which visual encoding channel types are valid for expressing its semantic properties, following the §26.6 channel taxonomy:

- **Ordered** channels: `Position`, `Size`, `Value` — support ordinal and quantitative mappings (D26-6-2, D26-6-4).
- **Selective** channels: `Shape`, `Hue`, `Texture`, `Orientation` — support categorical mappings (D26-6-3).

A role's encoding compatibility specifies which channel types carry its primary semantic distinction. This does not prevent foundries from using additional channels for aesthetic purposes — it constrains which channels carry the **semantic** mapping that must be preserved across contexts.

### 1.5 Protection Levels

| Level | Meaning | PDL Behavior |
|---|---|---|
| **Standard** | Normal adaptation rules apply. | PDL can weight, freeze, relax, guard. |
| **Elevated** | Constraints can be reweighted but not relaxed below authored values. | PDL can weight (>=), freeze, guard. Cannot relax. |
| **Protected** | Constraints are floor-locked. Guard is implicit. | PDL cannot relax or weight below authored values. All CDL obligations are hard constraints. |

---

## 2. Content Roles

Elements whose primary purpose is to convey information to the user.

### 2.1 `heading`

- **Purpose**: Primary structural heading. Establishes content hierarchy.
- **CDL obligations**:
  - `foregrounding` >= `prominent` relative to `body` elements in the same container.
  - `contrast` >= `clear` relative to `body` elements.
  - `separation` >= `clear` from following content (establishes section boundary).
- **Encoding compatibility**: Ordered (Size, Value) for hierarchy level. The heading's hierarchical rank is an ordinal distinction.
- **Accessibility binding**: `role="heading"` with `aria-level` corresponding to hierarchy depth.
- **Protection level**: Elevated. Headings are structural anchors. Adaptation must not demote a heading below its authored foregrounding.

### 2.2 `subheading`

- **Purpose**: Secondary heading, subordinate to `heading`. Provides additional sectional structure.
- **CDL obligations**:
  - `foregrounding` < parent `heading` but >= `prominent` relative to `body`.
  - `alignment` >= `aligned` with parent `heading`.
- **Encoding compatibility**: Ordered (Size, Value) for hierarchy level.
- **Accessibility binding**: `role="heading"` with `aria-level` one deeper than parent heading.
- **Protection level**: Standard.

### 2.3 `body`

- **Purpose**: Primary content text. The default content role.
- **CDL obligations**:
  - None beyond baseline readability (inherited from perceptual invariants D26-5-1).
- **Encoding compatibility**: Ordered (Value) for emphasis variation.
- **Accessibility binding**: None required (default content).
- **Protection level**: Standard.

### 2.4 `caption`

- **Purpose**: Descriptive text associated with a `figure` or `media` element.
- **CDL obligations**:
  - `proximity` >= `near` to its associated `figure` or `media` element.
  - `foregrounding` < associated element (subordinate).
  - `grouping` >= `cohesive` with associated element.
- **Encoding compatibility**: Ordered (Size, Value) for subordination. Smaller/lighter than the element it describes.
- **Accessibility binding**: Linked to parent element via `aria-describedby` or `figcaption` semantics.
- **Protection level**: Standard.

### 2.5 `label`

- **Purpose**: Identifies or names another element. Required for `input` and `control` elements.
- **CDL obligations**:
  - `proximity` >= `tight` to labeled element.
  - `grouping` >= `cohesive` with labeled element.
  - `alignment` >= `aligned` with labeled element.
- **Encoding compatibility**: Ordered (Value) for visual weight distinction from labeled element.
- **Accessibility binding**: `<label>` semantics or `aria-labelledby` association. MUST programmatically associate with labeled element.
- **Protection level**: Elevated. A label separated from its target is a usability failure.

### 2.6 `annotation`

- **Purpose**: Supplementary note, metadata, or aside. Not primary content.
- **CDL obligations**:
  - `foregrounding` <= `subtle`. Annotations are background information.
  - `separation` >= `subtle` from primary content.
- **Encoding compatibility**: Ordered (Size, Value) for de-emphasis.
- **Accessibility binding**: `role="note"` or equivalent.
- **Protection level**: Standard.

### 2.7 `data_value`

- **Purpose**: A specific data point — number, date, measurement, quantity. Distinguished from narrative text.
- **CDL obligations**:
  - `contrast` >= `clear` relative to surrounding `body` text. Data values must be visually distinguishable from narrative.
- **Encoding compatibility**: Ordered (Position, Size, Value) for quantitative comparisons between data values. Selective (Hue) for categorical data types.
- **Accessibility binding**: Semantic markup for machine-readable value (e.g., `<data>`, `<time>`, `<meter>`).
- **Protection level**: Standard. Exception: `data_value` elements scoped within any Disclosure-category role inherit Protected level.

### 2.8 `media`

- **Purpose**: Image, video, audio, or embedded content.
- **CDL obligations**:
  - `foregrounding` >= `prominent` when declared as primary content.
  - `negative_space` >= `balanced` around media boundary.
- **Encoding compatibility**: N/A (media is its own encoding).
- **Accessibility binding**: Requires `alt` text or `aria-label`. Audio/video requires captions or transcript.
- **Protection level**: Elevated for primary media. Standard for decorative media.

### 2.9 `figure`

- **Purpose**: A self-contained content unit (diagram, chart, illustration) typically with a `caption`.
- **CDL obligations**:
  - `separation` >= `clear` from surrounding content.
  - `grouping` >= `cohesive` between figure content and its `caption`.
  - `negative_space` >= `balanced` around figure boundary.
- **Encoding compatibility**: N/A (figures contain their own encoding).
- **Accessibility binding**: `role="figure"` with `aria-labelledby` linking to `caption`.
- **Protection level**: Standard.

---

## 3. Structure Roles

Elements whose primary purpose is to organize and group other elements.

### 3.1 `container`

- **Purpose**: A grouping boundary with semantic identity. Contains other elements as a named section.
- **CDL obligations**:
  - `separation` >= `clear` from sibling containers.
  - `grouping` >= `cohesive` for contained elements.
  - Perceptual boundary integrity (D26-5-5).
- **Encoding compatibility**: Selective (Hue, Texture) for categorical distinction between container types.
- **Accessibility binding**: `role="region"` with `aria-label` if the container has a named purpose.
- **Protection level**: Standard.

### 3.2 `group`

- **Purpose**: A perceptual unit of related elements without named semantic identity. Lighter than `container`.
- **CDL obligations**:
  - `grouping` >= `cohesive` for contained elements.
  - Intra-group proximity tighter than inter-group (D26-5-2).
- **Encoding compatibility**: Selective (Texture, Hue) for visual grouping cues.
- **Accessibility binding**: `role="group"` with `aria-label` if contextually useful.
- **Protection level**: Standard.

### 3.3 `separator`

- **Purpose**: Visual and semantic boundary between sections.
- **CDL obligations**:
  - `separation` >= `clear` (the separator defines the boundary).
  - `foregrounding` <= `subtle`. Separators are structural, not content.
  - `contrast` >= `soft` (visible but not dominant).
- **Encoding compatibility**: Ordered (Value) for visual weight.
- **Accessibility binding**: `role="separator"`.
- **Protection level**: Standard.

### 3.4 `landmark`

- **Purpose**: A major navigational reference point in the content structure. There should be few landmarks per composition.
- **CDL obligations**:
  - `foregrounding` >= `prominent`. Landmarks must be findable.
  - `separation` >= `strong` from surrounding content.
- **Encoding compatibility**: Ordered (Position) for spatial predictability. Selective (Hue) for categorical landmark identification.
- **Accessibility binding**: Appropriate ARIA landmark role (`banner`, `main`, `contentinfo`, `navigation`, `complementary`, `search`, `form`). The specific landmark type is author-declared.
- **Protection level**: Elevated. Landmarks are navigational anchors. Adaptation must not demote their findability.

### 3.5 `table`

- **Purpose**: A two-dimensional data structure with rows and columns. Tables present structured data where relationships between rows and columns carry meaning.
- **CDL obligations**:
  - `alignment` = `locked` for column content. Columns must be vertically aligned.
  - `repetition` >= `cohesive` across rows (consistent row treatment).
  - `separation` >= `subtle` between rows. `separation` >= `clear` between header and body.
  - `grouping` >= `cohesive` for the entire table boundary.
  - `negative_space` >= `balanced` around table boundary.
- **Encoding compatibility**: Ordered (Position) for both row and column axes. This is the defining characteristic: tables use two-dimensional positional encoding.
- **Accessibility binding**: `role="table"`. Requires programmatic row/column structure.
- **Protection level**: Standard.

### 3.6 `table_header`

- **Purpose**: A column or row header in a `table`. Identifies the meaning of the data in its column or row.
- **CDL obligations**:
  - `contrast` >= `clear` relative to `table_cell` content. Headers must be visually distinguishable from data.
  - `foregrounding` >= `prominent` relative to `table_cell`.
  - `alignment` = `locked` with the column or row it heads.
  - `repetition` >= `cohesive` across all headers (consistent header treatment).
- **Encoding compatibility**: Ordered (Value) for emphasis distinction from cells. Selective (Texture) for categorical distinction from data cells.
- **Accessibility binding**: `role="columnheader"` or `role="rowheader"`. Must declare `scope` (col/row).
- **Protection level**: Elevated. Headers are structural anchors. Adaptation must not demote header distinguishability.

### 3.7 `table_cell`

- **Purpose**: A data cell in a `table`. Contains a single data value at the intersection of a row and column.
- **CDL obligations**:
  - `alignment` = `locked` with its column.
  - `repetition` >= `cohesive` with sibling cells in the same column (consistent column treatment).
- **Encoding compatibility**: Inherits from the data type of the cell content. Ordered (Position, Size, Value) for quantitative data. Selective (Hue, Shape) for categorical data. The encoding must be consistent within a column.
- **Accessibility binding**: `role="cell"`. Must be programmatically associated with its `table_header`(s).
- **Protection level**: Standard. Exception: `table_cell` elements within a Disclosure scope inherit Protected level.

### 3.8 `list`

- **Purpose**: An ordered or unordered collection of items.
- **CDL obligations**:
  - `grouping` >= `cohesive` for list items.
  - `alignment` >= `aligned` for list items.
  - `repetition` >= `cohesive` across list items (consistent treatment).
- **Encoding compatibility**: Ordered (Position) for ordered lists.
- **Accessibility binding**: `role="list"`.
- **Protection level**: Standard.

### 3.9 `list_item`

- **Purpose**: A member of a `list`.
- **CDL obligations**:
  - `repetition` >= `cohesive` with sibling list items.
  - `alignment` >= `aligned` with sibling list items.
  - `separation` >= `subtle` between items.
- **Encoding compatibility**: Inherits from parent list context.
- **Accessibility binding**: `role="listitem"`.
- **Protection level**: Standard.

---

## 4. Interactive Roles

Elements whose primary purpose is to enable user action.

### 4.1 `primary_action`

- **Purpose**: The main action for the current context. There should be exactly one per composition scope.
- **CDL obligations**:
  - `foregrounding` = `dominant`. The primary action must be the most visually prominent interactive element.
  - `contrast` >= `strong` relative to all other interactive elements.
  - `negative_space` >= `balanced` (breathing room prevents accidental activation).
- **Encoding compatibility**: Selective (Hue, Shape) for categorical distinction from other action types. Ordered (Size) for emphasis.
- **Accessibility binding**: `role="button"` (or `role="link"` if navigation). Must be keyboard-focusable. Default focus target in its scope.
- **Protection level**: Elevated.

### 4.2 `secondary_action`

- **Purpose**: An alternative or supporting action. Complements `primary_action`.
- **CDL obligations**:
  - `foregrounding` >= `prominent` but < `primary_action` foregrounding.
  - `contrast` >= `clear` relative to `primary_action` (must be visually distinguishable).
  - `proximity` >= `near` to `primary_action` (related actions should be findable together).
- **Encoding compatibility**: Selective (Hue, Shape) for categorical distinction from `primary_action`.
- **Accessibility binding**: `role="button"` or `role="link"`. Keyboard-focusable.
- **Protection level**: Standard.

### 4.3 `destructive_action`

- **Purpose**: An action with irreversible or high-impact consequences (delete, cancel, revoke, etc.).
- **CDL obligations**:
  - `contrast` >= `strong` relative to `primary_action`. Must be categorically distinguishable.
  - `separation` >= `clear` from `primary_action`. Physical separation prevents accidental activation.
  - `foregrounding` <= `prominent`. Must not be the most visually dominant element (prevents impulsive activation).
  - Must NOT be the default focus target.
- **Encoding compatibility**: Selective (Hue) — must use a distinct hue from `primary_action` and `secondary_action`. This is a categorical distinction.
- **Accessibility binding**: `role="button"`. Keyboard-focusable. Should require confirmation pattern (not specified here — foundry UX concern, but the role's CDL obligations ensure visual caution).
- **Protection level**: Elevated. Adaptation must not increase the foregrounding of destructive actions or reduce their separation from primary actions.

### 4.4 `navigation`

- **Purpose**: A link or route to another location (page, section, external resource).
- **CDL obligations**:
  - `contrast` >= `clear` relative to `body` text. Links must be distinguishable from non-interactive text.
- **Encoding compatibility**: Selective (Hue, Texture) for categorical distinction from non-interactive text. Convention: underline or color change.
- **Accessibility binding**: `role="link"`. Keyboard-focusable. Must have descriptive accessible name.
- **Protection level**: Standard.

### 4.5 `input`

- **Purpose**: A field for user data entry (text, number, date, selection, etc.).
- **CDL obligations**:
  - `proximity` >= `tight` to its `label`. Input-label association must be perceptually obvious.
  - `grouping` >= `cohesive` with its `label`.
  - `separation` >= `subtle` from sibling `input` elements (prevents field confusion).
  - `contrast` >= `clear` between input boundary and background.
- **Encoding compatibility**: Ordered (Size) for input importance. Selective (Shape) for input type distinction.
- **Accessibility binding**: Appropriate input role (`textbox`, `spinbutton`, `combobox`, `listbox`, etc.). MUST have programmatic label association.
- **Protection level**: Elevated. An input separated from its label or visually indistinguishable from background is a usability failure.

### 4.6 `toggle`

- **Purpose**: A binary state switch (on/off, enabled/disabled, expanded/collapsed).
- **CDL obligations**:
  - `contrast` >= `strong` between the two states. The current state must be unambiguous.
  - `proximity` >= `tight` to its `label`.
- **Encoding compatibility**: Selective (Hue, Shape) for state distinction. Ordered (Value) for on/off mapping.
- **Accessibility binding**: `role="switch"` or `role="checkbox"`. Must communicate current state.
- **Protection level**: Standard.

### 4.7 `search`

- **Purpose**: A search input or search trigger. Distinct from generic `input` because search is a primary navigation/discovery pattern with specific placement and prominence expectations.
- **CDL obligations**:
  - `foregrounding` >= `prominent`. Search is a primary navigation mechanism.
  - `contrast` >= `clear` relative to surrounding content.
  - `negative_space` >= `balanced` (search needs clear visual identity).
- **Encoding compatibility**: Selective (Shape) for distinctive input form. Ordered (Size) for prominence.
- **Accessibility binding**: `role="search"` landmark wrapping an input. Must have accessible label.
- **Protection level**: Elevated. Search is a core navigation affordance.

### 4.8 `control`

- **Purpose**: A generic interactive control (slider, stepper, color picker, date picker, etc.) not covered by more specific roles.
- **CDL obligations**:
  - `contrast` >= `clear` relative to non-interactive elements.
  - `proximity` >= `tight` to its `label`.
- **Encoding compatibility**: Depends on control semantics. Ordered channels for value-oriented controls (slider). Selective channels for categorical controls.
- **Accessibility binding**: Appropriate ARIA widget role. Must be keyboard-operable.
- **Protection level**: Standard.

---

## 5. Status Roles

Elements whose primary purpose is to communicate system or process state to the user.

### 5.1 `success`

- **Purpose**: Positive outcome indication (action completed, validation passed, etc.).
- **CDL obligations**:
  - `foregrounding` >= `prominent`. Success feedback must be noticeable.
  - `contrast` >= `clear` relative to neutral content.
- **Encoding compatibility**: Selective (Hue) — must use a categorically distinct hue from `error` and `warning`. Convention: green family, but foundry-determined.
- **Accessibility binding**: `role="status"`. Must be announced to assistive technology (live region).
- **Protection level**: Standard.

### 5.2 `warning`

- **Purpose**: Caution indication. Non-blocking but attention-worthy.
- **CDL obligations**:
  - `foregrounding` >= `prominent`.
  - `contrast` >= `clear` relative to neutral content.
  - `contrast` >= `clear` relative to `error` (must not be confused with error).
- **Encoding compatibility**: Selective (Hue) — categorically distinct from `success` and `error`.
- **Accessibility binding**: `role="status"` or `role="alert"` depending on urgency. Must be announced to assistive technology.
- **Protection level**: Elevated. Warnings must not be demoted below noticeable prominence.

### 5.3 `error`

- **Purpose**: Failure indication. Blocking or requires user attention.
- **CDL obligations**:
  - `foregrounding` >= `dominant`. Errors demand immediate attention.
  - `contrast` >= `strong` relative to all other status roles.
  - `proximity` >= `near` to the element that caused the error (if applicable).
- **Encoding compatibility**: Selective (Hue) — categorically distinct from `success` and `warning`. Must not rely on Hue alone (accessibility: color blindness). Must use a second channel (Shape, Texture, or Position).
- **Accessibility binding**: `role="alert"`. Must be immediately announced to assistive technology (assertive live region).
- **Protection level**: Protected. Errors must never be obscured, demoted, or hidden by adaptation.

### 5.4 `info`

- **Purpose**: Neutral informational notice. Not success, warning, or error.
- **CDL obligations**:
  - `foregrounding` >= `subtle`. Informational but not alarming.
  - `contrast` >= `soft` relative to `body`.
- **Encoding compatibility**: Selective (Hue) for categorical distinction from other status types. May be omitted if the info role is visually integrated with content.
- **Accessibility binding**: `role="status"`.
- **Protection level**: Standard.

### 5.5 `progress`

- **Purpose**: Activity or completion indication (loading bar, step indicator, percentage).
- **CDL obligations**:
  - `foregrounding` >= `prominent` during active processes.
  - `contrast` >= `clear` relative to background.
- **Encoding compatibility**: Ordered (Position, Size, Value) for quantitative progress representation.
- **Accessibility binding**: `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`. Or `role="status"` for indeterminate progress.
- **Protection level**: Elevated during active processes.

---

## 6. Disclosure Roles

Elements that carry legal, financial, safety, or consent obligations. These roles exist to implement the non-deception contract (DEC-05): adaptation MUST NOT reduce the visibility of elements that a reasonable user needs to see before making a decision.

**All Disclosure roles have Protection level: Protected.** This is not configurable per-element. It is inherent to the category.

### 6.1 `cost_disclosure`

- **Purpose**: Monetary cost, fee, price, or financial obligation. Any element that communicates what the user will pay.
- **CDL obligations**:
  - `foregrounding` >= `prominent`. Cost must be visible without searching.
  - `contrast` >= `clear` relative to surrounding content.
  - `proximity` >= `near` to the action that triggers the cost (e.g., a purchase button).
  - `separation` >= `subtle` from unrelated content (cost must not visually merge with non-cost text).
- **Encoding compatibility**: Ordered (Size, Value) for magnitude. Cost is quantitative.
- **Accessibility binding**: Semantic markup for machine-readable value. Must be programmatically associated with its triggering action.
- **Protection level**: **Protected.** Guard is implicit. PDL cannot relax or weight below authored values. Adaptation MUST NOT demote cost visibility.

### 6.2 `risk_disclosure`

- **Purpose**: Potential negative consequence or hazard. Communicates what could go wrong.
- **CDL obligations**:
  - `foregrounding` >= `prominent`.
  - `contrast` >= `clear` relative to surrounding content.
  - `proximity` >= `near` to the action or condition that creates the risk.
- **Encoding compatibility**: Selective (Hue, Shape) for categorical identification as risk. Must not rely on Hue alone.
- **Accessibility binding**: `role="alert"` or `role="note"` depending on severity. Must be announced to assistive technology if the risk is blocking.
- **Protection level**: **Protected.**

### 6.3 `consent_gate`

- **Purpose**: Requires explicit user agreement before proceeding. The element gates an action on informed consent (terms acceptance, data sharing opt-in, subscription confirmation, etc.).
- **CDL obligations**:
  - `foregrounding` >= `prominent`.
  - `contrast` >= `strong` relative to surrounding content. Consent gates must be unmissable.
  - `separation` >= `clear` from non-consent elements. Must not be visually embedded in unrelated content.
  - `proximity` >= `tight` to the action it gates.
  - Must NOT be pre-checked or pre-selected by adaptation.
- **Encoding compatibility**: Selective (Shape, Hue) for categorical identification as consent-requiring.
- **Accessibility binding**: Appropriate input role (`checkbox`, `button`). Must be keyboard-focusable. Must have explicit accessible label describing what is being consented to.
- **Protection level**: **Protected.** This is the strongest protection case. Adaptation cannot modify any CDL obligation on a consent gate.

### 6.4 `legal_disclosure`

- **Purpose**: Legally required information: terms of service, privacy policy, regulatory notices, warranty disclaimers.
- **CDL obligations**:
  - `foregrounding` >= `subtle` (legal text is available, not necessarily prominent). Exception: when associated with a `consent_gate`, inherits the gate's `foregrounding` obligation.
  - `contrast` >= `soft` relative to background. Must be readable.
  - Must remain accessible (reachable via navigation, not hidden behind interaction).
- **Encoding compatibility**: Ordered (Value) for readability.
- **Accessibility binding**: Must be navigable. Linked to `consent_gate` if applicable.
- **Protection level**: **Protected.** Even though foregrounding is lower, adaptation cannot make legal disclosure less accessible than authored.

### 6.5 `identity_disclosure`

- **Purpose**: Personal data being collected, displayed, or transmitted. Communicates what the system knows or is learning about the user.
- **CDL obligations**:
  - `foregrounding` >= `prominent` when displaying user's personal data.
  - `contrast` >= `clear` relative to non-personal content.
  - `separation` >= `clear` from unrelated content.
- **Encoding compatibility**: Selective (Hue, Texture) for categorical identification as personal data.
- **Accessibility binding**: Appropriate content role. Should be programmatically identifiable as personal data for privacy tools.
- **Protection level**: **Protected.**

---

## 7. Summary Table

| Role | Category | Protection | Primary Encoding Type | ARIA Binding |
|---|---|---|---|---|
| `heading` | Content | Elevated | Ordered (Size, Value) | `heading` |
| `subheading` | Content | Standard | Ordered (Size, Value) | `heading` |
| `body` | Content | Standard | Ordered (Value) | (default) |
| `caption` | Content | Standard | Ordered (Size, Value) | `figcaption` assoc. |
| `label` | Content | Elevated | Ordered (Value) | `label` assoc. |
| `annotation` | Content | Standard | Ordered (Size, Value) | `note` |
| `data_value` | Content | Standard* | Ordered (Position, Size, Value) | `<data>` / `<time>` |
| `media` | Content | Elevated/Standard | N/A | `img` / `video` / `audio` |
| `figure` | Content | Standard | N/A | `figure` |
| `container` | Structure | Standard | Selective (Hue, Texture) | `region` |
| `group` | Structure | Standard | Selective (Texture, Hue) | `group` |
| `separator` | Structure | Standard | Ordered (Value) | `separator` |
| `landmark` | Structure | Elevated | Ordered (Position) + Selective (Hue) | ARIA landmark |
| `table` | Structure | Standard | Ordered (Position) two-axis | `table` |
| `table_header` | Structure | Elevated | Ordered (Value) + Selective (Texture) | `columnheader` / `rowheader` |
| `table_cell` | Structure | Standard* | (column-consistent) | `cell` |
| `list` | Structure | Standard | Ordered (Position) | `list` |
| `list_item` | Structure | Standard | (inherits) | `listitem` |
| `primary_action` | Interactive | Elevated | Selective (Hue, Shape) + Ordered (Size) | `button` / `link` |
| `secondary_action` | Interactive | Standard | Selective (Hue, Shape) | `button` / `link` |
| `destructive_action` | Interactive | Elevated | Selective (Hue) | `button` |
| `navigation` | Interactive | Standard | Selective (Hue, Texture) | `link` |
| `input` | Interactive | Elevated | Ordered (Size) + Selective (Shape) | input role |
| `toggle` | Interactive | Standard | Selective (Hue, Shape) + Ordered (Value) | `switch` / `checkbox` |
| `search` | Interactive | Elevated | Selective (Shape) + Ordered (Size) | `search` landmark |
| `control` | Interactive | Standard | (context-dependent) | widget role |
| `success` | Status | Standard | Selective (Hue) | `status` |
| `warning` | Status | Elevated | Selective (Hue) | `status` / `alert` |
| `error` | Status | Protected | Selective (Hue + Shape/Texture) | `alert` |
| `info` | Status | Standard | Selective (Hue) | `status` |
| `progress` | Status | Elevated | Ordered (Position, Size, Value) | `progressbar` |
| `cost_disclosure` | Disclosure | Protected | Ordered (Size, Value) | value markup |
| `risk_disclosure` | Disclosure | Protected | Selective (Hue, Shape) | `alert` / `note` |
| `consent_gate` | Disclosure | Protected | Selective (Shape, Hue) | input role |
| `legal_disclosure` | Disclosure | Protected | Ordered (Value) | navigable |
| `identity_disclosure` | Disclosure | Protected | Selective (Hue, Texture) | content role |

*`data_value` and `table_cell` inherit Protected when scoped inside any Disclosure-category role.

---

## 8. Cross-Layer Constraints

### 8.1 Status Roles Must Use Multi-Channel Encoding

Per D26-6-3 and accessibility requirements: `error`, `warning`, `success`, and `info` MUST NOT rely on a single selective channel (Hue) as their only distinguishing encoding. At minimum, `error` must use Hue + one other channel (Shape or Texture). This ensures color-blind users can distinguish status types.

### 8.2 Disclosure Roles Are Constitutionally Protected

Per the non-deception contract (DEC-05):

1. All Disclosure-category roles have implicit `guard` on all CDL obligations.
2. PDL `relax` and `weight` (downward) operations are prohibited on Disclosure-role constraints.
3. PDL `weight` (upward) and `freeze` are permitted (you can make disclosures more prominent, never less).
4. Violation of Disclosure protection is a Fatal diagnostic, same stratum as accessibility violations.

### 8.3 Interactive Roles Require Distinguishability

Within any composition scope, the following interactive roles MUST be categorically distinguishable from each other via selective encoding channels:

- `primary_action` vs. `secondary_action` vs. `destructive_action`
- `navigation` vs. `body` (links must not look like plain text)

This is a CDL obligation enforced at the solver level: the solver MUST reject any candidate where these roles share identical selective-channel encoding.

### 8.4 Heading Hierarchy Is Ordinal

`heading` and `subheading` roles within a container MUST maintain ordinal encoding consistency: a `heading` at hierarchy level N must have greater ordered-channel encoding (Size or Value) than a `heading` at level N+1. The solver enforces this as a hard constraint.

### 8.5 Disclosure Protection Inheritance

Any element scoped within a Disclosure-category role inherits Protected level. This applies regardless of the element's own category:

- A `data_value` inside a `cost_disclosure` is Protected (financial figures must not be obscured).
- A `table_cell` inside an `identity_disclosure` is Protected (personal data fields must not be obscured).
- A `body` element inside a `legal_disclosure` is Protected (legal text must remain readable).
- A `navigation` inside a `consent_gate` is Protected (links to full terms must remain accessible).

Inheritance is scope-based: it applies to all descendants of the Disclosure-role element in the canonical design graph.

### 8.6 Table Encoding Consistency

Within a `table`, all `table_cell` elements in the same column MUST use the same encoding channel type. If the column contains quantitative data, all cells use ordered channels. If categorical, all cells use selective channels. The solver enforces column-consistent encoding as a hard constraint. This is required for tables to be readable: inconsistent column encoding destroys the two-dimensional reading pattern.

---

## 9. Role Count and Extensibility

### 9.1 Current Count

- Content: 9 roles
- Structure: 9 roles
- Interactive: 8 roles
- Status: 5 roles
- Disclosure: 5 roles
- **Total: 36 roles**

### 9.2 Sufficiency Argument

These 36 roles cover the full design space by addressing:

- **All major content types**: text hierarchy (heading, subheading, body), associated content (caption, label, annotation), data (data_value), rich content (media, figure).
- **All structural patterns**: containment (container, group), boundaries (separator), navigation reference points (landmark), tabular data (table, table_header, table_cell), collections (list, list_item).
- **All interaction patterns**: action hierarchy (primary, secondary, destructive), wayfinding (navigation, search), data entry (input, toggle, control).
- **All major feedback patterns**: outcome status (success, warning, error, info), process state (progress).
- **All major trust/safety obligations**: financial (cost_disclosure), safety (risk_disclosure), consent (consent_gate), legal (legal_disclosure), privacy (identity_disclosure).

### 9.3 What Is Intentionally Excluded

- **Composite roles** (card, dialog, popover, tooltip, menu): These are foundry-level composition patterns, not semantic roles. A "card" is a `container` with specific CDL constraints. A "dialog" is a `container` with `landmark` elevation and focus-trapping behavior. The semantic vocabulary provides the building blocks; the foundry assembles them.
- **Media-specific roles** (audio_player, video_controls): Foundry-level interactive patterns built from `control`, `toggle`, and `progress`.
