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
if [[ ! -d "$ONTOLOGY_ROOT" ]]; then
  ONTOLOGY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

run_contract_script() {
  local script_name="$1"
  local canonical_script="$ONTOLOGY_ROOT/scripts/$script_name"
  local local_script="$SCRIPT_DIR/$script_name"
  if [[ -x "$canonical_script" ]]; then
    "$canonical_script"
    return
  fi
  if [[ -x "$local_script" ]]; then
    "$local_script"
    return
  fi
  echo "Ontology contract check failed: missing script $script_name" >&2
  exit 1
}

for script_name in \
  check_namespaces.sh \
  check_repo_token_guard.sh \
  check_shacl_bundle.sh \
  check_traceability_matrix.sh \
  check_fixture_coverage.sh
do
  run_contract_script "$script_name"
done

# Deprecated stub vocabulary files MUST remain absent.
for f in \
  "$ONTOLOGY_ROOT/wd-core-grid.ttl" \
  "$ONTOLOGY_ROOT/wd-core-figureground.ttl" \
  "$ONTOLOGY_ROOT/wd-core-closure.ttl"
do
  if [[ -e "$f" ]]; then
    echo "Ontology contract check failed: deprecated stub file exists: $f" >&2
    exit 1
  fi
done

echo "Ontology contract checks passed."
