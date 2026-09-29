# Final Remediation Report

Branch `remediation/priority-audit` · 8 commits · 86 files changed
(+4526 / −120) · 2026-09-11

---

## Executive summary

The nine mandatory scientific corrections were **already implemented by the
author** in a rewrite of `manuscript/apendice_geometria_laplace.qmd` that landed
between the audit prompt and this run. That rewrite is more careful than the
version the audit was written against: it defines $\nu$ by weighted
pushforward, states H3 conditionally on a linear-response kernel, carries the
explicit screening sign, separates complete monotonicity from H3 with two
counterexamples, and adds Theorems F–H and a Mellin bridge. Remediation
therefore **verified** each correction rather than re-litigating it, and spent
its effort where the work was genuinely missing: falsification, priority, and
reproducible infrastructure.

Two findings dominate the outcome.

**The adversarial priority audit substantially reduced the novelty claim.** The
lattice-QCD effective-mass and GEVP technology is mathematically identical to
Theorems C and E — a positive Euclidean correlator, a monotone one-sided bound
on the lowest state, a refining generalized-eigenvalue hierarchy. Threshold
extraction from vacuum-polarization moments already exists (Masjuan–Peris,
via the Padé–Stieltjes–Hankel equivalence). Bachas obtains two derivative
conditions on the static potential from reflection positivity *alone*, a
strictly weaker hypothesis than H3. Claims C2, C3 and C4 were downgraded to
`CLASSICAL_APPLICATION`. What survives is the assembly, not the method.

**The two adversarial tests the author specified both behaved as predicted, and
neither was FATAL.** The positivity gate refuses a signed measure — while a
screening-only diagnostic is fooled by it, which is the strongest available
argument that the infinite hierarchy is operationally useful. A measure with
$10^{-12}$ of weight at the true edge does not produce a wrong answer; it
produces an uninformative one until the predicted crossover radius $22.76$,
confirmed numerically. That is now a stated limitation with Theorem H as its
formal content.

---

## 1. Completed phases

| Phase | Scientific acceptance criterion | Closed by |
|---|---|---|
| 0 forensics | every path classified; caches untracked; nothing deleted | `data/repository_forensics.csv` (62 rows); 72.9 MB excluded; guard in CI |
| 1 sign convention | derived from the quadratic effective action; three checks; discriminating test | `paper/appendix.tex` §A; `tests/test_sign_convention.py` (9 tests) — flipped convention **must** give $d\sigma<0$ |
| 2 Wilson-loop observable | no "gauge-invariant propagator" language; $r$-independence of the perimeter term stated | verified by grep; `paper/paper.tex` §2 |
| 3 Laplace construction | exact identity under H3, separated from the perturbative expansion | Theorem 1 + Remark; kernel identity verified symbolically and numerically |
| 4 structure | CM, $\Gamma=\langle x\rangle_r$, $\Gamma'=-\mathrm{Var}$, convergence conditions | Theorems C; 17 tests in `test_measure_and_hierarchy.py` |
| 5 edge law | Watson applied separately to numerator and denominator; QED verified | spinor $p\to1.4981$ vs $3/2$; scalar $\to2.4904$ vs $5/2$ |
| 6 Hankel | Rayleigh first, then bound/monotonicity, then determinacy, then edge convergence | `paper/appendix.tex` §B; conditioning quantified (86 digits needed vs 16 in float64) |
| 7 priority audit | HIGH/MEDIUM threats identified with exact overlap and difference | `data/literature_audit.csv` (17 rows); 3 HIGH, 4 MEDIUM |
| 8 harvesting | structured APIs, caching, backoff, no fabricated fields | `scripts/literature_harvester.py`; 18 records; 9 fields `PENDING_VERIFICATION` |
| 9 bibliography | academic sources only; identifiers; provenance | `paper/references.bib`; `tests/test_bibliography.py` (7 tests) |
| 10 paper | English LaTeX, restrained, conditional abstract | `paper/paper.tex` + `appendix.tex`; 10 structural/honesty tests |
| 11 numerics | model zoo incl. signed and tiny-weight; interval subset | 79 numerical checks across three scripts; **A–H, J, K done; I partial; L, M, N not implemented** |
| 12 testing | `make test` passes | 44 tests, exit 0 |
| 13 red team | no unresolved FATAL | `RED_TEAM_REPORT.md`: 4 FATAL all resolved |
| 14 QA | this report | below |

**Not complete:** `make pdf` and CI — see blockers.

## 2. Commits

