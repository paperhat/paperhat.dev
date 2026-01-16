Status: INFORMATIVE  
Lock State: DRAFT (candidate for LOCKED)  
Version: 0.1  
Editor: Charles F. Munat

# Canonical Math API Surface — Conformance Appendix

This appendix provides a **human-readable set of test vectors** for cross-language conformance.

This document is **Informative**. The blessed Codex conformance suite is the enforcement mechanism.

Unless otherwise stated, all tests assume IEEE 754 binary64 (`double` / `Float64`).

Conventions used below:

- `0.0` denotes numeric zero.
- `<NegativeZero />` denotes negative zero. Any numeric-literal spelling of negative zero (for example `-0.0`) is forbidden.
- `<NotANumber />` denotes NaN (any NaN payload is acceptable unless sign is tested).
- “Must be negative zero” means the value is `<NegativeZero />`.

---

## A. Classification and special values

### A.1 IsNotANumber

1. `IsNotANumber(<NotANumber />) → true`
2. `IsNotANumber(0.0) → false`
3. `IsNotANumber(<PositiveInfinity />) → false`

### A.2 IsFinite

1. `IsFinite(0.0) → true`
2. `IsFinite(-123.456) → true`
3. `IsFinite(<PositiveInfinity />) → false`
4. `IsFinite(<NegativeInfinity />) → false`
5. `IsFinite(<NotANumber />) → false`

### A.3 IsInfinite

1. `IsInfinite(<PositiveInfinity />) → true`
2. `IsInfinite(<NegativeInfinity />) → true`
3. `IsInfinite(0.0) → false`
4. `IsInfinite(<NotANumber />) → false`

---

## B. CopySign and Sign (including negative zero)

### B.1 CopySign basic

1. `CopySign(2.5, 3.0) → 2.5`
2. `CopySign(2.5, -3.0) → -2.5`
3. `CopySign(-2.5, 3.0) → 2.5`
4. `CopySign(-2.5, -3.0) → -2.5`

### B.2 CopySign with zero sign source

1. `CopySign(2.5, 0.0) → 2.5`
2. `CopySign(2.5, <NegativeZero />) → -2.5`

### B.3 Sign basic

1. `Sign(7.0) → 1`
2. `Sign(-7.0) → -1`
3. `Sign(0.0) → 0`
4. `Sign(<NegativeZero />) → 0`
5. `Sign(<NotANumber />) → <NotANumber />`

---

## C. Rounding: direction and tie-breaking

### C.1 RoundTowardNegativeInfinity

1. `RoundTowardNegativeInfinity( 1.9) → 1`
2. `RoundTowardNegativeInfinity( 1.0) → 1`
3. `RoundTowardNegativeInfinity(-1.0) → -1`
4. `RoundTowardNegativeInfinity(-1.1) → -2`

### C.2 RoundTowardPositiveInfinity

1. `RoundTowardPositiveInfinity( 1.1) → 2`
2. `RoundTowardPositiveInfinity( 1.0) → 1`
3. `RoundTowardPositiveInfinity(-1.0) → -1`
4. `RoundTowardPositiveInfinity(-1.9) → -1`

### C.3 RoundTowardZero

1. `RoundTowardZero( 1.9) → 1`
2. `RoundTowardZero(-1.9) → -1`
3. `RoundTowardZero( 0.0) → 0`
4. `RoundTowardZero(-0.0) → -0`  *(must preserve negative zero if representable)*

### C.4 RoundToNearestTiesToEven

1. `RoundToNearestTiesToEven( 2.5) → 2`  *(2 is even)*
2. `RoundToNearestTiesToEven( 3.5) → 4`  *(4 is even)*
3. `RoundToNearestTiesToEven(-2.5) → -2` *(−2 is even)*
4. `RoundToNearestTiesToEven(-3.5) → -4` *(−4 is even)*
5. `RoundToNearestTiesToEven( 2.5000000000000004) → 3` *(not a tie; nearest is 3)*

### C.5 RoundToNearestTiesAwayFromZero

1. `RoundToNearestTiesAwayFromZero( 2.5) → 3`
2. `RoundToNearestTiesAwayFromZero( 3.5) → 4`
3. `RoundToNearestTiesAwayFromZero(-2.5) → -3`
4. `RoundToNearestTiesAwayFromZero(-3.5) → -4`
5. `RoundToNearestTiesAwayFromZero( 2.49) → 2`
6. `RoundToNearestTiesAwayFromZero(-2.49) → -2`

