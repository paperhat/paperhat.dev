#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

COVERAGE="notes/design/ontology/fixture-coverage.csv"

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

  if [[ "$enforcement" == "SHACL" ]]; then
    if [[ "$positive" == "N/A" || "$negative" == "N/A" ]]; then
      echo "Fixture coverage check failed: SHACL clause ${clause} cannot use N/A coverage." >&2
      exit 1
    fi
  fi

  if [[ "$positive" != "N/A" && ! -f "$positive" ]]; then
    echo "Fixture coverage check failed: missing positive fixture for ${clause}: ${positive}" >&2
    exit 1
  fi

  if [[ "$negative" != "N/A" && ! -f "$negative" ]]; then
    echo "Fixture coverage check failed: missing negative fixture for ${clause}: ${negative}" >&2
    exit 1
  fi
done

echo "Fixture coverage check passed."
