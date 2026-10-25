# E4. The massless three-photon tail and the QED window of the pair threshold

23 October 2026. Code: `reproducibility/three_photon_window.py`. Tests:
`tests/test_three_photon_window.py`. The predictions were recorded before any
computation; they are reproduced in `.agent/reports/R2.md`.

**Status.**

- *Coefficient* — CHECKED. Two independent routes agree exactly in rational
  arithmetic:
  $$\rho_\Pi^{3\gamma}(s)=\frac{17}{11\,664\,000}\Bigl(\frac\alpha\pi\Bigr)^4
  \Bigl(\frac{s}{m^2}\Bigr)^4\bigl[1+O(s/m^2)\bigr],\qquad s\ll m^2 .$$
- *Laplace tail* — follows from the coefficient by Watson's lemma:
  $$\Phi_{3\gamma}(r)=\frac{238}{225}\Bigl(\frac\alpha\pi\Bigr)^4
  \frac{1}{m^8r^{10}}\bigl[1+O\bigl((mr)^{-2}\bigr)\bigr].$$
- *Window* — CHECKED (Section 10 supersedes the leading-term numbers of
  Section 7; Section 11 adds the $O(\alpha^5)$ term of the leading
  coefficient). The three-photon model uses six low-energy coefficients of
  the one-loop amplitude, cut off at $s=4m^2$, rather than the full spectral
  density. The leading coefficient carries the factor
  $1+\frac{1555}{153}\frac\alpha\pi$ from the two-loop Euler–Heisenberg
  coefficients. The pair channel is taken at $O(\alpha^2)$. There are two
  criteria, with two radii:
  - $\Gamma\ge2m$ holds only for $r<r_\Gamma=20.64/m$;
  - the pair term exceeds the three-photon term for $r<r_\times=22.55/m$.

  Between the two radii the pair term still dominates $\Phi$, yet
  $\Gamma<2m$ in that model. Section 12 bounds the spectral truncation below
  $s=1.5\,m^2$ with an analytic envelope evaluated in float64. Together with
  a factor-of-two assumption above $1.5\,m^2$, which covers 0.04% of the
  profile, it moves the radii by at most $3\times10^{-4}/m$. This replaces the
  earlier $0.002/m$ estimate. The computed
  $O(\alpha^5)$ term moves both radii in by $0.013/m$. The uncomputed
  $O(\alpha^5)$ parts of the later coefficients, and higher orders, are
  estimated at about $0.003/m$ (the rows of Section 11.5 added linearly)
  and are not bounded either.
- *Novelty* — UNRESOLVED. Groote and Pivovarov give the QCD analogue and the
  $s^4$ law. Beneke and Ruiz-Femenía state that the QED cut from $s=0$ enters
  at $O(\alpha^4)$. Five targeted searches (Section 10.7) found no published
  QED coefficient in this normalization. Abdul Hameed–Chaubey–Shao (2026)
  has only on-shell amplitudes: it checks our box but is not a precedent for
  the density. The fermion-loop $Z\to3\gamma$ literature, which has the same
  off-shell vertex, was not searched. None of this proves novelty.

## 1. Question

Theorem C gives $\Gamma(r)\ge M_*$, where $M_*$ is the bottom of the support of
$\nu$. In full QED the photon self-energy has a cut from $s=0$, through three
real photons, first at $O(\alpha^4)$ (Beneke–Ruiz-Femenía 2016, footnote 1).
So $M_*=0$ and the bound is empty, as the paper's paragraph "The first
threshold need not be charged" says.

The useful question is quantitative. Over what range of $r$ does the $2m$ pair
threshold still control the linear coefficient $\Phi(r)$? Answering it needs
the small-$s$ coefficient of the three-photon density, in this repository's
normalization.

## 2. Conventions

$\rho_\Pi={\rm Im}\,\Pi/\pi$ and $d\nu=\rho_\Pi\,ds$ in the variable
$x=\sqrt s$; this is the paper's measure. One Dirac pair gives
$\rho_\Pi=(\alpha/3\pi)(1+2m^2/s)\beta$.

Groote–Pivovarov (GP) normalize
$12\pi^2i\int\langle Tjj\rangle=(q^\mu q^\nu-q^2g^{\mu\nu})\Pi_{\rm GP}$ (their
eq. 22). So $\rho_{\rm GP}\to1$ for a lepton at high energy, and
$\rho_\Pi=(\alpha/3\pi)\rho_{\rm GP}$. Portolés–Ruiz-Femenía (PRF) use
$\Pi_{\rm PRF}=\Pi_{\rm GP}/12\pi^2$ (their eqs. 1 and 8).

Three expansions are kept apart:

1. in the probe charge $q_W$ — Theorem A concerns the linear coefficient;
2. in the dynamical coupling $\alpha$ — the three-photon cut is $O(\alpha^4)$;
3. the source-nonlinear Euler–Heisenberg term $\propto cq^2/r^6$ of note E3,
   which is not part of the linear coefficient.

## 3. Why the Euler–Heisenberg vertex fixes the leading term

For $s\ll m^2$ every momentum in $\gamma^*\to3\gamma$ is small compared with
$m$. The one-loop box has only massive propagators, so it is analytic there
and its expansion is local. Gauge invariance makes each leg enter through a
field strength, and the lowest term has four field strengths: the
Euler–Heisenberg Lagrangian.

Operators with more derivatives carry at least two more powers of momentum and
contribute from $O(s^5)$ on. This includes $\partial_\mu F^{\mu\nu}$, which
vanishes on shell but not on the virtual leg. The $s^4$ coefficient is
therefore fixed by the Euler–Heisenberg Lagrangian alone (Dunne, eq. 1.9; GP,
eq. 7).

## 4. Route A: the three-body cut

**The vertex.**
$L_{\rm EH}=\kappa e^4P(F)$ with $P=14\,{\rm tr}F^4-5({\rm tr}F^2)^2$ and
$\kappa=1/[180(4\pi)^2m^4]$. Here $P=8(E^2-B^2)^2+56(E\cdot B)^2$, so
$\kappa e^4P=(2\alpha^2/45m^4)[(E^2-B^2)^2+7(E\cdot B)^2]$ (tested).

**The induced current.** A source of the current couples exactly like $eA$.
From $\kappa e^4Q(F,F,F,F)$, with $Q$ the symmetric quartic form of $P$,
$$\langle3\gamma|j^\mu|0\rangle\varepsilon_\mu
=4\cdot3!\,\kappa e^3\,Q(q\wedge\varepsilon,\,k_1\wedge\varepsilon_1,\,
k_2\wedge\varepsilon_2,\,k_3\wedge\varepsilon_3).$$
The factor 4 counts the legs and $3!$ the assignments of the photons.

