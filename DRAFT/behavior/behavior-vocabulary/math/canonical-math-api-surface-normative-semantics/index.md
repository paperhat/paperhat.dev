Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Canonical Math API Surface — Normative Semantics

This document defines the **normative meaning** of the canonical plain-English Math API surface. It exists to prevent cross-language drift caused by differing standard-library definitions.

Unless otherwise stated:

- All functions operate on **real numbers** (`RealNumber`).
- `RealNumber` conformance for this surface assumes an IEEE 754 floating-point representation (typically binary64 in major targets).
- Where a target lacks an operation, the result **MUST** be obtained by the **normative emulation** specified here.
- Errors and special values follow IEEE 754 whenever the target type does.

Conformance note:

- The single blessed Codex conformance suite for this surface is co-normative with this document.
- Any disagreement between the suite and this prose semantics document is a specification defect that MUST be resolved explicitly.

---

## 1. Value domains and special values

### 1.1 NotANumber, infinities

- `NotANumber` denotes `<NotANumber />` (IEEE NaN).
- `PositiveInfinity` and `NegativeInfinity` denote `<PositiveInfinity />` and `<NegativeInfinity />` (IEEE infinities).

If a target does not support IEEE 754 semantics for the chosen `RealNumber` representation, that representation **MUST NOT** be used for this surface.

---

## 2. Classification functions

### 2.1 IsNotANumber(x)

Returns `true` iff `x` is NaN.

### 2.2 IsFinite(x)

Returns `true` iff `x` is neither NaN nor ±infinity.

### 2.3 IsInfinite(x)

Returns `true` iff `x` is +infinity or −infinity.

### 2.4 IsPositiveInfinity(x), IsNegativeInfinity(x)

Return `true` iff `x` is exactly the corresponding infinity.

---

## 3. Basic value operations

### 3.1 AbsoluteValue(x)

Returns $|x|$ with IEEE semantics for NaN/infinities.

### 3.2 CopySign(magnitude, signSource)

Returns a value equal to `AbsoluteValue(magnitude)` with the sign bit taken from `signSource`.

Normative sign-bit behavior:

- If `signSource` is negative zero, the result **MUST** be negative.
- If `signSource` is NaN, the sign bit of that NaN is used (where observable).

### 3.3 Sign(x)

Returns:

- `NotANumber` if `x` is NaN.
- `+1` if `x > 0`.
- `-1` if `x < 0`.
- `0` if `x` is +0 or −0.

---

## 4. Rounding and integral mapping

The following define **rounding direction** and **tie-breaking** unambiguously.

### 4.1 RoundTowardNegativeInfinity(x)

Returns the greatest integer $n$ such that $n \le x$.

### 4.2 RoundTowardPositiveInfinity(x)

Returns the least integer $n$ such that $n \ge x$.

### 4.3 RoundTowardZero(x)

Returns:

- `RoundTowardNegativeInfinity(x)` if $x \ge 0$
- `RoundTowardPositiveInfinity(x)` if $x \le 0$

Equivalently: truncation toward zero.

### 4.4 RoundToNearestTiesToEven(x)

Returns the nearest integer to $x$. If $x$ is exactly halfway between two integers, returns the one with an **even** least significant bit.

### 4.5 RoundToNearestTiesAwayFromZero(x)

Returns the nearest integer to $x$. If $x$ is exactly halfway between two integers, returns the one **farther from zero**.

### 4.6 SplitFractionalAndIntegralParts(x)

Returns a record `{ fractionalPart, integralPart }` such that:

- `integralPart = RoundTowardZero(x)`
- `fractionalPart = x - integralPart`
- `fractionalPart` has the **same sign as `x`** (except that for ±0 it is ±0 accordingly).

### 4.7 FractionalPart(x)

Returns `SplitFractionalAndIntegralParts(x).fractionalPart`.

---

## 5. “Next representable” functions

These are defined in terms of the target’s IEEE 754 representation.

### 5.1 NextRepresentableToward(value, direction)

Returns the unique floating-point number $y$ such that:

- $y$ is representable,
- $y \ne value$,
- $y$ is the nearest representable value to `value` in the direction toward `direction`,
- If `value == direction`, returns `direction`.

Special cases follow IEEE 754 `nextafter`.

### 5.2 NextRepresentableUp(value)

Equivalent to `NextRepresentableToward(value, PositiveInfinity)`.

### 5.3 NextRepresentableDown(value)

