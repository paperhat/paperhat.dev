# Codex Canon Index (LOCKED)

This folder contains the **single authoritative global canon** for all Paperhat libraries and generated applications.

- **Authoritative global canon lives here:** `codex/docs/canonical/`
- **Library-local canon lives in each repo:** `docs/canonical/CONTRACT.md`
- **Work packets live in each repo:** `docs/work-packets/`
- **Archived docs live here:** `codex/docs/old-docs/` (read-only by convention)

No other location is authoritative.

---

## 1. Canonical Documents

### Required (global)

1. **DOC_GOVERNANCE.md**
   Rules that prevent document drift and duplication.

2. **LLM_ROLES_AND_LIMITS.md**
   Defines allowed behaviors for Spec Writer vs Implementer LLMs and prohibits dangerous git operations.

3. **CODEX_SYSTEM_CONTRACT.md**
   Global system invariants: philosophy, purity/IO, help system, newtypes, folder privacy rules, Scribe pipeline, runtime model.

4. **OWNERSHIP.md**
   Hard boundaries: which library owns which responsibilities, and what it explicitly does not own.

5. **TOOLSMITH_EXTENSION_POLICY.md**
   What belongs in Toolsmith vs libraries, and how libraries extend help/types without duplicating kernels.

6. **WORK_PACKET_TEMPLATE.md** _(optional; may be global)_
   Template for “need-to-know only” packets for implementer LLMs.

---

## 2. Reading Order (Hard)

### For any work on any library

1. Read: `codex/docs/canonical/DOC_GOVERNANCE.md`
2. Read: `codex/docs/canonical/LLM_ROLES_AND_LIMITS.md`
3. Read: `codex/docs/canonical/CODEX_SYSTEM_CONTRACT.md` _(once available)_
4. Read: `<library>/docs/canonical/CONTRACT.md`
5. Read: `<library>/docs/work-packets/<packet>.md` (if implementing)

---

## 3. Canonical Rule (Hard)

- There is exactly **one** canonical document per topic.
- Canonical documents are updated **in place**.
- When the meaning changes substantially, the old document is archived (see governance).

---

## Status

LOCKED.
