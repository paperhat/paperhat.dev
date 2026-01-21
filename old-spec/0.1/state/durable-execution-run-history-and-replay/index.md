Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Durable Execution: Run History and Replay

This specification defines Paperhat’s **durable execution** semantics: how workflow execution can be made crash-resumable by representing execution as replay over an **append-only run history**, while preserving Paperhat’s determinism and authority boundaries.

This document is **Normative**.

---

## 1. Purpose

Durable execution exists to:

- allow long-running work to survive process restarts and deployment changes
- make execution outcomes reproducible and inspectable
- preserve determinism by recording external results as explicit history

---

## 2. Core Invariants (Normative)

1. **History is append-only.** Durable run history MUST be append-only.
2. **Replay is deterministic.** Given identical run history and identical Semantics, re-evaluation MUST produce identical outcomes.
3. **Side effects are outside semantics.** External interactions MUST be modeled as explicit inputs/results recorded into history.
4. **No ambient dependencies.** Time, randomness, environment, and network MUST NOT be consulted except as explicit inputs.

---

## 3. Run History (Normative)

A Workflow Run MUST have a canonical **Run History**: an append-only sequence of Run Events.

### 3.1. Run Event Shape (Normative)

A Run Event MUST have:

- identity
- run identity
- event kind
- a canonical ordering key (to make “history” a deterministic sequence)
- timestamp semantics as explicit inputs (per Paperhat determinism rules)
- correlation identifiers as needed
- payload typed by Kernel vocabulary

More specifically, a Run Event MUST include, at minimum:

- `eventId` (stable identity)
- `runId`
- `kind`
- `seq` (a total-ordering key within the run; MUST be unique within `runId`)
- `payload`

If a timestamp is present, it MUST be treated as an explicit input value (recorded into history) and MUST NOT be consulted from ambient time sources during replay.

### 3.2. Run Event Kinds (Normative)

Kernel MUST define a closed set of Run Event kinds sufficient to model durable execution. At minimum, the vocabulary MUST include kinds representing:

- timer delivery (a timer firing)
- signal delivery (an external signal being delivered)
- recording an external result (a previously-missing external value becoming available)
- recording a step outcome (a step completion producing a value)
- recording a snapshot/checkpoint (a derived artifact emitted to speed replay)

This specification does not mandate a storage engine.

---

## 4. Replay Model (Normative)

Kernel MUST be able to evaluate a Workflow Run by replaying its Run History.

Rules:

- If a step requires an external result that is not present in history, evaluation MAY be Pending.
- When the external result becomes available, it MUST be recorded as a Run Event and evaluation may proceed.
- Recording the same external result twice MUST be treated as a de-duplication concern (see Idempotency).

### 4.1. Idempotency and De-duplication (Normative)

Durable execution MUST be robust to retries.

Rules:

1. If two Run Events for the same `runId` have the same `eventId`, they MUST be treated as the same event.
2. If a Run Event includes an idempotency key (for example `dedupeKey`), the storage/adapter layer MUST prevent multiple distinct events for the same `runId` and `dedupeKey` from being appended.
3. If duplicates occur anyway (for example due to eventual consistency), Kernel MUST handle them deterministically:
	- if duplicates are byte-for-byte equivalent in normalized form, Kernel MUST ignore the duplicates
	- if duplicates conflict in payload for the same identity/idempotency key, Kernel MUST report a deterministic diagnostic (not consult ambient state to resolve)

---

## 5. Timers, Signals, and Waiting (Normative)

Timers, signals, and waiting MUST be represented as Run Events (history facts), not as hidden engine state.

- A timer firing is a Run Event.
- A signal delivery is a Run Event.
- Waiting is a Pending evaluation state due to missing required Run Events.

This specification does not define scheduler implementations.

---

## 6. Snapshots / Checkpoints (Normative)

Because histories can grow large, implementations MAY create snapshots (checkpoints) of derived run state.

Rules:

1. A snapshot MUST be derived, not authoritative.
2. A snapshot MUST be attributable to a specific history prefix and Kernel version.
3. If a snapshot is missing or invalid, Kernel MUST be able to replay from history.

Attribution MUST include enough information to verify the snapshot is safe to apply, including at least:

- the `runId`
- the highest `seq` (or equivalent) included in the snapshot
- a digest/identifier for the history prefix the snapshot summarizes, OR a provably-unique reference to that prefix
- a Kernel version/digest

---

## 7. HADR (Informative)

High availability and disaster recovery are realized by storage replication and backup.

To preserve Paperhat semantics:

- recovery MUST restore append-only history sufficient for replay
- derived artifacts (snapshots, projections) MAY be rebuilt if lost

---

## 8. Ownership Summary

- **Kernel owns:** the vocabulary for Run History and Run Events.
- **Kernel owns:** deterministic evaluation and replay semantics.
- **Adapters own:** storage/transport realization as long as invariants hold.

---

**End of Durable Execution: Run History and Replay v0.1**
