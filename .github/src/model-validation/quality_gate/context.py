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
# The Context object is created once by the master script and handed to
# every criterion sub-routine together with the parsed model. It bundles
# everything that is shared across criteria (repo root, list of changed
# files, a lazily-downloaded SAMM CLI jar, git plumbing, ...) so individual
# criteria stay small and don't each re-implement this bookkeeping.

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import config, samm_cli


# Every artifact format generate.sh also produces for a model (see its
# `commands`/`toggles` arrays), kept in sync with that script by hand:
# there's no single source both a shell script and this Python package can
# read without one shelling out to the other. Unlike generate.sh, these go
# into a scratch directory nothing gets committed from. HTML is generated
# without the Catena-X stylesheet (generate.sh's `-c`) here - that flag
# only changes the page's look, not whether generation succeeds.
ARTIFACT_FORMATS: list[tuple[str, list[str]]] = [
    ("aas.xml", ["aas", "-f", "xml"]),
    ("aasx", ["aas", "-f", "aasx"]),
    ("schema.json", ["schema"]),
    ("payload.json", ["json"]),
    ("openapi.yml", ["openapi", "-b=catenax.io"]),
    ("html", ["html"]),
    ("parquet", ["parquet"]),
]


@dataclass
class Artifacts:
    # Every format in ARTIFACT_FORMATS, generated once per model by
    # Context.generate_artifacts (called from ms2_check.py's main loop
    # before any criterion runs) - criteria only read this, so each
    # `samm-cli aspect <file> to <format>` runs exactly once per model.
    #
    # paths: artifact label -> generated file, for every format that
    # succeeded. failures: artifact label -> truncated samm-cli error, for
    # every format that didn't. A label is always in exactly one of them -
    # unless `skipped`, where generation was deliberately not attempted
    # (no jar) and both are empty; callers report SKIP rather than FAIL for
    # that, as it's no evidence of anything wrong with the model.
    paths: dict[str, Path] = field(default_factory=dict)
    failures: dict[str, str] = field(default_factory=dict)
    skipped: bool = False
    skip_reason: str | None = None


@dataclass
class Context:
    repo_root: Path
    base_branch: str
    _samm_jar: Path | None = field(default=None, init=False, repr=False)
    _samm_jar_resolved: bool = field(default=False, init=False, repr=False)
    _validation_results: dict[str, subprocess.CompletedProcess] = field(default_factory=dict, init=False, repr=False)
    _artifacts: dict[str, Artifacts] = field(default_factory=dict, init=False, repr=False)
    # .ttl files that already exist on base_branch and are modified on this
    # branch (MS2-25). None = not determined in this run.
    modified_ttl_files: list[str] | None = None

    @property
    def samm_jar(self) -> Path | None:
        # Lazily downloads (once per run) the SAMM CLI jar in the version
        # pinned in config.json (see config.py), used by the criteria
        # that need to actually run the CLI (MS2-01 validation, artifact generation for MS2-02/MS2-03).
        if not self._samm_jar_resolved:
            cfg = config.load_config(self.repo_root)
            self._samm_jar = samm_cli.ensure_samm_cli(cfg.samm_cli_version, cfg.samm_cli_sha256)
            self._samm_jar_resolved = True
        return self._samm_jar

    def validation_result(self, model) -> subprocess.CompletedProcess | None:
        # Lazily runs (once per model file, cached for the rest of this
        # run) `samm-cli aspect <file> validate`. Shared between MS2-01
        # (which reports it directly) and ms2_check.py's main loop (which skip further work entirely for a
        # model that doesn't even validate - no point generating artifacts
        # from, or checking naming conventions on, a model that's already
        # known to be broken). Returns None if the jar itself is
        # unavailable (caller can't distinguish "not run" from "ran and
        # passed" any other way).
        if model.file in self._validation_results:
            return self._validation_results[model.file]

        jar = self.samm_jar
        if jar is None:
            return None

        result = samm_cli.run_samm_cli(jar, ["aspect", model.file, "validate"])
        self._validation_results[model.file] = result
        return result

    def generate_artifacts(self, model) -> Artifacts:
        # Generates every format in ARTIFACT_FORMATS for `model` into a
        # fresh temp directory and keeps the result for artifacts() below.
        # Called once per model by ms2_check.py's main loop - only for a
        # model that validates, since nothing gets checked on any other.
        jar = self.samm_jar
        if jar is None:
            result = Artifacts(skipped=True, skip_reason="SAMM CLI jar unavailable (no Java / no network)")
            self._artifacts[model.file] = result
            return result

        out_dir = Path(tempfile.mkdtemp(prefix="ms2-artifacts-"))
        result = Artifacts()
        for label, args in ARTIFACT_FORMATS:
            out_path = out_dir / label
            cli_result = samm_cli.run_samm_cli(jar, ["aspect", model.file, "to", *args, "-o", str(out_path)])
            if cli_result.returncode != 0 or not out_path.exists():
                detail = (cli_result.stderr or cli_result.stdout or f"exit code {cli_result.returncode}").strip()
                result.failures[label] = detail[:300]
            else:
                result.paths[label] = out_path

        self._artifacts[model.file] = result
        return result

    def artifacts(self, model) -> Artifacts:
        # The artifacts generate_artifacts() already produced for `model`.
        # Never generates anything itself - a criterion asking for them
        # before the main loop generated them is a bug in the caller.
        return self._artifacts[model.file]

    def get_changed_files(self) -> list[str]:
        # Returns every file changed on this branch compared to base_branch
        # (not just .ttl files). Assumes `git fetch` has already made
        # base_branch available locally (see the checkout step in
        # governance.yml).
        #
        # Three dots, not two: `A...B` diffs against the merge-base of A
        # and B, i.e. "what did this branch change since it forked from
        # base_branch" - independent of whatever else has landed on
        # base_branch since then. `A..B` (two dots) instead diffs directly
        # against base_branch's current tip, which would also pick up
        # unrelated files simply because base_branch moved on without this
        # branch, misattributing them to this PR.
        #
        # --diff-filter=d excludes deleted paths: a matrix leg checks out a
        # shallow copy of HEAD (see governance.yml), where a deleted file
        # simply doesn't exist any more - parse_model() would just raise
        # FileNotFoundError on it. Deleting a model isn't an MS2 violation
        # to begin with, so it shouldn't get a check (or a crash) at all.
        #
        # A failed git diff (e.g. base_branch was never fetched) is *not*
        # swallowed into an empty list here: that would be indistinguishable
        # from a genuine "no files changed", and would make detect-changed-
        # models silently skip the whole MS2 matrix instead of failing the
        # job - propagate the error so it does fail.
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=d", f"{self.base_branch}...HEAD"],
                capture_output=True, text=True, check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running git diff: {e}", file=sys.stderr)
            raise
        return result.stdout.splitlines()

    def get_changed_ttl_files(self) -> list[str]:
        return [f for f in self.get_changed_files() if f.endswith(".ttl")]

    def get_modified_ttl_files(self) -> list[str]:
        # Like get_changed_ttl_files(), but only files that already existed
        # at the merge-base and were modified (--diff-filter=M).
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=M", f"{self.base_branch}...HEAD"],
                capture_output=True, text=True, check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running git diff: {e}", file=sys.stderr)
            raise
        return [f for f in result.stdout.splitlines() if f.endswith(".ttl")]
