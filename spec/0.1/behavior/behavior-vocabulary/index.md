Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Behavior Vocabulary

This specification defines the **Behavior Vocabulary** for Paperhat: the closed set of Concepts (operators, predicates, formatters, constructors, and type/domain helpers) usable by Behavior Programs.

This document is **Normative**.

---

## 1. Purpose

This spec exists to define:

- the canonical operator inventory for v0.1
- per-operator meaning, domains, and error behavior
- operator families (math, comparison, text, temporal, formatting, shapes/validation)

This spec does not define:

- the evaluation model (see Behavior Dialect — Semantics)
- program surface form / encoding (see Behavior Program Surface Form)

---

## 2. General Operator Contract (Normative)

For every operator Concept defined in this document, the spec MUST include:

- **Name** (stable, human-readable, no abbreviations)
- **Arity** (fixed or variadic, with minimum)
- **Domains** (accepted input types/domains)
- **Result type/domain**
- **Semantics** (precise meaning)
- **Error behavior** (what becomes `Invalid`, and with what diagnostic codes)
- **Special cases** (empty inputs, NaN/infinities, boundary conditions)

---

## 3. Operator Families (Normative)

### 3.1 Math

See [math/index.md](math/index.md).

### 3.2 Relational and predicates

(TBD)

### 3.3 Text

(TBD)

### 3.4 Temporal

(TBD)

### 3.5 Formatting

(TBD)

### 3.6 Data shapes and validation

(TBD)

---

**End of Behavior Vocabulary v0.1**
