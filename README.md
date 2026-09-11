# Spectral structure of approximate one-form symmetry breaking

Conditional on a positive Stieltjes representation of the gauge-invariant
static response, the reduced one-form symmetry-breaking profile
$\Phi(r)=\delta(r)/r^2$ is exactly the Laplace transform of a positive measure
whose support edge is the lowest threshold of the charged sector.

**"Exact" means exact within that hypothesis.** It is not a proof that the
hypothesis holds nonperturbatively, and it does not hold in full QED, where
massless multi-photon cuts remove the positive gap.

## What is and is not new

The adversarial priority audit in `data/literature_audit.csv` found direct
precedents on every methodological axis. Recording them is the point:

| Ingredient | Status | Precedent |
|---|---|---|
| Laplace structure of Uehling screening | classical | Uehling 1935 |
| Complete monotonicity of a Laplace transform | classical | Bernstein–Widder |
| Sign conditions on static-potential derivatives | **precedent, weaker hypothesis** | Bachas 1986 (from reflection positivity alone) |
| Monotone one-sided bound on the lowest state | **precedent, same mathematics** | lattice effective mass / GEVP |
| Threshold from vacuum-polarization moments | **precedent** | Masjuan–Peris 2009 |

What remains is the assembly: that a generalized-symmetry observable carries
this structure under a stated hypothesis, the resulting operational bounds, and
the explicit failure modes. See `data/claims_matrix.csv` for the per-claim
verdict.

## Layout

```
paper/          canonical manuscript (LaTeX) + verified references.bib
manuscript/     author's working draft (pt-BR, Quarto) -- NOT canonical
reproducibility/
  spectral_models.py     model zoo (atoms + continuum, positive and signed)
  falsification_suite.py adversarial tests, predictions computed first
  interval_bounds.py     the only module that says "certified"
  laplace_geometry.py    benchmark identities
  extended_analysis.py   sampled hierarchies, Mellin bridge, figures
tests/          pytest suite (44 tests)
data/           forensics, literature audit, claims matrix, theorem status
scripts/        literature harvester, bibliography and audit builders
```

## Reproducing

```
pip install -r requirements.txt
python make.py check      # report available external tools
python make.py numerics   # regenerate all numerical results and figures
python make.py test       # 44 tests
python make.py pdf        # requires a LaTeX toolchain (absent here; exits 2)
```

`make` and LaTeX are **not** installed in the reference environment, so
`make pdf` cannot be executed there and is not claimed to pass. A `Makefile` is
provided for environments that have them; `make.py` is the portable equivalent.

## Status and honesty conventions

* **CHECKED** — verified by high-precision arithmetic. `mp.quad` carries no
  rigorous error bound, so this is *not* a certificate.
* **CERTIFIED** — a rigorous enclosure (`mpmath.iv`) or a proved deterministic
  inequality. Confined to `reproducibility/interval_bounds.py`.
* **PENDING_VERIFICATION** — not confirmed against a primary source. Never
  guessed, never silently filled in.

Every formal result carries a status in `data/theorem_status.csv`; nothing is
called a "Theorem" in the paper unless it is `PROVED` or
`PROVED_CONDITIONALLY`.

See `REMEDIATION_LOG.md` for assumptions and deviations, `RED_TEAM_REPORT.md`
for the self-refereeing pass, and `FINAL_REPORT.md` for scores and remaining
blockers.
