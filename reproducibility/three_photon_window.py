"""The massless three-photon tail of the QED vacuum polarization (note E4).

In QED the photon self-energy has a cut from s = 0, through three real photons;
it first enters at O(alpha^4). For s << m^2 the vertex gamma* -> 3 gamma is the
Euler-Heisenberg term with one leg off shell: operators with more derivatives,
including those that vanish on shell, carry more powers of momentum and start
one order higher in s. This module computes the leading spectral density by two
independent routes, and the distances at which the 2m pair threshold dominates
the linear probe profile Phi(r) = int exp(-r sqrt(s)) rho_Pi(s) ds.

Conventions: metric (+,-,-,-), Heaviside-Lorentz units, alpha = e^2/(4 pi),
m = 1 in the numerics. rho_Pi = Im Pi/pi, so one Dirac pair gives
(alpha/3 pi)(1 + 2/s) sqrt(1 - 4/s), and d nu = rho_Pi ds is the paper's
measure (spectral_models.dirac_density).

Route A, exact rational arithmetic. L_EH = kappa e^4 P(F) with
P = 14 tr F^4 - 5 (tr F^2)^2 and kappa = 1/(180 (4 pi)^2 m^4) (Groote and
Pivovarov, hep-ph/0103313, eqs. (6)-(7)). The source of the current can attach
to any of the four legs, so <3 gamma|j^mu|0> = 4 * 3! * kappa e^3 Q(q^a, k_i^eps_i),
with Q the symmetric quartic form of P. Then
rho_Pi = (e^2/(6 pi s)) (1/3!) int dPhi_3 sum_pol (-g_{mu nu}) M^mu M^nu*.

Route B. Groote and Pivovarov, eqs. (22) and (28)-(29), give the heavy-quark
current in QCD: rho_GP = (17/243000) d^{abc} d^{abc} (alpha_s/pi)^3 (s/4m^2)^4.
There the photon attaches to the single F of F G G G. Mapping to QED replaces
g_s^6 d^{abc} d^{abc} by (4 e^3)^2 = 16 e^6, and rho_Pi = (alpha/3 pi) rho_GP.

Both routes give rho_Pi = (17/11664000) (alpha/pi)^4 (s/m^2)^4.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from itertools import permutations, product

import mpmath as mp
import sympy as sp

import nonlinear_probe_eh as nl

ETA = (1, -1, -1, -1)
BASIS = tuple(tuple(1 if i == j else 0 for i in range(4)) for j in range(4))


# --- the Euler-Heisenberg quartic form ------------------------------------------
def _mixed(F):
    """M^mu_nu = eta^{mu a} F_{a nu}; then tr F^2 = F^{mu nu} F_{nu mu} = tr M^2."""
    return [[ETA[m] * F[m][n] for n in range(4)] for m in range(4)]


def wedge(k, e):
    """Mixed tensor of F_{mu nu} = k_mu e_nu - k_nu e_mu, for upper-index k and e."""
    kl, el = [ETA[i] * k[i] for i in range(4)], [ETA[i] * e[i] for i in range(4)]
    return _mixed([[kl[m] * el[n] - kl[n] * el[m] for n in range(4)] for m in range(4)])


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _tr(A):
    return sum(A[i][i] for i in range(4))


def quartic_form(Ms):
    """The fully symmetric quartic form Q of P = 14 tr F^4 - 5 (tr F^2)^2."""
    total = Fr(0)
    for p in permutations(range(4)):
        a, b, c, d = (Ms[i] for i in p)
        total += 14 * _tr(_mul(_mul(a, b), _mul(c, d))) - 5 * _tr(_mul(a, b)) * _tr(_mul(c, d))
    return total / 24


def field_tensor(E, B):
    """Mixed tensor of the constant field with electric part E and magnetic part B."""
    F = [[Fr(0)] * 4 for _ in range(4)]
    for i in range(3):
        F[0][i + 1], F[i + 1][0] = Fr(E[i]), -Fr(E[i])
    for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        F[i + 1][j + 1], F[j + 1][i + 1] = -Fr(B[k]), Fr(B[k])
    return _mixed(F)


def eh_polynomial(E, B):
    """(P(F), 8 (E^2-B^2)^2 + 56 (E.B)^2) for fields E, B; kappa e^4 P is the EH term."""
    M = field_tensor(E, B)
    P = 14 * _tr(_mul(_mul(M, M), _mul(M, M))) - 5 * _tr(_mul(M, M)) ** 2
    X = sum(Fr(e) ** 2 for e in E) - sum(Fr(b) ** 2 for b in B)
    Y = sum(Fr(e) * Fr(b) for e, b in zip(E, B))
    return P, 8 * X * X + 56 * Y * Y


def summed_square(momenta):
    """sum over polarizations of |Q(k0^e0, ..., k3^e3)|^2, polarization sums -eta.

    Q is gauge invariant in each leg, so -eta is exact for real photons and,
    since q.M = 0, gives the three polarizations of the massive leg.
    """
    W = [[wedge(k, e) for e in BASIS] for k in momenta]
    total = Fr(0)
    for idx in product(range(4), repeat=4):
        val = quartic_form([W[leg][idx[leg]] for leg in range(4)])
        total += ETA[idx[0]] * ETA[idx[1]] * ETA[idx[2]] * ETA[idx[3]] * val * val
    return total


# --- route A: the three-body cut ------------------------------------------------
# Three photons closing in the centre-of-mass frame: (E, unit direction) per photon.
CONFIGS = (
    (3, (1, 0, 0), 4, (0, 1, 0), 5, (Fr(-3, 5), Fr(-4, 5), 0)),
    (5, (Fr(3, 5), Fr(4, 5), 0), 5, (Fr(3, 5), Fr(-4, 5), 0), 6, (-1, 0, 0)),
    (13, (Fr(5, 13), Fr(12, 13), 0), 15, (Fr(3, 5), Fr(-4, 5), 0), 14, (-1, 0, 0)),
    (5, (1, 0, 0), 12, (0, 1, 0), 13, (Fr(-5, 13), Fr(-12, 13), 0)),
    (8, (1, 0, 0), 15, (0, 1, 0), 17, (Fr(-8, 17), Fr(-15, 17), 0)),
    (7, (1, 0, 0), 24, (0, 1, 0), 25, (Fr(-7, 25), Fr(-24, 25), 0)),
    (1, (1, 0, 0), 1, (1, 0, 0), 2, (-1, 0, 0)),
)


def _three_body(E1, n1, E2, n2, E3, n3):
    """(q, [k1, k2, k3], y) with y_i = 1 - 2E_i/sqrt(s) = s_jk/s."""
    k = [[Fr(E)] + [Fr(c) * E for c in n] for E, n in ((E1, n1), (E2, n2), (E3, n3))]
    q = [k[0][i] + k[1][i] + k[2][i] for i in range(4)]
    if any(q[1:]):
        raise ValueError("the three momenta do not close")
    return q, k, [1 - 2 * ki[0] / q[0] for ki in k]


def three_body_point(E1, n1, E2, n2, E3, n3):
    """(sum |Q|^2 / s^4, y) with y_i = 1 - 2E_i/sqrt(s) = s_jk/s."""
    q, k, y = _three_body(E1, n1, E2, n2, E3, n3)
    return summed_square([q] + k) / q[0] ** 8, y


def _dalitz_fit(points):
    """Fit S = A + B e2 + C e3 + D e2^2 to (value, y) points; (coeffs, residuals, int S dy1 dy2).

    A symmetric polynomial of degree 4 on y1+y2+y3 = 1 has this form; four points
    fix it and the remaining ones are checks.
    """
    y1, y2, y3 = sp.symbols("y1 y2 y3", nonnegative=True)
    A, B, C, D = sp.symbols("A B C D")
    e2, e3 = y1 * y2 + y1 * y3 + y2 * y3, y1 * y2 * y3
    ansatz = A + B * e2 + C * e3 + D * e2 ** 2
    rat = lambda f: sp.Rational(f.numerator, f.denominator)
    pts = [(rat(v), {y1: rat(y[0]), y2: rat(y[1]), y3: rat(y[2])}) for v, y in points]
    coeffs = sp.solve([ansatz.subs(y) - v for v, y in pts[:4]], [A, B, C, D], dict=True)[0]
    S = ansatz.subs(coeffs)
    residuals = [sp.simplify(S.subs(y) - v) for v, y in pts]
    on_simplex = sp.expand(S.subs(y3, 1 - y1 - y2))
    integral = sp.integrate(sp.integrate(on_simplex, (y2, 0, 1 - y1)), (y1, 0, 1))
    return coeffs, residuals, integral


def three_photon_polynomial():
    """sum|Q|^2 = s^4 S(y) on the Dalitz simplex y1+y2+y3 = 1, and int S dy1 dy2."""
    return _dalitz_fit([three_body_point(*cfg) for cfg in CONFIGS])


def route_a_coefficient(integral=None):
    """rho_Pi / [(alpha/pi)^4 (s/m^2)^4] from the cut.

    With M = 24 kappa e^3 Q, dPhi_3 = s/(128 pi^3) dy1 dy2 and 1/3! for identical
    photons, rho_Pi = e^8 kappa^2 s^4 int S/(8 pi^4) = (alpha/pi)^4 (s/m^2)^4 int S/259200.
    """
    if integral is None:
        integral = three_photon_polynomial()[2]
    return integral / 259200


def route_b_coefficient():
    """The same coefficient from Groote-Pivovarov eq. (29) and the abelian map."""
    c_qcd = sp.Rational(17, 243000)          # rho_GP / [d^{abc} d^{abc} (alpha_s/pi)^3 (s/4m^2)^4]
    legs = 4 ** 2                            # the source attaches to any of four legs in QED
    to_rho_pi = sp.Rational(1, 3)            # rho_Pi = (alpha/3 pi) rho_GP = (alpha/pi) rho_GP/3
    to_s_over_m2 = sp.Rational(1, 4 ** 4)    # (s/4m^2)^4 = (s/m^2)^4/256
    return c_qcd * legs * to_rho_pi * to_s_over_m2


def three_body_phase_space():
    """Dalitz normalization s/(128 pi^3) dy1 dy2 against the recursive formula.

    Returns (int dPhi_3 from the Dalitz form, from dPhi_3 = int dM^2/(2 pi) dPhi_2 dPhi_2), s = 1.
    """
    M2 = sp.Symbol("M2", positive=True)
    dalitz = sp.Rational(1, 2) / (128 * sp.pi ** 3)
    recursive = sp.integrate((1 - M2) / (8 * sp.pi) / (8 * sp.pi) / (2 * sp.pi), (M2, 0, 1))
    return sp.simplify(dalitz), sp.simplify(recursive)


# --- checks of the amplitude and of the cut normalization ------------------------
# (cos, sin) of the scattering angle at four rational points
ANGLES = ((Fr(3, 5), Fr(4, 5)), (Fr(5, 13), Fr(12, 13)), (Fr(-8, 17), Fr(15, 17)), (Fr(0), Fr(1)))


def _scattering(cth, sth):
    """gamma gamma -> gamma gamma at omega = 1 in the centre-of-mass frame."""
    return [[Fr(1), 0, 0, Fr(1)], [Fr(1), 0, 0, Fr(-1)], [Fr(1), sth, 0, cth], [Fr(1), -sth, 0, -cth]]


def light_by_light_cross_section():
    """Low-energy gamma gamma -> gamma gamma from the same Q, in alpha^4 omega^6/m^8.

    Returns (dsigma/dOmega, sigma) as sympy expressions in c = cos(theta), omega = 1.
    """
    vals = []
    for cth, sth in ANGLES:
        vals.append((cth, summed_square(_scattering(cth, sth))))
    shape = {v / (3 + c * c) ** 2 for c, v in vals}
    if len(shape) != 1:
        raise ArithmeticError("sum |Q|^2 is not proportional to (3 + cos^2)^2")
    K = shape.pop()
    alpha, m, c = sp.symbols("alpha m c", positive=True)
    kappa = 1 / (180 * (4 * sp.pi) ** 2 * m ** 4)
    msq = (24 * kappa * (4 * sp.pi * alpha) ** 2) ** 2 * sp.Rational(K.numerator, K.denominator) * (3 + c ** 2) ** 2
    dsig = msq / 4 / (2 * 4) / (32 * sp.pi ** 2)            # spin average, flux 1/(2s), s = 4
    sigma = 2 * sp.pi * sp.integrate(dsig, (c, -1, 1)) / 2   # identical photons
    unit = alpha ** 4 / m ** 8
    return sp.simplify(dsig / unit), sp.simplify(sigma / unit)


def _gamma_matrices():
    I2, Z = sp.eye(2), sp.zeros(2)
    sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
    g0 = sp.Matrix(sp.BlockMatrix([[I2, Z], [Z, -I2]]))
    return [g0] + [sp.Matrix(sp.BlockMatrix([[Z, s], [-s, Z]])) for s in sig]


def pair_cut_density(s, m=1):
    """rho_Pi of a Dirac pair from the same cut formula, divided by alpha.

    rho_Pi = (e^2/(6 pi s)) int dPhi_2 sum_spins (-g_{mu nu}) tr[(p1/ + m) g^mu (p2/ - m) g^nu],
    with int dPhi_2 = beta/(8 pi); to be compared with (1/3 pi)(1 + 2m^2/s) beta.
    """
    s, m = sp.nsimplify(s), sp.nsimplify(m)
    g = _gamma_matrices()
    E, beta = sp.sqrt(s) / 2, sp.sqrt(1 - 4 * m ** 2 / s)
    p1, p2 = (E, 0, 0, E * beta), (E, 0, 0, -E * beta)
    slash = lambda p: sum((ETA[i] * p[i] * g[i] for i in range(4)), sp.zeros(4))
    T = 0
    for mu in range(4):
        T += -ETA[mu] * ((slash(p1) + m * sp.eye(4)) * g[mu] * (slash(p2) - m * sp.eye(4)) * g[mu]).trace()
    e2_over_alpha = 4 * sp.pi
    return sp.simplify(e2_over_alpha / (6 * sp.pi * s) * beta / (8 * sp.pi) * T)


# --- two loops: the O(alpha^5) term of the leading coefficient -------------------
# Ritus's two-loop weak-field coefficients. In L = c1 X^2 + c2 Y^2 with X = E^2 - B^2
# and Y = E.B, c1 -> c1 (1 + (40/9) alpha/pi) and c2 -> c2 (1 + (1315/252) alpha/pi):
# Ravndal (hep-ph/9708449, Sect. 3) and Dunne (hep-th/0406216, eqs. (1.9) and (4.11)).
# Below 4m^2 every cut of the two-loop four-photon function passes through the
# fermion loop, so its low-energy limit is this local term (note E4, Section 11).
ONE_LOOP_EH = (8, 56)                       # P = 8 X^2 + 56 Y^2 (eh_polynomial)
TWO_LOOP_EH = (Fr(40, 9), Fr(1315, 252))


def invariant_forms(Ms):
    """(Q_X, Q_Y): the symmetric quartic forms of X^2 and Y^2.

    tr F^2 = 2X and tr F^4 = 2X^2 + 4Y^2, so X^2 = (tr F^2)^2/4 and
    Y^2 = tr F^4/4 - (tr F^2)^2/8; then 8 Q_X + 56 Q_Y = quartic_form.
    """
    a, b, c, d = Ms
    pairs = Fr(_tr(_mul(a, b)) * _tr(_mul(c, d)) + _tr(_mul(a, c)) * _tr(_mul(b, d))
               + _tr(_mul(a, d)) * _tr(_mul(b, c))) / 3
    # the 24 orderings of tr(abcd) form six cyclic classes, each with one ordering starting at a
    quads = sum((_tr(_mul(_mul(a, x), _mul(y, z))) for x, y, z in permutations((b, c, d))), Fr(0)) / 6
    return pairs / 4, quads / 4 - pairs / 8


def invariant_products(momenta):
    """2x2 matrix of sum over polarizations of Q_i Q_j, polarization sums -eta."""
    W = [[wedge(k, e) for e in BASIS] for k in momenta]
    S = [[Fr(0)] * 2 for _ in range(2)]
    for idx in product(range(4), repeat=4):
        q = invariant_forms([W[leg][idx[leg]] for leg in range(4)])
        sign = ETA[idx[0]] * ETA[idx[1]] * ETA[idx[2]] * ETA[idx[3]]
        for i, j in product(range(2), repeat=2):
            S[i][j] += sign * q[i] * q[j]
    return S


def two_loop_factor(S):
    """kappa: a rate quadratic in (c1, c2) with weights S changes by 1 + kappa alpha/pi."""
    c, d = ONE_LOOP_EH, TWO_LOOP_EH
    ij = list(product(range(2), repeat=2))
    return (sum(c[i] * c[j] * (d[i] + d[j]) * S[i][j] for i, j in ij)
            / sum(c[i] * c[j] * S[i][j] for i, j in ij))


def gamma_gamma_two_loop():
    """(W, kappa) for unpolarized low-energy gamma gamma -> gamma gamma.

    For any c1, c2, sum_pol |Q|^2 = (3 + cos^2)^2 sum_ij c_i c_j W_ij.
    """
    shapes = set()
    for cth, sth in ANGLES:
        S = invariant_products(_scattering(cth, sth))
        shapes.add(tuple(S[i][j] / (3 + cth * cth) ** 2 for i, j in product(range(2), repeat=2)))
    if len(shapes) != 1:
        raise ArithmeticError("the weights are not proportional to (3 + cos^2)^2")
    w = shapes.pop()
    W = [[w[0], w[1]], [w[2], w[3]]]
    return W, two_loop_factor(W)


def three_photon_two_loop():
    """(I, kappa): I_ij = int over the Dalitz simplex of the weights, and kappa.

    The O(alpha^5) term of the leading coefficient: 17/11664000 -> (17/11664000)(1 + kappa alpha/pi).
    """
    values = {ij: [] for ij in product(range(2), repeat=2)}
    for cfg in CONFIGS:
        q, k, y = _three_body(*cfg)
        S = invariant_products([q] + k)
        for i, j in values:
            values[(i, j)].append((S[i][j] / q[0] ** 8, y))
    I = [[None] * 2 for _ in range(2)]
    for (i, j), points in values.items():
        _, residuals, integral = _dalitz_fit(points)
        if any(r != 0 for r in residuals):
            raise ArithmeticError("the weights are not of the symmetric degree-4 form")
        I[i][j] = Fr(str(integral))
    return I, two_loop_factor(I)


def self_dual_two_loop_ratio():
    """Two-loop over one-loop quartic term on a self-dual background, in units of alpha/pi.

    Dunne (hep-th/0406216) eqs. (6.2), (6.5) and (6.6), with kappa = m^2/(2 e f) and
    e^2 = 4 pi alpha: L1 = -(e^2 f^2/8 pi^2) int dt/t^3 e^{-2 kappa t} [t^2 coth^2 t - 1 - 2t^2/3]
    and L2 = -alpha^2 (f^2/2 pi^2) [3 xi^2 - xi'], where xi = -kappa(psi - ln kappa + 1/2kappa)
    ~ sum_n B_2n/(2n kappa^(2n-1)) (DLMF 5.11.2). Their f^4 terms are
    -(e^2 f^2/8 pi^2) A1/kappa^2 and -alpha^2 (f^2/2 pi^2) A2/kappa^2, so the ratio is
    (A2/A1) alpha/pi. A self-dual field has (E^2-B^2)^2 = 4 eps^4 and (E.B)^2 = -eps^4 in
    Ritus's eigenvalues, so it measures 4 c1 - c2: an independent check of TWO_LOOP_EH.
    """
    k, t = sp.symbols("kappa t", positive=True)
    xi = sum(sp.bernoulli(2 * n) / (2 * n) / k ** (2 * n - 1) for n in (1, 2, 3))
    A2 = sp.limit(k ** 2 * (3 * xi ** 2 - sp.diff(xi, k)), k, sp.oo)
    lead = sp.series(t ** 2 * sp.coth(t) ** 2 - 1 - 2 * t ** 2 / 3, t, 0, 6).removeO()
    A1 = sp.simplify(k ** 2 * sp.integrate(lead / t ** 3 * sp.exp(-2 * k * t), (t, 0, sp.oo)))
    return Fr(str(A2 / A1))


# --- the window in r ---------------------------------------------------------------
def three_photon_rho_coefficient():
    return sp.Rational(17, 11664000)


def phi_three_photon(r, alpha, factor=1, b=0):
    """Leading tail 2 K Gamma(10)/r^10 = (238/225)(alpha/pi)^4/r^10, m = 1.

    By Watson's lemma the relative correction is O(1/r^2); b parametrizes an
    s^5 term, rho = K s^4 (1 + b s/4), which multiplies the tail by 1 + 27.5 b/r^2.
    """
    a, r = mp.mpf(alpha), mp.mpf(r)
    K = mp.mpf(17) / 11664000 * (a / mp.pi) ** 4 * factor
    return 2 * K * mp.factorial(9) / r ** 10 * (1 + mp.mpf(b) * 110 / 4 / r ** 2)


def _pair_density(alpha, sommerfeld):
    dnu = nl.dirac_dnu(alpha)
    if not sommerfeld:
        return dnu
    a = mp.mpf(alpha)

    def corrected(x):
        z = mp.pi * a / mp.sqrt(1 - 4 / x ** 2)
        return dnu(x) * z / (1 - mp.e ** (-z))
    return corrected


def phi_pair_moment(r, alpha, k=0, sommerfeld=False):
    """int x^k e^{-rx} d nu over the one-loop pair cut, optionally with the Sommerfeld factor."""
    r = mp.mpf(r)
    dnu = _pair_density(alpha, sommerfeld)
    cuts = [2, 2 + 1 / r, 2 + 4 / r, 2 + 16 / r, 3, 4, 8, mp.inf]
    return nl.quad_relative(lambda x: x ** k * mp.e ** (-r * x) * dnu(x), cuts, mp.e ** (-2 * r))


def total_gamma(r, alpha, factor=1, b=0, sommerfeld=False):
    """-d log(Phi_pair + Phi_3gamma)/dr, with the pair part as an exact moment ratio."""
    r = mp.mpf(r)
    p0, p1 = phi_pair_moment(r, alpha, 0, sommerfeld), phi_pair_moment(r, alpha, 1, sommerfeld)
    t = phi_three_photon(r, alpha, factor, b)
    t_gamma = 10 / r + mp.mpf(b) * 110 / 2 / r ** 3 / (1 + mp.mpf(b) * 110 / 4 / r ** 2)
    return (p1 + t * t_gamma) / (p0 + t)


def window(alpha, factor=1, b=0, sommerfeld=False, dps=30):
    """(r_x, r_Gamma): Phi_pair = Phi_3gamma, and Gamma = 2m, in units of 1/m."""
    with mp.workdps(dps):
        r_x = mp.findroot(lambda r: mp.log(phi_pair_moment(r, alpha, 0, sommerfeld))
                          - mp.log(phi_three_photon(r, alpha, factor, b)), 22)
        r_g = mp.findroot(lambda r: total_gamma(r, alpha, factor, b, sommerfeld) - 2, 20.5)
        return r_x, r_g
