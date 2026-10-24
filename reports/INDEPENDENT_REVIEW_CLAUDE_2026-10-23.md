# Independent review of the Claude handback — 23 October 2026

## Verdict and scope

The takeover contains substantial correct progress, but the assertion that
everything is finished is too strong. The central positive-Z3 RPA proof,
ordered conserved-current construction, nonnegative compact radial probe
lemma, and local-theory energy bound survived independent review. The
headline Gaussian counterexample and three matched crossovers also survived.
There are still a false quoted far-tail number, a missing explicit source
positivity premise in the canonical paper, a repairable critical-case proof
omission, and reproduction gates that remain open.

This review read `.agent/TAKEOVER_CLAUDE_2026-10-23.md` first and did not
reapply P5–P9 or edit reviewed scientific sources. Independent reviewers
examined finite probes/energy and RPA/transport separately. Only new review
reports, source-access evidence, and command logs were written. No commit,
push, staging or publication was performed.

## Confirmed by fresh execution

- `python -B -m pytest tests -q -rs`, with repository-local TinyTeX on PATH:
  **466 passed, no skips**, in 99.46 seconds. This is implementation evidence,
  not a proof of the physics. Log:
  `.agent/evidence/independent-review-tests-2026-10-23.log`.
- `verify_one_loop_output.py --reintegrate --no-write`: **PASS** for 12
  datasets, 144 rows and 288 certificates, reintegrating all 28 distinct
  source samples and 12 weight benchmarks. No certificate output was changed.
- `build_claim_graph.py --check`: 57 reviewed claims, 32 inventoried units,
  none uncovered. This validates inventory consistency, not every scientific
  assertion inside each inventoried paragraph.
- Offline bibliography provenance: all 29 API-derived records verified.
- The stored clean-room log really reports **469 passed**. Its three extra
  tests are source-hygiene parametrizations for files tracked only in the
  candidate repository. Those logs support the reported earlier candidate,
  not automatically every later edit.
- Latest remote workflow remains run **37331435402**, green only for original
  HEAD `78b637cb6a2cf4d92691a3eb7e31312baf23ef32`.

## Corrections required

### 1. Gaussian far-tail quadrature — numerical error, CHECKED

At `R=10`, `m=1`, the spectral routine
`reproducibility/nonlinear_probe_eh.py:365` integrates an exponentially tiny
quantity without removing its leading exponential. Increasing nominal
precision alone does not cure the observed failure of its error estimate.

At `r=300`, the existing routine gives
`Gamma = 2.00755065423793887472...`. An independently reweighted endpoint
integral and an exponentially rescaled direct spectral calculation give
`Gamma = 2.007515904186790945...`, stable at 40/60/90 digits. The original
profile's relative discrepancy is approximately `0.0017343921`.

`tests/test_e3_nonlinear_probe.py:357` currently enshrines the incorrect
rounded value `2.00755`. Replace the unstable integration or honestly refuse
that domain, then test independent accuracy. Merely changing the expected
number or broadening its tolerance would not repair the algorithm.

This defect does **not** refute the central counterexample or the quoted
crossovers. Independent checks retained:

- `Gamma(50) = 0.932403168696575383... < 2`;
- Gaussian crossover `55.9067264856621765...`;
- uniform-ball crossover `20.4822190112477458...`;
- compact-polynomial crossover `18.9502732027310442...`.

See `INDEPENDENT_FINITE_PROBE_REVIEW_2026-10-23.md` for independent routes,
precision checks and the important high-s tail handling.

### 2. Finite-probe premise and wording — manuscript scope

`paper/paper.tex:443–460` needs to state **rho >= 0**. The source lemma E3
11.1 already does; the canonical paragraph omits it, although `F >= 1`
depends on it. A signed normalized compact radial density is a counterexample.
For radius one, take density `12/pi` inside radius 1/2 and
`-6/(7pi)` in the remaining shell. Its total charge is one, but its Yukawa
factor at mass four is approximately **-1.25785979636**.

The final phrase saying that bounds apply to an extended source *only*
outside a radius where charge vanishes also overstates necessity. Compact
nonnegative radial support is a proved sufficient criterion. A particular
Gaussian failure does not classify every noncompact source.

