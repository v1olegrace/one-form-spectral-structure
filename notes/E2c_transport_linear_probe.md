# E2c — From ⟨FF⟩ to the static observables, at linear order in the probe

Working note, 1 October 2026. Roadmap obligation 2 of E2.4 (O2 of D5 in
`DECISIONS.md`): transport the positivity of ⟨FF⟩ to the static kernel through
the Wilson loop, with the tensor projection, the sign, the contact terms, the
perimeter and the limit T → ∞ each accounted for.

**Status.** Proved here, conditionally on the classification of note E2b
(`notes/E2b_tensor_classification.tex`), whose measure-theoretic lemmas
(Bochner–Schwartz; covariant disintegration over orbits) and the continuation
from Wightman to Schwinger functions have not been checked against primary
sources. Every algebraic and numerical step is machine-checked in
`tests/test_e2c_transport.py` (Section 9). Nothing here concerns the nonlinear
probe, the nonabelian theory, or the existence of four-dimensional QED.

## 0. The result in one paragraph

Let $F$ be a two-form field obeying the Wightman axioms W1–W3 (no locality, no
CPT, no parity), the Bianchi identity at separated points (B), and the Bianchi
identity in the Euclidean two-point function *including coincident points*
(B<sub>T</sub>). Then, at linear order in the probe charge (L), both the static
potential of a Wilson loop and the field of a static line depend on the
two-point function only through
$$a^{(3)}(r)=\int_{[0,\infty)}d\mu(s)\,\frac{e^{-\sqrt s\,r}}{4\pi r},\qquad \mu\ge0 ,$$
where $\mu$ is the Källén–Lehmann measure of ⟨FF⟩ from E2b. For $r>0$ this is
Hypothesis 3 of the paper, with $g_R^2=\mu(\{0\})$ and $\sigma=\mu|_{(0,\infty)}$,
up to a contact polynomial that does not reach $r>0$; it also gives the
linear-response relation of Hypothesis 5. The massless helicity term that E2b
could remove only through CPT never reaches either observable. What
(B<sub>T</sub>) excludes is the local structure $G=\delta\delta-\delta\delta$,
which produces an area law; that mechanism is the stochastic vacuum model's
(Section 8). The Coulomb phase $\mu(\{0\})>0$ and the gap of Hypothesis 2 are
not implied.

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
  massless helicity term $i\alpha'T^\star$ on the cone with $\alpha\ge|\alpha'|$.
- **(B)** The Bianchi identity at separated points, as in E2b; it removes the
  massive dual structure. It is implied by (B<sub>T</sub>) below.
- **(I)** $\int d\mu(s)/(1+s)<\infty$. This is the integrability clause of the
  paper's Hypothesis 3, and it is equivalent to local integrability of
  $a^{(3)}$ in $\mathbb R^3$.
- **(B<sub>T</sub>)** The Euclidean two-point function satisfies Bianchi in both
  slots as a distribution on all of $\mathbb R^4$. By Proposition "local terms"
  of E2b, its local part is then $q(p^2)\,T^E(p)$ with $q$ a polynomial; $G$ and
  $\epsilon$ are excluded. When the probe is a Wilson loop of a potential with
  $F=dA$, (B<sub>T</sub>) holds identically.
- **(L)** Linear probe: the static potential is taken from the $O(q_W^2)$
  cumulant, the field of the line from its $O(q_W)$ term.
- **(C)** Coulomb phase: $\mu(\{0\})>0$. Used only for the profile, not for the
  representation.

Under (W), the Euclidean two-point function away from coincident points is
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
either static observable. The local term $\epsilon$ never reaches them.

## 3. Stokes for the rectangle

With $f_L(k)=2-2\cos kL$, the rectangle's Fourier transform satisfies
$|\tilde\Sigma(p_0,p_1)|^2=f_T(p_0)f_r(p_1)/(p_0^2p_1^2)$, and

