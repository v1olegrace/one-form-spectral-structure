"""From <F F> to the static observables at linear order in the probe (note E2c).

Each test checks one step of notes/E2c_transport_linear_probe.md by a route
that does not share code with the step it checks. The sign of the whole chain
is anchored on free Proca and free Maxwell, which are positive theories.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import transport_linear_probe as tl  # noqa: E402

P = sp.symbols("p0:4", real=True)
DELTA = sp.eye(4)
EPS4 = sp.LeviCivita


def _T(a, b, c, e):
    p, d = P, DELTA
    return p[a]*p[c]*d[b, e] - p[b]*p[c]*d[a, e] - p[a]*p[e]*d[b, c] + p[b]*p[e]*d[a, c]


def _T_dual2(a, b, c, e):
    return sp.Rational(1, 2)*sum(EPS4(c, e, x, y)*_T(a, b, x, y) for x in range(4) for y in range(4))


def _T_dual1(a, b, c, e):
    return sp.Rational(1, 2)*sum(EPS4(a, b, x, y)*_T(x, y, c, e) for x in range(4) for y in range(4))


def _G(a, b, c, e):
    return DELTA[a, c]*DELTA[b, e] - DELTA[a, e]*DELTA[b, c]


def _E(a, b, c, e):
    return EPS4(a, b, c, e)


IDX = [(a, b, c, e) for a in range(4) for b in range(4) for c in range(4) for e in range(4)]


# --- the sign anchor -------------------------------------------------------------
def test_free_proca_and_maxwell_fix_the_euclidean_sign():
    """F = dA from a positive free theory gives S_E = +T_E a(p^2), a > 0.

    Proca has mu = delta_{m^2} with positive weight; Maxwell in any covariant
    gauge xi gives the same T-structure with 1/p^2, the gauge term dropping.
    """
    p2 = sum(x**2 for x in P)
    m, xi = sp.symbols("m xi", positive=True)
    proca = lambda a, b: (DELTA[a, b] + P[a]*P[b]/m**2)/(p2 + m**2)
    maxwell = lambda a, b: (DELTA[a, b] - xi*P[a]*P[b]/p2)/p2

    def FF(D, a, b, c, e):
        return P[a]*P[c]*D(b, e) - P[a]*P[e]*D(b, c) - P[b]*P[c]*D(a, e) + P[b]*P[e]*D(a, c)

    assert all(sp.simplify(FF(proca, *i) - _T(*i)/(p2 + m**2)) == 0 for i in IDX)
    assert all(sp.simplify(FF(maxwell, *i) - _T(*i)/p2) == 0 for i in IDX)


# --- which components a planar probe sees -------------------------------------------
def test_the_planar_loop_sees_only_T_and_the_local_G():
    """S_{01,01}: T -> p0^2 + p1^2; both duals of T and eps vanish identically."""
    assert sp.expand(_T(0, 1, 0, 1) - (P[0]**2 + P[1]**2)) == 0
    assert sp.simplify(_T_dual2(0, 1, 0, 1)) == 0
    assert sp.simplify(_T_dual1(0, 1, 0, 1)) == 0
    assert _E(0, 1, 0, 1) == 0
    assert _G(0, 1, 0, 1) == 1


def test_the_field_of_a_static_line_drops_the_helicity_term():
    """S_{0i,01} enters <E_i> through a half-plane. At p0 = 0 the T component is
    p1 p_i, so after the 1/(i p1) of the half-plane it is a gradient and does not
    depend on the half-plane's direction. The duals of T are proportional to p0,
    so the massless helicity term of note E2b drops without CPT. G gives
    delta_i1/(i p1): a field along the auxiliary surface."""
    for i in (1, 2, 3):
        assert sp.expand(_T(0, i, 0, 1).subs(P[0], 0) - P[1]*P[i]) == 0
        for dual in (_T_dual1, _T_dual2):
            expr = sp.expand(dual(0, i, 0, 1))
            assert sp.expand(expr.subs(P[0], 0)) == 0
            assert sp.simplify(expr/P[0]).has(P[0]) is False or sp.expand(expr) == 0
        assert _E(0, i, 0, 1) == 0
        assert _G(0, i, 0, 1) == (1 if i == 1 else 0)


def test_rectangle_stokes_identity_in_momentum_space():
    """|Sigma(p0, p1)|^2 (p0^2 + p1^2) equals the squared boundary integrals."""
    T, r = sp.symbols("T r", positive=True)
    q0, q1 = sp.symbols("q0 q1", real=True, nonzero=True)
    t, x = sp.symbols("t x", real=True)
    fT, fr = 2 - 2*sp.cos(q0*T), 2 - 2*sp.cos(q1*r)
    I0 = sp.integrate(sp.exp(sp.I*q0*t), (t, 0, T))
    I1 = sp.integrate(sp.exp(sp.I*q1*x), (x, 0, r))
    side0 = I0*(1 - sp.exp(sp.I*q1*r))
    side1 = I1*(sp.exp(sp.I*q0*T) - 1)
    line = sp.expand_complex(side0*sp.conjugate(side0) + side1*sp.conjugate(side1))
    surface = fT*fr/(q0**2*q1**2)*(q0**2 + q1**2)
    assert sp.simplify(sp.expand_trig(line - surface)) == 0


# --- the static slice ---------------------------------------------------------------
@pytest.mark.parametrize("s", [0.0, 0.25, 1.0, 9.0])
@pytest.mark.parametrize("r", [0.3, 1.0, 4.0])
def test_time_slice_of_the_4d_propagator_is_yukawa(s, r):
    got, _ = tl.yukawa_time_integral(s, r)
    assert abs(got/tl.yukawa(s, r) - 1) < 1e-12


def test_regulated_slice_tends_to_yukawa():
    """For r >> sqrt(eps) the regulated slice is exp(eps s) times the Yukawa, and
    the factor goes to one with eps."""
    r, s = 1.0, 4.0
    for eps in (1e-2, 1e-3, 1e-4):
        ratio = tl.a3_reg(r, [1.0], [s], eps)/tl.yukawa(s, r)
        assert abs(ratio/math.exp(eps*s) - 1) < 1e-9
    assert abs(tl.a3_reg(r, [1.0], [s], 1e-6)/tl.yukawa(s, r) - 1) < 1e-5


def test_regulated_kernel_routes_agree():
    eps = 0.01
    for r in (0.05, 0.5, 3.0):
        erf_form = math.erf(r/(2*math.sqrt(eps)))/(4*math.pi*r)
        assert abs(tl.a3_reg(r, [1.0], [0.0], eps)/erf_form - 1) < 1e-12


# --- Stokes, numerically: surface integral of S equals the line integral of a -------
MEASURES = [([1.0], [0.0]), ([0.7, 0.3], [0.0, 2.0])]


@pytest.mark.parametrize("w,s", MEASURES)
def test_surface_cumulant_equals_boundary_cumulant(w, s):
    eps, T, r = 0.05, 3.0, 1.2
    surf, _ = tl.surface_cumulant(T, r, lambda rho: tl.S0101_reg(rho, w, s, eps))
    line, _ = tl.boundary_cumulant(T, r, lambda rho: tl.a_reg(rho, w, s, eps))
    assert abs(surf/line - 1) < 1e-10


def test_stokes_is_structural_and_the_check_can_fail():
    """A Gaussian, not a propagator, obeys the same identity; a wrong operator
    in place of the in-plane Laplacian does not."""
    T, r, L = 3.0, 1.2, 0.8
    ag = lambda rho: math.exp(-rho*rho/L**2)
    Sg = lambda rho: -math.exp(-rho*rho/L**2)*(4*rho*rho/L**4 - 4/L**2)
    assert abs(tl.surface_cumulant(T, r, Sg)[0]/tl.boundary_cumulant(T, r, ag)[0] - 1) < 1e-10
    wrong = lambda rho: -math.exp(-rho*rho/L**2)*(4*rho*rho/L**4 - 2/L**2)   # a'' only
    assert abs(tl.surface_cumulant(T, r, wrong)[0]/tl.boundary_cumulant(T, r, ag)[0] - 1) > 0.1


# --- T -> infinity ----------------------------------------------------------------
def test_static_limit_and_its_measured_rate():
    """V_T(r) - V_inf(r) = C(r)/T + o(1/T), with
    C = -2 int_0^inf u [a(u) - a(sqrt(u^2+r^2))] du + 2 int_0^r (r - v) a(v) dv.

    The long-distance tails of a(u, 0) and a(u, r) cancel in the bracket, so in
    the Coulomb phase the rate is 1/T, not log T / T."""
    from scipy import integrate
    eps, r = 0.02, 1.0
    w, s = [0.6, 0.4], [0.0, 1.0]
    a = lambda rho: tl.a_reg(rho, w, s, eps)
    a3 = lambda x: tl.a3_reg(x, w, s, eps)
    v_inf = tl.potential_limit(r, a3)
    A = integrate.quad(lambda u: u*(a(u) - a(math.hypot(u, r))), 0, math.inf, epsrel=1e-12, limit=800)[0]
    B = integrate.quad(lambda v: (r - v)*a(v), 0, r, epsrel=1e-12)[0]
    C = -2*A + 2*B
    d40 = tl.potential_T(40.0, r, a) - v_inf
    d160 = tl.potential_T(160.0, r, a) - v_inf
    assert abs(160.0*d160/C - 1) < 1e-4
    assert abs(d40/d160 - 4.0) < 1e-2


def test_flux_profile_matches_theorem_A_kernel():
    """-4 pi r^2 d a3/dr = sum_k w_k (1 + sqrt(s_k) r) exp(-sqrt(s_k) r); its large-r
    limit is the s = 0 weight, the Coulomb residue."""
    w, s = [0.6, 0.4], [0.0, 1.0]
    for r in (0.2, 1.0, 3.0):
        assert abs(tl.flux_profile_numeric(r, w, s)/tl.flux_profile(r, w, s) - 1) < 1e-7
    assert abs(tl.flux_profile(60.0, w, s) - 0.6) < 1e-12


# --- what Bianchi on the T-product excludes ---------------------------------------
def test_bianchi_violating_local_term_gives_an_area_law():
    """A smeared G term c G h_eps (the D structure of the stochastic vacuum
    model) adds a potential linear in r: slope q^2 c/(8 pi eps) - sqrt(pi eps)/(4 pi^2 eps T)
    at finite T."""
    c, eps, T = 1.0, 0.01, 60.0
    h = lambda rho: c*tl.heat_kernel4(rho, eps)
    V = {r: tl.surface_cumulant(T, r, h)[0]/T for r in (1.5, 2.0, 3.0)}
    predicted = tl.area_term_slope(c, eps) - math.sqrt(math.pi*eps)/(4*math.pi**2*eps*T)
    for (r1, r2) in ((1.5, 2.0), (2.0, 3.0)):
        slope = (V[r2] - V[r1])/(r2 - r1)
        assert abs(slope/predicted - 1) < 1e-8
