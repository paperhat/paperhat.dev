#!/usr/bin/env python3
"""Run procedural conformance tests for PROC-enforced ontology clauses."""

from __future__ import annotations

import csv
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any

from pyshacl import validate
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF

WD = "https://paperhat.dev/ns/wd#"
WD_STROKE = URIRef(f"{WD}Stroke")
WD_STROKE_WIDTH = URIRef(f"{WD}strokeWidth")
WD_BASELINE_GRID = URIRef(f"{WD}BaselineGrid")
WD_BASELINE_STEP = URIRef(f"{WD}baselineStep")
WD_OWNED_BY = URIRef(f"{WD}ownedBy")

FORBIDDEN_IMPLICIT_PROPERTIES = {
    URIRef(f"{WD}inheritsStyleFrom"),
    URIRef(f"{WD}implicitGridSnap"),
    URIRef(f"{WD}implicitZOrder"),
    URIRef(f"{WD}implicitGroupDefault"),
}

CANONICAL_ONTOLOGY_PREFIX = "spec/1.0.0/validation/design/ontology/"
CANONICAL_WORKSHOP_PREFIX = "spec/1.0.0/validation/design/workshop/"


class ProcTestError(Exception):
    """Procedural conformance fixture or execution error."""


def _discover_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ProcTestError(f"Unable to locate repository root from {start}")


def _local_design_roots(script_path: Path) -> tuple[Path, Path]:
    ontology_root = script_path.parent.parent
    workshop_candidates = (
        ontology_root.parent / "workshop",
        ontology_root.parent.parent / "workshop" / "design",
    )
    for candidate in workshop_candidates:
        if candidate.exists():
            return ontology_root, candidate
    return ontology_root, workshop_candidates[0]


