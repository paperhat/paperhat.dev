#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
find_repo_root() {
  local dir="$1"
  while [[ "$dir" != "/" ]]; do
    if [[ -d "$dir/.git" ]]; then
      printf "%s" "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}
ROOT_DIR="$(find_repo_root "$SCRIPT_DIR")"
if [[ -z "$ROOT_DIR" ]]; then
  echo "Unable to locate repository root from $SCRIPT_DIR" >&2
  exit 1
fi
cd "$ROOT_DIR"

WORKSHOP_ROOT="${WORKSHOP_ROOT:-$ROOT_DIR/../workshop}"
DESIGN_VALIDATION_ROOT="${DESIGN_VALIDATION_ROOT:-$WORKSHOP_ROOT/spec/1.0.0/validation/design}"
ONTOLOGY_ROOT="$DESIGN_VALIDATION_ROOT/ontology"
WORKSHOP_DESIGN_ROOT="$DESIGN_VALIDATION_ROOT/workshop"

# Legacy namespace MUST NOT appear in ontology/SHACL/fixture files.
if rg -n "paperhat\\.example" \
  "$ONTOLOGY_ROOT" \
  "$WORKSHOP_DESIGN_ROOT" \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**'
then
  echo "Namespace check failed: found forbidden legacy namespace paperhat.example" >&2
  exit 1
fi

# Any declared wd: prefix MUST use the canonical namespace.
if rg -n "^@prefix wd:\\s*<" \
  "$ONTOLOGY_ROOT" \
  "$WORKSHOP_DESIGN_ROOT" \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/wd#"
then
  echo "Namespace check failed: found non-canonical wd: prefix declaration." >&2
  exit 1
fi

# Any declared wdm: prefix MUST use the canonical namespace.
if rg -n "^@prefix wdm:\\s*<" \
  "$ONTOLOGY_ROOT" \
  "$WORKSHOP_DESIGN_ROOT" \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/wdm#"
then
  echo "Namespace check failed: found non-canonical wdm: prefix declaration." >&2
  exit 1
fi

# Core namespaces MUST be present in the authority files.
if ! rg -q "https://paperhat\\.dev/ns/wd#" "$ONTOLOGY_ROOT/wd-core.ttl"; then
  echo "Namespace check failed: wd namespace missing from wd-core.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/wdm#" "$WORKSHOP_DESIGN_ROOT/wd-metrics.ttl"; then
  echo "Namespace check failed: wdm namespace missing from wd-metrics.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/wdm#" "$WORKSHOP_DESIGN_ROOT/wd-metrics.shacl.ttl"; then
  echo "Namespace check failed: wdm namespace missing from wd-metrics.shacl.ttl" >&2
  exit 1
fi

echo "Namespace check passed."
