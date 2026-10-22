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
# MS2-21: "use Camel-Case".

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

CAMEL_CASE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")

class Criterion(base.Criterion):
    ID = "MS2-21"
    # All identifiers must use Camel-Case (letters/digits only, no other characters).
    TITLE = "Identifiers use Camel-Case"
    CATEGORY = "Naming Conventions"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        def bad(el):
            return None if CAMEL_CASE_RE.match(el.name) else "contains characters other than letters/digits"

        return self.element_findings(model, bad, lambda el, msg: f"identifier '{el.name}' is not Camel-Case ({msg})")
