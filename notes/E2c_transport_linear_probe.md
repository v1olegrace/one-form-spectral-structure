# E2c — From ⟨FF⟩ to the static observables, at linear order in the probe

Working note, 1 October 2026. Roadmap obligation 2 of E2.4 (O2 of D5 in
`DECISIONS.md`): transport the positivity of ⟨FF⟩ to the static kernel through
the Wilson loop, with the tensor projection, the sign, the contact terms, the
perimeter and the limit T → ∞ each accounted for.

**Status.** Proved here, conditionally on a positive Euclidean spectral
representation of ⟨FF⟩, hypothesis (E) below. Section 11 (3–5 October)
derives the $T$ part of (E) from the Källén–Lehmann form of note E2b
(`notes/E2b_tensor_classification.tex`) without locality, because that part
is automatically two-point local. The massless helicity term is excluded only
by (B<sub>T</sub>), whose content on the plane $\tau=0$ is, given E2b's form,
two-point locality in that sector: the premise has moved from (E) into
(B<sub>T</sub>), not disappeared. E2b's form itself rests on two
measure-theoretic lemmas (Bochner–Schwartz; covariant disintegration over
orbits) not yet checked against primary sources. The algebraic identities and the
numerical steps listed in Section 9 are machine-checked in
`tests/test_e2c_transport.py`; the distributional steps (restriction to the
rectangle and to the half-plane, the product $\delta(p_0)/p_1$) are not.
Nothing here concerns the probe beyond the quadratic cumulant, the nonabelian
theory, or the existence of four-dimensional QED.

**Corrections of 3 October 2026**, after the audit of 2 October
(`reports/AUDITORIA_SEVERA_E2C_2026-10-02.md`), each checked by computation
before it was applied:

1. The boundary display of Lemma 2 carried a spurious factor 2 on both
   bilateral integrals. The code, $C(r)$ and every number in Section 9 always
   used the correct coefficient, so no measured value changes.
2. The rate of Proposition 3 holds at fixed regulator and carries $q_W^2$:
   $q_W^2C_\varepsilon(r)/T$. $C_\varepsilon$ has no limit as $\varepsilon\to0$
   (Section 4). The audit's asymptotic coefficient $r/(2\pi^2\sqrt\varepsilon)$
   is itself wrong; the exact one is $\sqrt\pi\,r/(4\pi^2\sqrt\varepsilon)$,
   and the other term diverges logarithmically rather than staying finite.
3. The area term from a local contact $c\,G$ has a slope that diverges like
   $1/\varepsilon$: a regulated contact, not a finite string tension, and not
   the nonlocal function $D$ of the stochastic vacuum model (Sections 7, 8).
4. The Euclidean representation is now hypothesis (E), stated. Section 11
   derives its $T$ part from E2b's form; the helicity part is excluded by
   (B<sub>T</sub>), which in that sector amounts to two-point locality.
5. The output is a positive Stieltjes kernel. It has the form of the paper's
   Hypothesis 3 only with the Coulomb weight $\mu(\{0\})>0$, with the integral
   starting at $\inf\operatorname{supp}\sigma$; that this lower limit is
   positive is the gap of Hypothesis 2, a further, separate input.
6. "Linear order" means truncation at the quadratic cumulant. The cubic
   cumulant vanishes only if the state is charge-conjugation invariant; the
   connected four-field cumulant is $O(q_W^4)$, and calling it light-by-light
   presupposes the dynamics.

## 0. The result in one paragraph

Let the Euclidean two-point function of a two-form field $F$ have the positive
spectral form (E) of Section 1, with Källén–Lehmann measure $\mu\ge0$.
Section 11 obtains the $T$ part of (E) from E2b's form under the Wightman
axioms W1–W3 (no locality, no CPT, no parity); the helicity part is excluded by
(B<sub>T</sub>), which on $\tau=0$ amounts to two-point locality in that
sector. E2b's form rests on two lemmas not yet checked. Let it satisfy
the Bianchi identity *including coincident points* (B<sub>T</sub>) and
$\int d\mu/(1+s)<\infty$ (I). Then, truncating at the quadratic cumulant in the
probe charge (L), both the static potential of a Wilson loop and the field of
a static line depend on the two-point function only through
$$a^{(3)}(r)=\int_{[0,\infty)}d\mu(s)\,\frac{e^{-\sqrt s\,r}}{4\pi r},\qquad \mu\ge0 .$$
For $r>0$ the static kernel is therefore the positive Stieltjes function
$\int d\mu(s)/(Q^2+s)$, up to a contact polynomial that does not reach $r>0$,
and the linear-response relation of Hypothesis 5 holds. This has the form of
Hypothesis 3 of the paper, with $g_R^2=\mu(\{0\})$, $\sigma=\mu|_{(0,\infty)}$
and the integral starting at $\inf\operatorname{supp}\sigma$, only when the
Coulomb weight $\mu(\{0\})$ is positive. That lower limit may be $0$; the gap
of Hypothesis 2, which makes it positive, is not implied. The massless helicity term that E2b could remove
only through CPT never reaches either observable. What (B<sub>T</sub>)
excludes is the local structure $G=\delta\delta-\delta\delta$; a contact
$c\,G$ gives an area term whose regulated coefficient diverges as the
regulator is removed, so it is not a finite string tension. The same tensor
structure multiplies the function $D$ of the stochastic vacuum model
(Section 8), but a local contact is not that nonlocal function.

