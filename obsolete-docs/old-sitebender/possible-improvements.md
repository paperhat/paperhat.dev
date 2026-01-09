# Possible README Improvements

This document tracks potential improvements to the Codex README for future
consideration.

## Getting Started Section

The Installation section is minimal. Consider adding a complete quickstart
showing:

```bash
pph new myapp --template=blog
cd myapp
pph dev
```

With a brief walkthrough of what gets generated and how to make a first
modification.

## Performance Characteristics

For users evaluating Paperhat for production use, consider documenting:

- Bundle size impact of Oxigraph WASM in browser deployments
- Compile-time vs runtime characteristics (clarify that the pipeline runs at
  build time, not per-request)
- Memory and query latency benchmarks for typical workloads

## Honest Limitations

Consider adding a section on what Paperhat is NOT ideal for:

- What use cases are better served by simpler tools?
- Where are the current rough edges?

Honesty about limitations builds trust with evaluators.

## Library Description Clarity

Some library descriptions use accessible language ("precision arithmetic,
monads, Help system") while others assume specialist knowledge ("SHACL-aware
generators, metamorphic testing, lazy shrink trees" for Quarrier).

Consider a pass for consistency — either explain the jargon inline or link to
glossary entries.

## Comparison to Alternatives

Experienced developers will ask: "Why this over React + Zod + Prisma? Over
SolidStart? Over Remix?"

Consider a brief comparison highlighting what trade-offs Paperhat makes and
what capabilities it enables that alternatives cannot provide.

## Name Origin

"Paperhat" is unexplained. Consider a brief note on the name's meaning or
origin for the curious.

## Concrete Examples for Abstractions

Some phrases could benefit from concrete examples:

- "Semantic diffs, not text diffs" — what does this actually look like?
- "Federation at query time" — show a simple example
- "Inference engines derive facts you didn't explicitly program" — demonstrate
  with a real case
