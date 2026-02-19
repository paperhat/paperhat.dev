#!/usr/bin/env python3
"""Run compile -> Stage A -> Stage B -> Stage C end-to-end vectors."""

from __future__ import annotations

import difflib
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

from compile_adaptive_intent import compile_fixture, load_fixture, render_compiled_cdx
from emit_adaptive_plan import emit_plan, load_compiled_request, load_stage_a_result, load_stage_b_result
from evaluate_stage_a import evaluate_stage_a, render_stage_a_result
from evaluate_stage_b import evaluate_stage_b, render_stage_b_result


class PipelineE2EError(Exception):
    """Pipeline e2e vector error."""


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise PipelineE2EError(f"Missing required attribute '{name}' at {path}")
    return value


def _canonical(text: str) -> str:
    return text.rstrip() + "\n"


def _diff(expected: str, actual: str, expected_name: str, actual_name: str) -> str:
    return "\n".join(
        difflib.unified_diff(
            _canonical(expected).splitlines(),
            _canonical(actual).splitlines(),
            fromfile=expected_name,
            tofile=actual_name,
            lineterm="",
        )
    )


def run_vector(vector_path: Path, repo_root: Path) -> tuple[bool, str]:
    try:
        root = ET.parse(vector_path).getroot()
    except ET.ParseError as exc:
        return False, f"Malformed AdaptivePipelineVector XML: {exc}"

    if root.tag != "AdaptivePipelineVector":
        return False, f"Root tag must be AdaptivePipelineVector in {vector_path}"

    vector_id = _require_attr(root, "id", "AdaptivePipelineVector")
    input_fixture_file = repo_root / _require_attr(root, "inputFixtureFile", "AdaptivePipelineVector")
    policy_graph_file = repo_root / _require_attr(root, "policyGraphFile", "AdaptivePipelineVector")
    candidates_file = repo_root / _require_attr(root, "stageBCandidatesFile", "AdaptivePipelineVector")
    expect_stage_a_file = repo_root / _require_attr(root, "expectStageAFile", "AdaptivePipelineVector")
    expect_stage_b_file = repo_root / _require_attr(root, "expectStageBFile", "AdaptivePipelineVector")
    expect_plan_file = repo_root / _require_attr(root, "expectPlanFile", "AdaptivePipelineVector")

    compiled = compile_fixture(load_fixture(input_fixture_file))
    compiled_text = render_compiled_cdx(compiled)

    with TemporaryDirectory(prefix="adaptive-pipeline-e2e-") as tmp_dir:
        tmp_root = Path(tmp_dir)
        compiled_file = tmp_root / "compiled.cdx"
        stage_a_file = tmp_root / "stage_a_result.cdx"
        stage_b_file = tmp_root / "stage_b_result.cdx"

        compiled_file.write_text(compiled_text, encoding="utf-8")

        stage_a_result = evaluate_stage_a(compiled_file, policy_graph_file, repo_root)
        stage_a_text = render_stage_a_result(stage_a_result)
        stage_a_file.write_text(stage_a_text, encoding="utf-8")

        stage_b_result = evaluate_stage_b(compiled_file, candidates_file)
        stage_b_text = render_stage_b_result(stage_b_result)
        stage_b_file.write_text(stage_b_text, encoding="utf-8")

        emitted_plan_text = emit_plan(
            load_compiled_request(compiled_file),
            load_stage_a_result(stage_a_file),
            load_stage_b_result(stage_b_file),
        )

    expected_stage_a = expect_stage_a_file.read_text(encoding="utf-8")
    if _canonical(stage_a_text) != _canonical(expected_stage_a):
        return (
            False,
            "StageAResult mismatch.\n"
            + _diff(expected_stage_a, stage_a_text, f"expected:{expect_stage_a_file.name}", f"actual:{vector_id}:stage-a"),
        )

    expected_stage_b = expect_stage_b_file.read_text(encoding="utf-8")
    if _canonical(stage_b_text) != _canonical(expected_stage_b):
        return (
            False,
            "StageBResult mismatch.\n"
            + _diff(expected_stage_b, stage_b_text, f"expected:{expect_stage_b_file.name}", f"actual:{vector_id}:stage-b"),
        )

    expected_plan = expect_plan_file.read_text(encoding="utf-8")
    if _canonical(emitted_plan_text) != _canonical(expected_plan):
        return (
            False,
            "AdaptivePlanResult mismatch.\n"
            + _diff(expected_plan, emitted_plan_text, f"expected:{expect_plan_file.name}", f"actual:{vector_id}:plan"),
        )

    return True, vector_id


def main() -> int:
    repo_root = Path(__file__).resolve().parents[5]
    vector_dir = repo_root / "notes/workshop/design/compiler-mapping/pipeline-vectors"
    vectors = sorted(vector_dir.glob("*.cdx"))
    if not vectors:
        print("No adaptive pipeline e2e vectors found (.cdx).")
        return 1

    failures = 0
    for vector in vectors:
        ok, detail = run_vector(vector, repo_root)
        if ok:
            print(f"[PASS] adaptive-pipeline vector: {vector.name}")
        else:
            failures += 1
            print(f"[FAIL] adaptive-pipeline vector: {vector.name}: {detail}")

    if failures:
        print(f"Adaptive pipeline e2e failed with {failures} failing vector(s).")
        return 1

    print("All adaptive pipeline e2e vectors passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
