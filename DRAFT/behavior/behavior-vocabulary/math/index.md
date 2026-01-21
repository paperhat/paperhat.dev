Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Vocabulary — Math

This specification defines the **Math operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines comprehensive mathematical operations for Behavior Programs, including:

- Basic arithmetic
- Complex and imaginary number operations
- Rounding and precision
- Exponentials, logarithms, and powers
- Trigonometry and hyperbolic functions
- Linear algebra
- Statistics
- Combinatorics
- Calculus operations

All operators are fully specified and implemented.

---

## 2. Shared Definitions (Normative)

### 2.1 Evaluation Contract

- Each operand is a Behavior expression evaluated to `Validation<Value>`.
- Unless explicitly stated otherwise, if any required operand evaluates to `Invalid(...)`, the operator result MUST be `Invalid(...)` (propagation).
- Operators MUST NOT encode failures as `<Absent/>`.

Diagnostic code rule:
- Where this specification requires an `Invalid(...)` produced by the operator itself, it MUST use the corresponding `Math::...` code defined by Behavior Diagnostic Codes.

### 2.2 Numeric Domains

As defined by Behavior Dialect Semantics:

- `Integer` — exact integer values (unbounded)
- `Fraction` — exact rational numbers
- `PrecisionNumber` — decimal with explicit precision
- `RealNumber` — approximate real (IEEE 754)
- `Imaginary` — pure imaginary numbers
- `Complex` — complex numbers

Derived domains:
- `OrderableNumber` := `Integer` | `Fraction` | `PrecisionNumber`
- `ExactNumber` := `Integer` | `Fraction`
- `AnyRealNumber` := `Integer` | `Fraction` | `PrecisionNumber` | `RealNumber`
- `AnyNumber` := `AnyRealNumber` | `Imaginary` | `Complex`

### 2.3 Special Values

- `PositiveInfinity`
- `NegativeInfinity`
- `NotANumber`
- `NegativeZero`

### 2.4 Presence

Unless explicitly stated otherwise, Math operators MUST treat `<Absent/>` as a domain violation and return `Invalid(...)` with code `Math::NEED_PRESENT_NUMBER`.

### 2.5 Numeric Promotion

When operators accept mixed numeric domains:

1. `Integer` + `Fraction` -> `Fraction`
2. `Integer` + `PrecisionNumber` -> `PrecisionNumber`
3. `Fraction` + `PrecisionNumber` -> `PrecisionNumber`
4. Any exact type + `RealNumber` -> `RealNumber`
5. Any real type + `Imaginary` -> `Complex`
6. Any real type + `Complex` -> `Complex`

---

## 3. Mathematical Constants (Normative)

Zero-arity operators returning constant values.

### 3.1 Real Constants

| Operator | Returns | Value |
|----------|---------|-------|
| `Pi` | `RealNumber` | π ≈ 3.14159265358979... |
| `Tau` | `RealNumber` | τ = 2π ≈ 6.28318530717958... |
| `EulerNumber` | `RealNumber` | e ≈ 2.71828182845904... |
| `GoldenRatio` | `RealNumber` | φ ≈ 1.61803398874989... |

### 3.2 Special Values

| Operator | Returns |
|----------|---------|
| `PositiveInfinity` | `PositiveInfinity` |
| `NegativeInfinity` | `NegativeInfinity` |
| `NotANumber` | `NotANumber` |
| `NegativeZero` | `NegativeZero` |

### 3.3 Complex Constants

| Operator | Returns | Value |
|----------|---------|-------|
| `ImaginaryUnit` | `Imaginary` | i (√-1) |

---

## 4. Basic Arithmetic (Normative)

### 4.1 `Add`

Arity: 2 or more

Domain: `AnyNumber`

```
Add(a, b, ...) -> AnyNumber
```

Semantics:
- Returns the sum of all operands.
- Result domain follows promotion rules.

### 4.2 `Subtract`

Arity: 2

Domain: `AnyNumber`

```
Subtract(left, right) -> AnyNumber
```

Semantics:
- Returns `left - right`.

### 4.3 `Multiply`

Arity: 2 or more