**Lemma 2.**
$$|\tilde\Sigma|^2\,(p_0^2+p_1^2)=\frac{f_T(p_0)}{p_0^2}f_r(p_1)+f_T(p_0)\frac{f_r(p_1)}{p_1^2},$$
and the right side is $|\oint dx^0e^{ipx}|^2+|\oint dx^1e^{ipx}|^2$ around the
boundary. So for $S=T^Ea$ the surface cumulant equals the Feynman-gauge line
cumulant $\tfrac12\oint\oint dx\cdot dy\,a(x-y)$. Only parallel sides contribute:
$$\tfrac12\oint\oint=2\int_{-T}^{T}\!du\,(T-|u|)\,[a(u,0)-a(u,r)]+2\int_{-r}^{r}\!dv\,(r-|v|)\,[a(0,v)-a(T,v)].$$

## 4. The static limit

Regulate by heat-kernel smearing, $\hat a_\varepsilon(p^2)=e^{-\varepsilon p^2}a(p^2)$,
which keeps the sign of every Fourier mode and makes $\hat a_\varepsilon\in L^1(\mathbb R^4)$
under (I). Let $V_T(r)=-T^{-1}\log\langle\mathcal W\rangle$ at $O(q_W^2)$.

**Proposition 3.** $\lim_{T\to\infty}V_T(r)=q_W^2\,[a^{(3)}_\varepsilon(0)-a^{(3)}_\varepsilon(r)]$,
with $a^{(3)}_\varepsilon(\mathbf r)=\int dt\,a_\varepsilon(t,\mathbf r)$, and
$$V_T(r)-V_\infty(r)=\frac{C(r)}{T}+o(1/T),\qquad
C(r)=-2\!\int_0^\infty\!u\,[a(u)-a(\sqrt{u^2+r^2})]\,du+2\!\int_0^r\!(r-v)\,a(v)\,dv .$$
As $\varepsilon\to0$, $a^{(3)}_\varepsilon(r)\to a^{(3)}(r)=\int d\mu(s)e^{-\sqrt sr}/(4\pi r)$
for every $r>0$, so $V(r)-V(r_0)=-q_W^2[a^{(3)}(r)-a^{(3)}(r_0)]$.

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
$C(r)$ (table in Section 9). With a gap and no Coulomb weight it is constant to
six significant digits already at $T=10$.

## 5. The field of a static line

**Proposition 4.** At $O(q_W)$ the field of a static line through the origin is
a gradient, $\langle E_i(\mathbf x)\rangle\propto q_W\,\partial_ia^{(3)}(\mathbf x)$,
independent of the half-plane chosen to span it. Its flux through a sphere is
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

Under (B<sub>T</sub>) violated, the $G$ component $\delta_{i1}/(ip_1)$ is not a
gradient: it is a field concentrated on the auxiliary half-plane, a flux sheet
whose position depends on an arbitrary choice.

## 6. Theorem

**Theorem E2c.** Assume (W), (I), (B<sub>T</sub>) and (L). For every $r>0$:

1. $V(r)-V(r_0)=-q_W^2\,[a^{(3)}(r)-a^{(3)}(r_0)]$ with
   $a^{(3)}(r)=\int d\mu(s)\,e^{-\sqrt s\,r}/(4\pi r)$ and $\mu\ge0$;
2. the field of a static line is $-q_W\nabla a^{(3)}$ up to normalisation, so the
   linear-response relation of Hypothesis 5 holds with
   $\mathcal G(Q^2)=\int d\mu(s)/(Q^2+s)$ plus a polynomial;
3. under (C), Hypothesis 3 holds on $r>0$ with $g_R^2=\mu(\{0\})$ and
   $d\sigma=d\mu|_{(0,\infty)}$, and Theorem A of the paper follows.

Not used: locality W4, CPT, parity, $F=dA$, Maxwell's equations, a gauge
choice. Not implied: the gap of Hypothesis 2, the Coulomb phase, anything at
$O(q_W^4)$.

## 7. What fails without each hypothesis

