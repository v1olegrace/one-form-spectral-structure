"""The static Wilson loop at fourth order in the probe charge, in the
Euler-Heisenberg effective theory (note E3).

notes/E3_nonlinear_probe_EH.md states that, for two rigid spherically
symmetric sources of radius R at separation r > 2R, with 1/m << R and weak
fields everywhere, the O(q^4) part of the static energy at fixed free charge
is -c int |E_0|^4, with c = e^4/(360 pi^2 m^4) and E_0 the vacuum Coulomb
field of the two sources. The r-dependent part is

    U4(r) = -c [4 q1^3 q2 I31 + 4 q1 q2^3 I13 + q1^2 q2^2 I22],
    I31 = int |d1|^2 (d1 . d2),
    I22 = int [2 |d1|^2 |d2|^2 + 4 (d1 . d2)^2],

with d_i the field of source i for unit charge. This module evaluates I31 and
I22 by quadrature in bipolar coordinates, without the closed forms that the
note compares them with, and checks the sign of the fixed-charge energy on a
single source by solving the nonlinear radial problem exactly.

The linear one-loop profile used for the crossover is taken from
reproducibility/spectral_models.py (dirac_density), the model the paper uses.

The ball and infinitesimally thin shell are benchmarks of the local quartic
functional, with sharp boundaries that do not meet the EFT slow-variation
assumption. Boundary derivative corrections are not controlled. The crossover
combines a point-source linear profile with the exterior nonlinear tail; it
is not a prediction matched to the same smooth source. Isolated source
self-energies are r-independent; the mixed polarizability is an interaction.

Nothing here is an interval certificate: the quadratures are CHECKED, not
CERTIFIED. The first-order flux is cubic in q_W; cancellation of that cubic
term isolates the linear coefficient only within this truncation. A general
odd response retains an O(q_W^4) error from its quintic term.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy import integrate, special

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spectral_models as sm  # noqa: E402

FOUR_PI = 4.0 * math.pi


# --- Euler-Heisenberg coefficient ---------------------------------------------
def eh_c(alpha, m=1.0):
    """c in L = E^2/2 + c E^4 (static, Heaviside-Lorentz, hbar = c = 1).

    Dunne, arXiv:hep-th/0406216, eq. (1.9): e^4/(360 pi^2 m^4) times
    (E^2 - B^2)^2 + 7 (E.B)^2; with e^2 = 4 pi alpha this is 2 alpha^2/(45 m^4).
    """
    e2 = 4.0 * math.pi * alpha
    return e2 * e2 / (360.0 * math.pi ** 2 * m ** 4)


# --- unit-charge fields of spherical sources ----------------------------------
def _out(x):
    return x if x.ndim else float(x)


def g_ball(u, R):
    """Unit-charge uniform-ball field; a sharp-edge benchmark of the local term."""
    u = np.asarray(u, dtype=float)
    far = 1.0 / (FOUR_PI * np.maximum(u, 1e-300) ** 2)
    return _out(np.where(u < R, u / (FOUR_PI * R ** 3), far))


def g_shell(u, R):
    """Unit-charge thin-shell field; a sharp-edge benchmark of the local term."""
    u = np.asarray(u, dtype=float)
    far = 1.0 / (FOUR_PI * np.maximum(u, 1e-300) ** 2)
    return _out(np.where(u < R, 0.0, far))


def g_gaussian(u, R):
    """Smooth unit-charge field for rho=exp(-u^2/R^2)/(pi^(3/2) R^3).

    Its scale R is a width, not a compact support radius. A small-u series
    avoids subtracting two nearly equal terms in the enclosed charge.
    """
    u = np.asarray(u, dtype=float)
    z = u / R
    safe_z = np.maximum(z, 1e-100)
    enclosed = special.erf(z) - 2.0 / math.sqrt(math.pi) * z * np.exp(-z * z)
    regular = enclosed / (FOUR_PI * (R * safe_z) ** 2)
    series = z * (1.0 / 3.0 - z ** 2 / 5.0 + z ** 4 / 14.0 - z ** 6 / 54.0)
    series /= math.pi ** 1.5 * R ** 2
    return _out(np.where(z < 1e-3, series, regular))


PROFILES = {"ball": g_ball, "shell": g_shell, "gaussian": g_gaussian}


def gaussian_density(r, R):
    return math.exp(-(r / R) ** 2) / (math.pi ** 1.5 * R ** 3)


def gaussian_yukawa(r, R, mass):
    """Exact convolution of the Yukawa kernel with the same Gaussian source.

    The erfcx branch avoids overflow when mass*R is large. This is a finite
    atomic spectral benchmark; it is not the full QED one-loop kernel.
    """
    if r <= 0 or R <= 0 or mass < 0:
        raise ValueError("r,R must be positive and mass nonnegative")
    x, b = r / R, mass * R / 2.0
    if b >= x:
        first = math.exp(-x * x) * special.erfcx(b - x)
    else:
        first = math.exp(b * b - mass * r) * special.erfc(b - x)
    second = math.exp(-x * x) * special.erfcx(b + x)
    return (first - second) / (8.0 * math.pi * r)


def matched_gaussian_phi(r, q, R, c, mass, weight):
    """Corrections to the Gaussian Coulomb flux: O(weight) + O(c q^2).

    Both terms use rho_R. The linear correction is a positive Yukawa atom;
    the quartic correction is evaluated on the Maxwell field of rho_R.
    Mixed weight*c, weight^2 and higher EH operators are omitted explicitly.
    Return the separate terms so no full-QED interpretation is implicit.
    """
    rho = gaussian_density(r, R)
    g = g_gaussian(r, R)
    gp = rho - 2.0 * g / r  # radial Gauss law
    linear = weight * FOUR_PI * r * (mass ** 2 * gaussian_yukawa(r, R, mass) - rho)
    nonlinear = 16.0 * math.pi * c * q ** 2 * (2.0 * g ** 3 + 3.0 * r * g ** 2 * gp)
    return {"linear": linear, "nonlinear": nonlinear, "total": linear + nonlinear}


def local_quartic_remainder_bound(q, R, c, profile="gaussian"):
    """8 c^2 int |D|^6: analytic upper bound in the radial local quartic model.

    Quadrature evaluates its value; that value is CHECKED, not an interval
    certificate. The pointwise inequality is proved in E3 Section 10.
    """
    if c < 0:
        raise ValueError("the convex Legendre bound requires c >= 0")
    g = PROFILES[profile]
    f = lambda u: FOUR_PI * u * u * (q * g(u, R)) ** 6
    a = integrate.quad(f, 0.0, R, epsabs=0.0, epsrel=1e-12)[0]
    b = integrate.quad(f, R, math.inf, epsabs=0.0, epsrel=1e-12)[0]
    return 8.0 * c * c * (a + b)


# --- bipolar quadrature -------------------------------------------------------
_GX, _GW = np.polynomial.legendre.leggauss(40)


def _nodes(edges):
    """Composite Gauss-Legendre nodes and weights on consecutive edges."""
    xs, ws = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        if b > a:
            h, m = 0.5 * (b - a), 0.5 * (b + a)
            xs.append(m + h * _GX)
            ws.append(h * _GW)
    return np.concatenate(xs), np.concatenate(ws)


def _geometric(start, stop):
    out, x = [], start
    while x < stop:
        out.append(x)
        x *= 2.0
    return out


def _bipolar(f, r, R1, R2):
    """(2 pi / r) int du int dv u v f(u, v, cos) over |u - v| <= r <= u + v.

    u, v are the distances to the two centres and cos = (u^2 + v^2 - r^2)/(2 u v)
    is the cosine between the two radial unit vectors. Composite Gauss-Legendre:
    edges at the kinks of the profiles (u = R1; v = R2, which the lower limit
    |r - u| crosses at u = r -+ R2; u = r) and on geometric ladders where a
    Coulomb field is steep (u = R1 2^k, v = R2 2^k, u = r -+ R2 2^k). The tail
    u > 2r is mapped to t = 2r/u in (0, 1].
    """
    half = 0.5 * r
    eu = {0.0, half, r, 1.5 * r, 2.0 * r, R1}
    eu |= set(_geometric(R1, half))
    eu |= {r - x for x in _geometric(R2, half)} | {r + x for x in _geometric(R2, half)}
    us, wus = _nodes(sorted(x for x in eu if 0.0 <= x <= 2.0 * r))
    t, wt = _nodes([0.0, 0.5, 1.0])
    us = np.concatenate([us, 2.0 * r / t])
    wus = np.concatenate([wus, wt * 2.0 * r / t ** 2])
    ladder = _geometric(R2, 4.0 * r) + [half, r, 1.5 * r, 2.0 * r]
    total = 0.0
    for u, wu in zip(us, wus):
        lo, hi = abs(r - u), r + u
        ev = sorted({lo, hi} | {x for x in ladder if lo < x < hi})
        v, wv = _nodes(ev)
        cos = (u * u + v * v - r * r) / (2.0 * u * v)
        total += wu * np.dot(wv, u * v * f(u, v, cos))
    return 2.0 * math.pi / r * total


def I31(r, R1, R2, profile1="ball", profile2="ball"):
    """int |d1|^2 (d1 . d2) d^3x for unit charges."""
    g1, g2 = PROFILES[profile1], PROFILES[profile2]
    return _bipolar(lambda u, v, cos: g1(u, R1) ** 3 * g2(v, R2) * cos, r, R1, R2)


def I22(r, R1, R2, profile1="ball", profile2="ball"):
    """int [2 |d1|^2 |d2|^2 + 4 (d1 . d2)^2] d^3x for unit charges."""
    g1, g2 = PROFILES[profile1], PROFILES[profile2]
    return _bipolar(lambda u, v, cos: (g1(u, R1) * g2(v, R2)) ** 2 * (2.0 + 4.0 * cos * cos),
                    r, R1, R2)


def self_energy(R, profile="ball"):
    """W = (1/2) int |d|^2 for unit charge."""
    g = PROFILES[profile]
    inside, _ = integrate.quad(lambda u: FOUR_PI * u * u * g(u, R) ** 2, 0.0, R,
                               epsabs=0.0, epsrel=1e-13)
    outside, _ = integrate.quad(lambda u: FOUR_PI * u * u * g(u, R) ** 2, R, math.inf,
                                epsabs=0.0, epsrel=1e-13)
    return 0.5 * (inside + outside)


def u4_interaction(r, q1, q2, R1, R2, c, profile1="ball", profile2="ball"):
    """The r-dependent O(c) energy of two sources at fixed free charge."""
    i31 = I31(r, R1, R2, profile1, profile2)
    i13 = I31(r, R2, R1, profile2, profile1)
    i22 = I22(r, R1, R2, profile1, profile2)
    return -c * (4.0 * q1 ** 3 * q2 * i31 + 4.0 * q1 * q2 ** 3 * i13 + q1 * q1 * q2 * q2 * i22)


# --- sign of the fixed-charge energy, one source, exactly ---------------------
def single_source_energy(q, R, c, profile="ball"):
    """Energy of one spherical source at fixed free charge in L = E^2/2 + c E^4.

    With spherical symmetry D = q d(u) exactly (Gauss). E solves E + 4 c E^3 = D
    (Newton, started at D), and the energy density is D E - L = E^2/2 + 3 c E^4.
    """
    g = PROFILES[profile]

    def density(u):
        D = q * g(u, R)
        E = D
        for _ in range(60):
            step = (E + 4.0 * c * E ** 3 - D) / (1.0 + 12.0 * c * E * E)
            E -= step
            if abs(step) <= 1e-17 * max(abs(E), 1e-300):
                break
        return FOUR_PI * u * u * (0.5 * E * E + 3.0 * c * E ** 4)

    a, _ = integrate.quad(density, 0.0, R, epsabs=0.0, epsrel=1e-13, limit=200)
    b, _ = integrate.quad(density, R, math.inf, epsabs=0.0, epsrel=1e-13, limit=200)
    return a + b


def int_D4(q, R, profile="ball"):
    """int |D_0|^4 d^3x for one source."""
    g = PROFILES[profile]
    a, _ = integrate.quad(lambda u: FOUR_PI * u * u * (q * g(u, R)) ** 4, 0.0, R,
                          epsabs=0.0, epsrel=1e-13)
    b, _ = integrate.quad(lambda u: FOUR_PI * u * u * (q * g(u, R)) ** 4, R, math.inf,
                          epsabs=0.0, epsrel=1e-13)
    return a + b


# --- the profile at finite probe charge ---------------------------------------
def flux_E(r, qW, gR2, c):
    """q(r) of eq:qdef (flux of E over g_R^2, paper units) outside a static source.

    Canonical charge q = g_R q_W; D = q/(4 pi r^2) exactly; E = D - 4 c D^3 + O(c^2).
    """
    q = math.sqrt(gR2) * qW
    D = q / (FOUR_PI * r * r)
    E = D - 4.0 * c * D ** 3
    return FOUR_PI * r * r * E / math.sqrt(gR2)


def phi_nl_qed(r, qW, alpha, m=1.0):
    """Phi_NL = -c g_R^2 q_W^2/(pi^2 r^6) = -8 alpha^3 q_W^2/(45 pi m^4 r^6)."""
    return -8.0 * alpha ** 3 * qW ** 2 / (45.0 * math.pi * m ** 4 * r ** 6)


def qed_model(alpha):
    """One-loop Dirac profile of the paper (spectral_models.dirac_density), m = 1."""
    g2 = 4 * mp.pi * mp.mpf(alpha)
    return sm.Model(name="qed_one_loop", description="one Dirac fermion, m = 1",
                    branches=[(2, sm.dirac_density(m=1, q=1, g2=g2), 1.5)],
                    M_star=2, edge_p=1.5)


def phi_lin_qed(r, alpha):
    """Point-source Phi_lin for the one-loop Dirac measure, m = 1."""
    model = qed_model(alpha)
    return mp.e ** (-2 * mp.mpf(r)) * model.Phi_scaled(r)


def crossover(qW, alpha, guess=12.0):
    """Formal point-linear/exterior-EH crossover in units 1/m, CHECKED only.

    The two pieces have not been matched to the same extended source. This
    is not a controlled point-probe or full-QED prediction.
    """
    model = qed_model(alpha)
    a3 = mp.mpf(alpha) ** 3

    def f(rr):
        lin = -2 * rr + mp.log(model.Phi_scaled(rr))
        nl = mp.log(8 * a3 * mp.mpf(qW) ** 2 / (45 * mp.pi * rr ** 6))
        return lin - nl

    return mp.findroot(f, mp.mpf(guess))


# --- extended probes with the one-loop Dirac measure (note E3, Section 11) ----
# Units m = 1. The linear response kernel is 1/Q^2 + int dnu(x)/(x^2 (Q^2+x^2)),
# with dnu the paper's measure (spectral_models.dirac_density, g^2 = 4 pi alpha).
# All values below are CHECKED by quadrature, never interval certificates.


def quad_relative(f, cuts, scale):
    """mp.quad of f over cuts, made relative by dividing f by a bound of |f|.

    mp.quad stops once its error estimate is below 2^(4-prec) in absolute
    terms. An integrand far below that (the profiles at r of order 100/m are
    about e^-200) is integrated at the coarsest level, and the result is
    stable in dps and wrong. Refuses when the estimate is not small relative
    to the result.
    """
    val, err = mp.quad(lambda x: f(x) / scale, cuts, error=True)
    if not err <= mp.mpf(10) ** (10 - mp.mp.dps) * abs(val):
        raise ArithmeticError("quadrature error estimate %s for a value %s"
                              % (mp.nstr(err, 3), mp.nstr(val, 3)))
    return val * scale


_quad_relative = quad_relative   # the earlier private name, for older scripts

# Radial Laplacian powers of exp(-y^2), y = r/R: lap^k rho = P_k(y) rho / R^(2k).
_GAUSS_LAPLACIAN = (lambda y: 1,
                    lambda y: 4 * y ** 2 - 6,
                    lambda y: 16 * y ** 4 - 80 * y ** 2 + 60,
                    lambda y: 64 * y ** 6 - 672 * y ** 4 + 1680 * y ** 2 - 840)


def dirac_dnu(alpha):
    """dnu/dx of the paper's one-loop Dirac measure, m = 1, x = sqrt(s)."""
    return sm.dirac_density(m=1, q=1, g2=4 * mp.pi * mp.mpf(alpha))


