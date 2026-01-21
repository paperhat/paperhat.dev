Status: INFORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Text Conformance Appendix

This document provides **test vectors** for the v0.1 Text operator family.

This document is **Informative**.

---

## 1. Test Vector Format

Each case specifies:

- operator
- inputs
- expected output (`Valid(true|false)` or `Invalid([...])`)
- expected diagnostic codes where applicable

---

## 2. Containment

### 2.1 `ContainsSubstring`

| Value | Needle | Expected |
| --- | --- | --- |
| `"paperhat"` | `"hat"` | `Valid(true)` |
| `"paperhat"` | `"cap"` | `Valid(false)` |
| `<Absent/>` | `"x"` | `Valid(false)` |
| `Integer(1)` | `"1"` | `Valid(false)` |

### 2.2 `StartsWithSubstring`

| Value | Prefix | Expected |
| --- | --- | --- |
| `"paperhat"` | `"paper"` | `Valid(true)` |
| `"paperhat"` | `"hat"` | `Valid(false)` |

### 2.3 `EndsWithSubstring`

| Value | Suffix | Expected |
| --- | --- | --- |
| `"paperhat"` | `"hat"` | `Valid(true)` |
| `"paperhat"` | `"paper"` | `Valid(false)` |

---

## 3. Length

Length is the number of Unicode scalar values.

### 3.1 Scalar-count examples

| Value | Operator | N | Expected |
| --- | --- | --- | --- |
| `"A"` | `HasLengthEqualTo` | `1` | `Valid(true)` |
| `"A"` | `HasLengthEqualTo` | `0` | `Valid(false)` |
| `"A\u030A"` | `HasLengthEqualTo` | `2` | `Valid(true)` |
| `"\u00C5"` | `HasLengthEqualTo` | `1` | `Valid(true)` |

### 3.2 Boundary checks

2-arity:

| Value | Operator | N | Expected |
| --- | --- | --- | --- |
| `"abc"` | `HasLengthAtLeast` | `3` | `Valid(true)` |
| `"abc"` | `HasLengthAtMost` | `2` | `Valid(false)` |
| `"abc"` | `HasLengthEqualTo` | `-1` | `Valid(false)` |

3-arity:

| Value | Min | Max | Expected |
| --- | --- | --- | --- |
| `"abc"` | `2` | `3` | `Valid(true)` |
| `"abc"` | `4` | `5` | `Valid(false)` |

---

## 4. Alphabetical Ordering

Ordering uses the locked profile: NFC normalization then codepoint order.

| Left | Right | Operator | Expected |
| --- | --- | --- | --- |
| `"A\u030A"` | `"\u00C5"` | `IsAlphabeticallyBefore` | `Valid(false)` |
| `"A\u030A"` | `"\u00C5"` | `IsAlphabeticallyAfter` | `Valid(false)` |
| `"a"` | `"b"` | `IsAlphabeticallyBefore` | `Valid(true)` |

---

## 5. Case

### 5.1 `IsCaseInsensitiveEqualTo`

| Left | Right | Expected |
| --- | --- | --- |
| `"Hello"` | `"hELLo"` | `Valid(true)` |
| `"Hello"` | `"World"` | `Valid(false)` |
| `Integer(1)` | `"1"` | `Valid(false)` |

---

## 6. Regular Expressions

Invalid patterns produce `Invalid(...)` with stable codes.

### 6.1 `MatchesRegularExpression`

| Value | Pattern | Expected |
| --- | --- | --- |
| `"abc"` | `"^a"` | `Valid(true)` |
| `"abc"` | `"^b"` | `Valid(false)` |
| `"abc"` | `"("` | `Invalid(["MatchesRegularExpression::INVALID_PATTERN"])` |
| `"abc"` | `Integer(1)` | `Valid(false)` |

### 6.2 `DoesNotMatchRegularExpression`

| Value | Pattern | Expected |
| --- | --- | --- |
| `"abc"` | `"^b"` | `Valid(true)` |
| `"abc"` | `"("` | `Invalid(["DoesNotMatchRegularExpression::INVALID_PATTERN"])` |

---

**End of Text Conformance Appendix v0.1**
