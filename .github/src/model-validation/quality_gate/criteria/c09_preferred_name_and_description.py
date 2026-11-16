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

# MS2-09: "all model elements at least contain the fields 'preferred name'
# and 'description' in English language. The description must be
# comprehensible. [...] style should be consistent over the whole model"
#
# Checks that every model element has samm:preferredName and
# samm:description in English. Comprehensibility and style are left to the
# reviewer.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-09"
    # Every model element must have samm:preferredName and samm:description in English.
    TITLE = "preferredName and description present (English)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements:
            if el.text("preferredName") is None:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"'{el.label}' is missing samm:preferredName ... @en",
                                         element=el.label, line=el.line_no))
            if el.text("description") is None:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"'{el.label}' is missing samm:description ... @en",
                                         element=el.label, line=el.line_no))
        return findings
