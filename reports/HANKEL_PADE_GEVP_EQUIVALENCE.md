# HANKEL / PADE / GEVP / LANCZOS EQUIVALENCE

## Side-by-side map

| Our object | Lattice / QFT object | Status of the analogy |
|---|---|---|
| Φ(r) = ∫ e^{−rx} dν(x) | Euclidean correlator C(t) = ∫ e^{−tE} ρ(E) dE | **exact isomorphism** under r ↔ t |
| Γ(r) = −d log Φ/dr | effective mass m_eff(t) | **exact isomorphism**; monotone decrease is the standard argument |
| M_* = inf supp ν | ground-state energy E₀ | **exact isomorphism** |
| Hankel pencil λ_min(H₁,H₀) | GEVP / variational method | **equivalent after change of variables** |
| Sampled b_j = Φ(r+jh)/Φ(r) | Lanczos / Prony on C(t+ja) | **equivalent**; same Hankel data |
| tiny lower weight | poor ground-state overlap | **exact isomorphism** |
| large-r convergence | ground-state dominance | **exact isomorphism** |

The analogy is an isomorphism almost everywhere. The honest conclusion is
that the *extraction machinery* is not new, and the paper must say so.

## Where the analogy genuinely breaks

One place, and it is the place the contribution lives:

**In lattice spectroscopy, positivity of the spectral measure is
guaranteed** by reflection positivity of the transfer matrix. A GEVP
practitioner never asks whether ρ ≥ 0; it is a theorem. Consequently the
positivity hierarchy can only ever *confirm*, and the Hankel determinants
are used solely as an estimator, never as a test.

**Here, positivity is the physical hypothesis H3 under test.** The same
determinants become a falsifier. The signed-measure model in the test
suite is the demonstration: it satisfies Φ > 0 and −Φ′ > 0 — it looks
exactly like screening — and is rejected at a₃ = −0.4715, det H₀ =
−0.1839. No effective-mass analysis would have flagged it, because no
effective-mass analysis is looking.

## Closest published analogues (2024–2025)

Two recent works are closer to the core method than the lattice
effective mass is, and neither is currently cited:

1. **Lawrence, *Model-free spectral reconstruction via Lagrange duality*
   (arXiv:2408.11766).** Convex optimization + Lagrange duality gives
   bounds on arbitrary integrals of the spectral density from positivity
   alone, stated to be **information-theoretically complete**. If that
   completeness claim holds for linear functionals, no method can beat it
   on those functionals. M_* is not a linear functional, so the Hankel
   bound is not directly dominated — but the paper cannot claim
   optimality without addressing this. *Read at abstract level only;
   requires equation-level read before any optimality language is used.*

2. **Mutzel & Tilloy (arXiv:2512.19594).** Linear-programming extraction
   of the **mass gap from an equal-time two-point function at spatial
   separation**, via Källén–Lehmann inversion as convex optimization.
   This matches our geometry — spatial separation, not Euclidean time —
   more closely than any lattice reference. **This is the single closest
   published analogue to the core method and must be cited.**

3. **Wagman's Lanczos formalism for lattice correlators** (and
   *Lanczos algorithm for lattice QCD matrix elements*, Phys. Rev. D
   2025, DOI 10.1103/zjzt-rv86) extracts energies from Euclidean
   correlators with faster ground-state convergence than effective
   masses. Lanczos on moment data *is* the Jacobi-matrix route to the
   same Hankel pencil. Directly relevant to Theorem E's claimed
   improvement over Γ(r), and not cited.
