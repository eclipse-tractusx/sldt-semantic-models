#!/usr/bin/env python3
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
# Master script for the MS2 criteria check (see .github/PULL_REQUEST_TEMPLATE.md).
#
# This is the single entry point triggered by CI on every pull request (see
# .github/workflows/governance.yml, which runs it two ways):
#
#   --list-changed-files      -> used once by the "detect-changed-models" job
#                                 to build the per-model check matrix (prints
#                                 a JSON array of changed .ttl files)
#   --list-modified-files     -> also used by "detect-changed-models": prints
#                                 the subset of those that already existed on
#                                 the base branch (existing versions being
#                                 overwritten, see MS2-25)
#   --file <path>              -> used by each matrix leg of the
#                                 "ms2-criteria-check" job to check exactly
#                                 one model, so each model gets its own check
#                                 mark in the PR UI. Needs no git history at
#                                 all - just a shallow checkout. Gets the
#                                 --list-modified-files result via
#                                 --modified-files.
#
# Run without any of these, it auto-detects and checks every changed .ttl
# file in one go via its own git diff (useful for local runs). Either way,
# per file it:
#
#   1. Parses the file into a TTLModel (quality_gate/samm_model_parser.py).
#   2. Loads the per-criterion overrides from config.json (in
#      .github/src/), if any (see quality_gate/config.py).
#   3. Hands the model + a shared Context to every enabled criterion
#      sub-routine registered in quality_gate/criteria/, downgrading
#      FAILs to WARN for criteria configured as non-blocking. FAIL/WARN
#      findings from criteria that opt in via POST_COMMENT (see
#      criteria/__init__.py) are collected and posted as a single PR
#      checklist comment per model (quality_gate/github_comments.py).
#   4. Collects all Findings, prints/reports them, and fails the job if any
#      criterion reports a FAIL-level finding.
#
# It intentionally does none of the actual rule-checking itself - each MS2
# checklist item lives in its own sub-routine under criteria/, which is
# where you extend this when a criterion is added or changes. See
# quality_gate/criteria/__init__.py for details.
#
# Usage (run from the repository root):
#     python .github/src/model-validation/ms2_check.py [--base-branch origin/main]
#     python .github/src/model-validation/ms2_check.py --list-changed-files
#     python .github/src/model-validation/ms2_check.py --list-modified-files
#     python .github/src/model-validation/ms2_check.py --file path/to/Model.ttl

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quality_gate import config as config_module
from quality_gate import criteria, github_comments, report, samm_model_parser
from quality_gate.context import Context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Runs the MS2 criteria check (see .github/PULL_REQUEST_TEMPLATE.md) "
                     "against .ttl files changed on this branch."
    )
    parser.add_argument(
        "--base-branch",
        default=os.environ.get("MS2_BASE_BRANCH", "origin/main"),
        help="Branch to diff against to find changed files (default: origin/main)",
    )
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Check only this .ttl file instead of auto-detecting changed files "
             "(repeatable). Used by the per-model matrix job in governance.yml.",
    )
    parser.add_argument(
        "--list-changed-files",
        action="store_true",
        help="Print the changed .ttl files as a JSON array and exit - nothing "
             "else is printed. Used by the detect-changed-models job to build "
             "the per-model check matrix.",
    )
    parser.add_argument(
        "--list-modified-files",
        action="store_true",
        help="Print the .ttl files that already existed on the base branch and "
             "were modified on this branch as a JSON array and exit. Used by the "
             "detect-changed-models job, handed to each matrix leg via --modified-files.",
    )
    parser.add_argument(
        "--modified-files",
        default=None,
        help="JSON array as printed by --list-modified-files (used by MS2-25).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    ctx = Context(repo_root=repo_root, base_branch=args.base_branch)

    if args.list_changed_files:
        ttl_files = ctx.get_changed_ttl_files()
        _write_step_summary(report.render_detected_models(ttl_files))
        print(json.dumps(ttl_files))
        return 0

    if args.list_modified_files:
        print(json.dumps(ctx.get_modified_ttl_files()))
        return 0

    if args.modified_files is not None:
        ctx.modified_ttl_files = json.loads(args.modified_files)
    elif not args.files:
        ctx.modified_ttl_files = ctx.get_modified_ttl_files()

    config = config_module.load_config(repo_root)
    _warn_about_unknown_criteria(config)
    categories = {criterion.id: criterion.category for criterion in criteria.REGISTRY}

    ttl_files_to_check = args.files or ctx.get_changed_ttl_files()

    if not ttl_files_to_check:
        print("No .ttl files changed - nothing to check for MS2 criteria.")
        _write_step_summary(report.render_markdown([], [], categories))
        return 0

    all_findings: list[report.Finding] = []
    for ttl_file in ttl_files_to_check:
        print(f"\n=== MS2 criteria for {ttl_file} ===")
        try:
            model = samm_model_parser.parse_model(ttl_file)
        except samm_model_parser.TurtleSyntaxError as e:
            # Not even valid Turtle - gated the same way as a model failing
            # samm-cli validate (see below): only MS2-01's FAIL is reported.
            ms2_01 = next(c for c in criteria.REGISTRY if c.id == "MS2-01")
            finding = report.Finding(ms2_01.id, ms2_01.title, "FAIL", ttl_file, f"not valid Turtle: {e}", line=1)
            all_findings.append(finding)
            report.print_console([finding])
            github_comments.post_checklist_comment(ttl_file, [finding])
            continue

        # If the model doesn't even validate against SAMM (MS2-01), don't
        # bother running the rest of the criteria on it - naming
        # conventions, example values etc. on a model that's already known
        # to be broken are noise, not signal. Computed once via the shared
        # cache (see Context.validation_result) rather than by relying on
        # MS2-01 happening to run first in REGISTRY order.
        validation = ctx.validation_result(model) if ctx.samm_jar else None
        model_invalid = validation is not None and validation.returncode != 0

        # Every artifact type (schema, payload, AAS, ...) is generated once
        # here, before any criterion runs - criteria only read the result
        # via ctx.artifacts(model) instead of each shelling out to samm-cli
        # for the same file again.
        if not model_invalid:
            ctx.generate_artifacts(model)

        # Findings from POST_COMMENT-enabled criteria, collected across the
        # whole model and posted as a single PR checklist comment after the
        # loop below - see github_comments.post_checklist_comment.
        comment_findings: list[report.Finding] = []

        for criterion in criteria.REGISTRY:
            if not config.is_enabled(criterion.id):
                finding = report.Finding(
                    criterion.id, criterion.title, "SKIP", ttl_file,
                    f"disabled via {config_module.DEFAULT_CONFIG_RELPATH} (enabled: false)",
                )
                all_findings.append(finding)
                report.print_console([finding])
                continue

            if model_invalid and criterion.id != "MS2-01":
                # Not even reported as SKIP: an invalid model makes every
                # other criterion moot, so only MS2-01's own FAIL shows up
                # for this model at all - no SKIP row for every other criterion to
                # scroll past.
                print(f"{criterion.id} not evaluated - model does not validate against SAMM CLI (see MS2-01)")
                continue

            findings = criterion.check(model, ctx)
            if not findings:
                # A criterion that only flags problems (and stays silent
                # when there's nothing to flag) still needs a row in the
                # report table, so treat "nothing reported" as a pass.
                findings = [report.Finding(criterion.id, criterion.title, "SUCCESS", ttl_file, "no issues found")]
            if not config.is_blocking(criterion.id):
                for finding in findings:
                    if finding.level == "FAIL":
                        finding.level = "WARN"
                        finding.message += " (non-blocking: downgraded from FAIL via " \
                                            f"{config_module.DEFAULT_CONFIG_RELPATH})"
            if criterion.post_comment:
                comment_findings.extend(f for f in findings if f.level in ("FAIL", "WARN"))
            all_findings.extend(findings)
            report.print_console(findings)

        github_comments.post_checklist_comment(ttl_file, comment_findings)

    markdown = report.render_markdown(all_findings, ttl_files_to_check, categories)
    _write_step_summary(markdown)

    if report.has_failures(all_findings):
        print("\nMS2 criteria check FAILED - see FAIL entries above.")
        return 1

    print("\nMS2 criteria check passed (WARN/SUCCESS entries may still need human review).")
    return 0


def _warn_about_unknown_criteria(config: config_module.Config) -> None:
    known_ids = {criterion.id for criterion in criteria.REGISTRY}
    unknown = set(config.overrides) - known_ids
    for criterion_id in sorted(unknown):
        print(f"WARNING: {config_module.DEFAULT_CONFIG_RELPATH} configures unknown criterion "
              f"'{criterion_id}' (typo? known ids: {sorted(known_ids)})")


def _write_step_summary(markdown: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(markdown)
        f.write("\n")


if __name__ == "__main__":
    sys.exit(main())
