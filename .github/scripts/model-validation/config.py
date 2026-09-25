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
# Loads config.json from .github/scripts/ (one level up from this module -
# shared by other scripts under .github/scripts/, not just the MS2 criteria
# check), the per-repo config. Two separate sections:
#
# "settings": general settings, currently just:
#
#   "samm_cli_version": the SAMM CLI version to download and run for
#   MS2-01 / MS2-02 (see samm_cli.py). Single source of truth - not parsed
#   out of README.md prose, so it can't silently drift if that text gets
#   reworded, and editing the README doesn't invalidate the SAMM CLI
#   download cache in governance.yml.
#
# "criteria": per-criterion overrides, keyed by criterion id
# ("MS2-01".."MS2-23"), two independent knobs each (both default to "on"):
#
#   "enabled":  false -> the criterion is skipped entirely, no Findings at all
#   "blocking": false -> the criterion still runs and is reported, but any
#                        FAIL it produces is downgraded to WARN, so it no
#                        longer breaks the CI job (still a MUST per the PR
#                        template, just not (yet) enforced automatically)
#
# Example config.json:
#
# {
#   "settings": {
#     "samm_cli_version": "2.12.0"
#   },
#   "criteria": {
#     "MS2-19": {"blocking": false},
#     "MS2-14": {"enabled": false}
#   }
# }
#
# A criterion not mentioned in "criteria", or the file not existing at all
# (it's fine to delete it - an empty/missing file just means no overrides
# and the default SAMM CLI version), behaves exactly as if this module
# didn't exist.

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CONFIG_RELPATH = ".github/scripts/config.json"
DEFAULT_SAMM_CLI_VERSION = "2.12.0"


@dataclass(frozen=True)
class CriterionOverride:
    enabled: bool = True
    blocking: bool = True


@dataclass
class Config:
    overrides: dict[str, CriterionOverride] = field(default_factory=dict)
    samm_cli_version: str = DEFAULT_SAMM_CLI_VERSION

    def for_criterion(self, criterion_id: str) -> CriterionOverride:
        return self.overrides.get(criterion_id, CriterionOverride())

    def is_enabled(self, criterion_id: str) -> bool:
        return self.for_criterion(criterion_id).enabled

    def is_blocking(self, criterion_id: str) -> bool:
        return self.for_criterion(criterion_id).blocking


def load_config(repo_root: Path, path: str = DEFAULT_CONFIG_RELPATH) -> Config:
    config_path = repo_root / path
    if not config_path.exists():
        return Config()

    raw = json.loads(config_path.read_text(encoding="utf-8")) or {}
    settings = raw.get("settings") or {}
    samm_cli_version = settings.get("samm_cli_version") or DEFAULT_SAMM_CLI_VERSION

    overrides = {}
    for criterion_id, criterion_settings in (raw.get("criteria") or {}).items():
        criterion_settings = criterion_settings or {}
        overrides[criterion_id] = CriterionOverride(
            enabled=bool(criterion_settings.get("enabled", True)),
            blocking=bool(criterion_settings.get("blocking", True)),
        )
    return Config(overrides, samm_cli_version)