Domain: `AnyNumber`

```
Multiply(a, b, ...) -> AnyNumber
```

Semantics:
- Returns the product of all operands.
- Result domain follows promotion rules.

### 4.4 `Divide`

Arity: 2

Domain: `AnyNumber`

```
Divide(dividend, divisor) -> AnyNumber
```

Semantics:
- Returns `dividend / divisor`.

Error behavior:
- Division by zero: For exact types, return `Invalid(...)` with code `Math::DIVIDE_BY_ZERO`.
- For RealNumber: follows IEEE 754 (returns infinity or NaN as appropriate).

### 4.5 `Negate`

Arity: 1

Domain: `AnyNumber`

```
Negate(x) -> AnyNumber
```

Semantics:
- Returns `-x`.

### 4.6 `Reciprocal`

Arity: 1

Domain: `AnyNumber`

```
Reciprocal(x) -> AnyNumber
```

Semantics:
- Returns `1/x`.

Error behavior:
- If x is zero: return `Invalid(...)` with code `Math::DIVIDE_BY_ZERO`.

---

## 5. Integer Arithmetic (Normative)

### 5.1 `QuotientTowardZero`

Arity: 2

Domain: `Integer`

```
QuotientTowardZero(dividend, divisor) -> Integer
```

Semantics:
- Integer division truncated toward zero.

### 5.2 `QuotientTowardNegativeInfinity`

Arity: 2

Domain: `Integer`

```
QuotientTowardNegativeInfinity(dividend, divisor) -> Integer
```

Semantics:
- Integer division truncated toward negative infinity (floor division).

### 5.3 `Remainder`

Arity: 2

Domain: `Integer`

```
Remainder(dividend, divisor) -> Integer
```

Semantics:
- Returns `dividend - divisor * QuotientTowardZero(dividend, divisor)`.
- Sign follows the dividend.

### 5.4 `Modulus`

Arity: 2

Domain: `Integer`

```
Modulus(dividend, divisor) -> Integer
```

Semantics:
- Euclidean modulus: `dividend - divisor * QuotientTowardNegativeInfinity(dividend, divisor)`.
- Result is always non-negative when divisor is positive.

### 5.5 `QuotientAndRemainder`

Arity: 2

Domain: `Integer`

```
QuotientAndRemainder(dividend, divisor) -> Tuple(Integer, Integer)
```

Semantics:
- Returns `(quotient, remainder)` using truncation toward zero.

### 5.6 `QuotientAndModulus`

Arity: 2

Domain: `Integer`

```
QuotientAndModulus(dividend, divisor) -> Tuple(Integer, Integer)
```

Semantics:
- Returns `(quotient, modulus)` using floor division.

---

## 6. Complex Number Operations (Normative)

### 6.1 `MakeComplex`

Arity: 2

Domain: `AnyRealNumber`, `AnyRealNumber`

```
MakeComplex(real, imaginary) -> Complex
```

Semantics:
- Constructs a complex number from real and imaginary parts.

### 6.2 `MakeImaginary`

Arity: 1

Domain: `AnyRealNumber`

```
MakeImaginary(coefficient) -> Imaginary
```

Semantics:
- Constructs a pure imaginary number.

### 6.3 `RealPart`

Arity: 1

Domain: `Complex` | `Imaginary` | `AnyRealNumber`

```
RealPart(z) -> AnyRealNumber
```

Semantics:
- Returns the real part.
- For `Imaginary`, returns 0.
- For real numbers, returns the value itself.

### 6.4 `ImaginaryPart`

Arity: 1

Domain: `Complex` | `Imaginary` | `AnyRealNumber`

```
ImaginaryPart(z) -> AnyRealNumber
```

Semantics:
- Returns the imaginary coefficient.
- For real numbers, returns 0.

### 6.5 `Conjugate`

Arity: 1

Domain: `Complex` | `Imaginary`

```
Conjugate(z) -> Complex | Imaginary
```

Semantics:
- Returns the complex conjugate (negates imaginary part).

### 6.6 `Magnitude`

Arity: 1

Domain: `Complex` | `Imaginary` | `AnyRealNumber`

