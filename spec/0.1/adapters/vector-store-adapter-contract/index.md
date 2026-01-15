Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Vector Store Adapter Contract

This specification defines the contract a **Vector Store Adapter** MUST satisfy to serve as Paperhat’s vector index substrate.

This document is **Normative**.

---

## 1. Purpose

A Vector Store Adapter exists to:

- store and query vectors for similarity search
- attach lightweight metadata sufficient to map results back to canonical Paperhat artifacts
- remain compatible with deterministic rebuild expectations

---

## 2. Source-of-Truth Rule (Normative)

A vector store MUST NOT be treated as a semantic source of truth.

Vectors and vector indices are **derived** artifacts.

---

## 3. Required Capabilities (Normative)

A conforming adapter MUST provide:

- create/index collections (or equivalent partitions)
- insert/upsert vector points with stable ids
- similarity search with:
  - top-k
  - optional score threshold
  - optional metadata filtering (backend permitting)

---

## 4. Rebuildability (Normative)

The adapter contract MUST permit rebuild from canonical sources.

Rules:

- Loss of the vector store MUST NOT compromise semantic correctness.
- Tooling MAY rebuild vector indices from canonical artifacts and/or projections.
- The Kernel MUST NOT permit vectors to introduce or override semantic meaning.

---

## 5. HADR Expectations (Informative)

Replication and backup are realization details.

Because vector indices are derived, HADR MAY choose either:

- replicate and back up the vector store, or
- rebuild the vector store from canonical sources after failover

---

**End of Vector Store Adapter Contract v0.1**
