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

# MS2-25: "existing model versions are never overwritten - every change to
# a model requires a new version".
#
# Fails if this model's .ttl file already exists on the base branch and was
# modified on this branch.

from __future__ import annotations

from pathlib import PurePosixPath

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base


def _norm(path: str) -> str:
    return PurePosixPath(path.replace("\\", "/")).as_posix()


class Criterion(base.Criterion):
    ID = "MS2-25"
    # An existing model version (.ttl already on the base branch) must not be modified.
    TITLE = "Existing model version is not overwritten"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        if ctx.modified_ttl_files is None:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file,
                             "modified-files list not available in this run (pass --modified-files)")]

        if _norm(model.file) in {_norm(f) for f in ctx.modified_ttl_files}:
            return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                             f"{model.file} already exists on {ctx.base_branch} and was modified - "
                             f"existing versions must not be overwritten, create a new version instead",
                             line=1)]
        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                         "new model version, no existing version overwritten")]
