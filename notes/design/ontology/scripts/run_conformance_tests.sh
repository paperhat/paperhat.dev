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
POLICY_VECTOR_SCRIPT="$WORKSHOP_ROOT/spec/1.0.0/validation/design/ontology/scripts/run_policy_vectors.sh"
PROC_CONFORMANCE_SCRIPT="$WORKSHOP_ROOT/spec/1.0.0/validation/design/ontology/scripts/run_proc_conformance_tests.sh"
if [[ ! -f "$POLICY_VECTOR_SCRIPT" ]]; then
  POLICY_VECTOR_SCRIPT="$SCRIPT_DIR/run_policy_vectors.sh"
fi
if [[ ! -f "$PROC_CONFORMANCE_SCRIPT" ]]; then
  PROC_CONFORMANCE_SCRIPT="$SCRIPT_DIR/run_proc_conformance_tests.sh"
fi

if ! command -v pyshacl >/dev/null 2>&1; then
  if [[ -x "$ROOT_DIR/.venv-ontology/bin/pyshacl" ]]; then
    PATH="$ROOT_DIR/.venv-ontology/bin:$PATH"
  fi
fi

if ! command -v pyshacl >/dev/null 2>&1; then
  echo "Conformance test runner requires pyshacl on PATH." >&2
  echo "Install with: python3 -m pip install pyshacl" >&2
  exit 1
fi

CORE_SHAPES="$DESIGN_VALIDATION_ROOT/ontology/wd-all.shacl.ttl"
CORE_ONTOLOGY="$DESIGN_VALIDATION_ROOT/ontology/wd-core.ttl"
METRICS_SHAPES="$DESIGN_VALIDATION_ROOT/workshop/wd-metrics.shacl.ttl"
METRICS_ONTOLOGY_TMP="$(mktemp)"

cleanup() {
  rm -f "$METRICS_ONTOLOGY_TMP"
}
trap cleanup EXIT

cat "$CORE_ONTOLOGY" "$DESIGN_VALIDATION_ROOT/workshop/wd-metrics.ttl" > "$METRICS_ONTOLOGY_TMP"

run_case() {
  local mode="$1"
  local name="$2"
  local shapes="$3"
  local ontology="$4"
  local data="$5"

  if pyshacl -s "$shapes" -e "$ontology" -i rdfs "$data" >/tmp/pyshacl.out 2>/tmp/pyshacl.err; then
    if [[ "$mode" == "valid" ]]; then
      echo "[PASS] $name"
    else
      echo "[FAIL] $name (expected invalid but validation passed)" >&2
      cat /tmp/pyshacl.out >&2 || true
      cat /tmp/pyshacl.err >&2 || true
      exit 1
    fi
  else
    if [[ "$mode" == "invalid" ]]; then
      echo "[PASS] $name"
    else
      echo "[FAIL] $name (expected valid but validation failed)" >&2
      cat /tmp/pyshacl.out >&2 || true
      cat /tmp/pyshacl.err >&2 || true
      exit 1
    fi
  fi
}

echo "Running core valid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/core/valid/*.ttl; do
  run_case "valid" "core valid: $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
done

echo "Running core invalid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/core/invalid/*.ttl; do
  run_case "invalid" "core invalid: $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
done

echo "Running policy valid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/policy/valid/*.ttl; do
  run_case "valid" "policy valid: $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
done

echo "Running policy invalid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/policy/invalid/*.ttl; do
  run_case "invalid" "policy invalid: $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
done

echo "Running metrics valid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/metrics/valid/*.ttl; do
  run_case "valid" "metrics valid (core pass): $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
  run_case "valid" "metrics valid (metrics pass): $(basename "$f")" "$METRICS_SHAPES" "$METRICS_ONTOLOGY_TMP" "$f"
done

echo "Running metrics invalid fixtures..."
for f in "$DESIGN_VALIDATION_ROOT"/ontology/fixtures/metrics/invalid/*.ttl; do
  run_case "valid" "metrics invalid (core pass): $(basename "$f")" "$CORE_SHAPES" "$CORE_ONTOLOGY" "$f"
  run_case "invalid" "metrics invalid (metrics fail): $(basename "$f")" "$METRICS_SHAPES" "$METRICS_ONTOLOGY_TMP" "$f"
done

echo "Running policy evaluation vectors..."
"$POLICY_VECTOR_SCRIPT"

echo "Running procedural conformance vectors..."
"$PROC_CONFORMANCE_SCRIPT"

echo "All conformance tests passed."
