"""Control characters in source text.

A shell here-document can reduce a doubled backslash to a single one before a
script sees it. In a Python string, a single backslash before r, v, a, b, f or n
is then an escape: "\\ref" becomes a carriage return followed by "ef", "\\v{c}"
a vertical tab. LaTeX and BibTeX accept the damaged file silently, or render a
missing letter. Every such character in these files has been an accident.

A carriage return is allowed only as the first half of a CRLF line ending.

Only files tracked by git are scanned, so a working copy with private notes
runs the same tests as a clean checkout. Without git, every matching file is.
"""
from __future__ import annotations

import subprocess
import unicodedata
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _tracked():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True,
                             capture_output=True, timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return {ROOT / p for p in out.decode("utf-8").split("\0") if p}


_CANDIDATES = [
    *ROOT.glob("paper/*.tex"), ROOT / "paper" / "references.bib",
    *ROOT.glob("*.md"), *ROOT.glob("notes/*.md"), *ROOT.glob("notes/*.tex"),
    *ROOT.glob("reports/*.md"), *ROOT.glob("scripts/*.py"),
    *ROOT.glob("reproducibility/*.py"),
    *ROOT.glob("reports/h3_ghost_2026-09-29/*.py"),
    *ROOT.glob("output/impressao_professor_2026-09-28/fontes_tex/*.tex")]
_TRACKED = _tracked()
FILES = sorted(p for p in _CANDIDATES if _TRACKED is None or p in _TRACKED)


def _defects(text):
    out = []
    for i, ch in enumerate(text):
        if ch == "\r":
            if text[i + 1:i + 2] != "\n":
                out.append((i, "stray CR"))
        elif ch in "\n\t":
            continue
        elif unicodedata.category(ch) == "Cc":
            out.append((i, repr(ch)))
    return out


def test_the_scan_catches_what_it_is_for():
    assert _defects("see Hypothesis~\ref{hyp}") == [(15, "stray CR")]
    assert _defects("Vondra{\v{c}}ek")[0][1] == repr("\v")
    assert _defects("line one\r\nline two\n") == []


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_control_characters(path):
    text = path.read_text(encoding="utf-8", errors="strict")
    bad = _defects(text)
    if bad:
        pos, kind = bad[0]
        line = text.count("\n", 0, pos) + 1
        pytest.fail(f"{len(bad)} control character(s); first is {kind} on line {line}")
