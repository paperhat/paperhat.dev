#!/usr/bin/env python3
"""Emit deterministic Stage C adaptive plan output from compiled request and Stage A/B results."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

from validate_output_schema import OutputSchemaValidationError, validate_rendered_cdx_against_schema

EVALUATION_ERROR = "EVALUATION_ERROR"


class EmitError(Exception):
    """Stage C plan emission error."""


@dataclass(frozen=True)
class StageAResult:
    status: str
    selected_actions: tuple[str, ...]
    delta_remove: tuple[str, ...]
    delta_add: tuple[str, ...]
    error: str | None


@dataclass(frozen=True)
class StageBRelaxation:
    relax_order: int
    relax_weight_class: str | None
    relaxation_action: str


@dataclass(frozen=True)
class StageBResult:
    status: str
    selected_candidate: str | None
    selected_score: str | None
    applied_relaxations: tuple[StageBRelaxation, ...]
    error: str | None


@dataclass(frozen=True)
class CompiledRequest:
    intent_id: str
    target_foundry: str
    policy_set_ref: str
    composition_iri: str
    view_iri: str | None


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EmitError(f"Missing required attribute '{name}' at {path}")
    return value


def _set_attr_if_present(element: ET.Element, name: str, value: str | None) -> None:
    if value is not None:
        element.set(name, value)


def load_compiled_request(path: Path) -> CompiledRequest:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise EmitError(f"Malformed compiled request XML: {path}") from exc

    if root.tag != "CompiledAdaptiveRequest":
        raise EmitError(f"Root tag must be CompiledAdaptiveRequest in {path}")

    stage_a_node = root.find("StageA")
    if stage_a_node is None:
        raise EmitError(f"Missing StageA node in {path}")

    return CompiledRequest(
        intent_id=_require_attr(root, "intentId", "CompiledAdaptiveRequest"),
        target_foundry=_require_attr(root, "targetFoundry", "CompiledAdaptiveRequest"),
        policy_set_ref=_require_attr(root, "policySetRef", "CompiledAdaptiveRequest"),
        composition_iri=_require_attr(stage_a_node, "compositionIri", "CompiledAdaptiveRequest/StageA"),
        view_iri=stage_a_node.get("viewIri"),
    )


def load_stage_a_result(path: Path) -> StageAResult:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise EmitError(f"Malformed StageAResult XML: {path}") from exc

    if root.tag != "StageAResult":
        raise EmitError(f"Root tag must be StageAResult in {path}")

    status = _require_attr(root, "status", "StageAResult")
    if status not in {"ok", "error"}:
        raise EmitError(f"Unsupported StageAResult status '{status}' in {path}")

    if status == "error":
        return StageAResult(
            status=status,
            selected_actions=(),
            delta_remove=(),
            delta_add=(),
            error=root.get("error", EVALUATION_ERROR),
        )

    selected_actions = tuple(
        _require_attr(node, "iri", "StageAResult/SelectedActions/Action")
        for node in root.findall("SelectedActions/Action")
    )
    delta_remove = tuple(
        _require_attr(node, "triple", "StageAResult/Delta/Remove")
        for node in root.findall("Delta/Remove")
    )
    delta_add = tuple(
        _require_attr(node, "triple", "StageAResult/Delta/Add")
        for node in root.findall("Delta/Add")
    )
    return StageAResult(
        status=status,
        selected_actions=selected_actions,
        delta_remove=delta_remove,
        delta_add=delta_add,
        error=None,
    )


def load_stage_b_result(path: Path) -> StageBResult:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise EmitError(f"Malformed StageBResult XML: {path}") from exc

    if root.tag != "StageBResult":
        raise EmitError(f"Root tag must be StageBResult in {path}")

    status = _require_attr(root, "status", "StageBResult")
    if status not in {"ok", "error"}:
        raise EmitError(f"Unsupported StageBResult status '{status}' in {path}")

    if status == "error":
        return StageBResult(
            status=status,
            selected_candidate=None,
            selected_score=None,
            applied_relaxations=(),
            error=root.get("error", EVALUATION_ERROR),
        )

    selected_candidate = _require_attr(root, "selectedCandidate", "StageBResult")
    selected_score = _require_attr(root, "selectedScore", "StageBResult")
    relaxations: list[StageBRelaxation] = []
    for node in root.findall("AppliedRelaxation"):
        order_raw = _require_attr(node, "relaxOrder", "StageBResult/AppliedRelaxation")
        try:
            order = int(order_raw)
        except Exception as exc:  # noqa: BLE001
            raise EmitError(f"Invalid integer relaxOrder '{order_raw}' in {path}") from exc
        relaxations.append(
            StageBRelaxation(
                relax_order=order,
                relax_weight_class=node.get("relaxWeightClass"),
                relaxation_action=_require_attr(
                    node,
                    "relaxationAction",
                    f"StageBResult/AppliedRelaxation[@relaxOrder='{order}']",
                ),
            )
        )
    return StageBResult(
        status=status,
        selected_candidate=selected_candidate,
        selected_score=selected_score,
        applied_relaxations=tuple(relaxations),
        error=None,
    )


def emit_plan(
    compiled_request: CompiledRequest,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
) -> str:
    root = ET.Element("AdaptivePlanResult")

    if stage_a_result.status != "ok":
        root.set("status", "error")
        root.set("error", EVALUATION_ERROR)
        root.set("failedStage", "stageA")
        ET.indent(root, space="\t")
        return ET.tostring(root, encoding="unicode") + "\n"
    if stage_b_result.status != "ok":
        root.set("status", "error")
        root.set("error", EVALUATION_ERROR)
        root.set("failedStage", "stageB")
        ET.indent(root, space="\t")
        return ET.tostring(root, encoding="unicode") + "\n"

    root.set("status", "ok")
    root.set("intentId", compiled_request.intent_id)
    root.set("targetFoundry", compiled_request.target_foundry)
    root.set("policySetRef", compiled_request.policy_set_ref)

    scope = ET.SubElement(root, "PlanScope")
    scope.set("compositionIri", compiled_request.composition_iri)
    _set_attr_if_present(scope, "viewIri", compiled_request.view_iri)

    stage_a_outcome = ET.SubElement(root, "StageAOutcome")
    selected_actions_node = ET.SubElement(stage_a_outcome, "SelectedActions")
    for iri in stage_a_result.selected_actions:
        action_node = ET.SubElement(selected_actions_node, "Action")
        action_node.set("iri", iri)

    delta_node = ET.SubElement(stage_a_outcome, "Delta")
    for triple in stage_a_result.delta_remove:
        remove_node = ET.SubElement(delta_node, "Remove")
        remove_node.set("triple", triple)
    for triple in stage_a_result.delta_add:
        add_node = ET.SubElement(delta_node, "Add")
        add_node.set("triple", triple)

    stage_b_outcome = ET.SubElement(root, "StageBOutcome")
    stage_b_outcome.set("selectedCandidate", stage_b_result.selected_candidate or "")
    stage_b_outcome.set("selectedScore", stage_b_result.selected_score or "")
    for relax in stage_b_result.applied_relaxations:
        relax_node = ET.SubElement(stage_b_outcome, "AppliedRelaxation")
        relax_node.set("relaxOrder", str(relax.relax_order))
        _set_attr_if_present(relax_node, "relaxWeightClass", relax.relax_weight_class)
        relax_node.set("relaxationAction", relax.relaxation_action)

    ET.indent(root, space="\t")
    return ET.tostring(root, encoding="unicode") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compiled_request", type=Path, help="CompiledAdaptiveRequest (.cdx)")
    parser.add_argument("stage_a_result", type=Path, help="StageAResult (.cdx)")
    parser.add_argument("stage_b_result", type=Path, help="StageBResult (.cdx)")
    parser.add_argument("-o", "--output", type=Path, help="Output path (defaults to stdout)")
    args = parser.parse_args()

    compiled = load_compiled_request(args.compiled_request)
    stage_a = load_stage_a_result(args.stage_a_result)
    stage_b = load_stage_b_result(args.stage_b_result)
    rendered = emit_plan(compiled, stage_a, stage_b)
    repo_root = Path(__file__).resolve().parents[5]
    schema_path = repo_root / "notes/workshop/design/codex/adaptive-plan-result.schema.cdx"
    validate_rendered_cdx_against_schema(rendered, schema_path)

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EmitError as exc:
        raise SystemExit(f"[emit-error] {exc}")
    except OutputSchemaValidationError as exc:
        raise SystemExit(f"[plan-schema-error] {exc}")
