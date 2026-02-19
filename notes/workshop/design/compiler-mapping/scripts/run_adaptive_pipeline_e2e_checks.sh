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
    echo "Adaptive pipeline e2e checks require python3." >&2
    exit 1
  fi
fi

if ! "$PYTHON_BIN" - <<'PY'
import importlib.util
import sys
for module in ("rdflib", "pyshacl"):
    if importlib.util.find_spec(module) is None:
        print(f"Missing Python dependency: {module}", file=sys.stderr)
        raise SystemExit(1)
PY
then
  echo "Adaptive pipeline e2e checks require rdflib and pyshacl in the selected Python environment." >&2
  echo "Set PYTHON_BIN or install dependencies in .venv-ontology." >&2
  exit 1
fi

"$PYTHON_BIN" "$ROOT_DIR/compiler-mapping/scripts/run_adaptive_pipeline_e2e_check.py"
