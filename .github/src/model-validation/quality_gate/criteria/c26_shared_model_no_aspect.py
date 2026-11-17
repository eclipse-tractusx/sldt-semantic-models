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

# MS2-26: "shared models (io.catenax.shared.*) must not define a samm:Aspect".
#
# Shared models only provide reusable elements for import; an Aspect is
# never used by importing models.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base


class Criterion(base.Criterion):
    ID = "MS2-26"
    TITLE = "Shared model defines no samm:Aspect"
    CATEGORY = "Formal Requirements"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        if not model.is_shared:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file, "not a shared model")]

        aspect = model.aspect
        if aspect is None:
            return []
        return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                         f"shared model must not define a samm:Aspect, found '{aspect.name}'",
                         element=aspect.label, line=aspect.line_no)]
