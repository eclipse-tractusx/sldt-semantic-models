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
# Heuristic only (WARN, not FAIL): flags sibling properties of the same
# Aspect/Entity that share a leading camel-case word, as a hint the
# reviewer should consider factoring out an Entity.
#
# Redundancy is judged on the name that actually ends up in the payload:
# a property's samm:payloadName (if set) overrides its SAMM identifier for
# this purpose, since a payloadName can already resolve the redundancy
# (e.g. SAMM identifiers `dismantlerId`/`dismantlerName` overridden to
# payload names `id`/`name`) even though the underlying model identifiers
# still share a prefix.

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
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
        for el in model.elements.values():
            if el.short_type not in ("Aspect", "Entity") or len(el.properties) < 2:
                continue
            first_words: dict[str, list[str]] = {}
            for prop_name in el.properties:
                prop = model.elements.get(prop_name)
                effective_name = prop.payload_name if prop and prop.payload_name else prop_name
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
