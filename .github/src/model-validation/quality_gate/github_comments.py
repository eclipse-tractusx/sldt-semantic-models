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
# Posts one PR *issue* comment per checked model file, listing every
# FAIL/WARN finding from criteria that opt in via POST_COMMENT = True (see
# criteria/__init__.py) as a Markdown checklist.
#
# Deliberately an issue comment (POST/PATCH .../issues/{pr}/comments), not
# a *review* comment anchored to a diff line: an earlier version tried the
# latter, but GitHub's review-comment API only accepts lines that are part
# of the PR's diff - a FAIL on an untouched line (e.g. pre-existing model
# content that wasn't part of this PR) would then silently fail to post.
# One issue comment per model sidesteps that entirely (no diff-line
# constraint) and is also simpler to keep in sync: since there's at most
# one comment per model, a re-run can just PATCH it in place instead of
# juggling "does a comment for this exact finding already exist".
#
# Stdlib-only (urllib), matching the rest of this package's "no external
# dependencies beyond the optional jsonschema check" approach.
#
# Silently does nothing (prints a one-line note instead) whenever posting
# isn't possible or doesn't make sense, rather than failing the check run:
#   - not running on a `pull_request` event (e.g. local run, push, schedule)
#   - no GITHUB_TOKEN available, or the token lacks `pull-requests: write`
#   - no findings to report for this model (nothing to post/update) - an
#     existing comment from a previous, now-fixed run is left as-is rather
#     than being deleted (deleting needs a separate `delete` call; a stale
#     "all clear now" comment is a minor cosmetic issue, not a correctness
#     one, so that's left for a future version)
#
# A human can "Hide" (minimize) the comment on GitHub - that doesn't delete
# it (still found and PATCHed on the next run), it just keeps sitting there
# collapsed even after the edit. An earlier version of this module tried to
# auto-un-hide it via the GraphQL `unminimizeComment` mutation (REST has no
# equivalent), but that mutation reliably fails for the Actions-provided
# GITHUB_TOKEN ("Resource not accessible by integration" - a known GitHub
# limitation, not a bug here) - fixing it for real would need a PAT stored
# as a repo secret, not worth it for this. Whether something is still
# actually open is always visible from the check run status itself anyway.

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

from .report import Finding, ICON

API_ROOT = "https://api.github.com"
HIDDEN_MARKER = "<!-- ms2-check:{path} -->"


@dataclass(frozen=True)
class PRContext:
    owner: str
    repo: str
    pull_number: int


def _pr_context() -> PRContext | None:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return None
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    repo_slug = os.environ.get("GITHUB_REPOSITORY")
    if not event_path or not repo_slug:
        return None
    try:
        event = json.loads(open(event_path, encoding="utf-8").read())
        owner, repo = repo_slug.split("/", 1)
        return PRContext(owner=owner, repo=repo, pull_number=event["pull_request"]["number"])
    except (OSError, json.JSONDecodeError, KeyError):
        return None


def _api_request(method: str, path: str, token: str, body: dict | None = None) -> tuple[int, object]:
    url = f"{API_ROOT}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        # Network hiccup / GitHub outage / unexpected non-JSON response -
        # comment posting is a nice-to-have on top of the actual MS2 check,
        # never a reason to fail (or hang) the whole run over it.
        return 0, {"message": str(e)}


def _find_existing_comment(pr: PRContext, token: str, marker: str) -> int | None:
    status, payload = _api_request(
        "GET", f"/repos/{pr.owner}/{pr.repo}/issues/{pr.pull_number}/comments?per_page=100", token)
    if status != 200 or not isinstance(payload, list):
        return None
    for comment in payload:
        if marker in comment.get("body", ""):
            return comment["id"]
    return None


def _render_checklist(model_file: str, findings: list[Finding], marker: str) -> str:
    lines = [marker, f"### MS2 Criteria issues — `{model_file}`", ""]
    for finding in findings:
        loc = f"{finding.file}:{finding.line}" if finding.line is not None else finding.file
        lines.append(f"- [ ] {ICON[finding.level]} **{finding.criterion_id}** ({loc}) — {finding.message}")
    return "\n".join(lines)


def post_checklist_comment(model_file: str, findings: list[Finding]) -> None:
    if not findings:
        return

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(f"{model_file}: GITHUB_TOKEN not set - skipping PR checklist comment")
        return

    pr = _pr_context()
    if pr is None:
        # Expected for local runs and non-PR CI triggers - not worth a log line.
        return

    marker = HIDDEN_MARKER.format(path=model_file)
    body = _render_checklist(model_file, findings, marker)
    existing_id = _find_existing_comment(pr, token, marker)

    if existing_id is not None:
        status, payload = _api_request(
            "PATCH", f"/repos/{pr.owner}/{pr.repo}/issues/comments/{existing_id}", token, body={"body": body})
    else:
        status, payload = _api_request(
            "POST", f"/repos/{pr.owner}/{pr.repo}/issues/{pr.pull_number}/comments", token, body={"body": body})

    if status not in (200, 201):
        message = payload.get("message", payload) if isinstance(payload, dict) else payload
        print(f"{model_file}: could not post/update MS2 checklist PR comment: {message}")
