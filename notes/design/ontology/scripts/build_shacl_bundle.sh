#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ONTOLOGY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LIST_FILE="$ONTOLOGY_DIR/shacl-bundle-files.txt"
OUT_FILE="${1:-$ONTOLOGY_DIR/wd-all.shacl.ttl}"

{
  cat <<'EOF'
@prefix wd: <https://paperhat.dev/ns/wd#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#####################################################################
# wd-all.shacl.ttl
#
# Canonical SHACL validation bundle entrypoint for the Workshop
# design ontology core constraints.
#
# Generated from files listed in shacl-bundle-files.txt using
# scripts/build_shacl_bundle.sh.
#####################################################################

EOF

  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    printf "\n#####################################################################\n"
    printf "# BEGIN %s\n" "$rel"
    printf "#####################################################################\n\n"
    cat "$ONTOLOGY_DIR/$rel"
    printf "\n#####################################################################\n"
    printf "# END %s\n" "$rel"
    printf "#####################################################################\n"
  done < "$LIST_FILE"
} > "$OUT_FILE"

echo "Wrote $OUT_FILE"
