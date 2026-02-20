#!/usr/bin/env python3
"""Validate emitted output fixtures against Codex output schemas."""

from __future__ import annotations

from pathlib import Path

from validate_output_schema import (
    OutputSchemaValidationError,
    load_cdx_root,
    validate_rendered_cdx_against_schema,
)


def _validate_files(files: list[Path], schema: Path, label: str) -> int:
    failures = 0
    for path in files:
        try:
            rendered = path.read_text(encoding="utf-8")
            validate_rendered_cdx_against_schema(rendered, schema)
            print(f"[PASS] {label} schema: {path.name}")
        except (OSError, OutputSchemaValidationError) as exc:
            failures += 1
            print(f"[FAIL] {label} schema: {path.name}: {exc}")
    return failures


def _validate_linkage_pairs(pairs: list[tuple[Path, Path]]) -> int:
    failures = 0
    for package_file, report_file in pairs:
        try:
            package_root = load_cdx_root(package_file)
            report_root = load_cdx_root(report_file)

            if package_root.tag != "AdaptivePlanPackage":
                raise OutputSchemaValidationError(
                    f"Expected AdaptivePlanPackage root in {package_file.name}, found {package_root.tag}"
                )
            if report_root.tag != "AdaptiveDecisionReport":
                raise OutputSchemaValidationError(
                    f"Expected AdaptiveDecisionReport root in {report_file.name}, found {report_root.tag}"
                )

            package_hash = package_root.get("adaptivePlanPackageContentHash")
            report_hash = report_root.get("adaptivePlanPackageContentHash")
            if not package_hash:
                raise OutputSchemaValidationError(
                    f"{package_file.name} is missing adaptivePlanPackageContentHash"
                )
            if not report_hash:
                raise OutputSchemaValidationError(
                    f"{report_file.name} is missing adaptivePlanPackageContentHash"
                )
            if package_hash != report_hash:
                raise OutputSchemaValidationError(
                    f"package/report linkage mismatch: package={package_hash} report={report_hash}"
                )

            print(
                "[PASS] package/report linkage: "
                f"{package_file.name} <-> {report_file.name}"
            )
        except (OSError, OutputSchemaValidationError) as exc:
            failures += 1
            print(
                "[FAIL] package/report linkage: "
                f"{package_file.name} <-> {report_file.name}: {exc}"
            )
    return failures


def _validate_error_reports_without_linkage(files: list[Path]) -> int:
    failures = 0
    for path in files:
        try:
            root = load_cdx_root(path)
            if root.tag != "AdaptiveDecisionReport":
                raise OutputSchemaValidationError(
                    f"Expected AdaptiveDecisionReport root in {path.name}, found {root.tag}"
                )
            status = root.get("status")
            if status != "error":
                raise OutputSchemaValidationError(
                    f"{path.name} must use status='error', found {status!r}"
                )
            if root.get("adaptivePlanPackageContentHash") is not None:
                raise OutputSchemaValidationError(
                    f"{path.name} must not include adaptivePlanPackageContentHash for error reports"
                )
            print(f"[PASS] error report no-linkage: {path.name}")
        except (OSError, OutputSchemaValidationError) as exc:
            failures += 1
            print(f"[FAIL] error report no-linkage: {path.name}: {exc}")
    return failures


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


def main() -> int:
    repo_root = _discover_repo_root(Path(__file__).resolve())
    fixtures = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/compiler-mapping/fixtures",
    )
    schemas = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex",
    )

    stage_a_schema = schemas / "stage-a-result.schema.cdx"
    stage_b_schema = schemas / "stage-b-result.schema.cdx"
    package_schema = schemas / "adaptive-plan-package.schema.cdx"
    decision_report_schema = schemas / "adaptive-decision-report.schema.cdx"

    stage_a_files = [
        fixtures / "stage-a-result-empty-ok.cdx",
        fixtures / "stage-a-result-stage-a-e2e.expect.cdx",
        fixtures / "stage-a-result-stage-a-error.expect.cdx",
    ]

    stage_b_files = [
        fixtures / "stage-b-result-error.cdx",
        fixtures / "stage-b-result-widen-threshold-ok.cdx",
        fixtures / "stage-b-result-stage-a-e2e.expect.cdx",
        fixtures / "stage-b-result-stage-a-error.expect.cdx",
    ]

    package_files = [
        fixtures / "adaptive-plan-package-widen-threshold.expect.cdx",
        fixtures / "adaptive-plan-package-stage-a-e2e.expect.cdx",
    ]

    decision_report_files = [
        fixtures / "adaptive-decision-report-widen-threshold.expect.cdx",
        fixtures / "adaptive-decision-report-stage-a-e2e.expect.cdx",
        fixtures / "adaptive-decision-report-error-stage-a.expect.cdx",
        fixtures / "adaptive-decision-report-error-stage-b.expect.cdx",
    ]

    linkage_pairs = [
        (
            fixtures / "adaptive-plan-package-widen-threshold.expect.cdx",
            fixtures / "adaptive-decision-report-widen-threshold.expect.cdx",
        ),
        (
            fixtures / "adaptive-plan-package-stage-a-e2e.expect.cdx",
            fixtures / "adaptive-decision-report-stage-a-e2e.expect.cdx",
        ),
    ]

    error_reports = [
        fixtures / "adaptive-decision-report-error-stage-a.expect.cdx",
        fixtures / "adaptive-decision-report-error-stage-b.expect.cdx",
    ]

    failures = 0
    failures += _validate_files(stage_a_files, stage_a_schema, "stage-a-result")
    failures += _validate_files(stage_b_files, stage_b_schema, "stage-b-result")
    failures += _validate_files(package_files, package_schema, "adaptive-plan-package")
    failures += _validate_files(
        decision_report_files,
        decision_report_schema,
        "adaptive-decision-report",
    )
    failures += _validate_linkage_pairs(linkage_pairs)
    failures += _validate_error_reports_without_linkage(error_reports)

    if failures:
        print(f"Output schema checks failed with {failures} failing file(s).")
        return 1

    print("All output schema checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
