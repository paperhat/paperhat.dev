Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Diagnostic Messaging and Help Philosophy Specification

---

## 1. Purpose

This specification defines the **normative philosophy, structure, and constraints** for all user-facing diagnostic messaging produced by the system.

It exists to ensure that:

* diagnostics are **helpful, empathetic, and constructive**
* users are never scolded, blamed, or shamed
* failures are framed as **system limitations or unmet requirements**, not user mistakes
* messaging remains consistent across validation, compilation, and execution
* internal semantic correctness is preserved while external communication is humane

This specification governs **messaging only**.
It does not alter predicate, guard, or validation evaluation semantics.

---

## 2. Scope

This specification applies to:

* all diagnostics presented to users
* all messages derived from validation or guard failures
* all error/help/warning text surfaced by tools, editors, or renderers

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

Invalids are **machine-facing** and MUST NOT be exposed directly to users.

They exist to support:

* deterministic evaluation
* conformance testing
* compilation to SHACL and other targets

---

### 4.2 Help (User-Facing)

A **Help** object is the **user-facing explanation** derived from one or more Invalids.

Help objects MUST:

* explain what the system could not understand or satisfy
* describe requirements in neutral, constructive language
* avoid accusatory or moralizing terms
* where possible, suggest corrective action

Help objects are the **only** diagnostics intended for direct user consumption.

---

## 5. Messaging Tone and Framing (Normative)

All user-facing messages MUST adhere to the following rules.

### 5.1 Prohibited Framing

Messages MUST NOT:

* state or imply that the user is wrong, careless, or incompetent
* use “invalid”, “illegal”, “bad”, “wrong”, or equivalent blame-oriented terms
* use imperative scolding language (“You must…”, “You did not…”)
* express frustration, sarcasm, or judgment

---

### 5.2 Required Framing

Messages SHOULD:

* describe what the system could not understand
* describe what the system needs in order to proceed
* acknowledge ambiguity or missing information
* treat the user as cooperative and well-intentioned

Preferred constructions include:

* “We couldn’t make sense of…”
* “We need… in order to…”
* “This doesn’t work yet because…”
* “Try providing…”

---

## 6. Severity Semantics

Severity communicates **impact**, not blame.

The following severity levels are normative:

* **help** — Everything works; additional guidance or optimization is offered.
* **warning** — The system can proceed, but behavior may not match intent.
* **critical** — The system cannot proceed until the issue is addressed.

Severity MUST NOT be used to express judgment or fault.

---

## 7. Diagnostic Codes

### 7.1 Purpose of Codes

Diagnostic codes exist to:

* identify the location and nature of an issue
* support tooling, filtering, and automation
* provide stable references across versions

Codes are **not** user-facing explanations.

---

### 7.2 Code Structure

All diagnostic codes MUST follow the pattern:

```
<surfaceName>::<ISSUE_DESCRIPTION>
```

Where:

* `<surfaceName>` is the public, user-visible name of the construct
* `<ISSUE_DESCRIPTION>` describes the system’s difficulty or requirement

---

### 7.3 Prohibited Code Patterns

Codes MUST NOT use blame-oriented terms, including but not limited to:

* `INVALID_*`
* `ILLEGAL_*`
* `BAD_*`
* `WRONG_*`

---

### 7.4 Preferred Issue Patterns

Codes SHOULD use system-centric language, including:

* `*_NOT_UNDERSTOOD`
* `FAILED_TO_UNDERSTAND_*`
* `NEED_*`
* `NOT_ENOUGH_*`
* `TOO_MANY_*`
* `NOTHING_PROVIDED`
* `HIT_SNAG`
* `*_FUMBLED`

These patterns explicitly frame the issue as a limitation or requirement of the system.

---

## 8. Help Object Requirements

A Help object MUST contain:

* a diagnostic `code`
* a human-readable `message`
* a `severity`

A Help object MAY contain:

* a `suggestion`
* contextual metadata
* references to related diagnostics

---

## 9. Suggestions

When the corrective action is known, Help objects SHOULD include a suggestion.

Suggestions MUST:

* be phrased as assistance, not instruction
* describe an option, not a command
* avoid imperative language where possible

Examples:

* “You could try…”
* “Providing … may help”
* “This usually works when…”

---

## 10. Aggregated Diagnostics

When multiple issues are present:

* diagnostics MUST be grouped and presented coherently
* summary messages SHOULD explain the overall situation
* detailed messages SHOULD explain individual issues without repetition

In logical “AnyOf” failures, the summary MUST explain that no option matched, not that options were “wrong”.

---

## 11. Localization and Custom Presentation

This specification governs **meaning and tone**, not formatting or localization.

Implementations MAY:

* localize messages
* adapt phrasing for different audiences
* reformat messages for UI constraints

Provided that all normative tone and framing requirements are preserved.

---

## 12. Conformance

An implementation conforms to this specification if and only if:

* all user-facing diagnostics are expressed as Help objects
* internal Invalid artifacts are never surfaced directly
* messages follow the required tone and framing rules
* codes follow the prescribed structure and naming constraints
* severity reflects impact, not blame

---

## 13. Rationale (Non-Normative)

Users interact with declarative systems to express intent.
When intent cannot be realized, the system must assist, not admonish.

A respectful, empathetic diagnostic philosophy is not cosmetic; it is a core usability requirement and a responsibility of system designers.

---

**End of Specification**