def vacuum_polarization(k2, alpha):
    """Subtracted one-loop Pi_bar(k^2), Euclidean, m = 1.

    Closed form of (2 alpha/pi) int_0^1 t(1-t) log(1 + t(1-t) k^2) dt. It does
    not use the spectral density, so the momentum routes below are an
    independent check of the spectral routes. Below k^2 = 1e-2 the closed form
    cancels, and the Taylor series sum (-1)^(n+1)/n ((n+1)!)^2/(2n+3)! k^(2n)
    is used instead.
    """
    k2, a = mp.mpf(k2), mp.mpf(alpha)
    if k2 < mp.mpf("1e-2"):
        total = mp.mpf(0)
        for n in range(1, 16):
            total += ((-1) ** (n + 1) * mp.factorial(n + 1) ** 2
                      / (n * mp.factorial(2 * n + 3)) * k2 ** n)
        return 2 * a / mp.pi * total
    beta = mp.sqrt(1 + 4 / k2)
    return a / (3 * mp.pi) * ((1 - 2 / k2) * beta * mp.log((beta + 1) / (beta - 1))
                              + 4 / k2 - mp.mpf(5) / 3)


def _gauss_rho_mp(r, R):
    return mp.e ** (-(r / R) ** 2) / (mp.pi ** 1.5 * R ** 3)


