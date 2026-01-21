Status: INFORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Canonical Math API Surface — Backend Mapping Specification

This document records **how each canonical function maps to major target language standard libraries**, and how to emulate it when not available.

This document is **Informative**.

When this document uses requirements language (for example, MUST), it is describing constraints imposed by the Normative semantics and the blessed Codex conformance suite.

Legend:

- **Direct**: call exists and matches semantics.
- **Direct (verify)**: call exists but has known semantic traps; must validate against normative semantics.
- **Emulate**: implement using the normative formula here.
- **Library**: not in standard library; requires third-party or platform framework.

This spec records the core set that’s broadly “Math-like”. Statistics / Linear Algebra / Calculus mappings follow afterward.

---

## A. Constants

| Canonical        | JavaScript           | Python              | Java                 | C#                   | C / C++               | Rust                           | Go                     | Swift                                   | Kotlin                  |
| ---------------- | -------------------- | ------------------- | -------------------- | -------------------- | --------------------- | ------------------------------ | ---------------------- | --------------------------------------- | ----------------------- |
| Pi               | Direct: `Math.PI`    | Direct: `math.pi`   | Direct: `Math.PI`    | Direct: `Math.PI`    | Emulate: `acos(-1)`   | Direct: `std::f64::consts::PI` | Direct: `math.Pi`      | Direct: `Double.pi`                     | Direct: `Math.PI`       |
| Tau              | Emulate: `2*Math.PI` | Direct: `math.tau`  | Emulate: `2*Math.PI` | Emulate: `2*Math.PI` | Emulate: `2*acos(-1)` | Direct: `std::f64::consts::TAU`| Emulate: `2*math.Pi`   | Emulate: `2*Double.pi`                  | Emulate: `2*Math.PI`    |
| EulerNumber      | Direct: `Math.E`     | Direct: `math.e`    | Direct: `Math.E`     | Direct: `Math.E`     | Emulate: `exp(1)`     | Direct: `std::f64::consts::E`  | Direct: `math.E`       | Emulate: `exp(1)` (or `M_E` if present) | Direct: `kotlin.math.E` |
| PositiveInfinity | Direct: `Infinity`   | Direct: `math.inf`  | Direct               | Direct               | Direct: `INFINITY`    | Direct                         | Direct: `math.Inf(1)`  | Direct                                  | Direct                  |
| NegativeInfinity | Direct: `-Infinity`  | Direct: `-math.inf` | Direct               | Direct               | Direct: `-INFINITY`   | Direct                         | Direct: `math.Inf(-1)` | Direct                                  | Direct                  |
| NotANumber       | Direct: `NaN`        | Direct: `math.nan`  | Direct               | Direct               | Direct: `NAN`         | Direct                         | Direct: `math.NaN()`   | Direct                                  | Direct                  |

---

## B. Classification

All are Direct except where noted:

| Canonical       | JavaScript                   | Python | Java   | C#               | C / C++            | Rust   | Go                          | Swift  | Kotlin                    |
| --------------- | ---------------------------- | ------ | ------ | ---------------- | ------------------ | ------ | --------------------------- | ------ | ------------------------- |
| IsNotANumber(x) | Direct: `Number.isNaN(x)`    | Direct | Direct | Direct           | Direct: `isnan`    | Direct | Direct: `math.IsNaN`        | Direct | Direct                    |
| IsFinite(x)     | Direct: `Number.isFinite(x)` | Direct | Direct | Direct (.NET 5+) | Direct: `isfinite` | Direct | Emulate: `!IsNaN && !IsInf` | Direct | Direct                    |
| IsInfinite(x)   | Emulate: `x===Infinity \|\| x===-Infinity` | Direct | Direct | Direct | Direct: `isinf` | Direct | Direct: `math.IsInf(x,0)` | Direct | Direct |

---

## C. Basic value operations

### C.1 AbsoluteValue

Direct everywhere (`Math.abs`, `abs`, `fabs`, `.abs()`, etc.).

### C.2 CopySign

| Target     | Mapping |
| ---------- | ------- |
| JavaScript | **Emulate** using sign-bit detection (must preserve negative zero): `CopySign(m,s) = AbsoluteValue(m) * (IsNegativeSignBit(s) ? -1 : 1)` where `IsNegativeSignBit(s)` is `s < 0 \|\| Object.is(s, -0)`; NaN sign-bit is not reliably observable in JS—document as “best effort”. |
| Python     | Direct: `math.copysign` |
| Java       | Direct: `Math.copySign` |
| C#         | Direct in modern .NET: `Math.CopySign` (else emulate) |
| C/C++      | Direct: `copysign` |
| Rust       | Direct: `copysign` method |
| Go         | Direct: `math.Copysign` |
| Swift      | Direct: `copysign` (Darwin/Glibc) |
| Kotlin     | **Emulate**: `abs(m) * if (s < 0.0 \|\| IsNegativeZero(s)) -1.0 else 1.0` where `IsNegativeZero(s)` uses a bit check (`toBits()`). |

