# `output/` — generated artefacts

Apart from this index, numerical artefacts are produced by scripts in
[`reproducibility/`](../reproducibility) or [`scripts/`](../scripts), and every
numerical file can be regenerated. A discrepancy between a script and the
paper requires investigation; neither is an authority merely by existing.

```
output/
  data/               numerical results (tracked)
  figures/            plots, PNG + SVG (tracked)
  certified_one_loop/ Arb-validated one-loop benchmark (NOT tracked)
  html/               historical Quarto renders (NOT tracked)
  pdf/                canonical v0.3 PDF plus historical Quarto PDFs (NOT tracked)
```

---

## Status vocabulary

The distinction is enforced by module boundary, not by convention.

| Label | Meaning |
|---|---|
| `CERTIFIED` | A rigorous interval enclosure or a proved inequality. Rounding error is controlled. |
| `CHECKED` | High-precision numerics with no rigorous error bound. `mp.quad` lands here no matter how many digits agree. |
| `PENDING_VERIFICATION` | Never guessed, never silently filled. |

A randomised perturbation trial is a **test**, not a certificate. It is labelled
`CHECKED` even when all 200 trials pass.

---

## What writes what

### `data/` — tracked

| File | Written by |
|---|---|
| `extended_verification.json`, `sampled_hierarchy.csv`, `robust_sampled_bounds.csv` | `extended_analysis.py` |
| `falsification_suite.json` | `falsification_suite.py` |
| `interval_bounds.json` | `interval_bounds.py` |
| `laplace_geometry_certification.json` | `laplace_geometry.py` |
| `dirac_moment_ratios.csv`, `localizing_bounds.csv`, `uncertainty_summary.json`, `verification_checks.json` | `analysis.py` |
| `pdf_qa.json` | `pdf_qa.py` |
| `canonical_pdf_qa.json` | `canonical_pdf_qa.py` (canonical paper, source/PDF hashes) |

### `figures/` — tracked

| File | Written by |
|---|---|
| `hidden_threshold.{png,svg}`, `sampled_hierarchy.{png,svg}` | `extended_analysis.py` |
| `dirac_ratio_convergence.{png,svg}`, `localizing_bound_convergence.{png,svg}` | `analysis.py` |

These are **not** the paper's figures. Figure 1 of `paper/paper.tex` is drawn by
pgfplots at compile time from `paper/figures/*.dat`, which
`reproducibility/figure_data.py` generates.

**Precision provenance of these non-canonical artefacts.**
`dirac_ratio_convergence` and `localizing_bounds.csv` / `localizing_bound_convergence`
come from `analysis.py`, which handles the **Stieltjes** pencil
(negative-power moments, H₁ as denominator) — the opposite orientation to the
Laplace pencil of the paper. The bound values are computed at 120 decimal
digits; `localizing_bounds.csv` records, per row, the gate status, the digits
the denominator actually requires (1 to 13 at K = 0..5) and the discrepancy of
the former double-precision route (at most 5.9e-12). So the double precision
that was used before turns out to have been adequate *for this pencil at this
order* — but that is now a measured statement with a refusal path, not an
assumption. It does not weaken the separate statement in `paper/paper.tex`
about the Laplace pencil, where a wide-dynamic-range model needs about 86
digits. `sampled_hierarchy` comes from `extended_analysis.py` at 60 dps and is
`CHECKED`; the `CERTIFIED` derivative-free bounds live in
`certified_one_loop/`, not here.

### `certified_one_loop/` — not tracked

Written by `run_one_loop_certificates.py` (`python make.py certified`), which
needs `python-flint` (Arb). Roughly 4.5 MB, dominated by `comparison.json` and
`weight_certificates.json`. Gitignored because it regenerates deterministically
and `summary.json` carries a `configuration_sha256` that pins the inputs.
`verify_one_loop_output.py` re-verifies it independently of the run that
produced it.

---

## Current validation — 23 Sep 2026

Numerical outputs and figures were regenerated; historical Quarto PDFs and
their `pdf_qa.json` were not used as evidence for the canonical paper.

| Step | Command | Result |
|---|---|---|
| Numerics and audit ledgers | `python make.py numerics`, `python make.py audit` | exit 0 (run twice; all four SVG byte-identical on repeat) |
| Test suite | `python -m pytest tests -q` with Tectonic on PATH | **169 passed, no skips** |
| Validated one-loop benchmark | `python make.py certified` | exit 0, `configuration_sha256` unchanged |
| Independent re-verification | `python reproducibility/verify_one_loop_output.py --reintegrate --no-write` | `PASS`, 28 distinct samples, 12 benchmarks, cardinalities and index bijection checked |
| Paper's quoted numbers | `python reproducibility/figure_data.py --check` | all reproduced |
| Canonical PDF still described by its QA record | source and PDF SHA-256 vs `data/canonical_pdf_qa.json` | all 6 source hashes and the PDF hash match; no rebuild needed |

