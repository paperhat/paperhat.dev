Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Message Pack Imports and Interchange Specification

This specification defines Paperhat’s target-independent semantics for importing localized message content from external interchange formats into a canonical message representation.

This document governs semantic meaning, determinism, and validation requirements.
It does **not** define any particular interchange file format in full detail.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* define how external message content may be imported without changing meaning
* make imports deterministic and auditable
* ensure imported content conforms to Paperhat message semantics (keys, locales, schemas, templates)

---

## 2. Scope

This specification governs:

* import as a Kernel action producing a canonical message pack
* mapping from external interchange fields to semantic concepts
* deterministic normalization and conflict handling
* validation requirements for imported message content

This specification does **not** govern:

* a user interface for translation management
* collaborative editing protocols
* translation services
* any particular storage engine for the canonical pack

---

## 3. Related Specifications

This specification is designed to compose with:

* [Localized Messages and Locale Resolution](../../validation/localized-messages-and-locale-resolution/)
* [Data Validation and Shape Constraints](../../validation/data-validation-and-shape-constraints/)
* [Provenance and Lineage](../provenance-and-lineage/)
* [Run Logs and Observability](../../operations/run-logs-and-observability/)

---

## 4. Core Invariants (Normative)

1. **Imports preserve meaning.** Import MUST NOT change semantic meaning of message content.
2. **Deterministic compilation.** Import MUST be deterministic given explicit inputs.
3. **Canonical output.** Import MUST produce a canonical message pack representation.
4. **No secret material.** Import artifacts and records MUST NOT embed secret material.
5. **Target independence.** Import semantics MUST NOT depend on any vendor tools.

---

## 5. Definitions (Normative)

### 5.1 Interchange Source

An **InterchangeSource** is an external input providing localized message content.

InterchangeSource MUST be treated as an explicit input to the Kernel.

---

### 5.2 Import Mapping

An **ImportMapping** is a declarative mapping from an interchange source’s structure to message semantics:

* MessageKey identity
* LocaleTag
* MessageTemplate
* ParameterSchema (when present)

---

### 5.3 Canonical Message Pack

A **CanonicalMessagePack** is a deterministic representation of:

* message keys and their variants
* parameter schemas
* template structures (render trees / AST)
* metadata required for validation and locale resolution

This specification does not mandate a particular serialization.

---

## 6. Supported Interchange Families (Normative)

Conforming systems MAY support one or more interchange families, including:

* PO-family
* XLIFF-family
* tree-structured document family (records/lists/scalars)
* TMS export artifacts

Supporting an interchange family means defining a deterministic ImportMapping and validation rules for that family.

Interchange families describe classes of external artifacts.
They MUST NOT be construed as canonical representations for Paperhat.

---

## 7. Determinism and Normalization (Normative)

The Kernel MUST apply deterministic normalization, including:

* locale tag normalization (when a normalization policy is provided)
* consistent whitespace and newline normalization for templates (when configured)
* canonical ordering for pack emission

If normalization policies are configurable, they MUST be explicit inputs.

---

## 8. Conflict Handling (Normative)

If an import produces multiple entries that target the same (MessageKey, LocaleTag, SelectorSignature), the Kernel MUST apply an explicit, deterministic conflict policy.

Conflict policies MAY include:

* reject conflicts
* last-writer-wins within a single import (deterministically ordered)
* prefer-source priority order (explicit)

The chosen policy MUST be recorded.

---

## 9. Schema Strategy (Normative)

Because many interchange formats do not carry parameter typing, a conforming system MUST support one of these strategies per import:

* **SchemaProvided**: ParameterSchema is imported as authoritative
* **SchemaRequiredByPack**: import is rejected unless the schema is already declared in the target pack
* **SchemaInferredAsCandidate**: the Kernel infers a candidate schema, but does not treat it as authoritative until accepted into authored artifacts

Schema strategy MUST be explicit.

---

## 10. Validation Requirements (Normative)

The Kernel MUST validate imported content against the message semantics, including:

* keys are valid identities
* locales are valid tokens
* templates compile to valid render-tree structures
* parameter references are consistent with schema strategy
* selection constructs meet completeness requirements

Validation failures MUST produce structured violations.

---

## 11. Provenance and Recordability (Normative)

The Kernel SHOULD record provenance for imported content:

* which interchange source(s) contributed to a message variant
* the mapping and conflict policies used
* validation outcomes

Records MUST NOT include secret material.

---

## 12. Target Independence (Normative)

This specification MUST NOT define:

* a required file format
* an external toolchain
* a database schema
* a query language

Targets may implement imports using any appropriate parsers and tooling, provided semantic meaning, determinism, and validation requirements are preserved.
