#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

# Legacy namespace MUST NOT appear in non-test files.
if rg -n "paperhat\\.example" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '!**/fixtures/**' \
  --glob '!**/tests/**'
then
  echo "Namespace check failed: found forbidden legacy namespace paperhat.example" >&2
  exit 1
fi

# Core namespaces MUST be the paperhat.dev namespaces.
if ! rg -q "https://paperhat\\.dev/ns/gd#" notes/design/ontology/gd-core.ttl; then
  echo "Namespace check failed: gd namespace missing from gd-core.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/gdm#" notes/workshop/design/gd-metrics.ttl; then
  echo "Namespace check failed: gdm namespace missing from gd-metrics.ttl" >&2
  exit 1
fi

echo "Namespace check passed."
