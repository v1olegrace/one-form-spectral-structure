# Spectral structure of approximate one-form symmetry breaking

**Mauro de Oliveira Cardoso** (research name: *Viole*) · independent researcher, Botucatu, SP, Brazil

A one-form symmetry observable, a positivity hypothesis, and an honest account
of exactly where the argument holds and where it stops.

Manuscript: [`paper/paper.tex`](paper/paper.tex) — draft **v0.5.2** ·
Research plan: [`ROADMAP_CIENTIFICO.md`](ROADMAP_CIENTIFICO.md) (pt-BR)

---

## What this is, in one paragraph

The electric one-form symmetry of Maxwell theory is broken by charged matter.
The breaking is measured by a radial profile δ(r), defined by Córdova, Ohmori
and Rudelius and computed at one loop by Basile and Golmohammadi. **We do not
compute that profile.** We ask what its *shape* says about the spectrum.
Conditional on a positive Stieltjes representation of the static response
(Hypothesis **H3**), the reduced profile Φ(r) = δ(r)/r² is exactly the Laplace
transform of a positive measure, whose support edge is the lowest threshold that
*couples to this observable* — so standard inverse-spectral tools apply, and
give upper bounds that descend to that threshold.

**H3 is not proved unconditionally.** At linear order in the probe, the static
kernel inherits a positive Stieltjes form from an *assumed* positive Euclidean
spectral representation of ⟨FF⟩ obeying the Bianchi identity at coincident
points (Appendix A, Proposition 7). With a Coulomb weight it has the form of
H3, the integral starting at the bottom of the spectral support; that this is
positive, the gap, is a separate input. Deriving the representation from the
Wightman axioms needs lemmas and a continuation not yet checked against their sources;
beyond the quadratic cumulant it is open. Most of this repository is the work
of finding out precisely what each of those words costs.

## Start here

Compiled PDFs are **not** tracked — they are build products, rebuilt from the
sources below in one command.

