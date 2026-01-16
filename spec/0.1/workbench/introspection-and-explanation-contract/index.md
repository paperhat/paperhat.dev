Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench Introspection and Explanation Contract

---

## 1. Purpose

This specification defines the **introspection and explanation capabilities** of the Paperhat Workbench.

Introspection exists to:

* make authored meaning observable
* make system behavior explainable
* allow users to understand *what the system sees* and *why it behaves as it does*
* support trust through transparency

This document is **Normative**.

---

## 2. Scope

This specification governs:

* read-only inspection of authored and derived artifacts
* explanation of validation, assembly, and planning outcomes
* snapshot-based observation
* diff and comparison capabilities

This specification does **not** define:

* mutation behavior
* semantic rules
* UI presentation
* storage formats

---

## 3. Read-Only Discipline (Normative)

All introspection is **read-only**.

Introspection MUST:

* observe immutable Snapshots
* produce no side effects
* introduce no hidden state

Introspection MUST NOT:

* mutate authored content
* influence subsequent execution
* bypass validation or refusal semantics

---

## 4. Snapshot Authority (Normative)

All introspection MUST be based on an explicit Snapshot.

Rules:

* introspection without a Snapshot is forbidden
* identical Snapshots MUST yield identical introspection results
* introspection MUST reflect exactly the state captured by the Snapshot

Snapshots are the sole authority for explanation.

---

## 5. Introspectable Artifacts (Normative)

The Workbench MUST support introspection of:

* workspace structure
* module inventory
* assembled artifacts
* resolved identifiers and references
* constraint and validation outcomes
* graphs and relationships
* ViewModels
* Presentation Plans
* File Plans
* build artifacts

All introspection targets MUST be deterministic and inspectable.

---

## 6. Explanation Semantics (Normative)

When introspection is used for explanation, the system MUST:

* describe *what was derived*
* describe *why it was derived*
* reference the rules or constraints involved
* preserve causal relationships

Explanation MUST NOT:

* speculate
* invent intent
* assign blame

---

## 7. Diagnostic Integration (Normative)

Introspection and explanation MUST integrate with Diagnostics.

Rules:

* Diagnostics MAY reference introspected artifacts
* explanations MAY cite Diagnostics as causal evidence
* Diagnostic causality MUST be preserved

Introspection MUST NOT suppress or reframe Diagnostics.

---

## 8. Diff and Comparison (Normative)

Workbench MAY support diffing of:

* Snapshots
* assembled artifacts
* Presentation Plans
* File Plans
* build outputs

Diff operations MUST:

* be deterministic
* be read-only
* compare like-for-like artifacts
* explain differences without judgment

---

## 9. Projection Neutrality (Normative)

Introspection MUST be projection-neutral.

The same introspection result MUST be available regardless of:

* CLI usage
* desktop studio usage
* web interface usage

Presentation differences MUST NOT affect introspection semantics.

---

## 10. Extensibility (Normative)

New introspection capabilities MAY be added only if:

* snapshot discipline is preserved
* determinism is maintained
* no mutation paths are introduced
* behavior is specified normatively

---

## 11. Reality Rule (Normative)

This specification defines introspection and explanation **as they are**.

There is no legacy explanation model.
There are no hidden inspection modes.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
