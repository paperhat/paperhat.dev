# Codex Authoring Gotchas (DRAFT)

## Status

- **DRAFT**
- Informative
- Applies to humans and LLMs authoring Codex (`.cdx`) files

---

## Purpose

This document lists **common mistakes** made when authoring Codex and explains **why they are invalid**.

Its goals are to:

- reduce frustration during authoring
- prevent repeated validation errors
- reinforce correct mental models
- clarify intent without reintroducing theory

This document introduces **no new rules**.

---

## 1. “Why can’t I add an `id` here?”

Because **identity is intentional**.

- Only Concepts authorized by schema may be Entities.
- Many Concepts (e.g. `Step`, `Description`, `Data`) are **not things** — they are structure or values.
- Giving everything an `id` pollutes the graph and breaks reasoning.

**Rule of thumb:**
If it doesn’t make sense to refer to it independently, it probably must not have an `id`.

---

## 2. “Why does this parse but fail validation?”

Parsing checks **syntax**.
Validation checks **meaning**.

A file can parse correctly but still be invalid because:

- a Trait is not allowed on that Concept
- a required Trait is missing
- a reference points to a non-Entity
- a Concept is used outside its valid context

This is expected and intentional.

---

## 3. “Why can’t I invent a new Concept or Trait?”

Because Codex separates **authoring** from **modeling**.

- Authors use Concepts and Traits
- Schemas define Concepts and Traits

Allowing ad hoc invention would:

- break determinism
- break validation
- make tools disagree about meaning

If something is not documented by a schema, it is not valid Codex.

---

## 4. “Why doesn’t Codex understand my prose?”

Because prose is **Content**, not data.

- Content is preserved verbatim
- Content is not interpreted
- Content is not used for inference

This prevents accidental semantics leaking out of natural language.

If the system needs to reason about something, it must be expressed as **Traits or Concepts**, not prose.

---

## 5. “Why did my comment disappear from the output?”

Because **annotations are not always rendered**.

Codex supports **annotations**, not code-style comments:

- Editorial annotations (`[ ... ]`) are for authors and tooling
- Output annotations (`<Annotation>`) are for intentional downstream visibility

By default:

- `[ ... ]` annotations are preserved for round-tripping but **ignored by HTML, PDF, or voice renderers**
- `<Annotation>` Concepts may be rendered or spoken, depending on the target

If you want something to appear in rendered output, use an explicit `<Annotation>` Concept.

---

## 6. “Why didn’t this `[ ... ]` annotation show up in my CDX?”

It did — just not where you expected.

Editorial annotations:

- attach to the **next Concept**, not the previous one
- are ignored inside Content
- are not inline markup

They behave like **editorial margin notes**, not inline text.

If you need precise attachment or output visibility, use `<Annotation>`.

---

## 7. “Why didn’t Codex recognize my annotation type?”

Because annotation kinds are **enumerated**.

In an editorial annotation:

```
[todo: verify cooking time]
```

The prefix (`todo`) is treated as a kind **only if it is recognized by schema**.

If the prefix is not recognized:

```
[bob says: this sucks]
```

The entire annotation is treated as plain text, not as a typed annotation.

This avoids accidental or ambiguous typing.

---

## 8. “Why can’t I put annotations inside text?”

Because **Content is opaque**.

Inside Content:

- `[ ... ]` is just text
- `<Annotation>` has no meaning
- nothing is parsed or interpreted

This prevents inline markup and avoids HTML-style confusion.

Annotations belong **between Concepts**, not inside prose.

---

## 9. “Why can’t I rely on order here?”

Because **ordering is explicit**.

- Some collections are ordered (e.g. `Steps`)
- Some are unordered (e.g. `Ingredients`)
- Schema decides which is which

Never encode order using:

- numbers
- implicit conventions
- identifiers

If order matters, the schema will say so.

---

## 10. “Why does formatting matter so much?”

Because Codex is **canonical**.

- There is exactly one valid surface form
- Formatting is mechanical, not stylistic
- Canonical form enables round-tripping and stable tooling

If formatting is wrong, the document is invalid — even if the meaning seems obvious.

---

## 11. “Why won’t Codex ‘just fix it’?”

Because silent correction destroys trust.

- Codex tools do not guess
- Codex tools do not auto-correct
- Codex tools do not infer intent

Every change must be explicit and visible.

---

## 12. “Why is Codex so strict?”

Because strictness is what makes everything else possible:

- deterministic compilation
- stable querying
- multiple render targets
- safe automation
- correct LLM assistance

Relaxed rules here would create chaos downstream.

---

## Summary

- Codex is strict by design
- Identity, meaning, and structure are intentional
- Schemas own semantics; authors provide facts
- Prose is preserved but not interpreted
- Annotations are preserved but selectively rendered
- Canonical form is non-negotiable

If Codex rejects something, it is protecting the system — not being pedantic.
