# Work Packet — Scribe Demo 16

## Scope: Freeze Demo v0.1 + Guardrails for LLM-Assisted Development (Work Packets, Contracts, No-Guessing)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs:

* All demo code and specs produced in Demo 01–15

Outputs:

* `DEMO_V0_1.md` (single-page “what is frozen” declaration)
* `AGENT_RULES.md` (LLM guardrails for this repo)
* `WORK_PACKETS.md` (index of approved packets + status)
* Locked tags or markers for demo artifacts (code + specs)

---

## Objective

Turn the demo from “works on my machine” into **a controlled, repeatable system** that LLMs can help with safely.

This packet:

* freezes *behavior*, not ideology
* defines what LLMs may and may not do
* prevents silent semantic drift
* preserves determinism and trust

This is how you keep the 20% effectiveness from collapsing into chaos.

---

## Non-Goals (Explicit)

* Do **not** refactor demo code.
* Do **not** expand scope or add features.
* Do **not** change schemas, rendering contracts, or defaults.
* Do **not** optimize performance.

This is about **control**, not capability.

---

## Deliverable A: `DEMO_V0_1.md`

A single authoritative document that states:

### 1) What is frozen

* Essay → HTML default rendering behavior
* Recipe → HTML default rendering behavior
* Asset inclusion semantics
* Schema authoring in Codex → SHACL compilation
* Determinism guarantees

### 2) What is explicitly *not* frozen

* Additional Concepts
* Additional targets (PDF, XML, etc.)
* Additional DesignPolicy features
* Alternate Views

### 3) What counts as a breaking change

Examples:

* changing ViewModel shape
* changing default HTML element mapping
* changing asset dependency ordering
* changing validation semantics

### 4) How changes must be made

* new spec version
* new Work Packet
* never “just fix it”

This document is **informative**, but treated as operationally binding for the demo.

---

## Deliverable B: `AGENT_RULES.md`

This is critical.

Define **hard constraints** for LLM-assisted work:

### Mandatory rules (normative)

* LLMs MUST NOT invent Concepts, Traits, or predicates.
* LLMs MUST NOT modify locked contracts.
* LLMs MUST NOT refactor without an explicit Work Packet.
* LLMs MUST ask when information is missing.
* LLMs MUST operate on one Work Packet at a time.

### Prohibited behavior

* guessing schema semantics
* “improving” naming
* introducing shortcuts
* changing ordering semantics
* silently fixing tests

### Required workflow

* read the governing docs listed in the Work Packet
* implement exactly the authorized scope
* stop when scope is complete

This document is what you hand to Copilot / Claude / Opus / etc.

---

## Deliverable C: `WORK_PACKETS.md`

An index file listing:

* Demo 01 → Demo 16
* short description
* status: `DONE | IN PROGRESS | PLANNED`
* governing docs for each packet

This becomes the **canonical task ledger**.

Example entry:

```
Demo 08 — End-to-End Essay Build
Status: DONE
Governing Docs:
- Essay → HTML Default Rendering Contract v0.1
- Architect Runtime Contract v0.1
```

---

## Deliverable D: Lock markers

Add explicit markers (not necessarily Git tags yet) indicating:

* which specs are considered stable for demo
* which directories are “demo-frozen”

Example:

* `spec/0.1/` → stable
* `demo/` → frozen behavior
* `docs/` → informative only

This prevents accidental edits during iteration.

---

## Required Public API (Minimal)

* `assertDemoFrozen(): void`

  * fails loudly if a frozen artifact is modified without version bump
  * may be a simple checksum comparison for demo purposes

(Implementation can be light; intent matters more than machinery.)

---

## Tests

### A) Process tests (manual/structural)

* New Work Packet required to change a frozen artifact.
* AGENT_RULES.md is present and readable.

### B) Determinism regression test

* Re-run Demo 14 build:

  * identical digest
  * identical proof artifacts

---

## Acceptance Criteria

This packet is DONE when:

* You can point an LLM at the repo and it **cannot** plausibly wreck it without violating explicit written rules.
* The demo’s behavior is frozen and defensible.
* Future work is clearly separated from demo v0.1.

---

## Notes

* This packet is what turns “visionary prototype” into “serious system.”
* After this, you can:

  * iterate safely
  * invite collaborators
  * or walk away for a month and come back without entropy

---

If you want, the **next** logical step after this is **Demo 17: second target (PDF or XML) using the *same* pipeline**, to prove the multi-target claim.
