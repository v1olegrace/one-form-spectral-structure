# E3. The static Wilson loop at fourth order in the probe charge (Euler–Heisenberg)

**Status (5 October 2026).** A computation in the Euler–Heisenberg effective
theory, for smooth rigid sources in its regime of validity. The analytic steps
are derived below; the two-centre integrals are checked by quadrature in
`reproducibility/nonlinear_probe_eh.py`, and the statements by
`tests/test_e3_nonlinear_probe.py` (18 tests). An earlier derivation of 4
October was redone here by a different numerical route, and the two sources it
rests on were read: Dunne, arXiv:hep-th/0406216, eq. (1.9) on p. 7 and
eq. (1.17) on p. 10, and Frolov, arXiv:1111.2303v5, eqs. (9)–(13) on p. 6.
Nothing here is an interval certificate: the numbers are CHECKED, not
CERTIFIED. No novelty is claimed: the single-source result is Frolov's
eq. (13), and the method is textbook nonlinear electrostatics.

**What it changes.** Theorem A is untouched: it concerns the coefficient of the
profile linear in the probe charge, which depends on the two-point function
alone. Two sentences of the paper need qualification. "The probe self-energy
subtraction is r-independent" holds at quadratic order only. "Nothing here
fixes the sign" of the four-field cumulant is now false in the effective
theory: there the sign is fixed (Sections 4–6). The profile taken at finite
probe charge, as eq:qdef defines it, is not completely monotone at large r
(Section 7), so Hypothesis 5 carries the load exactly in the large-r regime
that the threshold bounds use.

## 1. Set-up

Static fields, Heaviside–Lorentz units, ħ = c = 1, canonical normalisation.
The one-loop Euler–Heisenberg Lagrangian to quartic order is

    L = (E² − B²)/2 + c [(E² − B²)² + 7 (E·B)²],   c = e⁴/(360 π² m⁴) = 2α²/(45 m⁴),

with e² = 4πα (Dunne, eq. (1.9); the same coefficient appears in Frolov's
eq. (9) as 4c = e⁴/(90 π² m⁴)). For static electric fields L = E²/2 + c E⁴.
In the paper's normalisation, S = −F²/(4 g_R²) + A·j, the canonical charge of a
probe of charge q_W is q = g_R q_W, and for one Dirac species c = g_R⁴/(360 π² m⁴).

Two rigid, spherically symmetric sources of charges q₁, q₂ and radii R₁, R₂ sit
a distance r apart, with r > R₁ + R₂. The effective theory applies when
1/m ≪ R_i and the field stays far below m²/e everywhere, which for a source of
radius R means α q_W/(mR)² ≪ 1. The O(q³) term vanishes: the cubic cumulant is
zero in a charge-conjugation-invariant state, and L is even in F (Furry).

## 2. The energy at fixed free charge

The Wilson loop couples A to a fixed external current, so V(r) is the
minimum energy at fixed free charge: Gauss's law of the nonlinear theory is
div D = ρ with D = ∂L/∂E = E + 4c|E|²E. The energy density is
D·E − L = E²/2 + 3c E⁴, which in terms of D reads D²/2 − c D⁴ + O(c²). Write
D = D₀ + δD with D₀ = −∇φ₀ the vacuum Coulomb field and div δD = 0. Then
∫ D₀·δD = ∫ φ₀ div δD = 0, so

    U = U₀ − c ∫ |E₀|⁴ d³x + O(c²).

The sign is negative: the vacuum responds as a dielectric with ε > 1. The
naive evaluation of T₀₀ = E²/2 + 3cE⁴ on the unadjusted Coulomb field gives
+3c∫|E₀|⁴, which is wrong; the test solves the nonlinear radial problem of one
source exactly and finds (U(c) − U(0))/c → −∫|D₀|⁴.

## 3. Sectors

With d_i the field of source i for unit charge and E₀ = q₁d₁ + q₂d₂,

    U₄(r) = −c [4 q₁³q₂ I₃₁ + 4 q₁q₂³ I₁₃ + q₁²q₂² I₂₂],
    I₃₁ = ∫ |d₁|² (d₁·d₂),   I₂₂ = ∫ [2 |d₁|²|d₂|² + 4 (d₁·d₂)²].

The q_i⁴ terms are self-energies, independent of r.

## 4. The q₁³q₂ sector: universal, r⁻⁵

Outside source 1, |d₁|²d₁ = û/((4π)³u⁶) = −∇ψ₁ with ψ₁(u) = 1/(5 (4π)³ u⁵),
u = |x − x₁|. Integrating by parts, I₃₁ = ∫ ψ₁ div d₂ = ⟨ψ₁⟩ over source 2.
So the sector sees only the exterior field of source 1, whatever its profile,
and for a point-like source 2 it is exactly 1/(320 π³ r⁵). For a uniform ball
or a thin shell of radius R as source 2, averaging u⁻⁵ gives

    ball:  I₃₁ = 1/(320 π³ r⁵ (1 − R²/r²)²),
    shell: I₃₁ = (3 + R²/r²)/(960 π³ r⁵ (1 − R²/r²)³).

The universal part of the two odd sectors is

    U₄,univ = −c q₁q₂ (q₁² + q₂²)/(80 π³ r⁵).

## 5. The q₁²q₂² sector: a polarizability, no r⁻⁵ and no r⁻³

Near source 1 the field of source 2 is nearly constant, so the leading term is
the energy of a polarizable body in an external field:
∫|d₁|²|d₂|² + 2∫(d₁·d₂)² ≈ (1 + 2/3) ∫|d₁|² / ((4π)² r⁴). With W_i the Coulomb
self-energy of source i (W_i = ½∫|D_i|²),

    U₄,pol = −A/r⁴,   A = (5c/(12 π²)) (W₁ q₂² + W₂ q₁²) > 0.

