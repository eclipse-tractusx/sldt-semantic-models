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
# MS2-07: "file RELEASE_NOTES.md exists and contains entries for proposed
# model changes".

from __future__ import annotations

import re
from pathlib import Path

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-07"
    TITLE = "RELEASE_NOTES.md exists and documents this version"
    CATEGORY = "Formal Requirements"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        if not model.namespace:
            return [Finding(self.ID, self.TITLE, "FAIL", model.file, "could not determine this model's namespace", line=1)]

        release_notes = Path(model.namespace) / "RELEASE_NOTES.md"
        if not release_notes.exists():
            return [Finding(self.ID, self.TITLE, "FAIL", model.file, f"{release_notes} does not exist", line=1)]

        text = release_notes.read_text(encoding="utf-8")
        if model.version and not re.search(re.escape(f"[{model.version}]"), text):
            return [Finding(self.ID, self.TITLE, "WARN", model.file,
                             f"{release_notes} has no entry mentioning '[{model.version}]'", line=1)]

        # An entry for this version is enough on its own - whether
        # RELEASE_NOTES.md itself was touched in this PR used to be checked
        # separately, but that only ever produced a near-duplicate warning
        # alongside the one above without adding real signal.
        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                         f"{release_notes} mentions version {model.version}")]