---

## D. SplitFractionalAndIntegralParts and FractionalPart

### D.1 SplitFractionalAndIntegralParts sign rule

1. `SplitFractionalAndIntegralParts( 3.25) → { fractionalPart:  0.25, integralPart:  3 }`
2. `SplitFractionalAndIntegralParts(-3.25) → { fractionalPart: -0.25, integralPart: -3 }`

### D.2 Zero sign preservation

1. `SplitFractionalAndIntegralParts(+0) → { fractionalPart: +0, integralPart: +0 }`
2. `SplitFractionalAndIntegralParts(-0) → { fractionalPart: -0, integralPart: -0 }`

### D.3 FractionalPart derived

1. `FractionalPart( 5.75) →  0.75`
2. `FractionalPart(-5.75) → -0.75`

---

## E. Remainder vs Modulus (the critical drift tests)

Assume `divisor ≠ 0`.

### E.1 Positive divisor (divisor = 3)

For `dividend = 7`, `divisor = 3`:

- `QuotientTowardZero(7,3) → 2`
- `Remainder(7,3) → 1`
- `QuotientTowardNegativeInfinity(7,3) → 2`
- `Modulus(7,3) → 1`

For `dividend = -7`, `divisor = 3`:

- `QuotientTowardZero(-7,3) → -2`
- `Remainder(-7,3) → -1`
- `QuotientTowardNegativeInfinity(-7,3) → -3`
- `Modulus(-7,3) → 2`  *(must be in 0..2)*

For `dividend = 7`, `divisor = -3` (tests the “magnitude range” rule):

- `QuotientTowardZero(7,-3) → -2`
- `Remainder(7,-3) → 1`
- `QuotientTowardNegativeInfinity(7,-3) → -3`
- `Modulus(7,-3) → 1`  *(range is 0..2)*

For `dividend = -7`, `divisor = -3`:

- `QuotientTowardZero(-7,-3) → 2`
- `Remainder(-7,-3) → -1`
- `QuotientTowardNegativeInfinity(-7,-3) → 2` *(because (-7)/(-3)=2.333…, floor is 2)*
- `Modulus(-7,-3) → 2` *(range is 0..2)*

### E.2 Divisor = 4 (more cases)

1. `Remainder( 9, 4) → 1`
2. `Remainder(-9, 4) → -1`
3. `Modulus( 9, 4) → 1`
4. `Modulus(-9, 4) → 3`

### E.3 Dividend multiple of divisor

1. `Remainder( 8, 4) → 0`
2. `Remainder(-8, 4) → -0` *(must preserve sign where representable)*
3. `Modulus( 8, 4) → 0`
4. `Modulus(-8, 4) → 0`

(Note: some targets lose negative zero for integer types; the negative-zero requirement applies to floating types.)

---

## F. FloatingRemainder vs IeeeRemainder

Use `dividend = 5.5`, `divisor = 2.0`:

- `FloatingRemainder(5.5, 2.0) → 1.5` (since trunc(2.75)=2; 5.5-2*2=1.5)

Use `dividend = 5.0`, `divisor = 2.0`:

- `FloatingRemainder(5.0, 2.0) → 1.0`
- `IeeeRemainder(5.0, 2.0) → 1.0` (nearest integer to 2.5 is 2 (ties to even); 5-2*2=1)

Use `dividend = 7.0`, `divisor = 2.0`:

- `FloatingRemainder(7.0, 2.0) → 1.0` (trunc(3.5)=3; 7-2*3=1)
- `IeeeRemainder(7.0, 2.0) → -1.0` (nearest integer to 3.5 is 4 (ties to even); 7-2*4=-1)

Use `dividend = -7.0`, `divisor = 2.0`:

- `FloatingRemainder(-7.0, 2.0) → -1.0`
- `IeeeRemainder(-7.0, 2.0) → 1.0` (nearest integer to -3.5 is -4; -7 - 2*(-4)=1)

---

## G. Next representable (spot checks)

These tests require that the backend can observe ±0 and step floats by representable increments.

### G.1 Around zero

1. `NextRepresentableUp(+0) → smallest positive subnormal` (if subnormals supported; else smallest positive normal)

2. `NextRepresentableDown(+0) → -0` **or** the largest negative subnormal?

Normative requirement:

- Stepping “down” from +0 MUST produce **-0** if the target distinguishes signed zero.
- The next step down from -0 MUST produce the largest-magnitude negative subnormal.