Equivalent to `NextRepresentableToward(value, NegativeInfinity)`.

---

## 6. Division families: Quotient, Remainder, Modulus (distinct)

This section is **the** most important for cross-language consistency.

### 6.1 Preconditions

For all functions below, `divisor` must be non-zero. If `divisor == 0`, behavior follows IEEE rules where applicable (infinities/NaN), but for integer types it is an error.

### 6.2 QuotientTowardZero(dividend, divisor)

Returns the integer $q$ such that:

- $q = RoundTowardZero(dividend / divisor)$ for real division,
- and for integer division it matches truncation toward zero.

### 6.3 Remainder(dividend, divisor)

**Remainder is paired with QuotientTowardZero.**

Returns $r$ such that:

- $r = dividend - divisor * QuotientTowardZero(dividend, divisor)$
- $r$ has the **same sign as `dividend`** or is ±0 as appropriate.
- $|r| < |divisor|$ when both are finite reals and $divisor \ne 0$.

This corresponds to the behavior of `%` in many languages under truncating division.

### 6.4 QuotientTowardNegativeInfinity(dividend, divisor)

Returns the integer $q$ such that:

- $q = RoundTowardNegativeInfinity(dividend / divisor)$ for real division.

For integers, this is “floor division”.

### 6.5 Modulus(dividend, divisor)

**Modulus is paired with QuotientTowardNegativeInfinity and is Euclidean-style.**

Define:

- $q = QuotientTowardNegativeInfinity(dividend, divisor)$
- $m = dividend - divisor * q$

Then `Modulus(dividend, divisor) = m`, with the following normative range rule:

If `divisor > 0`, then $m$ **MUST** satisfy:

- $0 \le m < divisor$

If `divisor < 0`, then $m$ **MUST** satisfy:

- $0 \le m < |divisor|$  (range uses the magnitude)

This is the wrap-around modulus suitable for indexing and angle normalization.

### 6.6 QuotientAndRemainderTowardZero(dividend, divisor)

Returns `{ Quotient: QuotientTowardZero(...), Remainder: Remainder(...) }`.

### 6.7 QuotientAndModulus(dividend, divisor)

Returns `{ Quotient: QuotientTowardNegativeInfinity(...), Modulus: Modulus(...) }`.

### 6.8 FloatingRemainder(dividend, divisor)

Returns the IEEE 754 “fmod-style” remainder:

- $r = dividend - divisor * RoundTowardZero(dividend/divisor)$

This is numerically identical to `Remainder` for reals, but is named separately because some targets expose multiple “remainder” variants.

### 6.9 IeeeRemainder(dividend, divisor)

Returns the IEEE 754 “remainder-style” remainder:

- $r = dividend - divisor * n$
- where $n$ is the nearest integer to $dividend/divisor$ (ties to even)

This differs from `FloatingRemainder` and from `%` in many languages.

---

## 7. IsApproximatelyEqual

### 7.1 IsApproximatelyEqual(left, right, absoluteTolerance, relativeTolerance)

Returns `true` iff:

- If either is NaN → `false`.
- If both are exactly equal (including both +∞ or both −∞) → `true`.
- Otherwise, let `difference = AbsoluteValue(left - right)`.
- Return `true` iff:

$difference \le \operatorname{maximum}(absoluteTolerance,\ relativeTolerance * \operatorname{maximum}(AbsoluteValue(left),\ AbsoluteValue(right)))$

Notes:

- This is a symmetric absolute+relative tolerance check.
- `absoluteTolerance` and `relativeTolerance` must be ≥ 0; otherwise error.

---

## 8. Quantiles and percentiles (if you expose Statistics)

If you include quantiles/percentiles in the canonical surface, you must lock an interpolation method.

### 8.1 Quantile(values, probability)

Normative requirements:

- `values` must be non-empty.
- `probability` must satisfy $0 \le probability \le 1$.
- Sort values ascending as $x[0..n-1]$.
- Use **linear interpolation between closest ranks** (a common “Type 7”-like rule):

Let $h = (n - 1) * probability$  
Let $i = \lfloor h \rfloor$ and $f = h - i$  
Return $x[i]$ if $i == n-1$, else $(1 - f) * x[i] + f * x[i+1]$.

### 8.2 Percentile(values, percentile)

Equivalent to `Quantile(values, percentile / 100)` with $0 \le percentile \le 100$.

(If you want a different quantile definition, lock it here and keep it consistent across all targets.)
