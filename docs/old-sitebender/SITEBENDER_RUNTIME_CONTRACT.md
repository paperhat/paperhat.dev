# Paperhat Runtime Contract

## Canonical Execution Semantics (LOCKED, AMENDED)

This document defines the **runtime semantics** of all Paperhat applications after compilation.

It is **normative**.
Any library or runtime behavior that violates this contract is **not a Paperhat component**.

---

## 1. Authoring vs Runtime Boundary

### Authoring

- Humans author **only Codex (`.cdx`)**
- CDX is versioned in git
- CDX is the **source of truth for authored intent**

### Runtime

- Runtime executes **compiled artifacts**
- Runtime never executes CDX directly
- Runtime behavior is entirely **derived**

---

## 2. Compilation Boundary (Hard Rule)

The only valid compilation pipeline is:

```
CDX
 → AST
 → IR
 → RDF (triples)
```

Properties:

- Pure
- Deterministic
- Referentially transparent
- No IO
- No side effects

Compilation failures:

- Are **compile-time**
- Are reported as **Help**
- Prevent runtime execution

---

## 3. Runtime Inputs

At runtime, evaluation operates over:

1. **Compiled IR**
2. **Triple store contents**
   - App-derived triples
   - Library ontologies
   - Reference datasets

3. **Runtime context**
   - DOM
   - Events
   - Time
   - Viewport
   - User/session state
   - Network

---

## 4. Universal Evaluation Model

### 4.1 Everything Is Asynchronous

All runtime evaluation is **async**.

Formally:

```
Evaluation<A> = Future<Validation<Help, A>>
```

This applies to:

- Injectors
- Operators
- Validators
- Event publishers
- Projections
- Rendering decisions

There are **no synchronous execution paths**.

---

### 4.2 Lazy by Default

- Evaluations are **lazy**
- No computation occurs until:
  - explicitly invoked, or
  - subscribed to by the runtime

Injectors may opt into eager evaluation, but semantics are unchanged.

---

## 5. Validation Is the Universal Result Type

### 5.1 No Exceptions

- Runtime code never throws
- Runtime code never returns `null` or `undefined`

All failure states are represented as **Help**.

---

### 5.2 Validation Outcomes

Every evaluation yields exactly one of:

1. **Usable(value)**
2. **Helps([...])**

---

### 5.3 Pending Is Not Failure

- Pending evaluation is **not an error**
- Pending is represented by an unresolved `Future`
- Pending may emit lifecycle events

Pending never produces Helps.

---

## 6. Help System Contract

### 6.1 Helps Are First-Class Runtime Artifacts

Helps are:

- Structured data
- Accumulative
- Renderable
- Inspectable
- Serializable

Helps may include:

- Severity
- Human-facing message
- Target (element / property / path)
- Context
- Suggestions
- Causal chain

---

### 6.2 Helps Replace Debuggers

There is no step debugger.

The Help system is the **only** runtime explanation mechanism.

---

## 7. Injectors

### 7.1 Definition

Injectors are **pure, read-only leaf nodes** that introduce values into evaluation graphs.

They never:

- mutate state
- throw
- perform hidden IO

All injectors return:

```
Future<Validation<Help, A>>
```

---

### 7.2 FromArgument

- A composed function may accept **at most one argument**
- The argument is immutable
- The argument is threaded unchanged through the tree
- Only `<FromArgument />` reads it
- All other nodes ignore it

`FromArgument` is semantically identical to any other injector.

---

## 8. Observed Environment Injectors (LOCKED)

Certain runtime values are **observed**, not polled or inferred from raw DOM events.

### 8.1 Viewport & Layout Observers

The runtime provides the following **first-class injectors**:

- **FromViewport**
  - Viewport dimensions and orientation

- **FromResize**
  - Element/container size changes
  - Backed by `ResizeObserver`

- **FromScroll**
  - Scroll position and extent
  - Coalesced per animation frame

- **FromIntersection**
  - Visibility and proximity signals
  - Backed by `IntersectionObserver`

---

### 8.2 Event Model for Observers

- Observers emit **measurement data**, not raw DOM events
- Updates are:
  - asynchronous
  - validated
  - coalesced

- Observer updates may emit Operator lifecycle events

Raw DOM `scroll` and `resize` events are **never consumed directly** by authored logic.

---

## 9. Operators

Operators are **branch nodes** that:

- Lift Toolsmith pure functions
- Combine child evaluations
- Preserve Validation semantics

Operators:

- Never inspect monad internals
- Never throw
- Never mutate
- Never short-circuit outside Validation rules

---

## 10. Event Runtime (Operator)

### 10.1 Events Are Data

- Events are immutable
- Events are triples
- Events are append-only

---

### 10.2 Publishing

Publishing an event:

```
Evaluation → Validation → Store → Dispatch
```

Invalid events:

- Produce Helps
- Do not enter the system

---

### 10.3 Subscribing

Subscriptions:

- Declare dependencies
- Never register callbacks
- Cause re-evaluation on matching events

---

## 11. Projection Runtime

- Projections consume events
- Projections derive state
- Derived state is replaceable
- Replay deterministically rebuilds state

---

## 12. Rendering Runtime

### 12.1 Rendering Is Pure

Rendering consumes:

- IR or query results
- Evaluation outputs

Rendering produces:

- DOM mutations
- HTML strings
- CDX text (round-trip)

Rendering never performs IO and never throws.

---

### 12.2 Progressive Enhancement

- Without JS: server executes runtime
- With JS: client executes runtime
- Semantics are identical

---

## 13. Environment Isolation

### Dev-A

- No triple store
- IR-driven evaluation
- Fast preview

### Dev-B / Test

- Ephemeral store
- Full validation

### Prod

- Persistent store
- Same semantics

---

## 14. Forbidden Runtime Behaviors

Explicitly forbidden:

- Throwing exceptions
- Imperative callbacks
- Mutation
- Hidden control flow
- Silent failure
- Partial success

---

## 15. Runtime Invariants (Summary)

- Everything async
- Everything lazy
- Everything validated
- Everything explainable
- Everything derived
- Nothing throws
- Nothing mutates
- Nothing is implicit

---

**Status:** LOCKED
This document is authoritative.