## 1. Setting

Euclidean conventions, metric $\delta_{\mu\nu}$, index 0 the Euclidean time. Write
$$T^E_{\mu\nu\rho\sigma}(p)=p_\mu p_\rho\delta_{\nu\sigma}-p_\nu p_\rho\delta_{\mu\sigma}-p_\mu p_\sigma\delta_{\nu\rho}+p_\nu p_\sigma\delta_{\mu\rho},
\qquad G_{\mu\nu\rho\sigma}=\delta_{\mu\rho}\delta_{\nu\sigma}-\delta_{\mu\sigma}\delta_{\nu\rho},$$
$T^\star$ for $T^E$ dualised on either pair, and $\epsilon$ for the Levi-Civita
symbol. One identity is used repeatedly: the dual structure satisfies
$\epsilon\epsilon pp = p^2G-T^E$.

**Hypotheses.**

- **(W)** W1–W3 of E2b for $F$: covariance, spectral condition, positive
  Hilbert space. Not W4 (locality), so not CPT. E2b then gives the Wightman
  function as $\int d\mu(s)\,\delta(p^2-s)\,(-T)$ with $\mu\ge0$, plus a possible
  massless helicity term $i\alpha'T^\star$ on the cone with $\alpha\ge|\alpha'|$,
  through the two unchecked lemmas named in the status paragraph.
- **(E)** The Euclidean two-point function, away from coincident points, is
  $S(p)=T^E(p)\,a(p^2)$ plus the helicity term, with $a(p^2)=\int d\mu(s)/(p^2+s)$
  and the same $\mu\ge0$. This is what the arguments below use. Passing from
  (W) to (E) is the Wightman → Schwinger continuation. Section 11 does it for
  this two-point function: the $T^E$ part needs no locality, because it is
  automatically two-point local; the helicity term, whose time-ordered
  function would change sign at $\tau=0$, is excluded by (B<sub>T</sub>), and
  that exclusion is two-point locality in that sector.
- **(B)** The Bianchi identity at separated points, as in E2b; it removes the
  massive dual structure. It is implied by (B<sub>T</sub>) below.
- **(I)** $\int d\mu(s)/(1+s)<\infty$. This is the integrability clause of the
  paper's Hypothesis 3, and it is equivalent to local integrability of
  $a^{(3)}$ in $\mathbb R^3$.
- **(B<sub>T</sub>)** The Euclidean two-point function satisfies Bianchi in both
  slots as a distribution on all of $\mathbb R^4$. By Proposition "local terms"
  of E2b, its local part is then $q(p^2)\,T^E(p)$ with $q$ a polynomial (assuming
  the extension to the origin is $O(4)$-covariant; Section 11); $G$ and
  $\epsilon$ are excluded. When the probe is a Wilson loop of a potential with
  $F=dA$, (B<sub>T</sub>) holds identically for $d\langle TAA\rangle d$; it
  holds for the time-ordered function of $F$ on the plane $\tau=0$ only if the
  potential is equal-time local, as in a local covariant gauge (Section 11).
- **(L)** Linear probe: the static potential is taken from the quadratic
  cumulant of $\log\langle\mathcal W\rangle$, the field of the line from its
  $O(q_W)$ term. The next connected cumulant is cubic; it vanishes if the state
  is charge-conjugation invariant, and otherwise enters at $O(q_W^3)$.
- **(C)** Coulomb phase: $\mu(\{0\})>0$. Used only for the profile, not for the
  representation.

Under (E), the Euclidean two-point function away from coincident points is
$$S(p)=T^E(p)\,a(p^2)+\text{helicity term},\qquad a(p^2)=\int\frac{d\mu(s)}{p^2+s}.$$

**Sign anchor.** Free Proca of mass $m$ is a positive Wightman theory with
$\mu=\delta_{m^2}$ of weight $+1$ in E2b's normalisation. Built from $F=dA$ with
the Euclidean propagator $(\delta+pp/m^2)/(p^2+m^2)$, it gives exactly
$S=+T^E/(p^2+m^2)$. Free Maxwell in any covariant gauge gives $+T^E/p^2$, the
gauge term dropping out. Every sign below rests on these two computations.

**Probes.** For a surface $\Sigma$, $\mathcal W_\Sigma=\exp(iq_W\int_\Sigma F)$.
When $F=dA$ this is the Wilson loop of $\partial\Sigma$ by Stokes. Without a
potential, (B<sub>T</sub>) is exactly what makes the $O(q_W^2)$ cumulant
independent of $\Sigma$ at fixed boundary: two surfaces differ by
$\int_{\partial V}F=\int_V dF$, and the difference of cumulants is a two-point
function of $dF$ with an $F$ whose support meets $V$, coincident points
included.

## 2. What a planar probe sees

The rectangular loop $C_{r\times T}$ spans a rectangle $R$ in the $(x^0,x^1)$
plane; the static line spans a half-plane $\{x^0\in\mathbb R,\,x^1\ge0\}$. The
loop involves only $S_{01,01}$, the line only $S_{0i,01}$.

