#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPO_ROOT="$(cd "$ROOT_DIR/../../.." && pwd)"

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" && -x "$REPO_ROOT/.venv-ontology/bin/python3" ]]; then
  PYTHON_BIN="$REPO_ROOT/.venv-ontology/bin/python3"
fi

if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "Stage C vector checks require python3." >&2
    exit 1
  fi
fi

"$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_stage_c_vectors.py"