**The cut.**
$$\rho_\Pi(s)=\frac{e^2}{6\pi s}\,\frac1{3!}\int d\Phi_3
\sum_{\rm pol}(-g_{\mu\nu})M^\mu M^{\nu*},$$
with $1/3!$ for identical photons. The polarization sums are $-g$, which is
exact because $Q$ is gauge invariant in each leg and $q\cdot M=0$. The same
prefactor applied to a Dirac pair reproduces
$(\alpha/3\pi)(1+2m^2/s)\beta$ (tested at four values of $s$).

**Exact evaluation.** Seven centre-of-mass configurations with integer
energies give, with $y_i=s_{jk}/s$ on the simplex $y_1+y_2+y_3=1$,
$$\sum|Q|^2=s^4\Bigl[\tfrac{139}{9}e_2^2-\tfrac{148}{9}e_3\Bigr].$$
Four points fix the four coefficients, and the other three residuals vanish
exactly. With $d\Phi_3=s\,dy_1dy_2/(128\pi^3)$, checked against the recursive
formula, $\int S=17/45$. Hence
$$\rho_\Pi^{3\gamma}=\frac{17}{11\,664\,000}\Bigl(\frac\alpha\pi\Bigr)^4
\Bigl(\frac s{m^2}\Bigr)^4>0.$$

**Amplitude check.** The same $Q$ code gives the low-energy
$\gamma\gamma\to\gamma\gamma$ cross section
$$\frac{d\sigma}{d\Omega}=\frac{139\,\alpha^4\omega^6}{32400\pi^2m^8}
(3+\cos^2\theta)^2,\qquad\sigma=\frac{973\,\alpha^4\omega^6}{10125\pi m^8},$$
as in Gamberg–Kalbfleisch–Milton, hep-ph/9906526, eqs. (42)–(43). This tests
the quartic form, the $4!$ leg counting and the polarization sums together.

## 5. Route B: the published QCD coefficient

GP (hep-ph/0103313), eqs. (22) and (28)–(29), give for a heavy quark
$$\rho_{\rm GP}^{3g}=\frac{17}{243000}\,d^{abc}d^{abc}
\Bigl(\frac{\alpha_s}\pi\Bigr)^3\Bigl(\frac s{4m^2}\Bigr)^4.$$
PRF eq. (8) is the same result in their normalization, reached through a
different Fourier route (differential regularization rather than GP's
configuration-space spectral formula, eq. 30).

**The map to QED.**

- **Legs.** In GP eq. (6) the photon is the single $F$ in $F\cdot G\cdot
  G\cdot G$, and the gluons enter as
  $d^{abc}g_s^3Q(F,G^a,G^b,G^c)$. In QED the source attaches to any of the
  four legs of $\kappa e^4Q(F,F,F,F)$. The induced current is
  $4\kappa e^3Q(\cdot,F,F,F)$, four times what the substitution
  $G\to F$, $d\to1$, $g_s\to e$ gives in GP eq. (15) or PRF eq. (5). The
  density gains $4^2=16$, and $\sum d^{abc}d^{abc}\to1$.
- **Normalization.** $\rho_\Pi=(\alpha/3\pi)\rho_{\rm GP}$, and
  $(s/4m^2)^4=(s/m^2)^4/256$.

$$\frac{17}{243000}\cdot16\cdot\frac13\cdot\frac1{256}=\frac{17}{11\,664\,000},$$
in exact agreement with route A.

The substitution is valid for the effective action, which is what GP's
eq. (7) states. Applied to the current, it would give $1/16$ of the density.
The correct abelian current comes from differentiating the action, where the
source couples to all four legs.

**Independence.** The two routes share only the Euler–Heisenberg Lagrangian.
Route A's amplitude and phase-space integral do not use GP's
configuration-space sunset calculation (their eq. 26).

## 6. The Laplace tail

$$\Phi_{3\gamma}(r)=\int e^{-rx}\rho_\Pi^{3\gamma}(x^2)\,2x\,dx
=\frac{2K\,9!}{r^{10}}=\frac{238}{225}\Bigl(\frac\alpha\pi\Bigr)^4
\frac1{m^8r^{10}},$$
which is $3.08\times10^{-11}/(mr)^{10}$. By Watson's lemma the relative
correction is $O((mr)^{-2})$. An $s^5$ term,
$\rho=Ks^4(1+bs/4m^2)$, multiplies the tail by $1+27.5\,b/(mr)^2$.

## 7. The window at leading order

This section keeps the leading terms only: the one-loop pair profile, and
the $s^4$ density extrapolated as a large-$r$ asymptotic form. Section 10
supersedes its radii. Here $\Phi_{\rm pair}=\int_{2m}e^{-rx}d\nu$ is the exact
one-loop profile, with $\alpha=1/137.035999$ and $m=1$.

| $r$ | $\Phi_{\rm pair}$ | $\Phi_{3\gamma}$ | $\Phi_{3\gamma}/\Phi_{\rm pair}$ | $\Gamma_{\rm total}$ |
|---|---|---|---|---|
| 5 | $1.60\times10^{-8}$ | $3.15\times10^{-18}$ | $2.0\times10^{-10}$ | 2.29444 |
| 10 | $2.62\times10^{-13}$ | $3.08\times10^{-21}$ | $1.2\times10^{-8}$ | 2.14795 |
| 15 | $6.51\times10^{-18}$ | $5.34\times10^{-23}$ | $8.2\times10^{-6}$ | 2.09894 |
| 20 | $1.93\times10^{-22}$ | $3.01\times10^{-24}$ | $0.016$ | 2.05020 |
| 22 | $3.06\times10^{-24}$ | $1.16\times10^{-24}$ | $0.38$ | 1.62491 |
| 25 | $6.28\times10^{-27}$ | $3.23\times10^{-25}$ | $51$ | 0.43166 |
| 30 | $2.17\times10^{-31}$ | $5.21\times10^{-26}$ | $2.4\times10^{5}$ | 0.33334 |
| 40 | $2.92\times10^{-40}$ | $2.94\times10^{-27}$ | $1.0\times10^{13}$ | 0.25000 |

- $\Phi_{\rm pair}=\Phi_{3\gamma}$ at $r_\times=22.6007/m$.
- $\Gamma=2m$ at $r_\Gamma=20.7025/m$. Beyond it $\Gamma$ falls to $10/r$
  within a few units of $1/m$.
- In physical units, with $1/m_e=386.16$ fm: $r_\Gamma\approx7.99$ pm and
  $r_\times\approx8.73$ pm.

**Sensitivity.** Because the pair term is exponential and the tail a power,
an uncertainty in the tail moves the radii only logarithmically.

