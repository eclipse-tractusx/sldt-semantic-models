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
# MS2-02: "generated json schema validates against example json payload".
#
# The JSON schema and example payload themselves come from
# ctx.generated_artifacts() (see context.py), which runs the SAMM CLI's
# `aspect <file> to schema` / `aspect <file> to json` commands (same ones
# as generate.sh) and caches the result per model file - shared with any
# other criterion that wants the same generated artifacts. This criterion
# just cross-validates them with the `jsonschema` package if installed.

from __future__ import annotations

import json

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

class Criterion(base.Criterion):
    ID = "MS2-02"
    TITLE = "Generated JSON schema validates against generated example payload"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        artifacts = ctx.generated_artifacts(model)
        if artifacts.schema_path is None or artifacts.payload_path is None:
            level = "SKIP" if artifacts.skipped else "FAIL"
            return [Finding(self.ID, self.TITLE, level, model.file, artifacts.error, line=1 if level == "FAIL" else None)]

        try:
            import jsonschema
        except ImportError:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file,
                             "schema and example payload generated successfully, but the "
                             "'jsonschema' package is not installed so they were not cross-validated "
                             "(pip install jsonschema)")]

        schema = json.loads(artifacts.schema_path.read_text(encoding="utf-8"))
        payload = json.loads(artifacts.payload_path.read_text(encoding="utf-8"))
        try:
            jsonschema.validate(payload, schema)
        except jsonschema.ValidationError as e:
            return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                             f"generated example payload does not validate against the generated "
                             f"JSON schema: {e.message}", line=1)]

        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                         "generated JSON schema validates against the generated example payload")]
