# Red-Team Referee Report

Role: hostile but technically fair JHEP/PRD referee. The objective is to
**reject** the manuscript. Objections are classified FATAL / MAJOR / MINOR /
RESOLVED. Every FATAL must be resolved before the work is submission-ready.

Reviewed: `paper/paper.tex`, `paper/appendix.tex`,
`manuscript/apendice_geometria_laplace.qmd`, the `reproducibility/` suite and
the audit ledgers in `data/`.

---

## R1. Novelty — "this is the lattice effective mass in a different variable"

**FATAL (as originally framed) → RESOLVED.**

The correlator $C(t)=\int e^{-Et}\rho(E)dE$ with $\rho\ge0$ and our
$\Phi(r)=\int e^{-rx}d\nu(x)$ are the same object. The effective mass
$m_{\rm eff}(t)=-\partial_t\log C$ is a monotonically decreasing upper bound on
the ground-state energy; the GEVP on a correlator matrix gives a refining
hierarchy of one-sided bounds. Theorems C and E are those two statements.

Had the paper presented them as a new inverse-spectral method, that alone
warranted rejection.

*Resolution.* The audit identified this before the paper was written
(`data/literature_audit.csv`, threat HIGH). Claims C3 and C4 are downgraded to
`CLASSICAL_APPLICATION` in `data/claims_matrix.csv`; the introduction states
plainly that the machinery is imported from lattice field theory and cites
Lüscher–Wolff and Blossier et al.; `tests/test_bibliography.py` fails if those
citations are ever removed. The surviving claim is the transport to a
generalized-symmetry observable, which is narrow but real.

**Residual risk:** a referee may still judge that transporting known technology
to a new observable is insufficient for a full paper. That is an editorial
judgement, not a technical defect, and it is reported honestly rather than
argued away.

## R2. Novelty — Masjuan–Peris already extract thresholds from VP moments

**MAJOR → PARTIALLY RESOLVED.**

Padé approximants to a Stieltjes series are equivalent to Gaussian quadrature,
orthogonal polynomials and Hankel determinants. Threshold extraction from the
low-energy expansion of the vacuum polarization is therefore already in the
literature, using the same classical machinery.

*Resolution.* Cited and discussed; claim C4 marked `CLASSICAL_APPLICATION`.
The difference recorded is narrow and honest: they estimate a threshold
constant by fitting, we prove a one-sided bound.

**Unresolved:** the audit records `read_level = "abstract + metadata"` for that
paper. An equation-level reading was not completed. Until it is, the recorded
difference is provisional. This is flagged in `data/literature_audit.csv` and
below in the blockers.

## R3. Hypothesis H3 is stronger than reflection positivity, so Theorem B is weaker than Bachas

**MAJOR → RESOLVED (by disclosure).**

Bachas (1986) derives $V'\ge0$, $V''\le0$ from Osterwalder–Schrader positivity
with **no** spectral hypothesis. We derive infinitely many alternating-sign
conditions, but only under H3, which is strictly stronger. In hypothesis-free
content our result is therefore *weaker*, not stronger.

*Resolution.* Stated explicitly in the introduction and again in the
discussion, and recorded in the audit table. The paper does not claim to
improve on Bachas. The open question — whether reflection positivity alone
constrains higher derivatives of the radial profile, and hence whether H3 can
be weakened — is posed as such.

## R4. "Nonperturbative" overclaim

**FATAL (in the earlier draft) → RESOLVED.**

An earlier draft asserted that the master identity holds "nonperturbatively".
It does not: it holds *exactly under H3*, and H3 itself is unproved beyond
leading order. Conflating the two is exactly the error the audit was written to
catch.

*Resolution.* The abstract states the conditional form and immediately
disclaims the stronger reading. `tests/test_latex_structure.py::
test_nonperturbative_is_never_claimed_unqualified` fails the build if the word
appears in a sentence lacking a qualifier.

## R5. Gauge invariance of the positivity hypothesis

**FATAL (in the earlier draft) → RESOLVED.**

Spectral positivity of a gauge-field propagator in a covariant gauge is not a
gauge-invariant statement, and an earlier draft rested H3 on exactly that.

*Resolution.* H3 is now stated on the static potential between heavy probes,
defined by the large-time rectangular Wilson loop — a gauge-invariant
observable. The perimeter/self-energy subtraction is $r$-independent and
therefore drops from $dV/dr$, which closes the obvious follow-up objection
about subtraction ambiguity.

## R6. Sign conventions

**MAJOR → RESOLVED.**

The earlier draft contained an inconsistency: the resummed kernel was written
$1+g^2\bar\Pi$ with $\bar\Pi\ge0$, which yields $d\sigma\le0$ and destroys H3.

*Resolution.* The sign is derived once from the Euclidean quadratic effective
action and propagated (Appendix A), with three independent checks: the
inverse-kernel expansion, the Uehling coefficient $2\alpha/3\pi$, and the
screening direction of the running coupling. `tests/test_sign_convention.py`
contains a **discriminating** test: the flipped convention must produce a
*negative* spectral measure and antiscreening. A test that only checked the
correct branch would pass under either convention and would be worthless.

## R7. Measure-theoretic gaps: atoms, bound states, densities

**MAJOR → RESOLVED.**

Applying a density formula $d\nu = 2x^3\sigma(x^2)dx/g_R^2$ to a measure with
atoms is meaningless.

*Resolution.* $\nu$ is defined as the weighted pushforward
$\int f\,d\nu = g_R^{-2}\int s f(\sqrt s)\,d\sigma$, with the density formula
demoted to the absolutely continuous special case and the atom transport given
explicitly. `tests/test_measure_and_hierarchy.py::
test_atom_transport_is_not_a_density_formula` enforces it.

