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

Nothing here is an interval certificate: the quadratures are CHECKED, not
CERTIFIED.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy import integrate

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
    """|d| at distance u from the centre of a uniform ball of radius R, unit charge."""
    u = np.asarray(u, dtype=float)
    far = 1.0 / (FOUR_PI * np.maximum(u, 1e-300) ** 2)
    return _out(np.where(u < R, u / (FOUR_PI * R ** 3), far))


def g_shell(u, R):
    """|d| at distance u from the centre of a thin shell of radius R, unit charge."""
    u = np.asarray(u, dtype=float)
    far = 1.0 / (FOUR_PI * np.maximum(u, 1e-300) ** 2)
    return _out(np.where(u < R, 0.0, far))


PROFILES = {"ball": g_ball, "shell": g_shell}


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
    """Phi_lin(r) = int e^{-r x} dnu(x) for the one-loop Dirac measure, m = 1."""
    model = qed_model(alpha)
    return mp.e ** (-2 * mp.mpf(r)) * model.Phi_scaled(r)


def crossover(qW, alpha, guess=12.0):
    """r_x (units 1/m) where Phi_lin + Phi_NL changes sign."""
    model = qed_model(alpha)
    a3 = mp.mpf(alpha) ** 3

    def f(rr):
        lin = -2 * rr + mp.log(model.Phi_scaled(rr))
        nl = mp.log(8 * a3 * mp.mpf(qW) ** 2 / (45 * mp.pi * rr ** 6))
        return lin - nl

    return mp.findroot(f, mp.mpf(guess))


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
