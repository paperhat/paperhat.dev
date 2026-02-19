#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

# Legacy namespace MUST NOT appear in ontology/SHACL/fixture files.
if rg -n "paperhat\\.example" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**'
then
  echo "Namespace check failed: found forbidden legacy namespace paperhat.example" >&2
  exit 1
fi

# Any declared gd: prefix MUST use the canonical namespace.
if rg -n "^@prefix gd:\\s*<" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/gd#"
then
  echo "Namespace check failed: found non-canonical gd: prefix declaration." >&2
  exit 1
fi

# Any declared gdm: prefix MUST use the canonical namespace.
if rg -n "^@prefix gdm:\\s*<" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/gdm#"
then
  echo "Namespace check failed: found non-canonical gdm: prefix declaration." >&2
  exit 1
fi

# Core namespaces MUST be present in the authority files.
if ! rg -q "https://paperhat\\.dev/ns/gd#" notes/design/ontology/gd-core.ttl; then
  echo "Namespace check failed: gd namespace missing from gd-core.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/gdm#" notes/workshop/design/gd-metrics.ttl; then
  echo "Namespace check failed: gdm namespace missing from gd-metrics.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/gdm#" notes/workshop/design/gd-metrics.shacl.ttl; then
  echo "Namespace check failed: gdm namespace missing from gd-metrics.shacl.ttl" >&2
  exit 1
fi

echo "Namespace check passed."
