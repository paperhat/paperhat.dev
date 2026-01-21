# Graph Adapter (Library)

The Graph Adapter (`@paperhat/graph-adapter`) defines the **adapter contract** between Paperhat and graph persistence backends (triple stores / named graph stores).

The intent is to support Paperhat’s non-negotiable constraints:

- append-only durable event history (semantic durability)
- deterministic replay and rebuild of derived artifacts
- CQRS-style projections/read models derived from canonical history

A graph store is a **realization detail**.

- The adapter contract MUST preserve Paperhat invariants regardless of which graph backend is used.
- Loss of derived artifacts MUST be recoverable by rebuilding from canonical history.

This library is deliberately backend-agnostic.
