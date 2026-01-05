# Documentation Governance (LOCKED)

This project maintains a single canonical documentation set to prevent drift, duplication, and LLM-generated sprawl.

This document is **normative**.

---

## 1. Canonical Sources of Truth

### Global canon

- `codex/docs/canonical/` (authoritative)

### Library-local canon

- `<library>/docs/canonical/CONTRACT.md` (authoritative for that library only)

### Work packets

- `<library>/docs/work-packets/` (task-scoped, temporary)
- `codex/docs/work-packets/` (cross-cutting only, optional)

Everything else is non-canonical.

---

## 2. Update, Don’t Create (Hard Rule)

If a canonical document exists for a topic:

- you **must update it**
- you **must not** create a new competing doc
- you **must not** create “v2”, “final”, “revamp”, “new plan”, etc.

Canonical docs are living contracts.

---

## 3. One Canonical Document Per Topic (Hard Rule)

Each topic has exactly one canonical file.

If multiple documents exist for the same topic:

- pick one as canonical
- archive the rest

---

## 4. Archiving and Rewrites

### 4.1 Read-only archive

Archived docs are stored under:

- `codex/docs/old-docs/`
- `<library>/docs/old-sitebender/` (temporary staging during cleanup)

Archived docs are read-only by convention.

### 4.2 Rewrite policy (Hard)

When a canonical document’s meaning changes substantially:

1. Rewrite the canonical doc cleanly (do not patch endlessly).
2. Move the prior version into old-docs with a version tag:

`@vYYYY-MM-DD_<short-slug>.md`

### 4.3 What does NOT trigger archiving

- spelling
- wording improvements
- clarifications that do not change meaning
- formatting

Only archive when the contract meaning changes.

---

## 5. Work Packets Are the Only Allowed New Docs

Work packets are the only documents that may be created routinely.

Rules:

- Must live under `docs/work-packets/` (kebab case).
- Must be small, task-scoped, and disposable.
- Must never become “documentation.”
- Must be marked `Status: DONE` or `Status: ABANDONED`.

---

## 6. No Junk Drawers (Hard Rule)

No “plans” folders.
No “notes” folders.
No “misc” folders.

If a document cannot be classified as canonical, work-packet, or old-docs, it should not exist.

---

## 7. Git Safety Policy (Hard Rule)

- Only the repository owner commits changes.
- Implementer LLMs must never run destructive git operations:
  - reset / rebase / force-push / reflog surgery

- LLMs may review diffs/status when provided by the owner.

---

## Status

LOCKED.