def _resolve_repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve a repo-relative path against paperhat.dev or sibling workshop repo."""
    primary = repo_root / relative_path
    if primary.exists():
        return primary
    sibling_workshop = repo_root.parent / "workshop" / relative_path
    if sibling_workshop.exists():
        return sibling_workshop

    script_path = Path(__file__).resolve()
    ontology_root, workshop_root = _local_design_roots(script_path)
    if relative_path.startswith(CANONICAL_ONTOLOGY_PREFIX):
        local_ontology = ontology_root / relative_path[len(CANONICAL_ONTOLOGY_PREFIX) :]
        if local_ontology.exists():
            return local_ontology
    if relative_path.startswith(CANONICAL_WORKSHOP_PREFIX):
        local_workshop = workshop_root / relative_path[len(CANONICAL_WORKSHOP_PREFIX) :]
        if local_workshop.exists():
            return local_workshop
    return primary


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ProcTestError(f"Unable to read fixture file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProcTestError(f"Invalid JSON fixture: {path}") from exc


def _graph_format(path: Path) -> str:
    if path.suffix == ".ttl":
        return "turtle"
    if path.suffix == ".nt":
        return "nt"
    raise ProcTestError(f"Unsupported graph fixture extension: {path}")


def _load_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format=_graph_format(path))
    return graph


def _check_nfc_graph(graph: Graph) -> bool:
    for subject, predicate, obj in graph:
        for value in (str(subject), str(predicate), str(obj)):
            if unicodedata.normalize("NFC", value) != value:
                return False
        if isinstance(obj, Literal):
            if obj.language and unicodedata.normalize("NFC", obj.language) != obj.language:
                return False
            if obj.datatype and unicodedata.normalize("NFC", str(obj.datatype)) != str(obj.datatype):
                return False
    return True


def _check_no_blank_nodes(graph: Graph) -> bool:
    for subject, _predicate, obj in graph:
        if isinstance(subject, BNode) or isinstance(obj, BNode):
            return False
    return True


def _canonical_object_sort_key(obj: URIRef | Literal) -> tuple[Any, ...]:
    if isinstance(obj, URIRef):
        return (0, str(obj), "", "", "")
    if isinstance(obj, Literal):
        datatype = str(obj.datatype) if obj.datatype else ""
        language = obj.language or ""
        return (1, str(obj), datatype, language, "")
    raise ProcTestError(f"Unsupported RDF term in object position: {obj!r}")


def _canonical_bytes(graph: Graph) -> bytes:
    if not _check_nfc_graph(graph):
        raise ProcTestError("Graph is not NFC-normalized")
    if not _check_no_blank_nodes(graph):
        raise ProcTestError("Graph contains blank nodes")

    lines: list[str] = []
    for subject, predicate, obj in sorted(
        graph,
        key=lambda triple: (
            str(triple[0]),
            str(triple[1]),
            _canonical_object_sort_key(triple[2]),
        ),
    ):
        lines.append(f"{subject.n3()} {predicate.n3()} {obj.n3()} .")
    return ("\n".join(lines) + "\n").encode("utf-8")


def _sha256_lower_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _check_no_implicit_semantics(graph: Graph) -> bool:
    for forbidden in FORBIDDEN_IMPLICIT_PROPERTIES:
        if any(True for _ in graph.triples((None, forbidden, None))):
            return False
    return True


def _check_defaults_materialized(graph: Graph) -> bool:
    for stroke in graph.subjects(RDF.type, WD_STROKE):
        if not any(True for _ in graph.objects(stroke, WD_STROKE_WIDTH)):
            return False
    for baseline in graph.subjects(RDF.type, WD_BASELINE_GRID):
        if not any(True for _ in graph.objects(baseline, WD_BASELINE_STEP)):
            return False
    return True


def _extract_scope_subgraph(graph: Graph, composition_iri: str) -> Graph:
    composition = URIRef(composition_iri)
    in_scope: set[URIRef] = {composition}
    for node in graph.subjects(WD_OWNED_BY, composition):
        if isinstance(node, URIRef):
            in_scope.add(node)

    scoped = Graph()
    for subject, predicate, obj in graph:
        if subject in in_scope:
            scoped.add((subject, predicate, obj))
    return scoped


def _check_validation_contract(graph: Graph, shapes: Graph, ontology: Graph) -> bool:
    if not _check_no_implicit_semantics(graph):
        return False
    if not _check_defaults_materialized(graph):
        return False
    if not _check_nfc_graph(graph):
        return False
    if not _check_no_blank_nodes(graph):
        return False

    conforms, _result_graph, _results_text = validate(
        data_graph=graph,
        shacl_graph=shapes,
        ont_graph=ontology,
        inference="rdfs",
    )
    return bool(conforms)


def _load_expected_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def _run_case(case: dict[str, Any], repo_root: Path, shapes: Graph, ontology: Graph) -> bool:
    kind = case.get("kind")
    if not isinstance(kind, str) or not kind:
        raise ProcTestError("Fixture case must define non-empty string field 'kind'")

    input_value = case.get("input")
    if not isinstance(input_value, str) or not input_value:
        raise ProcTestError("Fixture case must define non-empty string field 'input'")
    input_path = _resolve_repo_relative_path(repo_root, input_value)

    if kind == "no_implicit_semantics":
        return _check_no_implicit_semantics(_load_graph(input_path))

    if kind == "defaults_materialized":
        return _check_defaults_materialized(_load_graph(input_path))

    if kind == "nfc_graph":
        return _check_nfc_graph(_load_graph(input_path))

    if kind == "no_blank_nodes":
        return _check_no_blank_nodes(_load_graph(input_path))

    if kind == "canonical_serialization":
        expected_value = case.get("expected")
        if not isinstance(expected_value, str) or not expected_value:
            raise ProcTestError("canonical_serialization case requires string field 'expected'")
        expected_path = _resolve_repo_relative_path(repo_root, expected_value)
        rendered = _canonical_bytes(_load_graph(input_path)).decode("utf-8")
        return rendered == _load_expected_text(expected_path)

    if kind == "sha256_hash":
        expected_value = case.get("expected")
        if not isinstance(expected_value, str) or not expected_value:
            raise ProcTestError("sha256_hash case requires string field 'expected'")
        expected_hash = _resolve_repo_relative_path(repo_root, expected_value).read_text(
            encoding="utf-8"
        ).strip()
        actual_hash = _sha256_lower_hex(_canonical_bytes(_load_graph(input_path)))
        return (
            actual_hash == expected_hash
            and expected_hash == expected_hash.lower()
            and len(expected_hash) == 64
        )

    if kind == "scoped_hash":
        composition = case.get("composition")
        expected_value = case.get("expected")
        if not isinstance(composition, str) or not composition:
            raise ProcTestError("scoped_hash case requires string field 'composition'")
        if not isinstance(expected_value, str) or not expected_value:
            raise ProcTestError("scoped_hash case requires string field 'expected'")

        scoped = _extract_scope_subgraph(_load_graph(input_path), composition)
        actual_hash = _sha256_lower_hex(_canonical_bytes(scoped))
        expected_hash = _resolve_repo_relative_path(repo_root, expected_value).read_text(
            encoding="utf-8"
        ).strip()
        return actual_hash == expected_hash

    if kind == "validation_contract":
        return _check_validation_contract(_load_graph(input_path), shapes, ontology)

    raise ProcTestError(f"Unsupported fixture case kind: {kind}")


def main() -> int:
    repo_root = _discover_repo_root(Path(__file__).resolve())
    coverage_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/ontology/fixture-coverage.csv",
    )
    shapes_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/ontology/wd-all.shacl.ttl",
    )
    ontology_path = _resolve_repo_relative_path(
        repo_root,
        "spec/1.0.0/validation/design/ontology/wd-core.ttl",
    )

    shapes = Graph()
    ontology = Graph()
    shapes.parse(shapes_path, format="turtle")
    ontology.parse(ontology_path, format="turtle")

    failures = 0
    with coverage_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            clause_id = row.get("clause_id", "").strip()
            enforcement = row.get("enforcement", "").strip()
            if enforcement != "PROC":
                continue

            positive_fixture = (row.get("positive_fixture") or "").strip()
            negative_fixture = (row.get("negative_fixture") or "").strip()
            if not positive_fixture or not negative_fixture:
                failures += 1
                print(f"[FAIL] proc clause {clause_id}: missing fixture path(s)")
                continue

            positive_case = _read_json(_resolve_repo_relative_path(repo_root, positive_fixture))
            negative_case = _read_json(_resolve_repo_relative_path(repo_root, negative_fixture))

            try:
                positive_ok = _run_case(positive_case, repo_root, shapes, ontology)
                negative_ok = _run_case(negative_case, repo_root, shapes, ontology)
            except ProcTestError as exc:
                failures += 1
                print(f"[FAIL] proc clause {clause_id}: {exc}")
                continue

            if positive_ok and not negative_ok:
                print(f"[PASS] proc clause {clause_id}")
            else:
                failures += 1
                print(
                    f"[FAIL] proc clause {clause_id}: "
                    f"expected positive=true and negative=false, got positive={positive_ok}, negative={negative_ok}"
                )

    if failures:
        print(f"Procedural conformance tests failed with {failures} failing clause(s).")
        return 1

    print("All procedural conformance tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
