Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Diagnostic Messaging and Help Contract

---

## 1. Purpose

This specification defines the **normative philosophy, structure, and constraints** for all user-facing diagnostics produced by the Paperhat Workbench.

It exists to ensure that:

* diagnostics are **helpful, empathetic, and constructive**
* users are never scolded, blamed, or shamed
* failures are framed as **system limitations or unmet requirements**, not user mistakes
* messaging remains consistent across validation, compilation, preview, and build orchestration
* diagnostics are **structured data**, not ad-hoc strings
* internal semantic correctness is preserved while external communication is humane

This specification governs **diagnostic messaging only**.
It does not alter predicate evaluation, guard semantics, or validation logic.

---

## 2. Scope

This specification applies to:

* all user-facing diagnostics emitted by the Workbench Core
* all diagnostics surfaced by CLI, desktop studio, or web interfaces
* all diagnostics derived from validation, orchestration, or execution outcomes
* all diagnostics propagated from subordinate systems (e.g., Kernel)

This specification does **not** govern:

* internal control flow
* predicate truth values
* evaluation order
* runtime optimization behavior

---

## 3. Core Principle

### 3.1 Responsibility

**User mistakes are system failures of communication.**

When a diagnostic is produced, it means:

* the user attempted to express valid intent
* the system was unable to fully understand or satisfy that intent
* the system must explain what it needs, not accuse the user

All diagnostics MUST reflect this principle.

---

## 4. Internal vs User-Facing Concepts

### 4.1 Invalid (Internal)

An **Invalid** is an internal semantic artifact indicating that:

* a guard failed
* a validation failed
* a constraint was not satisfied

Invalids are **machine-facing only** and MUST NOT be exposed directly to users.

They exist to support:

* deterministic evaluation
* conformance testing
* semantic compilation and reasoning

---

### 4.2 Diagnostic (User-Facing)

A **Diagnostic** is a **structured, user-facing description** of a condition encountered by the system.

Diagnostics MUST:

* explain what the system could not understand or satisfy
* describe requirements in neutral, constructive language
* avoid accusatory, moralizing, or judgmental terms
* preserve causal structure when multiple issues are involved

Diagnostics are the **only** artifacts intended for direct user consumption.

---

### 4.3 Help Diagnostic

A **Help Diagnostic** is a Diagnostic whose purpose is to assist the user in understanding what the system needs in order to proceed.

All Workbench diagnostics are Help Diagnostics unless explicitly documented otherwise.

---

## 5. Diagnostic as Data (Normative)

Diagnostics MUST be represented as **structured data**, not raw text.

A Diagnostic MUST be composable, inspectable, serializable, and deterministic.

Diagnostics MAY be accumulated, nested, or grouped.

Presentation (formatting, layout, localization) is a **projection** of diagnostic data and MUST NOT alter diagnostic meaning.

---

## 6. Messaging Tone and Framing (Normative)

All user-facing diagnostic messages MUST adhere to the following rules.

### 6.1 Prohibited Framing

Diagnostics MUST NOT:

* state or imply that the user is wrong, careless, or incompetent
* use “invalid”, “illegal”, “bad”, “wrong”, or equivalent blame-oriented terms
* use imperative scolding language (“You must…”, “You did not…”)
* express frustration, sarcasm, or judgment

---

### 6.2 Required Framing

Diagnostics SHOULD:

* describe what the system could not understand
* describe what the system needs in order to proceed
* acknowledge ambiguity or missing information
* treat the user as cooperative and well-intentioned

Preferred constructions include:

* “We couldn’t make sense of…”
* “We need… in order to…”
* “This can’t proceed yet because…”
* “Providing … may help”

---

## 7. Severity Semantics (Normative)

Severity communicates **impact**, not blame.

The following severity levels are normative:

* **help** — The system can proceed; additional guidance or optimization is offered.
* **warning** — The system can proceed, but behavior may not match intent.
* **critical** — The system cannot proceed until the issue is addressed.

Severity MUST NOT be used to express judgment or fault.

---

## 8. Diagnostic Codes (Normative)

### 8.1 Purpose of Codes

Diagnostic codes exist to:

* identify the location and nature of an issue
* support tooling, filtering, and automation
* provide stable references across versions

Codes are **not** user-facing explanations.

---

### 8.2 Code Structure

All diagnostic codes MUST follow the pattern:

```
<component>::<ISSUE_DESCRIPTION>
```

Reminder:

* `<component>` identifies the public Workbench or Kernel surface
* `<ISSUE_DESCRIPTION>` describes the system’s difficulty or requirement

---

### 8.3 Prohibited Code Patterns

Codes MUST NOT use blame-oriented terms, including but not limited to:

* `INVALID_*`
* `ILLEGAL_*`
* `BAD_*`
* `WRONG_*`

---

### 8.4 Preferred Issue Patterns

Codes SHOULD use system-centric language, including:

* `*_NOT_UNDERSTOOD`
* `FAILED_TO_UNDERSTAND_*`
* `NEED_*`
* `NOT_ENOUGH_*`
* `TOO_MANY_*`
* `NOTHING_PROVIDED`
* `HIT_SNAG`
* `*_FUMBLED`

These patterns explicitly frame issues as system limitations or unmet requirements.

---

## 9. Diagnostic Structure (Normative)

A Diagnostic MUST contain:

* a `code`
* a human-readable `message`
* a `severity`

A Diagnostic MAY contain:

* a `suggestion`
* contextual data
* contextual pointers
* a causal Diagnostic

---

## 10. Suggestions (Normative)

When a corrective action is known, Diagnostics SHOULD include a suggestion.

Suggestions MUST:

* be phrased as assistance, not instruction
* describe an option, not a command
* avoid imperative language where possible

Examples:

* “You could try…”
* “Providing … may help”
* “This usually works when…”

---

## 11. Context and Pointers (Normative)

Diagnostics MAY include structured context to support explanation and navigation.

Context MAY include:

* runtime values
* paths
* identifiers
* ranges
* configuration pointers
* plan destinations

Context MUST NOT be used to assign blame.

---

## 12. Causal Structure (Normative)

When a Diagnostic is derived from another Diagnostic:

* the causal Diagnostic MUST be preserved
* upstream meaning MUST NOT be erased
* causal chains MUST remain inspectable

Opaque runtime exceptions MAY be attached as causes only when no structured Diagnostic exists.

---

## 13. Aggregated Diagnostics (Normative)

When multiple Diagnostics are present:

* Diagnostics MUST be grouped coherently
* summaries SHOULD explain the overall situation
* individual Diagnostics SHOULD explain specific conditions without repetition
* ordering MUST be deterministic

In logical “AnyOf” failures, summaries MUST explain that no option matched, not that options were wrong.

---

## 14. Localization and Presentation

This specification governs **meaning and tone**, not formatting or localization.

Implementations MAY:

* localize messages
* adapt phrasing for different audiences
* reformat diagnostics for UI constraints

Provided that all normative tone, structure, and framing requirements are preserved.

---

## 15. Conformance

An implementation conforms to this specification if and only if:

* all user-facing diagnostics are expressed as Diagnostics
* internal Invalid artifacts are never surfaced directly
* diagnostic tone and framing rules are followed
* codes follow the prescribed structure and naming constraints
* severity reflects impact, not blame
* diagnostics are structured data, not ad-hoc strings

---

## 16. Reality Rule (Normative)

This specification defines how diagnostics **are**.

There is no legacy behavior.
There are no deprecated modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
