#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
REPO_ROOT="$(cd "$ROOT_DIR/../../.." && pwd)"
INPUT_FILE="$ROOT_DIR/compiler-mapping/fixtures/adaptive-intent-article-homepage.input.cdx"
EXPECTED_FILE="$ROOT_DIR/compiler-mapping/fixtures/adaptive-intent-article-homepage.compiled.cdx"
TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" && -x "$REPO_ROOT/.venv-ontology/bin/python3" ]]; then
  PYTHON_BIN="$REPO_ROOT/.venv-ontology/bin/python3"
fi

if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "Compiler mapping checks require python3." >&2
    exit 1
  fi
fi

"$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/compile_adaptive_intent.py" "$INPUT_FILE" -o "$TMP_FILE"
diff -u "$EXPECTED_FILE" "$TMP_FILE"

PYTHON_BIN="$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_output_schema_checks.sh"
PYTHON_BIN="$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_stage_a_e2e_checks.sh"
PYTHON_BIN="$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_stage_b_vectors.sh"
PYTHON_BIN="$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_stage_c_vectors.sh"
PYTHON_BIN="$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_adaptive_pipeline_e2e_checks.sh"

echo "Compiler mapping checks passed."
