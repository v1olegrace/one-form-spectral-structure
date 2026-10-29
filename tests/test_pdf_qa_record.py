"""The PDF QA record must describe the sources the repository holds.

output/data/canonical_pdf_qa.json stores the SHA-256 of every source the
canonical PDF was built from. The v0.4 record matched the committed blob for
one source in six: it had been generated in a Windows working copy where some
files had been rewritten with LF endings and the rest checked out with CRLF.
Nothing failed. Compare with the current source files, normalizing only CRLF
to LF, so local edits are checked before commit as well as in a clean clone.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "output" / "data" / "canonical_pdf_qa.json"


def _source(path):
    return (ROOT / path).read_bytes().replace(b"\r\n", b"\n")


def _record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def test_record_hashes_are_those_of_the_current_sources():
    rec = _record()
    assert rec["status"] == "PASS"
    expected = {f"paper/{name}" for name in
                ("paper.tex", "appendix.tex", "references.bib", "physofall.bst")}
    expected.update(p.relative_to(ROOT).as_posix()
                    for p in (ROOT / "paper/figures").glob("*.dat"))
    actual = {key.replace("\\", "/") for key in rec["source_sha256"]}
    assert actual == expected, "the QA record must cover the full source inventory"
    for key, digest in rec["source_sha256"].items():
        path = key.replace("\\", "/")
        blob = _source(path)
        assert hashlib.sha256(blob).hexdigest() == digest, (
            f"{path}: the QA record is stale, or was taken from a checkout that "
            "converted line endings")


def test_record_is_for_the_current_draft():
    source = _source("paper/paper.tex")
    version = re.search(rb"Draft (v[\d.]+)", source).group(1).decode()
    assert _record()["draft"] == version


def test_log_warnings_of_every_kind_fail_qa():
    from reproducibility.canonical_pdf_qa import LOG_ISSUE

    log = ("LaTeX Font Warning: Font shape `T1/cmr/m/n' undefined\n"
           "Package pdftex.def Warning: File `x.pdf' not found\n"
           "LaTeX Warning: Citation `x' undefined\n"
           "Overfull \\hbox (1.2pt too wide) in paragraph\n"
           "! Undefined control sequence.\n"
           "Package hyperref Info: not a warning\n")
    assert len(LOG_ISSUE.findall(log)) == 5


def test_source_hash_ignores_checkout_endings_but_detects_content_edits(tmp_path):
    from reproducibility.canonical_pdf_qa import source_digest

    source = tmp_path / "source.tex"
    source.write_bytes(b"hypothesis\npositive measure\n")
    expected = source_digest(source)
    source.write_bytes(b"hypothesis\r\npositive measure\r\n")
    assert source_digest(source) == expected
    source.write_bytes(b"theorem\r\npositive measure\r\n")
    assert source_digest(source) != expected
    source.write_bytes(b"hypothesis\rpositive measure\n")
    assert source_digest(source) != expected
