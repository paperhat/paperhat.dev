#!/usr/bin/env python3
"""Evaluate Stage B optimization semantics and emit StageBResult."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

from run_stage_b_vectors import (
    EVALUATION_ERROR,
    StageBEvaluationError,
    evaluate,
    load_stage_b_request,
    parse_candidate,
)


class StageBEmitError(Exception):
    """Stage B result emission error."""


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise StageBEmitError(f"Missing required attribute '{name}' at {path}")
    return value


def load_candidates(path: Path):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise StageBEmitError(f"Malformed StageBCandidates XML: {path}") from exc

    if root.tag != "StageBCandidates":
        raise StageBEmitError(f"Root tag must be StageBCandidates in {path}")

    candidates = []
    for node in root.findall("Candidate"):
        candidates.append(parse_candidate(node))

    if not candidates:
        raise StageBEvaluationError("Candidate set MUST NOT be empty")

    return _require_attr(root, "id", "StageBCandidates"), candidates


def evaluate_stage_b(compiled_request_path: Path, candidates_path: Path):
    try:
        candidates_id, candidates = load_candidates(candidates_path)
        request = load_stage_b_request(compiled_request_path)
        actual = evaluate(request, candidates)
    except StageBEvaluationError:
        return {"id": "stage-b-result:error", "status": "error", "error": EVALUATION_ERROR}
    except StageBEmitError:
        return {"id": "stage-b-result:error", "status": "error", "error": EVALUATION_ERROR}

    if actual.get("status") != "ok":
        return {"id": f"stage-b-result:{candidates_id}", "status": "error", "error": EVALUATION_ERROR}

    return {
        "id": f"stage-b-result:{candidates_id}",
        "status": "ok",
        "selected_candidate": actual.get("selected_candidate"),
        "selected_score": actual.get("selected_score"),
        "applied_relaxations": actual.get("applied_relaxations", []),
    }


def render_stage_b_result(result: dict) -> str:
    root = ET.Element("StageBResult")
    root.set("id", str(result.get("id", "stage-b-result:unknown")))
    root.set("status", str(result.get("status", "error")))

    if result.get("status") != "ok":
        root.set("error", EVALUATION_ERROR)
        ET.indent(root, space="\t")
        return ET.tostring(root, encoding="unicode") + "\n"

    root.set("selectedCandidate", str(result.get("selected_candidate", "")))
    root.set("selectedScore", str(result.get("selected_score", "")))
    for relax_order, relax_weight_class, relaxation_action in result.get("applied_relaxations", []):
        node = ET.SubElement(root, "AppliedRelaxation")
        node.set("relaxOrder", str(relax_order))
        if relax_weight_class is not None:
            node.set("relaxWeightClass", str(relax_weight_class))
        node.set("relaxationAction", str(relaxation_action))

    ET.indent(root, space="\t")
    return ET.tostring(root, encoding="unicode") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compiled_request", type=Path, help="CompiledAdaptiveRequest (.cdx)")
    parser.add_argument("candidates", type=Path, help="StageBCandidates (.cdx)")
    parser.add_argument("-o", "--output", type=Path, help="Output StageBResult path (.cdx)")
    args = parser.parse_args()

    result = evaluate_stage_b(args.compiled_request, args.candidates)
    rendered = render_stage_b_result(result)

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StageBEmitError as exc:
        raise SystemExit(f"[stage-b-emit-error] {exc}")