| Change | $r_\times$ | $r_\Gamma$ |
|---|---|---|
| coefficient $\times2$ or $\times\frac12$ | $\mp0.43$ | $\mp0.42$ |
| $s^5$ term, $\lvert b\rvert\le2$ | $\le0.07$ | $\le0.08$ |
| Sommerfeld factor on the pair (leading Coulomb correction, $O(\alpha)$ relative near threshold) | $+0.04$ | $+0.02$ |

The positronium poles below $2m$ are
$\rho_\Pi\supset\sum_n(m^2\alpha^4/n^3)\,\delta(s-M_n^2)$, with
$M_n=2m-m\alpha^2/(4n^2)$ (Beneke–Ruiz-Femenía, eqs. 7–8). At $r_\times$ they
are $9\times10^{-5}$ of the pair term.

## 8. What this shows and what it does not

- **The linear coefficient in QED.** There are two criteria with two radii.
  At leading order, $\Gamma\ge2m$ holds for $r<20.70/m$, and the pair term
  exceeds the three-photon term for $r<22.60/m$. Between them the pair still
  dominates $\Phi$ (13 times larger at $21/m$), yet $\Gamma=1.958m<2m$.
  Sections 10 and 11 give the final values, $20.64/m$ and $22.55/m$. This quantifies
  "the first threshold need not be charged". It does not contradict
  Theorem C, whose $M_*$ is zero here.
- **Asymptotic regime.** The $s^4$ form is the small-$s$ limit, and its
  Laplace transform is a large-$r$ statement. At $r=0.1/m$ the same formula
  would give $\Phi_{3\gamma}/\Phi_{\rm pair}=2.04$, which is meaningless:
  there the integral is dominated by $s\gg m^2$, outside the expansion.
- **A probe of physical charge $e$.** At $r_\times$ the source-nonlinear term
  of note E3, $cq^2/(\pi^2r^6)$, exceeds $\Phi_{3\gamma}$ by about
  $2\times10^8$. The $2m$ window then closes earlier, near the crossovers of
  note E3: $11.57/m$ in the formal point-source benchmark, and $10.48/m$ and
  $8.95/m$ outside the surface of the two compact probes. The three-photon
  term does not matter there.
- **Omitted at this stage.** Section 10 computes the $s^5$ and higher terms
  and the two-loop pair term. What remains is listed in Section 10.6:
  - $O(\alpha^5)$ corrections to the three-photon cut, which keep the power
    $s^4$;
  - five photons, which start at $O(\alpha^6)$ with $\rho\propto s^8$ and so
    fall like $r^{-18}$.

  None of these is bounded rigorously, so the radii are CHECKED, not PROVED.

## 9. Sources read

All at equation level, from local copies whose SHA-256 is recorded in
`.agent/evidence/R2-literature.json`; the PDFs are not part of the
repository.

- **Groote–Pivovarov, hep-ph/0103313:** §2.1–2.2, eqs. (1)–(12); §3.1,
  eqs. (13)–(15); §4.1, eqs. (22)–(32).
- **Portolés–Ruiz-Femenía, hep-ph/0107324:** eqs. (1)–(9) and (11), and
  footnote 2.
- **Gamberg–Kalbfleisch–Milton, hep-ph/9906526:** eqs. (41)–(43). This is a
  secondary source for the light-by-light cross section; its own source is
  their Ref. [37].
- **Beneke–Ruiz-Femenía, arXiv:1606.02434:** footnote 1, eqs. (7)–(8) and
  footnote 6.

## 10. Beyond the leading term: the full one-loop amplitude (23 October 2026, evening)

Code: `reproducibility/three_photon_amplitude.py`. Tests:
`tests/test_three_photon_amplitude.py`. Predictions and acceptance criteria
were recorded before computing, in `.agent/reports/R5.md`. This section
answers the review `reports/NEXT_STEPS_E4_REVIEW_2026-10-23.md`, step 2.

### 10.1 The amplitude and its checks

The 1PI four-photon vertex of a Dirac loop is
$$\Gamma=-\frac{e^4}{16\pi^2}\sum_{\sigma}J_\sigma,\qquad
J=\int_{\rm simplex}d^3x\Bigl[\frac{N_0}{\Delta^2}-\frac{N_2}{2\Delta}
-\frac{N_4}4\log\Delta\Bigr],$$
summed over the six orderings. Here $N_{0,2,4}$ collect zero, two and four
loop momenta after the Feynman-parameter shift. Each propagator slot is
$m+\lambda\,\slashed v_j(x)$, where $v_j$ is linear in fixed vectors, so every
Dirac trace is computed once and does not depend on $x$. Two uses follow:

- **Expansion.** Scaling the momenta by $\lambda$ gives the low-energy
  polynomial expansion. Each order is a polynomial on the simplex, and the
  rules have sufficient degree of exactness in exact arithmetic. The code
  uses float64/complex128 with rounding error, not exact rational arithmetic.
- **Full value.** Setting $\lambda=1$ gives the unexpanded amplitude.

**The regularization constant.** Dropping the constant of the
log-divergent $l^4$ terms leaves a momentum-independent constant tensor. It
is the same at two different kinematic points. Gauge invariance makes the
true amplitude vanish at zero momenta, so this constant is subtracted.

**Checks.**

1. **Ward identity** on every leg, the virtual one included (contracted
   with $q$). It holds to $10^{-13}$ at every order of the expansion. For
   the full amplitude it is limited only by quadrature: on the virtual leg,
   $3\times10^{-14}$ with $8^3$ nodes and $7\times10^{-17}$ with $11^3$,
   against amplitudes of $2.5\times10^{-2}$.
2. **Bose symmetry** in the photons holds. The odd orders and $\lambda^2$
   vanish to $2\times10^{-15}$.
3. **EH limit, with an absolute normalization not used as input.** The
   $\lambda^4$ term equals $-\frac2{15}Q$ for every polarization, where $Q$
   is the quartic form of route A. The Dalitz integral then gives
   $c_0=17/11\,664\,000$ to $10^{-15}$.
4. **On-shell $\gamma\gamma\to\gamma\gamma$ at low energy.** The helicity
   amplitudes at $\omega^4$ and $\omega^6$ equal those of Dicus, Kao and
   Repko (hep-ph/9709415, Table II, computed independently by expanding the
   electron box with SCHOONSCHIP and FORM). Their eq. (11) at $\omega^4$ and
   at the $\omega^4\times\omega^6$ cross term is reproduced to $10^{-12}$ at
   every angle.