def _gauss_yukawa_mp(mass, r, R):
    """Multiprecision Yukawa(mass) * rho_R at distance r; no overflow in mpmath."""
    b, y = mass * R / 2, r / R
    return mp.e ** (b * b) / (8 * mp.pi * r) * (mp.e ** (-mass * r) * mp.erfc(b - y)
                                                - mp.e ** (mass * r) * mp.erfc(b + y))


def gaussian_dirac_phi_lin(r, R, alpha, dps=30):
    """Linear profile of the Gaussian probe, spectral route.

    Phi = 4 pi r int dnu(x) [K_x(r) - rho_R(r)/x^2], K_x the Yukawa kernel
    smeared with rho_R; the Maxwell flux of rho_R is subtracted first. For
    x >= X the bracket is replaced by its expansion
    sum_k lap^k rho_R / x^(2k+2), k = 1..3; this avoids the cancellation
    K - rho/x^2 at large x. The truncation is not exact: at R = 10 and
    r = 5..300 the omitted k = 4 term is below 3e-16 of Phi (note E3, 11.2).
    Since K_x <= K_2 for x >= 2, the bracket is bounded by K_2 + rho_R/4,
    which sets the scale for quad_relative.
    """
    with mp.workdps(dps):
        r, R = mp.mpf(r), mp.mpf(R)
        dnu, y = dirac_dnu(alpha), r / R
        X = max(mp.mpf(40), 200 * (1 + y) / R)
        rho = _gauss_rho_mp(r, R)
        cuts = ({mp.mpf(2), mp.mpf("2.5"), mp.mpf(3), mp.mpf(5), mp.mpf(10), mp.mpf(20), X}
                | {2 + mp.mpf(k) / r for k in (1, 4, 16) if 2 + mp.mpf(k) / r < X}
                | ({2 * y / R} if 2 < 2 * y / R < X else set()))
        direct = quad_relative(lambda x: dnu(x) * (_gauss_yukawa_mp(x, r, R) - rho / x ** 2),
                                sorted(cuts), _gauss_yukawa_mp(mp.mpf(2), r, R) + rho / 4)
        tail = mp.mpf(0)
        for k in (1, 2, 3):
            moment = mp.quad(lambda x: dnu(x) / x ** (2 * k + 2), [X, mp.inf])
            tail += _GAUSS_LAPLACIAN[k](y) * rho / R ** (2 * k) * moment
        return 4 * mp.pi * r * (direct + tail)


