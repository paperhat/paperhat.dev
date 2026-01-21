Status: INFORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Temporal Conformance Appendix

This document provides **test vectors** for the v0.1 Temporal operator family.

This document is **Informative**.

---

## 1. Test Vector Format

Each case specifies:

- operator
- inputs (as semantic values)
- expected output (`Valid(true|false)` or `Invalid([...])`)
- expected diagnostic codes where applicable

---

## 2. Type Guards

Guards are total predicates in v0.1: non-Text inputs and parse failures yield `Valid(false)`.

### 2.1 `IsPlainDate`

| Input | Expected |
| --- | --- |
| `"2026-01-18"` | `Valid(true)` |
| `"2026-1-18"` | `Valid(false)` |
| `"2026-13-01"` | `Valid(false)` |
| `<Absent/>` | `Valid(false)` |
| `Integer(1)` | `Valid(false)` |

### 2.2 `IsPlainTime`

| Input | Expected |
| --- | --- |
| `"09:30:00"` | `Valid(true)` |
| `"09:30"` | `Valid(false)` |
| `"25:00:00"` | `Valid(false)` |

---

## 3. Date Relations

Relation operators are strict and parse failures are `Invalid(...)`.

### 3.1 `IsAfterDate`

| Left | Right | Expected |
| --- | --- | --- |
| `"2026-01-18"` | `"2026-01-17"` | `Valid(true)` |
| `"2026-01-18"` | `"2026-01-18"` | `Valid(false)` |
| `"2026-01-18"` | `"nope"` | `Invalid(["IsAfterDate::INVALID_PLAIN_DATE"])` |
| `Integer(1)` | `"2026-01-18"` | `Invalid(["IsAfterDate::NEED_TEXT"])` |

### 3.2 `IsSameDate`

| Left | Right | Expected |
| --- | --- | --- |
| `"2026-01-18"` | `"2026-01-18"` | `Valid(true)` |
| `"2026-01-18"` | `"2026-01-17"` | `Valid(false)` |

---

## 4. Time Relations

### 4.1 `IsBeforeTime`

| Left | Right | Expected |
| --- | --- | --- |
| `"09:30:00"` | `"10:00:00"` | `Valid(true)` |
| `"10:00:00"` | `"10:00:00"` | `Valid(false)` |
| `"nope"` | `"10:00:00"` | `Invalid(["IsBeforeTime::INVALID_PLAIN_TIME"])` |

---

## 5. DateTime Relations

### 5.1 `IsNotBeforeDateTime`

| Left | Right | Expected |
| --- | --- | --- |
| `"2026-01-18T10:00:00"` | `"2026-01-18T10:00:00"` | `Valid(true)` |
| `"2026-01-18T10:00:01"` | `"2026-01-18T10:00:00"` | `Valid(true)` |
| `"bad"` | `"2026-01-18T10:00:00"` | `Invalid(["IsNotBeforeDateTime::INVALID_PLAIN_DATETIME"])` |

---

**End of Temporal Conformance Appendix v0.1**
