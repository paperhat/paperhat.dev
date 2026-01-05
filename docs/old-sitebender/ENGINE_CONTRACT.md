# Sitebender Runtime Engine Contract

## Canonical Execution Engine Semantics (LOCKED)

This document defines the **runtime engine** responsible for executing compiled Sitebender applications in both client and server environments.

It refines the **Runtime Contract** by specifying **how execution is scheduled, triggered, delegated, and coordinated**.

This document is **normative**.

---

## 1. Role of the Runtime Engine

The runtime engine is the **only imperative system** in Sitebender.

It is responsible for:

- Event delegation
- Dependency tracking
- Evaluation scheduling
- Lifecycle coordination
- Rendering invocation

The engine does **not**:

- perform semantic computation
- encode business logic
- interpret CDX
- bypass Validation semantics

---

## 2. Execution Model (Hard Rules)

### 2.1 Single Entry Point

The engine attaches **a fixed set of listeners** at initialization:

- `document` (bubble + capture as required)
- `window` (limited cases only)

No per-element event handlers are attached, except where technically unavoidable.

---

### 2.2 Event Delegation

All user and system events are handled via **event delegation**.

Process:

1. An event occurs
2. The engine receives it at the document (or window)
3. The engine determines the **action-bearing element** via:
   - `event.target.closest(...)`, or
   - `event.composedPath()` (if shadow boundaries exist)

4. The engine derives a **stable ActionKey**
5. The engine consults its dependency registry

Author-authored logic never receives raw DOM events.

---

## 3. Action Resolution

### 3.1 ActionKey

An ActionKey is a stable identifier derived from:

- Element identity
- Compiled behavior metadata
- Action type (click, submit, input, etc.)

ActionKeys are opaque to authors.

---

### 3.2 Dependency Registry

The engine maintains a **WeakMap**:

```
WeakMap<Element, DependencyRecord>
```

Each DependencyRecord contains:

- Declared actions (publish, validate, toggle, etc.)
- Evaluation thunks (lazy)
- Dependency graph metadata
- Subscription relationships
- Render targets

Garbage collection of elements automatically cleans dependencies.

---

## 4. Evaluation Scheduling

### 4.1 Lazy Invocation

No evaluation occurs until:

- an event resolves to an ActionKey, or
- a subscribed dependency invalidates

---

### 4.2 Async-Only Execution

All engine-invoked evaluations return:

```
Future<Validation<Help, A>>
```

The engine never blocks.

---

### 4.3 Coalescing Rules

High-frequency triggers (scroll, resize, observer updates):

- Are coalesced per animation frame
- Trigger at most **one evaluation cycle per frame**
- Multiple invalidations collapse into one cycle

No authored logic may observe raw event frequency.

---

## 5. Observer Integration

### 5.1 Observers Used

The engine is responsible for wiring:

- `ResizeObserver` → `FromResize`
- `IntersectionObserver` → `FromIntersection`
- Viewport changes → `FromViewport`
- Scroll monitoring → `FromScroll`

Observers emit **measurement data**, not events.

---

### 5.2 Observer Semantics

- Observers publish validated measurements
- Measurements enter the system as injector updates
- Observer updates may emit Operator lifecycle events
- Raw observer callbacks are never exposed

---

## 6. Lifecycle Events

The engine emits **evaluation lifecycle signals** via Operator:

- `eval.started`
- `eval.succeeded`
- `eval.failed`

These events include:

- computation identity
- target element / path
- timestamp
- outcome (value or helps)

Lifecycle events are informational and non-authorable.

---

## 7. Dependency Invalidation

When:

- an event is published
- a projection updates
- an observer measurement changes
- state changes (Custodian)

The engine:

1. Marks dependent nodes invalid
2. Schedules re-evaluation (lazy)
3. Coalesces execution
4. Executes affected thunks

Invalidation is **graph-based**, not imperative.

---

## 8. Rendering Invocation

### 8.1 Render Triggers

Rendering is invoked only when:

- a `Usable(value)` is produced, or
- `Helps([...])` must be displayed

---

### 8.2 Render Purity

The engine calls renderers, but:

- rendering is pure
- rendering never mutates state
- rendering never throws
- rendering never performs IO

---

## 9. Server vs Client Execution

### Client

- Engine runs in browser
- Uses DOM, observers, events
- Progressive enhancement applies

### Server

- Engine runs in request scope
- No DOM observers
- Events are simulated
- Same semantics, different inputs

The engine does not branch on “mode”; only inputs differ.

---

## 10. Forbidden Engine Behaviors

The runtime engine must **never**:

- Attach per-element handlers (except unavoidable cases)
- Call authored code imperatively
- Bypass Validation
- Inspect monad internals
- Mutate shared state
- Swallow failures
- Perform semantic computation

---

## 11. Engine Invariants (Summary)

- One engine
- One event surface
- One dependency registry
- One evaluation model
- One scheduling model
- No hidden execution paths
- No special cases for authors

---

## Status

**LOCKED.**

This document is authoritative.