def gaussian_dirac_phi_lin_momentum(r, R, alpha, dps=30):
    """Same profile, momentum route: -(2/pi) int k sin(kr) e^{-k^2 R^2/4} Pi_bar dk.

    Independent of the spectral density and of the Yukawa smearing formula.
    The oscillatory cancellation limits it to moderate r/R (about r <= 5R at
    30-40 digits); at larger r only the spectral route has the precision.
    """
    with mp.workdps(dps):
        r, R = mp.mpf(r), mp.mpf(R)
        kmax = 2 * mp.sqrt(200) / R
        nodes = [mp.mpf(0)] + [mp.pi * j / r for j in range(1, int(kmax * r / mp.pi) + 2)]
        f = lambda k: k * mp.sin(k * r) * mp.e ** (-(k * R) ** 2 / 4) * vacuum_polarization(k * k, alpha)
        return -2 / mp.pi * mp.quad(f, nodes)


def gaussian_local_uehling_phi(r, R, alpha, dps=30):
    """Leading derivative-expansion term (4 alpha/15) r lap(rho_R), m = 1.

    It uses int dnu(x)/x^4 = alpha/(15 pi), the Uehling coefficient
    alpha/(15 pi m^2) of the local F box F operator: 4 pi r lap(rho) times it.
    """
    with mp.workdps(dps):
        r, R = mp.mpf(r), mp.mpf(R)
        y = r / R
        return 4 * mp.mpf(alpha) / 15 * r * _GAUSS_LAPLACIAN[1](y) * _gauss_rho_mp(r, R) / R ** 2