| Hash | Subject |
|---|---|
| `e2859ee` | chore: initialise repository and quarantine generated artifacts |
| `f60a459` | test: add adversarial falsification suite and spectral model zoo |
| `dc55404` | research: adversarial priority audit finds three HIGH threats |
| `be1ee0a` | bibliography: verified references.bib, sign-convention proof, validation tests |
| `62be930` | manuscript: English LaTeX paper, appendix, and interval-certified bounds |
| `18994e0` | ci: portable build driver, Makefile, workflow and repository metadata |

## 3. Principal files

**Created:** `paper/{paper.tex,appendix.tex,references.bib}`;
`reproducibility/{spectral_models,falsification_suite,interval_bounds}.py`;
`tests/{test_sign_convention,test_measure_and_hierarchy,test_bibliography,test_latex_structure}.py`;
`scripts/{literature_harvester,build_bibliography,build_audit_tables}.py`;
`data/{repository_forensics,literature_audit,claims_matrix,theorem_status,literature_harvest}.csv`;
`make.py`, `Makefile`, `.github/workflows/tests.yml`, `README.md`,
`REMEDIATION_LOG.md`, `RED_TEAM_REPORT.md`, `CITATION.cff`, `LICENSE`.

**Preserved unmodified:** `manuscript/*.qmd` and
`reproducibility/{analysis,laplace_geometry,extended_analysis,pdf_qa}.py` — the
author's active work. `tmp/revision_before/` (their backup) is kept on disk and
untracked.

## 4. Scientific corrections

Corrections A–I were verified, not re-made (see `REMEDIATION_LOG.md` §B for the
per-item disposition). The corrections **this run** contributed:

1. **Discriminating sign test.** The historical error was $1+g^2\bar\Pi$ with
   $\bar\Pi\ge0$. The test now asserts that the flipped convention yields a
   negative spectral measure *and* antiscreening, so it fails if the convention
   is ever changed inconsistently. A test checking only the correct branch would
   pass under either convention.
2. **Positivity gate.** No bound is reported until $(-1)^n\Phi^{(n)}>0$ and
   $H_0\succ0$ are checked. Without it the pipeline would return a plausible
   $M_*$ for a signed measure.
3. **Precision requirement measured, not asserted.** Wide-dynamic-range pencils
   are numerically singular at 60 digits and need ~86; float64 has 16.
4. **Quadrature bug caught.** The Yukawa transform test initially used
   tanh–sinh quadrature on a conditionally convergent oscillatory integral and
   returned a wrong value; `quadosc` was required.
5. **Bibliography mis-resolution caught.** A fuzzy title seed for "Padé
   Approximants" silently resolved to Basdevant (1968) and would have entered
   the bibliography as the Baker–Graves-Morris monograph. Title seeds removed.

## 5. Mathematical proof status

From `data/theorem_status.csv` (11 entries): `PROVED` 5 · `PROVED_CONDITIONALLY`
4 · `CLASSICAL_APPLICATION` 2 · `CONJECTURE`/`FAILED` 0.

Nothing is called a Theorem in `paper/paper.tex` without `PROVED` or
`PROVED_CONDITIONALLY` status. Theorem E carries one `PENDING_VERIFICATION`:
the self-contained edge-convergence argument is given in full, but the classical
density criterion it mirrors (Riesz / Berg–Christensen) is cited without a
theorem number, because the text was not read.

## 6. Priority audit

17 papers assessed. **HIGH:** Lüscher–Wolff 1990, Blossier et al. 2009,
Masjuan–Peris 2009. **MEDIUM:** Bachas 1986, Brown–Weisberger 1979,
Bellazzini et al. 2020, Baker–Graves-Morris.

## 7. Surviving novelty

| Claim | Verdict |
|---|---|
| C1 — the COR/BG breaking profile is an exact positive Laplace transform under H3 | **YES**, moderate confidence |
| C6 — Mellin bridge between radial and low-energy moments | YES but minor |
| C5 — derivative-free sampling hierarchy with deterministic error envelope | PARTIAL |
| C7 — no uniform lower bound without minimum weight | PARTIAL (standard ill-posedness, stated precisely) |
| C8 — scale-invariance obstruction to WGC inference | PARTIAL |
| C2, C3, C4 — complete monotonicity, $\Gamma$ tomography, Hankel hierarchy | **NO** — classical; imported from lattice/Padé technology |

## 8. Weakened or removed

- "Nonperturbative" → "exact under H3", enforced by a test.
- "CM ⟺ H3" → CM ⟺ positive Laplace representation only.
- "New inverse-spectral method" → imported lattice technology.
- H3 moved off the gauge propagator onto the Wilson-loop static potential.
- Theorem B no longer presented as strengthening Bachas; the opposite is stated.

## 9. Numerical validation

79 checks: `extended_analysis.py` 52 · `falsification_suite.py` 17 (0 FATAL,
0 FAIL) · `interval_bounds.py` 10 certified, 0 failures. Plus 44 pytest tests.