```
Magnitude(z) -> RealNumber
```

Semantics:
- Returns |z| = √(real² + imaginary²).
- For real numbers, returns absolute value.

### 6.7 `Phase`

Arity: 1

Domain: `Complex` | `Imaginary`

```
Phase(z) -> RealNumber
```

Semantics:
- Returns the argument (angle) in radians, range (-π, π].

### 6.8 `MakeComplexFromPolar`

Arity: 2

Domain: `AnyRealNumber`, `AnyRealNumber`

```
MakeComplexFromPolar(magnitude, phase) -> Complex
```

Semantics:
- Constructs a complex number from polar form.
- `real = magnitude * cos(phase)`
- `imaginary = magnitude * sin(phase)`

---

## 7. Value Operations (Normative)

### 7.1 `AbsoluteValue`

Arity: 1

Domain: `AnyRealNumber`

```
AbsoluteValue(x) -> AnyRealNumber
```

Semantics:
- Returns |x|.

### 7.2 `Sign`

Arity: 1

Domain: `AnyRealNumber`

```
Sign(x) -> Integer
```

Semantics:
- Returns -1 if x < 0, 0 if x = 0, 1 if x > 0.
- For NaN, returns NaN.

### 7.3 `CopySign`

Arity: 2

Domain: `AnyRealNumber`

```
CopySign(magnitude, signSource) -> AnyRealNumber
```

Semantics:
- Returns a value with the magnitude of the first operand and the sign of the second.

### 7.4 `Minimum`

Arity: 2 or more

Domain: `OrderableNumber`

```
Minimum(a, b, ...) -> OrderableNumber
```

Semantics:
- Returns the smallest value.

### 7.5 `Maximum`

Arity: 2 or more

Domain: `OrderableNumber`

```
Maximum(a, b, ...) -> OrderableNumber
```

Semantics:
- Returns the largest value.

### 7.6 `Clamp`

Arity: 3

Domain: `OrderableNumber`

```
Clamp(value, minimum, maximum) -> OrderableNumber
```

Semantics:
- Returns value constrained to [minimum, maximum].

Error behavior:
- If minimum > maximum, return `Invalid(...)` with code `Math::NEED_VALID_RANGE`.

---

## 8. Rounding Operations (Normative)

### 8.1 `RoundTowardNegativeInfinity`

Arity: 1

Domain: `AnyRealNumber`

```
RoundTowardNegativeInfinity(x) -> Integer
```

Semantics:
- Floor function. Returns the largest integer ≤ x.

### 8.2 `RoundTowardPositiveInfinity`

Arity: 1

Domain: `AnyRealNumber`

```
RoundTowardPositiveInfinity(x) -> Integer
```

Semantics:
- Ceiling function. Returns the smallest integer ≥ x.

### 8.3 `RoundTowardZero`

Arity: 1

Domain: `AnyRealNumber`

```
RoundTowardZero(x) -> Integer
```

Semantics:
- Truncation. Removes fractional part toward zero.

### 8.4 `RoundToNearestTiesToEven`

Arity: 1

Domain: `AnyRealNumber`

```
RoundToNearestTiesToEven(x) -> Integer
```

Semantics:
- Banker's rounding. Ties go to nearest even integer.

### 8.5 `RoundToNearestTiesAwayFromZero`

Arity: 1

Domain: `AnyRealNumber`

```
RoundToNearestTiesAwayFromZero(x) -> Integer
```

Semantics:
- Standard rounding. Ties go away from zero.

### 8.6 `RoundToDecimalPlaces`

Arity: 2

Domain: `AnyRealNumber`, `Integer`

```
RoundToDecimalPlaces(x, places) -> PrecisionNumber
```

Semantics:
- Rounds to specified decimal places using ties-to-even.

### 8.7 `RoundToSignificantFigures`

Arity: 2

Domain: `AnyRealNumber`, `Integer`

```
RoundToSignificantFigures(x, figures) -> PrecisionNumber
```

Semantics:
- Rounds to specified significant figures.

### 8.8 `FractionalPart`

Arity: 1

