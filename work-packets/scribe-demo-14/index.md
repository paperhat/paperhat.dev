# Work Packet — Scribe Demo 14

## Scope: One-Command Demo Runner + “Proof” Artifacts (Manifests, Reports, Snapshots)

Status: PROPOSED  
Governing Docs:

* Architect Runtime Contract — Schema Retrieval, Validation, and Default Presentation Bundles (v0.1)
* Essay → HTML Default Rendering Contract (v0.1, WORKING DRAFT)

Inputs:

* All prior demo components (parser, lowering, schema compile, validation, bundles, projection, rendering, site build, theme tokens)

Outputs (in addition to `dist/`):

* `dist/_paperhat/manifest.json` (build manifest)
* `dist/_paperhat/validation-report.json` (aggregated validation summaries)
* `dist/_paperhat/bundles.json` (digests + bundle metadata)
* `dist/_paperhat/viewmodels/essay.json` (golden ViewModel snapshot)
* `dist/_paperhat/viewmodels/recipe.json` (golden ViewModel snapshot, if recipe included)

---

## Objective

Make the demo *easy to run and hard to dispute*:

* one command produces the complete site
* a manifest proves determinism
* bundle digests prove “defaults came from Architect”
* validation summaries prove “schemas enforce correctness”
* ViewModel snapshots prove “projection is deterministic and inspectable”

This packet is the credibility layer that turns a nice demo into a defensible technical proof.

---

## Non-Goals (Explicit)

* Do **not** implement CI.
* Do **not** implement performance optimizations.
* Do **not** implement incremental builds.
* Do **not** implement a GUI.
* Do **not** implement a dev server (static output is enough).

---

## Required Behavior (Normative)

### 1) One command

Provide a single public entry point:

* `runDemoBuild(): Result<{ outputDir: string; digest: string }, BuildError[]>`

This must:

* build the demo site (`dist/`)
* produce proof artifacts under `dist/_paperhat/`
* return a stable digest (sha256 of canonical manifest)

### 2) Manifest

Write `dist/_paperhat/manifest.json` containing:

* build timestamp (optional; if included, must not affect digest)
* list of emitted files (excluding timestamped fields)
* sha256 hash of each file content
* final digest computed from a canonical file list

Canonical ordering:

* sort file paths ascending

Digest computation:

* build a canonical text representation of `path + "\t" + sha256 + "\n"` for each file
* sha256 of that text = overall build digest

### 3) Validation report summary

Write `dist/_paperhat/validation-report.json` containing for each built document:

* `sourcePath`
* `rootConceptName`
* `conforms: boolean`
* `reportDigest`
* `violationCount`

Do not dump verbose engine output. Keep it compact.

### 4) Bundle metadata

Write `dist/_paperhat/bundles.json` including:

* schema bundle digests for `Essay` and `Recipe`
* presentation bundle digests for `Essay+html` and `Recipe+html`
* bundle version and lock state values

This proves defaults and schema are sourced from Architect.

### 5) ViewModel snapshots

Write:

* `dist/_paperhat/viewmodels/essay.json`
* `dist/_paperhat/viewmodels/recipe.json` (if recipe included)

These must be canonical JSON:

* stable key ordering (or stable stringify)
* stable array ordering (already required)

---

## Required Public APIs

* `runDemoBuild()`
* `writeJsonCanonical(path: string, value: unknown): Result<void, WriteError>`
* `computeFileSha256(path: string): string`
* `computeBuildDigest(fileEntries: { path: string; sha256: string }[]): string`

---

## Tests

### A) Smoke run test

* Running `runDemoBuild()` creates:

  * `dist/index.html`
  * `dist/_paperhat/manifest.json`
  * `dist/_paperhat/validation-report.json`
  * `dist/_paperhat/bundles.json`
  * `dist/_paperhat/viewmodels/essay.json`

### B) Determinism

* Run twice with identical inputs:

  * identical `dist/index.html` and page outputs
  * identical ViewModel snapshots
  * identical manifest digest

### C) Tamper detection (manual test)

* Modify one output file and re-run manifest computation:

  * digest changes

---

## Acceptance Criteria

This packet is DONE when:

* You can run one command and get a complete demo + proof artifacts.
* The proof artifacts are compact, inspectable, and deterministic.
* The overall digest is stable across runs.
* Tests pass.

---

## Notes

* This packet is about presentation and credibility, not new semantics.
* Putting proof artifacts inside `dist/_paperhat/` is intentional: you can publish them with the demo site for transparency.
