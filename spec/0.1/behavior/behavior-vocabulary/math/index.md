Status: NORMATIVE  
Lock State: DRAFT (IEEE 754 alignment in progress)  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary — Math

This specification defines the v0.1 **Math operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines the canonical v0.1 Math surface:

- names are plain-English and MUST NOT use abbreviations
- semantic intent is recorded explicitly (even where v0.1 defers exact numeric accuracy to a conformance suite)
- historically conflated operations are separated (for example, Modulus vs Remainder)

---

## 2. Shared Definitions (Normative)

### 2.1 Evaluation contract

- Each operand is a Behavior expression evaluated to `Validation<Value>`.
- Unless explicitly stated otherwise, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)` (propagation).
- Operators MUST NOT encode failures as `<Absent/>`.

Diagnostic code rule (Normative):

- Where this specification requires an `Invalid(...)` produced by the operator itself (not propagated from an operand), it MUST use the corresponding `Math::...` code defined by Behavior Diagnostic Codes.

### 2.2 Numeric domains

v0.1 numeric domains are defined by Behavior Dialect — Semantics:

- `Integer`
- `Fraction` (rational)
- `PrecisionNumber` (precision-carrying decimal)
- `RealNumber` (approximate real)

Derived domains:

- `OrderableNumber := Integer | Fraction | PrecisionNumber`

### 2.2.1 IEEE 754 RealNumber conformance profile (Normative)

When the active conformance profile declares that `RealNumber` is IEEE 754 (for example, binary64), then the following apply:

- The normative meaning of IEEE-profile operators is defined by:
  - `Canonical Math API Surface — Normative Semantics`
  - the single blessed Codex conformance suite for this surface
- Backend mapping tables and human-readable test-vector appendices are Informative guidance only; they must survive the suite.
- Operators whose meaning depends on representability (for example, `NextRepresentableToward`) MUST follow IEEE 754 semantics for the declared representation.
- Implementations MUST NOT “guess” representation-dependent behavior when the representation contract is absent.

### 2.3 Canonical special values

Where applicable, v0.1 math MUST support canonical special values as Concepts:

- `<NotANumber />`
- `<PositiveInfinity />`
- `<NegativeInfinity />`
- `<NegativeZero />`

Rule:

- `<NegativeZero />` is the only permitted representation of negative zero.

### 2.4 Presence

Unless explicitly stated otherwise, Math operators MUST treat `<Absent/>` as a domain violation and return `Invalid(...)` with code `Math::NEED_PRESENT_NUMBER`.

---

## 3. Constants (Normative)

These are zero-arity operators returning `Validation<RealNumber>`:

- `Pi`
- `Tau`
- `EulerNumber`
- `PositiveInfinity`
- `NegativeInfinity`
- `NotANumber`
- `NegativeZero`

---

## 4. Classification and Comparison (Normative)

All operators in this section return `Validation<boolean>`.

- `IsNotANumber(x)`
- `IsFinite(x)`
- `IsInfinite(x)`
- `IsPositiveInfinity(x)`
- `IsNegativeInfinity(x)`

Optional (recorded as part of the canonical surface; see conformance note below):

- `IsNormal(x)`
- `IsSubnormal(x)`

### 4.1 `IsApproximatelyEqual`

Arity: 4

Domain:

- `IsApproximatelyEqual(left, right, absoluteTolerance, relativeTolerance)`

Semantics (Normative):

1. If either `left` or `right` is `<NotANumber />`, the result MUST be `Valid(false)`.
2. If `left` and `right` are exactly equal (including both `<PositiveInfinity />` or both `<NegativeInfinity />`), the result MUST be `Valid(true)`.
3. If either tolerance is negative, the result MUST be `Invalid(...)` with code `Math::NEED_VALID_RANGE`.
4. Otherwise, let `difference = AbsoluteValue(left - right)` and return `Valid(true)` iff:
  - $difference \le \operatorname{maximum}(absoluteTolerance,\ relativeTolerance \cdot \operatorname{maximum}(AbsoluteValue(left),\ AbsoluteValue(right)))$.

---

## 5. Basic Value Operations (Normative)

- `AbsoluteValue(x)`
- `CopySign(magnitude, signSource)`
- `Sign(x)`
- `Minimum(a, b)`
- `Maximum(a, b)`
- `Clamp(value, minimum, maximum)`
- `FusedMultiplyAdd(multiplicand, multiplier, addend)`

Operator notes (Normative):

- `Minimum` and `Maximum` are defined over `OrderableNumber`.
- `Clamp` returns `Invalid(...)` with code `Math::NEED_VALID_RANGE` when `minimum` is greater than `maximum`.
- `Sign` follows IEEE-profile semantics when applied to `RealNumber`:
  - returns `<NotANumber />` when given `<NotANumber />`
  - returns `+1` for values greater than 0
  - returns `-1` for values less than 0
  - returns `0` for `+0` and `-0`
  - the result is a `RealNumber` value

---

## 6. Rounding and Integral Mapping (Normative)

- `RoundTowardNegativeInfinity(x)`
- `RoundTowardPositiveInfinity(x)`
- `RoundTowardZero(x)`
- `RoundToNearestTiesToEven(x)`
- `RoundToNearestTiesAwayFromZero(x)`
- `SplitFractionalAndIntegralParts(x)`
- `FractionalPart(x)`

`SplitFractionalAndIntegralParts` returns a `Record` with keys:

- `fractionalPart`
- `integralPart`

Normative split rule:

- `integralPart` MUST equal `RoundTowardZero(x)`.
- `fractionalPart` MUST equal `x - integralPart`.
- `fractionalPart` MUST have the same sign as `x` (including `+0` and `-0` behavior).

Neighbor representables (recorded as part of the canonical surface):

- `NextRepresentableToward(value, direction)`
- `NextRepresentableUp(value)`
- `NextRepresentableDown(value)`

Conformance note (Normative):

- In the IEEE 754 RealNumber profile, these operators MUST follow IEEE 754 `nextafter` semantics for the declared representation.
- If the RealNumber representation contract is not supplied, evaluation MUST return `Invalid(...)` with code `Math::REAL_NUMBER_REPRESENTATION_UNSPECIFIED`.

---

## 7. Division, Modulus, and Remainder (Normative)

Integer quotient helpers:

- `QuotientTowardZero(dividend, divisor)`
- `QuotientTowardNegativeInfinity(dividend, divisor)`

Remainder (truncation-quotient remainder):

- `Remainder(dividend, divisor)`

IEEE remainder variants (recorded as part of the canonical surface):

- `FloatingRemainder(dividend, divisor)`
- `IeeeRemainder(dividend, divisor)`

Modulus (Euclidean modulus):

- `Modulus(dividend, divisor)`

Combined:

- `QuotientAndRemainderTowardZero(dividend, divisor)`
- `QuotientAndModulus(dividend, divisor)`

Normative definitions:

- `Remainder(dividend, divisor)` MUST equal:
  - `dividend - divisor * QuotientTowardZero(dividend, divisor)`.
- In the IEEE 754 RealNumber profile, `FloatingRemainder` MUST equal:
  - `dividend - divisor * RoundTowardZero(dividend/divisor)`.
- In the IEEE 754 RealNumber profile, `IeeeRemainder` MUST equal:
  - `dividend - divisor * n`, where `n` is the nearest integer to `dividend/divisor` (ties to even).
- `Modulus(dividend, divisor)` MUST equal:
  - `dividend - divisor * QuotientTowardNegativeInfinity(dividend, divisor)`.
- For integer domains, division by zero MUST return `Invalid(...)` with code `Math::DIVIDE_BY_ZERO`.
- For the IEEE 754 RealNumber profile, divide-by-zero behavior follows IEEE 754 (infinities/NaN as applicable).

---

## 8. Exponentials, Logarithms, Powers, and Roots (Reserved, v0.1 surface)

- `Power(base, exponent)`
- `SquareRoot(x)`
- `CubeRoot(x)`
- `HypotenuseLength(x, y)`
- `HypotenuseLengthThree(x, y, z)`
- `Exponential(x)`
- `ExponentialBaseTwo(x)`
- `ExponentialMinusOne(x)`
- `NaturalLogarithm(x)`
- `BaseTenLogarithm(x)`
- `BaseTwoLogarithm(x)`
- `NaturalLogarithmOfOnePlus(x)`
- `DecomposeIntoSignificandAndExponentBaseTwo(x)`
- `ComposeFromSignificandAndExponentBaseTwo(significand, exponent)`
- `ScaleByPowerOfTwo(x, exponent)`

---

## 9. Trigonometry (Reserved, v0.1 surface)

Radians are the canonical angle unit.

- `Sine(radians)`
- `Cosine(radians)`
- `Tangent(radians)`
- `ArcSine(x)`
- `ArcCosine(x)`
- `ArcTangent(x)`
- `ArcTangentFromCoordinates(y, x)`
- `RadiansFromDegrees(degrees)`
- `DegreesFromRadians(radians)`
- `SineOfPiTimes(x)`
- `CosineOfPiTimes(x)`
- `TangentOfPiTimes(x)`

---

## 10. Hyperbolic Functions (Reserved, v0.1 surface)

- `HyperbolicSine(x)`
- `HyperbolicCosine(x)`
- `HyperbolicTangent(x)`
- `AreaHyperbolicSine(x)`
- `AreaHyperbolicCosine(x)`
- `AreaHyperbolicTangent(x)`

---

## 11. Geometry and Coordinate Helpers (Reserved, v0.1 surface)

- `DistanceBetweenPointsTwo(x1, y1, x2, y2)`
- `DistanceBetweenPointsThree(x1, y1, z1, x2, y2, z2)`
- `LinearInterpolation(start, end, t)`
- `InverseLinearInterpolation(start, end, value)`
- `Remap(value, fromStart, fromEnd, toStart, toEnd)`
- `NormalizeAngleRadians(radians)`
- `NormalizeAngleDegrees(degrees)`

---

## 12. Combinatorics and Discrete Mathematics (Reserved, v0.1 surface)

- `GreatestCommonDivisor(a, b)`
- `LeastCommonMultiple(a, b)`
- `Factorial(n)`
- `BinomialCoefficient(n, k)`
- `PermutationCount(n, k)`
- `IsPrime(n)`
- `PrimeFactorization(n)`

---

## 13. Statistics (Reserved, v0.1 surface)

- `ArithmeticMean(values)`
- `GeometricMean(values)`
- `HarmonicMean(values)`
- `Median(values)`
- `Mode(values)`
- `Range(values)`
- `InterquartileRange(values)`
- `MeanAbsoluteDeviation(values)`
- `MedianAbsoluteDeviation(values)`
- `PopulationVariance(values)`
- `SampleVariance(values)`
- `PopulationStandardDeviation(values)`
- `SampleStandardDeviation(values)`
- `Covariance(valuesX, valuesY)`
- `PearsonCorrelationCoefficient(valuesX, valuesY)`
- `Quantile(values, probability)`
- `Percentile(values, percentile)`

---

## 14. Linear Algebra (Reserved, v0.1 surface)

- `DotProduct(vectorA, vectorB)`
- `CrossProductThree(vectorA, vectorB)`
- `VectorLength(vector)`
- `NormalizeVector(vector)`
- `MatrixMultiply(matrixA, matrixB)`
- `MatrixTranspose(matrix)`
- `MatrixDeterminant(matrix)`
- `MatrixTrace(matrix)`
- `SolveLinearSystem(matrixA, vectorB)`
- `MatrixInverse(matrixA)`
- `EigenDecomposition(matrixA)`

---

## 15. Calculus and Numerical Analysis (Reserved, v0.1 surface)

These names are RESERVED for future versions. v0.1 does not define higher-order function values as operands.

- `NumericalDerivative(function, x)`
- `NumericalGradient(function, point)`
- `NumericalJacobian(function, point)`
- `NumericalHessian(function, point)`
- `NumericalDefiniteIntegral(function, lowerBound, upperBound)`
- `FindRootByBisection(function, lowerBound, upperBound)`
- `FindRootByNewtonMethod(function, initialGuess)`
- `FindRootByBrentMethod(function, lowerBound, upperBound)`
- `MinimizeFunction(function, initialGuess)`

---

## 16. Basic Arithmetic (Normative)

These operators are fully specified in v0.1 because they can be defined using exact rational semantics on `OrderableNumber`.

- `Add(a, b, ...)`
- `Subtract(left, right)`
- `Multiply(a, b, ...)`
- `Divide(dividend, divisor)`

OrderableNumber overloads (Normative):

- Any operand outside `OrderableNumber` MUST return `Invalid(...)` with code `Math::NEED_ORDERABLE_NUMBER`.
- Division by zero MUST return `Invalid(...)` with code `Math::DIVIDE_BY_ZERO`.

IEEE 754 RealNumber overloads (Normative, when the RealNumber profile is IEEE 754):

- `Add`, `Subtract`, `Multiply`, and `Divide` applied to `RealNumber` MUST follow IEEE 754 semantics for the declared representation.
- For these RealNumber overloads, divide-by-zero behavior follows IEEE 754 (infinities/NaN as applicable) rather than producing `Invalid(...)`.

---

## 17. Conformance for Reserved Operators (Normative)

For operators marked “Reserved, v0.1 surface”:

- If the active conformance profile does not define the operator, evaluation MUST return `Invalid(...)` with code `Math::OPERATOR_NOT_SUPPORTED`.

---

**End of Behavior Vocabulary — Math v0.1**
