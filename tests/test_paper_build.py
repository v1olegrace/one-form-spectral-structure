"""End-to-end build of the paper, when a LaTeX toolchain is available.

The build must be *clean*, not merely successful: no LaTeX/BibTeX warnings,
no overfull boxes, no undefined references, and no bitmap (Type 3) fonts in
the PDF.  Skipped, never faked, on machines without pdflatex/bibtex.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=300)


def test_figure_data_reproduces_quoted_numbers() -> None:
    """Every number quoted in Section 7 is recomputed and asserted."""
    res = _run([sys.executable, "reproducibility/figure_data.py", "--check"], ROOT)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "all quoted values reproduced" in res.stdout


def test_paper_compiles_cleanly(tmp_path: Path) -> None:
    if not (shutil.which("pdflatex") and shutil.which("bibtex")):
        pytest.skip("pdflatex/bibtex not installed")
    build = tmp_path / "build"
    shutil.copytree(PAPER, build)
    for cmd in (["pdflatex", "-interaction=nonstopmode", "paper"],
                ["bibtex", "paper"],
                ["pdflatex", "-interaction=nonstopmode", "paper"],
                ["pdflatex", "-interaction=nonstopmode", "paper"]):
        res = _run(cmd, build)
        assert res.returncode == 0, f"{cmd[0]} failed:\n{res.stdout[-2000:]}"
    log = (build / "paper.log").read_text(errors="replace")
    problems = re.findall(r"^(?:LaTeX|Package \w+) Warning.*$|^Overfull.*$|^!.*$",
                          log, re.M)
    assert not problems, problems
    blg = (build / "paper.blg").read_text(errors="replace")
    assert "Warning--" not in blg, blg
    if shutil.which("pdffonts"):
        fonts = _run(["pdffonts", "paper.pdf"], build).stdout
        assert "Type 3" not in fonts, "bitmap fonts embedded:\n" + fonts
