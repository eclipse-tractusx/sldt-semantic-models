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
# MS2-18: "all properties with an simple type have an example value".
#
# Only resolvable within a single file: if a Property's Characteristic (and
# its samm:dataType) is defined in an imported model rather than locally,
# we can't tell whether it's a simple (xsd:) type, so it's skipped rather
# than guessed.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-18"
    TITLE = "Properties with simple (xsd) type have an example value"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            if el.short_type != "Property" or not el.characteristic:
                continue
            characteristic = model.elements.get(el.characteristic)
            if not characteristic or not characteristic.data_type:
                continue  # characteristic defined elsewhere / not resolvable locally
            if not characteristic.data_type.startswith("xsd:"):
                continue  # complex (Entity) type, not a "simple type"
            if not el.has_example_value:
                findings.append(Finding(
                    self.ID, self.TITLE, "FAIL", model.file,
                    f"property '{el.name}' -> characteristic '{characteristic.name}' has simple type "
                    f"'{characteristic.data_type}' but no samm:exampleValue", element=el.name, line=el.line_no,
                ))
        return findings
