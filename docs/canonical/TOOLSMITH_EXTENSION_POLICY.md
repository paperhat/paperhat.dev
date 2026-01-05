# Toolsmith Extension Policy (LOCKED)

This document defines the **exclusive responsibilities of Toolsmith** and the **strict rules by which other libraries may extend it**.

Toolsmith is the **kernel** of the Sitebender system.

This document is **normative**.

---

## 1. Role of Toolsmith (Hard)

Toolsmith provides the **foundational computational substrate** for all Sitebender libraries.

It is intentionally:

- large
- boring
- stable
- opinionated
- slow to change

All other libraries are built **on top of Toolsmith**, never alongside it.

---

## 2. What Toolsmith Owns (Exclusive)

Only Toolsmith may define or implement the following:

### 2.1 Monads and Control Structures

- `Maybe`
- `Result`
- `Validation`
- `Future` / async abstractions
- traversal, sequencing, folding, chaining utilities

No other library may define its own monads or control abstractions.

---

### 2.2 Newtype Framework

Toolsmith exclusively owns:

- newtype constructors
- runtime tagging mechanisms
- validation entry points
- canonical conversion helpers (`toMaybe`, `toResult`, `toValidation`)

All newtypes across the system must use Toolsmith machinery.

---

### 2.3 Numeric and Structural Types

Including but not limited to:

- Integer, Fraction, PrecisionNumber, WholeNumber, SafeFloat
- collections and structural helpers
- canonical serialization formats

No library may introduce competing numeric systems.

---

### 2.4 BaseHelp and Help Infrastructure

Toolsmith owns:

- `BaseHelp`
- severity levels
- context attachment
- suggestion attachment
- help composition utilities
- help rendering primitives (non-UI)

All help across the system must be representable as `BaseHelp`.

---

### 2.5 Purity Boundaries

Toolsmith is the **only place** where:

- mutation
- loops
- imperative constructs

may exist internally **for performance reasons only**.

All such constructs must be:

- fully encapsulated
- referentially transparent at the boundary
- exposed only as pure, curried, composable functions

---

## 3. What Libraries May Extend (Strictly)

Libraries may extend Toolsmith **only in the following ways**.

---

### 3.1 Help Extension (Allowed)

A library may:

- define **library-local help codes**
- define **library-local help constructors**
- return `BaseHelp<LocalCode>`

Rules:

- Help language must follow global pedagogy rules
- Libraries must not redefine BaseHelp
- Libraries must not change severity semantics

---

### 3.2 Newtypes (Allowed, Constrained)

A library may define domain-specific newtypes **only if**:

- they use Toolsmith’s newtype framework
- validation is explicit and total
- conversions route through Toolsmith helpers

Libraries must not:

- invent ad-hoc tagged unions
- bypass runtime tagging
- introduce structural typing as a substitute

---

### 3.3 Pure Functions (Allowed)

Libraries may define:

- pure functions
- curried functions
- higher-order functions

**Only if**:

- they use Toolsmith monads for failure
- they return `Maybe`, `Result`, or `Validation` as appropriate
- they never throw

---

## 4. Forbidden Extensions (Hard)

Libraries must never:

- define their own monads
- inspect monad internals (`_tag`, private fields, etc.)
- throw exceptions
- return `null` or `undefined`
- perform IO in pure paths
- mutate shared state
- redefine numeric semantics
- create parallel help systems

If a capability is missing, Toolsmith must be extended instead.

---

## 5. Extension Escalation Rule (Hard)

If a library requires functionality not supported by Toolsmith:

1. The requirement must be documented.
2. Toolsmith is extended first.
3. The library consumes the new capability.
4. Duplicate or local workarounds are forbidden.

Convenience is not a justification for bypassing Toolsmith.

---

## 6. Stability Contract

- Toolsmith changes slowly.
- Toolsmith changes are deliberate.
- Toolsmith changes may require coordinated library updates.
- Toolsmith versioning is conservative.

Downstream libraries adapt; Toolsmith does not chase them.

---

## 7. Relationship to Other Canonical Docs

This policy must be read in conjunction with:

- `CODEX_SYSTEM_CONTRACT.md`
- `LLM_ROLES_AND_LIMITS.md`
- library-specific `CONTRACT.md` files

In case of conflict, **Toolsmith Extension Policy prevails** for kernel concerns.

---

## Status

LOCKED.
