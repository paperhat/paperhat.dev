#!/usr/bin/env python3
"""Compile adaptive authoring fixture CDX into a normalized evaluation request map."""

from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

GD = "https://paperhat.dev/ns/gd#"

GD_VIEWPORT_WIDTH = f"{GD}ViewportWidthPx"
GD_VIEWPORT_HEIGHT = f"{GD}ViewportHeightPx"
GD_VIEWPORT_ASPECT = f"{GD}ViewportAspectRatio"
GD_VIEWPORT_ORIENTATION = f"{GD}ViewportOrientation"
GD_DEVICE_CLASS = f"{GD}DeviceClass"
GD_REDUCED_MOTION = f"{GD}ReducedMotionPreference"

OBJECTIVE_PRIORITY_WEIGHTS = {
    "must": Decimal("1.0"),
    "prefer": Decimal("0.7"),
    "neutral": Decimal("0.4"),
}

SOFT_TERM_WEIGHTS = {
    "critical": Decimal("1.0"),
    "high": Decimal("0.75"),
    "medium": Decimal("0.5"),
    "low": Decimal("0.25"),
}

OVERRIDE_PRIORITY_RANKS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


class CompileError(Exception):
    """Compilation failed under fail-closed semantics."""


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise CompileError(f"Missing required attribute '{name}' at {path}")
    return value


def _find_required(root: ET.Element, tag: str) -> ET.Element:
    node = root.find(tag)
    if node is None:
        raise CompileError(f"Missing required concept: {tag}")
    return node


def _attrs_dict(element: ET.Element) -> dict[str, str]:
    return {k: v for k, v in element.attrib.items()}


def load_cdx_fixture(path: Path) -> dict[str, Any]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:  # noqa: PERF203
        raise CompileError(f"Invalid CDX fixture syntax in {path}: {exc}") from exc

    if root.tag != "AdaptiveFixture":
        raise CompileError(f"Root tag must be AdaptiveFixture in {path}")

    context = _attrs_dict(_find_required(root, "AdaptiveContextProfile"))
    objective = _attrs_dict(_find_required(root, "AdaptiveObjectiveProfile"))

    optimization_node = _find_required(root, "AdaptiveOptimizationProfile")
    optimization = _attrs_dict(optimization_node)
    optimization["hardConstraints"] = [
        _attrs_dict(node)
        for node in optimization_node.findall("OptimizationHardConstraint")
    ]
    optimization["softTerms"] = [
        _attrs_dict(node)
        for node in optimization_node.findall("OptimizationSoftTerm")
    ]
    optimization["relaxationRules"] = [
        _attrs_dict(node)
        for node in optimization_node.findall("RelaxationRule")
    ]

    override_node = root.find("AdaptiveOverrideSet")
    override_set: dict[str, Any] | None = None
    if override_node is not None:
        override_set = _attrs_dict(override_node)
        override_set["constraints"] = [
            _attrs_dict(node)
            for node in override_node.findall("OverrideConstraint")
        ]

    intent = _attrs_dict(_find_required(root, "AdaptiveIntent"))

    return {
        "adaptiveContextProfile": context,
        "adaptiveObjectiveProfile": objective,
        "adaptiveOptimizationProfile": optimization,
        "adaptiveOverrideSet": override_set,
        "adaptiveIntent": intent,
    }


def load_fixture(path: Path) -> dict[str, Any]:
    if path.suffix != ".cdx":
        raise CompileError(f"Unsupported fixture format (required .cdx): {path}")
    return load_cdx_fixture(path)


