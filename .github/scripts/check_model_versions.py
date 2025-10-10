import os
import re
import json
import sys
from pathlib import Path

def get_changed_ttl_files():
    # Get list of changed files from GITHUB_EVENT_PATH
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        print('GITHUB_EVENT_PATH not found, cannot determine changed files.')
        return []
    with open(event_path) as f:
        event = json.load(f)
    files = []
    for file in event.get('pull_request', {}).get('files', []):
        if file['filename'].endswith('.ttl'):
            files.append(file['filename'])
    # Fallback: use git diff if event doesn't contain files
    if not files:
        import subprocess
        result = subprocess.run(['git', 'diff', '--name-only', 'origin/main...HEAD'], capture_output=True, text=True)
        files = [f for f in result.stdout.splitlines() if f.endswith('.ttl')]
    return files

def parse_prefixes(ttl_path):
    prefixes = []
    prefix_re = re.compile(r'@prefix\s+([\w-]+):\s+<urn:samm:([\w\.]+):(\d+\.\d+\.\d+)#>')
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
    # Try to get changed files from environment
    if 'GITHUB_EVENT_PATH' in os.environ:
        ttl_files = get_changed_ttl_files()
    else:
        # Local fallback: check all ttl files
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.ttl'):
                    ttl_files.append(os.path.join(root, file))
    for ttl in ttl_files:
        prefixes = parse_prefixes(ttl)
        for p in prefixes:
            meta = check_metadata(p['folder'], p['version'])
            if meta and meta.get('deprecated'):
                warnings.append(f"WARNING: {ttl} imports deprecated model {p['folder']}:{p['version']}")
    if warnings:
        for w in warnings:
            print(w)
        sys.exit(1)
    else:
        print('No deprecated models imported.')

if __name__ == '__main__':
    main()
