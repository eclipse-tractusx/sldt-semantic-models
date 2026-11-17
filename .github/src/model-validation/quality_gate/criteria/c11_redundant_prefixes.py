#######################################################################
# Copyright (c) 2026 Catena-X Automotive Network e.V.
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This work is made available under the terms of the
# Creative Commons Attribution 4.0 International (CC-BY-4.0) license,
# which is available at
# https://creativecommons.org/licenses/by/4.0/legalcode.
#
# SPDX-License-Identifier: CC-BY-4.0
#######################################################################

# MS2-11: "avoid redundant prefixes in property names (consider adding
# properties to an enclosing Entity or even adapt the namespace of the
# model elements, e.g., instead of having two properties `DismantlerId`
# and `DismantlerName` use an Entity `Dismantler` with the properties
# `name` and `id` [...])"
#
# Flags sibling properties of the same Aspect/Entity whose names (payloadName
# if set, otherwise identifier) share a leading camel-case word (WARN).

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import Element, TTLModel
from ..report import Finding
from . import base

def _split_camel(name: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", name)]

class Criterion(base.Criterion):
    ID = "MS2-11"
    TITLE = "Avoid redundant prefixes in property names (heuristic, needs human review)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements:
            if not (el.is_a("Aspect") or el.is_a("Entity")):
                continue
            # samm:properties ( :a [ samm:property :b ; samm:optional true ] ext:c )
            properties = [p.get("property") if isinstance(p, Element) else p for p in el.get("properties") or []]
            if len(properties) < 2:
                continue
            first_words: dict[str, list[str]] = {}
            for prop_name in properties:
                prop = model.element(prop_name)
                payload_name = prop.get("payloadName") if prop else None
                effective_name = payload_name.text if payload_name else prop_name.rsplit(":", 1)[-1]
                words = _split_camel(effective_name)
                if not words:
                    continue
                first_words.setdefault(words[0], []).append(prop_name)
            for word, props in first_words.items():
                if len(props) >= 2:
                    findings.append(Finding(
                        self.ID, self.TITLE, "WARN", model.file,
                        f"properties {props} of '{el.name}' all share the prefix '{word}' - "
                        f"consider an enclosing Entity instead (e.g. '{word}' with sub-properties)",
                        element=el.name, line=el.line_no,
                    ))
        return findings