| If you want | Read | Build it |
|---|---|---|
| The physics, 15 pages | [`paper/paper.tex`](paper/paper.tex) | `python make.py pdf` |
| How ⟨FF⟩ reaches the static kernel | [`notes/E2c_transport_linear_probe.md`](notes/E2c_transport_linear_probe.md) | `python -m pytest tests/test_e2c_transport.py` |
| The probe at O(q⁴), Euler–Heisenberg | [`notes/E3_nonlinear_probe_EH.md`](notes/E3_nonlinear_probe_EH.md) | `python -m pytest tests/test_e3_nonlinear_probe.py` |
| A six-page discussion brief (pt-BR) | [`paper/professor_brief.tex`](paper/professor_brief.tex) | `tectonic paper/professor_brief.tex` |
| The argument and the mathematics (pt-BR) | [`output/impressao_professor_2026-09-28/fontes_tex/`](output/impressao_professor_2026-09-28/fontes_tex/) | `tectonic raciocinio_e_matematica.tex` |
| What is proved vs. checked vs. open | [Claim ledger](#claim-ledger) and [Status](#status-be-precise-about-what-is-what) below |
| The RPA result and how it broke twice | [`reports/H3_GHOST_ANALYSIS_2026-09-29.md`](reports/H3_GHOST_ANALYSIS_2026-09-29.md) |
| The proofs | [`notes/H3_RPA_proof_note_2026-09-29.md`](notes/H3_RPA_proof_note_2026-09-29.md) |
| To run everything | [Quickstart](#quickstart) |

```bash
pip install -r requirements.txt
python make.py test        # 396 tests
python make.py numerics    # regenerate every numerical result
```

---

## The RPA result

Within the Dyson/RPA structure — matter-current density ρ ≥ 0 by Lehmann
positivity, a once-subtracted polarization, and 𝒢 = g²/(Q²·W) with
W = 1 − g²Π̄ — one partial-fraction identity organises everything:

```
W(Q²) = Z₃ + g² ∫ ρ(s) ds/(s + Q²),     Z₃ := 1 − g² ∫ ρ(s)/s ds
```

so W(0) = 1, W(∞) = Z₃, and W is strictly decreasing. Three regimes follow,
and the complete spectral representation differs in each. Since v0.4 this is
stated in Appendix A of the paper; the proofs are in
[`notes/H3_RPA_proof_note_2026-09-29.md`](notes/H3_RPA_proof_note_2026-09-29.md).

| Regime | Coulomb pole | Continuum | Timelike atom | Spacelike pole | Constant | H3 (contact-free) |
|---|---|---|---|---|---|---|
| **Z₃ > 0** | g²/Q², residue > 0 | dσ ≥ 0 on [4m², Λ²] | **one**, at s_a > Λ², weight > 0 | none | none | **holds** |
| **Z₃ = 0** | same | same | none | none | 1/μ | **fails** if μ < ∞, by a contact term only |
| **Z₃ < 0** | same | same | none | **one**, residue < 0 | — | **fails** |

Three things are worth stating plainly, because each of them cost a correction:

**H3 is not equivalent to "no ghost".** A spacelike pole obstructs it, but the
boundary Z₃ = 0 has no pole and H3 can still fail through an additive constant.
Absence of a pole is *necessary, not sufficient*. The constant is a contact
term, supported at r = 0, so the paper's Theorem A still holds on r > 0 there;
only the literal hypothesis fails. The genuine failure is Z₃ < 0.

**The continuum density stays non-negative for every coupling.** It is
g⁴ρ/(s|W|²) — ρ divided by a modulus squared. So a moment test on the continuum
returns `CHECKED_COMPATIBLE` even when H3 is false. That is a scope limit of
such tests; the paper states it, and a test here asserts it.

**Resummation moves the measure outside the input support.** With a hard
cutoff, W is real again on (Λ², ∞). If the density does not vanish at the
cutoff, as the Dirac one does not, W runs to −∞ at the edge and vanishes exactly
once there when Z₃ > 0, producing a discrete atom with positive weight above
the cutoff. The mechanism is **known**: Giacosa and Wolkanowski (2012,
arXiv:1209.2332) obtain, by one-loop resummation, a physical-sheet pole outside
the input support with positive residue, closed by a spectral sum rule. We did
not discover it; we rediscovered it by first getting the support claim wrong.

For QED at α = 1/137, Z₃ = 0.966 at Λ² = 10²⁰ m², and Z₃ vanishes only near the
Landau pole, log(Λ²/4m²) = 3π/α ≈ 1291. Below it the bubble chain satisfies the
hypothesis with a wide margin.

## Claim ledger

| # | Statement | Status | Nearest precedent |
|---|---|---|---|
| C1 | Under H3, Φ(r) = ∫e^{−rx}dν, ν ≥ 0, exactly | proved conditionally | Uehling; COR 2022; BG 2025 |
| C2 | Φ is completely monotone | classical | Bernstein–Widder; Bachas 1986 |
| C3 | Γ = −(log Φ)′ ↓ M\*, an upper bound | classical (effective mass) | Lüscher–Wolff; Blossier et al. |
| C4 | Hankel pencil B_K ↓ M\* | classical (GEVP / Padé) | Blossier et al.; Masjuan–Peris |
| C7 | No uniform lower bound on M\* from a finite window | proved; phenomenon known | inverse-Laplace ill-posedness |
| C8 | Positivity alone cannot fix a WGC scale | proved conditionally | COR 2022; Dvali |
| C9 | Bubble chain: H3 holds for Z₃ > 0, fails for Z₃ < 0; at Z₃ = 0 only a contact term | proved in the model | Giacosa–Wolkanowski 2012 (atom); Källén |
| C10 | Linear probe: positive Euclidean ⟨FF⟩ + Bianchi with contacts ⟹ positive Stieltjes kernel on r > 0 (the form of H3, given a Coulomb weight) | proved conditionally | stochastic vacuum model (tensor split D vs D₁) |

Per-claim novelty verdicts: [`data/claims_matrix.csv`](data/claims_matrix.csv).
C5 and C6 are **not** in the canonical paper — see [`DECISIONS.md`](DECISIONS.md).

## Status: be precise about what is what

**Proved** (within the stated hypotheses, RPA model): the partial-fraction
identity; strict monotonicity and the endpoints of W; existence, uniqueness and
simplicity of the spacelike zero iff Z₃ < 0, with residue < 0; existence and
uniqueness of the timelike atom iff Z₃ > 0, with weight > 0; absence of complex
zeros on the physical sheet; the two sum rules; the Coulomb residue, support and
absence of a constant term for Z₃ > 0.

**Checked numerically, not proved**: the numerical values of every table; the
atom position and weight; the reconstruction; finite-moment compatibility.
Vocabulary is enforced by module boundary — `CHECKED` means high-precision
numerics without a rigorous bound, `CERTIFIED` means an interval enclosure or a
proved inequality, `PENDING_VERIFICATION` is never guessed.

**Measured accuracy, against an independent reference** (mpmath + an exact
closed-form anchor, sharing no code with the production path), at Λ² = 10⁶:

| Quantity | g²/g²_c | before | now |
|---|---|---|---|
| Π̄(∞) | any | 2.9 × 10⁻¹⁶ | 2.9 × 10⁻¹⁶ |
| log₁₀(edge distance) | 0.5 | 1.2 × 10⁻⁶ | 1.9 × 10⁻¹⁵ |
| atom weight | 0.5 | 2.0 × 10⁻⁶ | 2.7 × 10⁻¹⁵ |
| atom weight | 0.1 | 2.0 × 10⁻⁶ | 3.3 × 10⁻¹⁴ |

The "before" column is the history worth keeping. Two float64 weight routes
agreed with each other to 4.8 × 10⁻⁹ and both missed by 2 × 10⁻⁶, because they
consumed the same located root: agreement measured consistency, not accuracy.
The root was found by QUADPACK on an integrand with a square-root branch point
at the upper endpoint, where its error estimate is optimistic by orders of
magnitude. The edge integral and its derivative have a closed form, checked
against 50-digit quadrature to 10⁻⁴¹, and the production path now uses it for
edge distances up to 100 Λ². The 3.3 × 10⁻¹⁴ floor at g²/g²_c = 0.1 is
intrinsic: the distance there is 3.3 × 10⁻⁴², reached through its logarithm,
and converting amplifies the error by |log₁₀ d| ln 10 ≈ 95.

**Proved conditionally (v0.5, restated in v0.5.1)**: the transport ⟨FF⟩ →
Wilson loop → static kernel at linear order in the probe. *Assume* the
Euclidean two-point function of the field strength has a positive spectral
representation with measure μ ≥ 0, ∫dμ/(1+s) < ∞, and obeys the Bianchi
identity including coincident points. Truncating at the quadratic cumulant,
the static potential and the field of a static line see ⟨FF⟩ only through
a³(r) = ∫dμ(s) e^{−√s r}/(4πr), so on r > 0 the kernel is a positive Stieltjes
function: the form of H3 if μ({0}) > 0, with the integral starting at
inf supp σ, possibly zero; the gap, which makes it positive, is not implied.
The massless helicity term never reaches either observable, so CPT is not
needed. A local contact that violates Bianchi gives an area term whose slope
diverges as 1/ε when the regulator is removed: a regulated contact, not a
finite string tension, and only structurally like the function D of the
stochastic vacuum model. At fixed regulator the T → ∞ rate is q²C_ε(r)/T,
measured against its predicted coefficient; C_ε has no limit as ε → 0. The
representation itself is derived from the Wightman axioms only through two
classical lemmas and the Wightman → Schwinger continuation, all unread at the
level of the statements used, so it is an assumption.

**Beyond the quadratic cumulant, in the effective theory** (note E3): for
smooth sources of radius R ≫ 1/m, the Euler–Heisenberg O(q⁴) term of the
static energy is fixed in sign — a polarizability term −A/r⁴ with A > 0 leads
at large r, the universal term is −c q₁q₂(q₁² + q₂²)/(80π³r⁵), and its Z³ part
is Frolov's Wichmann–Kroll tail. At finite probe charge the profile gains a
negative, gapless −8α³q_W²/(45π m⁴r⁶), so it is not completely monotone at
large r: the limits q_W → 0 and r → ∞ do not commute. Theorem A, which concerns
the linear coefficient, is untouched.

**Open, and not close to closed**: those lemmas; point probes beyond the
quadratic cumulant, where the light-by-light kernel at distances of order 1/m
sets the coefficient and nothing here computes it; isolating charged channels
from massless cuts; **originality**,
which is not established — Brown–Weisberger (1979) is unread behind a paywall,
the stochastic-vacuum primaries are unread, and the Schilling–Song–Vondraček
theorem numbering is unconfirmed (secondary sources disagree).

**Continuous integration**: run 36543772146 at `730bdf0` failed in the `paper`
job with `! LaTeX Error: File 'lmodern.sty' not found`, while `tests`,
`certified` and the canonical manuscript build passed. The workflow installs
TeX Live with `--no-install-recommends`, and `lmodern` is a separate Debian
package that the discussion brief needs and the paper does not. With `lmodern`
added, run 36597424208 at `6672fdb` passed all three jobs. The status of later
commits is recorded in [`FINAL_REPORT.md`](FINAL_REPORT.md), not here, because
a README line about CI goes stale on the next push.

**Never done**: human expert review, submission.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python make.py check       # report available toolchain
python make.py test        # full suite, 396 tests
python make.py numerics    # regenerate every numerical result
python make.py audit       # rebuild audit ledgers
python make.py pdf         # build paper/paper.pdf (needs a LaTeX engine)
```

Optional certified backend (python-flint / Arb):

```bash
pip install -r reproducibility/requirements-certified.txt
python make.py certified
python reproducibility/verify_one_loop_output.py --reintegrate --no-write
```

The RPA analysis and its independent reference:

```bash
python reports/h3_ghost_2026-09-29/ghost_analysis.py   # tests, table, four figures
python reports/h3_ghost_2026-09-29/reference_mp.py     # multiprecision reference
```

**Known environment condition.** Run the suite as `python make.py test` or
`python -m pytest tests -q`. A bare `pytest` at the root is scoped by
`pytest.ini`; without it, an untracked historical copy under `laplace/` collides
on test basenames.

## Repository layout

```
paper/                    canonical manuscript (English, LaTeX)
  paper.tex appendix.tex  references.bib is GENERATED -- do not hand-edit
  professor_brief.tex     six-page discussion brief (pt-BR)
reproducibility/          numerical pipeline
  moment_conditions.py        shared finite-moment gate, used by all four pencils
  rpa_kernel_conditions.py    conditional RPA classifier, interval-based
  spectral_models.py          model zoo: atoms and continua, positive and signed
  falsification_suite.py      adversarial tests; predictions recorded before running
  one_loop_certified.py       validated one-loop data (Arb via python-flint)
  verify_one_loop_output.py   independent re-verification with completeness checks
reports/
  h3_ghost_2026-09-29/        RPA analysis, multiprecision reference, figures
  H3_GHOST_ANALYSIS_*.md      the spacelike obstruction, in full
  professor_2026-09-28/       meeting material and its number-checking script
notes/                    proof notes and working records
tests/                    396 tests; every one is meant to be able to fail
data/                     literature harvest with provenance, audit ledgers
output/impressao_*/       print-ready PDFs for a meeting
manuscript/               author's pt-BR Quarto draft -- NOT canonical, predates v0.2
```

## How this repository is built

These are the practices that make a theory paper's numerics trustworthy.

1. **Tests must be able to fail.** `test_sign_convention.py` asserts that the
   flipped vacuum-polarization sign produces a *negative* spectral measure. A
   test that passes under both conventions is worthless.
2. **Finite checks before derivative-based estimation.** `moment_gate` checks
   finite real moments, a₀ > 0, aₙ ≥ 0, H₀ ≻ 0 and the localizer H₁ ⪰ 0. Rank or
   precision failures refuse a bound; they do not refute H3.
3. **Refuse rather than return a number.** `reconstruct()` and `sum_rules()`
   raise outside the regime they implement. A Z₃ interval straddling zero is
   `UNRESOLVED` in *every* entry point, not just in the classifier.
4. **Diagnostics reach the result.** A quadrature non-convergence message
   produces `PRECISION_UNCERTAIN`, not `RESOLVED`. Locating a root is not the
   same as the quadrature achieving what was asked of it.
5. **Global controls, not just local agreement.** Agreement at a few values of
   Q² is exactly how a missing spectral atom hid for a day. Sum rules constrain
   the total weight, and a test requires that dropping the atom breaks them.
6. **Independent references, not self-consistency.** A deviation between two
   sides of an identity measures inconsistency, not error. Precision claims are
   backed by multiprecision arithmetic and an exact closed-form anchor.
7. **Provenance for literature.** Every field of the 28 articles and preprints
   in `data/literature_harvest.json` is returned by the API its provenance
   names, in a cached response under `data/api_responses/`, or is a hand
   correction whose note quotes the value; `python make.py bib` checks this
   offline and CI runs it. The six monographs and the DLMF, which have no such
   record, are entered by hand in `scripts/build_bibliography.py`. Forbidden
   sources (wikis, content farms, AI summaries) fail the test suite.
8. **Reproducibility.** Validated in a clean checkout: 396 tests run (one is
   skipped when Tectonic is absent) and
   `git status` is empty after `make.py numerics`, `audit` and `certified`, so
   those artefacts are regenerated byte-for-byte from the commit. The PDF QA
   record `output/data/canonical_pdf_qa.json` is the exception by design: it
   stores the path and hash of the PDF it inspected. Its source hashes must be
   those of the blobs git stores, which are LF, and
   `tests/test_pdf_qa_record.py` fails otherwise; generate it from an LF
   checkout, since a Windows checkout converts line endings.

## Errors found and corrected, on the record

Kept deliberately, because a repository that only shows successes is not
evidence of anything.

- Three sibling modules emitted spectral bounds with **no gate at all**,
  including a second function also named `hankel_bound` on the certification
  path. Fixed by extracting `moment_conditions.py`.
- The verifier bound what was present, not that nothing was missing: dropping a
  comparison row *with its counter* passed every assertion. Now the table must
  be a full cartesian product and the certificate indices a bijection.
- H3 was identified with the **general** Stieltjes class, which admits an
  additive constant the canonical H3 excludes. Corrected to a three-regime
  statement.
- The spectral measure was claimed to stay inside the input support. **False.**
  The ~10⁻⁸ agreement attributed to quadrature was an omitted atom; including it
  improved the reconstruction by four orders of magnitude.
- The atom finder reported "no atom" at small coupling — asserting absence
  against a theorem — because the edge distance shrinks exponentially. It now
  solves in log of the edge distance and reports `UNRESOLVED` rather than
  absence.
- A resonance on the unphysical sheet was claimed from an argument that only
  excluded a real zero. Retracted; the fate of that pole is undetermined.
- A `quadrature_ok` flag reported `True` while six non-convergence warnings
  escaped during the same call, because the root search discarded the
  diagnostics of the integrals it evaluated. Every evaluation in the chain now
  reports into the result, and a non-converged chain is `PRECISION_UNCERTAIN`.
- `ghost_root()` decided the regime from the point value of Z₃, bypassing the
  interval discipline everything else followed, and bracketed from 10⁻⁶, which
  can miss a small root. It now takes the shared interval decision and brackets
  from W(0) = 1.
- The continuum density returned the Dirac formula above the cutoff, where the
  regulator had removed it.
- Two tests required the code to stay imprecise: one asserted that two weight
  routes must disagree with the reference by more than with each other. They
  now pin the measured accuracy, and the historical failure is still shown on
  raw QUADPACK, where it belongs.
- The v0.4 PDF QA record matched the committed source for one file in six. It
  had been generated in a Windows working copy where some sources had been
  rewritten with LF and the rest checked out with CRLF, and no test compared it
  with anything. The v0.5 record comes from an LF clone and matches every blob,
  and a test now enforces that.
- `python make.py bib` did not reproduce the committed bibliography. Eight
  cited records came from outside the harvester's seed list, with no cached
  response; INSPIRE years were preprint years and article numbers were lost to
  `page_start`; failed fetches were cached and blocked retries; and a run
  rewrote the JSON in another format without its hand fields. Running it would
  silently have dropped eight citations. Fixed on 3 October: the target now
  verifies offline that every value is returned by the API its provenance
  names, or is a hand correction whose note quotes it, and writes nothing
  otherwise; CI runs it. Rebuilding it exposed two wrong entries: Banks–Seiberg
  was printed with its preprint year 2010 instead of 2011, and an uncited
  entry had page "3" instead of article number 035003.
- The E2c note printed the boundary form of its Stokes lemma with a factor 2
  in front of each bilateral integral; taken literally, it is twice the
  surface cumulant. The code was right, and the test compared the surface
  integral with the code rather than with the printed display, so nothing
  failed. A test of the display itself now does.
- The same note stated the T → ∞ rate as C(r)/T, without the probe charge
  squared and without saying it holds only at fixed regulator. The
  coefficient has no limit as the regulator is removed; its exact expansion
  for the Coulomb measure is now in the note and in a test. The audit that
  found this proposed the coefficient r/(2π²√ε); the correct leading term is
  √π r/(4π²√ε), with a logarithm the audit had taken to be finite.
- v0.5 called the area term of a Bianchi-violating local contact "the
  function D of the stochastic vacuum model". Its slope diverges like 1/ε, so
  it is a regulated contact, not a finite string tension, and the comparison
  with D is one of tensor structure only.
- v0.5 said Proposition 7 derives H3 "from Wightman positivity of the field
  strength and the Bianchi identity". The proposition assumes a positive
  Euclidean representation, whose derivation from the Wightman axioms is
  unchecked, and yields H3 only with a Coulomb weight; the gap is separate.
  Restated in v0.5.1 everywhere it appeared.
- The `paper` CI job failed on the discussion brief for want of `lmodern`, a
  risk that was visible when the job was added. Reproduced in a clean
  `ubuntu:24.04` container with the workflow's own `apt` line: the build fails
  with exactly the CI error without `lmodern` and passes with it.

## Citation

See [`CITATION.cff`](CITATION.cff). Please cite the paper, not this repository,
once it is public.

## License

Code: MIT ([`LICENSE`](LICENSE)). The manuscript text and figures are © the
author; the license for the paper will be set at submission.