| structure | $S_{01,01}$ | $S_{0i,01}$, $i=1,2,3$ | at $p_0=0$ |
|---|---|---|---|
| $T^E$ | $p_0^2+p_1^2$ | $(p_0^2+p_1^2,\ p_1p_2,\ p_1p_3)$ | $p_1p_i$ |
| $T^\star$, either pair | $0$ | $(0,\ \mp p_0p_3,\ \pm p_0p_2)$ | $0$ |
| $G$ | $1$ | $(1,0,0)$ | $\delta_{i1}$ |
| $\epsilon$ | $0$ | $0$ | $0$ |
| dual $p^2G-T^E$ | $p_2^2+p_3^2$ | — | — |

**Lemma 1.** The helicity term does not reach the loop, because the component
vanishes identically, nor the line, because the component is proportional to
$p_0$ and the line integrates over all time. CPT is therefore not needed for
either static observable. The local term $\epsilon$ never reaches them. (This
reads the helicity term as an $O(4)$-covariant part of (E). Section 11 shows
that without locality it is not covariant. For the loop the conclusion holds
regardless, since the component vanishes identically. For the line it holds
because (B<sub>T</sub>) excludes the term, and that exclusion is two-point
locality in this sector; so CPT is not used as an axiom, but its consequence
here is assumed.)

## 3. Stokes for the rectangle

With $f_L(k)=2-2\cos kL$, the rectangle's Fourier transform satisfies
$|\tilde\Sigma(p_0,p_1)|^2=f_T(p_0)f_r(p_1)/(p_0^2p_1^2)$, and

**Lemma 2.**
$$|\tilde\Sigma|^2\,(p_0^2+p_1^2)=\frac{f_T(p_0)}{p_0^2}f_r(p_1)+f_T(p_0)\frac{f_r(p_1)}{p_1^2},$$
and the right side is $|\oint dx^0e^{ipx}|^2+|\oint dx^1e^{ipx}|^2$ around the
boundary. So for $S=T^Ea$ the surface cumulant equals the Feynman-gauge line
cumulant $\tfrac12\oint\oint dx\cdot dy\,a(x-y)$. Only parallel sides contribute.
For the two time-like sides, the two self-terms and the two cross-terms (with
opposite orientation) give $2\int_{-T}^{T}du\,(T-|u|)[a(u,0)-a(u,r)]$ before the
overall $\tfrac12$; the space-like sides likewise. Hence
$$\tfrac12\oint\oint=\int_{-T}^{T}\!du\,(T-|u|)\,[a(u,0)-a(u,r)]+\int_{-r}^{r}\!dv\,(r-|v|)\,[a(0,v)-a(T,v)],$$
or, by parity, $2\int_0^T(T-u)[\dots]\,du+2\int_0^r(r-v)[\dots]\,dv$.

*Correction (3 October).* The display printed here on 1 October had a factor 2
in front of each bilateral integral. Taken literally it gives twice the
surface cumulant: for $a(\rho)=e^{-\rho^2}$, $T=2$, $r=0.7$, the surface
integral and the code both give $1.4317802$, the old display $2.8635604$.
The test compared the surface integral with the code, not with the printed
display, so it could not see the error; a test of the display itself now
does. Nothing downstream changes: $C(r)$ and the tables of Section 9 come
from the code.

## 4. The static limit

Regulate by heat-kernel smearing, $\hat a_\varepsilon(p^2)=e^{-\varepsilon p^2}a(p^2)$,
which keeps the sign of every Fourier mode and makes $\hat a_\varepsilon\in L^1(\mathbb R^4)$
under (I). Let $V_T(r)=-T^{-1}\log\langle\mathcal W\rangle$ at $O(q_W^2)$.

**Proposition 3.** At fixed $\varepsilon>0$,
$\lim_{T\to\infty}V_{T,\varepsilon}(r)=q_W^2\,[a^{(3)}_\varepsilon(0)-a^{(3)}_\varepsilon(r)]$,
with $a^{(3)}_\varepsilon(\mathbf r)=\int dt\,a_\varepsilon(t,\mathbf r)$, and
$$V_{T,\varepsilon}(r)-V_{\infty,\varepsilon}(r)=\frac{q_W^2\,C_\varepsilon(r)}{T}+o_\varepsilon(1/T),\qquad
C_\varepsilon(r)=-2\!\int_0^\infty\!u\,[a_\varepsilon(u)-a_\varepsilon(\sqrt{u^2+r^2})]\,du+2\!\int_0^r\!(r-v)\,a_\varepsilon(v)\,dv .$$
As $\varepsilon\to0$, $a^{(3)}_\varepsilon(r)\to a^{(3)}(r)=\int d\mu(s)e^{-\sqrt sr}/(4\pi r)$
for every $r>0$, so $V(r)-V(r_0)=-q_W^2[a^{(3)}(r)-a^{(3)}(r_0)]$. The order of
limits is $T\to\infty$ first, then $\varepsilon\to0$; the rate is not uniform
in $\varepsilon$ (below).

