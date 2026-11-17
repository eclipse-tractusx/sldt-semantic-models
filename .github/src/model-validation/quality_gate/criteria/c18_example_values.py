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
# Checks that every property with a simple (xsd) data type has a
# samm:exampleValue. Properties whose characteristic is defined in an
# imported model are skipped.

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
        for el in model.elements:
            if not el.is_a("Property"):
                continue
            characteristic = model.resolve(el.get("characteristic"))
            if characteristic is None:
                continue  # characteristic defined elsewhere / not resolvable locally
            data_type = characteristic.get("dataType")
            if not isinstance(data_type, str) or not data_type.startswith("xsd:"):
                continue  # no dataType, or complex (Entity) type - not a "simple type"
            if el.get("exampleValue") is None:
                findings.append(Finding(
                    self.ID, self.TITLE, "FAIL", model.file,
                    f"property '{el.label}' -> characteristic '{characteristic.label}' has simple type "
                    f"'{data_type}' but no samm:exampleValue", element=el.label, line=el.line_no,
                ))
        return findings