Coverage of the requested battery A–N, stated exactly:

| Test | Status |
|---|---|
| A analytic delta · B two atoms · C atom+continuum · D spinor QED · E scalar QED · F multi-species · G near-degenerate · K H3-violating (gapless) | **implemented**, all pass |
| H tiny weight at the true threshold | **implemented**; behaved as predicted |
| J signed measure | **implemented**; gate fires and refuses |
| I wide dynamic range | **partial** — used only as a conditioning probe; it is *not* run through the `Gamma`/`B_K` tomography as a recovery case |
| L synthetic data with controlled noise | **not implemented** |
| M noisy numerical derivatives of $\Phi$ | **not implemented** |
| N blind recovery of $M_*$ and $p$ from samples alone | **not implemented** |

The envelope-perturbation trials in `interval_bounds.py` perturb *exact atomic*
samples inside a deterministic envelope. That is adjacent to M but is neither
synthetic noisy data (L) nor noisy differentiation of $\Phi$ (M), and it is not
a blind recovery (N). Claiming it as coverage of L/M would be the "file created
≠ phase complete" failure this audit exists to prevent, so it is not claimed.

## 10. Reproducibility

`python make.py numerics` and `make.py test` run clean from the tracked tree.
Deterministic (fixed seeds), 30–200 digit arithmetic, no network needed
(API responses cached under `data/cache/`). No generated or cache artifact is
tracked; the CI guard enforces it.

## 11. Remaining blockers

1. **`make pdf` not executed.** No LaTeX engine exists here (`latexmk`,
   `pdflatex`, `xelatex`, `lualatex`, `tectonic` all absent), and `make` is
   absent. The target exits 2 with a clear message. Typesetting is therefore
   **unverified**; only structural validation was possible.
2. **CI unverified.** `.github/workflows/tests.yml` has never run.
   `UNVERIFIED_IN_ENVIRONMENT`.
3. **Two key papers not read at equation level:** Masjuan–Peris 2009 and
   Brown–Weisberger 1979. If the latter states a spectral representation of the
   static kernel, H3 should be attributed to it.
4. **No forward-citation search** was performed for any seed.
5. **Tests L, M and N not implemented** (synthetic noise, noisy
   differentiation, blind recovery); test I is only a conditioning probe.
6. **H3 unestablished** for an interacting kernel beyond leading order — the
   central open physics question.
7. **LICENSE choice assumed.** MIT was written without instruction; confirm.

## 12. Submission-readiness scores

Scored independently, not averaged, and deliberately not inflated.

| Dimension | Score | Reason |
|---|---:|---|
| Algebraic correctness | **8** | Sign derived from the effective action with a discriminating test; Uehling, kernel identity and Gauss-law closure verified. BG eq. (13) taken as quoted from their paper rather than re-derived from their setup. |
| Mathematical rigor | **7** | Proofs decomposed; Carleman confined to determinacy; pushforward handles atoms. One citation lacks a theorem number because the text was not read. |
| Physical defensibility | **7** | H3 conditional and delimited; failure modes explicit and demonstrated; WGC strictly conditional. H3 itself unestablished beyond leading order. |
| Novelty confidence | **3** | Three HIGH threats; the method is classical; three claims downgraded. One narrow observation survives. This is the honest weak point. |
| Bibliography quality | **7** | API-verified with provenance; forbidden domains excluded and tested; a mis-resolution was caught. No forward citations; two key papers unread; monographs hand-entered. |
| Numerical reproducibility | **8** | Deterministic, high precision, interval-certified subset, pre-registered adversarial predictions. No rigorous quadrature certificates for continuum models. |
| Repository hygiene | **8** | Forensics ledger, atomic commits, nothing deleted, caches untracked. `manuscript/` and `paper/` now hold parallel versions; `data/cache/` is tracked (defensible, noisy). |
| Manuscript quality | **6** | English, restrained, honest, structurally validated — but never compiled, so typesetting and length are unverified. |
| **JHEP/PRD readiness** | **4** | No unresolved FATAL, but: narrow surviving contribution, two unread precedents, uncompiled PDF, and the central hypothesis open. Not submittable as it stands; the physics gap, not the prose, is what blocks it. |

## 13. Recommended next actions

1. Read Masjuan–Peris and Brown–Weisberger at equation level; update
   `literature_audit.csv` and, if warranted, attribute H3.
2. Compile the paper on a machine with TeX Live; run CI once.
3. Implement tests L, M and N (synthetic noise, noisy differentiation, and
   blind recovery of $M_*$ and $p$ from samples alone).
4. Decide whether the surviving contribution supports a full paper or a letter.
5. Attack H3 beyond leading order — that is the result that would change the
   novelty score.
