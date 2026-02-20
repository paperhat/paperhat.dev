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
POLICY_VECTOR_RUNNER="$WORKSHOP_ROOT/spec/1.0.0/validation/design/ontology/scripts/policy_vector_runner.py"
if [[ ! -f "$POLICY_VECTOR_RUNNER" ]]; then
  POLICY_VECTOR_RUNNER="$SCRIPT_DIR/policy_vector_runner.py"
fi

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" && -x "$ROOT_DIR/.venv-ontology/bin/python3" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv-ontology/bin/python3"
fi

if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "Policy vector runner requires python3." >&2
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
  echo "Policy vector runner requires rdflib and pyshacl in the selected Python environment." >&2
  echo "Set PYTHON_BIN or install dependencies in .venv-ontology." >&2
  exit 1
fi

"$PYTHON_BIN" "$POLICY_VECTOR_RUNNER" "$@"
