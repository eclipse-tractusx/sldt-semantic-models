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
# Finding data structure and report rendering shared by all criteria.

from __future__ import annotations

from dataclasses import dataclass

# FAIL    -> objectively violates a MS2 rule, breaks the CI check
# WARN    -> rule is only partially machine-checkable (heuristic) or the
#            finding is a likely-but-not-certain violation; does not break CI
# SUCCESS -> a genuine automated pass: this was actually checked and nothing
#            is wrong
# NOTE    -> the criterion can never render a pass/fail verdict at all (the
#            question isn't machine-answerable from the file), so this is
#            just a fact for the reviewer, not a confirmation of anything.
#            Doesn't break CI (same as SUCCESS), but counted separately in
#            the summary line ("N passing" vs "M for manual review") and
#            given a different icon, so it never reads as an actual
#            automated pass.
# SKIP    -> criterion could not be evaluated (e.g. missing external tool)
LEVELS = ("FAIL", "WARN", "SUCCESS", "NOTE", "SKIP")


@dataclass
class Finding:
    criterion_id: str
    title: str
    level: str
    file: str
    message: str
    element: str | None = None
    # 1-based line in `file` this finding is anchored to (e.g. an element's
    # declaration line - see samm_model_parser.Element.line_no), or None
    # when the finding isn't tied to a specific line (e.g. a file-wide
    # criterion). Only consumed by github_comments.py to place an inline PR
    # review comment - unrelated to the console/Markdown report above.
    line: int | None = None

    def __str__(self) -> str:
        loc = f"{self.file}" + (f" [{self.element}]" if self.element else "")
        return f"{self.level:<4} {self.criterion_id} {loc}: {self.message}"


def has_failures(findings: list[Finding]) -> bool:
    return any(f.level == "FAIL" for f in findings)


# Table icon per level: check = genuine automated pass, info = non-
# evaluable fact for the reviewer, warning = non-blocking heads-up, cross =
# blocking failure, dash = doesn't matter right now (skipped/disabled/
# couldn't run).
ICON = {"FAIL": "❌", "WARN": "⚠️", "SUCCESS": "✅", "NOTE": "ℹ️", "SKIP": "➖"}


def _flatten(text: str) -> str:
    return text.replace("\n", " ")


def _escape_cell(text: str) -> str:
    return _flatten(text).replace("|", "\\|")


def _code_cell(text: str) -> str:
    # Wraps a table cell's content in an inline code span so it renders in
    # monospace - real line breaks don't survive inside a table cell, but
    # at least indentation/alignment reads better than flowing prose. `|`
    # doesn't need escaping inside a code span (GFM tables don't treat it
    # as a cell separator there); a literal backtick would end the span
    # early though, so that one still needs handling.
    return f"`{_flatten(text).replace('`', chr(39))}`"


def render_markdown(findings: list[Finding], files_checked: list[str], categories: dict[str, str]) -> str:
    # categories: criterion_id -> category name (see Criterion.category in
    # criteria/__init__.py), used to group each model's table into
    # sections. A criterion_id missing from this mapping (shouldn't happen
    # - every REGISTRY entry has a category) falls back to "Other" rather
    # than raising, so a report can still render.
    if not files_checked:
        return "\n".join(["# MS2 Criteria Report", "", "No `.ttl` files were changed in this PR."])

    # Each CI matrix leg (see governance.yml) checks exactly one model, so
    # its job summary would otherwise carry a redundant "## MS2 Criteria -
    # <file>" sub-header repeating what's already the only file in the
    # report. Put the model name in the title instead and skip the
    # sub-header - but only when there's actually just one file: a local
    # run without --file can check several changed .ttl files in one
    # report, where the sub-header is what tells those sections apart.
    # Category headers shift down one level accordingly (## normally,
    # ### when nested under a per-file ## sub-header).
    single_file = len(files_checked) == 1
    title = f"# MS2 Criteria Report — {files_checked[0]}" if single_file else "# MS2 Criteria Report"
    lines = [title, ""]
    category_heading = "##" if single_file else "###"

    by_file: dict[str, list[Finding]] = {}
    for finding in findings:
        by_file.setdefault(finding.file, []).append(finding)

    for file in files_checked:
        file_findings = by_file.get(file, [])

        if not single_file:
            lines.append(f"## MS2 Criteria — {file}")
            lines.append("")

        counts = {level: sum(1 for f in file_findings if f.level == level) for level in LEVELS}
        lines.append(
            f"**Summary:** {counts['FAIL']} failing, {counts['WARN']} warnings, "
            f"{counts['SUCCESS']} passing, {counts['NOTE']} for manual review, {counts['SKIP']} skipped."
        )
        lines.append("")

        by_criterion: dict[str, list[Finding]] = {}
        for finding in file_findings:
            by_criterion.setdefault(finding.criterion_id, []).append(finding)

        by_category: dict[str, list[str]] = {}
        for criterion_id in by_criterion:
            by_category.setdefault(categories.get(criterion_id, "Other"), []).append(criterion_id)

        # Categories ordered by the lowest criterion id they contain, so
        # the report still reads roughly MS2-01 -> MS2-23 top to bottom -
        # just grouped, not fully interleaved.
        def _category_sort_key(category: str) -> str:
            return min(by_category[category])

        for category in sorted(by_category, key=_category_sort_key):
            lines.append(f"{category_heading} {category}")
            lines.append("")
            lines.append("| | ID | Criterion | Message |")
            lines.append("|---|---|---|---|")

            for criterion_id in sorted(by_category[category]):
                group = by_criterion[criterion_id]
                worst = min(group, key=lambda f: LEVELS.index(f.level))
                messages = "<br>".join(_code_cell(f.message) for f in group)
                lines.append(
                    f"| {ICON[worst.level]} | {criterion_id} | {_escape_cell(group[0].title)} | {messages} |")

            lines.append("")

    return "\n".join(lines)


def render_detected_models(files: list[str]) -> str:
    lines = ["# Detected Models", ""]
    if not files:
        lines.append("No `.ttl` files changed in this PR - MS2 criteria check skipped.")
        return "\n".join(lines)

    lines.append(f"{len(files)} model file(s) changed, one MS2 Criteria check each:")
    lines.append("")
    for f in files:
        lines.append(f"- `{f}`")
    return "\n".join(lines)


def print_console(findings: list[Finding]) -> None:
    for finding in findings:
        print(finding)
