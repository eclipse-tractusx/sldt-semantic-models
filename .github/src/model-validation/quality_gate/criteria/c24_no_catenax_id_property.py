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

# MS2-24: "the property name 'catenaXId' (in any spelling) must not be used".
#
# Checks property identifiers and samm:payloadName values; spellings such
# as 'CatenaXID', 'catenaxid' or 'catena_x_id' count as the same name.

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

_FORBIDDEN = "catenaxid"


def _is_forbidden(name: str | None) -> bool:
    return bool(name) and re.sub(r"[^a-z0-9]", "", name.lower()) == _FORBIDDEN


class Criterion(base.Criterion):
    ID = "MS2-24"
    # The property name 'catenaXId' is not allowed, in any spelling.
    TITLE = "Property name 'catenaXId' is not used"
    CATEGORY = "Naming Conventions"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for el in model.elements:
            if not el.is_a("Property"):
                continue
            if _is_forbidden(el.name):
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"property identifier '{el.name}' is not allowed",
                                         element=el.label, line=el.line_no))
            payload_name = el.get("payloadName")
            if payload_name and _is_forbidden(payload_name.text):
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"payloadName '{payload_name.text}' is not allowed",
                                         element=el.label, line=el.line_no))
        return findings
