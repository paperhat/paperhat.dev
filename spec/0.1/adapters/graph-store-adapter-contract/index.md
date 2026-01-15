Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Graph Store Adapter Contract

This specification defines the contract a **Graph Store Adapter** MUST satisfy to serve as Paperhat’s primary graph persistence substrate.

This document is **Normative**.

---

## 1. Purpose

A Graph Store Adapter exists to:

- persist and query RDF-based artifacts (domain graphs, view graphs, policy graphs, run logs)
- persist **durable event channels** as an append-only history
- support deterministic rebuild of projections from history
- preserve semantics while allowing multiple backend realizations

---

## 2. Non-Goals

This contract does not define:

- a particular triple store product
- network protocols
- deployment topology
- specific replication/backup mechanisms

---

## 3. Required Capabilities (Normative)

A conforming adapter MUST provide:

- **Write** of canonical RDF artifacts into addressable partitions
- **Query** via a standard SPARQL surface (or an equivalent capability surface that can be shown to preserve the SPARQL semantics required by Paperhat)
- **Partitioning** that supports independent addressing of:
  - compile-time authored artifacts
  - runtime facts (events)
  - derived artifacts (projections, snapshots)

A conforming adapter MUST support **named graph**-like partitioning semantics even if the backend does not expose named graphs directly.

---

## 4. Durable Event Log Contract (Normative)

For **durable channels**, the adapter MUST preserve an append-only history.

Rules:

1. Appends MUST be atomic.
2. Events MUST NOT be modified in-place.
3. Event records MUST be retrievable for deterministic replay and projection rebuild.
4. If the backend supports transactions, event append and any same-transaction derived writes MUST be performed transactionally.

This contract does not require a particular physical storage layout.

---

## 5. CQRS Support (Normative)

The adapter MUST support the CQRS posture required by Paperhat:

- **Writes** are facts (events) and authored artifacts.
- **Reads** SHOULD be served from derived projections / read models where possible.

The adapter MUST NOT require consumers to query raw event logs to obtain current state.

---

## 6. Snapshot / Checkpoint Support (Normative)

To keep replay bounded, the adapter MUST support storage of **snapshots** as derived artifacts.

Rules:

- A snapshot MUST be attributable to a specific history range and semantics version.
- A snapshot MUST NOT be treated as semantic source of truth.
- If a snapshot is missing or invalid, the Kernel MUST be able to rebuild from history.

---

## 7. HADR Expectations (Informative)

High availability and disaster recovery are realization concerns.

However, any HADR strategy MUST preserve the meaning of this contract:

- durable event history remains append-only
- recovery restores a history sufficient for deterministic rebuild
- derived artifacts may be rebuilt if lost

---

**End of Graph Store Adapter Contract v0.1**
