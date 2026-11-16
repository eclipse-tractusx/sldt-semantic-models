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

# MS2-03: "all artifact types generate successfully".
#
# Checks that every artifact type (AAS XML, AASX, JSON schema, example
# payload, OpenAPI, HTML, Parquet) can be generated from the model.

from __future__ import annotations

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-03"
    TITLE = "All artifact types generate successfully"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        result = ctx.artifacts(model)
        if result.skipped:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file, result.skip_reason)]

        if result.failures:
            details = "; ".join(f"{label} ({msg})" for label, msg in result.failures.items())
            return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                             f"could not generate: {', '.join(result.failures)} - {details}", line=1)]

        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                         "all artifact types generated successfully")]
