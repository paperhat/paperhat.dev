### Paperhat is a semantic authoring system, not a web framework

Paperhat exists because the Web abandoned the idea that authored documents should be **structurally rigorous, semantically explicit, and machine-verifiable**.

Rather than attempting to re-impose those constraints on browsers — which are necessarily tolerant, error-recovering, and profit-driven — Paperhat restores rigor **upstream**, at authoring and compilation time.

Authors write in **Codex**, a declarative semantic language in which:

* Concepts are explicit (OWL-class-level, not implicit DOM tags)
* Traits are typed and governed
* Structure is validated deterministically
* Meaning is independent of presentation, runtime, or target platform

HTML, PDF, SVG, EPUB, LaTeX, and other outputs are treated as **serialization targets**, not as the source of truth.

In this sense, Paperhat revives the *intent* behind XML and XHTML — precise, self-describing documents — while avoiding the brittleness that made runtime XML parsing unsuitable for the open web.

The browser is not asked to enforce correctness.
The compiler already has.

---

### Why HTML is still a target

HTML is the dominant interchange format of the Web. Paperhat embraces this reality without inheriting HTML’s semantic weaknesses.

When targeting HTML, Paperhat emits explicit semantic provenance (e.g. via reserved `data-paperhat` metadata), allowing:

* introspection
* tooling
* hydration
* accessibility mapping
* round-trip traceability

…without relying on browser-level semantics that were never designed for this purpose.

Paperhat does not attempt to “fix HTML.”
It renders *past* it.
