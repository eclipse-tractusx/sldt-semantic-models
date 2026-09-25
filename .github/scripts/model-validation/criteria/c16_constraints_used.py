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
# Informational only (NOTE, never FAIL/WARN/SKIP/SUCCESS): whether constraints
# are *missing* for a given use case cannot be determined from the model
# file alone, so this never amounts to a verdict - it surfaces what's there
# plus an explicit "checked by reviewer" note, for the reviewer. NOTE
# rather than SUCCESS: SUCCESS is reserved for a genuine automated pass, and this
# criterion never actually confirms anything.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-16"
    TITLE = "Constraints used where applicable (not automatically verifiable)"
    CATEGORY = "Semantic Quality"
    # Harmless no-op today (check() below only ever returns NOTE) - see c10's
    # comment on POST_COMMENT for why this is still set.
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        constrained = [el.name for el in model.elements.values() if el.short_type.endswith("Constraint")]
        if constrained:
            result = f"{len(constrained)} constraint(s) defined: {constrained}"
        else:
            result = ("no samm-c constraints found - if the use case has known constraints "
                      "(ranges, patterns, lengths, ...), consider making them explicit")
        return [Finding(self.ID, self.TITLE, "NOTE", model.file,
                         f"{result} (checked by reviewer - not automatically verifiable)")]
