#!/usr/bin/env python3
"""Run compile -> Stage A -> Stage B -> Stage C end-to-end vectors."""

from __future__ import annotations

import difflib
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

from compile_adaptive_intent import compile_fixture, load_fixture, render_compiled_cdx
from emit_adaptive_plan import (
    emit_stage_c_outputs,
    load_compiled_request,
    load_stage_a_result,
    load_stage_b_result,
)
from evaluate_stage_a import evaluate_stage_a, render_stage_a_result
from evaluate_stage_b import evaluate_stage_b, render_stage_b_result
from validate_output_schema import (
    OutputSchemaValidationError,
    parse_rendered_cdx,
    validate_rendered_cdx_against_schema,
)


class PipelineE2EError(Exception):
    """Pipeline e2e vector error."""


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


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise PipelineE2EError(f"Missing required attribute '{name}' at {path}")
    return value


def _parse_bool_attr(element: ET.Element, name: str, default: bool) -> bool:
    raw_value = element.get(name)
    if raw_value is None:
        return default
    normalized = raw_value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise PipelineE2EError(
        f"Attribute '{name}' must be boolean (true|false) but was '{raw_value}'"
    )


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


def _extract_linkage_hashes(package_rendered: str, report_rendered: str) -> tuple[str, str]:
    package_root = parse_rendered_cdx(package_rendered)
    report_root = parse_rendered_cdx(report_rendered)

    if package_root.tag != "AdaptivePlanPackage":
        raise PipelineE2EError(f"Expected AdaptivePlanPackage root, found '{package_root.tag}'")
    if report_root.tag != "AdaptiveDecisionReport":
        raise PipelineE2EError(f"Expected AdaptiveDecisionReport root, found '{report_root.tag}'")

    package_hash = package_root.get("adaptivePlanPackageContentHash")
    report_hash = report_root.get("adaptivePlanPackageContentHash")

    if not package_hash:
        raise PipelineE2EError("AdaptivePlanPackage is missing adaptivePlanPackageContentHash")
    if not report_hash:
        raise PipelineE2EError("AdaptiveDecisionReport is missing adaptivePlanPackageContentHash")

    return package_hash, report_hash