The polynomial `(1-u^2/a^2)^2` cut off at `a` is globally C1, not C-infinity.
It is valid for the exterior lemma, but should not be confused with the
compact C-infinity mollifier of the current construction or with controlled
higher-derivative EFT at its boundary.

### 3. Critical RPA — missing source argument, true result

The direct proof explicitly excludes `Z3=0`, while later text asserts
Stieltjes membership and positivity after subtraction of the critical
constant. The asymptotic constant by itself is not a proof of the remaining
measure's positivity. The result is true: an independent completion appears
in `INDEPENDENT_RPA_TRANSPORT_REVIEW_2026-10-23.md`.

The completion takes subcritical couplings to the critical value and uses
weak limits of the positive measures `sigma_n/(1+s)`. An atom at infinity
becomes the constant `1/mu`; the Coulomb residue and lower support bound are
retained separately. This can be inserted in the proof note without relying
on unread Chapter 7. P1's execution record also needs updating because the
unbounded-support extension is now actually present in the note.

### 4. Reproduction/readiness — supported progress, unmet strict gate

The clean-room checkout remains dirty in eight rendered figures and
`extended_verification.json`, as the P13 report itself documents. Excluding
environment-dependent render bytes from a strict guard is defensible, but
does not literally satisfy the original clean-git-after-regeneration gate.
Semantic checks or a separate explicitly defined deterministic-artifact gate
are needed. Do not solve this by arbitrary tolerances.

The existing 498-file snapshot also predates later edits to eight
scientific/documentary files, including the brief and E3. Code and the
canonical article match the tested snapshot; this limits the discrepancy,
but a final candidate should be frozen and rerun exactly. A comparison
manifest is under `tmp/review_claude_2026-10-23/`.

PDF QA was not reproduced inside the fresh documented environment.
`reproducibility/requirements-pdf.txt` **does exist** and declares PyMuPDF;
the correction is to include that documented optional file in the gate, not
to claim the dependency is undocumented. Ubuntu regeneration and remote CI
on the candidate remain unverified.

## What the new SSV source actually settles

An original publisher-distributed second-edition preview was obtained:
https://api.pageplace.de/preview/DT0400.9783110269338_A19166479/preview-9783110269338_A19166479.pdf

The title/copyright identify the 2012 edition and ISBNs. Original printed
pages 16–18 include Definition 2.1 and Theorem 2.2 with proof. In particular,
2.2(iii) supplies closure under finite pointwise limits. It is directly useful
for the RPA limit argument after its model-specific assumptions are verified.

Original cross-references identify **Theorem 7.3** as reciprocal duality and
**Corollary 7.4** as analytic half-plane characterization. Their numbering is
no longer an unresolved either/or question. Their complete statements and
proofs are still unread here. Do not mark the entire book proof-level-read.

Definition 2.1 allows a constant: book-class Stieltjes membership is not
automatically contact-free H3. Nothing in this book establishes the physical
QED kernel, the quantum Wilson-line identification, a charged gap, or
nonlinear-probe control. Preserve the direct RPA proof.

Details, download hashes and usable original pages:
`reports/SSV_PRIMARY_REVIEW_2026-10-23.md`.

## Continuation

The exact execution handoff is
`.agent/CONTINUATION_AFTER_REVIEW_2026-10-23.md`. Correct the verified issues
first, then study the low-s three-photon channel with an explicit convention
map. Useful primary starting points were located and read at the relevant
equations: Groote–Pivovarov, hep-ph/0103313, sections 2.2, 3.1 and 4.1; and
Portoles–Ruiz-Femenia, hep-ph/0107324, equations 1 and 6–9. Their heavy-quark/
gluon coefficients cannot be imported as QED photon coefficients by an
unexplained substitution. No QED numerical coefficient was adopted here.

Verdict: **corrections required; not READY_FOR_EXPERT_REVIEW**. No false core
RPA or local-energy theorem was found, but absence of an observed fatal
objection is not a certificate that none exists. Expert review remains a
separate human activity.
