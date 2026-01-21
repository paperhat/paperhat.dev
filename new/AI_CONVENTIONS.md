Status: INFORMATIVE
Version: 0.1

# AI + Automation Conventions (Paperhat spec repo)

This document is **not part of the Paperhat specification**. It exists to prevent regressions in a multi-session, multi-agent workflow.

## Reality Check (LLM Limitations)

This repo assumes automation may be driven by LLMs.

LLMs can be helpful, but they are not authoritative: they can hallucinate, miss context, produce inconsistent output across sessions, and "helpfully" regress policy.

Therefore:

- Treat chat output as non-authoritative; only committed artifacts + gates count.
- Prefer deterministic checks over intent.
- Require tools/scripts to verify claims.

## Non-Negotiables

### Codex for Configuration, Markdown for Specs

- **Specifications**: MUST be Markdown (`.md`), human-readable but formal and precise.
- **Configuration and schemas**: MUST be Codex (`.cdx`).
- **No legacy formats**: JSON, YAML, TOML, and similar weak formats are forbidden.

### No JSON. Ever.

JSON is a legacy format with well-known limitations. Paperhat uses Codex as its schema definition and configuration language.

- Do not add JSON files to this repo.
- Do not generate JSON output from tools.
- Do not reference JSON Schema for validation.

If a situation appears to require JSON:

1. **Stop.**
2. Explain why Codex cannot serve the purpose.
3. Escalate to update the Codex spec if necessary.

The only acceptable exception is literal impossibility (e.g., an external tool with no alternative that requires JSON input). Such exceptions MUST be:

- documented with the specific external dependency
- marked as **TEMPORARY / compat-only**
- tracked for removal once Codex tooling is available

## Single Source of Truth (Required)

To prevent permanent drift across sessions (human or automated), this repo requires a **single source of truth** for every normative definition.

- A Concept, operator, type, rule, default, error code, or other normative construct MUST be **defined in exactly one place**.
- Any other document that needs to mention that construct MUST:
  - reference the single defining location, and
  - avoid restating the definition (no "duplicate definitions", even if the wording is intended to be identical).

If a document needs to summarize behavior for readability, it MUST do so using non-normative prose and a direct pointer to the defining clause.

When we find duplicated definitions, the fix is always:

1. Pick the canonical defining location.
2. Delete the duplicate text.
3. Replace it with a reference.

## Specification Quality Requirements

Specifications MUST be:

- **Formal**: Use precise language with defined terms.
- **Complete**: No gaps that leave behavior undefined.
- **Consistent**: No contradictions between specifications.
- **Non-redundant**: Each concept defined once (see Single Source of Truth).

When reviewing or creating specifications:

- Cross-reference related specs to check for conflicts.
- Verify all referenced specifications exist.
- Ensure diagnostic codes are defined in Behavior Diagnostic Codes.
- Confirm operator signatures match across vocabulary and encoding specs.

## Verification Rules

- Avoid "speculative edits": if a change is not directly supported by the spec text or a concrete artifact, write a short decision record in Markdown instead of silently changing behavior.
- If a file contains conflict markers (e.g., `<<<<<<<`), resolve them before claiming readiness.
- Every change that claims to improve "readiness" MUST be validated by running the readiness check (once tooling exists).

## Definition of Done ("Production Ready")

**Current state**: Readiness tooling does not yet exist.

**Target state**: "Production ready" means all checks in `tools/readiness_check.py` pass on a clean checkout.

Readiness checks will include:

- [ ] All cross-references resolve to existing specifications
- [ ] All diagnostic codes are defined in Behavior Diagnostic Codes
- [ ] No duplicate definitions across specifications
- [ ] All operator signatures are consistent between vocabulary and encoding specs
- [ ] No JSON files in the repository (except documented compat-only exceptions)
- [ ] All specifications have proper closing markers ("End of ... v0.1")
- [ ] No conflict markers in any file

## File Organization

```
specifications/paperhat.dev/new/
├── AI_CONVENTIONS.md          # This document
├── behavior/                   # Behavior Dialect specifications
│   ├── behavior-dialect/
│   ├── behavior-dialect-semantics/
│   ├── behavior-diagnostic-codes/
│   ├── behavior-program-encoding/
│   ├── behavior-program-surface-form/
│   ├── behavior-vocabulary/    # Operator family specifications
│   ├── predicate-guard-validation-composition/
│   └── value-ordering-and-structural-equality/
└── foundation/                 # Foundation specifications
    ├── enumerated-values/
    └── schema-hierarchy/
```

## Specification Document Structure

Each specification SHOULD follow this structure:

```markdown
Status: NORMATIVE | DRAFT | INFORMATIVE
Lock State: UNLOCKED | LOCKED
Version: 0.1
Editor: [Name]

# [Specification Title]

[Brief description]

This document is **Normative**.

---

## 1. Purpose

[Why this specification exists]

---

## 2-N. [Sections]

[Content organized by topic]

---

## N. Relationship to Other Specifications

[Cross-references to related specs]

---

**End of [Specification Title] v[version]**
```
