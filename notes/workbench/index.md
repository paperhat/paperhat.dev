# Workbench (Tooling)

Workbench (`@paperhat/workbench`) is Paperhat’s optional **developer tooling** for working with a Paperhat **workspace**.

A workspace is the on-disk unit that contains:

- `modules/` — authored modules (Concepts, Traits, Assemblies, Views, etc.)
- `.paperhat/` — Workbench configuration and dev-mode runtime artifacts (reserved namespace)

Workbench provides a CLI (`paperhat`) for:

- scaffolding a new workspace from templates (e.g. blog, recipes)
- generating boilerplate for authoring artifacts (Concepts, Traits, Assemblies, Views)
- running the Pipeline in dev/watch mode for specific realization targets (HTML app, ebook, PDF, etc.)

Workbench is **not authoritative**.

- Semantics owns meaning (Concepts/Traits and shape validity).
- Pipeline owns deterministic compilation, evaluation, planning, and realization.
- Workbench owns scaffolding and orchestration only.

Paperhat remains valid if Workbench is removed or replaced.
