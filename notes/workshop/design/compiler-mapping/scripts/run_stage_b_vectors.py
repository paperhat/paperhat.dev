#!/usr/bin/env python3
"""Run Stage B evaluation vectors defined in CDX."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

EVALUATION_ERROR = "EVALUATION_ERROR"


class StageBError(Exception):
    """Stage B vector/harness definition error."""


class StageBEvaluationError(Exception):
    """Stage B evaluation input/precondition failure."""


@dataclass(frozen=True)
class SoftTerm:
    key: str
    weight_class: str
    weight: Decimal


@dataclass(frozen=True)
class RelaxationRule:
    relax_order: int
    relax_weight_class: str | None
    relaxation_action: str


@dataclass(frozen=True)
class OverrideConstraint:
    kind: str
    target_ref: str


@dataclass(frozen=True)
class StageBRequest:
    hard_constraint_keys: tuple[str, ...]
    soft_terms: tuple[SoftTerm, ...]
    relaxation_rules: tuple[RelaxationRule, ...]
    satisfice_threshold: Decimal | None
    override_mode: str | None
    overrides: tuple[OverrideConstraint, ...]


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    hard_results: dict[str, bool]
    soft_scores: dict[str, Decimal]
    override_results: dict[tuple[str, str], bool]


@dataclass(frozen=True)
class VectorCase:
    vector_id: str
    expected: dict[str, Any]
    request: StageBRequest | None
    candidates: list[Candidate]
    precondition_error: bool


def _require_attr(
    element: ET.Element,
    name: str,
    path: str,
    error_class: type[Exception] = StageBError,
) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise error_class(f"Missing required attribute '{name}' at {path}")
    return value


def _parse_bool(
    value: str,
    path: str,
    error_class: type[Exception] = StageBError,
) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise error_class(f"Invalid boolean '{value}' at {path}; expected true or false")


def _parse_decimal(
    value: str,
    path: str,
    error_class: type[Exception] = StageBError,
) -> Decimal:
    try:
        return Decimal(value)
    except Exception as exc:  # noqa: BLE001
        raise error_class(f"Invalid decimal '{value}' at {path}") from exc


def _load_expectation(root: ET.Element, vector_id: str) -> dict[str, Any]:
    expect_node = root.find("Expect")
    if expect_node is None:
        raise StageBError(f"StageBVector '{vector_id}' MUST define Expect")

    status = _require_attr(expect_node, "status", f"StageBVector[@id='{vector_id}']/Expect")
    if status not in {"ok", "error"}:
        raise StageBError(f"Unsupported Expect status '{status}' in vector '{vector_id}'")

    expected: dict[str, Any] = {"status": status}
    if status == "error":
        expected["error"] = expect_node.get("error", EVALUATION_ERROR)
        return expected

    expected["selected_candidate"] = _require_attr(
        expect_node,
        "selectedCandidate",
        f"StageBVector[@id='{vector_id}']/Expect",
    )
    relaxes: list[tuple[int, str | None, str]] = []
    for node in expect_node.findall("AppliedRelaxation"):
        order_raw = _require_attr(
            node,
            "relaxOrder",
            f"StageBVector[@id='{vector_id}']/Expect/AppliedRelaxation",
        )
        try:
            order = int(order_raw)
        except Exception as exc:  # noqa: BLE001
            raise StageBError(f"Invalid relaxOrder '{order_raw}' in vector '{vector_id}'") from exc
        relaxes.append(
            (
                order,
                node.get("relaxWeightClass"),
                _require_attr(
                    node,
                    "relaxationAction",
                    f"StageBVector[@id='{vector_id}']/Expect/AppliedRelaxation[@relaxOrder='{order}']",
                ),
            )
        )
    expected["applied_relaxations"] = relaxes
    return expected


def load_stage_b_request(path: Path) -> StageBRequest:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise StageBEvaluationError(f"Malformed compiled request XML: {path}") from exc

    if root.tag != "CompiledAdaptiveRequest":
        raise StageBEvaluationError(f"Root tag must be CompiledAdaptiveRequest in {path}")

    stage_b = root.find("StageB")
    if stage_b is None:
        raise StageBEvaluationError(f"Missing StageB node in {path}")

    optimization = stage_b.find("OptimizationProfile")
    if optimization is None:
        raise StageBEvaluationError(f"Missing OptimizationProfile node in {path}")

    hard_keys = tuple(
        _require_attr(
            node,
            "constraintKey",
            "CompiledAdaptiveRequest/StageB/OptimizationProfile/HardConstraint",
            StageBEvaluationError,
        )
        for node in optimization.findall("HardConstraint")
    )

    soft_terms: list[SoftTerm] = []
    for node in optimization.findall("SoftTerm"):
        key = _require_attr(
            node,
            "termKey",
            "CompiledAdaptiveRequest/StageB/OptimizationProfile/SoftTerm",
            StageBEvaluationError,
        )
        weight_class = _require_attr(
            node,
            "weightClass",
            f"CompiledAdaptiveRequest/StageB/OptimizationProfile/SoftTerm[@termKey='{key}']",
            StageBEvaluationError,
        )
        weight_raw = _require_attr(
            node,
            "weight",
            f"CompiledAdaptiveRequest/StageB/OptimizationProfile/SoftTerm[@termKey='{key}']",
            StageBEvaluationError,
        )
        weight = _parse_decimal(
            weight_raw,
            f"CompiledAdaptiveRequest/StageB/OptimizationProfile/SoftTerm[@termKey='{key}']/@weight",
            StageBEvaluationError,
        )
        if weight <= 0:
            raise StageBEvaluationError(f"SoftTerm weight MUST be > 0 for termKey '{key}'")
        soft_terms.append(SoftTerm(key=key, weight_class=weight_class, weight=weight))

    rules: list[RelaxationRule] = []
    for node in optimization.findall("RelaxationRule"):
        relax_order_raw = _require_attr(
            node,
            "relaxOrder",
            "CompiledAdaptiveRequest/StageB/OptimizationProfile/RelaxationRule",
            StageBEvaluationError,
        )
        try:
            relax_order = int(relax_order_raw)
        except Exception as exc:  # noqa: BLE001
            raise StageBEvaluationError(f"Invalid integer relaxOrder '{relax_order_raw}'") from exc
        if relax_order < 1:
            raise StageBEvaluationError("RelaxationRule relaxOrder MUST be >= 1")

        relax_weight_class = node.get("relaxWeightClass")
        action = _require_attr(
            node,
            "relaxationAction",
            f"CompiledAdaptiveRequest/StageB/OptimizationProfile/RelaxationRule[@relaxOrder='{relax_order}']",
            StageBEvaluationError,
        )
        rules.append(
            RelaxationRule(
                relax_order=relax_order,
                relax_weight_class=relax_weight_class,
                relaxation_action=action,
            )
        )

    rules.sort(key=lambda r: (r.relax_order, r.relax_weight_class or "", r.relaxation_action))

    threshold: Decimal | None = None
    threshold_raw = optimization.get("satisficeThreshold")
    if threshold_raw is not None:
        threshold = _parse_decimal(
            threshold_raw,
            "CompiledAdaptiveRequest/StageB/OptimizationProfile/@satisficeThreshold",
            StageBEvaluationError,
        )
        if threshold < 0 or threshold > 1:
            raise StageBEvaluationError("satisficeThreshold MUST be in [0,1]")

    override_node = stage_b.find("OverrideSet")
    override_mode = None
    overrides: list[OverrideConstraint] = []
    if override_node is not None:
        override_mode = override_node.get("overrideMode")
        for node in override_node.findall("OverrideConstraint"):
            kind = _require_attr(
                node,
                "overrideKind",
                "CompiledAdaptiveRequest/StageB/OverrideSet/OverrideConstraint",
                StageBEvaluationError,
            )
            target_ref = _require_attr(
                node,
                "targetRef",
                f"CompiledAdaptiveRequest/StageB/OverrideSet/OverrideConstraint[@overrideKind='{kind}']",
                StageBEvaluationError,
            )
            overrides.append(OverrideConstraint(kind=kind, target_ref=target_ref))

    return StageBRequest(
        hard_constraint_keys=hard_keys,
        soft_terms=tuple(soft_terms),
        relaxation_rules=tuple(rules),
        satisfice_threshold=threshold,
        override_mode=override_mode,
        overrides=tuple(overrides),
    )


def parse_candidate(node: ET.Element) -> Candidate:
    candidate_id = _require_attr(node, "id", "StageBVector/Candidate", StageBEvaluationError)

    hard_results: dict[str, bool] = {}
    for child in node.findall("HardConstraintResult"):
        key = _require_attr(
            child,
            "key",
            f"StageBVector/Candidate[@id='{candidate_id}']/HardConstraintResult",
            StageBEvaluationError,
        )
        if key in hard_results:
            raise StageBEvaluationError(
                f"Candidate '{candidate_id}' has duplicate HardConstraintResult key '{key}'"
            )
        satisfied = _parse_bool(
            _require_attr(
                child,
                "satisfied",
                f"StageBVector/Candidate[@id='{candidate_id}']/HardConstraintResult[@key='{key}']",
                StageBEvaluationError,
            ),
            f"StageBVector/Candidate[@id='{candidate_id}']/HardConstraintResult[@key='{key}']/@satisfied",
            StageBEvaluationError,
        )
        hard_results[key] = satisfied

    soft_scores: dict[str, Decimal] = {}
    for child in node.findall("SoftTermScore"):
        key = _require_attr(
            child,
            "key",
            f"StageBVector/Candidate[@id='{candidate_id}']/SoftTermScore",
            StageBEvaluationError,
        )
        if key in soft_scores:
            raise StageBEvaluationError(f"Candidate '{candidate_id}' has duplicate SoftTermScore key '{key}'")
        value_raw = _require_attr(
            child,
            "value",
            f"StageBVector/Candidate[@id='{candidate_id}']/SoftTermScore[@key='{key}']",
            StageBEvaluationError,
        )
        soft_scores[key] = _parse_decimal(
            value_raw,
            f"StageBVector/Candidate[@id='{candidate_id}']/SoftTermScore[@key='{key}']/@value",
            StageBEvaluationError,
        )

    override_results: dict[tuple[str, str], bool] = {}
    for child in node.findall("OverrideResult"):
        kind = _require_attr(
            child,
            "kind",
            f"StageBVector/Candidate[@id='{candidate_id}']/OverrideResult",
            StageBEvaluationError,
        )
        target_ref = _require_attr(
            child,
            "targetRef",
            f"StageBVector/Candidate[@id='{candidate_id}']/OverrideResult[@kind='{kind}']",
            StageBEvaluationError,
        )
        tuple_key = (kind, target_ref)
        if tuple_key in override_results:
            raise StageBEvaluationError(
                "Candidate "
                f"'{candidate_id}' has duplicate OverrideResult for kind='{kind}' targetRef='{target_ref}'"
            )
        satisfied = _parse_bool(
            _require_attr(
                child,
                "satisfied",
                f"StageBVector/Candidate[@id='{candidate_id}']/OverrideResult[@kind='{kind}' and @targetRef='{target_ref}']",
                StageBEvaluationError,
            ),
            f"StageBVector/Candidate[@id='{candidate_id}']/OverrideResult[@kind='{kind}' and @targetRef='{target_ref}']/@satisfied",
            StageBEvaluationError,
        )
        override_results[tuple_key] = satisfied

    return Candidate(
        candidate_id=candidate_id,
        hard_results=hard_results,
        soft_scores=soft_scores,
        override_results=override_results,
    )


def load_vector(path: Path, repo_root: Path) -> VectorCase:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise StageBError(f"Malformed StageBVector XML: {path}") from exc

    if root.tag != "StageBVector":
        raise StageBError(f"Root tag must be StageBVector in {path}")

    vector_id = _require_attr(root, "id", "StageBVector")
    expected = _load_expectation(root, vector_id)
    request_file = _require_attr(root, "compiledRequestFile", "StageBVector")

    precondition_error = False
    request: StageBRequest | None
    candidates: list[Candidate] = []

    try:
        request = load_stage_b_request(repo_root / request_file)
    except StageBEvaluationError:
        precondition_error = True
        request = None

    if not precondition_error:
        try:
            candidates = [parse_candidate(node) for node in root.findall("Candidate")]
        except StageBEvaluationError:
            precondition_error = True
            candidates = []

    return VectorCase(
        vector_id=vector_id,
        expected=expected,
        request=request,
        candidates=candidates,
        precondition_error=precondition_error,
    )


def _candidate_hard_feasible(
    candidate: Candidate,
    required_hard_keys: set[str],
    override_mode: str | None,
    overrides: tuple[OverrideConstraint, ...],
) -> bool:
    for key in required_hard_keys:
        if key not in candidate.hard_results:
            raise StageBEvaluationError(
                f"Candidate '{candidate.candidate_id}' missing HardConstraintResult for key '{key}'"
            )
        if not candidate.hard_results[key]:
            return False

    if override_mode not in {None, "strict", "advisory"}:
        raise StageBEvaluationError(f"Unsupported overrideMode '{override_mode}'")

    if override_mode == "strict":
        for override in overrides:
            tuple_key = (override.kind, override.target_ref)
            if tuple_key not in candidate.override_results:
                raise StageBEvaluationError(
                    "Candidate "
                    f"'{candidate.candidate_id}' missing OverrideResult for kind='{override.kind}' targetRef='{override.target_ref}'"
                )
            if not candidate.override_results[tuple_key]:
                return False

    return True


def _candidate_score(candidate: Candidate, active_soft_terms: tuple[SoftTerm, ...]) -> Decimal:
    if not active_soft_terms:
        raise StageBEvaluationError("Active soft term set MUST NOT be empty")

    total_weight = Decimal("0")
    weighted_sum = Decimal("0")
    for term in active_soft_terms:
        if term.key not in candidate.soft_scores:
            raise StageBEvaluationError(
                f"Candidate '{candidate.candidate_id}' missing SoftTermScore for term key '{term.key}'"
            )
        score = candidate.soft_scores[term.key]
        if score < 0 or score > 1:
            raise StageBEvaluationError(
                f"Soft term score MUST be in [0,1] for candidate '{candidate.candidate_id}', term '{term.key}'"
            )
        total_weight += term.weight
        weighted_sum += term.weight * score

    if total_weight <= 0:
        raise StageBEvaluationError("Sum of active soft term weights MUST be > 0")

    return weighted_sum / total_weight


def _format_decimal(value: Decimal) -> str:
    return format(value.normalize(), "f")


def evaluate(request: StageBRequest | None, candidates: list[Candidate]) -> dict[str, Any]:
    try:
        if request is None:
            raise StageBEvaluationError("Missing compiled request")
        if not candidates:
            raise StageBEvaluationError("Candidate set MUST NOT be empty")

        active_hard_keys = set(request.hard_constraint_keys)
        active_soft_terms = tuple(request.soft_terms)
        threshold = request.satisfice_threshold
        applied_relaxations: list[RelaxationRule] = []

        rule_index = 0
        while True:
            hard_feasible = [
                candidate
                for candidate in candidates
                if _candidate_hard_feasible(
                    candidate,
                    active_hard_keys,
                    request.override_mode,
                    request.overrides,
                )
            ]

            if not hard_feasible:
                return {"status": "error", "error": EVALUATION_ERROR}

            scored = [(candidate, _candidate_score(candidate, active_soft_terms)) for candidate in hard_feasible]

            qualified = scored
            if threshold is not None:
                qualified = [(candidate, score) for candidate, score in scored if score >= threshold]

            if qualified:
                qualified.sort(key=lambda item: (-item[1], item[0].candidate_id))
                selected_candidate, selected_score = qualified[0]
                return {
                    "status": "ok",
                    "selected_candidate": selected_candidate.candidate_id,
                    "selected_score": _format_decimal(selected_score),
                    "applied_relaxations": [
                        (rule.relax_order, rule.relax_weight_class, rule.relaxation_action)
                        for rule in applied_relaxations
                    ],
                }

            if rule_index >= len(request.relaxation_rules):
                return {"status": "error", "error": EVALUATION_ERROR}

            rule = request.relaxation_rules[rule_index]
            rule_index += 1

            if rule.relaxation_action == "dropTerm":
                if rule.relax_weight_class is None:
                    raise StageBEvaluationError("dropTerm requires relaxWeightClass")
                next_terms = tuple(
                    term for term in active_soft_terms if term.weight_class != rule.relax_weight_class
                )
                if next_terms:
                    active_soft_terms = next_terms
            elif rule.relaxation_action == "widenThreshold":
                if threshold is not None:
                    threshold = threshold - Decimal("0.1")
                    if threshold < 0:
                        threshold = Decimal("0")
            elif rule.relaxation_action == "allowGroupSplit":
                active_hard_keys.discard("preserveGroupCohesion")
            else:
                raise StageBEvaluationError(f"Unsupported relaxation action '{rule.relaxation_action}'")

            applied_relaxations.append(rule)
    except StageBEvaluationError:
        return {"status": "error", "error": EVALUATION_ERROR}


def run_vector(path: Path, repo_root: Path) -> tuple[bool, str]:
    try:
        case = load_vector(path, repo_root)
    except StageBError as exc:
        return False, str(exc)

    actual = {"status": "error", "error": EVALUATION_ERROR} if case.precondition_error else evaluate(
        case.request,
        case.candidates,
    )

    expected = case.expected
    if actual.get("status") != expected.get("status"):
        return False, (
            f"status mismatch expected={expected.get('status')} actual={actual.get('status')}"
        )

    if expected["status"] == "error":
        expected_error = expected.get("error", EVALUATION_ERROR)
        if actual.get("error") != expected_error:
            return False, f"error mismatch expected={expected_error} actual={actual.get('error')}"
        return True, case.vector_id

    if actual.get("selected_candidate") != expected.get("selected_candidate"):
        return False, (
            "selected_candidate mismatch "
            f"expected={expected.get('selected_candidate')} actual={actual.get('selected_candidate')}"
        )

    expected_relax = expected.get("applied_relaxations", [])
    actual_relax = actual.get("applied_relaxations", [])
    if expected_relax != actual_relax:
        return False, f"applied_relaxations mismatch expected={expected_relax} actual={actual_relax}"

    return True, case.vector_id


def main() -> int:
    repo_root = Path(__file__).resolve().parents[5]
    vector_dir = repo_root / "notes/workshop/design/compiler-mapping/stage-b-vectors"
    vectors = sorted(vector_dir.glob("*.cdx"))
    if not vectors:
        print("No Stage B vectors found (.cdx).")
        return 1

    failures = 0
    for path in vectors:
        ok, detail = run_vector(path, repo_root)
        if ok:
            print(f"[PASS] stage-b vector: {path.name}")
        else:
            failures += 1
            print(f"[FAIL] stage-b vector: {path.name}: {detail}")

    if failures:
        print(f"Stage B vectors failed with {failures} failing vector(s).")
        return 1

    print("All Stage B vectors passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
