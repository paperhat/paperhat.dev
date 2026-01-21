Status: NORMATIVE
Lock State: UNLOCKED  
Version: 0.1
Editor: Charles F. Munat

# Paperhat Workbench ConceptForm Contract

---

## 1. Purpose

This specification defines **ConceptForm**, the schema-derived form projection used by the Paperhat Workbench for structured authoring.

ConceptForm exists to:

* provide a non-textual authoring projection derived from schema
* ensure forms are mechanically derivable from meaning
* eliminate hand-designed, schema-specific forms
* preserve determinism, validation, and mutation discipline

This document is **Normative**.

---

## 2. Scope

This specification governs:

* how ConceptForms are derived from schema
* how form structure may be constrained or customized
* how form interaction results in authoring proposals

This specification does **not** define:

* UI widgets or layout systems
* styling or presentation
* storage formats
* semantic rules or ontology design

---

## 3. Canonical Relationship (Normative)

A ConceptForm is a **projection** over the canonical authored state.

ConceptForms:

* do not define new meaning
* do not store independent authored truth
* do not bypass mutation boundaries

All ConceptForm interactions MUST result in deterministic Patches.

---

## 4. Mechanical Derivation (Normative)

ConceptForms MUST be mechanically derivable from schema.

Given a Concept type, the system MUST be able to determine:

* applicable properties
* cardinality
* required vs optional status
* value types
* constraints and validations

Form derivation MUST NOT require hand-authored form definitions.

---

## 5. Default Form Generation (Normative)

Given a Concept type, a default ConceptForm MUST include:

* all schema-defined properties
* properties ordered deterministically
* validation derived directly from schema constraints

Default ordering MUST be stable and documented.

---

## 6. Form Customization (Normative)

ConceptForm MAY be customized using a declarative specification.

Supported operations include:

* inclusion of specific properties
* exclusion of specific properties
* grouping of properties
* hiding of properties
* assigning default or sentinel-derived values

Customization MUST:

* remain declarative
* remain deterministic
* operate strictly within schema-defined bounds

Customization MUST NOT:

* redefine property semantics
* introduce properties not defined by schema
* relax schema validation

---

## 7. Hidden and Sentinel Values (Normative)

ConceptForm MAY declare hidden properties.

Hidden properties:

* are part of the authored data
* are not visible in the form
* MAY be assigned values via sentinels or explicit defaults

Sentinel-derived values MUST be:

* explicit
* deterministic
* inspectable

Implicit or ambient value derivation is forbidden.

---

## 8. Validation Behavior (Normative)

ConceptForm interactions MUST enforce validation:

* at proposal time
* according to schema constraints
* using Diagnostic Messaging and Help semantics

Validation failures MUST produce Diagnostics.

Form submission MUST NOT mutate authored content on validation failure.

---

## 9. Patch Production (Normative)

All ConceptForm interactions MUST result in:

* deterministic Patch proposals
* explicit review opportunity
* no implicit application

ConceptForms MUST NOT apply changes directly.

---

## 10. Relationship to Text Projection (Normative)

ConceptForm and Text Projection are equivalent in authority.

Both:

* operate over the same canonical authored state
* produce identical Patch semantics
* are subject to identical validation and refusal rules

Neither projection supersedes the other.

---

## 11. Gloss-Aware Fields (Normative)

ConceptForms MAY include Gloss-aware fields.

Gloss-aware fields:

* preserve explicit textual structure
* avoid hidden formatting
* do not introduce opaque rich-text storage

Gloss usage MUST remain explicit and inspectable.

---

## 12. Extensibility (Normative)

New ConceptForm capabilities MAY be added only if:

* derivation remains mechanical
* determinism is preserved
* no alternate authoring model is introduced
* mutation boundaries remain intact

---

## 13. Reality Rule (Normative)

This specification defines ConceptForm **as it is**.

There is no legacy form system.
There are no hand-authored forms.
There is no historical accommodation.

If this specification changes, the prior reality ceases to exist.

---

**End of Specification**