def gaussian_dirac_phi_nl(r, q, R, alpha, dps=30):
    """16 pi c q^2 [2 g^3 + 3 r g^2 g'] for the same Gaussian, in multiprecision."""
    with mp.workdps(dps):
        r, R, q = mp.mpf(r), mp.mpf(R), mp.mpf(q)
        y = r / R
        g = (mp.erf(y) - 2 / mp.sqrt(mp.pi) * y * mp.e ** (-y * y)) / (4 * mp.pi * r * r)
        gp = _gauss_rho_mp(r, R) - 2 * g / r
        c = 2 * mp.mpf(alpha) ** 2 / 45
        return 16 * mp.pi * c * q * q * (2 * g ** 3 + 3 * r * g * g * gp)


def gaussian_dirac_crossover(q, R, alpha, bracket, dps=30):
    """Zero of the matched first-order sum Phi_lin + Phi_NL, Gaussian probe."""
    with mp.workdps(dps):
        f = lambda r: gaussian_dirac_phi_lin(r, R, alpha, dps) + gaussian_dirac_phi_nl(r, q, R, alpha, dps)
        return mp.findroot(f, (mp.mpf(bracket[0]), mp.mpf(bracket[1])), solver="anderson")


def ball_exterior_factor(x, a):
    """F(x) = int rho sinh(xu)/(xu) d^3u for a uniform ball: 3 i_1(xa)/(xa)."""
    z = mp.mpf(x) * a
    if z < mp.mpf("1e-2"):
        return 1 + z ** 2 / 10 + z ** 4 / 280
    return 3 * (z * mp.cosh(z) - mp.sinh(z)) / z ** 3