Domain: `AnyRealNumber`

```
FractionalPart(x) -> AnyRealNumber
```

Semantics:
- Returns `x - RoundTowardZero(x)`.
- Sign matches the input.

### 8.9 `SplitFractionalAndIntegralParts`

Arity: 1

Domain: `AnyRealNumber`

```
SplitFractionalAndIntegralParts(x) -> Record { integralPart, fractionalPart }
```

Semantics:
- Returns both parts as a record.

---

## 9. Powers, Roots, and Exponentials (Normative)

### 9.1 `Power`

Arity: 2

Domain: `AnyNumber`, `AnyNumber`

```
Power(base, exponent) -> AnyNumber
```

Semantics:
- Returns base^exponent.
- Handles complex results (e.g., negative base with fractional exponent).

### 9.2 `SquareRoot`

Arity: 1

Domain: `AnyNumber`

```
SquareRoot(x) -> AnyNumber
```

Semantics:
- Returns √x.
- For negative real numbers, returns an Imaginary result.

### 9.3 `CubeRoot`

Arity: 1

Domain: `AnyRealNumber`

```
CubeRoot(x) -> AnyRealNumber
```

Semantics:
- Returns the real cube root.

### 9.4 `NthRoot`

Arity: 2

Domain: `AnyNumber`, `Integer`

```
NthRoot(x, n) -> AnyNumber
```

Semantics:
- Returns the nth root.

### 9.5 `Exponential`

Arity: 1

Domain: `AnyNumber`

```
Exponential(x) -> AnyNumber
```

Semantics:
- Returns e^x.

### 9.6 `ExponentialMinusOne`

Arity: 1

Domain: `AnyNumber`

```
ExponentialMinusOne(x) -> AnyNumber
```

Semantics:
- Returns e^x - 1 with higher precision for small x.

### 9.7 `ExponentialBaseTwo`

Arity: 1

Domain: `AnyRealNumber`

```
ExponentialBaseTwo(x) -> RealNumber
```

Semantics:
- Returns 2^x.

### 9.8 `ExponentialBaseTen`

Arity: 1

Domain: `AnyRealNumber`

```
ExponentialBaseTen(x) -> RealNumber
```

Semantics:
- Returns 10^x.

### 9.9 `NaturalLogarithm`

Arity: 1

Domain: `AnyNumber`

```
NaturalLogarithm(x) -> AnyNumber
```

Semantics:
- Returns ln(x).
- For negative real numbers, returns a Complex result.

### 9.10 `NaturalLogarithmOfOnePlus`

Arity: 1

Domain: `AnyNumber`

```
NaturalLogarithmOfOnePlus(x) -> AnyNumber
```

Semantics:
- Returns ln(1 + x) with higher precision for small x.

### 9.11 `BaseTwoLogarithm`

Arity: 1

Domain: `AnyRealNumber`

```
BaseTwoLogarithm(x) -> RealNumber
```

Semantics:
- Returns log₂(x).

### 9.12 `BaseTenLogarithm`

Arity: 1

Domain: `AnyRealNumber`

```
BaseTenLogarithm(x) -> RealNumber
```

Semantics:
- Returns log₁₀(x).

### 9.13 `Logarithm`

Arity: 2

Domain: `AnyNumber`, `AnyNumber`

```
Logarithm(x, base) -> AnyNumber
```

Semantics:
- Returns log_base(x).

### 9.14 `HypotenuseLength`

Arity: 2

Domain: `AnyRealNumber`

```
HypotenuseLength(x, y) -> RealNumber
```

Semantics:
- Returns √(x² + y²) without intermediate overflow.

### 9.15 `HypotenuseLengthThree`

Arity: 3

Domain: `AnyRealNumber`

```
HypotenuseLengthThree(x, y, z) -> RealNumber
```

Semantics:
- Returns √(x² + y² + z²).

---

## 10. Trigonometry (Normative)

All angles are in radians unless otherwise specified.

### 10.1 Basic Trigonometric Functions