## R8. Misuse of Carleman

**MAJOR → RESOLVED.**

"Carleman ⇒ $B_K\downarrow M_*$" is not a proof; Carleman gives determinacy and
nothing else.

*Resolution.* The argument is decomposed: (i) Rayleigh characterisation;
(ii) $B_K\ge M_*$ and $B_{K+1}\le B_K$; (iii) determinacy by Carleman;
(iv) edge convergence from density of polynomials in $L^2(\omega)$ for
$\omega=(1+x)e^{-rx}d\nu$, which has an exponential moment; (v)
$\operatorname{supp}\mu_r=\operatorname{supp}\nu$ since $e^{-rx}>0$. Step (iv)
is self-contained, which avoids citing a theorem number that was not read.

## R9. Support-edge convergence assumes what it wants

**MINOR → RESOLVED.**

$B_K$ and $\Gamma$ converge to $\inf\operatorname{supp}\nu$, which need not be
the kinematic threshold one has in mind: a state with zero residue is invisible.

*Resolution.* Stated in both the paper and the working manuscript; the
distinction between a declared lower bound on the support and the effective
infimum is made in H2. The gapless test model demonstrates the failure mode
numerically.

## R10. Numerical conditioning

**MAJOR → RESOLVED.**

High-order Hankel pencils are catastrophically ill-conditioned, and a
double-precision eigenvalue would be meaningless.

*Resolution.* Quantified, not asserted: in the wide-dynamic-range model the
pencil is numerically singular at 60 digits and needs ~86 to resolve, against
16 for float64. The suite detects the collapse instead of returning the
resulting garbage. All reported hierarchy values use 60–200 digits.

## R11. Interval arithmetic vs "certified"

**MINOR → RESOLVED.**

Agreement between two floating-point computations is not an error certificate,
and `mp.quad` carries no rigorous bound.

*Resolution.* The vocabulary is split and enforced by module boundary: only
`reproducibility/interval_bounds.py` says CERTIFIED, and only for finite-atom
`mpmath.iv` enclosures and the proved deterministic envelope inequality.
Everything from quadrature is CHECKED.

## R12. The tomography could be fooled by a non-positive measure

**FATAL if true → TESTED AND RESOLVED.**

If the pipeline returned a plausible $M_*$ for a signed measure, the entire
programme would be unsound.

*Result.* For $d\nu=\delta_1-\tfrac12\delta_2$ the gate fires at
$a_3(1)=-0.4715<0$ and $\det H_0=-0.1839<0$, and refuses to report a bound.
Crucially, $\Phi>0$ and $-\Phi'>0$ both hold, so a screening-only diagnostic
*is* fooled — only complete monotonicity at higher order detects the violation.
This is the strongest argument in the paper for why the infinite hierarchy is
operationally useful rather than decorative.

## R13. Tiny spectral weight at the true edge

**MAJOR → RESOLVED AS A STATED LIMITATION.**

With $d\nu=10^{-12}\delta_2+{}$continuum from 3, does the method lie?

*Result.* It does not lie, but it is uninformative for a long stretch. The
predicted crossover $r_\times=22.76$ is confirmed: $\Gamma=3.136$ at $r=10$,
$3.018$ at $r=20$, $2.532$ at $r=22.76$, $2.0005$ at $r=30$. At $r=3$ the
hierarchy stalls at $3.11$ and never approaches 2. $\Gamma\ge M_*$ is never
violated. Reported as a limitation, with Theorem H as its formal statement.

## R14. WGC overclaim

**FATAL if present → NOT PRESENT.**

*Assessment.* The paper states a conditional implication whose content is
entirely in its hypotheses, names the non-homogeneous gravitational input
required, and says explicitly that calibrating $\eta$ or $\kappa$ after seeing
the spectrum would make the conclusion circular. `test_no_overclaiming_language`
fails the build on "proof of the weak gravity conjecture" and similar.

## R15. The first threshold need not be charged

**MAJOR → RESOLVED (as a negative result).**

In full QED the photon vacuum polarization has massless multi-photon cuts
starting at $s=0$, so H2 cannot be inferred from the electron mass.

*Resolution.* Stated prominently as a scope limitation rather than buried, and
demonstrated numerically by the gapless model, where $\Gamma\to0$.

## R16. Interchange of limits

**MINOR → RESOLVED.**

The Fourier integral in the Yukawa transform is oscillatory and only
conditionally convergent; "the integrand is positive" is not a justification.

*Resolution.* The working manuscript truncates the spectral measure, applies
the regulated transform and takes the limit at $r>0$ under H4. Incidentally,
this bit during testing: a plain tanh–sinh quadrature of that integral does not
converge and gave a wrong value until `quadosc` was used.

---

## Summary

| Severity | Count | Status |
|---|---|---|
| FATAL | 4 (R1, R4, R5, R12) | all RESOLVED |
| MAJOR | 8 | 7 resolved, 1 partially (R2) |
| MINOR | 4 | all resolved |

**No unresolved FATAL objection remains.**

## Remaining referee-visible weaknesses

1. **R2 is only partially resolved.** Masjuan–Peris was not read at equation
   level. Until it is, the claimed difference is provisional.
2. **Brown–Weisberger 1979 was not read.** If it contains a spectral
   representation of the static kernel, H3 should be attributed to it. Marked
   `PENDING_VERIFICATION`.
3. **Forward citation search was not performed** for any seed. The audit is
   backward-looking and partial.
4. **The contribution is narrow.** After the downgrades, what survives is one
   observation (C1) plus minor items. A referee may reasonably ask for a
   physical application beyond the one-loop benchmark before recommending
   acceptance.
5. **H3 remains unestablished** for an interacting kernel beyond leading order.
   This is the central open physics question and the paper says so.