5. **Full one-loop cross section against DKR Table III.** Their Table III
   comes from an exact calculation with Passarino–Veltman functions. We
   compare $R_1=\sigma_{\rm EH}/\sigma_{\rm full}$:

   | $\omega/m$ | 0.25 | 0.35 | 0.45 | 0.55 | 0.65 | 0.75 | 0.85 |
   |---|---|---|---|---|---|---|---|
   | ours | 0.984 | 0.964 | 0.932 | 0.880 | 0.803 | 0.693 | 0.537 |
   | DKR | 0.983 | 0.966 | 0.931 | 0.876 | 0.799 | 0.692 | 0.537 |

   Our values are converged to $10^{-7}$ between $12^3$ and $16^3$ nodes.
   The differences, at most 0.5%, have both signs and no trend. Their own
   $\sigma$ and $R_1$ columns also differ by up to 0.5%.
6. **Series against the full amplitude.** A small-$\omega$ fit of the
   unexpanded amplitude reproduces the expansion coefficients $j_4$, $j_6$
   and $j_8$ (the last to $10^{-4}$). Section 10.2 compares the density at
   $s=1,2,3$.

**The $\omega^8$ disagreement with DKR.** Our $\omega^8$ helicity amplitudes
are exactly half of their Table II entries, for every helicity and angle
tested. Their eqs. (11) and (12) also disagree with each other at this
order. The evidence that the factor of 2 is theirs:

- (i) Our full amplitude contains the $\omega^8$ term. It agrees with their
  full calculation within 0.5% at all seven energies, with no trend.
  Doubling our $\omega^8$ amplitudes would raise $\sigma$ by 0.6% at
  $\omega/m=0.25$, 2.4% at $0.45$ and about 9% at $0.65$.
- (ii) With their coefficient, their own three-term series exceeds their
  full result by an amount that grows with $\omega$: their $R_2=1.001$,
  $1.010$, $1.020$, …. With ours, the remainder is small and positive, and
  consistent between the two lowest energies.

Our total low-energy cross section is
$$\sigma=\frac{1}{45^2}\frac{\alpha^4\omega^6}{\pi m^8}\Bigl[\frac{973}5
+\frac{128}3\frac{\omega^2}{m^2}+123.3975\,\frac{\omega^4}{m^4}+\dots\Bigr],$$
where $123.3975$ agrees with $126976/1029$ to $10^{-13}$, against their
$409792/1715$.

This conclusion rests on one implementation checked against a printed
table, so it is CHECKED, not established.

*Addendum, 24 October.* DKR also give effective Lagrangians at each order,
their eqs. (13)–(15). Heinzl, King and Mercuri-Baron (arXiv:2510.19921, 2025)
re-derived eq. (14) and confirmed it. They quote eq. (15) as $L_{4,4}$
without a check. `lagrangian_amplitudes` evaluates the matrix elements of all
three, with all 24 assignments of the photons to the field strengths:
- eq. (13) gives our $\omega^4$ amplitudes exactly, which fixes the
  conventions;
- eq. (14) gives our $\omega^6$ amplitudes exactly;
- eq. (15) gives exactly twice our $\omega^8$ amplitudes, for every
  polarization at both angles tested.

So DKR are consistent with themselves: their Lagrangian agrees with their
Table II, at twice our value. If the factor is theirs, as (i) and (ii) above
suggest, it entered their $\omega^8$ expansion upstream of both, and the 2025
quotation repeats it. That remains CHECKED, not established.

*Second addendum, 24 October: an independent calculation.* Abdul Hameed,
Chaubey and Shao (arXiv:2604.00099, 2026) give the one-loop low-energy
helicity amplitudes to $s^7$: eq. (22) and the ancillary `anc/Amp1L_LE.wl`.
Polarization sums do not depend on the basis. So for each pair of orders,
our box's bilinear summed over linear polarizations must equal theirs summed
over the 16 helicities. We compared every pair of orders from $\lambda^4$ to
$\lambda^{14}$, at four angles. They agree to $4\times10^{-16}$, with the
normalization exactly 1. This includes $\omega^8$, where their
$-\frac{1}{945}(s^2+t^2+u^2)^2$ in $M_{++++}$ is our value. The factor of 2
is therefore DKR's.

The test is `test_box_equals_the_published_one_loop_expansion_to_omega14`;
the evidence is `.agent/evidence/R11-literature-2604.00099.json`. The user's
other session first noticed the agreement (`reports/review_2026-10-24`). It
was re-derived here independently. It does not touch $c_1$, which
needs only the $\omega^6$ structure, numerically checked in item 4. $c_2$ moves
the radii by less than $0.007/m$.

### 10.2 The density beyond $s^4$

$\rho_\Pi/(\alpha/\pi)^4=\sum_nc_n\,s^{4+n}$ with $m=1$. The coefficients
were computed with rules that are exact for each order, to $s^9$:

| $n$ | $c_n$ | $c_n/c_0$ in units of $(s/4m^2)^n$ |
|---|---|---|
| 0 | $1.4574759945\times10^{-6}=17/11\,664\,000$ | 1 |
| 1 | $6.838297733\times10^{-7}$, $c_1/c_0\approx335/714$ | 1.876751 |
| 2 | $2.238138258\times10^{-7}$ | 2.457002 |
| 3 | $6.360593981\times10^{-8}$ | 2.793034 |
| 4 | $1.685409710\times10^{-8}$ | 2.960357 |
| 5 | $4.295553129\times10^{-9}$ | 3.017989 |

In the notation of Section 7, $b=1.877$: the correction is positive. The
observed ratios decrease (1.88, 1.31, 1.14, 1.06, 1.02), consistent with the
expected pair-threshold singularity at $s=4m^2$. Finitely many ratios do not
establish a radius of convergence. The rational value $335/714$ is a numerical
reconstruction, not an exact derivation from this floating-point computation.

The unexpanded amplitude gives the density at $s=1,2,3$:

| $s$ | full/series (6 terms) | estimated series tail | full/leading term |
|---|---|---|---|
| 1 | 1.00058 | $\approx5.9\times10^{-4}$ | 1.68 |
| 2 | 1.029 | $\approx2.9\times10^{-2}$ | 3.27 |
| 3 | 1.297 | $\approx0.25$ | 8.59 |

The full values match the series plus its estimated tail.

### 10.3 The pair channel at $O(\alpha^2)$

The irreducible two-loop density is that of Laporta and Jentschura
(arXiv:2403.07127, eq. 55). Their one-loop term, eq. (28), is
$(\alpha/6)v(3-v^2)$, which is $\pi\rho_\Pi^{(1)}$ here, so the conventions
agree. Checked:

- the bracket tends to $\pi^2/4$ at threshold, i.e.
  $\rho^{(2)}\to\alpha^2/4$, the first Coulomb term;
