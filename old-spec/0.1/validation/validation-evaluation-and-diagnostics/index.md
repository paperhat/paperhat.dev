Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Validation Evaluation and Diagnostics Specification

---

## 1. Purpose

This specification defines the canonical evaluation semantics for **Validations** and their diagnostics.

It exists to ensure that:

* nested boolean logic over constraints produces **actionable diagnostics**
* multiple failing checks may be reported deterministically
* “case” validations (logical OR) are explainable rather than opaque
* the system remains closed-world, analyzable, and compilable to SHACL

This specification complements the [Predicate, Guard, and Validation Composition Surface Specification](../predicate-guard-and-validation-composition-surface/).

---

## 2. Scope

This specification governs:

* the difference between Predicates, Guards, and Validations
* how validations are evaluated
* what diagnostics are produced
* how diagnostics are structured and deterministically ordered
* how branch failures are represented for “AnyOf” validations

This specification does not define:

* localization of human-readable messages
* the full taxonomy of error codes (covered elsewhere)
* backend-specific execution details beyond observable behavior

---

## 3. Core Concepts

### 3.1 Predicate

A Predicate:

* is total and side-effect-free
* returns Boolean only
* produces no diagnostics
* MUST NOT return Invalid

---

### 3.2 Guard

A Guard:

* returns `Valid(value)` or `Invalid(...)`
* is authoritative for type/shape enforcement
* MUST return the original value unchanged on success

Guards may be used inside validations to enforce applicability and prevent cascading errors.

---

### 3.3 Validation

A Validation is an evaluable rule that produces a **ValidationOutcome**.

A ValidationOutcome consists of:

* `Pass` or `Fail`
* an ordered list of `Invalid` diagnostics

A Validation MUST be deterministic given the same inputs.

A `Fail` outcome MUST contain at least one `Invalid` diagnostic.

---

## 4. Diagnostic Model

### 4.1 Invalid

An Invalid diagnostic contains:

* `Code` (required; stable identifier)
* `Path` (required; canonical reference to failing value)
* `Message` (optional; informative only)
* `Details` (optional; structured data)

`Message` MUST NOT be used for conformance.

---

### 4.2 Path

A Path is a canonical, structured reference that identifies the failing value.

A Path MUST support at least:

* root value reference
* trait/property reference by name
* array element reference by index
* map entry reference by key (if maps are present)

The exact path surface syntax is defined elsewhere.
This specification requires only that Path be stable and deterministic.

---

## 5. Validation Primitives

### 5.1 MustSatisfy

`MustSatisfy` is the atomic validation wrapper around a Predicate.

Normative behavior:

* Evaluate the predicate.
* If predicate returns `true`, outcome is `Pass` with no Invalids.
* If predicate returns `false`, outcome is `Fail` with exactly one Invalid diagnostic.

The Invalid MUST include:

* `Code` supplied by the validation author
* `Path` of the validated value (or specified subpath)
* optional `Message` and `Details`

Predicates MUST NOT raise Invalid; they may only yield false.

---

### 5.2 Require (Guard-as-validation)

A Guard may be used as a Validation.

Normative behavior:

* Evaluate the Guard.
* If Guard returns `Valid(value)`, outcome is `Pass` with no Invalids.
* If Guard returns `Invalid(...)`, outcome is `Fail` with that Invalid.

---

## 6. Validation Combinators

Validation combinators operate on Validations and return a ValidationOutcome.

Implementations MAY evaluate operands using any strategy (including short-circuiting, reordering, or parallelism) provided that:

* the final `Pass` / `Fail` outcome is identical to the reference evaluation defined by this specification
* the ordered list of produced `Invalid` diagnostics is identical to the reference ordering rules in §8

Unless explicitly stated otherwise, validation combinators MUST behave observably as if all operands were evaluated in authored order.

---

### 6.1 AllOf

`AllOf(validations...)` succeeds only if all validations succeed.

Normative behavior:

* Evaluate every validation operand.
* If all outcomes are Pass, AllOf outcome is Pass with no Invalids.
* Otherwise, AllOf outcome is Fail with Invalids equal to the concatenation of all operand Invalids.

Ordering of Invalids:

* Invalids MUST be concatenated in the lexical order of operands as authored.
* Within each operand, the operand’s own Invalid ordering is preserved.

AllOf MUST NOT short-circuit observably, because it MUST be capable of reporting multiple failures.

---

### 6.2 AnyOf

`AnyOf(validations...)` succeeds if at least one operand succeeds.

Normative behavior:

* Evaluate every validation operand.
* If at least one outcome is Pass, AnyOf outcome is Pass with no Invalids.
* If all outcomes are Fail, AnyOf outcome is Fail with:

  1. a single summary Invalid, and
  2. branch failure information in Details.

