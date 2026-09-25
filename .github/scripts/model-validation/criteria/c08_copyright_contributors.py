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
# MS2-08: "all contributors to this model are mentioned in copyright header
# of model file".
#
# Verifying that the header names *every* contributor isn't reliably
# automatable (git authorship is GitHub account names, headers name
# companies/organizations - the two don't map 1:1). Instead, this just
# checks for the standard "Contributors to the Eclipse Foundation" line
# that every properly-headered model carries alongside the named
# companies - its presence is a reliable proxy for "this header follows
# the required format", without parsing individual holder lines (which
# vary in year format: single year, comma lists, ranges, ...).

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

ECLIPSE_COPYRIGHT_RE = re.compile(
    r"#.*Copyright.*Contributors to the Eclipse Foundation", re.IGNORECASE)

class Criterion(base.Criterion):
    ID = "MS2-08"
    TITLE = "Copyright header exists"
    CATEGORY = "Formal Requirements"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        if ECLIPSE_COPYRIGHT_RE.search(model.text):
            return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                             "'Contributors to the Eclipse Foundation' copyright line present")]
        return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                         "no 'Copyright ... Contributors to the Eclipse Foundation' line found in header", line=1)]