- it tends to $1/4$ at high energy, i.e. ${\rm Im}\,\Pi_2\to\alpha^2/4\pi$;
- near threshold $\rho^{(2)}/\rho^{(1)}\to\pi\alpha/2v$, approached linearly
  in $v$.

No separate Sommerfeld factor is added: that would double count. The
reducible Dyson term $\Pi_1^2$ is $O(\alpha)$ relative, without threshold
enhancement. It is not included and is estimated in Section 10.6.

### 10.4 The two radii

The three-photon density is the series to $s^9$ for $s\le4m^2$. The pair
channel is at $O(\alpha^2)$. Units $1/m$:

| Probe | $r_\times$ (pair = 3γ) | $r_\Gamma$ ($\Gamma=2m$) |
|---|---|---|
| point, one-loop pair, leading 3γ (Section 7) | 22.6007 | 20.7025 |
| point, one-loop pair, 3γ series to $s^9$, cutoff $4m^2$ | 22.5346 | 20.6295 |
| **point, two-loop pair, same truncated 3γ model** | **22.5675** | **20.6490** |
| ball, $a=10/m$, full exterior factor | 30.7413 | 28.8838 |
| $C^1$ polynomial, $a=10/m$, full exterior factor | 29.4081 | 27.5754 |

- **Two criteria.** At $21/m$ the pair term is still 12.2 times the
  three-photon term, yet $\Gamma=1.9499\,m$. Beyond $r_\times$, $\Gamma$ falls
  towards $10/r$: 0.438 at $25/m$, 0.337 at $30/m$.
- **Size of the correction.** The three-photon profile exceeds its leading
  term by 30% at $15/m$, 15% at $20/m$ and 9% at $25/m$.
- **Physical units.** $r_\Gamma=7.97$ pm and $r_\times=8.71$ pm.

These radii have the one-loop three-photon vertex. Section 11.4 adds the
$O(\alpha^5)$ term of the leading coefficient, which moves every radius in by
about $0.013/m$.

### 10.5 Probe size and charge

**Size.** For a compact probe, both radii move outwards by about $8.2/m$ at
$a=10/m$. The first size correction to the three-photon term is
$110\langle u^2\rangle/(6r^2)=2.57$ at $r_\Gamma$ for the ball, so a
truncated size expansion fails. The radii above use the full exterior
factor $F$ of note E3, Section 11.1, on the whole measure, valid for $r>a$.

**Charge.** Compare the three-photon tail with the probe's own
Euler–Heisenberg tail, $cq^2/(\pi^2r^6)$.

- The three-photon tail ends the $2m$ window first only for very small
  charges: $q<9.4\times10^{-5}e$ (point), $9.3\times10^{-5}e$ (ball),
  $8.0\times10^{-5}e$ (polynomial). The tails are compared at $r_\Gamma$.
  With the $O(\alpha^5)$ term these become 9.5, 9.4 and
  $8.1\times10^{-5}e$ (Section 11.4).
- For $q=e$, the pair term equals the EH tail at $11.590/m$ (point),
  $20.492/m$ (ball) and $18.959/m$ (polynomial). These match the crossovers
  of note E3, shifted slightly by the two-loop pair term.

For a probe of charge $e$, then, the EH tail sets the window, and $r_\Gamma$
applies to the linear coefficient only.

### 10.6 Error budget for $D(r)=M_1-2mM_0$

The sign of $D$ is the sign of $\Gamma-2m$. At $r_\Gamma$:
$D_{\rm pair}=-D_{3\gamma}=3.735\times10^{-24}$ and
$dD/dr=-6.12\times10^{-24}$.

| Component | Status | Effect on $r_\Gamma$ |
|---|---|---|
| quadrature | computed | $<10^{-6}$ |
| three-photon series truncation and $1<s<4$ (0.34% of model $D_{3\gamma}$) | sensitivity scenario: three full-density samples do not bound an interval; factor $\le2$ up to $s=4$ is an additional unproved assumption | estimated $0.002$ under that assumption |
| three-photon part above $4m^2$ | estimated: $\alpha^3$ relative to the pair term | $<10^{-5}$ |
| three-photon cut at $O(\alpha^5)$ | estimated: the two-loop EH correction to $\gamma\gamma\to\gamma\gamma$ is $+\frac{186685}{17514}\frac\alpha\pi=2.5\%$ (DKR, note 10). Replaced in Section 11.5: computed for the leading coefficient | $\approx\mp0.015$; computed: $-0.0126$ |
| pair at $O(\alpha^3)$, and the reducible $\Pi_1^2$ | estimated | $\lesssim0.001$ |
| positronium | computed (Beneke–Ruiz-Femenía, eqs. 7–8) | $\sim10^{-4}$ |
| five photons | $O(\alpha^6)\,s^8$ | negligible |

The radii:

- $r_\Gamma=20.649/m$ in the six-term cutoff model;
- $r_\times=22.567/m$ in the same model;
- a $\pm2.5\%$ band on the three-photon term moves each by $\pm0.016/m$.

Under the stated sensitivity assumptions the transition lies near
$20.63<r<20.67$. This is not a certified interval or an unconditional
fixed-sign result for physical $D$: the spectral remainder and higher orders
have not been bounded uniformly. The radii stay CHECKED as model results.
Section 11.5 updates this budget with the computed $O(\alpha^5)$ term.

### 10.7 Novelty search

Five targeted searches found no published QED coefficient of the low-$s$
three-photon density. They covered the three-photon cut and photon spectral
function; four-loop QED vacuum polarization; low-energy light-by-light
beyond $\omega^6$; and the Källén–Sabry closed form.

The closest results:

- **Groote–Pivovarov and Portolés–Ruiz-Femenía:** QCD, heavy-quark current.
- **Baikov, Maier and Marquard (arXiv:1307.6105):** the four-loop QED
  low-energy moments with singlet diagrams, only to $z^3$. The
  three-photon logarithm enters at $z^4$.
- **Maier and Marquard (arXiv:1710.03724):** a fourth moment, for the QCD
  heavy-quark case (abstract only; not read).

Novelty is UNRESOLVED; the searches are not exhaustive.

Two later points (24 October 2026):

- **Abdul Hameed, Chaubey and Shao (arXiv:2604.00099), read in R11.**
  - They expand the on-shell four-photon amplitudes at low energy.
  - They have no off-shell photon, no three-photon cut and no
    vacuum-polarization density.
  - Their work checks our box on shell (Section 10.1). It is not a
    precedent for the density.