| Operator | Arity | Domain | Returns |
|----------|-------|--------|---------|
| `Sine` | 1 | `AnyNumber` | `AnyNumber` |
| `Cosine` | 1 | `AnyNumber` | `AnyNumber` |
| `Tangent` | 1 | `AnyNumber` | `AnyNumber` |
| `Secant` | 1 | `AnyNumber` | `AnyNumber` |
| `Cosecant` | 1 | `AnyNumber` | `AnyNumber` |
| `Cotangent` | 1 | `AnyNumber` | `AnyNumber` |

### 10.2 Inverse Trigonometric Functions

| Operator | Arity | Domain | Returns |
|----------|-------|--------|---------|
| `ArcSine` | 1 | `AnyNumber` | `AnyNumber` |
| `ArcCosine` | 1 | `AnyNumber` | `AnyNumber` |
| `ArcTangent` | 1 | `AnyNumber` | `AnyNumber` |
| `ArcTangentFromCoordinates` | 2 | `AnyRealNumber` | `RealNumber` |
| `ArcSecant` | 1 | `AnyNumber` | `AnyNumber` |
| `ArcCosecant` | 1 | `AnyNumber` | `AnyNumber` |
| `ArcCotangent` | 1 | `AnyNumber` | `AnyNumber` |

`ArcTangentFromCoordinates(y, x)` returns atan2(y, x) in range (-π, π].

### 10.3 Angle Conversion

| Operator | Arity | Semantics |
|----------|-------|-----------|
| `RadiansFromDegrees` | 1 | degrees × (π/180) |
| `DegreesFromRadians` | 1 | radians × (180/π) |
| `RadiansFromGradians` | 1 | gradians × (π/200) |
| `GradiansFromRadians` | 1 | radians × (200/π) |

### 10.4 Pi-Multiple Functions

| Operator | Semantics |
|----------|-----------|
| `SineOfPiTimes(x)` | sin(πx) with higher precision |
| `CosineOfPiTimes(x)` | cos(πx) with higher precision |
| `TangentOfPiTimes(x)` | tan(πx) with higher precision |

---

## 11. Hyperbolic Functions (Normative)

### 11.1 Basic Hyperbolic Functions

| Operator | Arity | Domain | Returns |
|----------|-------|--------|---------|
| `HyperbolicSine` | 1 | `AnyNumber` | `AnyNumber` |
| `HyperbolicCosine` | 1 | `AnyNumber` | `AnyNumber` |
| `HyperbolicTangent` | 1 | `AnyNumber` | `AnyNumber` |
| `HyperbolicSecant` | 1 | `AnyNumber` | `AnyNumber` |
| `HyperbolicCosecant` | 1 | `AnyNumber` | `AnyNumber` |
| `HyperbolicCotangent` | 1 | `AnyNumber` | `AnyNumber` |

### 11.2 Inverse Hyperbolic Functions

| Operator | Arity | Domain | Returns |
|----------|-------|--------|---------|
| `AreaHyperbolicSine` | 1 | `AnyNumber` | `AnyNumber` |
| `AreaHyperbolicCosine` | 1 | `AnyNumber` | `AnyNumber` |
| `AreaHyperbolicTangent` | 1 | `AnyNumber` | `AnyNumber` |
| `AreaHyperbolicSecant` | 1 | `AnyNumber` | `AnyNumber` |
| `AreaHyperbolicCosecant` | 1 | `AnyNumber` | `AnyNumber` |
| `AreaHyperbolicCotangent` | 1 | `AnyNumber` | `AnyNumber` |

---

## 12. Statistics (Normative)

All statistical operators take a List of numbers.

### 12.1 Central Tendency

| Operator | Semantics |
|----------|-----------|
| `ArithmeticMean(values)` | Sum / count |
| `GeometricMean(values)` | nth root of product |
| `HarmonicMean(values)` | n / sum of reciprocals |
| `Median(values)` | Middle value (average of two if even count) |
| `Mode(values)` | Most frequent value(s) — returns List |
| `WeightedMean(values, weights)` | Weighted average |

### 12.2 Dispersion

