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
# Checks that the file contains the copyright line "Copyright ... Contributors
# to the Eclipse Foundation". Whether all contributors are named is left to
# the reviewer.

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
