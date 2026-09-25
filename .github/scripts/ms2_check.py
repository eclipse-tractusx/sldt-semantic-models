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
# .github/workflows/governance.yml, which runs it three ways):
#
#   --list-changed-files      -> used once by the "detect-changed-models" job
#                                 to build the per-model check matrix (prints
#                                 a JSON array of changed .ttl files)
#   --list-all-changed-files  -> used once by the same job to also hand every
#                                 changed file (not just .ttl) to each matrix
#                                 leg, so they don't each need to compute
#                                 their own git diff (see --changed-files)
#   --file <path>              -> used by each matrix leg of the
#                                 "ms2-criteria-check" job to check exactly
#                                 one model, so each model gets its own check
#                                 mark in the PR UI. Combined with
#                                 --changed-files, a leg needs no git history
#                                 at all - just a shallow checkout.
#   --changed-files <json>     -> supplies the full changed-files list (see
#                                 --list-all-changed-files above) instead of
#                                 computing it locally via git diff
#
# Run without any of these, it auto-detects and checks every changed .ttl
# file in one go via its own git diff (useful for local runs). Either way,
# per file it:
#
#   1. Parses the file into a TTLModel (model-validation/samm_model_parser.py).
#   2. Loads the per-criterion overrides from config.json (one level up,
#      in .github/scripts/), if any (see model-validation/config.py).
#   3. Hands the model + a shared Context to every enabled criterion
#      sub-routine registered in model-validation/criteria/, downgrading
#      FAILs to WARN for criteria configured as non-blocking. FAIL/WARN
#      findings from criteria that opt in via POST_COMMENT (see
#      criteria/__init__.py) are collected and posted as a single PR
#      checklist comment per model (model-validation/github_comments.py).
#   4. Collects all Findings, prints/reports them, and fails the job if any
#      criterion reports a FAIL-level finding.
#
# It intentionally does none of the actual rule-checking itself - each MS2
# checklist item lives in its own sub-routine under criteria/, which is
# where you extend this when a criterion is added or changes. See
# model-validation/criteria/__init__.py for details.
#
# Usage (run from the repository root):
#     python .github/scripts/ms2_check.py [--base-branch origin/main]
#     python .github/scripts/ms2_check.py --list-changed-files
#     python .github/scripts/ms2_check.py --file path/to/Model.ttl

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# The package directory is named "model-validation" (matching the naming of
# .github/actions/model-validation), which is not a valid Python identifier,
# so it can't be the target of a static `from model-validation import ...`
# statement - it has to be loaded dynamically instead.
_pkg = importlib.import_module("model-validation")
criteria = importlib.import_module("model-validation.criteria")
report = importlib.import_module("model-validation.report")
Context = importlib.import_module("model-validation.context").Context
parse_model = importlib.import_module("model-validation.samm_model_parser").parse_model
config_module = importlib.import_module("model-validation.config")
github_comments = importlib.import_module("model-validation.github_comments")


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
        "--list-all-changed-files",
        action="store_true",
        help="Print every changed file (not just .ttl) as a JSON array and "
             "exit. Used by the detect-changed-models job to feed --changed-files.",
    )
    parser.add_argument(
        "--changed-files",
        help="JSON array of every file changed in this PR (not just .ttl), as "
             "produced by --list-all-changed-files. When given, a matrix leg "
             "doesn't need to compute this itself via git diff, so it doesn't "
             "need repo history - just the files at HEAD.",
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

    if args.list_all_changed_files:
        print(json.dumps(ctx.get_changed_files()))
        return 0

    config = config_module.load_config(repo_root)
    _warn_about_unknown_criteria(config)
    categories = {criterion.id: criterion.category for criterion in criteria.REGISTRY}

    # A matrix leg that already knows the full changed-files list (passed by
    # the detect-changed-models job) doesn't need to compute its own git diff
    # - and with it, doesn't need repo history at all, just a shallow checkout.
    ctx.changed_files = json.loads(args.changed_files) if args.changed_files else ctx.get_changed_files()
    ttl_files_to_check = args.files or ctx.get_changed_ttl_files()

    if not ttl_files_to_check:
        print("No .ttl files changed - nothing to check for MS2 criteria.")
        _write_step_summary(report.render_markdown([], [], categories))
        return 0

    all_findings: list[report.Finding] = []
    for ttl_file in ttl_files_to_check:
        print(f"\n=== MS2 criteria for {ttl_file} ===")
        model = parse_model(ttl_file)

        # If the model doesn't even validate against SAMM (MS2-01), don't
        # bother running the rest of the criteria on it - naming
        # conventions, example values etc. on a model that's already known
        # to be broken are noise, not signal. Computed once via the shared
        # cache (see Context.validation_result) rather than by relying on
        # MS2-01 happening to run first in REGISTRY order.
        validation = ctx.validation_result(model) if ctx.samm_jar else None
        model_invalid = validation is not None and validation.returncode != 0

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
                # for this model at all - no 21 additional SKIP rows to
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