| Operator | Semantics |
|----------|-----------|
| `Range(values)` | max - min |
| `InterquartileRange(values)` | Q3 - Q1 |
| `PopulationVariance(values)` | Σ(x - μ)² / n |
| `SampleVariance(values)` | Σ(x - μ)² / (n-1) |
| `PopulationStandardDeviation(values)` | √(PopulationVariance) |
| `SampleStandardDeviation(values)` | √(SampleVariance) |
| `MeanAbsoluteDeviation(values)` | Σ|x - μ| / n |
| `MedianAbsoluteDeviation(values)` | Median of |x - median| |
| `CoefficientOfVariation(values)` | σ / μ |

### 12.3 Distribution Shape

| Operator | Semantics |
|----------|-----------|
| `Skewness(values)` | Third standardized moment |
| `Kurtosis(values)` | Fourth standardized moment |
| `ExcessKurtosis(values)` | Kurtosis - 3 |

### 12.4 Position

| Operator | Semantics |
|----------|-----------|
| `Quantile(values, p)` | Value at proportion p (0 to 1) |
| `Percentile(values, p)` | Value at percentile p (0 to 100) |
| `Quartile(values, q)` | Q1, Q2, Q3 (q = 1, 2, or 3) |
| `Decile(values, d)` | Value at decile d (1 to 10) |

### 12.5 Correlation and Regression

| Operator | Semantics |
|----------|-----------|
| `Covariance(valuesX, valuesY)` | Population covariance |
| `SampleCovariance(valuesX, valuesY)` | Sample covariance |
| `PearsonCorrelation(valuesX, valuesY)` | Pearson r |
| `SpearmanCorrelation(valuesX, valuesY)` | Spearman rank correlation |
| `LinearRegression(valuesX, valuesY)` | Returns Record { slope, intercept, r } |

---

## 13. Combinatorics (Normative)

### 13.1 Basic Combinatorics

| Operator | Semantics |
|----------|-----------|
| `Factorial(n)` | n! |
| `DoubleFactorial(n)` | n!! |
| `BinomialCoefficient(n, k)` | "n choose k" |
| `PermutationCount(n, k)` | n! / (n-k)! |
| `MultisetCoefficient(n, k)` | (n+k-1) choose k |

### 13.2 Number Theory

| Operator | Semantics |
|----------|-----------|
| `GreatestCommonDivisor(a, b)` | GCD |
| `LeastCommonMultiple(a, b)` | LCM |
| `ExtendedGcd(a, b)` | Returns Record { gcd, x, y } where ax + by = gcd |
| `IsPrime(n)` | Boolean |
| `PrimeFactorization(n)` | List of prime factors with multiplicities |
| `NextPrime(n)` | Smallest prime > n |
| `PreviousPrime(n)` | Largest prime < n |
| `EulerTotient(n)` | φ(n) |
| `DivisorCount(n)` | Number of divisors |
| `DivisorSum(n)` | Sum of divisors |
| `Divisors(n)` | List of all divisors |
| `ModularExponentiation(base, exp, mod)` | base^exp mod mod |
| `ModularInverse(a, mod)` | Multiplicative inverse mod mod |

---

## 14. Linear Algebra (Normative)

Vectors are represented as Lists of numbers.
Matrices are represented as Lists of Lists (row-major).

### 14.1 Vector Operations

| Operator | Semantics |
|----------|-----------|
| `DotProduct(a, b)` | Σ(aᵢ × bᵢ) |
| `CrossProduct(a, b)` | 3D cross product |
| `VectorLength(v)` | Euclidean norm |
| `VectorLengthSquared(v)` | Sum of squares |
| `NormalizeVector(v)` | v / |v| |
| `VectorAngle(a, b)` | Angle between vectors in radians |
| `VectorProjection(a, onto)` | Projection of a onto b |
| `ScalarProjection(a, onto)` | Scalar projection |

### 14.2 Matrix Operations

