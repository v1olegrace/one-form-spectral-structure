# E3. The static Wilson loop at fourth order in the probe charge (Euler–Heisenberg)

**Status (extended 23 October 2026).** A computation in the Euler–Heisenberg effective
theory, for smooth rigid sources in its regime of validity. The analytic steps
are derived below; the two-centre integrals are checked by quadrature in
`reproducibility/nonlinear_probe_eh.py`, and the statements by
`tests/test_e3_nonlinear_probe.py`. Section 10 adds a smooth Gaussian source,
a matched finite-spectral benchmark, and an analytic remainder bound within
the radial local quartic model. Section 11 replaces that benchmark by the
one-loop Dirac measure. It proves that a compactly supported probe keeps the
support edge (exterior lemma). It finds that a Gaussian probe's own charge
tail pushes the effective mass below the threshold (CHECKED). It extends the
remainder bound to arbitrary sources by convex duality. The numerical ball and shell
profiles benchmark the local quartic functional; their sharp boundaries do
not satisfy the slow-variation assumption of the effective theory. An
earlier derivation of 4 October was redone here by a different numerical
route, and the two sources it
rests on were read: Dunne, arXiv:hep-th/0406216, eq. (1.9) on p. 7 and
eq. (1.17) on p. 10, and Frolov, arXiv:1111.2303v5, eqs. (9)–(13) on p. 6.
Nothing here is an interval certificate: the numbers are CHECKED, not
CERTIFIED. No novelty is claimed: the single-source result is Frolov's
eq. (13), and the method is textbook nonlinear electrostatics.

**What it changes.** Theorem A is untouched: it concerns the coefficient of the
profile linear in the probe charge, which depends on the two-point function
alone. The self-energies of isolated rigid sources remain r-independent;
the mixed polarizability term is an interaction and survives that subtraction.
The local effective theory fixes the sign of its fixed-charge quartic energy
and of the individual interaction sectors (Sections 2–6), without fixing a
general four-field cumulant or a universal sign for their sum. The formal
sum of the point-source one-loop linear profile and the exterior nonlinear
tail is not completely monotone at large r (Section 7). Its crossover is a
benchmark, not a matched prediction for the smooth sources assumed here.

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
1/m ≪ R_i, every field-variation length (including a smoothed edge) is much
larger than 1/m, and the field stays far below m²/e everywhere (Dunne,
pp. 29–30). For a source of radius R, the weak-field condition is
α q_W/(mR)² ≪ 1. The O(q³) term vanishes: the cubic cumulant is
zero in a charge-conjugation-invariant state, and L is even in F (Furry).

The uniform ball and infinitesimally thin shell used below are idealised
profiles for testing the local functional. Their boundary layers require
smoothing before the derivative expansion can be controlled. No bound on
the omitted derivative terms at those sharp boundaries is obtained by these
quadratures.

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

The q_i⁴ terms are self-energies of isolated rigid sources, independent of r.
Their subtraction does not remove the mixed q₁²q₂² interaction below,
although its coefficient depends on the Coulomb self-energies. The negative
sign of the un-subtracted quartic energy does not imply that every
interaction sector, or their sum for arbitrary charges, is negative.

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

Outside one spherical static source D = q/(4πr²) exactly. To first order in c,
the flux of E, which is what eq:qdef measures, is

    q(r) = q_W [1 − c g_R² q_W²/(4 π² r⁴)].

So δ_NL = −c g_R² q_W²/(π² r⁴) and

    Φ_NL(r) = −c g_R² q_W²/(π² r⁶) = −8 α³ q_W²/(45 π m⁴ r⁶)   (QED),

the Laplace transform of the density −(c g_R² q_W²/(120 π²)) x⁵ on (0, ∞):
negative and without a gap. For a numerical benchmark define
Φ_bench = Φ_lin,point + Φ_NL, using the point-source one-loop Dirac measure
(`spectral_models.dirac_density`) and α = 1/137.035999. The positive linear
term decays like e^{−2mr}; the negative power tail eventually dominates for
every fixed q_W ≠ 0. This formal sum crosses zero at r_x = 14.36/m, 11.57/m
and 9.52/m for q_W = 0.1, 1 and 5. The numbers are CHECKED, not CERTIFIED.
Beyond r_x, Φ_bench < 0 and is not completely monotone;
Γ_app = −∂_r log|Φ_bench| tends to 6/r. Since the profile is signed, Γ_app
is not a positive-measure spectral bound.

