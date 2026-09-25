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
# MS2-01: "the model validates with the SAMM SDS SDK in the version
# specified in the Readme.md of this repository by the time of the MS2
# check".
#
# Deviates from the letter of that wording: the version actually comes
# from config.json's "settings.samm_cli_version" key (see config.py), not
# parsed out of README.md - see config.py's module comment for why.
#
# The actual `validate` run lives in ctx.validation_result() (see
# context.py), shared with generated_artifacts() and ms2_check.py's main
# loop, which both skip further work entirely for a model that fails here
# - there's no point generating schema/payload or checking naming
# conventions on a model that's already known to be broken.

from __future__ import annotations

import re

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")
MAX_DETAIL_LENGTH = 2000

def _clean_detail(text: str) -> str:
    text = ANSI_ESCAPE_RE.sub("", text).strip()
    if len(text) > MAX_DETAIL_LENGTH:
        text = text[:MAX_DETAIL_LENGTH] + "... (truncated)"
    return text

# Runs `samm-cli aspect <file> validate` for real. A model that fails this
# is treated as broken at the most basic level - every other criterion is
# skipped entirely for it.
class Criterion(base.Criterion):
    ID = "MS2-01"
    TITLE = "Model validates with SAMM CLI"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        if ctx.samm_jar is None:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file,
                             "SAMM CLI jar unavailable (no Java / no network) - run "
                             "`java -jar samm-cli-<version>.jar aspect <file> validate` manually")]

        result = ctx.validation_result(model)
        if result.returncode != 0:
            detail = _clean_detail(result.stdout or result.stderr or f"exit code {result.returncode}")
            return [Finding(self.ID, self.TITLE, "FAIL", model.file, f"samm-cli validation failed:\n{detail}", line=1)]
        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file, "samm-cli validation passed")]
