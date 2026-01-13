Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Spec Taxonomy (0.1)

This specification defines the **taxonomy and indexing rules** for Paperhat specifications published at `paperhat.dev`.

This document is **Normative**.

---

## 1. Purpose

Paperhat Specs exist as prior art and as implementation contracts.

To keep the spec set usable and defensible, Paperhat MUST avoid:

- “junk drawer” sections
- ambiguous categorization (a spec that “fits anywhere”)
- duplicate sources of truth

This taxonomy exists to ensure that:

- every spec has one clear home
- cross-references remain stable
- the index stays navigable as the corpus grows

---

## 2. Core Rules (Hard)

1. Paperhat specs MUST be organized into a small, fixed set of categories.
2. Every spec MUST appear in exactly one category in the version index.
3. Creating a new category is forbidden without explicit editorial decision **by the human**.
4. A spec MUST NOT be “miscellaneous”, “other”, “notes”, or “uncategorized”.
5. The version index MUST be the canonical mapping of spec → category.

---

## 3. Category Set (Normative)

Paperhat v0.1 uses exactly these categories.

### 3.1 Foundation

Specs that define global invariants, identifiers, and filesystem/packaging boundaries.

### 3.2 Semantics and Validation

Specs that define meaning, constraint models, Behavior semantics, encodings, diagnostics semantics, and validation rules.

### 3.3 Execution and Reliability

Specs that define workflow execution semantics, durability, replay, concurrency, idempotency, failure behavior, rate limiting, and observability.

### 3.4 Data and Interchange

Specs that define data stores, shared variables, transformation/mapping, search/query, provenance, and interchange formats.

### 3.5 Security and Identity

Specs that define authentication/authorization, credentials, integrations, secrets handling, and redaction.

### 3.6 Operations and Observability

Specs that define logs, observability, alerting/notifications, and operator-facing diagnostic surfaces.

### 3.7 Presentation and Realization

Specs that define view/policy selection, planning, and realization contracts (including plan encodings) without leaking target implementation details.

### 3.8 Domain (Commerce)

Specs that define Paperhat’s commerce and transactional domain semantics.

---

## 4. Anti-Junk-Drawer Tests (Hard)

A spec fails taxonomy if any of the following is true:

- it is defined primarily by what it is NOT
- it exists only because it was "convenient to place"
- it mixes two category concerns without a clear primary contract

If a spec fails, it MUST be split, renamed, or re-scoped.

---

## 5. Indexing Rules (Normative)

1. The version index MUST list categories in a stable order.
2. Within a category, entries SHOULD be ordered by pipeline adjacency (or by dependency order), not by author preference.
3. Each entry MUST link to a kebab-case folder whose spec document is `index.md`.

---

**End of Paperhat Spec Taxonomy v0.1**