- **Not searched: the fermion-loop amplitude for $Z\to3\gamma$.**
  - Only the vector coupling contributes there. By $C$-parity the axial
    part drops out with three photons.
  - So it is the $\gamma^*(q^2)\to3\gamma$ vertex at $q^2=M_Z^2$.
  - Its heavy-fermion limit is our low-$s$ expansion. A width computed in
    that limit would fix the leading coefficient up to normalization.

### 10.8 Sources read for this section

At equation level, with SHA-256 in `.agent/evidence/R5-literature.json`:

- **Dicus–Kao–Repko, hep-ph/9709415:** eqs. (1), (2), (10)–(15),
  Tables I–III, note [10].
- **Laporta–Jentschura, arXiv:2403.07127:** eqs. (19), (28), (52)–(55), and
  their comparison with the literature.
- **Baikov–Maier–Marquard, arXiv:1307.6105:** Section 2.1.

## 11. Two loops: the $O(\alpha^5)$ term of the leading coefficient (24 October 2026)

Code: `three_photon_window.three_photon_two_loop`, `gamma_gamma_two_loop`,
`self_dual_two_loop_ratio`, and `three_photon_amplitude.profile_moments` with
`three_photon_loops=2`. Tests: `tests/test_three_photon_window.py` and
`tests/test_three_photon_amplitude.py`. The predictions are in
`.agent/reports/R8.md`.

### 11.1 Why the two-loop Euler–Heisenberg coefficients fix it

Below $4m^2$ the three-photon cut of the 1PI self-energy at $O(\alpha^5)$ is
$2\,{\rm Re}(M_1^*M_2)$, where $M_1$ and $M_2$ are the one- and two-loop
$\gamma^*\to3\gamma$ vertices.

- Every cut of the two-loop four-photon function crosses the fermion loop.
  So $M_2$ is analytic below $4m^2$, and its expansion in momenta starts with
  the constant-field quartic term, the two-loop Euler–Heisenberg Lagrangian.
- Two fermion loops joined by a fourth photon vanish by Furry's theorem: each
  loop then has five attachments.
- A vacuum-polarization insertion on a cut photon leaves the residue at
  $k^2=0$ equal to one in the on-shell scheme. Its continuum starts at $4m^2$.
- An insertion on the external leg is not 1PI.
- Operators that vanish on shell carry more derivatives, so they enter at
  higher order in $s$, as at one loop (Section 3).

At leading order in $s$, the $O(\alpha^5)$ term is therefore fixed by the
two-loop weak-field coefficients alone.

### 11.2 The coefficients and two checks

Write $L=c_1X^2+c_2Y^2$ with $X=\mathbf E^2-\mathbf B^2$ and
$Y=\mathbf E\cdot\mathbf B$. At one loop $c_1=2\alpha^2/45m^4$ and
$c_2=7c_1$ (Dunne, hep-th/0406216, eq. (1.9)). Ritus's two-loop result is
$$c_1\to c_1\Bigl(1+\frac{40}{9}\frac\alpha\pi\Bigr),\qquad
c_2\to c_2\Bigl(1+\frac{1315}{252}\frac\alpha\pi\Bigr).$$
It is read in Dunne, eq. (4.11), as
$(e^6/64\pi^4m^4)[\frac{16}{81}X^2+\frac{263}{162}Y^2]$, and stated in this
form by Ravndal (hep-ph/9708449, Section 3), who adds that Reuter, Schmidt
and Schubert confirmed it. Ritus's paper itself was not read.

Two checks, each from an independent computation quoted in the same review:

- **Magnetic background,** Dunne eq. (4.15). The leading term
  $\frac{e^2m^4}{(4\pi)^4}\frac{64}{81}(eB/m^2)^4$ equals
  $\frac{16}{81}\frac{\alpha^3}{\pi m^4}B^4$. Against
  $\frac{2}{45}\frac{\alpha^2}{m^4}B^4$, this gives $40/9$.
- **Self-dual background,** Dunne eqs. (6.2) and (6.6), Dunne–Schubert's
  closed forms. Expanding at large $\kappa=m^2/2ef$ gives quartic terms
  $-\frac{2}{15}\frac{\alpha^2}{m^4}f^4$ at one loop and
  $-\frac56\frac{\alpha^3}{\pi m^4}f^4$ at two loops. Their ratio is
  $\frac{25}{4}\frac\alpha\pi$. A self-dual field has $X^2=4\epsilon^4$ and
  $Y^2=-\epsilon^4$ in Ritus's eigenvalues, so it measures $4c_1-c_2$.
  Ritus's numbers give $(4\cdot\frac{40}{9}-7\cdot\frac{1315}{252})/(4-7)=\frac{25}{4}$.
  With $40/9$ from the magnetic case, this fixes $1315/252$.

`self_dual_two_loop_ratio` does this expansion. The test also compares both
expansions with direct evaluation at $\kappa=1000$.

**A third, independent check: the two-loop amplitudes themselves**
(added 24 October). Abdul Hameed, Chaubey and Shao (arXiv:2604.00099)
give the two-loop low-energy helicity amplitudes (`anc/Amp2L_LE.wl`); QED
follows from their gluon exchange with $\alpha_sC_F\to\alpha$. Divide their
leading two-loop terms by the one-loop ones:
- all-plus, $\propto a-b$: $(5/12)/(1/15)=\frac{25}{4}$;
- mixed, $\propto a+b$: $(391/324)/(11/45)=\frac{1955}{396}$.

These are exactly the combinations of $40/9$ and $1315/252$ given in
Section 11.3. Their two-loop amplitudes therefore confirm both of Ritus's
coefficients, the γγ factor $25555/2502$, and the sign reversal in DKR's
note [10]. Test: `test_two_loop_coefficients_from_the_published_two_loop_amplitudes`.

### 11.3 How the two invariants enter each rate

Let $a=c_1/4$ and $b=c_2/16$ be the coefficients of $(F_{\mu\nu}F^{\mu\nu})^2$
and $(F_{\mu\nu}\tilde F^{\mu\nu})^2$; at one loop $a:b=4:7$. Route A's exact
arithmetic, with the quartic form split into its two invariants, gives:

- **$\gamma\gamma\to\gamma\gamma$:**
  $\sum_{\rm pol}|M|^2\propto(3+\cos^2\theta)^2\,[2(a-b)^2+(a+b)^2]$ at every
  angle. A helicity count gives the same weights. All-plus amplitudes are
  $\propto a-b$ and mixed ones $\propto a+b$, and
  $s^4+t^4+u^4=\frac12(s^2+t^2+u^2)^2$. At one loop
  $2\cdot9+121=139$, the 139 of $973=7\cdot139$.
- **The three-photon density:** $\rho\propto5(a-b)^2+3(a+b)^2$. At one loop
  $45+363=408=24\cdot17$, the 17 of $17/11\,664\,000$.