def polynomial_exterior_factor(x, a, n=2):
    """F(x) for rho proportional to (1 - u^2/a^2)^n on u < a, by quadrature.

    Extended by zero, this density is C^(n-1) at u = a: n = 2 is C^1, not smooth.
    """
    w = lambda u: u * u * (1 - (u / a) ** 2) ** n
    norm = mp.quad(w, [0, a])
    return mp.quad(lambda u: w(u) * mp.sinh(x * u) / (x * u), [0, a / 2, a]) / norm


def polynomial2_exterior_factor(x, a):
    """Closed form of polynomial_exterior_factor(x, a, 2): 105 i_3(z)/z^3, z = xa.

    The closed form cancels for small z, where the quadrature is used instead.
    """
    z = mp.mpf(x) * a
    if z < 5:
        return polynomial_exterior_factor(x, a, 2)
    return 105 * (z ** 3 * mp.cosh(z) - 6 * z ** 2 * mp.sinh(z)
                  + 15 * z * mp.cosh(z) - 15 * mp.sinh(z)) / z ** 7


def _exterior_moment(r, a, alpha, factor, k):
    """int x^k e^{-rx} F(x) dnu(x) at r > a.

    F'/F <= a for a non-negative density inside radius a, so e^{-rx} F(x) is
    at most e^{-2r} F(2) on x >= 2; that bound is the scale for quad_relative.
    """
    if r <= a:
        raise ValueError("the exterior representation needs r > a")
    dnu = dirac_dnu(alpha)
    cuts = ({mp.mpf(2), mp.mpf("2.5"), mp.mpf(3), mp.mpf(4), mp.mpf(8)}
            | {2 + mp.mpf(j) / (r - a) for j in (1, 4, 16) if 2 + mp.mpf(j) / (r - a) < 8})
    return quad_relative(lambda x: x ** k * mp.e ** (-r * x) * factor(x, a) * dnu(x),
                          sorted(cuts) + [mp.inf], mp.e ** (-2 * r) * factor(mp.mpf(2), a))


def exterior_dirac_phi_lin(r, a, alpha, factor=ball_exterior_factor, dps=30):
    """int e^{-rx} F(x) dnu(x): the exact linear profile at r > a (exterior lemma)."""
    with mp.workdps(dps):
        return _exterior_moment(mp.mpf(r), mp.mpf(a), alpha, factor, 0)


