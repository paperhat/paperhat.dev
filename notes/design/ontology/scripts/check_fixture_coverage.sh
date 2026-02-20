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
WORKSHOP_DESIGN_ROOT="$DESIGN_VALIDATION_ROOT/workshop"
if [[ ! -d "$WORKSHOP_DESIGN_ROOT" ]]; then
  if [[ -d "$ONTOLOGY_ROOT/../workshop" ]]; then
    WORKSHOP_DESIGN_ROOT="$(cd "$ONTOLOGY_ROOT/../workshop" && pwd)"
  elif [[ -d "$ONTOLOGY_ROOT/../../workshop/design" ]]; then
    WORKSHOP_DESIGN_ROOT="$(cd "$ONTOLOGY_ROOT/../../workshop/design" && pwd)"
  fi
fi
COVERAGE="$ONTOLOGY_ROOT/fixture-coverage.csv"

if [[ ! -f "$COVERAGE" ]]; then
  echo "Fixture coverage check failed: missing $COVERAGE" >&2
  exit 1
fi

required_ids=(
  C2.1-1 C2.2-1 C2.3-1
  C3.1-1 C3.1-2 C3.1-3 C3.1-4
  C3.2-1 C3.2-2 C3.2-3 C3.2-4 C3.2-5 C3.2-6 C3.2-7
  C3.3-1 C3.3-2 C3.3-3 C3.3-4
  C3.4-1 C3.4-2 C3.4-3 C3.4-4 C3.4-5 C3.4-6
  C3.5-1 C3.5-2 C3.5-3 C3.5-4 C3.5-5
  C3.6-1 C3.6-2 C3.6-3 C3.6-4 C3.6-5
  C3.7-1 C3.7-2 C3.7-3 C3.7-4 C3.7-5 C3.7-6
  C3.8-1 C3.8-2 C3.8-3 C3.8-4 C3.8-5
  C4.1-1 C4.2-1 C4.3-1
  C5.1-1 C5.1-2 C5.2-1 C5.3-1 C5.4-1
  C6-1 C6-2
)

missing=0
for id in "${required_ids[@]}"; do
  if ! rg -q "^${id}," "$COVERAGE"; then
    echo "Fixture coverage check failed: missing coverage row for ${id}" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

TMP_REQUIRED="$(mktemp)"
TMP_SEEN="$(mktemp)"
cleanup() {
  rm -f "$TMP_REQUIRED" "$TMP_SEEN"
}
trap cleanup EXIT

printf "%s\n" "${required_ids[@]}" > "$TMP_REQUIRED"
tail -n +2 "$COVERAGE" | cut -d',' -f1 > "$TMP_SEEN"

while IFS= read -r clause; do
  [[ -z "$clause" ]] && continue
  if ! rg -q "^${clause}$" "$TMP_REQUIRED"; then
    echo "Fixture coverage check failed: unknown clause ID in coverage file: ${clause}" >&2
    exit 1
  fi
done < "$TMP_SEEN"

for id in "${required_ids[@]}"; do
  count="$(rg -n "^${id}$" "$TMP_SEEN" | wc -l | tr -d ' ')"
  if [[ "$count" -ne 1 ]]; then
    echo "Fixture coverage check failed: clause ${id} appears ${count} times (expected exactly 1)." >&2
    exit 1
  fi
done

tail -n +2 "$COVERAGE" | while IFS=',' read -r clause enforcement positive negative; do
  [[ -z "$clause" ]] && continue

  resolve_fixture_path() {
    local rel="$1"
    local canonical_ontology_prefix="spec/1.0.0/validation/design/ontology/"
    local canonical_workshop_prefix="spec/1.0.0/validation/design/workshop/"
    if [[ "$rel" == spec/* ]]; then
      local workshop_candidate="$WORKSHOP_ROOT/$rel"
      if [[ -f "$workshop_candidate" ]]; then
        printf "%s" "$workshop_candidate"
        return
      fi

      if [[ "$rel" == "$canonical_ontology_prefix"* ]]; then
        local local_ontology_candidate="$ONTOLOGY_ROOT/${rel#"$canonical_ontology_prefix"}"
        if [[ -f "$local_ontology_candidate" ]]; then
          printf "%s" "$local_ontology_candidate"
          return
        fi
      fi

      if [[ "$rel" == "$canonical_workshop_prefix"* ]]; then
        local local_workshop_candidate="$WORKSHOP_DESIGN_ROOT/${rel#"$canonical_workshop_prefix"}"
        if [[ -f "$local_workshop_candidate" ]]; then
          printf "%s" "$local_workshop_candidate"
          return
        fi
      fi

      printf "%s" "$workshop_candidate"
      return
    fi
    printf "%s/%s" "$ROOT_DIR" "$rel"
  }

  if [[ "$positive" == "N/A" || "$negative" == "N/A" ]]; then
    echo "Fixture coverage check failed: clause ${clause} cannot use N/A coverage." >&2
    exit 1
  fi

  positive_path="$(resolve_fixture_path "$positive")"
  negative_path="$(resolve_fixture_path "$negative")"

  if [[ ! -f "$positive_path" ]]; then
    echo "Fixture coverage check failed: missing positive fixture for ${clause}: ${positive}" >&2
    exit 1
  fi

  if [[ ! -f "$negative_path" ]]; then
    echo "Fixture coverage check failed: missing negative fixture for ${clause}: ${negative}" >&2
    exit 1
  fi
done

echo "Fixture coverage check passed."
