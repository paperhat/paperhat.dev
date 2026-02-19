#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

notes/design/ontology/scripts/check_namespaces.sh
notes/design/ontology/scripts/check_shacl_bundle.sh
notes/design/ontology/scripts/check_traceability_matrix.sh
notes/design/ontology/scripts/check_fixture_coverage.sh

# Deprecated stub vocabulary files MUST remain absent.
for f in \
  notes/design/ontology/wd-core-grid.ttl \
  notes/design/ontology/wd-core-figureground.ttl \
  notes/design/ontology/wd-core-closure.ttl
do
  if [[ -e "$f" ]]; then
    echo "Ontology contract check failed: deprecated stub file exists: $f" >&2
    exit 1
  fi
done

echo "Ontology contract checks passed."