def require_dict(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise CompileError(f"Missing object: {key}")
    return value


def require_field(obj: dict[str, Any], field: str) -> Any:
    if field not in obj or obj[field] is None:
        raise CompileError(f"Missing required field: {field}")
    return obj[field]


def normalize_token(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.startswith("$") or len(value) < 2:
        raise CompileError(f"Expected token ('$...') for field: {field}")
    return value[1:]


def normalize_optional_token(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return normalize_token(value, field)


def require_iri(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise CompileError(f"Expected non-empty IRI string for field: {field}")
    return value


def require_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise CompileError(f"Expected integer for field: {field}")
    try:
        number = int(value)
    except Exception as exc:  # noqa: BLE001
        raise CompileError(f"Invalid integer for field: {field}") from exc
    if Decimal(str(value)) != Decimal(number):
        raise CompileError(f"Non-integer numeric value for field: {field}")
    return number


def require_decimal(value: Any, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise CompileError(f"Expected number for field: {field}")
    try:
        return Decimal(str(value))
    except Exception as exc:  # noqa: BLE001
        raise CompileError(f"Invalid number for field: {field}") from exc


def quantize_ratio(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN), "f")


def context_entry(kind: str, value: Any) -> dict[str, Any]:
    return {"type": kind, "value": value}


def compile_stage_a_context(profile: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    stage_a_context: dict[str, Any] = {}
    context_ext: dict[str, Any] = {}

    width_raw = profile.get("viewportWidthPx")
    height_raw = profile.get("viewportHeightPx")
    width = require_int(width_raw, "viewportWidthPx") if width_raw is not None else None
    height = require_int(height_raw, "viewportHeightPx") if height_raw is not None else None

    if width is not None:
        stage_a_context[GD_VIEWPORT_WIDTH] = context_entry("integer", width)
    if height is not None:
        stage_a_context[GD_VIEWPORT_HEIGHT] = context_entry("integer", height)

    if width is not None and height is not None:
        if height <= 0:
            raise CompileError("viewportHeightPx must be > 0 for aspect ratio derivation.")
        ratio = Decimal(width) / Decimal(height)
        stage_a_context[GD_VIEWPORT_ASPECT] = context_entry("decimal", quantize_ratio(ratio))

        orientation = "square"
        if width > height:
            orientation = "landscape"
        elif height > width:
            orientation = "portrait"
        stage_a_context[GD_VIEWPORT_ORIENTATION] = context_entry("string", orientation)

    if profile.get("deviceClass") is not None:
        stage_a_context[GD_DEVICE_CLASS] = context_entry(
            "string",
            normalize_token(profile["deviceClass"], "deviceClass"),
        )

    motion = profile.get("motionPreference")
    if motion is not None:
        motion_token = normalize_token(motion, "motionPreference")
        if motion_token == "reduce":
            reduced = True
        elif motion_token == "noPreference":
            reduced = False
        else:
            raise CompileError("motionPreference must be $reduce or $noPreference.")
        stage_a_context[GD_REDUCED_MOTION] = context_entry("boolean", reduced)

    for field in (
        "zoomLevel",
        "inputModality",
        "contrastPreference",
        "colorSchemePreference",
        "language",
        "region",
        "scriptDirection",
        "networkClass",
        "interactionMode",
    ):
        value = profile.get(field)
        if value is None:
            continue
        if field == "zoomLevel":
            context_ext[field] = str(require_decimal(value, field))
            continue
        context_ext[field] = normalize_token(value, field)

    return stage_a_context, context_ext


def compile_objective_profile(profile: dict[str, Any]) -> dict[str, Any]:
    compiled: dict[str, Any] = {
        "profile_id": require_iri(require_field(profile, "profileId"), "objectiveProfile.profileId"),
        "primary_objective": normalize_token(
            require_field(profile, "primaryObjective"),
            "objectiveProfile.primaryObjective",
        ),
    }

    for token_field in (
        "secondaryObjective",
        "densityGoal",
        "motionGoal",
        "brandExpressionGoal",
        "localizationGoal",
        "precedenceProfile",
    ):
        value = profile.get(token_field)
        if value is not None:
            compiled[token_field] = normalize_token(value, f"objectiveProfile.{token_field}")

    priority_weights: dict[str, str] = {}
    for priority_field in ("readabilityPriority", "accessibilityPriority", "performancePriority"):
        value = profile.get(priority_field)
        if value is None:
            continue
        token = normalize_token(value, f"objectiveProfile.{priority_field}")
        if token not in OBJECTIVE_PRIORITY_WEIGHTS:
            raise CompileError(f"Unknown objective priority token: {token}")
        priority_weights[priority_field] = format(OBJECTIVE_PRIORITY_WEIGHTS[token], "f")

    compiled["priority_weights"] = priority_weights
    return compiled


def _string_or_none(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise CompileError(f"Expected string for field: {field}")
    return value


def compile_optimization_profile(profile: dict[str, Any]) -> dict[str, Any]:
    compiled: dict[str, Any] = {
        "profile_id": require_iri(require_field(profile, "profileId"), "optimizationProfile.profileId"),
    }

    for token_field in ("solverMode", "quantizationMode", "reflowMode", "relaxationStrategy"):
        value = profile.get(token_field)
        if value is not None:
            compiled[token_field] = normalize_token(value, f"optimizationProfile.{token_field}")

    if profile.get("satisficeThreshold") is not None:
        compiled["satisficeThreshold"] = str(
            require_decimal(profile["satisficeThreshold"], "optimizationProfile.satisficeThreshold")
        )

    hard_constraints = []
    for row in profile.get("hardConstraints", []):
        if not isinstance(row, dict):
            raise CompileError("hardConstraints entries must be objects.")
        hard_constraints.append(
            {
                "constraint_key": normalize_token(require_field(row, "constraintKey"), "hardConstraints.constraintKey"),
                "constraint_scope": normalize_optional_token(row.get("constraintScope"), "hardConstraints.constraintScope"),
                "target_ref": _string_or_none(row.get("targetRef"), "hardConstraints.targetRef"),
                "constraint_value": _string_or_none(row.get("constraintValue"), "hardConstraints.constraintValue"),
            }
        )

    hard_constraints.sort(
        key=lambda x: (
            x["constraint_key"] or "",
            x["constraint_scope"] or "",
            x["target_ref"] or "",
            x["constraint_value"] or "",
        )
    )
    compiled["hard_constraints"] = hard_constraints

    soft_terms = []
    for row in profile.get("softTerms", []):
        if not isinstance(row, dict):
            raise CompileError("softTerms entries must be objects.")
        weight_class = normalize_optional_token(row.get("weightClass"), "softTerms.weightClass")
        weight = None
        if weight_class is not None:
            if weight_class not in SOFT_TERM_WEIGHTS:
                raise CompileError(f"Unknown soft term weight class: {weight_class}")
            weight = format(SOFT_TERM_WEIGHTS[weight_class], "f")

        minimum_satisfaction = row.get("minimumSatisfaction")
        min_value = None
        if minimum_satisfaction is not None:
            min_value = str(require_decimal(minimum_satisfaction, "softTerms.minimumSatisfaction"))

        soft_terms.append(
            {
                "term_key": normalize_token(require_field(row, "termKey"), "softTerms.termKey"),
                "weight_class": weight_class,
                "weight": weight,
                "term_scope": normalize_optional_token(row.get("termScope"), "softTerms.termScope"),
                "target_ref": _string_or_none(row.get("targetRef"), "softTerms.targetRef"),
                "minimum_satisfaction": min_value,
            }
        )

    soft_terms.sort(
        key=lambda x: (
            x["term_key"] or "",
            x["term_scope"] or "",
            x["target_ref"] or "",
            x["weight_class"] or "",
        )
    )
    compiled["soft_terms"] = soft_terms

    relaxation_rules = []
    for row in profile.get("relaxationRules", []):
        if not isinstance(row, dict):
            raise CompileError("relaxationRules entries must be objects.")
        relax_order = require_int(require_field(row, "relaxOrder"), "relaxationRules.relaxOrder")
        relax_weight_class = normalize_token(
            require_field(row, "relaxWeightClass"),
            "relaxationRules.relaxWeightClass",
        )
        if relax_weight_class not in {"low", "medium", "high"}:
            raise CompileError(f"Unknown relaxWeightClass: {relax_weight_class}")
        relaxation_rules.append(
            {
                "relax_order": relax_order,
                "relax_weight_class": relax_weight_class,
                "relaxation_action": normalize_optional_token(
                    row.get("relaxationAction"),
                    "relaxationRules.relaxationAction",
                ),
            }
        )

    relaxation_rules.sort(
        key=lambda x: (x["relax_order"], x["relax_weight_class"], x["relaxation_action"] or "")
    )
    compiled["relaxation_rules"] = relaxation_rules
    return compiled


def compile_override_set(override_set: dict[str, Any] | None) -> dict[str, Any] | None:
    if override_set is None:
        return None

    compiled: dict[str, Any] = {
        "override_set_id": require_iri(
            require_field(override_set, "overrideSetId"),
            "overrideSet.overrideSetId",
        ),
        "override_mode": normalize_optional_token(
            override_set.get("overrideMode"),
            "overrideSet.overrideMode",
        ),
    }

    constraints = []
    for row in override_set.get("constraints", []):
        if not isinstance(row, dict):
            raise CompileError("override constraints entries must be objects.")
        override_priority = normalize_optional_token(row.get("overridePriority"), "override.constraints.overridePriority")
        priority_rank = None
        if override_priority is not None:
            if override_priority not in OVERRIDE_PRIORITY_RANKS:
                raise CompileError(f"Unknown override priority token: {override_priority}")
            priority_rank = OVERRIDE_PRIORITY_RANKS[override_priority]

        constraints.append(
            {
                "override_kind": normalize_token(require_field(row, "overrideKind"), "override.constraints.overrideKind"),
                "target_ref": require_iri(require_field(row, "targetRef"), "override.constraints.targetRef"),
                "target_property": _string_or_none(row.get("targetProperty"), "override.constraints.targetProperty"),
                "override_value": _string_or_none(row.get("overrideValue"), "override.constraints.overrideValue"),
                "override_priority": override_priority,
                "priority_rank": priority_rank,
                "expires_at": _string_or_none(row.get("expiresAt"), "override.constraints.expiresAt"),
            }
        )

    constraints.sort(
        key=lambda x: (
            -(x["priority_rank"] or 0),
            x["target_ref"],
            x["override_kind"],
        )
    )
    compiled["constraints"] = constraints
    return compiled


def compile_fixture(data: dict[str, Any]) -> dict[str, Any]:
    intent = require_dict(data, "adaptiveIntent")
    context = require_dict(data, "adaptiveContextProfile")
    objective = require_dict(data, "adaptiveObjectiveProfile")
    optimization = require_dict(data, "adaptiveOptimizationProfile")
    override_set = data.get("adaptiveOverrideSet")
    if override_set is not None and not isinstance(override_set, dict):
        raise CompileError("adaptiveOverrideSet must be an object if provided.")

    intent_id = require_iri(require_field(intent, "intentId"), "adaptiveIntent.intentId")
    composition_iri = require_iri(require_field(intent, "compositionRef"), "adaptiveIntent.compositionRef")
    context_profile_ref = require_iri(
        require_field(intent, "contextProfileRef"),
        "adaptiveIntent.contextProfileRef",
    )
    objective_profile_ref = require_iri(
        require_field(intent, "objectiveProfileRef"),
        "adaptiveIntent.objectiveProfileRef",
    )
    optimization_profile_ref = require_iri(
        require_field(intent, "optimizationProfileRef"),
        "adaptiveIntent.optimizationProfileRef",
    )
    policy_set_ref = require_iri(require_field(intent, "policySetRef"), "adaptiveIntent.policySetRef")
    target_foundry = normalize_token(require_field(intent, "targetFoundry"), "adaptiveIntent.targetFoundry")
    view_iri = intent.get("viewRef")
    if view_iri is not None:
        view_iri = require_iri(view_iri, "adaptiveIntent.viewRef")

    stage_a_context, context_ext = compile_stage_a_context(context)
    objective_compiled = compile_objective_profile(objective)
    optimization_compiled = compile_optimization_profile(optimization)
    override_compiled = compile_override_set(override_set)

    if context_profile_ref != require_iri(require_field(context, "profileId"), "adaptiveContextProfile.profileId"):
        raise CompileError("adaptiveIntent.contextProfileRef does not match adaptiveContextProfile.profileId.")
    if objective_profile_ref != objective_compiled["profile_id"]:
        raise CompileError("adaptiveIntent.objectiveProfileRef does not match adaptiveObjectiveProfile.profileId.")
    if optimization_profile_ref != optimization_compiled["profile_id"]:
        raise CompileError("adaptiveIntent.optimizationProfileRef does not match adaptiveOptimizationProfile.profileId.")
    if override_compiled is not None:
        override_ref = intent.get("overrideSetRef")
        if override_ref is None:
            raise CompileError("adaptiveIntent.overrideSetRef is required when adaptiveOverrideSet is provided.")
        if require_iri(override_ref, "adaptiveIntent.overrideSetRef") != override_compiled["override_set_id"]:
            raise CompileError("adaptiveIntent.overrideSetRef does not match adaptiveOverrideSet.overrideSetId.")

    return {
        "intent_id": intent_id,
        "target_foundry": target_foundry,
        "policy_set_ref": policy_set_ref,
        "stage_a": {
            "composition_iri": composition_iri,
            "view_iri": view_iri,
            "context": stage_a_context,
        },
        "stage_b": {
            "context_ext": context_ext,
            "objective_profile": objective_compiled,
            "optimization_profile": optimization_compiled,
            "override_set": override_compiled,
        },
    }


def _set_attrs(element: ET.Element, attrs: list[tuple[str, Any]]) -> None:
    for key, value in attrs:
        if value is None:
            continue
        element.set(key, str(value))


def render_compiled_cdx(compiled: dict[str, Any]) -> str:
    root = ET.Element("CompiledAdaptiveRequest")
    _set_attrs(
        root,
        [
            ("intentId", compiled["intent_id"]),
            ("targetFoundry", compiled["target_foundry"]),
            ("policySetRef", compiled["policy_set_ref"]),
        ],
    )

    stage_a = ET.SubElement(root, "StageA")
    _set_attrs(
        stage_a,
        [
            ("compositionIri", compiled["stage_a"]["composition_iri"]),
            ("viewIri", compiled["stage_a"]["view_iri"]),
        ],
    )

    for key in sorted(compiled["stage_a"]["context"].keys()):
        item = compiled["stage_a"]["context"][key]
        entry = ET.SubElement(stage_a, "ContextEntry")
        _set_attrs(
            entry,
            [
                ("key", key),
                ("type", item["type"]),
                ("value", str(item["value"]).lower() if isinstance(item["value"], bool) else item["value"]),
            ],
        )

    stage_b = ET.SubElement(root, "StageB")

    for key in sorted(compiled["stage_b"]["context_ext"].keys()):
        entry = ET.SubElement(stage_b, "ContextExtEntry")
        _set_attrs(entry, [("key", key), ("value", compiled["stage_b"]["context_ext"][key])])

    objective = compiled["stage_b"]["objective_profile"]
    objective_node = ET.SubElement(stage_b, "ObjectiveProfile")
    _set_attrs(
        objective_node,
        [
            ("profileId", objective["profile_id"]),
            ("primaryObjective", objective["primary_objective"]),
            ("secondaryObjective", objective.get("secondaryObjective")),
            ("densityGoal", objective.get("densityGoal")),
            ("motionGoal", objective.get("motionGoal")),
            ("brandExpressionGoal", objective.get("brandExpressionGoal")),
            ("localizationGoal", objective.get("localizationGoal")),
            ("precedenceProfile", objective.get("precedenceProfile")),
        ],
    )
    for field in sorted(objective.get("priority_weights", {}).keys()):
        entry = ET.SubElement(objective_node, "PriorityWeight")
        _set_attrs(entry, [("field", field), ("value", objective["priority_weights"][field])])

    optimization = compiled["stage_b"]["optimization_profile"]
    optimization_node = ET.SubElement(stage_b, "OptimizationProfile")
    _set_attrs(
        optimization_node,
        [
            ("profileId", optimization["profile_id"]),
            ("solverMode", optimization.get("solverMode")),
            ("quantizationMode", optimization.get("quantizationMode")),
            ("reflowMode", optimization.get("reflowMode")),
            ("satisficeThreshold", optimization.get("satisficeThreshold")),
            ("relaxationStrategy", optimization.get("relaxationStrategy")),
        ],
    )

    for row in optimization.get("hard_constraints", []):
        node = ET.SubElement(optimization_node, "HardConstraint")
        _set_attrs(
            node,
            [
                ("constraintKey", row.get("constraint_key")),
                ("constraintScope", row.get("constraint_scope")),
                ("targetRef", row.get("target_ref")),
                ("constraintValue", row.get("constraint_value")),
            ],
        )

    for row in optimization.get("soft_terms", []):
        node = ET.SubElement(optimization_node, "SoftTerm")
        _set_attrs(
            node,
            [
                ("termKey", row.get("term_key")),
                ("weightClass", row.get("weight_class")),
                ("weight", row.get("weight")),
                ("termScope", row.get("term_scope")),
                ("targetRef", row.get("target_ref")),
                ("minimumSatisfaction", row.get("minimum_satisfaction")),
            ],
        )

    for row in optimization.get("relaxation_rules", []):
        node = ET.SubElement(optimization_node, "RelaxationRule")
        _set_attrs(
            node,
            [
                ("relaxOrder", row.get("relax_order")),
                ("relaxWeightClass", row.get("relax_weight_class")),
                ("relaxationAction", row.get("relaxation_action")),
            ],
        )

    override = compiled["stage_b"].get("override_set")
    if override is not None:
        override_node = ET.SubElement(stage_b, "OverrideSet")
        _set_attrs(
            override_node,
            [
                ("overrideSetId", override.get("override_set_id")),
                ("overrideMode", override.get("override_mode")),
            ],
        )
        for row in override.get("constraints", []):
            node = ET.SubElement(override_node, "OverrideConstraint")
            _set_attrs(
                node,
                [
                    ("overrideKind", row.get("override_kind")),
                    ("targetRef", row.get("target_ref")),
                    ("targetProperty", row.get("target_property")),
                    ("overrideValue", row.get("override_value")),
                    ("overridePriority", row.get("override_priority")),
                    ("priorityRank", row.get("priority_rank")),
                    ("expiresAt", row.get("expires_at")),
                ],
            )

    ET.indent(root, space="\t")
    rendered = ET.tostring(root, encoding="unicode")
    return rendered + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input fixture (.cdx)")
    parser.add_argument("-o", "--output", type=Path, help="Output path. Defaults to stdout.")
    args = parser.parse_args()

    compiled = compile_fixture(load_fixture(args.input))
    rendered = render_compiled_cdx(compiled)

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CompileError as exc:
        raise SystemExit(f"[compile-error] {exc}")
