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
# Helper around the SAMM CLI jar.
#
# Mirrors the download logic and the command set already used in
# ``scripts/generate.sh`` (``aspect <file> validate`` / ``aspect <file> to
# <format>``), just ported to Python so the MS2 criteria that need the CLI
# (MS2-01 validation, artifact generation for MS2-02/MS2-03) can shell out to it too.

from __future__ import annotations

import hashlib
import shutil
import subprocess
import urllib.request
from pathlib import Path

CACHE_DIR = Path(".SAMMCLI")


class ChecksumMismatch(Exception):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify(path: Path, expected_sha256: str) -> None:
    actual = _sha256(path)
    if actual != expected_sha256:
        raise ChecksumMismatch(f"{path}: SHA-256 {actual} does not match pinned {expected_sha256}")


def ensure_samm_cli(version: str, sha256: str, cache_dir: Path = CACHE_DIR) -> Path | None:
    # Returns None only when Java itself isn't installed (a legitimate,
    # expected state for local/manual runs, tolerated so the criteria
    # needing the CLI can SKIP gracefully instead of failing the whole
    # run). A download failure is not caught here - it's left to propagate
    # and fail the run, same as any other unexpected error.
    cache_dir.mkdir(parents=True, exist_ok=True)
    jar_path = cache_dir / f"samm-cli-{version}.jar"

    if jar_path.exists():
        _verify(jar_path, sha256)
        return jar_path

    if shutil.which("java") is None:
        return None

    url = f"https://github.com/eclipse-esmf/esmf-sdk/releases/download/v{version}/samm-cli-{version}.jar"
    tmp_path = jar_path.with_suffix(".jar.part")
    urllib.request.urlretrieve(url, tmp_path)
    try:
        _verify(tmp_path, sha256)
    except ChecksumMismatch:
        tmp_path.unlink(missing_ok=True)
        raise
    tmp_path.replace(jar_path)
    return jar_path


def run_samm_cli(jar_path: Path, args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    command = ["java", "-Dpolyglot.engine.WarnInterpreterOnly=false", "-jar", str(jar_path), *args]
    return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
