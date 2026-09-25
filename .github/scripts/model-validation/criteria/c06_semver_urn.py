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
# MS2-06: "the versioning in the URN follows semantic versioning, where
# minor version bumps are backwards compatible and major version bumps are
# not backwards compatible."
#
# Only the MAJOR.MINOR.PATCH *format* of the URN (and that it matches the
# version folder it lives in) is machine-checkable here; whether a given
# bump is actually backwards-compatible requires comparing the model
# content against the previous version and is left to the reviewer.

from __future__ import annotations

import re
from pathlib import Path

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-06"
    # The URN version must be well-formed MAJOR.MINOR.PATCH semver and match its version folder.
    TITLE = "URN version follows semantic versioning"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        if model.version is None:
            findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                     "could not find a base ':' prefix of the form "
                                     "<urn:samm:<namespace>:<MAJOR.MINOR.PATCH>#>", line=1))
            return findings

        path_parts = Path(model.file).parts
        version_dirs = [p for p in path_parts if re.fullmatch(r"\d+\.\d+\.\d+", p)]
        if version_dirs and version_dirs[0] != model.version:
            findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                     f"URN version '{model.version}' does not match the "
                                     f"version folder '{version_dirs[0]}'", line=1))
        if not findings:
            findings.append(Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                                     f"URN version '{model.version}' is well-formed and matches its folder"))
        return findings