def exterior_dirac_gamma(r, a, alpha, factor=ball_exterior_factor, dps=30):
    """Gamma = int x e^{-rx} F dnu / int e^{-rx} F dnu, with no finite difference."""
    with mp.workdps(dps):
        r, a = mp.mpf(r), mp.mpf(a)
        return _exterior_moment(r, a, alpha, factor, 1) / _exterior_moment(r, a, alpha, factor, 0)


def ball_dirac_phi_lin_momentum(r, a, alpha, dps=40):
    """Uniform-ball profile by Fourier transform: -(2/pi) int k sin(kr) rho_hat Pi_bar dk.

    rho_hat = 3 j_1(ka)/(ka) decays only like 1/k^2, so beyond k0 the integrand
    is split exactly into pure oscillations of frequency r-a and r+a and each
    is summed with mp.quadosc. Independent of the exterior lemma. At 30 digits
    the quadosc extrapolation returns a wrong value without warning (observed
    at r = 11, a = 10); 40 and 50 digits agree, so the default is 40.
    """
    with mp.workdps(dps):
        r, a = mp.mpf(r), mp.mpf(a)

        def rho_hat(k):
            z = k * a
            if z < mp.mpf("1e-3"):
                return 1 - z * z / 10 + z ** 4 / 280
            return 3 * (mp.sin(z) - z * mp.cos(z)) / z ** 3

        k0 = mp.mpf(40)
        head = mp.quad(lambda k: k * mp.sin(k * r) * rho_hat(k) * vacuum_polarization(k * k, alpha),
                       mp.linspace(0, k0, 400))

        def osc(freq, trig, power):
            return mp.quadosc(lambda k: trig(freq * k) * vacuum_polarization(k * k, alpha) / k ** power,
                              [k0, mp.inf], omega=freq)

        # k sin(kr) 3[sin ka - ka cos ka]/(ka)^3 = (3/a^3)[sin kr sin ka/k^2 - a sin kr cos ka/k]
        t1 = (osc(r - a, mp.cos, 2) - osc(r + a, mp.cos, 2)) / 2
        t2 = -a * (osc(r + a, mp.sin, 1) + osc(r - a, mp.sin, 1)) / 2
        return -2 / mp.pi * (head + 3 / a ** 3 * (t1 + t2))


def exterior_dirac_crossover(q, a, alpha, bracket, factor=ball_exterior_factor, dps=30):
    """Zero of int e^{-rx} F dnu - c q^2/(pi^2 r^6) at r > a (first order in c)."""
    with mp.workdps(dps):
        c = 2 * mp.mpf(alpha) ** 2 / 45
        q = mp.mpf(q)
        f = lambda r: (exterior_dirac_phi_lin(r, a, alpha, factor, dps)
                       - c * q * q / (mp.pi ** 2 * r ** 6))
        return mp.findroot(f, (mp.mpf(bracket[0]), mp.mpf(bracket[1])), solver="anderson")


def log_slope(f, r, h="1e-6", dps=30):
    """Gamma = -d log Phi/dr by a central difference, in multiprecision."""
    with mp.workdps(dps):
        r, h = mp.mpf(r), mp.mpf(h)
        return -(mp.log(f(r + h)) - mp.log(f(r - h))) / (2 * h)


# --- the energy bound for arbitrary sources: a lattice check -------------------
def lattice_gradient(n):
    """Edge gradient G on an n x n grid with a grounded boundary.

    (G phi)_e = phi(head) - phi(tail); boundary nodes carry phi = 0. Then
    (div D)_v = -(G^T D)_v and sum_v rho_v phi_v = sum_e D_e E_e for E = -G phi.
    """
    import scipy.sparse as sps
    index = -np.ones((n, n), dtype=int)
    k = 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            index[i, j] = k
            k += 1
    rows, cols, vals, e = [], [], [], 0
    for i in range(n):
        for j in range(n):
            for di, dj in ((1, 0), (0, 1)):
                if i + di >= n or j + dj >= n:
                    continue
                tail, head = index[i, j], index[i + di, j + dj]
                if tail < 0 and head < 0:
                    continue
                if head >= 0:
                    rows.append(e); cols.append(head); vals.append(1.0)
                if tail >= 0:
                    rows.append(e); cols.append(tail); vals.append(-1.0)
                e += 1
    return sps.csr_matrix((vals, (rows, cols)), shape=(e, k)), index


