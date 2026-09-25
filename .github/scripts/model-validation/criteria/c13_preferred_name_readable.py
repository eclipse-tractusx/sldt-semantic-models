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
# MS2-13: "preferredName should be human readable and follow normal
# orthography (e.g., no camel case but normal word separation)".
#
# Heuristic only (WARN, not FAIL): a lowercase-to-uppercase hump can't be
# told apart from a genuine single established term that happens to use
# internal capitalization (e.g. "eCommerce", "iPhone"), so this is a
# plausible but not certain violation.

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

CAMEL_HUMP_RE = re.compile(r"[a-z][A-Z]")

class Criterion(base.Criterion):
    ID = "MS2-13"
    TITLE = "preferredName is human-readable (not Camel-Case) (heuristic, needs human review)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements.values():
            pn = el.preferred_name("en")
            if pn and " " not in pn and CAMEL_HUMP_RE.search(pn):
                findings.append(Finding(self.ID, self.TITLE, "WARN", model.file,
                                         f"preferredName '{pn}' of '{el.name}' looks Camel-Case, "
                                         f"expected normal word separation - confirm it isn't a "
                                         f"genuine single term with internal capitalization",
                                         element=el.name, line=el.line_no))
        return findings