3. `NextRepresentableUp(-0) → smallest positive subnormal`

4. `NextRepresentableDown(-0) → largest negative subnormal`

(If your target collapses signed zero, you may mark signed-zero tests as “not applicable”, but then you must not claim full IEEE conformance.)

### G.2 Infinity boundaries

1. `NextRepresentableUp(LargestFinite) → PositiveInfinity`
2. `NextRepresentableDown(NegativeInfinity) → LargestNegativeFinite`

### G.3 Directional stepping

Let `x = 1.0`.

1. `NextRepresentableToward(1.0, 2.0) → NextRepresentableUp(1.0)`
2. `NextRepresentableToward(1.0, 0.0) → NextRepresentableDown(1.0)`

---

## H. IsApproximatelyEqual

Use `absoluteTolerance = 1e-12`, `relativeTolerance = 1e-12` unless stated.

### H.1 Exact equalities

1. `IsApproximatelyEqual(1.0, 1.0, 0, 0) → true`
2. `IsApproximatelyEqual(PositiveInfinity, PositiveInfinity, 0, 0) → true`
3. `IsApproximatelyEqual(NegativeInfinity, NegativeInfinity, 0, 0) → true`
4. `IsApproximatelyEqual(PositiveInfinity, NegativeInfinity, 1, 1) → false`
5. `IsApproximatelyEqual(NotANumber, NotANumber, 1, 1) → false`

### H.2 Absolute tolerance dominance near zero

1. `IsApproximatelyEqual(0.0, 1e-13, 1e-12, 1e-12) → true`
2. `IsApproximatelyEqual(0.0, 1e-11, 1e-12, 1e-12) → false`

### H.3 Relative tolerance dominance at scale

1. `IsApproximatelyEqual(1e12, 1e12 + 1e0, 1e-12, 1e-12) → true`
   (difference is 1; relative bound is 1e-12 * 1e12 = 1)

2. `IsApproximatelyEqual(1e12, 1e12 + 2e0, 1e-12, 1e-12) → false`
   (difference is 2; relative bound is 1)

---

## I. Quantile / Percentile (if included)

Using the locked rule from the semantics document:

- Sort ascending.
- $h = (n - 1) * probability$
- linear interpolation between $x[i]$ and $x[i+1]$

Let `values = [0, 10, 20, 30]` (already sorted), `n=4`.

### I.1 Quantile

1. `Quantile(values, 0.0) → 0`
2. `Quantile(values, 1.0) → 30`
3. `Quantile(values, 0.5) → 15`
   (`h=3*0.5=1.5`, between 10 and 20)
4. `Quantile(values, 0.25) → 7.5`
   (`h=0.75`, between 0 and 10)
5. `Quantile(values, 2/3) → 20`
   (`h=2.0`, exactly x[2])

### I.2 Percentile

1. `Percentile(values, 0) → 0`
2. `Percentile(values, 50) → 15`
3. `Percentile(values, 100) → 30`

---

## J. Angle normalization (if you implement NormalizeAngle*)

These tests assume:

- `NormalizeAngleRadians(r) = Modulus(r, Tau)` (range [0, Tau))
- `NormalizeAngleDegrees(d) = Modulus(d, 360)` (range [0, 360))

### J.1 Radians

1. `NormalizeAngleRadians(0) → 0`
2. `NormalizeAngleRadians(Tau) → 0`
3. `NormalizeAngleRadians(-Pi/2) → Tau - Pi/2`

### J.2 Degrees

1. `NormalizeAngleDegrees(0) → 0`
2. `NormalizeAngleDegrees(360) → 0`
3. `NormalizeAngleDegrees(-90) → 270`

---

## Implementation note (Informative)

To make these tests runnable across languages, represent expected results using:

- exact integers where possible,
- signed-zero checks via bit inspection,
- approximate comparisons for transcendental outputs using `IsApproximatelyEqual`.

This appendix is the canonical machine-readable source for these vectors in v0.1.

### Ontology and reasoning (Informative)

If you want conformance results to support practical querying and reasoning, model test intent, applicability, backend capability, mapping claims, and execution outcomes as Concepts + Traits that compile into triples. See `Conformance Suite Ontology and Reasoning`.

### Authority and assertions (Normative)

The authority boundary for suites (suite vs prose) and the required “expected outcome” assertion forms are defined by `Conformance Suite Authority and Expected Assertions`.