This term attracts whatever the signs of the charges, because the integrand of
I₂₂ is non-negative. For two balls it is −c q₁²q₂²/(8 π³ R r⁴); for two shells,
−5c q₁²q₂²/(48 π³ R r⁴).

Why no other long-range power appears at order R⁰: write |d|² as the
homogeneous distribution (4π)⁻²|x|⁻⁴ plus a correction C supported in the
source. The Fourier transform of |x|⁻⁴ is −π²|k|, and that of x_ix_j/|x|⁶ is
|k|(a δ_ij + b k̂_ik̂_j); products of two such terms are proportional to k²,
which is analytic and gives only contact terms. The cross terms are
convolutions of a radial C with |x|⁻⁴, whose multipole expansion has only even
powers: r⁻⁴, r⁻⁶, …, with coefficients ∝ R⁻¹, R, R³, … . So at fixed r the
sector is r⁻⁵ h(R/r) with h odd in R/r: there is no R-independent r⁻⁵ term and
no r⁻³ term. The test fits h at r = 1 and finds the R⁰ coefficient at
−2×10⁻⁹ (2×10⁻⁵ of the universal coefficient, the truncation of the fit), the
R⁻² coefficient at 2×10⁻¹³, and the next term −27R/(140 π³) for balls.

## 6. Totals, and the Wichmann–Kroll tail

For charges ±q and two balls of radius R,

    V₄(r) = c q⁴ [ 1/(40 π³ r⁵ (1 − R²/r²)²) − 1/(8 π³ R r⁴) + 27R/(140 π³ r⁶) + … ].

The universal term is repulsive for ±q, +4α⁴/(225 π m⁴ r⁵) for ±e; the
polarizability term is attractive and larger by about 5r/R, so it leads at
large r. There is no r⁻³ term in any sector.

For (Ze, −e) the Z³ part of the universal term is

    +2 α (Zα)³/(225 π m⁴ r⁵),

which is Frolov's eq. (13): φ(r) = (Qe/4πr)[1 − 2Q²α³/(225 π m⁴ r⁴)], an
electron energy −eφ, so the correction is repulsive. Frolov states that it
"exactly coincides with the Wichmann-Kroll potential" of his reference [8];
that reference was not read here. Frolov uses the same effective-theory
method, so the agreement checks the arithmetic, not the method.

## 7. The profile at finite probe charge

Outside one static source D = q/(4πr²) exactly, and the flux of E, which is
what eq:qdef measures, is

    q(r) = q_W [1 − c g_R² q_W²/(4 π² r⁴)].

So δ_NL = −c g_R² q_W²/(π² r⁴) and

    Φ_NL(r) = −c g_R² q_W²/(π² r⁶) = −8 α³ q_W²/(45 π m⁴ r⁶)   (QED),

the Laplace transform of the density −(c g_R² q_W²/(120 π²)) x⁵ on (0, ∞):
negative and without a gap. The one-loop linear profile decays like e^{−2mr},
so for every q_W ≠ 0 the profile at finite charge changes sign. With the
paper's one-loop Dirac measure (`spectral_models.dirac_density`) and
α = 1/137.035999, the crossover is at r_x = 14.36/m, 11.57/m and 9.52/m for
q_W = 0.1, 1 and 5. Beyond r_x, Φ < 0, so it is not completely monotone, and
−∂_r log|Φ| tends to 6/r, as if M* were zero. These are leading-order numbers in
both pieces; derivative corrections to the effective theory are of relative
order 1/(mr)² and are not included.

The limits q_W → 0 and r → ∞ therefore do not commute. The linear coefficient
is still isolated exactly: q(r) is odd in q_W, so
[8 q(q_W) − q(2q_W)]/(6 q_W) removes the cubic term.

## 8. Not computed

- Point probes (R → 0). The effective theory gives A ∝ 1/R, which diverges;
  the true coefficient is set at distances of order 1/m by the full one-loop
  light-by-light kernel. Its magnitude, sign and finiteness are not computed.
  The vanishing of the R⁰ term of the q₁²q₂² sector rests on the parity
  argument of Section 5, which is not checked beyond the effective theory.
- Derivative operators (relative O(1/(mR)²) and O(1/(mr)²)), two-loop
  Euler–Heisenberg (relative O(α)), O(c²) terms (order q⁶), loops inside the
  effective theory.
- Non-spherical, deformable or overlapping sources; the nonabelian case.
- Outside this note, and not computed: power counting suggests that the photon
  two-point function of QED has a three-photon continuum starting at s = 0 at
  order α⁴, allowed by charge conjugation. If so, the support of σ
  reaches zero with a tiny positive weight, positivity survives, and the gap
  of Hypothesis 2 holds only at low order. This is not established.

## 9. Tests

`tests/test_e3_nonlinear_probe.py`: the coefficient in terms of α; the sign of
the fixed-charge energy on a ball and on a shell, against the +3∫E⁴ of the
naive evaluation; ψ₁ as a potential for |d₁|²d₁; the average of u⁻⁵ over a
ball; I₃₁ for balls and shells against the closed forms (10⁻¹¹), and its
independence of the profile of source 1; I₂₂ fitted in R for the absence of
R⁰ and R⁻² terms, its leading term from the self-energy, the shell case and
the positivity of its integrand; the totals for ±q and ±e and Frolov's
eq. (13) in symbols; the two-ball total against its sectors; the profile at
finite charge by finite differences; the oddness in q_W; the crossover with the
paper's one-loop measure; that measure against the Uehling form.
