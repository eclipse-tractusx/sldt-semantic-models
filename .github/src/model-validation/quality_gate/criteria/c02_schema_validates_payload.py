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
# Validates the generated example JSON payload against the generated JSON
# schema.

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
        artifacts = ctx.artifacts(model)
        if artifacts.skipped:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file, artifacts.skip_reason)]

        for label in ("schema.json", "payload.json"):
            if label in artifacts.failures:
                return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                                 f"{label} generation failed: {artifacts.failures[label]}", line=1)]

        try:
            import jsonschema
        except ImportError:
            return [Finding(self.ID, self.TITLE, "SKIP", model.file,
                             "schema and example payload generated successfully, but the "
                             "'jsonschema' package is not installed so they were not cross-validated "
                             "(pip install jsonschema==4.26.0)")]

        schema = json.loads(artifacts.paths["schema.json"].read_text(encoding="utf-8"))
        payload = json.loads(artifacts.paths["payload.json"].read_text(encoding="utf-8"))
        try:
            jsonschema.validate(payload, schema)
        except jsonschema.ValidationError as e:
            return [Finding(self.ID, self.TITLE, "FAIL", model.file,
                             f"generated example payload does not validate against the generated "
                             f"JSON schema: {e.message}", line=1)]

        return [Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                         "generated JSON schema validates against the generated example payload")]
