#!/usr/bin/env python
"""Portable build driver.

GNU make is not present in this environment (Git-Bash on Windows), so the
Makefile cannot be executed here.  This script provides the same targets with
no external dependency beyond Python:

    python make.py test      run the full test suite
    python make.py numerics  regenerate all numerical results and figures
    python make.py bib       re-harvest metadata and rebuild references.bib
    python make.py audit     rebuild the audit ledgers
    python make.py pdf       compile paper/paper.pdf (requires a LaTeX toolchain)
    python make.py all       numerics + audit + test
    python make.py check     report which external tools are available

``pdf`` reports a clear, non-zero failure if no LaTeX engine is installed
rather than pretending to succeed.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LATEX_ENGINES = ["latexmk", "pdflatex", "xelatex", "lualatex", "tectonic"]


def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    return subprocess.call([str(c) for c in cmd], cwd=str(cwd))


def target_test():
    return run([sys.executable, "-m", "pytest", "tests", "-q"])


def target_numerics():
    rc = 0
    for script in ["reproducibility/extended_analysis.py",
                   "reproducibility/falsification_suite.py",
                   "reproducibility/interval_bounds.py"]:
        path = ROOT / script
        if not path.exists():
            print(f"  skip (absent): {script}")
            continue
        rc |= run([sys.executable, path.name], cwd=path.parent)
    return rc


def target_bib():
    rc = run([sys.executable, "scripts/literature_harvester.py"])
    rc |= run([sys.executable, "scripts/build_bibliography.py"])
    return rc


def target_audit():
    return run([sys.executable, "scripts/build_audit_tables.py"])


def target_pdf():
    engine = next((e for e in LATEX_ENGINES if shutil.which(e)), None)
    if engine is None:
        print("\nERROR: no LaTeX engine found.")
        print("  Looked for: " + ", ".join(LATEX_ENGINES))
        print("  paper/paper.tex cannot be compiled in this environment.")
        print("  Install TeX Live or MiKTeX, or run `python make.py pdf` elsewhere.")
        print("  Structural validation is still available: "
              "python -m pytest tests/test_latex_structure.py")
        return 2
    paper = ROOT / "paper"
    if engine == "latexmk":
        return run([engine, "-pdf", "-interaction=nonstopmode", "paper.tex"], cwd=paper)
    if engine == "tectonic":
        return run([engine, "paper.tex"], cwd=paper)
    rc = run([engine, "-interaction=nonstopmode", "paper.tex"], cwd=paper)
    rc |= run(["bibtex", "paper"], cwd=paper)
    rc |= run([engine, "-interaction=nonstopmode", "paper.tex"], cwd=paper)
    rc |= run([engine, "-interaction=nonstopmode", "paper.tex"], cwd=paper)
    return rc


def target_check():
    print("External tool availability in this environment:")
    for tool in LATEX_ENGINES + ["bibtex", "make", "git", "quarto"]:
        where = shutil.which(tool)
        print(f"  {tool:12s} {where or 'NOT FOUND'}")
    print("\nPython packages:")
    for pkg in ["mpmath", "numpy", "scipy", "sympy", "matplotlib", "pytest"]:
        try:
            mod = __import__(pkg)
            print(f"  {pkg:12s} {getattr(mod, '__version__', 'present')}")
        except ImportError:
            print(f"  {pkg:12s} NOT INSTALLED")
    return 0


def target_all():
    rc = target_numerics()
    rc |= target_audit()
    rc |= target_test()
    return rc


TARGETS = {"test": target_test, "numerics": target_numerics, "bib": target_bib,
           "audit": target_audit, "pdf": target_pdf, "all": target_all,
           "check": target_check}


def main(argv):
    name = argv[1] if len(argv) > 1 else "all"
    fn = TARGETS.get(name)
    if fn is None:
        print(f"unknown target {name!r}; choose from {', '.join(sorted(TARGETS))}")
        return 2
    rc = fn()
    print(f"\n[{name}] exit status {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