| Operator | Semantics |
|----------|-----------|
| `MatrixAdd(a, b)` | Element-wise addition |
| `MatrixSubtract(a, b)` | Element-wise subtraction |
| `MatrixMultiply(a, b)` | Matrix multiplication |
| `MatrixScalarMultiply(m, s)` | Multiply by scalar |
| `MatrixTranspose(m)` | Transpose |
| `MatrixDeterminant(m)` | Determinant |
| `MatrixTrace(m)` | Sum of diagonal |
| `MatrixInverse(m)` | Inverse (if exists) |
| `MatrixRank(m)` | Rank |
| `MatrixNullity(m)` | Dimension of null space |

### 14.3 Matrix Decomposition

| Operator | Semantics |
|----------|-----------|
| `LuDecomposition(m)` | Returns Record { L, U, P } |
| `QrDecomposition(m)` | Returns Record { Q, R } |
| `CholeskyDecomposition(m)` | Returns lower triangular L |
| `SingularValueDecomposition(m)` | Returns Record { U, S, V } |
| `EigenDecomposition(m)` | Returns Record { values, vectors } |

### 14.4 Linear Systems

| Operator | Semantics |
|----------|-----------|
| `SolveLinearSystem(A, b)` | Solve Ax = b |
| `LeastSquaresSolution(A, b)` | Least squares solution |

### 14.5 Matrix Creation

| Operator | Semantics |
|----------|-----------|
| `IdentityMatrix(n)` | n×n identity |
| `ZeroMatrix(rows, cols)` | Matrix of zeros |
| `DiagonalMatrix(values)` | Diagonal from list |

---

## 15. Calculus (Normative)

These operators perform numerical differentiation and integration.

### 15.1 Differentiation

| Operator | Semantics |
|----------|-----------|
| `NumericalDerivative(f, x)` | df/dx at point x |
| `NumericalDerivativeSecond(f, x)` | d²f/dx² at point x |
| `NumericalPartialDerivative(f, point, variableIndex)` | Partial derivative |
| `NumericalGradient(f, point)` | Gradient vector |
| `NumericalJacobian(f, point)` | Jacobian matrix |
| `NumericalHessian(f, point)` | Hessian matrix |

Note: `f` is a Behavior expression where `Argument` is the input.

### 15.2 Integration

| Operator | Semantics |
|----------|-----------|
| `NumericalIntegral(f, lower, upper)` | Definite integral |
| `NumericalIntegralAdaptive(f, lower, upper, tolerance)` | Adaptive quadrature |

### 15.3 Root Finding

| Operator | Semantics |
|----------|-----------|
| `FindRootBisection(f, lower, upper)` | Bisection method |
| `FindRootNewton(f, initialGuess)` | Newton's method |
| `FindRootSecant(f, x0, x1)` | Secant method |
| `FindRootBrent(f, lower, upper)` | Brent's method |

### 15.4 Optimization

| Operator | Semantics |
|----------|-----------|
| `FindMinimumGoldenSection(f, lower, upper)` | Golden section search |
| `FindMinimumBrent(f, lower, upper)` | Brent's method for minimum |
| `FindMinimumGradientDescent(f, initialPoint, learningRate, iterations)` | Gradient descent |

---

## 16. Special Functions (Normative)

### 16.1 Gamma and Related

| Operator | Semantics |
|----------|-----------|
| `Gamma(x)` | Γ(x) |
| `LogGamma(x)` | ln(Γ(x)) |
| `Digamma(x)` | ψ(x) = d/dx ln(Γ(x)) |
| `Beta(a, b)` | B(a,b) = Γ(a)Γ(b)/Γ(a+b) |
| `IncompleteBeta(x, a, b)` | Incomplete beta function |
| `IncompleteGamma(a, x)` | Incomplete gamma function |

### 16.2 Error Functions

| Operator | Semantics |
|----------|-----------|
| `ErrorFunction(x)` | erf(x) |
| `ComplementaryErrorFunction(x)` | erfc(x) = 1 - erf(x) |
| `InverseErrorFunction(x)` | erf⁻¹(x) |

### 16.3 Bessel Functions

| Operator | Semantics |
|----------|-----------|
| `BesselJ(n, x)` | Bessel function of first kind |
| `BesselY(n, x)` | Bessel function of second kind |
| `BesselI(n, x)` | Modified Bessel first kind |
| `BesselK(n, x)` | Modified Bessel second kind |

