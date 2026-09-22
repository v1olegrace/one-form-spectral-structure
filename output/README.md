# `output/` — generated artefacts

Nothing here is written by hand. Every file is produced by a script in
[`reproducibility/`](../reproducibility) or [`scripts/`](../scripts), and every
file can be deleted and regenerated. If a number in the paper disagrees with a
number here, the script is the authority, not the text.

```
output/
  data/               numerical results (tracked)
  figures/            plots, PNG + SVG (tracked)
  certified_one_loop/ Arb-validated one-loop benchmark (NOT tracked)
  html/  pdf/         Quarto renders of the pt-BR working draft (NOT tracked)
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

### `figures/` — tracked

| File | Written by |
|---|---|
| `hidden_threshold.{png,svg}`, `sampled_hierarchy.{png,svg}` | `extended_analysis.py` |
| `dirac_ratio_convergence.{png,svg}`, `localizing_bound_convergence.{png,svg}` | `analysis.py` |

These are **not** the paper's figures. Figure 1 of `paper/paper.tex` is drawn by
pgfplots at compile time from `paper/figures/*.dat`, which
`reproducibility/figure_data.py` generates.

### `certified_one_loop/` — not tracked

Written by `run_one_loop_certificates.py` (`python make.py certified`), which
needs `python-flint` (Arb). Roughly 4.5 MB, dominated by `comparison.json` and
`weight_certificates.json`. Gitignored because it regenerates deterministically
and `summary.json` carries a `configuration_sha256` that pins the inputs.
`verify_one_loop_output.py` re-verifies it independently of the run that
produced it.

---

## Last full run — 21 Sep 2026

Everything in `data/` and `figures/` was regenerated in this run.

| Step | Command | Result |
|---|---|---|
| Numerics + audit + tests | `python make.py all` | exit 0 |
| Test suite | (within `all`) | **86 passed, 1 skipped** |
| Validated one-loop benchmark | `python make.py certified` | exit 0 |
| Independent re-verification | `python reproducibility/verify_one_loop_output.py` | `PASS` |
| Paper's quoted numbers | `python reproducibility/figure_data.py --check` | all reproduced |

**Headline results**

- `interval_bounds.py` — 5 `CERTIFIED` atomic enclosures, 5 `CHECKED` numerical
  checks, 0 failures.
- `run_one_loop_certificates.py` — 12 datasets, 40 unique raw integrals, 144
  comparison rows, **288 exact weight certificates, all verified**; 113 rows
  with a positive weight lower bound and 24 where the hierarchy correctly
  returns no bound. `configuration_sha256` = `b4b178b9…`
- `laplace_geometry.py` — all certified assertions passed.
- `figure_data.py --check` — r× = 22.7583, a₃(1) = −0.1735, det H₀(1) = −0.0249,
  rescaled −0.4715 and −0.1839.
- Audit ledgers — `literature_audit.csv` 17 rows, `claims_matrix.csv` 8 rows,
  `theorem_status.csv` 11 rows.

**Environment**

Python 3.13.7 on Windows 11 · mpmath 1.3.0 · numpy 2.3.5 · scipy 1.15.3 ·
sympy 1.13.1 · matplotlib 3.10.3 · pytest 8.4.1 · python-flint 0.9.0.

No LaTeX engine is installed here, so `paper/paper.pdf` was not built and
`tests/test_paper_build.py` is the one skipped test.

---

## Regenerating

```bash
python make.py all         # numerics + audit ledgers + test suite
python make.py certified   # Arb-validated one-loop benchmark (needs python-flint)
python make.py check       # report toolchain availability
```

`make.py all` runs `extended_analysis.py`, `falsification_suite.py` and
`interval_bounds.py` only. **It does not run** `analysis.py`,
`laplace_geometry.py`, `figure_data.py` or `pdf_qa.py`, so four `data/` files and
two figure pairs go stale unless those are run directly:

```bash
cd reproducibility && python analysis.py && python laplace_geometry.py
python reproducibility/figure_data.py --check
```

---

## Known issues

- **SVG output is not byte-reproducible.** Re-running an unchanged script
  rewrites every tracked `.svg`, because matplotlib stamps a `<dc:date>` and
  regenerates random element ids. The plotted data is identical — verified by
  diffing after normalising the date and the ids — but the files churn in git on
  every run. The PNGs do not. Fixing this means pinning `svg.hashsalt` and
  suppressing the date in metadata.
- **`html/` and `pdf/` are stale** (10 Sep 2026) and render the pt-BR Quarto
  working draft in `manuscript/`, which is **not** the canonical manuscript.
  `pdf_qa.json` reports `all_checks_pass` against that non-canonical PDF, so it
  says nothing about `paper/paper.tex`.
