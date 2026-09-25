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

from __future__ import annotations

import json
import re
from pathlib import Path

from ..context import Context
from ..samm_model_parser import TTLModel
from ..report import Finding
from . import base

PREFIX_RE = re.compile(r"@prefix\s+([\w-]+):\s+<urn:[bs]amm:([\w.]+):(\d+\.\d+\.\d+)#>")

def _parse_prefixes(ttl_path: str) -> list[dict[str, str]]:
    prefixes = []
    with open(ttl_path) as f:
        for line in f:
            m = PREFIX_RE.search(line)
            if m:
                prefixes.append({"prefix": m.group(1), "folder": m.group(2), "version": m.group(3)})
    return prefixes

def _read_metadata(folder: str, version: str) -> dict | None:
    meta_path = Path(folder) / version / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path) as f:
        return json.load(f)

class Criterion(base.Criterion):
    ID = "MS2-05"
    TITLE = "Imported models are in 'release' state"
    CATEGORY = "Model Validation"
    POST_COMMENT = True

    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        findings = []
        for prefix_info in _parse_prefixes(model.file):
            folder, version = prefix_info["folder"], prefix_info["version"]
            if folder == model.namespace and version == model.version:
                continue  # this is the model's own namespace, see MS2-03
            meta = _read_metadata(folder, version)
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
