#!/usr/bin/env python3
"""Validate output CDX envelopes against Codex schema documents."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree as ET


class OutputSchemaValidationError(Exception):
    """Output envelope validation error."""


@dataclass(frozen=True)
class ConceptRule:
    required_traits: frozenset[str]
    allowed_traits: frozenset[str]
    required_children: frozenset[str]
    allowed_children: frozenset[str]
    forbids_content: bool


@dataclass(frozen=True)
class TraitRule:
    value_type: str | None
    allowed_values: frozenset[str] | None


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise OutputSchemaValidationError(f"Missing required attribute '{name}' at {path}")
    return value


def _normalize_enum_value(value: str) -> str:
    token = value.strip()
    if token.startswith("$"):
        token = token[1:]
    return token


def _parse_allowed_values(raw: str) -> frozenset[str]:
    payload = raw.strip()
    if payload.startswith("[") and payload.endswith("]"):
        payload = payload[1:-1]

    values: set[str] = set()
    for part in payload.split(","):
        token = part.strip()
        if not token:
            continue
        if token.startswith('"') and token.endswith('"') and len(token) >= 2:
            token = token[1:-1]
        values.add(_normalize_enum_value(token))
    return frozenset(values)


def _parse_schema(schema_path: Path) -> tuple[dict[str, ConceptRule], dict[str, TraitRule]]:
    try:
        root = ET.parse(schema_path).getroot()
    except ET.ParseError as exc:
        raise OutputSchemaValidationError(f"Malformed schema XML: {schema_path}") from exc

    if root.tag != "Schema":
        raise OutputSchemaValidationError(f"Root tag must be Schema in {schema_path}")

    concept_rules: dict[str, ConceptRule] = {}
    for concept in root.findall("ConceptDefinitions/ConceptDefinition"):
        concept_name = _require_attr(
            concept,
            "name",
            f"Schema/ConceptDefinitions/ConceptDefinition in {schema_path}",
        )
        required_traits: set[str] = set()
        allowed_traits: set[str] = set()
        required_children: set[str] = set()
        allowed_children: set[str] = set()
        forbids_content = concept.find("ContentRules/ForbidsContent") is not None

        for node in concept.findall("TraitRules/RequiresTrait"):
            trait_name = _require_attr(
                node,
                "name",
                f"Schema/ConceptDefinitions/ConceptDefinition[@name='{concept_name}']/TraitRules/RequiresTrait",
            )
            required_traits.add(trait_name)
            allowed_traits.add(trait_name)

        for node in concept.findall("TraitRules/AllowsTrait"):
            trait_name = _require_attr(
                node,
                "name",
                f"Schema/ConceptDefinitions/ConceptDefinition[@name='{concept_name}']/TraitRules/AllowsTrait",
            )
            allowed_traits.add(trait_name)

        for node in concept.findall("ChildRules/RequiresChildConcept"):
            child_name = _require_attr(
                node,
                "conceptSelector",
                f"Schema/ConceptDefinitions/ConceptDefinition[@name='{concept_name}']/ChildRules/RequiresChildConcept",
            )
            required_children.add(child_name)
            allowed_children.add(child_name)

        for node in concept.findall("ChildRules/AllowsChildConcept"):
            child_name = _require_attr(
                node,
                "conceptSelector",
                f"Schema/ConceptDefinitions/ConceptDefinition[@name='{concept_name}']/ChildRules/AllowsChildConcept",
            )
            allowed_children.add(child_name)

        concept_rules[concept_name] = ConceptRule(
            required_traits=frozenset(required_traits),
            allowed_traits=frozenset(allowed_traits),
            required_children=frozenset(required_children),
            allowed_children=frozenset(allowed_children),
            forbids_content=forbids_content,
        )

    if not concept_rules:
        raise OutputSchemaValidationError(f"Schema has no ConceptDefinition entries: {schema_path}")

    trait_rules: dict[str, TraitRule] = {}
    for trait in root.findall("TraitDefinitions/TraitDefinition"):
        trait_name = _require_attr(
            trait,
            "name",
            f"Schema/TraitDefinitions/TraitDefinition in {schema_path}",
        )
        value_type = trait.get("defaultValueType")
        allowed_values_node = trait.find("AllowedValues/ValueIsOneOf")
        allowed_values = None
        if allowed_values_node is not None:
            raw_values = _require_attr(
                allowed_values_node,
                "values",
                f"Schema/TraitDefinitions/TraitDefinition[@name='{trait_name}']/AllowedValues/ValueIsOneOf",
            )
            allowed_values = _parse_allowed_values(raw_values)

        trait_rules[trait_name] = TraitRule(
            value_type=value_type,
            allowed_values=allowed_values,
        )

    return concept_rules, trait_rules


def _validate_trait_type(trait_name: str, trait_value: str, trait_rule: TraitRule, path: str) -> None:
    value_type = trait_rule.value_type
    if value_type is None:
        return

    if trait_value == "":
        raise OutputSchemaValidationError(f"Trait '{trait_name}' at {path} MUST NOT be empty")

    if value_type == "$Text":
        pass
    elif value_type == "$IriReference":
        if ":" not in trait_value or any(ch.isspace() for ch in trait_value):
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be a non-whitespace IRI reference"
            )
    elif value_type == "$Boolean":
        if trait_value not in {"true", "false"}:
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be true or false"
            )
    elif value_type == "$Integer":
        try:
            decimal = Decimal(trait_value)
        except InvalidOperation as exc:
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be an integer"
            ) from exc
        if decimal != decimal.to_integral_value():
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be an integer"
            )
    elif value_type == "$Number":
        try:
            Decimal(trait_value)
        except InvalidOperation as exc:
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be numeric"
            ) from exc
    elif value_type == "$EnumeratedToken":
        normalized = _normalize_enum_value(trait_value)
        if normalized == "":
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} MUST be a non-empty token"
            )
    # Other Codex value types are not currently required for output-envelope validation.

    if trait_rule.allowed_values is not None:
        normalized = _normalize_enum_value(trait_value)
        if normalized not in trait_rule.allowed_values:
            allowed_values = ", ".join(sorted(trait_rule.allowed_values))
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} has invalid value '{trait_value}'. "
                f"Allowed values: {allowed_values}"
            )


def _validate_node(
    node: ET.Element,
    path: str,
    concept_rules: dict[str, ConceptRule],
    trait_rules: dict[str, TraitRule],
) -> None:
    concept = node.tag
    if concept not in concept_rules:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} is not defined in schema")

    concept_rule = concept_rules[concept]
    attrs = set(node.attrib.keys())
    missing_traits = sorted(concept_rule.required_traits - attrs)
    if missing_traits:
        raise OutputSchemaValidationError(
            f"Concept '{concept}' at {path} is missing required trait(s): {', '.join(missing_traits)}"
        )

    if concept_rule.allowed_traits:
        unknown_attrs = sorted(attrs - concept_rule.allowed_traits)
        if unknown_attrs:
            raise OutputSchemaValidationError(
                f"Concept '{concept}' at {path} has unknown trait(s): {', '.join(unknown_attrs)}"
            )
    elif attrs:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} MUST NOT define traits")

    for trait_name in sorted(attrs):
        if trait_name not in trait_rules:
            raise OutputSchemaValidationError(
                f"Trait '{trait_name}' at {path} is not defined in schema TraitDefinitions"
            )
        _validate_trait_type(
            trait_name,
            node.attrib[trait_name],
            trait_rules[trait_name],
            f"{path}/@{trait_name}",
        )

    if concept_rule.forbids_content and (node.text or "").strip():
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} forbids content text")

    child_names = [child.tag for child in node]
    if concept_rule.allowed_children:
        for child in node:
            if child.tag not in concept_rule.allowed_children:
                raise OutputSchemaValidationError(
                    f"Concept '{concept}' at {path} has disallowed child concept '{child.tag}'"
                )
    elif child_names:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} MUST NOT define child concepts")

    for required_child in sorted(concept_rule.required_children):
        if required_child not in child_names:
            raise OutputSchemaValidationError(
                f"Concept '{concept}' at {path} is missing required child concept '{required_child}'"
            )

    for index, child in enumerate(node):
        child_path = f"{path}/{child.tag}[{index}]"
        _validate_node(child, child_path, concept_rules, trait_rules)


def validate_root_element_against_schema(root: ET.Element, schema_path: Path) -> None:
    concept_rules, trait_rules = _parse_schema(schema_path)
    _validate_node(root, root.tag, concept_rules, trait_rules)


def parse_rendered_cdx(rendered_cdx: str) -> ET.Element:
    try:
        return ET.fromstring(rendered_cdx)
    except ET.ParseError as exc:
        raise OutputSchemaValidationError("Rendered CDX is not well-formed XML") from exc


def load_cdx_root(path: Path) -> ET.Element:
    try:
        rendered = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OutputSchemaValidationError(f"Unable to read rendered CDX file: {path}") from exc
    return parse_rendered_cdx(rendered)


def validate_rendered_cdx_against_schema(rendered_cdx: str, schema_path: Path) -> None:
    root = parse_rendered_cdx(rendered_cdx)
    validate_root_element_against_schema(root, schema_path)