- **Without (B<sub>T</sub>)**, the local term $c\,G$ survives. For the loop it
  adds $\tfrac12q_W^2c\,\mathrm{Area}\times\delta^2_\perp(0)$, regulated
  $q_W^2c\,r/(8\pi\varepsilon)$: a linear potential, an area law. For the line it
  is the flux sheet of Section 5. Checked numerically, including the exact
  finite-$T$ correction $-\sqrt{\pi\varepsilon}/(4\pi^2\varepsilon T)$ to the slope.
- **Without (B) at separated points** (magnetic sources), the massive dual
  structure survives; since it equals $p^2G-T^E$, it is again a $G$-type,
  area-law term. The separated-point version is the same mechanism.
- **Without (C)**, e.g. free Proca, $\mu(\{0\})=0$, $q_\infty=0$, and the profile
  is undefined. This is obligation O1 of D5, unchanged.
- **Without (L)**, the $O(q_W^4)$ cumulant (light-by-light) enters. Nothing
  here constrains its sign.
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
the stochastic vacuum model's. The primary papers cited there — Dosch, Phys.
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

`tests/test_e2c_transport.py`, 24 tests, with the routines in
`reproducibility/transport_linear_probe.py`:

| step | check | result |
|---|---|---|
| sign anchor | Proca and Maxwell (any $\xi$) from $F=dA$ give $+T^E\,a$ | exact (sympy) |
| Lemma 1 | the table of Section 2 | exact (sympy) |
| Lemma 2 | surface form against the explicit boundary integrals | exact (sympy) |
| Lemma 2, numerically | $\tfrac12\int_R\int_RS_{01,01}$ against $\tfrac12\oint\oint a$, two measures and a Gaussian | agree to $\le4\times10^{-16}$ |
| the check can fail | $a''$ alone in place of the in-plane Laplacian | off by > 10% |
| Fourier slice | $\int dt\,\Delta_s=e^{-\sqrt sr}/(4\pi r)$, $s\in\{0,\tfrac14,1,9\}$, $r\in\{0.3,1,4\}$ | $\le2.2\times10^{-16}$ |
| regulator | $a^{(3)}_\varepsilon/\text{Yukawa}=e^{\varepsilon s}$ for $r\gg\sqrt\varepsilon$ | $<10^{-9}$ |
| Proposition 3 | $T(V_T-V_\infty)\to C(r)$, predicted $C$ | $160\,(V_{160}-V_\infty)/C=1$ to $10^{-4}$ |
| Proposition 4 | $-4\pi r^2\partial_ra^{(3)}$ against the closed form | $<10^{-7}$ |
| Section 7 | slope of the $G$ term at $T=60$ | $3.971391$ predicted and measured |

Measured rates ($\varepsilon=0.02$, $q_W=1$), $T\,(V_T-V_\infty)$:

| measure | $r$ | $T=10$ | $40$ | $160$ | $320$ | predicted $C(r)$ |
|---|---|---|---|---|---|---|
| $\delta_0$ | 0.5 | 0.0207551 | 0.0207947 | 0.0207971 | 0.0207972 | — |
| $0.6\,\delta_0+0.4\,\delta_1$ | 0.5 | 0.0205589 | 0.0205827 | 0.0205841 | 0.0205842 | 0.0205842 |
| $0.6\,\delta_0+0.4\,\delta_1$ | 2.0 | 0.3466152 | 0.3469936 | 0.3470173 | 0.3470185 | 0.3470189 |
| $\delta_1$ (Proca) | 0.5 | 0.02026465 | 0.02026466 | 0.02026466 | 0.02026466 | — |

## 10. Open, in order

1. Read Bochner–Schwartz, the covariant disintegration, and the Wightman →
   Schwinger continuation for a two-form generalized free field, at the level
   of the statements used (E2b's TO READ list minus CPT).
2. Read the SVM primaries and a textbook statement of the dispersive static
   potential; settle attribution.
3. The general tempered case without (I): subtractions add polynomials, which
   should still not reach $r>0$; not proved here.
4. $O(q_W^4)$: the sign of the light-by-light contribution to the static
   potential (roadmap E2.3f). This is where the real open question now sits.
