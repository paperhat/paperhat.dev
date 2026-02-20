#!/usr/bin/env python3
"""Emit deterministic Stage C package and decision-report outputs."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

from validate_output_schema import OutputSchemaValidationError, validate_rendered_cdx_against_schema

EVALUATION_ERROR = "EVALUATION_ERROR"
WORKSHOP_VERSION = "1.0.0"
CONTENT_HASH_ALGORITHM = "SHA256"
PROJECTION_DEFINITION_SEED = "projection-definition:adaptive-plan-projection:1.0.0"


class EmitError(Exception):
    """Stage C plan emission error."""


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


@dataclass(frozen=True)
class StageCOutputs:
    package: str | None
    decision_report: str


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EmitError(f"Missing required attribute '{name}' at {path}")
    return value


def _set_attr_if_present(element: ET.Element, name: str, value: str | None) -> None:
    if value is not None:
        element.set(name, value)


def _sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _render_xml(root: ET.Element) -> str:
    ET.indent(root, space="\t")
    return ET.tostring(root, encoding="unicode") + "\n"


def _intent_suffix(intent_id: str) -> str:
    parts = [part for part in intent_id.split(":") if part]
    if not parts:
        raise EmitError(f"Unable to derive intent suffix from '{intent_id}'")
    return parts[-1]


def _projection_identifier(compiled_request: CompiledRequest) -> str:
    return (
        "urn:projection:adaptive-plan:"
        f"{compiled_request.target_foundry}:{_intent_suffix(compiled_request.intent_id)}"
    )


def _parameter_seed(compiled_request: CompiledRequest) -> str:
    return (
        f"intentId={compiled_request.intent_id};"
        f"targetFoundry={compiled_request.target_foundry};"
        f"policySetRef={compiled_request.policy_set_ref};"
        f"compositionIri={compiled_request.composition_iri}"
    )


def _payload_canonical_bytes(
    projection_identifier: str,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
) -> str:
    if stage_b_result.selected_candidate is None or stage_b_result.selected_score is None:
        raise EmitError("Stage B success output is missing selectedCandidate/selectedScore")

    fields = [
        f"projection={projection_identifier}",
        f"selectedCandidate={stage_b_result.selected_candidate}",
        f"selectedScore={stage_b_result.selected_score}",
    ]

    relaxations = [entry.relaxation_action for entry in stage_b_result.applied_relaxations]
    if relaxations:
        fields.append(f"relaxation={'+'.join(relaxations)}")
    elif stage_a_result.selected_actions or stage_a_result.delta_remove or stage_a_result.delta_add:
        fields.append(f"actionCount={len(stage_a_result.selected_actions)}")
        fields.append(f"deltaRemoveCount={len(stage_a_result.delta_remove)}")
        fields.append(f"deltaAddCount={len(stage_a_result.delta_add)}")

    return ";".join(fields)


def _emit_error_decision_report(failed_stage: str) -> str:
    root = ET.Element("AdaptiveDecisionReport")
    root.set("status", "error")
    root.set("error", EVALUATION_ERROR)
    root.set("failedStage", failed_stage)
    return _render_xml(root)


def _emit_success_package(
    compiled_request: CompiledRequest,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
) -> tuple[str, str]:
    projection_identifier = _projection_identifier(compiled_request)
    projection_definition_hash = _sha256_hex(PROJECTION_DEFINITION_SEED)
    parameter_hash = _sha256_hex(_parameter_seed(compiled_request))
    payload_bytes = _payload_canonical_bytes(
        projection_identifier,
        stage_a_result,
        stage_b_result,
    )
    payload_content_hash = _sha256_hex(payload_bytes)

    package_seed = "|".join(
        (
            WORKSHOP_VERSION,
            projection_definition_hash,
            projection_identifier,
            parameter_hash,
            payload_content_hash,
        )
    )
    package_content_hash = _sha256_hex(package_seed)
    closure_hash = _sha256_hex(f"closure|{package_seed}")

    root = ET.Element("AdaptivePlanPackage")
    root.set("workshopVersion", WORKSHOP_VERSION)
    root.set("closureHash", closure_hash)
    root.set("adaptivePlanProjectionDefinitionClosureHash", projection_definition_hash)
    root.set("contentHashAlgorithm", CONTENT_HASH_ALGORITHM)
    root.set("adaptivePlanPackageContentHash", package_content_hash)

    payload_records = ET.SubElement(root, "PayloadRecords")

    record_root = ET.SubElement(payload_records, "AdaptivePlanPayloadRecord")
    record_root.set("projectionIdentifier", projection_identifier)
    record_root.set("projectionDefinitionClosureHash", projection_definition_hash)
    record_root.set("parameterHash", parameter_hash)
    record_root.set("payloadContentHash", payload_content_hash)
    record_root.set("payloadCanonicalBytes", payload_bytes)

    return _render_xml(root), package_content_hash


def _emit_success_decision_report(
    compiled_request: CompiledRequest,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
    package_content_hash: str,
) -> str:
    root = ET.Element("AdaptiveDecisionReport")
    root.set("status", "ok")
    root.set("intentId", compiled_request.intent_id)
    root.set("targetFoundry", compiled_request.target_foundry)
    root.set("policySetRef", compiled_request.policy_set_ref)
    root.set("adaptivePlanPackageContentHash", package_content_hash)

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

    if stage_b_result.selected_candidate is None or stage_b_result.selected_score is None:
        raise EmitError("Stage B success output is missing selectedCandidate/selectedScore")

    stage_b_outcome = ET.SubElement(root, "StageBOutcome")
    stage_b_outcome.set("selectedCandidate", stage_b_result.selected_candidate)
    stage_b_outcome.set("selectedScore", stage_b_result.selected_score)
    for relax in stage_b_result.applied_relaxations:
        relax_node = ET.SubElement(stage_b_outcome, "AppliedRelaxation")
        relax_node.set("relaxOrder", str(relax.relax_order))
        _set_attr_if_present(relax_node, "relaxWeightClass", relax.relax_weight_class)
        relax_node.set("relaxationAction", relax.relaxation_action)

    return _render_xml(root)


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


def emit_stage_c_outputs(
    compiled_request: CompiledRequest,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
) -> StageCOutputs:
    if stage_a_result.status != "ok":
        return StageCOutputs(
            package=None,
            decision_report=_emit_error_decision_report("stageA"),
        )

    if stage_b_result.status != "ok":
        return StageCOutputs(
            package=None,
            decision_report=_emit_error_decision_report("stageB"),
        )

    package, package_hash = _emit_success_package(
        compiled_request,
        stage_a_result,
        stage_b_result,
    )
    decision_report = _emit_success_decision_report(
        compiled_request,
        stage_a_result,
        stage_b_result,
        package_hash,
    )
    return StageCOutputs(package=package, decision_report=decision_report)


def emit_plan(
    compiled_request: CompiledRequest,
    stage_a_result: StageAResult,
    stage_b_result: StageBResult,
) -> str:
    """Legacy compatibility shim: returns the decision report artifact."""
    return emit_stage_c_outputs(compiled_request, stage_a_result, stage_b_result).decision_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compiled_request", type=Path, help="CompiledAdaptiveRequest (.cdx)")
    parser.add_argument("stage_a_result", type=Path, help="StageAResult (.cdx)")
    parser.add_argument("stage_b_result", type=Path, help="StageBResult (.cdx)")
    parser.add_argument("--package-output", type=Path, help="AdaptivePlanPackage output path")
    parser.add_argument(
        "--decision-report-output",
        type=Path,
        help="AdaptiveDecisionReport output path (defaults to stdout)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="legacy_decision_report_output",
        type=Path,
        help="Deprecated alias for --decision-report-output",
    )
    args = parser.parse_args()

    decision_report_output = args.decision_report_output or args.legacy_decision_report_output

    compiled = load_compiled_request(args.compiled_request)
    stage_a = load_stage_a_result(args.stage_a_result)
    stage_b = load_stage_b_result(args.stage_b_result)
    outputs = emit_stage_c_outputs(compiled, stage_a, stage_b)

    repo_root = _discover_repo_root(Path(__file__).resolve())
    package_schema_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex/adaptive-plan-package.schema.cdx",
    )
    decision_report_schema_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/codex/adaptive-decision-report.schema.cdx",
    )

    if outputs.package is not None:
        validate_rendered_cdx_against_schema(outputs.package, package_schema_path)
    validate_rendered_cdx_against_schema(outputs.decision_report, decision_report_schema_path)

    if args.package_output is not None:
        if outputs.package is None:
            args.package_output.unlink(missing_ok=True)
        else:
            args.package_output.write_text(outputs.package, encoding="utf-8")

    if decision_report_output is not None:
        decision_report_output.write_text(outputs.decision_report, encoding="utf-8")
    else:
        print(outputs.decision_report, end="")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EmitError as exc:
        raise SystemExit(f"[emit-error] {exc}")
    except OutputSchemaValidationError as exc:
        raise SystemExit(f"[stage-c-schema-error] {exc}")