These terms have not been matched to the same smooth source. For a unit
normalised spherical density ρ_R supported in u ≤ R, angular integration of
the Yukawa kernel gives the exterior factor
F_R(M) = ∫ d³u ρ_R(u) sinh(Mu)/(Mu). It multiplies each linear spectral
component for r > R; for a uniform ball it is
3[MR cosh(MR) − sinh(MR)]/(MR)³. Thus the linear profile, and its crossover
with the nonlinear tail, depend on the source profile. The tabulated r_x is
not a prediction for the smooth sources of Section 1 or a controlled
point-probe calculation. Derivative corrections outside the source have
relative order 1/(mr)² and are not included; boundary corrections are also
uncontrolled for the idealised ball and shell.

Non-commutation concerns the asymptotic diagnostic, not the value of Φ.
Extending the normalised benchmark continuously to q_W = 0,
lim_{r→∞} lim_{q_W→0} Γ_app = 2m, whereas
lim_{q_W→0} lim_{r→∞} Γ_app = 0. Both iterated limits of Φ_bench itself are
zero. This is a statement about the specified truncated benchmark, not
full QED.

For an odd analytic response q(r;h) = a₁(r)h + a₃(r)h³ + a₅(r)h⁵ + ⋯,
[8 q(r;h) − q(r;2h)]/(6h) = a₁(r) − 4a₅(r)h⁴ + O(h⁶).
It cancels the cubic term and estimates the linear coefficient with O(h⁴)
error at fixed r. It is exact only within the first-order-in-c truncation
used above, which retains no fifth-order response. Oddness alone does not
give an exact extraction at finite charge.

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
- Outside this note: the gap. The paper already states, citing Beneke and
  Ruiz-Femenía (footnote 1 of arXiv:1606.02434), that massless multi-photon
  cuts of the photon vacuum polarization start at s = 0 in full QED, so
  Hypothesis 2 cannot be inferred from the electron mass. That concerns the
  linear kernel at higher order in α, not the probe charge, and nothing here
  changes it.

## 9. Tests

`tests/test_e3_nonlinear_probe.py`: the coefficient in terms of α; the sign of
the fixed-charge energy on a ball and on a shell, against the +3∫E⁴ of the
naive evaluation; ψ₁ as a potential for |d₁|²d₁; the average of u⁻⁵ over a
ball; I₃₁ for balls and shells against the closed forms (10⁻¹¹), and its
independence of the profile of source 1; I₂₂ fitted in R for the absence of
R⁰ and R⁻² terms, its leading term from the self-energy, the shell case and
the positivity of its integrand; the totals for ±q and ±e and Frolov's
eq. (13) in symbols; the two-ball total against its sectors; the profile at
finite charge by finite differences; cancellation of the cubic term in the
truncated response and the surviving fourth-order error for an independent
odd polynomial with a quintic term; the formal crossover with the paper's
point-source one-loop measure; that measure against the Uehling form.
Section 10 adds the quoted numbers of that section.

Section 11 adds:

- the closed-form $\bar\Pi$ against its Feynman-parameter integral;
- the Gaussian Laplacian polynomials and $\int d\nu/x^4=\alpha/(15\pi)$;
- the Gaussian-probe profile by the spectral and momentum routes, and its
  local Uehling approximation;
- the effective masses below and above the threshold, the far Gaussian
  value against an endpoint reference with no finite difference, and the
  compact-probe values against the exact ratio of moments;
- a quadrature guard that refuses an error estimate that is not small
  relative to the result;
- the Gaussian, ball and $C^1$ polynomial crossovers;
- the exterior lemma against the Fourier route, and a signed source for
  which $F\ge1$ fails;
- the lattice duality check with its second-order coefficient;
- the $V(r)$ window.

## 10. Matched smooth-source progress and a local remainder bound

**Scope.** PROVED_CONDITIONALLY for the stated local electric model and
radial source; CHECKED for floating-point values. The Gaussian example
uses the same source for every term. It supplies no bound for omitted
QED derivative operators, higher field operators or higher loops. The
point-source crossover in Section 7 remains a separate formal benchmark.

### 10.1 A smooth source and common matching