*Proof.* By Lemma 2 the cumulant splits into the two terms of the display.
In the first, $f_T(p_0)/(Tp_0^2)$ is $2\pi$ times the Fejér kernel, an
approximate identity, and $p_0\mapsto\int d^3p\,\hat a_\varepsilon(p_0^2+\mathbf p^2)f_r(p_1)$
is bounded and continuous; its value at $p_0=0$ gives the limit. In the second,
$f_T\le4$ and $\int d^3p\,\hat a_\varepsilon f_r(p_1)/p_1^2\le r^2\int d^3p\,\hat a_\varepsilon$
is integrable in $p_0$, so that term is bounded uniformly in $T$ and drops after
division by $T$. The value at $p_0=0$ is a Fourier slice:
$\int d^3p\,e^{i\mathbf p\cdot\mathbf r}\hat a(\mathbf p^2)=\int dt\,a(t,\mathbf r)$.
For the measure, $\int dt\,\Delta_s(t,r)=e^{-\sqrt sr}/(4\pi r)$ with
$\Delta_s(x)=\sqrt sK_1(\sqrt s|x|)/(4\pi^2|x|)>0$, and Tonelli exchanges $\mu$
and $t$. The regulator is a 3D Gaussian convolution of $a^{(3)}$, which is
locally integrable by (I) and continuous on $r>0$. The rate follows from
writing $V_T-V_\infty$ in position space: the tails of $a(u,0)$ and $a(u,r)$
cancel in the bracket, which decays like $u^{-4}$ in the Coulomb phase, so
$\int u[\dots]du$ converges. ∎

A local term $q(p^2)T^E$ adds $q_W^2\int d^3p\,e^{-\varepsilon\mathbf p^2}q(\mathbf p^2)(1-\cos p_1r)$:
an $r$-independent constant plus derivatives of a Gaussian centred at the
origin, which vanish at every $r>0$ as $\varepsilon\to0$.

**Measured.** I had expected a $\log T/T$ rate in the Coulomb phase, from the
$1/u^2$ tail of $a(u,r)$ taken alone. The computation says otherwise: in the
bracket the tails cancel, and $T\,(V_T-V_\infty)$ converges to the predicted
$C_\varepsilon(r)$ (table in Section 9). With a gap and no Coulomb weight it is constant to
six significant digits already at $T=10$.

**The rate does not survive removing the regulator.** For the pure Coulomb
measure $\mu=\delta_0$ the regulated kernel is
$a_\varepsilon(\rho)=(1-e^{-\rho^2/4\varepsilon})/(4\pi^2\rho^2)$, and both
integrals in $C_\varepsilon$ can be expanded. With
$\int_0^X(1-e^{-x^2})x^{-2}dx=\sqrt\pi-1/X+\dots$ and
$\int_0^X(1-e^{-x^2})x^{-1}dx=\ln X+\gamma_E/2+\dots$,
$$C_\varepsilon(r)=\frac{\sqrt\pi\,r}{4\pi^2\sqrt\varepsilon}
-\frac{1}{\pi^2}\Bigl[\ln\frac{r}{2\sqrt\varepsilon}+\frac{\gamma_E}{2}+\frac12\Bigr]+o(1).$$
The first integral contributes $-\tfrac{1}{2\pi^2}[\ln(r/2\sqrt\varepsilon)+\gamma_E/2]$
and diverges logarithmically; the second carries the $1/\sqrt\varepsilon$ term.
At $r=1$ the expansion reproduces the computed values to five decimals:
$C_{10^{-2}}=0.20599$, $C_{10^{-3}}=1.06014$, $C_{10^{-4}}=4.01340$,
$C_{10^{-5}}=13.60468$. So the $1/T$ rate is a statement at fixed regulator.
The static potential is unaffected: $V_{\infty,\varepsilon}(r)-V_{\infty,\varepsilon}(r_0)$
converges as $\varepsilon\to0$, because the only divergent piece of
$V_{\infty,\varepsilon}$, the self-energy $a^{(3)}_\varepsilon(0)$, does not
depend on $r$.

## 5. The field of a static line

**Proposition 4.** At $O(q_W)$ the field of a static line through the origin is
a gradient, $\langle E_i(\mathbf x)\rangle\propto q_W\,\partial_ia^{(3)}(\mathbf x)$,
independent of the half-plane chosen to span it. Under (C), its flux through a
sphere, normalised by its limit at infinity, is
$$\frac{q(r)}{q_W}=\frac{1}{\mu(\{0\})}\Bigl[\mu(\{0\})+\int_{(0,\infty)}d\mu(s)\,(1+\sqrt s\,r)\,e^{-\sqrt s\,r}\Bigr],$$
which is the formula from which the paper's Theorem A starts, with
$g_R^2=\mu(\{0\})$ and $q_\infty=q_W$.

*Proof.* The half-plane gives $2\pi\delta(p_0)\cdot(-i)/(p_1-i0)$. At $p_0=0$
the $T^E$ component is $p_1p_i\hat a$ (Section 2), and $p_1/(p_1-i0)=1$ as a
distribution against it, leaving $-ip_i\hat a(\mathbf p^2)$: the gradient of
$a^{(3)}$, with no reference to the half-plane. The helicity term is
proportional to $p_0$ and is removed by $\delta(p_0)$. The sphere flux of
$-\nabla a^{(3)}$ is $-4\pi r^2\,\partial_ra^{(3)}$, and
$-4\pi r^2\partial_r[e^{-\sqrt sr}/(4\pi r)]=(1+\sqrt sr)e^{-\sqrt sr}$. ∎

