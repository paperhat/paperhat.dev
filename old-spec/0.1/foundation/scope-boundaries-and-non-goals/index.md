Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat 0.1: Scope, Boundaries, and Non-Goals

---

## 1. Purpose

This specification defines the **scope boundaries** and **non-goals** of Paperhat **0.1**.

It exists to:

* prevent accidental scope creep
* align implementers and authors on what Paperhat is and is not
* reduce recurring debates about out-of-scope features
* ensure that “missing features” are not mistaken for “unfinished spec”

This specification is normative.

---

## 2. What Paperhat Is

Paperhat is a **declarative specification system** for describing:

* authored intent (design intent, design policy)
* deterministic behavior graphs (behavior dialect, vocabulary, and encoding)
* validation and shape constraints with structured diagnostics
* portable compilation targets (including SHACL / SHACL-SPARQL)

Paperhat specifications define **formats**, **artifact classes**, and **authoring semantics**.

---

## 3. Boundaries (Normative)

Paperhat 0.1 is bounded by the following constraints.

### 3.1 Closed-world vocabulary

Where a surface vocabulary is defined as closed-world (e.g., predicates, validations, combinators):

* only the operators defined by the normative specs are permitted
* undefined operators MUST be rejected

### 3.2 Determinism as a design requirement

Where semantics are marked LOCKED, implementations:

* MUST produce identical observable results across supported targets
* MUST NOT depend on locale, environment, runtime flags, or host-language quirks

### 3.3 Bounded execution

Paperhat 0.1 is not a general-purpose execution environment.

* Looping and batching are bounded by design and resource limits.
* No part of Paperhat 0.1 is intended to be Turing-complete.

### 3.4 Messaging is explanatory, not punitive

Paperhat diagnostics are designed to help users express intent.

* Validation results MUST be representable as user-facing Help objects.
* User-facing messaging MUST be constructive and non-blaming.

(See the Diagnostic Messaging and Help Philosophy specification.)

---

## 4. Non-Goals (Normative)

Paperhat 0.1 explicitly does not attempt to be any of the following.

### 4.1 Not a general-purpose programming language

Paperhat is not:

* a replacement for JavaScript, Python, Rust, or other general-purpose languages
* a language with arbitrary user-defined functions
* a runtime intended for unconstrained computation

### 4.2 Not a UI widget framework

Paperhat does not define:

* widget libraries
* component lifecycles
* styling systems

Paperhat may describe presentation intent and may define HTML-runtime contracts, but it is not a general UI toolkit.

### 4.3 Not a payment gateway API specification

Commerce-domain specifications define **semantic intent** and canonical meaning (e.g., what a tax intent is), not:

* payment processor APIs
* shipping carrier APIs
* vendor-specific request/response contracts

### 4.4 Adapters are contracts, not implementations

Adapter specifications define:

* the contract surface
* required inputs/outputs
* conformance behavior

They do not define:

* a mandated backend technology
* a reference implementation
* deployment patterns

### 4.5 Not a storage engine specification

Paperhat does not specify:

* a required database engine
* an index engine implementation
* a particular RDF store, SPARQL engine, or vector store product

### 4.6 Not an authorization provider specification

Paperhat security specifications define intent, constraints, and redaction behavior; they do not define:

* a specific identity provider integration
* UI login flows
* proprietary token exchange protocols

---

## 5. Practical Implications

### 5.1 When to add a new spec

A new normative spec SHOULD be added only when:

* an implementation cannot proceed without a missing normative rule, and
* the rule cannot be expressed as a clarification inside an existing specification

### 5.2 When not to add a new spec

A new normative spec SHOULD NOT be added solely to:

* expand feature surface without implementation pressure
* add “best practices” or “advanced usage” guidance
* document optional profiles that are not required for conformance

---

## 6. Conformance

An implementation conforms to Paperhat 0.1 scope boundaries if and only if it:

* rejects out-of-scope constructs where the relevant surface is closed-world
* does not claim conformance based on features that are explicitly non-goals
* preserves determinism and bounded execution properties required by the normative specs

---

**End of Specification**
