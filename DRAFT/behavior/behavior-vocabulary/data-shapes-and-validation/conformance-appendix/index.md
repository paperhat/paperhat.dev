Status: INFORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Data Shapes and Validation Conformance Appendix

This document provides **test vectors** for v0.1 Data Shapes and Validation operators.

This document is **Informative**.

---

## 1. Collection size

### 1.1 `HasElementCountBetweenInclusive`

| List | Min | Max | Expected |
| --- | --- | --- | --- |
| `[]` | `0` | `0` | `Valid(true)` |
| `[1,2,3]` | `2` | `4` | `Valid(true)` |
| `[1,2,3]` | `4` | `5` | `Valid(false)` |
| `"abc"` | `2` | `4` | `Valid(false)` |
| `[1]` | `-1` | `2` | `Valid(false)` |
| `[1]` | `3` | `2` | `Valid(false)` |

---

## 2. Element membership

### 2.1 `ContainsElement`

Equality is structural equality.

| List | Element | Expected |
| --- | --- | --- |
| `[1,2,3]` | `2` | `Valid(true)` |
| `[1,2,3]` | `4` | `Valid(false)` |
| `[]` | `1` | `Valid(false)` |
| `<Absent/>` | `1` | `Valid(false)` |

---

## 3. Record key membership

### 3.1 `ContainsKey`

| Record | Key | Expected |
| --- | --- | --- |
| `{ "a": 1 }` | `"a"` | `Valid(true)` |
| `{ "a": 1 }` | `"b"` | `Valid(false)` |
| `{}` | `"a"` | `Valid(false)` |
| `{ "a": 1 }` | `Integer(1)` | `Valid(false)` |

---

## 4. Record satisfaction

These operators are higher-order and can fail when misapplied.

### 4.1 `AllKeysSatisfy`

Let predicate be `IsNonBlankString(Argument)`.

| Record | Expected |
| --- | --- |
| `{ "a": 1, "b": 2 }` | `Valid(true)` |
| `{ "": 1 }` | `Valid(false)` |
| `"not-a-record"` | `Invalid(["AllKeysSatisfy::NEED_RECORD"])` |

### 4.2 `AllValuesSatisfy`

Let predicate be `IsInteger(Argument)`.

| Record | Expected |
| --- | --- |
| `{ "a": 1, "b": 2 }` | `Valid(true)` |
| `{ "a": 1, "b": "x" }` | `Valid(false)` |
| `"not-a-record"` | `Invalid(["AllValuesSatisfy::NEED_RECORD"])` |

---

**End of Data Shapes and Validation Conformance Appendix v0.1**