*Scope of this proof.* The infinite half-plane is handled formally: the
product of $\delta(p_0)/(p_1-i0)$ with $p_1p_i\hat a$, and the replacement
$p_1/(p_1-i0)=1$, must be defined as a distribution against a specified class
of test functions. With the heat-kernel regulator the integrand is smooth and
the step goes through; for a general tempered $\mu$ it is not proved here, nor
is the independence of the half-plane for general distributions.

Under (B<sub>T</sub>) violated, the $G$ component $\delta_{i1}/(ip_1)$ is not a
gradient: it is a field concentrated on the auxiliary half-plane, a flux sheet
whose position depends on an arbitrary choice.

## 6. Theorem

**Theorem E2c.** Assume (E), (I), (B<sub>T</sub>) and (L). For every $r>0$:

1. $V(r)-V(r_0)=-q_W^2\,[a^{(3)}(r)-a^{(3)}(r_0)]$ with
   $a^{(3)}(r)=\int d\mu(s)\,e^{-\sqrt s\,r}/(4\pi r)$ and $\mu\ge0$;
2. the field of a static line is $-q_W\nabla a^{(3)}$ up to normalisation, so the
   linear-response relation of Hypothesis 5 holds with
   $\mathcal G(Q^2)=\int d\mu(s)/(Q^2+s)$ plus a polynomial;
3. under (C), the representation of Hypothesis 3 holds on $r>0$ with
   $g_R^2=\mu(\{0\})$, $d\sigma=d\mu|_{(0,\infty)}$ and the integral starting at
   $\inf\operatorname{supp}\sigma$, which may be $0$; Hypothesis 2 asks it to
   be positive. The Laplace representation of Theorem A follows, with
   $M_*=(\inf\operatorname{supp}\sigma)^{1/2}$ possibly zero: $q_\infty=q_W$
   needs only dominated convergence under (I), not the gap.

Not assumed as axioms: locality W4, CPT, parity, $F=dA$, Maxwell's equations,
a gauge choice. Qualification: the only consequence of W4 and CPT for this
two-point function, $\alpha'=0$, *is* assumed, as the content of
(B<sub>T</sub>) at separated points on the plane $\tau=0$ (Section 11); the
coincident-point clause of (B<sub>T</sub>) excludes $G$ and fixes the contact
at the origin. The $T$ part of (E) follows from E2b's form without locality
(Section 11); E2b's form rests on two unread lemmas. Not implied: the gap of
Hypothesis 2, the Coulomb phase, anything beyond the quadratic cumulant.

## 7. What fails without each hypothesis

- **Without (B<sub>T</sub>)**, the local term $c\,G$ survives. For the loop it
  adds $\tfrac12q_W^2c\,\mathrm{Area}\times\delta^2_\perp(0)$, regulated
  $q_W^2c\,r/(8\pi\varepsilon)$: at fixed regulator a linear potential, an area
  term. Its slope $\sigma_\varepsilon=q_W^2c/(8\pi\varepsilon)$ diverges as the
  regulator is removed (measured: halving $\varepsilon$ doubles it), so a local
  contact does not produce a finite string tension; it is a regulated contact.
  For the line it is the flux sheet of Section 5. Checked numerically,
  including the exact finite-$T$ correction
  $-\sqrt{\pi\varepsilon}/(4\pi^2\varepsilon T)$ to the slope.
- **Without (B) at separated points** (magnetic sources), the massive dual
  structure survives; since it equals $p^2G-T^E$, it carries the $G$ tensor
  structure with a nonlocal coefficient. Whether that gives a finite area law
  depends on the coefficient function, which is what the stochastic vacuum
  model's $D(x^2)$ parametrises; it is not computed here.
- **Without (C)**, e.g. free Proca, $\mu(\{0\})=0$, $q_\infty=0$, and the profile
  is undefined. This is obligation O1 of D5, unchanged.
- **Without (L)**, the cumulant expansion continues: a connected cubic
  cumulant at $O(q_W^3)$, absent in a charge-conjugation-invariant state, and
  the connected four-field cumulant at $O(q_W^4)$. Identifying the latter with
  light-by-light scattering is a statement about the dynamics, not made here.
  Note E3 (`notes/E3_nonlinear_probe_EH.md`) computes it in the
  Euler–Heisenberg effective theory for smooth sources of radius $R\gg1/m$,
  where its sign is fixed; point probes remain open.
- **Nonabelian:** $F$ is not gauge invariant and the abelian Stokes step fails.

## 8. Prior work, and what is not claimed

*Read at full-text level, directed reading:* A. Di Giacomo, H. G. Dosch,
V. I. Shevchenko and Yu. A. Simonov, *Field correlators in QCD. Theory and
applications*, Phys. Rept. 372 (2002) 319, arXiv:hep-ph/0007223:

