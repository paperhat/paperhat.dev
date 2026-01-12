Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Eventing and Event Sourcing Specification

This specification defines Paperhat’s **event model**, including declarative publishing and subscribing, and deterministic event sourcing with projections.

This document governs **event semantics only**.
It does **not** define transport implementations, network protocols, storage engines, or user interface refresh mechanisms.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define events as declarative, schema-validated data
* define publishing and subscribing as declarative intent (not callbacks)
* define event sourcing and deterministic projections
* preserve target independence by separating meaning from realization

---

## 2. Core Invariants (Hard)

The following invariants are non-negotiable:

1. **Events are data.**
2. **Events compile to graph form** and are queryable.
3. **Publishing and subscribing are declarative.**
4. **Validation is shape-based** (for example, via SHACL constraints).
5. **Failures do not throw**; failures are modeled as Help/diagnostics outcomes.
6. **Transport is an implementation detail** and MUST NOT be required to interpret meaning.

This specification defines event semantics, not user interface.

---

## 3. Concept Vocabulary (Normative)

Semantics MUST define the Concepts and Traits for:

* **Channel**

  * identity
  * visibility domain
  * durability
  * ordering guarantee

* **Event**

  * identity
  * channel
  * name
  * payload (typed values)
  * timestamp
  * source (actor)
  * correlation identifiers

* **Event Schema**

  * channel
  * event name
  * typed Property declarations
  * required/optional constraints
  * value constraints

* **Publish**

  * channel
  * event name
  * Argument set
  * optional metadata

* **Subscription**

  * event pattern
  * declared dependency

* **Projection**

  * input event pattern
  * output projection identity
  * fold specification
  * match rules

Invalid events MUST NOT exist.
An event that fails validation MUST NOT be appended.

---

## 4. Channel Scope and Guarantees (Target-Independent)

A Channel MUST declare semantic properties that do not name transport.

### 4.1 Visibility Domain

A Channel MUST declare one visibility domain:

* `document` — same authored surface instance
* `origin` — same authority origin boundary
* `authority` — authoritative server or tenant boundary
* `federated` — multiple authority domains

Visibility domain defines observability boundaries, not mechanisms.

---

### 4.2 Durability

A Channel MUST declare durability:

* `ephemeral` — publish/subscribe only; not replayable
* `durable` — append-only; replayable; projections permitted

---

### 4.3 Ordering Guarantee

A Channel MUST declare an ordering guarantee:

* `unordered`
* `per-channel`
* `global`

The ordering guarantee expresses the minimum ordering required for correctness.

---

### 4.4 Realization Rule (Normative)

Authors declare visibility domain, durability, and ordering.

Targets MUST select transports and storage strategies that satisfy these declarations.

---

## 5. Event Record Semantics (Hard)

An Event record MUST have a canonical representation that includes:

* event identity
* channel identity
* event name
* payload values (typed per Event Schema)
* timestamp (see §9)
* source (actor identity or a Semantics-permitted absence semantics)
* correlation identifiers (such as correlation and causation identifiers)

Semantics MUST define which fields are required and the semantics of absence.

---

## 6. Publishing (Normative)

### 6.1 Publish Is Declarative Intent

Publish is a declarative request.
Publish MUST NOT embed imperative handlers.

### 6.2 Arguments (Normative)

A Publish operation MUST supply an Argument set.

Each Argument MUST have:

* a `name`
* a Value Source (see §8)

Semantics MAY permit explicit coercion rules as a constrained, declarative facility.

### 6.3 Evaluation Result (Pipeline Responsibility)

Pipeline MUST evaluate publishing deterministically with explicitly bound inputs.

* If validation fails: return Help/diagnostics; nothing is appended; nothing is dispatched.
* If validation succeeds: the event is appended (for durable channels) and becomes available for subscription and projection derivation.

---

## 7. Subscribing (Normative)

Subscriptions are declared dependencies, not callbacks.

A Subscription MUST declare:

* an event pattern (for example `cart:item.*`)
* what derived artifact depends on that pattern

This specification does not require any specific user interface update mechanism.

---

## 8. Value Sources (Normative)

Value Sources MUST be target-independent.

Semantics MUST define a minimal set of Value Source concepts.

At minimum:

* **From Binding** — obtain a named bound input
* **From State** — obtain a value from derived state (such as a projection result)
* **From Literal** — use a literal authored value
* **From Event** — obtain a value from the triggering event (reactive contexts only)
* **From Context** — obtain an explicit external input (see §9)

Targets MAY provide binding policies that map “From Binding” to target details.
Those mappings are realization, not semantics.

---

## 9. Determinism and External Inputs (Hard)

Time, actor identity, randomness, locale, and environment are external inputs.

* Semantics MUST model such values as explicit inputs.
* Pipeline MUST require explicit binding for required external inputs.
* Pipeline MUST define hashing rules for external inputs so builds and replays are reproducible.

For durable event sourcing:

* Given an identical event log and identical Semantics, projection results MUST be identical.

---

## 10. Event Sourcing and Projections (Normative)

### 10.1 Append-Only Log (Durable Channels)

For durable channels, events are append-only.

State is derived.

### 10.2 Projections (Deterministic)

A Projection declares deterministic derivation of a projection state from events.

Pipeline MUST be able to rebuild projections deterministically from the event log.

Targets SHOULD read from projections rather than raw events except for auditing and inspection.

---

## 11. Transport and Realization (Non-Semantic)

This specification MUST NOT define:

* specific transports
* network protocols
* storage engines
* user interface refresh mechanics

Pipeline MAY emit target plans (for example: endpoint plans, client dispatch plans, progressive enhancement plans), but those plans MUST NOT change event meaning.

---

## 12. Summary of Ownership

* **Semantics owns:** the event vocabulary, constraints, scope and guarantee semantics, value source types, and projection language shape.
* **Pipeline owns:** validation execution, deterministic evaluation, canonical record formation, projection computation, and plan emission.
* **Targets/adapters own:** transport selection, user interface update mechanisms, protocol details, and storage backend specifics (as long as semantics are preserved).
