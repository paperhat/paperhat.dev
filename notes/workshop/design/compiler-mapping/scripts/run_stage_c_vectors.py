#!/usr/bin/env python3
"""Run Stage C plan emission vectors defined in CDX."""

from __future__ import annotations

import difflib
from pathlib import Path
from xml.etree import ElementTree as ET

from emit_adaptive_plan import EmitError, emit_plan, load_compiled_request, load_stage_a_result, load_stage_b_result


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EmitError(f"Missing required attribute '{name}' at {path}")
    return value


def _canonical_text(value: str) -> str:
    return value.rstrip() + "\n"


def run_vector(path: Path, repo_root: Path) -> tuple[bool, str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return False, f"Malformed StageCVector XML: {exc}"

    if root.tag != "StageCVector":
        return False, f"Root tag must be StageCVector in {path}"

    vector_id = _require_attr(root, "id", "StageCVector")
    compiled_path = repo_root / _require_attr(root, "compiledRequestFile", "StageCVector")
    stage_a_path = repo_root / _require_attr(root, "stageAResultFile", "StageCVector")
    stage_b_path = repo_root / _require_attr(root, "stageBResultFile", "StageCVector")
    expected_path = repo_root / _require_attr(root, "expectPlanFile", "StageCVector")

    try:
        rendered = emit_plan(
            load_compiled_request(compiled_path),
            load_stage_a_result(stage_a_path),
            load_stage_b_result(stage_b_path),
        )
    except EmitError as exc:
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
    repo_root = Path(__file__).resolve().parents[5]
    vector_dir = repo_root / "notes/workshop/design/compiler-mapping/stage-c-vectors"
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