At two loops $a-b$ gains $\frac{25}{4}\frac\alpha\pi$ and $a+b$ gains
$\frac{1955}{396}\frac\alpha\pi$. Hence:
$$\sigma_{\gamma\gamma}\to\sigma_{\gamma\gamma}\Bigl(1+\frac{25555}{2502}\frac\alpha\pi\Bigr),\qquad
\rho_\Pi^{3\gamma}\to\rho_\Pi^{3\gamma}\Bigl(1+\frac{1555}{153}\frac\alpha\pi\Bigr)
\quad\text{(leading coefficient)}.$$
Numerically $1555/153=10.163$, and the leading coefficient grows by 2.36%.

**Dicus–Kao–Repko, note [10].** From the same coefficients they give the
factor $1+\frac{186685}{17514}\frac\alpha\pi$ for their Eqs. (1), (10) and
the first term of (12), the unpolarized cross section. The weights above
give $\frac{178885}{17514}=\frac{25555}{2502}$ instead.

Write the factor as $2\delta_2+w(\delta_1-\delta_2)$, with
$\delta_1=\frac{40}{9}$ and $\delta_2=\frac{1315}{252}$. Here $w/2=20/139$ is
the part of the one-loop rate carried by $c_1$: $48-28=20$ of 139, in the
form $48c_1^2-8c_1c_2+3c_2^2$. With $w=+\frac{40}{139}$ this is our value.
With $w=-\frac{40}{139}$ it is exactly theirs. So their factor is ours with
the sign of one term reversed. That suggests a sign slip, but we have no
access to their calculation.

The difference is 4% of the correction and 0.1% of $\sigma$. Section 10.6
used their factor as a 2.5% estimate; it is replaced below.

### 11.4 The radii

The factor multiplies the leading coefficient only. The $O(\alpha^5)$ parts
of the $s^5,\dots,s^9$ coefficients are not computed. Units $1/m$:

| Probe | $r_\times$, one-loop 3γ | $r_\times$, with $O(\alpha^5)$ | $r_\Gamma$, one-loop 3γ | $r_\Gamma$, with $O(\alpha^5)$ |
|---|---|---|---|---|
| point | 22.5675 | **22.5544** | 20.6490 | **20.6364** |
| ball, $a=10/m$ | 30.7413 | 30.7284 | 28.8838 | 28.8713 |
| $C^1$ polynomial, $a=10/m$ | 29.4081 | 29.3952 | 27.5754 | 27.5629 |

- **Shifts.** Every radius moves in by 0.0125–0.0130$/m$. At $21/m$ the
  pair term is 11.96 times the three-photon term, and $\Gamma=1.9476\,m$.
- **Physical units:** unchanged at three digits: $r_\Gamma=7.97$ pm,
  $r_\times=8.71$ pm.
- **Charge.** The thresholds of Section 10.5 compare the three-photon tail
  with the probe's EH tail at $r_\Gamma$; that criterion reproduces their
  values. They become $q<9.5\times10^{-5}e$ (point), $9.4\times10^{-5}e$
  (ball), $8.1\times10^{-5}e$ (polynomial). Compared at $r_\times$ instead,
  they would be $7.8$, $7.6$ and $6.6\times10^{-5}e$. The EH crossovers for
  $q=e$ do not involve the three-photon term and are unchanged.
- **Sensitivity to the uncomputed terms.** Multiplying all six coefficients
  by the same factor moves the point radii in by a further 0.0015 ($r_\times$)
  and 0.0016 ($r_\Gamma$).

### 11.5 Error budget (replaces the $O(\alpha^5)$ row of Section 10.6)

At $r_\Gamma$, with the $O(\alpha^5)$ term:
$D_{\rm pair}=-D_{3\gamma}=3.837\times10^{-24}$ and
$dD/dr=-6.29\times10^{-24}$.

| Component | Status | Effect on $r_\Gamma$ |
|---|---|---|
| $O(\alpha^5)$, leading coefficient | computed, included | $-0.0126$ (included) |
| $O(\alpha^5)$, coefficients of $s^5$ to $s^9$ | not computed; the same factor as an estimate | $\approx\mp0.002$ |
| $O(\alpha^6)$ | estimated as $(10\alpha/\pi)^2$; three-loop coefficients not known | $\approx3\times10^{-4}$ |

The other rows of Section 10.6 stand: quadrature, the series truncation
with $1<s<4$ (0.002 under its unproved assumption), the part above $4m^2$,
the pair at $O(\alpha^3)$, positronium and five photons.

The radii in this model are $r_\Gamma=20.636/m$ and $r_\times=22.554/m$,
CHECKED as model results. Under the stated estimates the transition lies near
$20.63<r<20.64$. This is not a certified interval: the spectral remainder
and the higher orders are still not bounded uniformly.

### 11.6 Sources read for this section

At equation level, with SHA-256 in `.agent/evidence/R8-literature.json`:

- **Dunne, hep-th/0406216:** eqs. (1.9), (4.11), (4.15), (6.2)–(6.6).
- **Ravndal, hep-ph/9708449:** Section 3, the two-loop couplings.
- **Reuter–Schmidt–Schubert, hep-th/9610191:** searched for the weak-field
  numbers; it gives the magnetic integral representation, not these
  coefficients.
- **Dicus–Kao–Repko, hep-ph/9709415:** note [10] and Eqs. (1), (10), (12)
  re-read.

## 12. An envelope for the truncation remainder (24 October 2026)

Code: `three_photon_amplitude.amplitude_envelope`, `density_envelope`,
`amplitude_products`, `truncation_moment_bounds`. Tests:
`tests/test_three_photon_envelope.py`. Record: `.agent/reports/R9.md`,
with the predictions written before computing.

The bound is analytic and is evaluated in float64. It is CHECKED, not
certified.

### 12.1 The bound

Take the momenta of $s=1$ and scale them by $\lambda=\sqrt s$. In the
Feynman form of each ordering, $\Delta=1-\lambda^2R(x)$, where
$$R=x_0x_3+s_a\,x_0x_2+s_b\,x_1x_3 ,$$
and $s_a+s_b\le1$ are two of the Dalitz invariants.

**Lemma.** $0\le R\le\frac14$ on the simplex.

*Proof.* Put $t=s_a$. Then
$R\le x_0x_3+t\,x_0x_2+(1-t)\,x_1x_3$, which is at most
$(x_0+(1-t)x_1)(x_3+t\,x_2)$. By the arithmetic–geometric mean that product
is at most $\frac14$.