Use the normalized, infinitely differentiable density
$$\rho_R(r)=\frac{e^{-r^2/R^2}}{\pi^{3/2}R^3},\qquad
g_R(r)=\frac{\operatorname{erf}(r/R)-2(r/R)e^{-r^2/R^2}/\sqrt\pi}{4\pi r^2}.$$
Here $R$ is a width, not a support radius. The Maxwell displacement is
$D_0=qg_R(r)\hat r$ and is regular at zero. Its field and all its absolute
derivative scales follow from $g_R(r)=R^{-2}g_1(r/R)$. A conservative
bound is $|D_0|\le |q|/(4\pi R^2)$: for $r\le R$ bound the enclosed charge
by $4(r/R)^3/(3\sqrt\pi)$; for $r\ge R$ bound it by one.

For an independently specified positive massive atom of weight $\lambda$,
the linear response kernel is $1/Q^2+\lambda/(Q^2+M^2)$. Its convolution
with this same density is
$$K_{M,R}(r)=\frac{e^{M^2R^2/4}}{8\pi r}
\left[e^{-Mr}\operatorname{erfc}(MR/2-r/R)
      -e^{Mr}\operatorname{erfc}(MR/2+r/R)\right].$$
This follows by angular integration of the Yukawa Green function; the
code is independently checked against the two radial Green integrals.
The massive atom is a defined benchmark, not a substitute for the QED
one-loop spectral density. One may define a quadratic model by this
response kernel and perturb it by $cE^4$. To separate orders, keep
$O(\lambda)$ and $O(cq^2)$ in the normalized flux correction, dropping
$O(c\lambda q^2)$ and $O(c^2q^4)$. This is matching within a specified
perturbative model; no all-orders completion is inferred.

