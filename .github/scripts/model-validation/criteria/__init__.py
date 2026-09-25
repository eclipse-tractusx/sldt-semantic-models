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
# One file per MS2 checklist item from PULL_REQUEST_TEMPLATE.md, named
# `cNN_<slug>.py` (NN = the checklist item number). Each such module
# defines exactly one subclass of ``base.Criterion`` - see base.py for the
# blueprint (``ID``/``TITLE``/``CATEGORY``/``POST_COMMENT``/``check``) and
# the validation that runs the moment the module is imported.
#
# A criterion's ``check(model, ctx)`` receives the data package the master
# script (``ms2_check.py``) built for the changed ``.ttl`` file (see
# ``samm_model_parser.py``) plus the shared ``Context`` (see
# ``context.py``). Nothing in here talks to the list of changed files,
# GitHub, or the per-criterion config (see ``config.py``) directly -
# that's the master's job.
#
# Not every MS2 criterion can be verified with certainty from the file
# content alone. Criteria that are only heuristically checkable report at
# WARN level instead of FAIL, and say so, rather than pretending to be an
# authoritative check; criteria that can't render a verdict at all (e.g.
# "abbreviations only when necessary" is a pure judgement call - see
# c10_abbreviations.py) still implement ``check``, but it always returns
# the same static SKIP/NOTE regardless of file content, rather than
# pretending to analyze something unanalyzable. FAIL is reserved for
# criteria that are genuinely unambiguous from the text - and even those
# can be downgraded to non-blocking per-repo via config.json
# (see config.py) if a team decides a given MUST shouldn't break CI yet.
#
# REGISTRY below is built automatically by importing every cNN_*.py module
# in this folder (in numeric order) and instantiating the one
# base.Criterion subclass it defines. To add a new criterion: drop in a
# new cNN_<slug>.py file with a class following that blueprint - no need
# to touch this file. A module that doesn't define exactly one such
# subclass is a bug in that module, not a supported way to opt out of the
# report - blueprint violations fail the whole run at import time (see
# base.py) rather than being silently skipped.

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import base
from ..samm_model_parser import TTLModel
from ..context import Context
from ..report import Finding

_PACKAGE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class RegistryEntry:
    id: str
    title: str
    category: str
    check: Callable[[TTLModel, Context], list[Finding]]
    post_comment: bool = False


def _find_criterion_class(module) -> type[base.Criterion]:
    candidates = [
        obj for obj in vars(module).values()
        if isinstance(obj, type) and issubclass(obj, base.Criterion)
        and obj is not base.Criterion and obj.__module__ == module.__name__
    ]
    if len(candidates) != 1:
        raise TypeError(
            f"{module.__name__} must define exactly one base.Criterion subclass, found {len(candidates)}")
    return candidates[0]


def _discover_registry() -> list[RegistryEntry]:
    registry = []
    modules = sorted(
        (m for m in pkgutil.iter_modules([str(_PACKAGE_DIR)]) if m.name[:1] == "c"),
        key=lambda m: m.name,
    )
    for module_info in modules:
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        criterion_cls = _find_criterion_class(module)
        instance = criterion_cls()
        registry.append(RegistryEntry(
            id=instance.ID, title=instance.TITLE, category=instance.CATEGORY,
            check=instance.check, post_comment=instance.POST_COMMENT,
        ))
    return registry


REGISTRY = _discover_registry()