The same comparison gives the moments. $\int R^n$ is at most the integral of
the $n$-th power of the right-hand side. That integral is convex in $t$, so
it peaks at $t=0$ or $t=1$, and both give
$$\int_{\rm simplex}R^n\le I^*(n)=\int x_3^n(x_0+x_1)^n=\frac{n!\,(n+1)!}{(2n+3)!}.$$
This is a Dirichlet$(1,2,1)$ moment.

**Numerators.** The polarizations are spatial unit vectors, so
$\|\not e\|=1$; also $\|\gamma^\alpha\|=1$ and $|{\rm Tr}\,M|\le4\|M\|$. A
slot of degree one is $\not K_j-\sum_ix_i\not K_i$. Every $K_i^0$ lies in
$[-1,0]$ and $|\mathbf K_i|\le\frac12$, so its norm is at most 2. Hence
- $|N_0^{(j)}|\le4\binom4j2^j$;
- $|N_2^{(j)}|\le96\binom2j2^j$;
- $|T_4|\le192$.

**Tails.** With $u=\lambda^2R\le s/4$:
- $\sum_{n\ge n_0}(n+1)u^n\le(n_0+1)u^{n_0}/(1-s/4)^2$;
- $\sum_{n\ge n_0}u^n\le u^{n_0}/(1-s/4)$;
- $\sum_{n\ge n_0}u^n/n\le u^{n_0}/(n_0(1-s/4))$.

Here $n_0$ is the first order beyond $K$. Adding the tails over the six
orderings gives $E(s)$, with $|A-A_K|\le E$ at every Dalitz point and for
every polarization.

**Density.** Since $\rho=\frac1{4608}\int\sum_{\rm pol}|A|^2$ over the
triangle of area $\frac12$ with 24 polarizations, Cauchy–Schwarz gives
$$|\rho-\rho_K|\le2\sqrt{\rho_K\,\epsilon}+\epsilon,\qquad\epsilon=E^2/384 .$$
Here $\rho_K=\sum_{a,b\le K}M_{ab}\,s^{(a+b)/2}$ is the density of the
truncated amplitude; it keeps the cross terms beyond $s^9$ that the six-term
model drops.

### 12.2 Checks against the code

The checks ran at five Dalitz points: two interior points, the collinear
pairs $y_3=0$ and $y_1=0$, and a soft photon. All six orderings were used.

- $R\in[0,\frac14]$ at every node.
- The code's own quadrature of $R^n$, exact up to $n=12$, stays below
  $I^*(n)$.
- Slot norms are at most 2.
- $|N_0|$, $|N_2|$ and $|T_4|$ stay below their bounds.

The unexpanded amplitude minus its truncation, at $K=8$ and 12 and
$s=0.5$ to $1.5$, stays below $E$ everywhere. The ratio $E/|A-A_K|$ is 4000
to 5600, almost independent of $s$ and $K$. The bound therefore has the right
rate, $s/4$ per order, and a crude constant. Its source is the absolute sum
over orderings, which ignores their gauge cancellation.

### 12.3 The truncated density at $K=22$

`amplitude_products(22, 13, 12)` took 1508 s. Both quadrature rules are exact
at this order. The products are stored as `PRODUCTS_K22`.

- Their anti-diagonals reproduce the six stored coefficients of Section 10.2
  to $2\times10^{-15}$.
- The forbidden orders vanish to $1.7\times10^{-15}$.

The high-order coefficients come from sums over orderings with heavy
cancellation, so their relative float error is larger. It is still absolutely
far below $E$.

| $s/m^2$ | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|
| bound on $\lvert\rho-\rho_K\rvert/\rho_K$ | $1.0\times10^{-5}$ | $5.5\times10^{-4}$ | $9.8\times10^{-3}$ | 0.096 | 0.71 | 57 |
| $(\rho_K-\rho_6)/\rho_6$ | $1.0\times10^{-5}$ | $1.1\times10^{-4}$ | $5.8\times10^{-4}$ | $2.1\times10^{-3}$ | $5.8\times10^{-3}$ | 0.028 |

### 12.4 What it implies for the radii

Split the density at $s_1$:
- for $s\le s_1$, use the bound plus the computed $|\rho_K-\rho_6|$;
- for $s_1<s<4m^2$, assume the six-term model is right within a factor of
  two, $|\rho-\rho_6|\le\rho_6$.

$|\delta D|$ is the integral of $|x-2|\,e^{-rx}\,2x\,|\delta\rho|$, and
$|\delta r_\Gamma|\le|\delta D|/|dD/dr|$. For $r_\times$, the relative change
of $\Phi_{3\gamma}$ is divided by the difference of the two log-slopes. Both
are first-order estimates, ample at this size. Point probe, units $1/m$ (`.agent/evidence/R9-window-bound.json`):

| $s_1$ | $r_\Gamma$: bounded | $r_\Gamma$: assumed | share of $\Phi_{3\gamma}$ above $s_1$ | $r_\times$: bounded + assumed |
|---|---|---|---|---|
| 1.0 | $2.6\times10^{-5}$ | $2.1\times10^{-3}$ | 0.56% | $1.1\times10^{-3}$ |
| 1.25 | $7.4\times10^{-5}$ | $4.7\times10^{-4}$ | 0.15% | $2.7\times10^{-4}$ |
| **1.5** | $1.6\times10^{-4}$ | $1.2\times10^{-4}$ | 0.042% | $1.4\times10^{-4}$ |
| 1.75 | $3.2\times10^{-4}$ | $3.0\times10^{-5}$ | 0.013% | $1.7\times10^{-4}$ |

With $s_1=1.5\,m^2$, the spectral truncation moves $r_\Gamma$ by at most
$2.8\times10^{-4}/m$ and $r_\times$ by at most $1.4\times10^{-4}/m$.

- Of this, $1.6\times10^{-4}$ in $r_\Gamma$ is bounded.
- The rest rests on the factor-of-two assumption above $1.5\,m^2$, a region
  carrying 0.04% of $\Phi_{3\gamma}$.
- The part above $4m^2$ is separate (Section 10.6, $<10^{-5}$).

This replaces the 0.002/m estimate of Section 10.6. That estimate needed the
factor-of-two assumption on the whole range $1<s<4$.

### 12.5 Status

The truncation bound is an analytic bound evaluated in float64, CHECKED
against the code and the unexpanded amplitude; it is not certified. The window
is still not certified, because of three pieces outside this bound:
- the region above $1.5\,m^2$, under its assumption;
- the three-photon cut above $4m^2$;
- the uncomputed orders in $\alpha$, about $0.003/m$ (Section 11.5), which
  now dominate.

The ball and polynomial radii of Section 11.4 carry no truncation bound yet.
`truncation_moment_bounds` accepts their exterior factors, but it was run for
the point probe only.