### C.3 Sign

- Java: `Math.signum(x)` is **Direct** (but returns ±0 for ±0; normalize to 0 if you require 0 only).
- Kotlin: `kotlin.math.sign(x)` exists for floating types; verify ±0 behavior; normalize to 0 per normative rule.

Normative emulation (all targets):

- If `IsNotANumber(x)` → `NotANumber`
- Else if `x > 0` → `+1`
- Else if `x < 0` → `-1`
- Else → `0`

---

## D. Rounding

### D.1 Directional rounding

Direct in all targets:

- Toward negative infinity: `floor`
- Toward positive infinity: `ceil`
- Toward zero: `trunc` (or emulate via conditional floor/ceil)

### D.2 Tie-breaking rounding

#### RoundToNearestTiesToEven(x)

| Target     | Mapping |
| ---------- | ------- |
| Python     | Direct: `round(x)` (ties to even) |
| Java       | Direct: `Math.rint(x)` (ties to even) |
| C / C++    | Direct: `rint(x)` (ties to even, rounding mode sensitive) — **Direct (verify)** |
| C#         | Direct: `Math.Round(x, MidpointRounding.ToEven)` |
| JavaScript | **Emulate** (do not use `Math.round`) |
| Go         | **Emulate** (Go’s `math.Round` is ties away from zero) |
| Swift      | **Emulate** (mode-dependent; use explicit emulation) |
| Kotlin     | **Emulate** |

Normative emulation (language-independent):

1. If NaN or ±∞, return itself (IEEE).
2. Let `lower = RoundTowardNegativeInfinity(x)`, `upper = lower + 1`.
3. Compute distances `dLower = x - lower`, `dUpper = upper - x`.
4. If `dLower < dUpper` return `lower`; if `dUpper < dLower` return `upper`.
5. If exactly equal (tie), return the even integer among `lower` and `upper`.

#### RoundToNearestTiesAwayFromZero(x)

| Target            | Mapping |
| ----------------- | ------- |
| C / C++           | Direct: `round(x)` |
| Go                | Direct: `math.Round(x)` |
| Java              | Direct: `Math.round(x)` |
| C#                | Direct: `Math.Round(x, MidpointRounding.AwayFromZero)` |
| Python            | **Emulate** (Python’s `round` is ties to even) |
| JavaScript        | **Emulate** (JS `Math.round` is not symmetric for negatives) |
| Swift/Kotlin/Rust | Often **Emulate** unless a verified helper exists |

Normative emulation:

- Return `Sign(x) * RoundTowardNegativeInfinity(AbsoluteValue(x) + 0.5)` with a careful negative-zero rule: if result is 0, return +0 (unless you explicitly want sign preserved—this surface returns 0).

---

## E. SplitFractionalAndIntegralParts / FractionalPart

| Target                       | Mapping |
| ---------------------------- | ------- |
| Python                       | Direct: `math.modf(x)` but note order is `(fractional, integral)` |
| Go                           | Direct: `math.Modf(x)` returns `(fractional, integral)` |
| C/C++                        | Direct: `modf` (integral part via out param) |
| Java/C#/JavaScript/Rust/Swift/Kotlin | **Emulate**: `integral = RoundTowardZero(x)`; `fractional = x - integral` |

---

## F. Next representable

| Target            | Mapping |
| ----------------- | ------- |
| Python            | Direct: `math.nextafter(value, direction)` |
| Java              | Direct: `Math.nextAfter`, and `Math.nextUp/nextDown` |
| C/C++             | Direct: `nextafter` |
| Go                | Direct: `math.Nextafter` |
| C#                | Partial: `Math.BitIncrement/BitDecrement` (implement Toward via compare) |
| Swift             | Direct: `nextafter` in Darwin/Glibc |
| Rust              | Sometimes direct as methods (`next_up`, `next_down`) depending on toolchain; otherwise **Emulate** via bit-level stepping |
| JavaScript/Kotlin | **Emulate** via IEEE 754 bit stepping (library/internal utility) |

Normative bit-step emulation (IEEE 754 binary64):

- If NaN: return NaN.
- If value == direction: return direction.
- If value == +∞ and direction is finite: return largest finite.
- Else: interpret float bits as ordered and increment/decrement the integer representation toward the target direction, taking care with ±0.

---

## G. Division family mappings

### G.1 Remainder (trunc-division remainder)

| Target         | Mapping |
| -------------- | ------- |
| JavaScript     | `a % b` is **Direct (verify)** for finite values (floating remainder semantics). |
| Python         | `%` is **NOT** trunc remainder for negatives (it’s modulus-like with sign of divisor). Use **Emulate** with trunc quotient. |
| Java/C#/Kotlin | `%` on integers is trunc remainder → **Direct**. |
| Go             | `%` on integers is trunc remainder → **Direct**. |
| Swift          | `truncatingRemainder(dividingBy:)` for floats; integers `%` is trunc remainder. |
| C/C++          | `fmod` for floats corresponds to trunc remainder; `%` for integers. |
| Rust           | `%` for integers is trunc remainder; float remainder operator is trunc remainder. |

