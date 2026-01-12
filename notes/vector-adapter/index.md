# Vector Adapter (Library)

The Vector Adapter (`@paperhat/vector-adapter`) defines the **adapter contract** between Paperhat and vector index backends.

Vector indexing is treated as a **derived capability**:

- it MUST NOT be the semantic source of truth
- it MAY be rebuilt from canonical facts (events, projections, artifacts)
- it SHOULD be verifiable and HADR-friendly by being rebuildable

This library is deliberately backend-agnostic.
