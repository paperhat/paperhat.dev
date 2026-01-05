# LLM Roles and Limits (LOCKED)

This project uses LLMs to write code. To prevent drift and catastrophic mistakes, LLMs operate under strict roles.

This document is **normative**.

---

## 1. Roles

### A) Architect (Human Owner)

The sole stakeholder and approver.

Owns:

- priorities
- contracts
- acceptance criteria
- final merges/commits

Only the Architect may:

- commit
- merge
- release
- perform any history-altering git operations

---

### B) Spec Writer (High-Capability LLM)

Produces and updates:

- canonical documents (global + library-local)
- work packets
- ownership boundaries
- contract amendments

Spec Writer may:

- propose contract changes
- rewrite canonical docs when meaning changes
- create cross-cutting work packets in codex (only when needed)

Spec Writer must:

- follow DOC_GOVERNANCE
- update existing canon, not create competing docs
- keep library contracts “need-to-know only”

---

### C) Implementer (Cheap/Restricted LLM)

Implements code strictly inside a work packet.

Implementer may only:

- modify files explicitly listed in the active work packet
- add files explicitly listed in the work packet
- add tests explicitly required by the work packet

Implementer must never:

- create new docs (other than editing the work packet if instructed)
- refactor unrelated code
- change folder architecture
- change contracts
- introduce new libraries/modules not specified
- inspect monad internals
- introduce exceptions/mutation/loops outside Toolsmith rules

If requirements are missing or unclear:

- Implementer must stop and report the blockage, not “guess and invent.”

---

## 2. Required Reading Order (Hard)

Before any implementation work:

1. `codex/docs/canonical/CANON_INDEX.md`
2. `codex/docs/canonical/DOC_GOVERNANCE.md`
3. `codex/docs/canonical/LLM_ROLES_AND_LIMITS.md`
4. `codex/docs/canonical/CODEX_SYSTEM_CONTRACT.md` (once available)
5. `<library>/docs/canonical/CONTRACT.md`
6. `<library>/docs/work-packets/<packet>.md`

---

## 3. Git Restrictions (Hard)

Implementer LLMs must not run:

- `git reset` (any form)
- `git rebase`
- `git push --force`
- `git commit`
- `git clean`
- any command that rewrites history or deletes untracked work

Implementers may:

- read `git diff` output provided by the Architect
- reason about diffs
- propose patch content

The Architect remains the only committer.

---

## 4. Document Discipline (Hard)

LLMs must:

- update canonical docs in place
- archive old versions only when meaning changes
- never create “extra” plans

Work packets are the only routine new documents.

---

## Status

LOCKED.