- §2.1, eq. (2.6): the two-point field-strength correlator is decomposed into a
  function $D$ multiplying $G$ and a function $D_1$ multiplying a derivative
  structure — our $T^E$. Eq. (2.11): in QED $D\equiv0$ and $D_1$ is fixed by
  the running charge; "$D(z)\equiv0$ to all orders in perturbation theory".
- §3.1, eq. (3.7): $\sigma=\tfrac12\int d^2x\,D(x)$; "$D_1$ does not enter
  $\sigma$, but gives rise to the perimeter term".
- §3.2, eqs. (3.10)–(3.13): in an abelian theory without magnetic monopoles the
  Bianchi identity forces $D=0$, so there is no confinement; with monopoles $D$
  is tied to the monopole-current correlator.
- §4.2, eq. (4.12): the static potential from $D$ and $D_1$ in the bilocal
  approximation.

So the split into a Bianchi-violating part that confines and a
Bianchi-compatible part that does not, and the potential from the latter, are
the stochastic vacuum model's. The comparison is structural only. There
$D(x^2)$ is a nonlocal function with a finite correlation length, and that is
what makes $\sigma=\tfrac12\int d^2x\,D$ finite; the local contact
$c\,G\,\delta^{(4)}$ of Section 7 shares the tensor structure but has a
divergent area coefficient, and is not identified with $D$. The primary papers cited there — Dosch, Phys.
Lett. B 190 (1987) 177; Dosch and Simonov, Phys. Lett. B 205 (1988) 339;
Simonov, Nucl. Phys. B 307 (1988) 512; Simonov, Sov. J. Nucl. Phys. 50 (1989)
134 — have **not** been read.

The representation of a static potential as a superposition of Yukawas
weighted by the spectral function of the photon is classical (Källén–Lehmann;
the Uehling potential is the leading case). It is used here in that form and
needs a primary or textbook citation, not yet read.

*Not found in the sources searched:* a statement that positivity of the
⟨FF⟩ spectral measure, with Bianchi on the T-product, yields the
Laplace-positivity of the static kernel; or that the helicity term is invisible
to both static observables. The review's extracted text has no occurrence of
"spectral", "positiv" or "Källén". This does not establish novelty; the
primaries are unread.

## 9. Machine verification

`tests/test_e2c_transport.py`, 33 tests, with the routines in
`reproducibility/transport_linear_probe.py`:

| step | check | result |
|---|---|---|
| sign anchor | Proca and Maxwell (any $\xi$) from $F=dA$ give $+T^E\,a$ | exact (sympy) |
| Lemma 1 | the table of Section 2 | exact (sympy) |
| Lemma 2 | surface form against the explicit boundary integrals | exact (sympy) |
| Lemma 2, numerically | $\tfrac12\int_R\int_RS_{01,01}$ against $\tfrac12\oint\oint a$, two measures and a Gaussian | agree to $\le4\times10^{-16}$ |
| Lemma 2, the printed display | the bilateral display of Section 3, coded literally, against the surface integral; the 1 October version | equal to $10^{-10}$; old version off by exactly 2 |
| the check can fail | $a''$ alone in place of the in-plane Laplacian | off by > 10% |
| Fourier slice | $\int dt\,\Delta_s=e^{-\sqrt sr}/(4\pi r)$, $s\in\{0,\tfrac14,1,9\}$, $r\in\{0.3,1,4\}$ | $\le2.2\times10^{-16}$ |
| regulator | $a^{(3)}_\varepsilon/\text{Yukawa}=e^{\varepsilon s}$ for $r\gg\sqrt\varepsilon$ | $<10^{-9}$ |
| Proposition 3 | $T(V_T-V_\infty)\to q_W^2C_\varepsilon(r)$ at fixed $\varepsilon$, $q_W^2=1$ and $2.5$ | $160\,(V_{160}-V_\infty)/(q_W^2C_\varepsilon)=1$ to $10^{-4}$ |
| no uniform rate | $C_\varepsilon(r)$ for $\mu=\delta_0$, $r\in\{0.5,1\}$, $\varepsilon=10^{-2},10^{-3},10^{-4}$, against the expansion of Section 4 | $<10^{-4}$; the coefficient $1/(2\pi^2)$ fails |
| Proposition 4 | $-4\pi r^2\partial_ra^{(3)}$ against the closed form | $<10^{-7}$ |
| Section 7 | slope of the $G$ term at $T=60$ | $3.971391$ predicted and measured |
| Section 7, divergence | the same slope at $\varepsilon=0.005$ | $7.947165$, twice the slope at $0.01$ to $2\times10^{-3}$ |
| Section 11, helicity structure | pair symmetry of $T$; $T^{\star(1)}_{ab,ce}=T^{\star(2)}_{ce,ab}$; $T^{\star(1)}+T^{\star(2)}\propto p^2$, Euclidean and Minkowski | exact (sympy) |
| Section 11, (B<sub>T</sub>) | equal-time Bianchi term of $\operatorname{sign}(\tau)X(\partial)G$; smooth Bianchi of $X(\partial)G$ | nonzero (closed form checked); zero |
| Section 11, discriminator | $\int\operatorname{sign}(\tau)\partial_\tau g=-2g(0)$ against $\int\partial_\tau g=0$ | $<10^{-12}$ |
| Section 11, static response | retarded at $\omega=0$ against $\int d\tau$ of the time-ordered function, unequal weights for the two orderings | $<10^{-8}$ |