---

## 17. Interpolation (Normative)

| Operator | Semantics |
|----------|-----------|
| `LinearInterpolation(start, end, t)` | start + t × (end - start) |
| `InverseLinearInterpolation(start, end, value)` | (value - start) / (end - start) |
| `Remap(value, fromStart, fromEnd, toStart, toEnd)` | Map from one range to another |
| `CubicInterpolation(p0, p1, p2, p3, t)` | Catmull-Rom spline |
| `LagrangeInterpolation(points, x)` | Lagrange polynomial |
| `SplineInterpolation(points, x)` | Cubic spline |

---

## 18. Geometry (Normative)

### 18.1 2D Geometry

| Operator | Semantics |
|----------|-----------|
| `DistanceBetweenPoints2D(x1, y1, x2, y2)` | Euclidean distance |
| `MidpointBetweenPoints2D(x1, y1, x2, y2)` | Returns Tuple(x, y) |
| `AngleBetweenPoints2D(x1, y1, x2, y2)` | Angle in radians |
| `RotatePoint2D(x, y, angle)` | Rotate around origin |
| `RotatePointAround2D(x, y, cx, cy, angle)` | Rotate around point |

### 18.2 3D Geometry

| Operator | Semantics |
|----------|-----------|
| `DistanceBetweenPoints3D(x1, y1, z1, x2, y2, z2)` | Euclidean distance |
| `MidpointBetweenPoints3D(...)` | Returns Tuple(x, y, z) |

### 18.3 Angle Normalization

| Operator | Semantics |
|----------|-----------|
| `NormalizeAngleRadians(radians)` | Normalize to [0, 2π) |
| `NormalizeAngleRadiansSigned(radians)` | Normalize to (-π, π] |
| `NormalizeAngleDegrees(degrees)` | Normalize to [0, 360) |
| `NormalizeAngleDegreesSigned(degrees)` | Normalize to (-180, 180] |

---

## 19. Classification (Normative)

| Operator | Returns | Semantics |
|----------|---------|-----------|
| `IsNotANumber(x)` | Boolean | True if NaN |
| `IsFinite(x)` | Boolean | True if finite |
| `IsInfinite(x)` | Boolean | True if ±∞ |
| `IsPositiveInfinity(x)` | Boolean | True if +∞ |
| `IsNegativeInfinity(x)` | Boolean | True if -∞ |
| `IsPositive(x)` | Boolean | True if x > 0 |
| `IsNegative(x)` | Boolean | True if x < 0 |
| `IsZero(x)` | Boolean | True if x = 0 |
| `IsEven(x)` | Boolean | True if integer and even |
| `IsOdd(x)` | Boolean | True if integer and odd |
| `IsInteger(x)` | Boolean | True if integral value |
| `IsRational(x)` | Boolean | True if representable as fraction |

---

## 20. Conversion (Normative)

| Operator | Semantics |
|----------|-----------|
| `ConvertToInteger(x)` | Convert to Integer (must be integral) |
| `ConvertToFraction(x)` | Convert to Fraction |
| `ConvertToPrecisionNumber(x, precision)` | Convert with specified precision |
| `ConvertToRealNumber(x)` | Convert to RealNumber |
| `ConvertToComplex(x)` | Convert real to Complex |

Error behavior:
- `ConvertToInteger` on non-integral value: `Invalid(...)` with code `Math::NOT_INTEGRAL`.

---

## 21. IEEE 754 Specific (Normative)

For RealNumber with IEEE 754 profile:

| Operator | Semantics |
|----------|-----------|
| `NextRepresentableUp(x)` | Next larger representable value |
| `NextRepresentableDown(x)` | Next smaller representable value |
| `NextRepresentableToward(x, direction)` | Next representable toward direction |
| `IsNormal(x)` | True if normal (not subnormal) |
| `IsSubnormal(x)` | True if subnormal |
| `FusedMultiplyAdd(a, b, c)` | a×b + c with single rounding |
| `IsApproximatelyEqual(a, b, absTol, relTol)` | Approximate equality |

---

**End of Behavior Vocabulary — Math v0.1**
