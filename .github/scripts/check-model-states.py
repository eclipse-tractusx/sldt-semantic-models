#######################################################################
# Copyright (c) 2025 Catena-X Automotive Network e.V.
# Copyright (c) 2025 Contributors to the Eclipse Foundation
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

import os

import re
import json
import sys
import os, subprocess
from pathlib import Path

def get_changed_ttl_files(base_branch='origin/main'):
    """
    Returns a list of .ttl files changed in the current PR compared to the base branch.
    Assumes that 'git fetch' has been run and that the base branch exists locally.
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', f'{base_branch}..HEAD'],
            capture_output=True, text=True, check=True
        )
        changed_files = result.stdout.splitlines()
        ttl_files = [f for f in changed_files if f.endswith('.ttl')]
        return ttl_files
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []

def parse_prefixes(ttl_path):
    prefixes = []
    prefix_re = re.compile(r'@prefix\s+([\w-]+):\s+<urn:[b|s]amm:([\w\.]+):(\d+\.\d+\.\d+)#>')
    with open(ttl_path) as f:
        for line in f:
            m = prefix_re.search(line)
            if m:
                prefixes.append({
                    'prefix': m.group(1),
                    'folder': m.group(2),
                    'version': m.group(3)
                })
    return prefixes

def check_metadata(folder, version):
    meta_path = Path(folder) / version / 'metadata.json'
    if not meta_path.exists():
        print(f'WARNING: metadata.json not found for {folder}/{version}')
        return None
    with open(meta_path) as f:
        meta = json.load(f)
    return meta

def main():
    warnings = []
    ttl_files = []
    # if 'GITHUB_EVENT_PATH' in os.environ:
    # Get changed files from environment
    ttl_files = get_changed_ttl_files()

    for ttl in ttl_files:
        prefixes = parse_prefixes(ttl)

        for p in prefixes:

            meta = check_metadata(p['folder'], p['version'])
            if not meta:
                print(f"Checking model {p['folder']}:{p['version']} : metadata.json not found")
            else:
                print(f"Checking model {p['folder']}:{p['version']} : "+meta.get('status'))
            
            if not meta or meta.get('status') != 'release':
                warnings.append(f"WARNING: {ttl} imports deprecated or non-existing model ({p['folder']}:{p['version']})")
    if warnings:
        for w in warnings:
            print(w)
        sys.exit(1)
    else:
        print('No deprecated models imported.')

if __name__ == '__main__':
    main()
