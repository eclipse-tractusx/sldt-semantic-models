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
# MS2-20: "payload names and property identifiers must not contain two
# consecutive underscores ('__') at any position".

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-20"
    # Identifiers and payloadName values must not contain two consecutive underscores.
    TITLE = "No double underscores in identifiers/payload names"
    CATEGORY = "Naming Conventions"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            if "__" in el.name:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"identifier '{el.name}' contains '__'", element=el.name, line=el.line_no))
            if el.payload_name and "__" in el.payload_name:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"payloadName '{el.payload_name}' contains '__'",
                                         element=el.name, line=el.line_no))
        return findings
