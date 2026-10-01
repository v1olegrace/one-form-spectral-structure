"""The PDF QA record must describe the sources the repository holds.

output/data/canonical_pdf_qa.json stores the SHA-256 of every source the
canonical PDF was built from. The v0.4 record matched the committed blob for
one source in six: it had been generated in a Windows working copy where some
files had been rewritten with LF endings and the rest checked out with CRLF.
Nothing failed. This test compares the record with the blobs git stores, so a
stale or mixed record now fails; regenerate it from an LF checkout.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "output" / "data" / "canonical_pdf_qa.json"


def _blob(path):
    try:
        out = subprocess.run(["git", "cat-file", "blob", f"HEAD:{path}"], cwd=ROOT,
                             capture_output=True, check=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout


def _record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_record_hashes_are_those_of_the_committed_sources():
    rec = _record()
    assert rec["status"] == "PASS"
    checked = 0
    for key, digest in rec["source_sha256"].items():
        path = key.replace("\\", "/")
        blob = _blob(path)
        if blob is None:
            pytest.skip("git is not available, so there are no blobs to compare with")
        assert hashlib.sha256(blob).hexdigest() == digest, (
            f"{path}: the QA record is stale, or was taken from a checkout that "
            "converted line endings")
        checked += 1
    assert checked >= 6


def test_record_is_for_the_current_draft():
    source = _blob("paper/paper.tex")
    if source is None:
        pytest.skip("git is not available")
    version = re.search(rb"Draft (v[\d.]+)", source).group(1).decode()
    assert _record()["draft"] == version