Measured rates ($\varepsilon=0.02$ fixed, $q_W=1$), $T\,(V_T-V_\infty)$:

| measure | $r$ | $T=10$ | $40$ | $160$ | $320$ | predicted $C_\varepsilon(r)$ |
|---|---|---|---|---|---|---|
| $\delta_0$ | 0.5 | 0.0207551 | 0.0207947 | 0.0207971 | 0.0207972 | — |
| $0.6\,\delta_0+0.4\,\delta_1$ | 0.5 | 0.0205589 | 0.0205827 | 0.0205841 | 0.0205842 | 0.0205842 |
| $0.6\,\delta_0+0.4\,\delta_1$ | 2.0 | 0.3466152 | 0.3469936 | 0.3470173 | 0.3470185 | 0.3470189 |
| $\delta_1$ (Proca) | 0.5 | 0.02026465 | 0.02026466 | 0.02026466 | 0.02026466 | — |

## 10. Open, in order

1. Read Bochner–Schwartz and the covariant disintegration, at the level of
   the statements used (E2b's TO READ list minus CPT). The continuation to
   (E) is argued in Section 11 with symbolic checks; a textbook statement of
   it should still be located and read.
2. Read the SVM primaries and a textbook statement of the dispersive static
   potential; settle attribution.
3. The general tempered case without (I), and the distributional steps for a
   general $\mu$ (half-plane product, independence of the spanning surface):
   subtractions add polynomials, which should still not reach $r>0$; not
   proved here.
4. Beyond the quadratic cumulant: the cubic cumulant (zero under charge
   conjugation) and the connected four-field cumulant, which in QED is
   light-by-light scattering (roadmap E2.3f). Note E3 settles its sign in the
   Euler–Heisenberg effective theory for smooth sources (5 October); for point
   probes the coefficient is set by the full light-by-light kernel and is not
   computed.

## 11. From Wightman to (E), for this two-point function (3–5 October)

Argued here with symbolic checks, not read in a source; the two-point
continuation from a Källén–Lehmann form is presumably textbook material, and
no novelty is claimed. Tests: `tests/test_e2c_transport.py`, the tests under
"Section 11". An independent re-derivation on 4 October confirmed the
technical steps and corrected the framing; this version carries those
corrections (paragraph "Status" at the end).

**What the spectral sums fix, and what they do not.** With $A(t)$, $B$ two
operators and the connected spectral sums $\langle A(t)B\rangle=\sum_na_ne^{-iE_nt}$,
$\langle BA(t)\rangle=\sum_nb_ne^{iE_nt}$, $E_n>0$, the zero-frequency retarded
response is $i\int_0^\infty dt\,\langle[A(t),B]\rangle=\sum_n(a_n+b_n)/E_n$, and
so is $\int_0^\infty d\tau\sum_na_ne^{-E_n\tau}+\int_{-\infty}^0d\tau\sum_nb_ne^{E_n\tau}$.
This identifies the static response with the time-ordered Euclidean function
*away from* $\tau=0$ only. The object the theorem integrates, $T^Ea$, differs
from that $\theta$-split function by a non-covariant contact
$\propto\delta(\tau)\delta^{(3)}(\mathbf x)$ of weight $\int d\mu$; for free
Maxwell, the $\tau$-integral of the $\theta$-split $(0i,0j)$ block is purely
transverse, and the longitudinal Coulomb response sits in that contact. Under
(I) alone, $\int d\mu$ may be infinite. So spectral data do not fix the object
at $\tau=0$: the coincident-point clause of (B<sub>T</sub>), that is, the
covariant prescription, does.

**The $T$ part.** In E2b's form the Wightman function
$W_{\mu\nu,\rho\sigma}(x)=\langle F_{\mu\nu}(x)F_{\rho\sigma}(0)\rangle$ has a
part $\int d\mu(s)\,T_{\mu\nu\rho\sigma}(\partial)\,W_s(x)$, with $W_s$ the free
two-point function of mass$^2$ $s$. The time-ordered function is the
continuation of $W_{\mu\nu,\rho\sigma}(x)$ for $\tau>0$ and of
$\langle F_{\rho\sigma}(0)F_{\mu\nu}(x)\rangle=W_{\rho\sigma,\mu\nu}(-x)$ for
$\tau<0$ (translation invariance only). $T$ is symmetric under exchange of its
index pairs and even in $p$, and $W_s(\pm x)$ continue to the same Euclidean
propagator. The two halves join into one $O(4)$-covariant function,
$T^E(\partial)\int d\mu(s)\Delta_s(x_E)$ at $x_E\neq0$, with the same $\mu\ge0$
and the sign of the Proca anchor (checked on all components, massless and
massive). The integral converges at $x_E\neq0$ for any tempered $\mu$. This
part needs no locality *because it is automatically two-point local*: its
commutator is $T(\partial)$ acting on the Pauli–Jordan function, which
vanishes at spacelike separation for every mass.

**The helicity part.** The massless term $i\alpha'X\,\delta(p^2)$, with
$X=\tfrac12(T^{\star(1)}-T^{\star(2)})$, is allowed by Wightman positivity
when $|\alpha'|\le\alpha$ (at $\bar p=(1,0,0,1)$ the nonzero eigenvalues are
$2(\alpha\pm\alpha')$, as E2b states). Two identities, checked in Euclidean
and Minkowski signature: $T^{\star(1)}_{ab,ce}=T^{\star(2)}_{ce,ab}$ and
$T^{\star(1)}+T^{\star(2)}=p^2\epsilon$. The first makes $X$ antisymmetric
under exchange of the pairs, which is what makes $i\alpha'X$ Hermitian; the
second makes $X=T^{\star(1)}=-T^{\star(2)}$ on the cone, so $X$ is E2b's
$T^\star$ up to the sign convention of $\alpha'$. Without locality the
$\tau<0$ half enters with the opposite sign: the helicity part of the
time-ordered function is $\alpha'\operatorname{sign}(\tau)\,X^E(\partial)G$
(real coefficient after the Wick rotation), with $G$ the massless propagator,
and it is not $O(4)$-covariant. $X^E(\partial)G$ obeys Bianchi at $x_E\neq0$,
but the jump of $\operatorname{sign}(\tau)$ adds
$2\delta(\tau)\,\epsilon_{\kappa0\mu\nu}X^E_{\mu\nu,\rho\sigma}(\partial)G(0,\mathbf x)$
to $\epsilon\partial S$. That coefficient is not zero: in Minkowski language
it is the equal-time commutator $\langle[B_k(0,\mathbf x),E_j(0)]\rangle$,
proportional to $\alpha'(r^2\delta_{kj}-2x_kx_j)/r^6$, nine independent
components per slot ($\langle[B,B]\rangle=0$); one of them is
$\epsilon_{10\mu\nu}X^E_{\mu\nu,01}(\partial)G\,\big|_{\tau=0}=-2(x_1^2-x_2^2-x_3^2)/(\pi^2|\mathbf x|^6)$.
The $T$ part gives no jump, because its commutator vanishes at every
spacelike point.

**What (B<sub>T</sub>) then assumes.** Read on the time-ordered function at
separated points of the plane $\tau=0$, (B<sub>T</sub>) forces $\alpha'=0$. Given
E2b's form, $\alpha'=0$ is equivalent to two-point locality of $F$ and to the
CPT reality of $\tilde W$ (pair-symmetric $T$, pair-antisymmetric $X$). So
the content of (B<sub>T</sub>) on $\tau=0$ *is* two-point locality in this
sector: neither W4 nor the CPT theorem is assumed as an axiom, but their only
consequence for this two-point function is assumed, as part of
(B<sub>T</sub>). The premise has moved from (E) into (B<sub>T</sub>); it has not
disappeared. The Wightman Bianchi identity at separated points, (B), does not
exclude the term. The coincident-point clause of (B<sub>T</sub>) is what fixes
the contact of the first paragraph and excludes $G$ (Section 7).

**The Wilson-loop justification of (B<sub>T</sub>).** Section 1 says that for the
Wilson loop of a potential with $F=dA$, (B<sub>T</sub>) holds identically. That
is a statement about $d\langle TAA\rangle d$, which differs from the
time-ordered function of $F$ by $\delta(\tau)$ terms on $\tau=0$; these are
nonlocal in $\mathbf x$ unless the potential's equal-time commutators vanish at
$\mathbf x\neq0$. A free Coulomb-gauge vector with helicity weights
$\alpha\pm\alpha'$ makes the point: its $\langle FF\rangle$ has exactly E2b's form
with a helicity term $\propto\alpha'$, its Wilson-loop object obeys Bianchi
identically, and its time-ordered $\langle FF\rangle$ violates Bianchi on
$\tau=0$. So a Wilson loop supplies the $\tau=0$ content of (B<sub>T</sub>) only
when the potential is itself equal-time local, as in a local covariant gauge.

**If the term survived.** Its time-ordered function would reach the static
line: $\int d\tau\,\operatorname{sign}(\tau)\,\partial_\tau g=-2g(0)\neq0$, while
$\int d\tau\,\partial_\tau g=0$. The result is a field
$(0,\partial_3\Psi,-\partial_2\Psi)$ that depends on the spanning half-plane and
is azimuthal about the line, so it carries no flux through spheres centred on
it. The violation of (B<sub>T</sub>) on $\tau=0$ and the surface dependence appear
together, as they must. The loop component of the helicity structure
vanishes identically, whatever its time dependence, so the static potential
never sees it.

**Status.** Section 11 derives (E) for the $T$ part from E2b's Källén–Lehmann
form (two lemmas still unread) and (I), without locality, because that part is
automatically two-point local. The massless helicity term is excluded only by
(B<sub>T</sub>) read on the time-ordered Schwinger function off the origin, whose
content on $\tau=0$ is, given E2b's form, equivalent to two-point locality
($\alpha'=0$, CPT reality). The premise has moved from (E) into (B<sub>T</sub>)
rather than disappeared, and a Wilson loop of a potential supplies it only if
that potential is itself equal-time local. Two points remain open here: that
the terms supported at the origin are $O(4)$-covariant (or, if not, that
non-covariant Bianchi-compatible polynomials still do not reach $r>0$), and a
textbook statement of the continuation.
