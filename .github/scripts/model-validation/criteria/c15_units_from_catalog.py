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
# MS2-15: "units are referenced from the SAMM unit catalog whenever
# possible".
#
# Never FAIL/WARN/SUCCESS: whether a matching catalog unit actually exists
# for a given quantity isn't something this script can know (it doesn't
# load the catalog itself), so nothing here is ever confirmable as a
# genuine automated pass - not even "every unit reference already uses the
# catalog prefix and no custom samm:Unit is defined", since that still
# doesn't confirm the *right* catalog unit was chosen. A flagged unit is
# SKIP (a fact to point the reviewer at, not evidence of a violation -
# keeps it from claiming a "likely violation" it can't substantiate); the
# "nothing to flag" case is NOTE (a fact for the reviewer, not a
# confirmation of anything - same reasoning as MS2-15/MS2-16).

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-15"
    TITLE = "Units reference the SAMM unit catalog (heuristic, needs human review)"
    CATEGORY = "Semantic Quality"
    # Harmless no-op today (check() below never returns FAIL/WARN, the only
    # levels that get posted) - see c10's comment on POST_COMMENT for why this
    # is still set.
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            if el.unit and not el.unit.startswith("unit:"):
                findings.append(Finding(self.ID, self.TITLE, "SKIP", model.file,
                                         f"'{el.name}' uses unit '{el.unit}' which is not from the "
                                         f"'unit:' catalog prefix - confirm no catalog unit fits",
                                         element=el.name, line=el.line_no))
            if el.short_type == "Unit":
                findings.append(Finding(self.ID, self.TITLE, "SKIP", model.file,
                                         f"'{el.name}' defines a custom samm:Unit - confirm it does not "
                                         f"already exist in the SAMM unit catalog", element=el.name, line=el.line_no))
        if not findings:
            findings.append(Finding(self.ID, self.TITLE, "NOTE", model.file,
                                     "no non-catalog unit references or custom samm:Unit definitions found"))
        return findings
