Status: DRAFT
Lock State: UNLOCKED
Version: 1.0.0

# Workshop TTL/SHACL Migration Plan 1.0.0

## 1. Objective

Resolve Issue 5 by migrating design ontology and metrics TTL/SHACL assets from paperhat.dev into Workshop with a deterministic, explicit target layout.

Target state:

1. Workshop repository contains all migrated `.ttl` and `.shacl.ttl` assets currently staged in paperhat.dev design notes.
2. target layout is explicit, documented, and stable for tooling and conformance references.
3. migration is verifiable by deterministic file inventory and hashes.

## 2. Authority Policy

Policy for this plan:

1. paperhat.dev design notes are the active drafting source during this migration window
2. Workshop repository is updated to incorporate the newer design assets
3. final normative authority remains Workshop specification and Workshop repository artifacts

## 3. Source Inventory (Live)

Source roots:

1. `paperhat.dev/notes/design/ontology/` (ontology + SHACL + fixtures)
2. `paperhat.dev/notes/workshop/design/` (workshop design metrics TTL/SHACL)

Expected migrated file counts:

1. 49 files from `notes/design/ontology/` matching `*.ttl` or `*.shacl.ttl`
2. 2 files from `notes/workshop/design/` matching `*.ttl` or `*.shacl.ttl`
3. total: 51 files

## 4. Fixed Target Layout (Workshop)

All migrated files are placed under:

1. `spec/1.0.0/validation/design/`

Mapping rules:

1. `paperhat.dev/notes/design/ontology/<relpath>` -> `spec/1.0.0/validation/design/ontology/<relpath>`
2. `paperhat.dev/notes/workshop/design/<relpath>` -> `spec/1.0.0/validation/design/workshop/<relpath>`

Required structure:

1. `spec/1.0.0/validation/design/README.md`
2. `spec/1.0.0/validation/design/MIGRATION_MANIFEST.tsv`
3. `spec/1.0.0/validation/design/ontology/` (with fixtures subtree preserved)
4. `spec/1.0.0/validation/design/workshop/`

## 5. Migration Rules

1. preserve file bytes exactly (no content rewrites)
2. preserve relative directory structure beneath each source root
3. generate deterministic manifest with one row per migrated file and SHA-256 hash
4. do not delete paperhat.dev source files in this step

## 6. Manifest Contract

`MIGRATION_MANIFEST.tsv` columns:

1. `source_path`
2. `target_path`
3. `sha256`

Rows must be sorted lexicographically by `target_path`.

## 7. Verification Gates

Migration is complete only if all are true:

1. target file count equals 51
2. every source file has exactly one mapped target file
3. SHA-256 checksums match source vs target for every file
4. README documents target layout and verification command
5. no duplicate or orphan target records exist in manifest

## 8. Execution Sequence

Implement in this order:

1. create target directories under Workshop
2. copy ontology files and fixtures by mapping rule
3. copy workshop design metrics files by mapping rule
4. generate `MIGRATION_MANIFEST.tsv`
5. verify counts and checksums
6. update `spec-updates/index.md` and master plan cross-references

## 9. Deliverables

Required deliverables:

1. migrated TTL/SHACL trees under Workshop target layout
2. `README.md` for migrated design validation assets
3. deterministic `MIGRATION_MANIFEST.tsv`
4. verification output confirming count/hash parity

**End of Workshop TTL/SHACL Migration Plan v1.0.0**
