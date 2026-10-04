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


def test_the_printed_boundary_display_equals_the_surface_cumulant():
    """Lemma 2 as printed in the note, implemented literally and compared with
    the surface integral, not with boundary_cumulant. The 1 October display had
    2 in front of each bilateral integral; that version is off by a factor 2."""
    from scipy import integrate
    T, r = 2.0, 0.7
    a = lambda rho: math.exp(-rho*rho)
    S = lambda rho: -math.exp(-rho*rho)*(4*rho*rho - 4)   # -(a'' + a'/rho)
    It = integrate.quad(lambda u: (T - abs(u))*(a(abs(u)) - a(math.hypot(u, r))), -T, T,
                        points=[0.0], epsrel=1e-13)[0]
    Is = integrate.quad(lambda v: (r - abs(v))*(a(abs(v)) - a(math.hypot(T, v))), -r, r,
                        points=[0.0], epsrel=1e-13)[0]
    surf = tl.surface_cumulant(T, r, S)[0]
    assert abs((It + Is)/surf - 1) < 1e-10
    assert abs(surf - 1.4317801911976835) < 1e-10
    assert abs((2*It + 2*Is)/surf - 2) < 1e-10


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
    """At fixed regulator, V_T(r) - V_inf(r) = q^2 C_eps(r)/T + o(1/T), with
    C_eps = -2 int_0^inf u [a(u) - a(sqrt(u^2+r^2))] du + 2 int_0^r (r - v) a(v) dv
    and a = a_eps in both integrals.

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
    # the rate carries the probe charge squared
    q2 = 2.5
    d160q = tl.potential_T(160.0, r, a, q2) - tl.potential_limit(r, a3, q2)
    assert abs(160.0*d160q/(q2*C) - 1) < 1e-4


def _C_eps(eps, r):
    from scipy import integrate
    a = lambda rho: tl.a_reg(rho, [1.0], [0.0], eps)
    A = integrate.quad(lambda u: u*(a(u) - a(math.hypot(u, r))), 0, math.inf,
                       epsrel=1e-12, limit=2000)[0]
    B = integrate.quad(lambda v: (r - v)*a(v), 0, r, epsrel=1e-12, limit=800)[0]
    return -2*A + 2*B


@pytest.mark.parametrize("r", [0.5, 1.0])
def test_the_rate_coefficient_has_no_limit_without_the_regulator(r):
    """Pure Coulomb: C_eps(r) = sqrt(pi) r/(4 pi^2 sqrt(eps))
    - [ln(r/(2 sqrt(eps))) + gamma/2 + 1/2]/pi^2 + o(1). The 1/T rate holds at
    fixed regulator only. The coefficient r/(2 pi^2 sqrt(eps)) proposed in the
    audit of 2 October is checked to fail."""
    g = 0.5772156649015329
    vals = {}
    for eps in (1e-2, 1e-3, 1e-4):
        C = _C_eps(eps, r)
        x = r/(2*math.sqrt(eps))
        pred = math.sqrt(math.pi)*r/(4*math.pi**2*math.sqrt(eps)) - (math.log(x) + g/2 + 0.5)/math.pi**2
        assert abs(C - pred) < 1e-4
        wrong = r/(2*math.pi**2*math.sqrt(eps)) - (math.log(x) + g/2 + 0.5)/math.pi**2
        assert abs(C - wrong) > 0.01
        vals[eps] = C
    assert vals[1e-2] < vals[1e-3] < vals[1e-4]
    if r == 1.0:
        for eps, ref in ((1e-2, 0.20599), (1e-3, 1.06014), (1e-4, 4.01340)):
            assert abs(vals[eps] - ref) < 5e-6


def test_flux_profile_matches_theorem_A_kernel():
    """-4 pi r^2 d a3/dr = sum_k w_k (1 + sqrt(s_k) r) exp(-sqrt(s_k) r); its large-r
    limit is the s = 0 weight, the Coulomb residue."""
    w, s = [0.6, 0.4], [0.0, 1.0]
    for r in (0.2, 1.0, 3.0):
        assert abs(tl.flux_profile_numeric(r, w, s)/tl.flux_profile(r, w, s) - 1) < 1e-7
    assert abs(tl.flux_profile(60.0, w, s) - 0.6) < 1e-12


# --- what Bianchi on the T-product excludes ---------------------------------------
def test_bianchi_violating_local_term_gives_an_area_law():
    """A smeared local G term c G h_eps adds a potential linear in r: slope
    q^2 c/(8 pi eps) - sqrt(pi eps)/(4 pi^2 eps T) at finite T. G is the tensor
    structure that multiplies D in the stochastic vacuum model; a local contact
    is not D itself (next test)."""
    c, eps, T = 1.0, 0.01, 60.0
    h = lambda rho: c*tl.heat_kernel4(rho, eps)
    V = {r: tl.surface_cumulant(T, r, h)[0]/T for r in (1.5, 2.0, 3.0)}
    predicted = tl.area_term_slope(c, eps) - math.sqrt(math.pi*eps)/(4*math.pi**2*eps*T)
    for (r1, r2) in ((1.5, 2.0), (2.0, 3.0)):
        slope = (V[r2] - V[r1])/(r2 - r1)
        assert abs(slope/predicted - 1) < 1e-8


def test_the_local_area_term_is_a_regulated_contact_not_a_tension():
    """Halving the regulator doubles the slope of the c G term: its coefficient
    diverges like 1/eps, so it is not a finite string tension."""
    c, T = 1.0, 60.0
    slopes = {}
    for eps in (0.01, 0.005):
        h = lambda rho: c*tl.heat_kernel4(rho, eps)
        slopes[eps] = (tl.surface_cumulant(T, 3.0, h)[0] - tl.surface_cumulant(T, 2.0, h)[0])/T
        predicted = tl.area_term_slope(c, eps) - math.sqrt(math.pi*eps)/(4*math.pi**2*eps*T)
        assert abs(slopes[eps]/predicted - 1) < 1e-8
    assert abs(slopes[0.005]/slopes[0.01] - 2) < 2e-3


# --- Section 11: from Wightman to (E) ----------------------------------------------

def _duals(metric):
    """T and its duals on the first and second pair, indices down, for a metric."""
    g = sp.diag(*metric)
    gi = g.inv()
    p = P

    def T(a, b, c, e):
        return p[a]*p[c]*g[b, e] - p[b]*p[c]*g[a, e] - p[a]*p[e]*g[b, c] + p[b]*p[e]*g[a, c]

    def d2(a, b, c, e):
        return sp.Rational(1, 2)*sum(EPS4(c, e, X, Y)*gi[X, X]*gi[Y, Y]*T(a, b, X, Y)
                                     for X in range(4) for Y in range(4))

    def d1(a, b, c, e):
        return sp.Rational(1, 2)*sum(EPS4(a, b, X, Y)*gi[X, X]*gi[Y, Y]*T(X, Y, c, e)
                                     for X in range(4) for Y in range(4))

    p2 = sp.expand(sum(gi[i, i]*p[i]**2 for i in range(4)))
    return T, d1, d2, p2


PAIRS = [(a, b) for a in range(4) for b in range(4) if a < b]


@pytest.mark.parametrize("metric", [(1, 1, 1, 1), (1, -1, -1, -1)], ids=["euclidean", "minkowski"])
def test_the_helicity_structure_is_pair_antisymmetric_and_one_dual_on_the_cone(metric):
    """dual1(ab,ce) = dual2(ce,ab) identically, and dual1 + dual2 = p^2 (...): so
    X = (dual1 - dual2)/2 is antisymmetric under pair exchange (i alpha' X is
    Hermitian) and equals either dual on the cone. T itself is pair-symmetric."""
    T, d1, d2, p2 = _duals(metric)
    for (a, b) in PAIRS:
        for (c, e) in PAIRS:
            assert sp.expand(T(a, b, c, e) - T(c, e, a, b)) == 0
            assert sp.expand(d1(a, b, c, e) - d2(c, e, a, b)) == 0
            s = sp.expand(d1(a, b, c, e) + d2(a, b, c, e))
            assert sp.expand(sp.div(s, p2, *P)[1]) == 0


X4 = sp.symbols("x0:4", real=True)
G_E = 1/(4*sp.pi**2*sum(x**2 for x in X4))


def _on_G(poly):
    """A polynomial in p, read as a differential operator on the massless G."""
    out = 0
    for monom, coeff in sp.Poly(sp.expand(poly), *P).terms():
        term = G_E
        for i, k in enumerate(monom):
            if k:
                term = sp.diff(term, X4[i], k)
        out += coeff*term
    return out


def test_a_nonlocal_helicity_term_breaks_bianchi_at_equal_times():
    """Without locality the helicity part of the time-ordered function is
    sign(tau) Y, Y = X(d) G. Y obeys Bianchi off the contact, but the jump adds
    2 delta(tau) eps_{k0mn} Y_{mn,rs}(0, x), which is not zero: (B_T) excludes
    the term."""
    _, d1, d2, _ = _duals((1, 1, 1, 1))
    Y = {}
    for (m, n) in [(a, b) for a in range(4) for b in range(4)]:
        for (r, s) in [(0, 1), (2, 3)]:
            Y[(m, n, r, s)] = _on_G(sp.Rational(1, 2)*(d1(m, n, r, s) - d2(m, n, r, s)))
    r2 = X4[1]**2 + X4[2]**2 + X4[3]**2
    jump = sum(EPS4(1, 0, m, n)*Y[(m, n, 0, 1)] for m in range(4) for n in range(4))
    jump = sp.simplify(jump.subs(X4[0], 0))
    assert sp.simplify(jump + 2*(X4[1]**2 - X4[2]**2 - X4[3]**2)/(sp.pi**2*r2**3)) == 0
    assert jump.subs({X4[1]: 1, X4[2]: 0, X4[3]: 0}) != 0
    for (r, s) in [(0, 1), (2, 3)]:
        for k in range(4):
            smooth = sum(EPS4(k, l, m, n)*sp.diff(Y[(m, n, r, s)], X4[l])
                         for l in range(4) for m in range(4) for n in range(4))
            assert sp.simplify(smooth) == 0


def test_a_sign_flip_in_tau_would_reach_the_static_line():
    """int sign(tau) d_tau g = -2 g(0) is not zero, while int d_tau g = 0: the
    p0 argument of Lemma 1 needs the O(4)-covariant form that (B_T) enforces."""
    from scipy import integrate
    x1, x2, x3 = 0.3, 0.4, 0.5
    rr = x1*x1 + x2*x2 + x3*x3
    g = lambda t: -2*x3/(4*math.pi**2*(t*t + rr)**2)          # d_3 G at (t, x)
    dg = lambda t: 8*t*x3/(4*math.pi**2*(t*t + rr)**3)        # d_t of it
    plain = integrate.quad(dg, -math.inf, math.inf)[0]
    signed = (integrate.quad(dg, 0, math.inf)[0] - integrate.quad(dg, -math.inf, 0)[0])
    assert abs(plain) < 1e-12
    assert abs(signed - (-2*g(0.0))) < 1e-12 and abs(signed) > 1e-2


def test_static_response_is_the_euclidean_integral_of_both_orderings():
    """Zero-frequency retarded response = int dtau of the time-ordered Euclidean
    function, with unequal spectral weights for the two orderings (no locality)."""
    E = [0.7, 1.3, 2.9]
    a = [0.5, 0.2, 0.9]
    b = [0.1, 0.8, 0.3]
    eta = 1e-9
    retarded = sum((1j*ai/(eta + 1j*Ei) - 1j*bi/(eta - 1j*Ei)) for ai, bi, Ei in zip(a, b, E))
    from scipy import integrate
    euclid = (integrate.quad(lambda t: sum(ai*math.exp(-Ei*t) for ai, Ei in zip(a, E)), 0, math.inf)[0]
              + integrate.quad(lambda t: sum(bi*math.exp(Ei*t) for bi, Ei in zip(b, E)), -math.inf, 0)[0])
    assert abs(retarded.imag) < 1e-6
    assert abs(retarded.real - euclid) < 1e-8