def run_vector(vector_path: Path, repo_root: Path) -> tuple[bool, str]:
    try:
        try:
            root = ET.parse(vector_path).getroot()
        except ET.ParseError as exc:
            return False, f"Malformed AdaptivePipelineVector XML: {exc}"

        if root.tag != "AdaptivePipelineVector":
            return False, f"Root tag must be AdaptivePipelineVector in {vector_path}"

        vector_id = _require_attr(root, "id", "AdaptivePipelineVector")
        input_fixture_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "inputFixtureFile", "AdaptivePipelineVector"),
        )
        policy_graph_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "policyGraphFile", "AdaptivePipelineVector"),
        )
        candidates_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "stageBCandidatesFile", "AdaptivePipelineVector"),
        )
        expect_stage_a_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "expectStageAFile", "AdaptivePipelineVector"),
        )
        expect_stage_b_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "expectStageBFile", "AdaptivePipelineVector"),
        )
        expect_decision_report_file = _resolve_repo_relative_path(
            repo_root,
            _require_attr(root, "expectDecisionReportFile", "AdaptivePipelineVector"),
        )

        expect_no_package = _parse_bool_attr(root, "expectNoPackage", default=False)
        expect_package_report_linkage = _parse_bool_attr(
            root,
            "expectPackageReportLinkage",
            default=False,
        )
        expect_package_file_attr = root.get("expectPackageFile")

        if expect_no_package and expect_package_file_attr:
            return False, "expectNoPackage=true is incompatible with expectPackageFile"

        if expect_package_report_linkage and expect_no_package:
            return False, "expectPackageReportLinkage=true requires an expected package"

        if not expect_no_package and not expect_package_file_attr:
            return False, "Missing required attribute 'expectPackageFile' when expectNoPackage is false"

        expect_package_file = (
            _resolve_repo_relative_path(repo_root, expect_package_file_attr)
            if expect_package_file_attr
            else None
        )

        compiled = compile_fixture(load_fixture(input_fixture_file))
        compiled_text = render_compiled_cdx(compiled)
        stage_a_schema = _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/workshop/codex/stage-a-result.schema.cdx",
        )
        stage_b_schema = _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/workshop/codex/stage-b-result.schema.cdx",
        )
        package_schema = _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/workshop/codex/adaptive-plan-package.schema.cdx",
        )
        decision_report_schema = _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/workshop/codex/adaptive-decision-report.schema.cdx",
        )

        with TemporaryDirectory(prefix="adaptive-pipeline-e2e-") as tmp_dir:
            tmp_root = Path(tmp_dir)
            compiled_file = tmp_root / "compiled.cdx"
            stage_a_file = tmp_root / "stage_a_result.cdx"
            stage_b_file = tmp_root / "stage_b_result.cdx"

            compiled_file.write_text(compiled_text, encoding="utf-8")

            stage_a_result = evaluate_stage_a(compiled_file, policy_graph_file, repo_root)
            stage_a_text = render_stage_a_result(stage_a_result)
            validate_rendered_cdx_against_schema(stage_a_text, stage_a_schema)
            stage_a_file.write_text(stage_a_text, encoding="utf-8")

            stage_b_result = evaluate_stage_b(compiled_file, candidates_file)
            stage_b_text = render_stage_b_result(stage_b_result)
            validate_rendered_cdx_against_schema(stage_b_text, stage_b_schema)
            stage_b_file.write_text(stage_b_text, encoding="utf-8")

            stage_c_outputs = emit_stage_c_outputs(
                load_compiled_request(compiled_file),
                load_stage_a_result(stage_a_file),
                load_stage_b_result(stage_b_file),
            )
            validate_rendered_cdx_against_schema(
                stage_c_outputs.decision_report,
                decision_report_schema,
            )
            if stage_c_outputs.package is not None:
                validate_rendered_cdx_against_schema(stage_c_outputs.package, package_schema)

        expected_stage_a = expect_stage_a_file.read_text(encoding="utf-8")
        if _canonical(stage_a_text) != _canonical(expected_stage_a):
            return (
                False,
                "StageAResult mismatch.\n"
                + _diff(
                    expected_stage_a,
                    stage_a_text,
                    f"expected:{expect_stage_a_file.name}",
                    f"actual:{vector_id}:stage-a",
                ),
            )

        expected_stage_b = expect_stage_b_file.read_text(encoding="utf-8")
        if _canonical(stage_b_text) != _canonical(expected_stage_b):
            return (
                False,
                "StageBResult mismatch.\n"
                + _diff(
                    expected_stage_b,
                    stage_b_text,
                    f"expected:{expect_stage_b_file.name}",
                    f"actual:{vector_id}:stage-b",
                ),
            )

        expected_decision_report = expect_decision_report_file.read_text(encoding="utf-8")
        if _canonical(stage_c_outputs.decision_report) != _canonical(expected_decision_report):
            return (
                False,
                "AdaptiveDecisionReport mismatch.\n"
                + _diff(
                    expected_decision_report,
                    stage_c_outputs.decision_report,
                    f"expected:{expect_decision_report_file.name}",
                    f"actual:{vector_id}:decision-report",
                ),
            )

        if expect_no_package:
            if stage_c_outputs.package is not None:
                return False, "AdaptivePlanPackage mismatch. Expected no package, but package was emitted."
            return True, vector_id

        if stage_c_outputs.package is None:
            return False, "AdaptivePlanPackage mismatch. Expected package output, but no package was emitted."

        if expect_package_file is None:
            return False, "Internal vector configuration error: expected package file was not resolved"

        expected_package = expect_package_file.read_text(encoding="utf-8")
        if _canonical(stage_c_outputs.package) != _canonical(expected_package):
            return (
                False,
                "AdaptivePlanPackage mismatch.\n"
                + _diff(
                    expected_package,
                    stage_c_outputs.package,
                    f"expected:{expect_package_file.name}",
                    f"actual:{vector_id}:package",
                ),
            )

        if expect_package_report_linkage:
            package_hash, report_hash = _extract_linkage_hashes(
                stage_c_outputs.package,
                stage_c_outputs.decision_report,
            )
            if package_hash != report_hash:
                return (
                    False,
                    "Package/report linkage mismatch. "
                    f"package={package_hash} report={report_hash}",
                )

        return True, vector_id
    except (PipelineE2EError, OutputSchemaValidationError, ValueError, Exception) as exc:
        return False, str(exc)


def main() -> int:
    repo_root = _discover_repo_root(Path(__file__).resolve())
    vector_dir = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/compiler-mapping/pipeline-vectors",
    )
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
