#!/usr/bin/env python3
"""Compile adaptive fixture to Stage A request and run policy evaluator assertions."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from rdflib import Graph

from compile_adaptive_intent import compile_fixture, load_fixture


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


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
        raise ValueError(f"Missing required attribute '{name}' at {path}")
    return value


def load_stage_a_expectation(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    if root.tag != "StageAE2EExpectation":
        raise ValueError(f"Root tag must be StageAE2EExpectation: {path}")

    expect_node = root.find("Expect")
    if expect_node is None:
        raise ValueError(f"Missing Expect node: {path}")

    status = _require_attr(expect_node, "status", "StageAE2EExpectation/Expect")
    payload: dict[str, Any] = {
        "id": _require_attr(root, "id", "StageAE2EExpectation"),
        "graph_file": _require_attr(root, "graphFile", "StageAE2EExpectation"),
        "expect": {"status": status},
    }

    if status == "error":
        payload["expect"]["error"] = expect_node.get("error", "EVALUATION_ERROR")
        return payload

    selected_actions = [
        _require_attr(node, "iri", "StageAE2EExpectation/Expect/SelectedActions/Action")
        for node in expect_node.findall("SelectedActions/Action")
    ]
    delta_node = expect_node.find("Delta")
    if delta_node is None:
        raise ValueError(f"Missing Delta node for status=ok: {path}")

    delta_remove = [
        _require_attr(node, "triple", "StageAE2EExpectation/Expect/Delta/Remove")
        for node in delta_node.findall("Remove")
    ]
    delta_add = [
        _require_attr(node, "triple", "StageAE2EExpectation/Expect/Delta/Add")
        for node in delta_node.findall("Add")
    ]

    payload["expect"]["selected_actions"] = selected_actions
    payload["expect"]["delta"] = {"remove": delta_remove, "add": delta_add}
    return payload


def _write_temp_vector_cdx(vector_payload: dict[str, Any]) -> Path:
    root = ET.Element("PolicyVector")
    root.set("id", vector_payload["id"])
    root.set("graphFile", vector_payload["graph_file"])
    root.set("compositionIri", vector_payload["composition_iri"])
    if vector_payload.get("view_iri"):
        root.set("viewIri", vector_payload["view_iri"])

    for key in sorted(vector_payload.get("context", {}).keys()):
        item = vector_payload["context"][key]
        entry = ET.SubElement(root, "ContextEntry")
        entry.set("key", key)
        entry.set("type", str(item["type"]))
        value = item["value"]
        if isinstance(value, bool):
            rendered_value = "true" if value else "false"
        else:
            rendered_value = str(value)
        entry.set("value", rendered_value)

    expect_data = vector_payload["expect"]
    expect = ET.SubElement(root, "Expect")
    expect.set("status", expect_data["status"])

    if expect_data["status"] == "error":
        expect.set("error", expect_data.get("error", "EVALUATION_ERROR"))
    else:
        selected = ET.SubElement(expect, "SelectedActions")
        for action in expect_data.get("selected_actions", []):
            node = ET.SubElement(selected, "Action")
            node.set("iri", action)

        delta = ET.SubElement(expect, "Delta")
        for triple in expect_data.get("delta", {}).get("remove", []):
            node = ET.SubElement(delta, "Remove")
            node.set("triple", triple)
        for triple in expect_data.get("delta", {}).get("add", []):
            node = ET.SubElement(delta, "Add")
            node.set("triple", triple)

    ET.indent(root, space="\t")
    temp_file = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".cdx", delete=False)
    with temp_file:
        temp_file.write(ET.tostring(root, encoding="unicode") + "\n")
    return Path(temp_file.name)


def main() -> int:
    repo_root = _discover_repo_root(Path(__file__).resolve())
    fixtures_dir = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/workshop/compiler-mapping/fixtures",
    )

    input_fixture = load_fixture(fixtures_dir / "adaptive-intent-stage-a-e2e.input.cdx")
    expectation = load_stage_a_expectation(fixtures_dir / "adaptive-intent-stage-a-e2e.expect.cdx")
    compiled = compile_fixture(input_fixture)

    vector_payload = {
        "id": expectation["id"],
        "graph_file": expectation["graph_file"],
        "composition_iri": compiled["stage_a"]["composition_iri"],
        "view_iri": compiled["stage_a"]["view_iri"],
        "context": compiled["stage_a"]["context"],
        "expect": expectation["expect"],
    }

    runner = load_module(
        _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/ontology/scripts/policy_vector_runner.py",
        ),
        "policy_vector_runner",
    )

    shapes = Graph()
    ontology = Graph()
    shapes.parse(
        _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/ontology/wd-all.shacl.ttl",
        ),
        format="turtle",
    )
    ontology.parse(
        _resolve_repo_relative_path(
            repo_root,
            "spec/1.0.0/validation/design/ontology/wd-core.ttl",
        ),
        format="turtle",
    )

    temp_vector_path = _write_temp_vector_cdx(vector_payload)
    try:
        ok, detail = runner.run_vector(temp_vector_path, repo_root, shapes, ontology)
    finally:
        temp_vector_path.unlink(missing_ok=True)

    if not ok:
        raise SystemExit(f"[FAIL] stage-a e2e: {detail}")

    print("[PASS] stage-a e2e")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
