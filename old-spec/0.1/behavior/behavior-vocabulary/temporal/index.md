Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Temporal

This specification defines the v0.1 **Temporal operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines deterministic, runtime-neutral temporal predicates and relations for Behavior Programs.

In v0.1, temporal values are represented as `Text` values and interpreted using fixed lexical profiles.

---

## 2. Shared Definitions (Normative)

### 2.1 Representation

- Temporal values are represented as `Text`.
- The supported lexical forms are those defined by Behavior Dialect §18.1.

### 2.2 Evaluation contract

- Each operand is a Behavior expression evaluated to `Validation<Value>`.
- Unless explicitly stated otherwise, if any operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)` (propagation).

---

## 3. Temporal Type Guards (Normative)

These operators test whether an input value is a `Text` value with a valid lexical form for the corresponding temporal semantic type.

Names:

- `IsCalendar`
- `IsTimeZone`
- `IsDuration`
- `IsInstant`
- `IsPlainDate`
- `IsPlainTime`
- `IsPlainDateTime`
- `IsPlainMonthDay`
- `IsPlainYearMonth`
- `IsYearWeek`
- `IsZonedDateTime`

Arity: 1

Signature:

- `TemporalGuard(value) -> Validation<boolean>`

Semantics:

- If `value` is not `Text`, return `Valid(false)`.
- Otherwise return `Valid(true)` iff the string parses according to the required encoding.
- If an encoding requires a restricted identifier set (for example `Calendar`), unrecognized identifiers MUST return `Valid(false)`.

Note (Normative): these guards are *total predicates* in v0.1 and MUST NOT return `Invalid(...)` due to parse failure.

---

## 4. Date Relations (Normative)

Names:

- `IsAfterDate`
- `IsBeforeDate`
- `IsNotAfterDate`
- `IsNotBeforeDate`
- `IsSameDate`

Arity: 2

Signature:

- `DateRel(left, right) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Invalid(...)` with code `IsAfterDate::NEED_TEXT` / `IsBeforeDate::NEED_TEXT` / `IsNotAfterDate::NEED_TEXT` / `IsNotBeforeDate::NEED_TEXT` / `IsSameDate::NEED_TEXT`.
- Otherwise parse both operands as `PlainDate`.
- If parsing fails for either operand, return `Invalid(...)` with code `IsAfterDate::INVALID_PLAIN_DATE` / `IsBeforeDate::INVALID_PLAIN_DATE` / `IsNotAfterDate::INVALID_PLAIN_DATE` / `IsNotBeforeDate::INVALID_PLAIN_DATE` / `IsSameDate::INVALID_PLAIN_DATE`.
- Otherwise compare by chronological order.

---

## 5. Time Relations (Normative)

Names:

- `IsAfterTime`
- `IsBeforeTime`
- `IsNotAfterTime`
- `IsNotBeforeTime`
- `IsSameTime`

Arity: 2

Signature:

- `TimeRel(left, right) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Invalid(...)` with code `IsAfterTime::NEED_TEXT` / `IsBeforeTime::NEED_TEXT` / `IsNotAfterTime::NEED_TEXT` / `IsNotBeforeTime::NEED_TEXT` / `IsSameTime::NEED_TEXT`.
- Otherwise parse both operands as `PlainTime`.
- If parsing fails for either operand, return `Invalid(...)` with code `IsAfterTime::INVALID_PLAIN_TIME` / `IsBeforeTime::INVALID_PLAIN_TIME` / `IsNotAfterTime::INVALID_PLAIN_TIME` / `IsNotBeforeTime::INVALID_PLAIN_TIME` / `IsSameTime::INVALID_PLAIN_TIME`.
- Otherwise compare by chronological order within a day.

---

## 6. DateTime Relations (Normative)

Names:

- `IsAfterDateTime`
- `IsBeforeDateTime`
- `IsNotAfterDateTime`
- `IsNotBeforeDateTime`
- `IsSameDateTime`

Arity: 2

Signature:

- `DateTimeRel(left, right) -> Validation<boolean>`

Semantics:

- If either operand is not `Text`, return `Invalid(...)` with code `IsAfterDateTime::NEED_TEXT` / `IsBeforeDateTime::NEED_TEXT` / `IsNotAfterDateTime::NEED_TEXT` / `IsNotBeforeDateTime::NEED_TEXT` / `IsSameDateTime::NEED_TEXT`.
- Otherwise parse both operands as `PlainDateTime`.
- If parsing fails for either operand, return `Invalid(...)` with code `IsAfterDateTime::INVALID_PLAIN_DATETIME` / `IsBeforeDateTime::INVALID_PLAIN_DATETIME` / `IsNotAfterDateTime::INVALID_PLAIN_DATETIME` / `IsNotBeforeDateTime::INVALID_PLAIN_DATETIME` / `IsSameDateTime::INVALID_PLAIN_DATETIME`.
- Otherwise compare by chronological order in local date-time ordering.

---

## 7. Relationship to Other Specifications

- The lexical profiles are defined by Behavior Dialect §18.

---

## 8. Conformance Appendix (Informative)

See [conformance-appendix/index.md](conformance-appendix/index.md).

---

**End of Behavior Vocabulary — Temporal v0.1**
