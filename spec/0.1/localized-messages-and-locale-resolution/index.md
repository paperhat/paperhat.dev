Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Localized Messages and Locale Resolution Specification

This specification defines Paperhat’s target-independent semantics for:

* localized messages as declarative data
* message parameter contracts and compile-time verification
* structured message render trees
* locale resolution and fallback
* formatting intents for common internationalization needs
* writing direction (LTR/RTL) as semantic metadata

This document governs semantic meaning, constraints, and recordability requirements.
It does **not** define UI frameworks, runtime libraries, storage engines, query languages, or vendor services.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* make localized messaging portable and deterministic
* enable compile-time verification of message keys and parameters
* provide a structured render-tree representation to enable safe post-processing
* define locale resolution as declarative policy evaluated over explicit inputs

---

## 2. Scope

This specification governs:

* message identities and message variants by locale
* parameter schema contracts for messages
* structured message templates and render trees
* locale resolution policies and fallback chains
* formatting intents (date, number, relative time)
* writing direction metadata

This specification does **not** govern:

* translation services
* visual translation tooling
* collaboration platforms
* a specific schema language or query language

---

## 3. Related Specifications

This specification is designed to compose with:

* [Data Validation and Shape Constraints](../data-validation-and-shape-constraints/)
* [Run Logs and Observability](../run-logs-and-observability/)
* [Secrets and Redaction](../secrets-and-redaction/)
* [Search, Indexing, and Query](../search-indexing-and-query/)

---

## 4. Core Invariants (Hard)

1. **Messages are data.** Localized messages MUST be authored and processed as declarative data.
2. **Stable identities.** Message keys MUST have stable, IRI-like identities.
3. **Typed contracts.** Message parameters MUST have a declared schema contract.
4. **Deterministic compilation.** Pipeline MUST compile and validate messages deterministically.
5. **Structured rendering.** Rendering MUST be representable as a structured render tree.
6. **Target independence.** Semantics MUST NOT depend on a UI framework, storage engine, or vendor runtime.
7. **No secret leakage.** Message artifacts and records MUST NOT embed secret material.

---

## 5. Definitions (Normative)

### 5.1 Message Key

A **MessageKey** is a stable identity for a message.

A MessageKey MUST be IRI-like and MUST be stable across versions.

---

### 5.2 Locale Tag

A **LocaleTag** is a semantic token identifying a locale.

This specification does not define a particular locale-tag grammar. However, conforming systems MUST treat LocaleTag validity as a validation concern.

---

### 5.3 Message Variant

A **MessageVariant** is the localized content for a MessageKey for a particular LocaleTag.

A MessageKey MAY have multiple variants for a locale if and only if the variants are distinguished by **selectors** (for example, plural categories).

---

### 5.4 Parameter Schema

A **ParameterSchema** is a declared contract describing what parameters a message accepts.

A ParameterSchema MUST include:

* parameter names
* parameter types (semantic)
* optionality / requiredness

---

### 5.5 Template and Render Tree

A **MessageTemplate** is a declarative structure that, given parameters, produces a **RenderTree**.

A RenderTree MUST be representable as nodes such as:

* text nodes
* parameter nodes
* selection nodes (plural/select)
* formatting-intent nodes

RenderTree is target-independent and MUST support post-processing while preserving meaning.

---

### 5.6 Selection Semantics

A **Selection** is a template construct that chooses among variant branches based on inputs.

Conforming systems MUST support selection constructs sufficient to express:

* plural category selection
* enumerated selection (select)

This specification does not define a concrete syntax for selection constructs.

---

## 6. Authoring Requirements (Normative)

Authored artifacts MUST define messages such that:

* each MessageVariant references a MessageKey and LocaleTag
* each MessageKey has a ParameterSchema
* each template references only parameters declared in the schema

Parameter schemas MAY be produced by tooling assistance, but the authored schema is authoritative.

---

## 7. Compilation and Verification (Normative)

Pipeline MUST:

* parse authored message definitions into a canonical internal representation
* validate that every template parameter reference is declared
* validate that the declared schema does not contain unused required parameters
* validate selection constructs for completeness requirements

### 7.1 Optional Inference (Non-normative)

Tooling MAY infer a candidate ParameterSchema from templates or imported data, but Pipeline MUST validate the authored schema as authoritative.

---

## 8. Locale Resolution (Normative)

A **LocaleResolutionPolicy** is a declarative policy that chooses a ResolvedLocale from explicit inputs.

A policy MUST support:

* multiple detection sources, evaluated in order
* fallback chains (for example, more specific → more general → default)

Locale resolution MUST be deterministic with respect to explicit inputs.

---

## 9. Formatting Intents (Normative)

A **FormatIntent** is a target-independent intent to format a value.

Conforming systems MUST support at least:

* date/time formatting intent
* number formatting intent (including currency intent)
* relative time formatting intent

FormatIntent MUST be representable as nodes in the RenderTree.

---

## 10. Writing Direction and Bidi Metadata (Normative)

Messages and documents MAY carry writing direction metadata.

Conforming systems MUST support, at minimum:

* LTR
* RTL

The application of writing direction to rendering is a target concern, but the metadata and its meaning are semantic.

---

## 11. Recordability (Normative)

Systems SHOULD be able to record:

* which MessageKey was rendered
* which ResolvedLocale was selected
* which variant branch(es) were chosen

Records MUST NOT include secret material.

---

## 12. Target Independence (Hard)

This specification MUST NOT define:

* a UI framework API
* a specific message syntax
* a runtime library requirement
* a database schema, graph store, or query language

Targets may implement localization and rendering using any appropriate mechanisms, provided semantic meaning and constraints are preserved.
