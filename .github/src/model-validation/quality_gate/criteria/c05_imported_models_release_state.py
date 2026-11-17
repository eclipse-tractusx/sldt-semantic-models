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

# MS2-05: "all external / imported models have the state 'release'".
#
# Checks that every model imported via a prefix has a metadata.json with
# status 'release'.

from __future__ import annotations

import json
import re
from pathlib import Path

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

# A prefix URI pointing at another model in this repo, e.g.
# "urn:samm:io.catenax.shared.uuid:2.0.0#" -> folder + version.
MODEL_URN_RE = re.compile(r"urn:[bs]amm:([\w.]+):(\d+\.\d+\.\d+)#")

def _imported_models(model: TTLModel) -> list[tuple[str, str]]:
    imported = []
    for uri in model.prefixes.values():
        m = MODEL_URN_RE.fullmatch(uri)
        if m:
            imported.append((m.group(1), m.group(2)))
    return imported

def _read_metadata(folder: str, version: str) -> dict | None:
    meta_path = Path(folder) / version / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path) as f:
        return json.load(f)  # raises json.JSONDecodeError on malformed JSON; caller handles it

class Criterion(base.Criterion):
    ID = "MS2-05"
    TITLE = "Imported models are in 'release' state"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for folder, version in _imported_models(model):
            if folder == model.namespace and version == model.version:
                continue  # this is the model's own namespace, see MS2-04
            try:
                meta = _read_metadata(folder, version)
            except json.JSONDecodeError as e:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"metadata.json for imported model {folder}:{version} "
                                         f"is not valid JSON: {e}", line=1))
                continue
            if not meta:
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"metadata.json not found for imported model {folder}:{version}", line=1))
            elif meta.get("status") != "release":
                findings.append(Finding(self.ID, self.TITLE, "FAIL", model.file,
                                         f"imported model {folder}:{version} has status "
                                         f"'{meta.get('status')}', expected 'release'", line=1))
        if not findings:
            findings.append(Finding(self.ID, self.TITLE, "SUCCESS", model.file,
                                     "all imported/external models are in 'release' state"))
        return findings