**Headline results**

- `interval_bounds.py` — 5 `CERTIFIED` atomic enclosures, 5 `CHECKED` numerical
  checks, 0 failures.
- `run_one_loop_certificates.py` — 12 datasets; **40 source-enclosure
  evaluations representing 28 distinct inputs**, plus 12 direct weight-benchmark
  integrals and 40 independent mpmath cross-checks, all counted separately
  (`counter_scope` in `summary.json` says so: no single counter is the total
  number of quadratures performed). 144 comparison rows, **288 exact weight
  certificates, all verified**; 113 rows with a positive weight lower bound and
  24 where the hierarchy correctly returns no bound.
  `configuration_sha256` = `b4b178b9…`
- `verify_one_loop_output.py` — every counter above is recomputed from the data,
  the comparison table must equal datasets × degrees × cutoffs, and the
  certificate indices must be a bijection. Presence is no longer mistaken for
  completeness: a dropped row or a reused certificate index is refused.
- `laplace_geometry.py` — all numerical checks passed (`CHECKED`, not certified),
  now including the shared finite moment conditions at every reported
  (r, K); the per-row `gate_status`, `min_eig_H0` and `min_eig_H1` are in
  `laplace_geometry_certification.json`.
- `extended_analysis.py` — 70 checks passed (52 before; the 18 new ones are the
  finite moment conditions on the sampled Hausdorff pencil).
- `analysis.py` — the Stieltjes localizing bound is computed at 120 dps. The
  precision requirement is now measured rather than assumed: the denominator
  matrix needs 1 to 13 digits at K = 0..5 and the former float64 route differed
  by at most 5.9e-12, both recorded per row in `localizing_bounds.csv`. The
  opposite pencil orientation is declared explicitly (`strict_shift=1`).
- `falsification_suite.py` — 21 checks passed, including the missing-localizer
  counterexample, mandatory bound-level checking, a finite-order false negative
  and singular positive measures.
- `figure_data.py --check` — r× = 22.7583, a₃(1) = −0.1735, det H₀(1) = −0.0249,
  rescaled −0.4715 and −0.1839.
- Audit ledgers — `literature_audit.csv` 17 rows, `claims_matrix.csv` 8 rows,
  `theorem_status.csv` 11 rows.

**Environment**

Python 3.13.7 on Windows 11 · mpmath 1.3.0 · numpy 2.3.5 · scipy 1.15.3 ·
sympy 1.13.1 · matplotlib 3.10.3 · pytest 8.4.1 · python-flint 0.9.0.

The canonical PDF is `pdf/spectral_structure_v03.pdf` (12 pages), built with
portable Tectonic 0.17.0. Its LaTeX/BibTeX logs have no warnings or overfull
boxes; fonts are Type0/Type1. Structural QA is in `data/canonical_pdf_qa.json`.
All pages were visually inspected separately; the script itself does not
claim visual approval.

---

## Regenerating

```bash
python make.py all         # numerics + audit ledgers + test suite
python make.py certified   # Arb-validated one-loop benchmark (needs python-flint)
python make.py check       # report toolchain availability
```

`make.py numerics` (and therefore `make.py all`) runs `analysis.py`,
`laplace_geometry.py`, `extended_analysis.py`, `falsification_suite.py`,
`interval_bounds.py` and `figure_data.py --check`, about 50 s in total.
`pdf_qa.py` is deliberately excluded: it checks the Quarto render of the
non-canonical pt-BR draft. To re-integrate every certified source sample
with Arb:

```bash
python reproducibility/verify_one_loop_output.py --reintegrate
# Add --no-write for a read-only verification.
```

---

## PDF checks and reproducibility scope

- **SVG stability fixed:** `svg.hashsalt` is pinned, dates omitted and trailing
  whitespace normalized. All four outputs matched on repeat in this environment.
- **Historical Quarto outputs remain historical.** Their `pdf_qa.json` says
  nothing about `paper/paper.tex`; use `canonical_pdf_qa.json` for the new PDF.
- Canonical QA uses optional `PyMuPDF`. For a standard `python make.py pdf`
  build, run `python reproducibility/canonical_pdf_qa.py --render-dir tmp/pdfs/review`.
  For a PDF built elsewhere, supply `--pdf` and `--log` explicitly.
- A `CHECKED_COMPATIBLE` gate result is not an H3 certificate. Interval/dual
  certificates assume valid data enclosures and the stated positive measure.
- The gate lives in `reproducibility/moment_conditions.py` and is imported by
  every routine that emits a bound, so a refusal cannot be avoided by calling a
  sibling module. Its two refusal statuses stay distinct:
  `CHECKED_INCOMPATIBLE` (a tested necessary condition is violated) versus
  `UNRESOLVED_RANK_OR_PRECISION` (singular pencil or insufficient digits — not
  a refutation of H3).
