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
# The blueprint every cNN_*.py criterion module must follow - enforced
# here, not just documented. Each such module defines exactly one
# subclass of ``Criterion`` below. Getting it wrong fails immediately at
# import time (the moment criteria/__init__.py's auto-discovery imports
# the module) with a clear ``TypeError`` naming the offending class:
#
# - missing/empty ID, TITLE, or CATEGORY
# - ID not shaped like "MS2-<number>"
# - CATEGORY not one of the four known report sections
# - POST_COMMENT set to something other than a bool
# - ``check`` not overridden (enforced by ABCMeta on instantiation)
#
# That replaces what used to be five separate module-level conventions
# that nothing actually checked - a module could silently omit CATEGORY,
# mistype it, or forget POST_COMMENT, and the only symptom was a
# confusing AttributeError (or nothing at all) far away in ms2_check.py.

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Callable

from ..context import Context
from ..samm_model_parser import Element, TTLModel
from ..report import Finding

# The four report sections a criterion's CATEGORY must be one of - see
# report.py for where this grouping is rendered into the job summary.
CATEGORIES = ("Model Validation", "Formal Requirements", "Naming Conventions", "Semantic Quality")

_ID_RE = re.compile(r"^MS2-\d+$")


class Criterion(ABC):
    ID: str
    TITLE: str
    CATEGORY: str
    # Opt-in (see github_comments.py): include this criterion's FAIL/WARN
    # findings in the per-model PR checklist comment, not just the report.
    POST_COMMENT: bool = False

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        where = f"{cls.__module__}.{cls.__qualname__}"

        id_ = getattr(cls, "ID", None)
        if not isinstance(id_, str) or not _ID_RE.match(id_):
            raise TypeError(f"{where}.ID must look like 'MS2-<number>', got {id_!r}")

        title = getattr(cls, "TITLE", None)
        if not isinstance(title, str) or not title:
            raise TypeError(f"{where}.TITLE must be a non-empty string")

        category = getattr(cls, "CATEGORY", None)
        if category not in CATEGORIES:
            raise TypeError(f"{where}.CATEGORY={category!r} must be one of {CATEGORIES}")

        if not isinstance(cls.POST_COMMENT, bool):
            raise TypeError(f"{where}.POST_COMMENT must be a bool, got {cls.POST_COMMENT!r}")

    @abstractmethod
    def check(self, model: TTLModel, ctx: Context) -> list[Finding]:
        ...

    def element_findings(
        self,
        model: TTLModel,
        predicate: Callable[[Element], str | None],
        message_fn: Callable[[Element, str], str],
        level: str = "FAIL",
    ) -> list[Finding]:
        # Shared by any criterion whose check is "flag every element where
        # some per-element predicate fails" (e.g. c19/c21/c22's naming
        # rules) - runs `predicate(element)` over every element in the
        # model, and turns each truthy result into a Finding via
        # `message_fn`, tagged with this criterion's own ID/TITLE.
        findings = []
        for el in model.elements.values():
            msg = predicate(el)
            if msg:
                findings.append(Finding(self.ID, self.TITLE, level, model.file,
                                         message_fn(el, msg), element=el.name, line=el.line_no))
        return findings
