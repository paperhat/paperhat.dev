#!/usr/bin/env python3
"""Validate output CDX envelopes against Codex schema documents."""

from __future__ import annotations

from dataclasses import dataclass
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


def _require_attr(element: ET.Element, name: str, path: str) -> str:
    value = element.get(name)
    if value is None or value == "":
        raise OutputSchemaValidationError(f"Missing required attribute '{name}' at {path}")
    return value


def _parse_schema(schema_path: Path) -> dict[str, ConceptRule]:
    try:
        root = ET.parse(schema_path).getroot()
    except ET.ParseError as exc:
        raise OutputSchemaValidationError(f"Malformed schema XML: {schema_path}") from exc

    if root.tag != "Schema":
        raise OutputSchemaValidationError(f"Root tag must be Schema in {schema_path}")

    rules: dict[str, ConceptRule] = {}
    for concept in root.findall("ConceptDefinitions/ConceptDefinition"):
        concept_name = _require_attr(concept, "name", f"Schema/ConceptDefinitions/ConceptDefinition in {schema_path}")
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

        rules[concept_name] = ConceptRule(
            required_traits=frozenset(required_traits),
            allowed_traits=frozenset(allowed_traits),
            required_children=frozenset(required_children),
            allowed_children=frozenset(allowed_children),
            forbids_content=forbids_content,
        )

    if not rules:
        raise OutputSchemaValidationError(f"Schema has no ConceptDefinition entries: {schema_path}")
    return rules


def _validate_node(node: ET.Element, path: str, rules: dict[str, ConceptRule]) -> None:
    concept = node.tag
    if concept not in rules:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} is not defined in schema")

    rule = rules[concept]
    attrs = set(node.attrib.keys())
    missing_traits = sorted(rule.required_traits - attrs)
    if missing_traits:
        raise OutputSchemaValidationError(
            f"Concept '{concept}' at {path} is missing required trait(s): {', '.join(missing_traits)}"
        )

    if rule.allowed_traits:
        unknown_attrs = sorted(attrs - rule.allowed_traits)
        if unknown_attrs:
            raise OutputSchemaValidationError(
                f"Concept '{concept}' at {path} has unknown trait(s): {', '.join(unknown_attrs)}"
            )
    elif attrs:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} MUST NOT define traits")

    if rule.forbids_content and (node.text or "").strip():
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} forbids content text")

    child_names = [child.tag for child in node]
    if rule.allowed_children:
        for child in node:
            if child.tag not in rule.allowed_children:
                raise OutputSchemaValidationError(
                    f"Concept '{concept}' at {path} has disallowed child concept '{child.tag}'"
                )
    elif child_names:
        raise OutputSchemaValidationError(f"Concept '{concept}' at {path} MUST NOT define child concepts")

    for required_child in sorted(rule.required_children):
        if required_child not in child_names:
            raise OutputSchemaValidationError(
                f"Concept '{concept}' at {path} is missing required child concept '{required_child}'"
            )

    for index, child in enumerate(node):
        child_path = f"{path}/{child.tag}[{index}]"
        _validate_node(child, child_path, rules)


def validate_root_element_against_schema(root: ET.Element, schema_path: Path) -> None:
    rules = _parse_schema(schema_path)
    _validate_node(root, root.tag, rules)


def validate_rendered_cdx_against_schema(rendered_cdx: str, schema_path: Path) -> None:
    try:
        root = ET.fromstring(rendered_cdx)
    except ET.ParseError as exc:
        raise OutputSchemaValidationError("Rendered CDX is not well-formed XML") from exc
    validate_root_element_against_schema(root, schema_path)
