Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Paperhat Identifier Canonicalization and Derivation Specification

This specification defines how authored identifier values in Codex (`id` Traits) are interpreted, canonicalized to IRIs, and derived when shorthand forms are used. It forbids filesystem-path-derived identity and guarantees that moving modules does not change identity.

---

## 1. Purpose

This specification exists to:

* make identifiers **author-friendly** while remaining **globally unambiguous**
* support **IRI canonical identity** without forcing authors to type full IRIs
* enable stable cross-document references
* define deterministic, explainable identifier canonicalization
* forbid identity schemes that break when folders move

---

## 2. Scope

This specification governs:

* the interpretation of `id` Trait values in Codex artifacts
* canonical IRI construction rules
* relative identifier resolution for recipe-scoped (or parent-scoped) subresources
* uniqueness and collision handling
* round-trip expectations related to identifier surface forms

This specification does **not** govern:

* schema design for which Concepts require `id`
* naming rules for Concepts or Traits (owned by Codex language specification)
* URL routing or target-specific linking behavior

---

## 3. Definitions

* **Authored ID:** the literal value written by an author in `id="..."`.
* **Canonical IRI:** the fully-qualified identifier used internally by Scribe and emitted into RDF graphs.
* **ID Base:** an absolute IRI prefix used to construct canonical IRIs.
* **Type Segment:** a path segment derived from the Concept type (e.g. `recipe` for `<Recipe>`).
* **Relative ID:** an ID value interpreted relative to a parent canonical IRI (e.g. `step/3`).

---

## 4. Normative Requirements

### 4.1 Canonical Identity is an IRI

All entity identity used for storage and cross-reference MUST be represented as a **canonical IRI**.

Scribe MUST operate on canonical IRIs internally and when emitting RDF.

---

### 4.2 ID Base Declaration (Required)

Canonicalization requires an **ID Base**.

An ID Base MUST be declared in authored Codex, not tool configuration.

A Module MUST declare its ID Base in `module.cdx`.

The ID Base MUST be an absolute IRI ending with `/`.

Example (Illustrative):

```cdx
<Module id="module:recipes" idBase="https://paperhat.dev/id/" />
```

---

### 4.3 Prohibition: No Filesystem-Derived Identity

Scribe MUST NOT derive canonical identity from:

* folder names
* file paths
* directory depth
* filesystem timestamps

Moving or renaming folders MUST NOT change canonical identity.

---

## 5. Authoring Forms

Scribe MUST accept the following authored forms for `id` values.

### 5.1 Absolute IRI

If an authored `id` is an absolute IRI, it MUST be used as the canonical IRI.

Example (Illustrative):

```cdx
<Recipe id="https://paperhat.dev/id/recipe/spaghetti-aglio-e-olio" />
```

---

### 5.2 Root-Local ID (Recommended)

If an authored `id` is a single token without `/`, it is a **local identifier**.

Scribe MUST construct the canonical IRI as:

```
canonical = idBase + typeSegment + "/" + localId
```

Example (Illustrative):

```cdx
<Recipe id="spaghetti-aglio-e-olio" />
```

Canonical (Illustrative):

```
https://paperhat.dev/id/recipe/spaghetti-aglio-e-olio
```

---

### 5.3 Relative ID (Parent-Scoped Subresource)

If an authored `id` contains `/` but is not an absolute IRI, it is a **relative identifier**.

A relative ID MUST be resolved against a parent canonical IRI as:

```
canonical = parentCanonicalIri + "/" + relativeId
```

Example (Illustrative):

```cdx
<Recipe id="spaghetti-aglio-e-olio">
	<Step id="step/3">Serve immediately.</Step>
</Recipe>
```

Canonical Step IRI (Illustrative):

```
https://paperhat.dev/id/recipe/spaghetti-aglio-e-olio/step/3
```

Relative IDs are permitted only where a schema authorizes parent-scoped identity.

---

## 6. Type Segment Rules

### 6.1 Type Segment Derivation (Default)

The Type Segment MUST be derived from the Concept type in a deterministic way.

For v0.1:

* Type Segment is the Concept name lowercased (ASCII), e.g.:

  * `Recipe` → `recipe`
  * `Ingredient` → `ingredient`

If a schema defines an explicit type-segment override, that override takes precedence.

---

## 7. Precedence Rules

When determining canonical identity:

1. Absolute IRIs win.
2. Otherwise, relative IDs resolve against the parent canonical IRI (if permitted by schema).
3. Otherwise, root-local IDs canonicalize using `idBase + typeSegment + "/" + localId`.

No other derivation mechanisms are permitted.

---

## 8. Uniqueness and Collisions

Within a Module revision:

* All canonical IRIs in the Domain Graph MUST be unique for entities.
* All canonical IRIs in the View Graph MUST be unique for view entities.
* All canonical IRIs in the Design Graph MUST be unique for design entities.

If canonicalization produces a collision:

* Scribe MUST emit Help and MUST fail the Module revision (all-or-nothing).

Collision resolution is an authoring responsibility (choose a different localId or provide an absolute IRI).

---

## 9. Validation

* Canonical IRI formation rules are enforced by Scribe during compilation.
* Graph-specific identity constraints MAY be enforced by SHACL, but Scribe MUST reject collisions regardless.

---

## 10. Round-Trip Expectations

Scribe MUST preserve authored surface IDs as authored where possible.

* Canonical IRIs are emitted to RDF.
* Round-tripped CDX MAY preserve the authored form (absolute, local, or relative) provided the canonical IRI would be identical.
* Canonical formatting applies independently of ID surface form.

This specification does not require Scribe to rewrite authored IDs.

---

## 11. Examples (Illustrative)

### 11.1 Root Entity (Local ID)

```cdx
<Recipe id="spaghetti-aglio-e-olio" title="Spaghetti Aglio e Olio" />
```

### 11.2 Parent-Scoped Subresource (Relative ID)

```cdx
<Recipe id="spaghetti-aglio-e-olio">
	<Step id="step/1">Boil water.</Step>
</Recipe>
```

---

## 12. Non-Goals

This specification does not:

* define URL routing
* define hyperlink behavior
* define how IDs are presented to users
* define how UIs generate IDs

It defines only canonicalization and identity rules.

---

## 13. Summary

* Canonical identity is a full IRI.
* Authors may write short IDs.
* Modules declare an `idBase`.
* Type segments are derived deterministically.
* Relative IDs allow parent-scoped subresources.
* Identity MUST NOT be derived from filesystem paths.
* Collisions fail the module revision.

---

**End of Paperhat Identifier Canonicalization and Derivation Specification v0.1**
