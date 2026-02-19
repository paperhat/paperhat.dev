#!/usr/bin/env python3
"""Evaluate Stage A policy semantics and emit StageAResult."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from validate_output_schema import OutputSchemaValidationError, validate_rendered_cdx_against_schema

EVALUATION_ERROR = "EVALUATION_ERROR"


class StageAEmitError(Exception):
    """Stage A result emission error."""


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise StageAEmitError(f"Missing required attribute '{name}' at {path}")
    return value


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise StageAEmitError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _parse_context(stage_a_node: ET.Element) -> dict[str, dict[str, Any]]:
    context: dict[str, dict[str, Any]] = {}
    for entry in stage_a_node.findall("ContextEntry"):
        key = _require_attr(entry, "key", "CompiledAdaptiveRequest/StageA/ContextEntry")
        kind = _require_attr(
            entry,
            "type",
            f"CompiledAdaptiveRequest/StageA/ContextEntry[@key='{key}']",
        )
        raw_value = _require_attr(
            entry,
            "value",
            f"CompiledAdaptiveRequest/StageA/ContextEntry[@key='{key}']",
        )
        if key in context:
            raise StageAEmitError(f"Duplicate StageA ContextEntry key '{key}'")

        if kind == "integer":
            value: Any = int(raw_value)
        elif kind == "decimal":
            value = raw_value
        elif kind == "string":
            value = raw_value
        elif kind == "boolean":
            if raw_value not in {"true", "false"}:
                raise StageAEmitError(f"Boolean StageA ContextEntry value must be true/false for key '{key}'")
            value = raw_value == "true"
        else:
            raise StageAEmitError(f"Unsupported StageA ContextEntry type '{kind}' for key '{key}'")

        context[key] = {"type": kind, "value": value}
    return context


def load_stage_a_request(compiled_request_path: Path) -> dict[str, Any]:
    try:
        root = ET.parse(compiled_request_path).getroot()
    except ET.ParseError as exc:
        raise StageAEmitError(f"Malformed compiled request XML: {compiled_request_path}") from exc

    if root.tag != "CompiledAdaptiveRequest":
        raise StageAEmitError(f"Root tag must be CompiledAdaptiveRequest in {compiled_request_path}")

    intent_id = _require_attr(root, "intentId", "CompiledAdaptiveRequest")
    stage_a_node = root.find("StageA")
    if stage_a_node is None:
        raise StageAEmitError(f"Missing StageA node in {compiled_request_path}")

    composition_iri = _require_attr(stage_a_node, "compositionIri", "CompiledAdaptiveRequest/StageA")
    view_iri = stage_a_node.get("viewIri")
    if view_iri == "":
        view_iri = None

    context = _parse_context(stage_a_node)

    return {
        "intent_id": intent_id,
        "composition_iri": composition_iri,
        "view_iri": view_iri,
        "context": context,
    }


def evaluate_stage_a(compiled_request_path: Path, graph_path: Path, repo_root: Path) -> dict[str, Any]:
    request = load_stage_a_request(compiled_request_path)

    runner = _load_module(
        repo_root / "notes/design/ontology/scripts/policy_vector_runner.py",
        "policy_vector_runner_stage_a_emit",
    )

    try:
        composition = URIRef(request["composition_iri"])
        view = URIRef(request["view_iri"]) if request.get("view_iri") else None
        context = runner.load_context(request.get("context", {}))

        graph = Graph()
        graph.parse(graph_path, format="turtle")

        shapes = Graph()
        ontology = Graph()
        shapes.parse(repo_root / "notes/design/ontology/wd-all.shacl.ttl", format="turtle")
        ontology.parse(repo_root / "notes/design/ontology/wd-core.ttl", format="turtle")

        runner.validate_graph(graph, shapes, ontology, stage="pre-evaluation")

        if (composition, RDF.type, runner.WD_COMPOSITION) not in graph:
            raise runner.EvaluationError(f"Composition not found or mistyped: {composition}")
        if view is not None and (view, RDF.type, runner.WD_VIEW) not in graph:
            raise runner.EvaluationError(f"View not found or mistyped: {view}")

        matched_policies = runner.collect_candidates(graph, composition, view, context)
        ordered_actions = runner.collect_ordered_actions(graph, matched_policies)
        selected_actions = runner.resolve_conflicts(matched_policies, ordered_actions)
        removed, added = runner.apply_actions(graph, selected_actions)

        runner.validate_graph(graph, shapes, ontology, stage="post-evaluation")

        return {
            "intent_id": request["intent_id"],
            "status": "ok",
            "selected_actions": [str(action.action) for action in selected_actions],
            "delta": {
                "remove": removed,
                "add": added,
            },
        }
    except runner.EvaluationError:
        return {
            "intent_id": request["intent_id"],
            "status": "error",
            "error": EVALUATION_ERROR,
        }


def render_stage_a_result(result: dict[str, Any]) -> str:
    root = ET.Element("StageAResult")
    root.set("id", f"stage-a-result:{result.get('intent_id', 'unknown')}")
    root.set("status", result.get("status", "error"))

    if result.get("status") != "ok":
        root.set("error", EVALUATION_ERROR)
        ET.indent(root, space="\t")
        return ET.tostring(root, encoding="unicode") + "\n"

    selected = ET.SubElement(root, "SelectedActions")
    for iri in result.get("selected_actions", []):
        action = ET.SubElement(selected, "Action")
        action.set("iri", iri)

    delta = ET.SubElement(root, "Delta")
    for triple in result.get("delta", {}).get("remove", []):
        node = ET.SubElement(delta, "Remove")
        node.set("triple", triple)
    for triple in result.get("delta", {}).get("add", []):
        node = ET.SubElement(delta, "Add")
        node.set("triple", triple)

    ET.indent(root, space="\t")
    return ET.tostring(root, encoding="unicode") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("compiled_request", type=Path, help="CompiledAdaptiveRequest (.cdx)")
    parser.add_argument("policy_graph", type=Path, help="Policy graph (.ttl)")
    parser.add_argument("-o", "--output", type=Path, help="Output StageAResult path (.cdx)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[5]
    result = evaluate_stage_a(args.compiled_request, args.policy_graph, repo_root)
    rendered = render_stage_a_result(result)
    schema_path = repo_root / "notes/workshop/design/codex/stage-a-result.schema.cdx"
    validate_rendered_cdx_against_schema(rendered, schema_path)

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StageAEmitError as exc:
        raise SystemExit(f"[stage-a-emit-error] {exc}")
    except OutputSchemaValidationError as exc:
        raise SystemExit(f"[stage-a-schema-error] {exc}")
