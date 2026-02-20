#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ONTOLOGY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUNDLE_FILE="$ONTOLOGY_DIR/wd-all.shacl.ttl"
TMP_FILE="$(mktemp)"

cleanup() {
  rm -f "$TMP_FILE"
}
trap cleanup EXIT

"$SCRIPT_DIR/build_shacl_bundle.sh" "$TMP_FILE" >/dev/null

if [[ ! -f "$BUNDLE_FILE" ]]; then
  echo "SHACL bundle check failed: $BUNDLE_FILE does not exist." >&2
  echo "Run $SCRIPT_DIR/build_shacl_bundle.sh." >&2
  exit 1
fi

if ! cmp -s "$BUNDLE_FILE" "$TMP_FILE"; then
  echo "SHACL bundle check failed: wd-all.shacl.ttl is out of sync." >&2
  echo "Run $SCRIPT_DIR/build_shacl_bundle.sh and update the bundle file." >&2
  exit 1
fi

echo "SHACL bundle check passed."
