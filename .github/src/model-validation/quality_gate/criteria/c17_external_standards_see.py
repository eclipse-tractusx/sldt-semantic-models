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

# MS2-17: "when relying on external standards, they are referenced through
# a 'see' element".
#
# Lists the samm:see references in the model for the reviewer (NOTE).

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-17"
    TITLE = "External standards referenced via samm:see (not automatically verifiable)"
    CATEGORY = "Semantic Quality"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        with_see = [el.label for el in model.elements if el.get_all("see")]
        if with_see:
            result = f"{len(with_see)} element(s) carry a samm:see reference: {with_see}"
        else:
            result = ("no samm:see references found - if this model implements/relates to an "
                      "external standard, reference it via samm:see")
        return [Finding(self.ID, self.TITLE, "NOTE", model.file,
                         f"{result} (checked by reviewer - not automatically verifiable)")]
