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
# MS2-12: "fields preferredName and description are not the same".

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-12"
    TITLE = "preferredName and description are not identical"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            pn = el.preferred_name("en")
            de = el.description("en")
            if pn is not None and pn == de:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"'{el.name}': preferredName and description are identical",
                                         element=el.name, line=el.line_no))
        return findings