AnyOf MUST NOT short-circuit observably, because it MUST be capable of explaining why no branch matched.

#### 6.2.1 Summary Invalid for AnyOf failure

The summary Invalid MUST have:

* `Code` supplied by the validation author (or a locked default if not supplied)
* `Path` of the validated value (or specified path)
* optional `Message`
* `Details` containing ordered branch failure information as defined in §6.2.2

The summary Invalid MUST be the first Invalid in the AnyOf Fail outcome.

#### 6.2.2 Branch failure information

When AnyOf fails, the summary Invalid’s `Details` MUST include branch failures in operand order.

Each branch failure entry MUST include:

* `BranchIndex` (0-based)
* `BranchInvalids` (the ordered Invalid list from that branch)

No branch failures may be omitted.

---

### 6.3 OneOf

`OneOf(validations...)` succeeds only if exactly one operand succeeds.

Normative behavior:

* Evaluate every operand.
* Count the number of Pass outcomes.

Cases:

1. Exactly one Pass:

   * outcome is Pass with no Invalids.

2. Zero Pass:

   * outcome is Fail with the same structure as AnyOf failure:

     * a summary Invalid and branch failures in Details.

3. More than one Pass:

   * outcome is Fail with a summary Invalid that indicates multiple matches.
   * Details MUST include the indices of all passing branches.

OneOf MUST NOT short-circuit observably.

---

### 6.4 NotValidation

`NotValidation(validation)` inverts Pass/Fail.

Normative behavior:

* Evaluate the operand validation.
* If operand is Pass, NotValidation is Fail with exactly one Invalid (supplied or default code).
* If operand is Fail, NotValidation is Pass with no Invalids.

NotValidation MUST NOT expose operand Invalids as failures when it passes.
(Those operand Invalids are informative to the failed branch, not to a successful negation.)

---

## 7. Guard Gating (Preventing Cascading Failures)

A common pattern is:

* require a type/shape guard
* then apply validations that assume that type

This specification defines a canonical gating rule.

### 7.1 GateBy

`GateBy(guardValidation, thenValidation)` is a ValidationCombinator.

Normative behavior:

* Evaluate `guardValidation`.
* If it is Fail, GateBy outcome is Fail with guard Invalids only.
* If it is Pass, evaluate `thenValidation` and return its outcome.

GateBy MUST short-circuit on guard failure to prevent meaningless downstream errors.

---

## 8. Deterministic Ordering Rules

To ensure reproducible diagnostics, implementations MUST apply these reference ordering rules:

1. Validation operands are evaluated in authored order for the purpose of defining observable results.
2. AllOf, AnyOf, and OneOf MUST produce branch details in operand order.
3. Invalid lists are concatenated in operand order.
4. No reordering based on runtime characteristics is permitted in the produced outcomes.

---

## 9. Example (Normative Outcome Shape)

Given:

* a root path `$.x`
* a validation:

`AllOf( RequireRealNumber(x), AnyOf(RangeA, RangeB, Equals1234) )`

Where:

* `RangeA = AllOf(MustSatisfy(IsGreaterThan(x,7)), MustSatisfy(IsLessThanOrEqualTo(x,42)))`
* `RangeB = AllOf(MustSatisfy(IsGreaterThanOrEqualTo(x,100)), MustSatisfy(IsLessThan(x,200)))`
* `Equals1234 = MustSatisfy(IsEqualTo(x,1234))`

If `x = 50`:

* `RequireRealNumber` passes
* `RangeA` fails (upper bound)
* `RangeB` fails (lower bound)
* `Equals1234` fails
* `AnyOf` fails with:

  * one summary Invalid at path `$.x`
  * branch Invalids for RangeA, RangeB, Equals1234 in Details
* `AllOf` fails with the AnyOf Invalid(s)

If `x = "bob"`:

* `RequireRealNumber` fails
* GateBy semantics (if used) MUST prevent evaluating numeric ranges
* diagnostics include only the type failure at `$.x`

---

## 10. Conformance

An implementation conforms if and only if it:

* evaluates validations according to the semantics above
* produces Invalid diagnostics with required fields
* preserves deterministic ordering (§8)
* never relies on predicate failures producing Invalid
* does not short-circuit observably for AllOf, AnyOf, or OneOf
* does short-circuit GateBy on guard failure

Conformance requirements for diagnostics:

* `Code` and `Path` MUST match exactly for all produced Invalids.
* This matching requirement applies recursively to Invalids nested within `Details` branch information for AnyOf and OneOf.
* `Message` is optional and non-normative.

---

**End of Specification**
