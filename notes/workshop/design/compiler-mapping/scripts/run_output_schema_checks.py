#!/usr/bin/env python3
"""Validate emitted output fixtures against Codex output schemas."""

from __future__ import annotations

from pathlib import Path

from validate_output_schema import OutputSchemaValidationError, validate_rendered_cdx_against_schema


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


def main() -> int:
    repo_root = Path(__file__).resolve().parents[5]
    fixtures = repo_root / "notes/workshop/design/compiler-mapping/fixtures"
    schemas = repo_root / "notes/workshop/design/codex"

    stage_a_schema = schemas / "stage-a-result.schema.cdx"
    stage_b_schema = schemas / "stage-b-result.schema.cdx"
    plan_schema = schemas / "adaptive-plan-result.schema.cdx"

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

    plan_files = [
        fixtures / "adaptive-plan-error-stage-a.expect.cdx",
        fixtures / "adaptive-plan-error-stage-b.expect.cdx",
        fixtures / "adaptive-plan-stage-a-e2e.expect.cdx",
        fixtures / "adaptive-plan-widen-threshold.expect.cdx",
    ]

    failures = 0
    failures += _validate_files(stage_a_files, stage_a_schema, "stage-a-result")
    failures += _validate_files(stage_b_files, stage_b_schema, "stage-b-result")
    failures += _validate_files(plan_files, plan_schema, "adaptive-plan-result")

    if failures:
        print(f"Output schema checks failed with {failures} failing file(s).")
        return 1

    print("All output schema checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