Python trunc-quotient emulation (integers):

- `q = int(dividend / divisor)` trunc toward zero
- `r = dividend - divisor*q`

### G.2 Modulus (Euclidean modulus with non-negative result)

| Target                                | Mapping |
| ------------------------------------- | ------- |
| Python                                | `%` matches `0 ≤ m < divisor` when `divisor > 0` → **Direct (verify)** if you lock divisor-positive usage; otherwise verify against the magnitude rule. |
| Java/C#/JavaScript/Go/Kotlin/Swift/C/C++/Rust | **Emulate** using the floor-quotient definition. |

Universal emulation:

- `m = dividend - divisor * RoundTowardNegativeInfinity(dividend/divisor)`
- If you require the `[0, |divisor|)` range, normalize when divisor < 0.

### G.3 FloatingRemainder vs IeeeRemainder

- `FloatingRemainder` maps to `fmod` / trunc remainder.
- `IeeeRemainder` maps to IEEE `remainder` / `IEEEremainder`.

| Canonical         | Python            | Java                | C#                   | C/C++       |
| ----------------- | ----------------- | ------------------- | -------------------- | ----------- |
| FloatingRemainder | `math.fmod`       | **Emulate**         | **Emulate** unless helper exists | `fmod`      |
| IeeeRemainder     | `math.remainder`  | `Math.IEEEremainder`| `Math.IEEERemainder`  | `remainder` |

---

## H. Exponentials / logarithms / powers / roots

Most are direct. Marked emulations are for missing special stable forms.

| Canonical                 | Notes |
| ------------------------- | ----- |
| ExponentialMinusOne       | Prefer direct `expm1`; otherwise emulate `Exponential(x) - 1` (less accurate for small x). |
| NaturalLogarithmOfOnePlus | Prefer direct `log1p`; otherwise emulate `NaturalLogarithm(1 + x)` (less accurate for small x). |
| BaseTwoLogarithm          | If missing, emulate: `NaturalLogarithm(x) / NaturalLogarithm(2)`. |
| ExponentialBaseTwo        | If missing, emulate: `Power(2, x)`. |
| CubeRoot                  | If missing, emulate: `CopySign(Power(AbsoluteValue(x), 1/3), x)`. |

---

## I. Trigonometry and angle conversion

Sine/Cosine/Tangent and inverse functions are Direct everywhere.

Angle conversion is typically emulated as:

- `RadiansFromDegrees(d) = d * (Pi / 180)`
- `DegreesFromRadians(r) = r * (180 / Pi)`

---

## J. Geometry helpers

These are canonical helpers, not standard calls.

### DistanceBetweenPointsTwo

Emulate:

- `HypotenuseLength(x2 - x1, y2 - y1)`

### DistanceBetweenPointsThree

Emulate:

- `SquareRoot((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)` (or a stable hypot3 if you provide one)

### LinearInterpolation(start, end, t)

Emulate:

- `(1 - t) * start + t * end`
- For numerical stability in some cases you may use `start + t*(end-start)`; semantics are the same.

---

# Extended Modules

These are not reliably in “core Math” across languages. If you want them in the canonical surface, standardize which backend library is “official” per target or provide your own deterministic implementation.

## 1) Statistics (Descriptive) — backend choices

### Python (standard library is sufficient)

- `ArithmeticMean` → `statistics.fmean` (preferred for floats) or `statistics.mean`
- `Median` → `statistics.median`
- `Mode` → `statistics.multimode` (to avoid single-mode exceptions)
- `PopulationVariance` → `statistics.pvariance`
- `SampleVariance` → `statistics.variance`
- `PopulationStandardDeviation` → `statistics.pstdev`
- `SampleStandardDeviation` → `statistics.stdev`

### Recommended “official libraries” for other targets (if you want parity)

- Java: Apache Commons Math (statistics) or EJML (linear algebra)
- C#: MathNet.Numerics
- JavaScript: simple-statistics (or your own)
- Go: gonum/stat
- Rust: statrs or ndarray-stats
- Swift: Accelerate (limited descriptive stats) + your own for the rest
- Kotlin/JVM: prefer JVM libraries (Commons Math / EJML)

## 2) Linear Algebra — backend choices

Recommended:

- Python: NumPy (`numpy`, `numpy.linalg`)
- Go: gonum/mat
- Rust: nalgebra (or ndarray + ndarray-linalg)
- Java: EJML
- C#: MathNet.Numerics.LinearAlgebra
- Swift: Accelerate (LAPACK/vDSP)
- Kotlin/JVM: EJML (via JVM)

## 3) Calculus / Numerical analysis — backend choices

Recommended:

- Python: SciPy (`scipy.optimize`, `scipy.integrate`)
- Go: gonum/optimize + integration packages
- Rust: argmin (optimization), roots (root finding), peroxide (numerics)
- Java: Commons Math (some), or dedicated numeric libraries
- C#: MathNet (some) + additional libraries
