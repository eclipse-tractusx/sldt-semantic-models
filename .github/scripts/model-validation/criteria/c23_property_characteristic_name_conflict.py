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
# MS2-23: "Property and the referenced Characteristic should not have the
# same name".

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-23"
    # A property and its referenced Characteristic must not share the same name.
    TITLE = "Property and its Characteristic have different names"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            if el.short_type == "Property" and el.characteristic and el.characteristic == el.name:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"property '{el.name}' and its characteristic share the same name",
                                         element=el.name, line=el.line_no))
        return findings
