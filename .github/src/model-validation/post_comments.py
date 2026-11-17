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

# Posts the PR checklist comments saved by ms2_check.py. Run by
# .github/workflows/ms2-comments.yml, which has the write access the
# check run itself lacks for PRs from forks.
#
# Usage (run from the repository root):
#     python .github/src/model-validation/post_comments.py --dir <artifact dir> --head-sha <sha>

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quality_gate import github_comments


def main() -> int:
    parser = argparse.ArgumentParser(description="Posts saved MS2 PR checklist comments.")
    parser.add_argument("--dir", required=True, help="Directory with the downloaded checklist JSON files")
    parser.add_argument("--head-sha", required=True, help="Head commit the checklists were produced for")
    args = parser.parse_args()
    return github_comments.post_saved_checklists(args.dir, args.head_sha)


if __name__ == "__main__":
    sys.exit(main())
