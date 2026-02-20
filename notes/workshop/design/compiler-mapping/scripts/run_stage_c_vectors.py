#!/usr/bin/env python3
"""Run Stage C plan emission vectors defined in CDX."""

from __future__ import annotations

import difflib
from pathlib import Path
from xml.etree import ElementTree as ET

from emit_adaptive_plan import EmitError, emit_plan, load_compiled_request, load_stage_a_result, load_stage_b_result
from validate_output_schema import OutputSchemaValidationError, validate_rendered_cdx_against_schema


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EmitError(f"Missing required attribute '{name}' at {path}")
    return value


def _canonical_text(value: str) -> str:
    return value.rstrip() + "\n"


CANONICAL_ONTOLOGY_PREFIX = "spec/1.0.0/validation/design/ontology/"
CANONICAL_WORKSHOP_PREFIX = "spec/1.0.0/validation/design/workshop/"


def _discover_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"Unable to locate repository root from {start}")


def _local_design_roots(script_path: Path) -> tuple[Path, Path]:
    workshop_root = script_path.parents[2]
    ontology_root = script_path.parents[4] / "design" / "ontology"
    return ontology_root, workshop_root


def _resolve_repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve a repo-relative path against paperhat.dev or sibling workshop repo."""
    primary = repo_root / relative_path
    if primary.exists():
        return primary
    sibling_workshop = repo_root.parent / "workshop" / relative_path
    if sibling_workshop.exists():
        return sibling_workshop

    ontology_root, workshop_root = _local_design_roots(Path(__file__).resolve())
    if relative_path.startswith(CANONICAL_ONTOLOGY_PREFIX):
        local_ontology = ontology_root / relative_path[len(CANONICAL_ONTOLOGY_PREFIX) :]
        if local_ontology.exists():
            return local_ontology
    if relative_path.startswith(CANONICAL_WORKSHOP_PREFIX):
        local_workshop = workshop_root / relative_path[len(CANONICAL_WORKSHOP_PREFIX) :]
        if local_workshop.exists():
            return local_workshop
    return primary


def run_vector(path: Path, repo_root: Path) -> tuple[bool, str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return False, f"Malformed StageCVector XML: {exc}"

    if root.tag != "StageCVector":
        return False, f"Root tag must be StageCVector in {path}"

    vector_id = _require_attr(root, "id", "StageCVector")
    compiled_path = _resolve_repo_relative_path(
        repo_root,
        _require_attr(root, "compiledRequestFile", "StageCVector"),
    )
    stage_a_path = _resolve_repo_relative_path(
        repo_root,
        _require_attr(root, "stageAResultFile", "StageCVector"),
    )
    stage_b_path = _resolve_repo_relative_path(
        repo_root,
        _require_attr(root, "stageBResultFile", "StageCVector"),
    )
    expected_path = _resolve_repo_relative_path(
        repo_root,
        _require_attr(root, "expectPlanFile", "StageCVector"),
    )
    schema_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex/adaptive-plan-result.schema.cdx",
    )

    try:
        rendered = emit_plan(
            load_compiled_request(compiled_path),
            load_stage_a_result(stage_a_path),
            load_stage_b_result(stage_b_path),
        )
        validate_rendered_cdx_against_schema(rendered, schema_path)
    except (EmitError, OutputSchemaValidationError) as exc:
        return False, str(exc)

    expected = expected_path.read_text(encoding="utf-8")
    if _canonical_text(rendered) != _canonical_text(expected):
        diff = "\n".join(
            difflib.unified_diff(
                _canonical_text(expected).splitlines(),
                _canonical_text(rendered).splitlines(),
                fromfile=f"expected:{expected_path.name}",
                tofile=f"actual:{path.name}",
                lineterm="",
            )
        )
        return False, f"Rendered plan mismatch for vector '{vector_id}'.\n{diff}"

    return True, vector_id


def main() -> int:
    repo_root = _discover_repo_root(Path(__file__).resolve())
    vector_dir = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/compiler-mapping/stage-c-vectors",
    )
    vectors = sorted(vector_dir.glob("*.cdx"))
    if not vectors:
        print("No Stage C vectors found (.cdx).")
        return 1

    failures = 0
    for path in vectors:
        ok, detail = run_vector(path, repo_root)
        if ok:
            print(f"[PASS] stage-c vector: {path.name}")
        else:
            failures += 1
            print(f"[FAIL] stage-c vector: {path.name}: {detail}")

    if failures:
        print(f"Stage C vectors failed with {failures} failing vector(s).")
        return 1

    print("All Stage C vectors passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
