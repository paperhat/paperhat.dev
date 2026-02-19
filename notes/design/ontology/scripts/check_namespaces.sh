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

# Any declared wd: prefix MUST use the canonical namespace.
if rg -n "^@prefix wd:\\s*<" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/wd#"
then
  echo "Namespace check failed: found non-canonical wd: prefix declaration." >&2
  exit 1
fi

# Any declared wdm: prefix MUST use the canonical namespace.
if rg -n "^@prefix wdm:\\s*<" \
  notes/design/ontology \
  notes/workshop/design \
  --glob '*.ttl' \
  --glob '*.shacl.ttl' \
  --glob '!**/tests/**' \
  | rg -v "https://paperhat\\.dev/ns/wdm#"
then
  echo "Namespace check failed: found non-canonical wdm: prefix declaration." >&2
  exit 1
fi

# Core namespaces MUST be present in the authority files.
if ! rg -q "https://paperhat\\.dev/ns/wd#" notes/design/ontology/wd-core.ttl; then
  echo "Namespace check failed: wd namespace missing from wd-core.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/wdm#" notes/workshop/design/wd-metrics.ttl; then
  echo "Namespace check failed: wdm namespace missing from wd-metrics.ttl" >&2
  exit 1
fi

if ! rg -q "https://paperhat\\.dev/ns/wdm#" notes/workshop/design/wd-metrics.shacl.ttl; then
  echo "Namespace check failed: wdm namespace missing from wd-metrics.shacl.ttl" >&2
  exit 1
fi

echo "Namespace check passed."
