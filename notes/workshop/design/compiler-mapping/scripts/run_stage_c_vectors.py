#!/usr/bin/env python3
"""Run Stage C package/report emission vectors defined in CDX."""

from __future__ import annotations

import difflib
from pathlib import Path
from xml.etree import ElementTree as ET

from emit_adaptive_plan import (
    EmitError,
    emit_stage_c_outputs,
    load_compiled_request,
    load_stage_a_result,
    load_stage_b_result,
)
from validate_output_schema import (
    OutputSchemaValidationError,
    parse_rendered_cdx,
    validate_rendered_cdx_against_schema,
)


CANONICAL_ONTOLOGY_PREFIX = "spec/1.0.0/validation/design/ontology/"
CANONICAL_WORKSHOP_PREFIX = "spec/1.0.0/validation/design/workshop/"


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EmitError(f"Missing required attribute '{name}' at {path}")
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
    raise EmitError(
        f"Attribute '{name}' must be boolean (true|false) but was '{raw_value}'"
    )


def _canonical_text(value: str) -> str:
    return value.rstrip() + "\n"


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


def _extract_linkage_hashes(package_rendered: str, report_rendered: str) -> tuple[str, str]:
    package_root = parse_rendered_cdx(package_rendered)
    report_root = parse_rendered_cdx(report_rendered)

    if package_root.tag != "AdaptivePlanPackage":
        raise EmitError(f"Expected AdaptivePlanPackage root, found '{package_root.tag}'")
    if report_root.tag != "AdaptiveDecisionReport":
        raise EmitError(f"Expected AdaptiveDecisionReport root, found '{report_root.tag}'")

    package_hash = package_root.get("adaptivePlanPackageContentHash")
    report_hash = report_root.get("adaptivePlanPackageContentHash")
    if not package_hash:
        raise EmitError("AdaptivePlanPackage is missing adaptivePlanPackageContentHash")
    if not report_hash:
        raise EmitError("AdaptiveDecisionReport is missing adaptivePlanPackageContentHash")

    return package_hash, report_hash


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

    expect_no_package = _parse_bool_attr(root, "expectNoPackage", default=False)
    expect_package_report_linkage = _parse_bool_attr(
        root,
        "expectPackageReportLinkage",
        default=False,
    )

    expected_package_file_attr = root.get("expectPackageFile")
    expected_report_path = _resolve_repo_relative_path(
        repo_root,
        _require_attr(root, "expectDecisionReportFile", "StageCVector"),
    )

    if expect_no_package and expected_package_file_attr:
        return False, "expectNoPackage=true is incompatible with expectPackageFile"

    if expect_package_report_linkage and expect_no_package:
        return False, "expectPackageReportLinkage=true requires an expected package"

    if not expect_no_package and not expected_package_file_attr:
        return False, "Missing required attribute 'expectPackageFile' when expectNoPackage is false"

    expected_package_path = (
        _resolve_repo_relative_path(repo_root, expected_package_file_attr)
        if expected_package_file_attr
        else None
    )

    package_schema_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex/adaptive-plan-package.schema.cdx",
    )
    decision_report_schema_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex/adaptive-decision-report.schema.cdx",
    )

    try:
        outputs = emit_stage_c_outputs(
            load_compiled_request(compiled_path),
            load_stage_a_result(stage_a_path),
            load_stage_b_result(stage_b_path),
        )
        validate_rendered_cdx_against_schema(outputs.decision_report, decision_report_schema_path)
        if outputs.package is not None:
            validate_rendered_cdx_against_schema(outputs.package, package_schema_path)
    except (EmitError, OutputSchemaValidationError) as exc:
        return False, str(exc)

    expected_report = expected_report_path.read_text(encoding="utf-8")
    if _canonical_text(outputs.decision_report) != _canonical_text(expected_report):
        diff = "\n".join(
            difflib.unified_diff(
                _canonical_text(expected_report).splitlines(),
                _canonical_text(outputs.decision_report).splitlines(),
                fromfile=f"expected:{expected_report_path.name}",
                tofile=f"actual:{path.name}:decision-report",
                lineterm="",
            )
        )
        return False, f"Rendered decision report mismatch for vector '{vector_id}'.\n{diff}"

    if expect_no_package:
        if outputs.package is not None:
            return False, f"Vector '{vector_id}' expected no package output, but package was emitted"
        return True, vector_id

    if outputs.package is None:
        return False, f"Vector '{vector_id}' expected package output, but none was emitted"

    if expected_package_path is None:
        return False, "Internal vector configuration error: expected_package_path was not resolved"

    expected_package = expected_package_path.read_text(encoding="utf-8")
    if _canonical_text(outputs.package) != _canonical_text(expected_package):
        diff = "\n".join(
            difflib.unified_diff(
                _canonical_text(expected_package).splitlines(),
                _canonical_text(outputs.package).splitlines(),
                fromfile=f"expected:{expected_package_path.name}",
                tofile=f"actual:{path.name}:package",
                lineterm="",
            )
        )
        return False, f"Rendered package mismatch for vector '{vector_id}'.\n{diff}"

    if expect_package_report_linkage:
        try:
            package_hash, report_hash = _extract_linkage_hashes(
                outputs.package,
                outputs.decision_report,
            )
        except (EmitError, OutputSchemaValidationError) as exc:
            return False, str(exc)
        if package_hash != report_hash:
            return (
                False,
                f"Package/report linkage hash mismatch for vector '{vector_id}': "
                f"package={package_hash} report={report_hash}",
            )

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