def lattice_energy(G, rho, c):
    """min sum_e h_c(D_e) subject to div D = rho, solved through its concave dual.

    Newton on J(phi) = rho.phi - sum_e L_c(E_e), E = -G phi, L_c = E^2/2 + c E^4.
    Returns the primal value at D = L_c'(E), the dual value and the
    constraint residual; strong duality is checked, not assumed.
    """
    import scipy.sparse as sps
    import scipy.sparse.linalg as spla
    phi = spla.spsolve((G.T @ G).tocsc(), rho)
    for _ in range(100):
        E = -(G @ phi)
        D = E + 4 * c * E ** 3
        step = spla.spsolve((G.T @ sps.diags(1 + 12 * c * E * E) @ G).tocsc(), rho + G.T @ D)
        phi = phi + step
        if np.max(np.abs(step)) < 1e-15 * (1 + np.max(np.abs(phi))):
            break
    E = -(G @ phi)
    D = E + 4 * c * E ** 3
    Ep = D.copy()
    for _ in range(80):  # invert D = E + 4 c E^3 independently, then h = E^2/2 + 3cE^4
        Ep -= (Ep + 4 * c * Ep ** 3 - D) / (1 + 12 * c * Ep * Ep)
    primal = float(np.sum(0.5 * Ep * Ep + 3 * c * Ep ** 4))
    dual = float(rho @ phi - np.sum(0.5 * E * E + c * E ** 4))
    return {"primal": primal, "dual": dual, "residual": float(np.max(np.abs(-G.T @ D - rho))), "D": D}


def int_D6_pair(r, q1, q2, R1, R2, profile1="gaussian", profile2="gaussian"):
    """int |q1 d1 + q2 d2|^6 d^3x by bipolar quadrature."""
    g1, g2 = PROFILES[profile1], PROFILES[profile2]
    return _bipolar(lambda u, v, cos: ((q1 * g1(u, R1)) ** 2 + (q2 * g2(v, R2)) ** 2
                                       + 2 * q1 * q2 * g1(u, R1) * g2(v, R2) * cos) ** 3, r, R1, R2)


def interaction_remainder_bound(r, q1, q2, R1, R2, c, profile1="gaussian", profile2="gaussian"):
    """|V_c - (V_0 - c W_4)| <= 8 c^2 max(I6(pair), I6(1) + I6(2)), by Section 11.4."""
    single = (local_quartic_remainder_bound(q1, R1, c, profile1)
              + local_quartic_remainder_bound(q2, R2, c, profile2))
    pair = 8.0 * c * c * int_D6_pair(r, q1, q2, R1, R2, profile1, profile2)
    return max(pair, single)


if __name__ == "__main__":
    pi3 = math.pi ** 3
    print("c(alpha) / alpha^2 =", eh_c(1.0 / 137.035999) / (1.0 / 137.035999) ** 2,
          " (2/45 =", 2 / 45, ")")
    for R in (0.1, 0.2, 0.3):
        val = I31(1.0, R, R)
        ref = 1.0 / (320 * pi3 * (1 - R * R) ** 2)
        print(f"I31 ball  R={R}: {val:.15e}  closed form {ref:.15e}  rel {val / ref - 1:.1e}")
    for R in (0.1, 0.2, 0.3):
        val = I31(1.0, R, R, "shell", "shell")
        ref = (3 + R * R) / (960 * pi3 * (1 - R * R) ** 3)
        print(f"I31 shell R={R}: {val:.15e}  closed form {ref:.15e}  rel {val / ref - 1:.1e}")
    for R in (0.05, 0.1, 0.2):
        val = I22(1.0, R, R)
        lead = (10.0 / 3.0) * 2 * (2 * self_energy(R)) / (FOUR_PI ** 2)
        print(f"I22 ball  R={R}: {val:.12e}  leading {lead:.12e}  diff/R {(val - lead) / R:.6e}")
    q, R = 1.0, 1.0
    for c in (1e-4, 1e-5, 1e-6):
        dU = (single_source_energy(q, R, c) - single_source_energy(q, R, 0.0)) / c
        print(f"(U(c)-U(0))/c = {dU:.10e}   -int D^4 = {-int_D4(q, R):.10e}")
    a = 1.0 / 137.035999
    for qW in (0.1, 1.0, 5.0):
        print(f"crossover q_W = {qW}: r_x = {mp.nstr(crossover(qW, a), 8)} / m")
