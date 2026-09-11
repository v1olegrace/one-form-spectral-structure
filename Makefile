# Build targets. GNU make is absent in the reference environment (Git-Bash on
# Windows); use `python make.py <target>` there. The targets are identical.

PY ?= python

.PHONY: all test numerics bib audit pdf check clean

all: numerics audit test

test:
	$(PY) -m pytest tests -q

numerics:
	cd reproducibility && $(PY) extended_analysis.py
	cd reproducibility && $(PY) falsification_suite.py
	cd reproducibility && $(PY) interval_bounds.py

bib:
	$(PY) scripts/literature_harvester.py
	$(PY) scripts/build_bibliography.py

audit:
	$(PY) scripts/build_audit_tables.py

# Fails loudly if no LaTeX engine is installed, rather than pretending to work.
pdf:
	@command -v latexmk >/dev/null 2>&1 || command -v pdflatex >/dev/null 2>&1 || \
	  { echo "ERROR: no LaTeX engine (latexmk/pdflatex) found; cannot build paper/paper.pdf"; exit 2; }
	cd paper && latexmk -pdf -interaction=nonstopmode paper.tex

check:
	$(PY) make.py check

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg *.fls *.fdb_latexmk paper.pdf
