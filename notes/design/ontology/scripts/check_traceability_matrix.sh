#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

MATRIX="notes/design/ontology/CANONICAL_RULE_TRACEABILITY.md"

if [[ ! -f "$MATRIX" ]]; then
  echo "Traceability check failed: missing $MATRIX" >&2
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
  if ! rg -q "\\| ${id} \\|" "$MATRIX"; then
    echo "Traceability check failed: missing clause ID ${id}" >&2
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
awk -F'|' '/^\| C[0-9]/{gsub(/ /, "", $2); print $2}' "$MATRIX" > "$TMP_SEEN"

while IFS= read -r clause; do
  [[ -z "$clause" ]] && continue
  if ! rg -q "^${clause}$" "$TMP_REQUIRED"; then
    echo "Traceability check failed: unknown clause ID in matrix: ${clause}" >&2
    exit 1
  fi
done < "$TMP_SEEN"

for id in "${required_ids[@]}"; do
  count="$(rg -n "^${id}$" "$TMP_SEEN" | wc -l | tr -d ' ')"
  if [[ "$count" -ne 1 ]]; then
    echo "Traceability check failed: clause ${id} appears ${count} times (expected exactly 1)." >&2
    exit 1
  fi
done

echo "Traceability check passed."
