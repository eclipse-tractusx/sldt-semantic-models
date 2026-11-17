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

# MS2-16: "use constraints to make known constraints from the use case
# explicit in the aspect model".
#
# Lists the constraints defined in the model for the reviewer (NOTE).

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-16"
    TITLE = "Constraints used where applicable (not automatically verifiable)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        constrained = [el.label for el in model.elements if el.type and el.type.endswith("Constraint")]
        if constrained:
            result = f"{len(constrained)} constraint(s) defined: {constrained}"
        else:
            result = ("no samm-c constraints found - if the use case has known constraints "
                      "(ranges, patterns, lengths, ...), consider making them explicit")
        return [Finding(self.ID, self.TITLE, "NOTE", model.file,
                         f"{result} (checked by reviewer - not automatically verifiable)")]
