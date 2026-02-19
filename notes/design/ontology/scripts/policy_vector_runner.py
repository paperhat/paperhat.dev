#!/usr/bin/env python3
"""Run executable policy evaluation vectors for POLICY_EVALUATION_1_0_0."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from pyshacl import validate
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

WD = "https://paperhat.dev/ns/wd#"

WD_POLICY = URIRef(f"{WD}Policy")
WD_CONDITION = URIRef(f"{WD}Condition")
WD_ACTION = URIRef(f"{WD}Action")
WD_VIEW = URIRef(f"{WD}View")
WD_COMPOSITION = URIRef(f"{WD}Composition")

WD_APPLIES_TO = URIRef(f"{WD}appliesTo")
WD_ENABLED = URIRef(f"{WD}enabled")
WD_PRIORITY = URIRef(f"{WD}priority")
WD_CONFLICT_STRATEGY = URIRef(f"{WD}conflictStrategy")
WD_HAS_CONDITION = URIRef(f"{WD}hasCondition")
WD_HAS_ACTION = URIRef(f"{WD}hasAction")
WD_HAS_POLICY = URIRef(f"{WD}hasPolicy")

WD_CONTEXT_KEY = URIRef(f"{WD}contextKey")
WD_OPERATOR = URIRef(f"{WD}operator")
WD_CONDITION_VALUE_DECIMAL = URIRef(f"{WD}conditionValueDecimal")
WD_CONDITION_VALUE_INTEGER = URIRef(f"{WD}conditionValueInteger")
WD_CONDITION_VALUE_STRING = URIRef(f"{WD}conditionValueString")
WD_CONDITION_VALUE_BOOLEAN = URIRef(f"{WD}conditionValueBoolean")

WD_ACTION_MODE = URIRef(f"{WD}actionMode")
WD_TARGET_NODE = URIRef(f"{WD}targetNode")
WD_TARGET_PROPERTY = URIRef(f"{WD}targetProperty")
WD_ACTION_VALUE_DECIMAL = URIRef(f"{WD}actionValueDecimal")
WD_ACTION_VALUE_INTEGER = URIRef(f"{WD}actionValueInteger")
WD_ACTION_VALUE_STRING = URIRef(f"{WD}actionValueString")
WD_ACTION_VALUE_BOOLEAN = URIRef(f"{WD}actionValueBoolean")
WD_ACTION_VALUE_IRI = URIRef(f"{WD}actionValueIRI")

WD_OP_EQ = URIRef(f"{WD}OpEq")
WD_OP_NE = URIRef(f"{WD}OpNe")
WD_OP_LT = URIRef(f"{WD}OpLt")
WD_OP_LTE = URIRef(f"{WD}OpLte")
WD_OP_GT = URIRef(f"{WD}OpGt")
WD_OP_GTE = URIRef(f"{WD}OpGte")

WD_STRATEGY_ERROR = URIRef(f"{WD}ErrorOnConflict")
WD_STRATEGY_FIRST = URIRef(f"{WD}FirstMatchWins")
WD_STRATEGY_PRIORITY = URIRef(f"{WD}HigherPriorityWins")

WD_MODE_REPLACE = URIRef(f"{WD}ReplaceAll")
WD_MODE_ADD = URIRef(f"{WD}Add")
WD_MODE_REMOVE = URIRef(f"{WD}Remove")


class EvaluationError(Exception):
    """Evaluation failed under fail-closed rules."""


@dataclass(frozen=True)
class TypedValue:
    kind: str
    value: Any


@dataclass(frozen=True)
class PolicyInfo:
    policy: URIRef
    priority: int
    specificity_rank: int  # 0 = view, 1 = composition
    strategy: URIRef


@dataclass(frozen=True)
class ActionInfo:
    action: URIRef
    mode: URIRef
    target_node: URIRef
    target_property: URIRef
    value: URIRef | Literal
    policy: PolicyInfo


def must_single_object(graph: Graph, subject: URIRef, predicate: URIRef) -> URIRef | Literal:
    values = list(graph.objects(subject, predicate))
    if len(values) != 1:
        raise EvaluationError(f"Expected exactly one value for {predicate} on {subject}")
    return values[0]


def parse_condition_value(graph: Graph, condition: URIRef) -> TypedValue:
    candidates = []
    for predicate, kind in (
        (WD_CONDITION_VALUE_DECIMAL, "decimal"),
        (WD_CONDITION_VALUE_INTEGER, "integer"),
        (WD_CONDITION_VALUE_STRING, "string"),
        (WD_CONDITION_VALUE_BOOLEAN, "boolean"),
    ):
        for value in graph.objects(condition, predicate):
            candidates.append(TypedValue(kind, value.toPython()))

    if len(candidates) != 1:
        raise EvaluationError(f"Condition {condition} must have exactly one typed condition value")
    return candidates[0]


def parse_action_value(graph: Graph, action: URIRef) -> URIRef | Literal:
    candidates: list[URIRef | Literal] = []
    for predicate in (
        WD_ACTION_VALUE_DECIMAL,
        WD_ACTION_VALUE_INTEGER,
        WD_ACTION_VALUE_STRING,
        WD_ACTION_VALUE_BOOLEAN,
        WD_ACTION_VALUE_IRI,
    ):
        candidates.extend(graph.objects(action, predicate))

    if len(candidates) != 1:
        raise EvaluationError(f"Action {action} must have exactly one typed action value")
    return candidates[0]


def load_context(vector_context: dict[str, dict[str, Any]]) -> dict[URIRef, TypedValue]:
    context: dict[URIRef, TypedValue] = {}
    for key_iri, typed in vector_context.items():
        kind = typed.get("type")
        if kind not in {"integer", "decimal", "string", "boolean"}:
            raise EvaluationError(f"Unsupported context type '{kind}' for key {key_iri}")

        raw_value = typed.get("value")
        if kind == "integer":
            value = int(raw_value)
        elif kind == "decimal":
            value = Decimal(str(raw_value))
        elif kind == "string":
            value = str(raw_value)
        else:
            value = bool(raw_value)

        context[URIRef(key_iri)] = TypedValue(kind, value)

    return context


def to_numeric(value: TypedValue) -> Decimal:
    if value.kind == "integer":
        return Decimal(int(value.value))
    if value.kind == "decimal":
        return Decimal(str(value.value))
    raise EvaluationError("Numeric comparison attempted on non-numeric value")


def evaluate_condition(graph: Graph, condition: URIRef, context: dict[URIRef, TypedValue]) -> bool:
    context_key = must_single_object(graph, condition, WD_CONTEXT_KEY)
    if not isinstance(context_key, URIRef):
        raise EvaluationError("contextKey must be an IRI")

    operator = must_single_object(graph, condition, WD_OPERATOR)
    if not isinstance(operator, URIRef):
        raise EvaluationError("operator must be an IRI")

    condition_value = parse_condition_value(graph, condition)

    if context_key not in context:
        raise EvaluationError(f"Missing context key: {context_key}")

    context_value = context[context_key]

    compatible_numeric = {condition_value.kind, context_value.kind}.issubset({"integer", "decimal"})
    if not compatible_numeric and condition_value.kind != context_value.kind:
        raise EvaluationError(
            f"Context type mismatch for {context_key}: expected {condition_value.kind}, got {context_value.kind}"
        )

    if operator in {WD_OP_LT, WD_OP_LTE, WD_OP_GT, WD_OP_GTE}:
        left = to_numeric(context_value)
        right = to_numeric(condition_value)
        if operator == WD_OP_LT:
            return left < right
        if operator == WD_OP_LTE:
            return left <= right
        if operator == WD_OP_GT:
            return left > right
        return left >= right

    if operator == WD_OP_EQ:
        return context_value.value == condition_value.value

    if operator == WD_OP_NE:
        return context_value.value != condition_value.value

    raise EvaluationError(f"Unsupported operator: {operator}")


def is_enabled(graph: Graph, policy: URIRef) -> bool:
    enabled_literal = must_single_object(graph, policy, WD_ENABLED)
    if not isinstance(enabled_literal, Literal):
        raise EvaluationError(f"Policy {policy} enabled must be a literal")
    return bool(enabled_literal.toPython())


def collect_candidates(
    graph: Graph,
    composition: URIRef,
    view: URIRef | None,
    context: dict[URIRef, TypedValue],
) -> list[PolicyInfo]:
    candidates: list[PolicyInfo] = []

    for policy in set(graph.subjects(WD_APPLIES_TO, composition)):
        if (policy, RDF.type, WD_POLICY) not in graph:
            continue
        if not is_enabled(graph, policy):
            continue

        if policy_matches(graph, policy, context):
            candidates.append(build_policy_info(graph, policy, view))

    if view is not None:
        for policy in set(graph.subjects(WD_APPLIES_TO, view)):
            if (policy, RDF.type, WD_POLICY) not in graph:
                continue
            if not is_enabled(graph, policy):
                continue

            if policy_matches(graph, policy, context):
                candidates.append(build_policy_info(graph, policy, view))

    return sorted(
        candidates,
        key=lambda p: (-p.priority, p.specificity_rank, str(p.policy)),
    )


def build_policy_info(graph: Graph, policy: URIRef, target_view: URIRef | None) -> PolicyInfo:
    priority_literal = must_single_object(graph, policy, WD_PRIORITY)
    strategy = must_single_object(graph, policy, WD_CONFLICT_STRATEGY)
    applies_to = must_single_object(graph, policy, WD_APPLIES_TO)

    if not isinstance(priority_literal, Literal):
        raise EvaluationError(f"Policy {policy} priority must be a literal")
    if not isinstance(strategy, URIRef):
        raise EvaluationError(f"Policy {policy} conflictStrategy must be an IRI")
    if not isinstance(applies_to, URIRef):
        raise EvaluationError(f"Policy {policy} appliesTo must be an IRI")

    specificity_rank = 0 if target_view is not None and applies_to == target_view else 1

    return PolicyInfo(
        policy=policy,
        priority=int(priority_literal.toPython()),
        specificity_rank=specificity_rank,
        strategy=strategy,
    )


def policy_matches(graph: Graph, policy: URIRef, context: dict[URIRef, TypedValue]) -> bool:
    conditions = list(graph.objects(policy, WD_HAS_CONDITION))
    if not conditions:
        raise EvaluationError(f"Policy {policy} has no conditions")

    for condition in conditions:
        if (condition, RDF.type, WD_CONDITION) not in graph:
            raise EvaluationError(f"Condition node missing type wd:Condition: {condition}")
        if not evaluate_condition(graph, condition, context):
            return False

    return True


def collect_ordered_actions(graph: Graph, policies: list[PolicyInfo]) -> list[ActionInfo]:
    ordered_actions: list[ActionInfo] = []
    for policy in policies:
        actions = sorted(graph.objects(policy.policy, WD_HAS_ACTION), key=lambda iri: str(iri))
        if not actions:
            raise EvaluationError(f"Policy {policy.policy} has no actions")

        for action in actions:
            if (action, RDF.type, WD_ACTION) not in graph:
                raise EvaluationError(f"Action node missing type wd:Action: {action}")

            mode = must_single_object(graph, action, WD_ACTION_MODE)
            target_node = must_single_object(graph, action, WD_TARGET_NODE)
            target_property = must_single_object(graph, action, WD_TARGET_PROPERTY)
            value = parse_action_value(graph, action)

            if not isinstance(mode, URIRef):
                raise EvaluationError(f"Action mode must be an IRI on action {action}")
            if not isinstance(target_node, URIRef):
                raise EvaluationError(f"Action targetNode must be an IRI on action {action}")
            if not isinstance(target_property, URIRef):
                raise EvaluationError(f"Action targetProperty must be an IRI on action {action}")

            ordered_actions.append(
                ActionInfo(
                    action=action,
                    mode=mode,
                    target_node=target_node,
                    target_property=target_property,
                    value=value,
                    policy=policy,
                )
            )

    return ordered_actions


def resolve_conflicts(policies: list[PolicyInfo], ordered_actions: list[ActionInfo]) -> list[ActionInfo]:
    if not policies:
        return []

    strategies = {policy.strategy for policy in policies}
    if len(strategies) != 1:
        raise EvaluationError("Matched policies have mixed conflict strategies")

    strategy = next(iter(strategies))

    by_key: dict[tuple[URIRef, URIRef], list[ActionInfo]] = {}
    for action in ordered_actions:
        key = (action.target_node, action.target_property)
        by_key.setdefault(key, []).append(action)

    if strategy == WD_STRATEGY_ERROR:
        for key, actions in by_key.items():
            if len(actions) > 1:
                raise EvaluationError(f"Conflict under ErrorOnConflict for key {key}")
        return ordered_actions

    if strategy in {WD_STRATEGY_FIRST, WD_STRATEGY_PRIORITY}:
        selected: list[ActionInfo] = []
        seen_keys: set[tuple[URIRef, URIRef]] = set()
        for action in ordered_actions:
            key = (action.target_node, action.target_property)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            selected.append(action)
        return selected

    raise EvaluationError(f"Unsupported conflict strategy: {strategy}")


def triple_to_nt(subject: URIRef, predicate: URIRef, obj: URIRef | Literal) -> str:
    return f"{subject.n3()} {predicate.n3()} {obj.n3()} ."


def apply_actions(graph: Graph, actions: list[ActionInfo]) -> tuple[list[str], list[str]]:
    removed: set[str] = set()
    added: set[str] = set()

    for action in actions:
        subject = action.target_node
        predicate = action.target_property
        obj = action.value
        new_triple = (subject, predicate, obj)

        if action.mode == WD_MODE_REPLACE:
            existing_values = list(graph.objects(subject, predicate))
            for old in existing_values:
                graph.remove((subject, predicate, old))
                removed.add(triple_to_nt(subject, predicate, old))

            if new_triple not in graph:
                graph.add(new_triple)
                added.add(triple_to_nt(subject, predicate, obj))

        elif action.mode == WD_MODE_ADD:
            if new_triple not in graph:
                graph.add(new_triple)
                added.add(triple_to_nt(subject, predicate, obj))

        elif action.mode == WD_MODE_REMOVE:
            if new_triple in graph:
                graph.remove(new_triple)
                removed.add(triple_to_nt(subject, predicate, obj))

        else:
            raise EvaluationError(f"Unsupported action mode: {action.mode}")

    return sorted(removed), sorted(added)


def validate_graph(graph: Graph, shapes: Graph, ontology: Graph, stage: str) -> None:
    conforms, _results_graph, results_text = validate(
        data_graph=graph,
        shacl_graph=shapes,
        ont_graph=ontology,
        inference="rdfs",
    )
    if not conforms:
        raise EvaluationError(f"SHACL validation failed at {stage}: {results_text}")


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise EvaluationError(f"Missing required attribute '{name}' at {path}")
    return value


def _parse_cdx_vector(vector_path: Path) -> dict[str, Any]:
    try:
        root = ET.parse(vector_path).getroot()
    except ET.ParseError as exc:  # noqa: PERF203
        raise EvaluationError(f"Invalid CDX vector syntax in {vector_path}: {exc}") from exc

    if root.tag != "PolicyVector":
        raise EvaluationError(f"Root tag must be PolicyVector in {vector_path}")

    vector_id = _require_attr(root, "id", "PolicyVector")
    graph_file = _require_attr(root, "graphFile", "PolicyVector")
    composition_iri = _require_attr(root, "compositionIri", "PolicyVector")
    view_iri = root.get("viewIri")
    if view_iri == "":
        view_iri = None

    context: dict[str, dict[str, Any]] = {}
    for entry in root.findall("ContextEntry"):
        key = _require_attr(entry, "key", "PolicyVector/ContextEntry")
        kind = _require_attr(entry, "type", f"PolicyVector/ContextEntry[@key='{key}']")
        raw_value = _require_attr(entry, "value", f"PolicyVector/ContextEntry[@key='{key}']")

        if kind == "integer":
            value: Any = int(raw_value)
        elif kind == "decimal":
            value = raw_value
        elif kind == "boolean":
            if raw_value not in {"true", "false"}:
                raise EvaluationError(f"Boolean ContextEntry value must be true/false for key {key}")
            value = raw_value == "true"
        elif kind == "string":
            value = raw_value
        else:
            raise EvaluationError(f"Unsupported ContextEntry type '{kind}' for key {key}")

        context[key] = {"type": kind, "value": value}

    expect_node = root.find("Expect")
    if expect_node is None:
        raise EvaluationError(f"Missing Expect node in {vector_path}")
    status = _require_attr(expect_node, "status", "PolicyVector/Expect")
    if status not in {"ok", "error"}:
        raise EvaluationError(f"Unsupported Expect status '{status}' in {vector_path}")

    expect: dict[str, Any] = {"status": status}

    if status == "error":
        expect["error"] = expect_node.get("error", "EVALUATION_ERROR")
    else:
        selected_actions = [
            _require_attr(action, "iri", "PolicyVector/Expect/SelectedActions/Action")
            for action in expect_node.findall("SelectedActions/Action")
        ]

        delta_node = expect_node.find("Delta")
        if delta_node is None:
            raise EvaluationError(f"Missing Delta node for status=ok in {vector_path}")
        delta_remove = [
            _require_attr(entry, "triple", "PolicyVector/Expect/Delta/Remove")
            for entry in delta_node.findall("Remove")
        ]
        delta_add = [
            _require_attr(entry, "triple", "PolicyVector/Expect/Delta/Add")
            for entry in delta_node.findall("Add")
        ]

        expect["selected_actions"] = selected_actions
        expect["delta"] = {"remove": delta_remove, "add": delta_add}

    return {
        "id": vector_id,
        "graph_file": graph_file,
        "composition_iri": composition_iri,
        "view_iri": view_iri,
        "context": context,
        "expect": expect,
    }


def _load_vector(vector_path: Path) -> dict[str, Any]:
    if vector_path.suffix == ".cdx":
        return _parse_cdx_vector(vector_path)
    raise EvaluationError(f"Unsupported vector file extension: {vector_path}")


def run_vector(vector_path: Path, repo_root: Path, shapes: Graph, ontology: Graph) -> tuple[bool, str]:
    vector = _load_vector(vector_path)

    vector_id = vector.get("id", vector_path.name)

    try:
        graph_file = repo_root / vector["graph_file"]
        composition = URIRef(vector["composition_iri"])
        view_value = vector.get("view_iri")
        view = URIRef(view_value) if view_value else None
        context = load_context(vector.get("context", {}))

        graph = Graph()
        graph.parse(graph_file, format="turtle")

        validate_graph(graph, shapes, ontology, stage="pre-evaluation")

        if (composition, RDF.type, WD_COMPOSITION) not in graph:
            raise EvaluationError(f"Composition not found or mistyped: {composition}")

        if view is not None and (view, RDF.type, WD_VIEW) not in graph:
            raise EvaluationError(f"View not found or mistyped: {view}")

        matched_policies = collect_candidates(graph, composition, view, context)
        ordered_actions = collect_ordered_actions(graph, matched_policies)
        selected_actions = resolve_conflicts(matched_policies, ordered_actions)
        removed, added = apply_actions(graph, selected_actions)

        validate_graph(graph, shapes, ontology, stage="post-evaluation")

        actual = {
            "status": "ok",
            "selected_actions": [str(action.action) for action in selected_actions],
            "delta": {
                "remove": removed,
                "add": added,
            },
        }

    except EvaluationError:
        actual = {
            "status": "error",
            "error": "EVALUATION_ERROR",
        }

    expected = vector.get("expect", {})

    if expected.get("status") != actual.get("status"):
        return False, f"status mismatch expected={expected.get('status')} actual={actual.get('status')}"

    if actual["status"] == "error":
        expected_error = expected.get("error", "EVALUATION_ERROR")
        if expected_error != actual.get("error"):
            return False, f"error mismatch expected={expected_error} actual={actual.get('error')}"
        return True, vector_id

    expected_actions = expected.get("selected_actions", [])
    if expected_actions != actual.get("selected_actions"):
        return False, (
            "selected_actions mismatch\n"
            f"expected={expected_actions}\n"
            f"actual={actual.get('selected_actions')}"
        )

    expected_remove = sorted(expected.get("delta", {}).get("remove", []))
    expected_add = sorted(expected.get("delta", {}).get("add", []))
    actual_remove = sorted(actual.get("delta", {}).get("remove", []))
    actual_add = sorted(actual.get("delta", {}).get("add", []))

    if expected_remove != actual_remove:
        return False, f"delta.remove mismatch expected={expected_remove} actual={actual_remove}"

    if expected_add != actual_add:
        return False, f"delta.add mismatch expected={expected_add} actual={actual_add}"

    return True, vector_id


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    vector_dir = repo_root / "notes/design/ontology/policy-vectors"

    vector_files = sorted(vector_dir.glob("*.cdx"))
    if not vector_files:
        print("No policy vector files found (.cdx).", file=sys.stderr)
        return 1

    shapes = Graph()
    ontology = Graph()
    shapes.parse(repo_root / "notes/design/ontology/wd-all.shacl.ttl", format="turtle")
    ontology.parse(repo_root / "notes/design/ontology/wd-core.ttl", format="turtle")

    failures = 0

    for vector_path in vector_files:
        ok, detail = run_vector(vector_path, repo_root, shapes, ontology)
        if ok:
            print(f"[PASS] policy vector: {vector_path.name}")
        else:
            failures += 1
            print(f"[FAIL] policy vector: {vector_path.name}: {detail}", file=sys.stderr)

    if failures:
        print(f"Policy vector run failed with {failures} failing vector(s).", file=sys.stderr)
        return 1

    print("All policy vectors passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
