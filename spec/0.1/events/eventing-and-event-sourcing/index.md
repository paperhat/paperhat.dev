Status: NORMATIVE  
Lock State: UNLOCKED  
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

## 2. Core Invariants (Normative)

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

Kernel MUST define the Concepts and Traits for:

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

## 5. Event Record Semantics (Normative)

An Event record MUST have a canonical representation that includes:

* event identity
* channel identity
* event name
* payload values (typed per Event Schema)
* timestamp (see §9)
* source (actor identity or a Kernel-permitted absence semantics)
* correlation identifiers (such as correlation and causation identifiers)

The Kernel MUST define which fields are required and the semantics of absence.

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

The Kernel MAY permit explicit coercion rules as a constrained, declarative facility.

### 6.3 Evaluation Result (Kernel Responsibility)

The Kernel MUST evaluate publishing deterministically with explicitly bound inputs.

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

Value Source categories are defined by [Value Source Specification](../../data/value-source/).

Targets MAY provide binding policies that map Value Sources to target details.
Those mappings are realization, not semantics.

---

## 9. Determinism and External Inputs (Normative)

Time, actor identity, randomness, locale, and environment are external inputs.

* The Kernel MUST model such values as explicit inputs.
* The Kernel MUST require explicit binding for required external inputs.
* The Kernel MUST define hashing rules for external inputs so builds and replays are reproducible.

For durable event sourcing:

* Given an identical event log and identical Kernel, projection results MUST be identical.

---

## 10. Event Sourcing and Projections (Normative)

### 10.1 Append-Only Log (Durable Channels)

For durable channels, events are append-only.

State is derived.

### 10.2 Projections (Deterministic)

A Projection declares deterministic derivation of a projection state from events.

The Kernel MUST be able to rebuild projections deterministically from the event log.

Targets SHOULD read from projections rather than raw events except for auditing and inspection.

---

## 10.3 CQRS (Normative)

Paperhat requires a CQRS posture.

Rules:

1. Commands (writes) MUST produce facts (events) on durable channels.
2. Queries (reads) SHOULD be served from derived projections (read models) rather than scanning raw event history.
3. If a projection is missing or invalid, it MUST be rebuildable deterministically from the durable event log.

This specification does not require a particular storage engine or indexing strategy.

---

## 10.4 Snapshots / Checkpoints (Normative)

To keep replay and projection rebuild bounded as event logs grow, implementations MAY materialize snapshots (checkpoints) of derived projection state.

Rules:

1. A snapshot MUST be treated as a derived artifact, not semantic source of truth.
2. A snapshot MUST be attributable to a specific event history range and Kernel version.
3. If a snapshot is missing, the Kernel MUST be able to rebuild the projection from event history.

---

## 11. Transport and Realization (Non-Semantic)

This specification MUST NOT define:

* specific transports
* network protocols
* storage engines
* user interface refresh mechanics

The Kernel MAY emit target plans (for example: endpoint plans, client dispatch plans, progressive enhancement plans), but those plans MUST NOT change event meaning.

---

## 12. Summary of Ownership

* **Kernel owns:** the event vocabulary, constraints, scope and guarantee semantics, value source types, and projection language shape.
* **Kernel owns:** validation execution, deterministic evaluation, canonical record formation, projection computation, and plan emission.
* **Targets/adapters own:** transport selection, user interface update mechanisms, protocol details, and storage backend specifics (as long as semantics are preserved).
