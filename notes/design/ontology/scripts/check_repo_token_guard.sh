#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_FILE="$SCRIPT_DIR/$(basename "${BASH_SOURCE[0]}")"
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
SCRIPT_REL="${SCRIPT_FILE#"$ROOT_DIR"/}"

# Owner-managed summary note is intentionally excluded from automated
# namespace/token enforcement.
EXCLUDE_GLOBS=(
  --glob "!.git/**"
  --glob "!.venv-ontology/**"
  --glob "!notes/OVERVIEW.md"
  --glob "!$SCRIPT_REL"
)

LEGACY_TOKEN_PATTERN="https://paperhat\\.dev/ns/gd#|https://paperhat\\.dev/ns/gdm#|\\bgd:|\\bgdm:|\\bgd\\b|\\bgdm\\b"

if rg -n "$LEGACY_TOKEN_PATTERN" . "${EXCLUDE_GLOBS[@]}"; then
  echo "Repo token guard failed: found forbidden legacy gd/gdm tokens." >&2
  exit 1
fi

if find . -type f \
  -not -path "./.git/*" \
  -not -path "./.venv-ontology/*" \
  -not -path "./notes/OVERVIEW.md" \
  -not -path "./$SCRIPT_REL" \
  | sed "s#^\\./##" \
  | rg -n "(^|/)gd[-_.]"; then
  echo "Repo token guard failed: found forbidden legacy gd-* file path(s)." >&2
  exit 1
fi

echo "Repo token guard passed."