Subtract the known Gaussian Maxwell flux $4\pi r^2g_R(r)$ before forming
the correction profile $\Phi=-r^{-1}d(\text{flux correction})/dr$. Gauss's
law $g'_R+2g_R/r=\rho_R$ and the Yukawa equation give
$$\Phi_{\rm lin,R}=4\pi\lambda r[M^2K_{M,R}-\rho_R],\qquad
\Phi_{\rm NL,R}=16\pi c q^2[2g_R^3+3r g_R^2g'_R].$$
Both expressions use $\rho_R$ even inside the source. Geometry can make
the source-subtracted linear expression signed there despite a positive
spectral measure; it is not the point-source complete-monotonicity test.
For $r/R\to\infty$ the nonlinear term approaches
$-cq^2/(\pi^2r^6)$ and the linear atom decays exponentially. Thus their
specified truncated matched sum is eventually negative for $c>0,q\ne0$.
No sharp edge or unmatched point-source term is used for this conclusion.

For $m=1$, $R=10$, $q=0.3$, $\alpha=1/137.035999$,
$c=2\alpha^2/45$, $M=0.2$, $\lambda=10^{-4}$, the computed totals at
$r=100,200$ are respectively $2.2411164\times10^{-14}$ and
$-2.9102525\times10^{-22}$ (CHECKED). The source satisfies the explicit
weak-field bound $e|D_0|/m^2\le7.22935\times10^{-5}$ and has derivative
parameter $(mR)^{-2}=0.01$. These are scale diagnostics, not rigorous error
bounds on the QED derivative expansion. Dunne's Section 2.3, (2.40)--(2.41)
was reread for that distinction; the expansion is asymptotic.

### 10.2 Exact remainder bound inside the radial local quartic theory

For $c\ge0$, the electric Legendre transform of
$L_c(E)=E^2/2+cE^4$ is strictly convex. At fixed signed radial displacement
$D$, its unique electric field solves $D=E+4cE^3$, and
$h_c(D)=E^2/2+3cE^4$. Differentiating at fixed $D$ gives
$$\partial_c h_c=-E^4,\qquad
\partial_c^2 h_c=\frac{16E^6}{1+12cE^2},\qquad |E|\le|D|.$$
Taylor's formula with an integral remainder therefore proves, for every
$D$ and $c\ge0$,
$$0\le h_c(D)-\left(\frac{D^2}{2}-cD^4\right)\le8c^2D^6.$$
For one radial source Gauss fixes $D=D_0$ exactly and the corresponding
radial $E$ is curl free. Integration is legitimate because the Gaussian
field is bounded at zero and falls as $r^{-2}$ at infinity. Consequently
$$0\le U(c)-U(0)+c\int D_0^4\,d^3x
\le8c^2\int D_0^6\,d^3x
\le8c^2\|D_0\|_\infty^2\int D_0^4\,d^3x.$$
This is an actual error bound for the $O(c)$ energy *inside this local
quartic theory*. It does not estimate the difference between that theory
and QED. For the weak-source parameters above the relative bound compared
with $c\int D_0^4$ is at most $1.07910\times10^{-12}$. In a numerically
resolvable stress case $q=4,R=1,c=0.2$, an independent exact radial solve
gives a remainder $2.2948903\times10^{-5}$ below the evaluated bound
$2.3763320\times10^{-5}$; these values are CHECKED, without directed
rounding. This stress case tests the local mathematical inequality and is
not asserted to be in the QED EFT regime.

The two-centre minimizer is not generally radial, so the argument above,
which uses $D=D_0$, does not apply to it as written; Section 11.4 extends
the two-sided bound to arbitrary sources by convex duality. Section 11
replaces the massive-atom benchmark of 10.1 by the one-loop Dirac measure.
Derivative remainders and interacting point probes remain UNRESOLVED.

## 11. Extended probes with the one-loop Dirac measure (23 October 2026)

**Scope.** 11.1 and 11.4 are proofs: 11.1 at linear order, conditional only
on the kernel being $\int d\mu(s)/(Q^2+s)$ with $\mu\ge0$ (Hypothesis 3, or
Proposition 4 of note E2c); 11.4 inside the local electric theory
$L_c=E^2/2+cE^4$. Everything numerical is CHECKED by quadrature, never
interval-certified. Units $m=1$, $\alpha=1/137.035999$, $c=2\alpha^2/45$, and
$d\nu$ is the paper's one-loop Dirac measure (`spectral_models.dirac_density`),
so the linear kernel is $1/Q^2+\int d\nu(x)/[x^2(Q^2+x^2)]$. Same truncation
as 10.1: $O(\alpha)$ in the linear term, $O(cq^2)$ in the nonlinear term.
Functions in `reproducibility/nonlinear_probe_eh.py`; each number below is
asserted in `tests/test_e3_nonlinear_probe.py`. The predictions were recorded
in `.agent/reports/P7.md` before any of these computations.

*Correction, 23 October 2026, after an independent review.* `mp.quad` stops
once its error estimate is below $2^{4-\text{prec}}$ in absolute terms. The
profiles at $r\gtrsim50$ are below that tolerance, so they were integrated at
the coarsest level. The result was stable under a change of `dps` and wrong.
Two quoted values were wrong in the fifth decimal: $\Gamma_{\rm lin}(300)$
for the Gaussian and $\Gamma(50)$ for the ball. Each integrand is now divided
by an a priori bound before integration, and a result whose error estimate
is not small relative to it is refused. Old and new values at 30–90 digits
are in `.agent/evidence/R0-quadrature.json`. The three crossover radii and
$\Gamma_{\rm lin}(30)$, $\Gamma_{\rm lin}(50)$ did not change.

### 11.1 Exterior lemma: a finite probe does not move the edge

**Lemma (PROVED_CONDITIONALLY, as stated in the scope).** Let $\rho\ge0$ be a
radial charge density of unit total charge, supported in $|u|\le a$. At
linear order in the probe, for every $r>a$,
$$\Phi_\rho(r)=\int e^{-rx}F_\rho(x)\,d\nu(x),\qquad
F_\rho(x)=\int\rho(u)\,\frac{\sinh xu}{xu}\,d^3u,\qquad
1\le F_\rho(x)\le\frac{\sinh xa}{xa}.$$

*Proof.* Each spectral component of the kernel is a Yukawa potential
$Y_x(r)=e^{-xr}/(4\pi r)$, the Coulomb atom being $x=0$. The radial solution
of $(-\nabla^2+x^2)\varphi=\delta(|y|-u)/(4\pi u^2)$ that decays at infinity
equals $[\sinh(xu)/(xu)]\,Y_x(r)$ for $r>u$ (Newton's shell theorem for the
Yukawa equation). Superposing shells gives $F_\rho(x)Y_x(r)$ outside the
support. The flux and $\Phi=-r^{-1}\partial_r(\text{flux})$ then follow
exactly as for a point source, with $d\nu$ replaced by $F_\rho\,d\nu$. Since
$\sinh z/z$ is at least one and increases, $1\le F_\rho\le\sinh(xa)/(xa)$, and
$F_\rho(0)=1$ leaves the Coulomb flux unchanged. $\blacksquare$

Consequences on $(a,\infty)$: $\Phi_\rho$ is completely monotone; since
$F_\rho>0$, $\inf\operatorname{supp}F_\rho\,d\nu=\inf\operatorname{supp}\nu=M_*$,
so $\Gamma_\rho\ge M_*$ and the Hankel bounds of Theorem E hold for the
reweighted measure. Convergence $\Gamma_\rho\to M_*$ needs the moment
condition of Hypothesis 4 for $F_\rho\,d\nu$ at some $r_0>a$. It holds because
$F_\rho(x)\le e^{xa}$ bounds every moment
$\int x^ke^{-r_0x}F_\rho\,d\nu$ by the point-source moment at $r_0-a$. The edge
does not move; the measure is reweighted by a factor growing like $e^{xa}$.
The mollified line of note E2c, Section 12, has this form at every fixed
$\delta$ once $T\to\infty$ and $R\to\infty$, and $F_\delta\to1$ as
$\delta\to0$.

*The sign condition is needed.* Both bounds on $F_\rho$, and the positivity
that keeps the edge, use $\rho\ge0$. Take unit total charge, support radius 1,
density $12/\pi$ for $u<1/2$ and $-6/(7\pi)$ for $1/2<u<1$. With
$B(z)=3(z\cosh z-\sinh z)/z^3$, $F(x)=[15B(x/2)-8B(x)]/7$, and
$F(4)=-1.25785979636\ldots<0$. A spectral atom at $x=4$ then gives a
negative exterior profile. So the lemma is a sufficient condition for
non-negative radial sources. It says nothing about signed sources. Nor does
it show that sources without compact support must violate the bound.

*Checks.* For a uniform ball, $F=3i_1(z)/z$ with $z=xa$. At $a=10$, $r=11$,
the lemma agrees to $10^{-30}$ with an independent Fourier route: the
Feynman-parameter one-loop $\bar\Pi(k^2)$ times $3j_1(ka)/(ka)$, summed with
`mp.quadosc`. That route returns a wrong value without warning at 30 digits
and is run at 40. The exterior effective mass decreases to $2m$ from above:
$\Gamma=2.94681,\ 2.25339,\ 2.07112,\ 2.03647$ at $r=11,15,30,50$. The
central difference agrees with the exact ratio
$\int xe^{-rx}F\,d\nu/\int e^{-rx}F\,d\nu$ to $3\times10^{-13}$. The value at
$r=50$ was quoted as $2.03646$ before the correction above; the old
integration was off by $1.3\times10^{-6}$ there.

### 11.2 A Gaussian probe: its own charge tail hides the threshold

For the Gaussian of 10.1 the exterior form is not available, because the
charge never ends. As in 10.1, the probe's own Maxwell flux is subtracted
first. Without that subtraction, the bare-charge term of $\delta/r^2$,
$-r^{-1}dQ_{\rm enc}/dr=-4\pi r\rho_R(r)<0$, enters $\Phi$ at order one, and
$\Phi$ is negative outside the core.
The linear vacuum-polarization profile is
$$\Phi_{{\rm lin},R}(r)=4\pi r\int d\nu(x)\,
\Bigl[K_{x,R}(r)-\frac{\rho_R(r)}{x^2}\Bigr],$$
with $K_{x,R}$ the smeared Yukawa kernel of 10.1. It is evaluated by two
independent routes:

- **Spectral.** Multiprecision quadrature. For $x\ge X$ the bracket is
  replaced by its expansion $\sum_{k=1}^3\nabla^{2k}\rho_R/x^{2k+2}$. The
  truncation is not exact. For $r=5$–$300$ the omitted $k=4$ term is below
  $3\times10^{-16}$ of $\Phi$; that bounds the accuracy of this route at
  small $r$.
- **Momentum.** $-\frac2\pi\int_0^\infty k\sin(kr)\,e^{-k^2R^2/4}\,
  \bar\Pi(k^2)\,dk$ with the Feynman-parameter polarization. This route uses
  neither $d\nu$ nor the erfc formula.

For $R=10$ the two routes agree to $10^{-14}$ at $r=5,15,30$. At larger $r$
the oscillatory cancellation leaves only the spectral route usable: at
$r=80$ the momentum route fails at 70 digits.

The local Uehling term $(4\alpha/15)\,r\,\nabla^2\rho_R$ reproduces the
profile to within 3% for $r=5$–$30$. It comes from
$\int d\nu/x^4=\alpha/(15\pi)$, the coefficient of the local $F\Box F$
operator. So outside the core the linear profile is the vacuum polarization
of the probe's own Gaussian tail.

The effective mass of the linear coefficient alone is
$$\Gamma_{\rm lin}=0.48395,\ 0.93240,\ 1.93672,\ 2.12222,\ 2.00752
\quad\text{at } r=30,\ 50,\ 100,\ 120,\ 300.$$
The values at $r=30$ and $50$ agree between the two routes to $10^{-9}$. At
$r=300$ the erfc factors have saturated on $2\le x\le3$, and
$\Gamma=\int xw/\int w$ with $w=e^{R^2x^2/4-rx}\,d\nu$ to a relative
$e^{-175}$. This endpoint ratio has no finite difference and gives
$2.0075159041867909454$, which matches the spectral route to $10^{-19}$.
Before the correction above, the value at $r=300$ was quoted as $2.00755$.
So $\Gamma_{\rm lin}<M_*=2m$ for $r\lesssim mR^2$, and it is not monotone.
The Yukawa tail $e^{M^2R^2/4-Mr}$ takes over only for $r\gtrsim MR^2/2$, which
is $r\gtrsim100$ at $M=2$.

This is a CHECKED counterexample, at linear order and in the one-loop model,
to transferring the threshold bound $\Gamma\ge M_*$ from point or compact
probes to probes with non-compact charge tails. It does not contradict
Theorem C: where $\Gamma<M_*$, the Gaussian-probe profile is not a positive
Laplace transform with support in $[M_*,\infty)$.

With the nonlinear term of 10.1 at $q=0.3$, the matched first-order sum
changes sign at $r_x=55.9067264857=5.59R$. The recorded prediction was
$5.6R$, from the local estimate
$x^7(4x^2-6)e^{-x^2}=\alpha q^2/(6\sqrt\pi R^2)$ with $x=r/R$. The $2m$
threshold never controls the matched sum for this probe.

### 11.3 Compact probes: the matched exterior profile

For $r>a$ Gauss's law gives $D=q/(4\pi r^2)$ exactly for any radial probe,
and a local constitutive relation fixes $E$ from $D$ at the same point. At
first order in $c$ the exterior nonlinear term is therefore exactly
$-cq^2/(\pi^2r^6)$, whatever happens inside the probe. With 11.1,
$$\Phi_a(r)=\int e^{-rx}F_\rho(x)\,d\nu(x)-\frac{cq^2}{\pi^2r^6},\qquad r>a.$$
This requires no derivative expansion inside the probe. It omits:

- $O(c^2q^4r^{-10})$ terms;
- local derivative corrections, of relative order $1/(mr)^2$;
- nonlocal light-by-light corrections sourced near the probe, which are
  expected to decay like $e^{-2m(r-a)}$.

None of these is bounded here.

For $a=10$ and $q=0.3$, the sum changes sign at:

| Probe | Exterior factor $F$ | $r_x$ | Distance from surface |
|---|---|---|---|
| Uniform ball | $3i_1(z)/z$ | $20.4822190112$ | $10.48$ |
| Polynomial $(1-u^2/a^2)^2$ | $105\,i_3(z)/z^3$ | $18.9502732027$ | $8.95$ |
| Point source, Section 7 ($q_W=1$) | — | $11.567$ | — |

The polynomial density, extended by zero, is $C^1$ and not smooth: its
second derivative jumps at $u=a$. It satisfies the exterior lemma, but it
differs from the $C^\infty$ mollifiers of note E2c, and it gives no control
of derivative corrections near its boundary. The recorded prediction for the
ball was 20–21. For these compact probes the threshold controls the exterior
linear term, and the crossover sits roughly the point-source distance away
from the probe's surface.

### 11.4 The first-order energy for arbitrary sources

**Theorem (PROVED, local electric theory).** Let $\rho$ have finite Maxwell
energy, with Maxwell field $D_0=-\nabla\varphi_0$ and
$\int|D_0|^6<\infty$. Let $c\ge0$ and
$U_c(\rho)=\min\{\int h_c(D):\operatorname{div}D=\rho\}$, where $h_c$ is the
Legendre transform of 10.2. Then, with no symmetry assumed,
$$0\le U_c(\rho)-U_0(\rho)+c\int|D_0|^4\le8c^2\int|D_0|^6.$$

*Proof.*

- **Upper bound.** $D_0$ is admissible, and pointwise
  $h_c(D)\le D^2/2-cD^4+8c^2D^6$ (10.2).
- **Lower bound.** Fenchel–Young gives $h_c(D)+L_c(E)\ge D\cdot E$ for all
  $D,E$. Take $E=E_0=-\nabla\varphi_0$. For every admissible $D$,
  $\int D\cdot E_0=\int\varphi_0\operatorname{div}D=\int\rho\varphi_0
  =\int|D_0|^2$. Hence
  $\int h_c(D)\ge\int|D_0|^2-\int(|D_0|^2/2+c|D_0|^4)$.

$\blacksquare$

Expanding formally to second order, $D=D_0+c\,\delta D$ with
$\operatorname{div}\delta D=0$, gives
$$U_c=U_0-c\int|D_0|^4+c^2\Bigl[8\int|D_0|^6-8\int|P_\perp(|D_0|^2D_0)|^2\Bigr]
+O(c^3),$$
where $P_\perp$ projects onto divergence-free fields. The transverse term
vanishes for one radial source, which is why 10.2 found $D=D_0$ there.

*Lattice check.* The same proof holds for a grounded $41\times41$ grid
with an edgewise scalar $h_c$. For three unequal point charges, an
independent Newton solve of the concave dual gives:

- primal equals dual to $10^{-12}$;
- remainder/bound $=0.98679,\,0.98091,\,0.92647,\,0.75136,\,0.46049$ at
  $c=10^{-4},10^{-3},10^{-2},0.05,0.2$;
- the second-order coefficient, transverse term included, to $10^{-3}$.

*Consequence for $V(r)$.* For two sources,
$$\bigl|V_c-(V_0-cW_4)\bigr|\le8c^2\max\bigl(I_6(\rho),\,I_6(\rho_1)+I_6(\rho_2)\bigr),$$
where $W_4$ is the interaction part of $\int|D_0|^4$ and $I_6=\int|D_0|^6$.
This bound does not decay with $r$, whereas the $O(c)$ interaction falls
like $r^{-4}$ (the polarizability of Section 5). The law $A/r^4$ is checked
to $10^{-3}$ at $r=10^4$.

For two Gaussians with $R=10$ and charges $\pm0.3$, the relative bound is
$2.13\times10^{-12}$ at $r=50$ and $2.31\times10^{-3}$ at $r=10^4$. Control
is lost at $r_V=4.56\times10^4/m\approx4564R$. The recorded prediction was
hundreds of $R$; the window is an order of magnitude larger. A bound on the
interaction remainder that decays with $r$ is OPEN.

### 11.5 What Section 11 changes

- The threshold bounds of the paper apply outside any non-negative radial
  probe of compact support, at every finite radius, with the same edge
  $M_*$. In particular they apply to the mollified line before $\delta\to0$.
  This is a sufficient condition. A signed source can break $F\ge1$.
- A probe with a non-compact charge tail can dominate its own linear
  profile. With a Gaussian tail, $\Gamma$ falls below $M_*$ (CHECKED).
  Positivity of the vacuum measure does not protect the bound for such
  probes. Whether every non-compact source fails is not claimed.
- With the actual one-loop Dirac measure, the matched first-order profile
  changes sign at $r_x$:
  - $55.91/m$ for the Gaussian, set by the probe tail;
  - $20.48/m$ for the ball and $18.95/m$ for the $C^1$ polynomial probe,
    set by the $2m$ threshold.
- The first-order energy formula of Section 2 now has a two-sided all-$c$
  remainder for arbitrary sources. For $V(r)$ it controls the interaction
  only for $r<r_V$.
- Unchanged and still OPEN or UNRESOLVED:
  - point probes;
  - nonlocal light-by-light corrections near the probe;
  - a decaying remainder for $V(r)$;
  - every statement about full QED.
