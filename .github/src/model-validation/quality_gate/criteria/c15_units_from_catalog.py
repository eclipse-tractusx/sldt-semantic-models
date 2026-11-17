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
# Lists unit references outside the SAMM unit catalog and custom samm:Unit
# definitions for the reviewer (SKIP); otherwise reports a NOTE.

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

# The unit catalog's namespace - bound to whatever prefix name the model
# chooses ("unit:", "samm-u:", ...), so the prefix is resolved, not compared.
UNIT_CATALOG_RE = re.compile(r"urn:[bs]amm:[\w.]+:unit:\d+\.\d+\.\d+#")

def _from_catalog(model: TTLModel, unit: str) -> bool:
    prefix = unit.split(":", 1)[0] if ":" in unit else None
    return prefix is not None and UNIT_CATALOG_RE.fullmatch(model.prefixes.get(prefix, "")) is not None

class Criterion(base.Criterion):
    ID = "MS2-15"
    TITLE = "Units reference the SAMM unit catalog (heuristic, needs human review)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements:
            unit = el.get("unit")
            if isinstance(unit, str) and not _from_catalog(model, unit):
                findings.append(Finding(self.ID, self.TITLE, "SKIP", model.file,
                                         f"'{el.label}' uses unit '{unit}' which is not from the "
                                         f"SAMM unit catalog - confirm no catalog unit fits",
                                         element=el.label, line=el.line_no))
            if el.is_a("Unit"):
                findings.append(Finding(self.ID, self.TITLE, "SKIP", model.file,
                                         f"'{el.label}' defines a custom samm:Unit - confirm it does not "
                                         f"already exist in the SAMM unit catalog", element=el.label, line=el.line_no))
        if not findings:
            findings.append(Finding(self.ID, self.TITLE, "NOTE", model.file,
                                     "no non-catalog unit references or custom samm:Unit definitions found"))
        return findings
