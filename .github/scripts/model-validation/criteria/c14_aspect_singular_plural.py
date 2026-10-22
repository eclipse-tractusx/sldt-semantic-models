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
# MS2-14: "name of aspect is singular except if it only has one property
# which is a Collection, List or Set. In these cases, the aspect name is
# plural."
#
# Not a machine-checkable criterion: singular/plural in English has too
# many edge cases (irregular plurals, property counts skewed by imported
# properties, ...) to decide reliably from the file alone. Doesn't attempt
# any analysis; always reports the same static SKIP note that this item
# needs manual review.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-14"
    TITLE = "Aspect name is singular/plural depending on single Collection property (not automatically verifiable)"
    CATEGORY = "Naming Conventions"
    # Harmless no-op today (check() below only ever returns SKIP) - see c10's
    # comment on POST_COMMENT for why this is still set.
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        return [Finding(self.ID, self.TITLE, "SKIP", model.file,
                         "checked by reviewer - singular/plural naming cannot be automatically verified")]
