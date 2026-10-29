"""The static Wilson loop at fourth order in the probe charge (note E3).

Each test checks one statement of notes/E3_nonlinear_probe_EH.md. The two-centre
integrals are evaluated by quadrature in bipolar coordinates and compared with
closed forms obtained by a different route (an average of 1/u^5 over the second
source), with an expansion fitted in the source radius, or with each other. The
crossover is a formal benchmark using the point-source one-loop Dirac measure
from spectral_models.py. Sharp ball/shell boundaries benchmark the local
functional and do not validate the EFT derivative expansion there.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import nonlinear_probe_eh as nl  # noqa: E402

PI3 = math.pi ** 3
ALPHA = 1.0 / 137.035999


# --- the coefficient ----------------------------------------------------------
def test_eh_coefficient_in_alpha():
    e, alpha, m = sp.symbols("e alpha m", positive=True)
    c = e ** 4 / (360 * sp.pi ** 2 * m ** 4)            # Dunne, eq. (1.9)
    assert sp.simplify(c.subs(e, sp.sqrt(4 * sp.pi * alpha)) - 2 * alpha ** 2 / (45 * m ** 4)) == 0
    assert nl.eh_c(ALPHA) == pytest.approx(2 * ALPHA ** 2 / 45, rel=1e-14)


# --- the sign of the fixed-charge energy --------------------------------------
@pytest.mark.parametrize("profile", ["ball", "shell"])
def test_fixed_charge_energy_is_minus_c_int_E4(profile):
    """(U(c) - U(0))/c -> -int |E_0|^4, not the +3 int |E_0|^4 of T00 on the Coulomb field."""
    q, R = 1.0, 1.0
    ref = nl.int_D4(q, R, profile)
    slopes = [(nl.single_source_energy(q, R, c, profile)
               - nl.single_source_energy(q, R, 0.0, profile)) / c for c in (1e-4, 1e-5)]
    assert slopes[0] < 0 and slopes[1] < 0
    # first-order slope, with an O(c) remainder that shrinks tenfold
    assert abs(slopes[1] + ref) < abs(slopes[0] + ref) / 5
    assert slopes[1] == pytest.approx(-ref, rel=1e-5)
    assert abs(slopes[1] - 3 * ref) > 3 * ref


# --- the q1^3 q2 sector -------------------------------------------------------
def test_psi1_is_a_potential_for_the_cubed_field():
    u = sp.symbols("u", positive=True)
    g = 1 / (4 * sp.pi * u ** 2)
    psi = 1 / (5 * (4 * sp.pi) ** 3 * u ** 5)
    assert sp.simplify(-sp.diff(psi, u) - g ** 3) == 0
    assert sp.limit(psi, u, sp.oo) == 0


def test_ball_average_closed_form():
    """Mean of 1/u^5 over a uniform ball at distance r is 1/(r (r^2 - R^2)^2)."""
    r, a, t, R = sp.symbols("r a t R", positive=True)
    # sphere of radius a: (1/2) int_{-1}^{1} (r^2 + a^2 - 2 r a t)^(-5/2) dt
    anti = (r ** 2 + a ** 2 - 2 * r * a * t) ** sp.Rational(-3, 2) / (3 * r * a)
    assert sp.simplify(sp.diff(anti, t) - (r ** 2 + a ** 2 - 2 * r * a * t) ** sp.Rational(-5, 2)) == 0
    sphere = ((r - a) ** -3 - (r + a) ** -3) / (6 * r * a)
    for rv, Rv in [(1, sp.Rational(1, 5)), (3, 1), (sp.Rational(7, 2), sp.Rational(3, 2))]:
        sub = {r: rv}
        for av in (Rv / 7, Rv / 2, Rv):                  # a < r, so the roots are (r -+ a)^3
            at = {r: rv, a: av}
            assert sp.nsimplify((anti.subs(t, 1) - anti.subs(t, -1)).subs(at) / 2)                 == sp.nsimplify(sphere.subs(at))
        ball = sp.integrate((3 * a ** 2 / Rv ** 3 * sphere).subs(sub), (a, 0, Rv))
        assert sp.simplify(ball - 1 / (rv * (rv ** 2 - Rv ** 2) ** 2)) == 0


@pytest.mark.parametrize("R", [0.1, 0.25])
def test_I31_ball_and_shell_closed_forms(R):
    ball = nl.I31(1.0, R, R)
    shell = nl.I31(1.0, R, R, "shell", "shell")
    assert ball == pytest.approx(1 / (320 * PI3 * (1 - R * R) ** 2), rel=1e-11)
    assert shell == pytest.approx((3 + R * R) / (960 * PI3 * (1 - R * R) ** 3), rel=1e-11)


def test_I31_sees_only_the_exterior_field_of_source_one():
    """The sector is the mean of psi_1 over source 2, whatever source 1 looks like."""
    R2 = 0.2
    vals = [nl.I31(1.0, 0.1, R2, "ball", "ball"),
            nl.I31(1.0, 0.3, R2, "ball", "ball"),
            nl.I31(1.0, 0.3, R2, "shell", "ball")]
    assert max(vals) - min(vals) < 1e-12 * vals[0]
    # a point-like source 2 gives the universal value
    assert nl.I31(1.0, 0.3, 1e-3) == pytest.approx(1 / (320 * PI3), rel=1e-5)


# --- the q1^2 q2^2 sector -----------------------------------------------------
def _lead_ball(R):
    """(10/3)(int|d1|^2 + int|d2|^2)/(4 pi)^2 for two equal balls, from the self-energy."""
    return (10 / 3) * 2 * (2 * nl.self_energy(1.0, "ball") / R) / (4 * math.pi) ** 2


@pytest.fixture(scope="module")
def ball_rest():
    """g(R) = I22 - lead/R at r = 1, solved for a_-2/R^2 + a_0 + a_1 R + a_3 R^3."""
    radii = np.array([0.0125, 0.025, 0.05, 0.1])
    g = np.array([nl.I22(1.0, R, R) - _lead_ball(R) for R in radii])
    basis = np.vstack([radii ** -2, radii ** 0, radii, radii ** 3]).T
    return dict(zip(["Rm2", "R0", "R1", "R3"], np.linalg.solve(basis, g)))


def test_I22_has_no_r5_and_no_r3_term(ball_rest):
    """At r = 1, I22 = h(R): an r^-5 term is an R^0 term, an r^-3 term an R^-2 term."""
    universal = 1 / (320 * PI3)                          # the q1^3 q2 sector, for scale
    assert abs(ball_rest["R0"]) < 1e-4 * universal
    assert abs(ball_rest["Rm2"]) < 1e-12
    # what a nonzero R^0 term would do: (I22 - lead/R)/R grows like 1/R as R -> 0
    rest = [(nl.I22(1.0, R, R) - _lead_ball(R)) / R for R in (0.0125, 0.025)]
    assert abs(rest[0] - rest[1]) < 1e-3 * abs(rest[1])


def test_I22_leading_term_is_the_self_energy(ball_rest):
    """a_-1 = (10/3)(int|d1|^2 + int|d2|^2)/(4 pi)^2, i.e. 1/(8 pi^3) for two balls."""
    W = nl.self_energy(1.0, "ball")                      # unit radius
    assert W == pytest.approx(3 / (5 * 4 * math.pi), rel=1e-12)
    assert _lead_ball(1.0) == pytest.approx(1 / (8 * PI3), rel=1e-12)
    # with the lead subtracted the remainder is O(R): the lead carries all of 1/R
    assert ball_rest["R1"] == pytest.approx(-27 / (140 * PI3), rel=1e-4)


def test_I22_shell_leading_term():
    W = nl.self_energy(1.0, "shell")
    assert W == pytest.approx(1 / (8 * math.pi), rel=1e-12)
    R = 0.05
    lead = (10 / 3) * 2 * (2 * W / R) / (4 * math.pi) ** 2
    assert lead == pytest.approx(5 / (48 * PI3 * R), rel=1e-12)
    val = nl.I22(1.0, R, R, "shell", "shell")
    assert (val - lead) / R == pytest.approx(-9 / (40 * PI3), rel=2e-2)


def test_I22_integrand_is_positive():
    """2|d1|^2|d2|^2 + 4(d1.d2)^2 >= 0: the polarizability term attracts, whatever the signs."""
    rng = np.random.default_rng(0)
    for _ in range(200):
        d1, d2 = rng.normal(size=3), rng.normal(size=3)
        assert 2 * d1 @ d1 * (d2 @ d2) + 4 * (d1 @ d2) ** 2 >= 0


# --- totals and the QED numbers -----------------------------------------------
def test_totals_and_the_wichmann_kroll_tail():
    e, alpha, m, r, Z, q = sp.symbols("e alpha m r Z q", positive=True)
    c = e ** 4 / (360 * sp.pi ** 2 * m ** 4)
    I31 = 1 / (320 * sp.pi ** 3 * r ** 5)
    def universal(q1, q2):
        return -c * (4 * q1 ** 3 * q2 + 4 * q1 * q2 ** 3) * I31
    assert sp.simplify(universal(q, -q) - c * q ** 4 / (40 * sp.pi ** 3 * r ** 5)) == 0
    to_alpha = {e: sp.sqrt(4 * sp.pi * alpha)}
    pm_e = sp.simplify(universal(e, -e).subs(to_alpha))
    assert sp.simplify(pm_e - 4 * alpha ** 4 / (225 * sp.pi * m ** 4 * r ** 5)) == 0
    # (Ze, -e): the Z^3 part is the q1^3 q2 sector
    z3 = sp.simplify((-c * 4 * (Z * e) ** 3 * (-e) * I31).subs(to_alpha))
    # Frolov, arXiv:1111.2303v5, eq. (13): phi = (Qe/4 pi r)[1 - 2 Q^2 alpha^3/(225 pi m^4 r^4)];
    # the electron's energy is -e phi, so its correction is +e (Qe/4 pi r) 2 Q^2 alpha^3/(...)
    frolov = sp.simplify((e * (Z * e / (4 * sp.pi * r)) * 2 * Z ** 2 * alpha ** 3
                          / (225 * sp.pi * m ** 4 * r ** 4)).subs(to_alpha))
    assert sp.simplify(z3 - frolov) == 0
    assert sp.simplify(z3 - 2 * alpha * (Z * alpha) ** 3 / (225 * sp.pi * m ** 4 * r ** 5)) == 0


def test_two_ball_total_against_the_sectors():
    q, R, r, c = 1.0, 0.1, 1.0, 1.0
    total = nl.u4_interaction(r, q, -q, R, R, c)
    i31, i22 = nl.I31(r, R, R), nl.I22(r, R, R)
    assert total == pytest.approx(c * q ** 4 * (8 * i31 - i22), rel=1e-12)
    # the polarizability term dominates the universal one by about 5 r/R
    assert total < 0
    assert i22 / (8 * i31) == pytest.approx(5 * r / R, rel=0.05)


# --- the profile at finite probe charge ---------------------------------------
def test_profile_at_finite_charge():
    gR2, c, qW = 4 * math.pi * ALPHA, nl.eh_c(ALPHA), 1.0
    for r in (5.0, 10.0, 20.0):
        h = 1e-4 * r
        dq = (nl.flux_E(r + h, qW, gR2, c) - nl.flux_E(r - h, qW, gR2, c)) / (2 * h)
        delta = -(r / qW) * dq
        assert delta == pytest.approx(-c * gR2 * qW ** 2 / (math.pi ** 2 * r ** 4), rel=1e-6)
        assert delta / r ** 2 == pytest.approx(nl.phi_nl_qed(r, qW, ALPHA), rel=1e-6)
    x, rr = sp.symbols("x r", positive=True)
    assert sp.simplify(sp.integrate(x ** 5 / 120 * sp.exp(-rr * x), (x, 0, sp.oo)) - rr ** -6) == 0


def test_cubic_response_cancels_in_first_order_truncation():
    gR2, c, r = 4 * math.pi * ALPHA, 1e3, 3.0
    for qW in (0.5, 1.0, 2.0):
        lin = (8 * nl.flux_E(r, qW, gR2, c) - nl.flux_E(r, 2 * qW, gR2, c)) / (6 * qW)
        assert lin == pytest.approx(1.0, rel=1e-12)


def test_oddness_does_not_remove_the_quintic_response():
    """An independent odd polynomial leaves -4 a5 h^4 after cubic cancellation.

    The module's truncated flux has no quintic term, so testing only that
    implementation cannot establish an exact extraction for an odd response.
    """
    h, a1, a3, a5 = sp.symbols("h a1 a3 a5")
    response = a1 * h + a3 * h ** 3 + a5 * h ** 5
    estimate = sp.expand((8 * response - response.subs(h, 2 * h)) / (6 * h))
    assert sp.simplify(estimate - (a1 - 4 * a5 * h ** 4)) == 0
    assert sp.simplify(estimate - a1) != 0
    error = estimate - a1
    assert sp.simplify(error.subs(h, h / 2) - error / 16) == 0


def test_crossover_with_the_one_loop_profile():
    with mp.workdps(30):                                 # mpmath precision is global state
        rx = float(nl.crossover(1.0, ALPHA))
        assert 11.5 < rx < 11.65
        assert float(nl.phi_lin_qed(8.0, ALPHA)) + nl.phi_nl_qed(8.0, 1.0, ALPHA) > 0
        assert float(nl.phi_lin_qed(14.0, ALPHA)) + nl.phi_nl_qed(14.0, 1.0, ALPHA) < 0
        r_small, r_big = float(nl.crossover(0.1, ALPHA)), float(nl.crossover(5.0, ALPHA))
    assert r_big < rx < r_small


def test_one_loop_profile_matches_uehling_form():
    """Phi_lin = (2 alpha/3 pi) int_2^inf (1 + 2/x^2) sqrt(1 - 4/x^2) x e^{-r x} dx, m = 1."""
    with mp.workdps(30):
        r = mp.mpf(3)
        direct = 2 * mp.mpf(ALPHA) / (3 * mp.pi) * mp.quad(
            lambda x: (1 + 2 / x ** 2) * mp.sqrt(1 - 4 / x ** 2) * x * mp.e ** (-r * x),
            [2, 3, 6, mp.inf])
        assert nl.phi_lin_qed(r, ALPHA) == pytest.approx(direct, rel=1e-12)


def test_gaussian_source_is_normalized_and_its_field_obeys_gauss():
    from scipy import integrate
    R = 1.7
    assert integrate.quad(lambda u: 4 * math.pi * u ** 2 * nl.gaussian_density(u, R),
                          0, math.inf)[0] == pytest.approx(1, rel=1e-12)
    for x in (1e-5, 0.3, 1.2, 5):
        r, h = x * R, x * R * 1e-4
        enclosed = 4 * math.pi * r ** 2 * nl.g_gaussian(r, R)
        direct = integrate.quad(lambda u: 4 * math.pi * u ** 2 * nl.gaussian_density(u, R),
                                0, r, epsabs=1e-28)[0]
        assert enclosed == pytest.approx(direct, rel=1e-10)
        derivative = (nl.g_gaussian(r + h, R) - nl.g_gaussian(r - h, R)) / (2 * h)
        assert derivative + 2 * nl.g_gaussian(r, R) / r == pytest.approx(
            nl.gaussian_density(r, R), abs=1e-9, rel=1e-5)


@pytest.mark.parametrize("r,R,mass", [(0.2, 1.0, 0.3), (3.0, 1.0, 1.2), (2.0, 10.0, 2.0)])
def test_matched_gaussian_yukawa_against_radial_green_integral(r, R, mass):
    """Independent angular integration, no erfc expression in reference."""
    from scipy import integrate
    left = integrate.quad(lambda u: u * nl.gaussian_density(u, R) * math.sinh(mass * u),
                          0, r, epsabs=1e-15, epsrel=1e-11)[0]
    # exp(-mass*u) multiplies sinh(mass*r) here, so all integrands decay.
    right = integrate.quad(lambda u: u * nl.gaussian_density(u, R) * math.exp(-mass * u),
                           r, math.inf, epsabs=1e-15, epsrel=1e-11)[0]
    reference = (math.exp(-mass * r) * left + math.sinh(mass * r) * right) / (mass * r)
    assert nl.gaussian_yukawa(r, R, mass) == pytest.approx(reference, rel=1e-11)


def test_matched_gaussian_nonlinear_flux_and_negative_tail():
    q, R, c, mass, weight = 0.3, 10.0, nl.eh_c(ALPHA), 0.2, 1e-4
    for r in (4.0, 20.0, 70.0):
        h = r * 1e-4
        correction = lambda u: -16 * math.pi * c * q * q * u * u * nl.g_gaussian(u, R) ** 3
        numerical = -(correction(r + h) - correction(r - h)) / (2 * h * r)
        terms = nl.matched_gaussian_phi(r, q, R, c, mass, weight)
        assert terms["nonlinear"] == pytest.approx(numerical, rel=2e-6)
    far = nl.matched_gaussian_phi(500.0, q, R, c, mass, weight)
    assert far["total"] < 0
    assert far["nonlinear"] == pytest.approx(-c * q ** 2 / (math.pi ** 2 * 500 ** 6), rel=1e-12)


def test_local_legendre_remainder_bound_is_positive_and_controls_smooth_source():
    """Independent radial exact nonlinear solution lies in the analytic bounds."""
    q, R, c = 4.0, 1.0, 0.2
    exact = nl.single_source_energy(q, R, c, "gaussian")
    first = nl.single_source_energy(q, R, 0.0, "gaussian") - c * nl.int_D4(q, R, "gaussian")
    bound = nl.local_quartic_remainder_bound(q, R, c)
    assert 0 < exact - first < bound
    assert 0.6 < (exact - first) / bound < 1.0
    # Algebraic derivation of h'' at fixed D, not a fitted truncation estimate.
    E, cc = sp.symbols("E c", positive=True)
    dE_dc = -4 * E ** 3 / (1 + 12 * cc * E ** 2)
    assert sp.simplify(-4 * E ** 3 * dE_dc - 16 * E ** 6 / (1 + 12 * cc * E ** 2)) == 0


def test_e3_section10_quoted_numbers():
    """Every literal of E3 Section 10, recomputed (roadmap rule 1)."""
    c = nl.eh_c(ALPHA)
    q, R, mass, weight = 0.3, 10.0, 0.2, 1e-4
    assert nl.matched_gaussian_phi(100.0, q, R, c, mass, weight)["total"] == pytest.approx(2.2411164e-14, rel=1e-7)
    assert nl.matched_gaussian_phi(200.0, q, R, c, mass, weight)["total"] == pytest.approx(-2.9102525e-22, rel=1e-7)
    e = math.sqrt(4 * math.pi * ALPHA)
    dmax = q / (4 * math.pi * R ** 2)
    assert e * dmax == pytest.approx(7.22935e-5, rel=1e-5)
    assert 8 * c * dmax ** 2 == pytest.approx(1.07910e-12, rel=1e-5)
    stress = nl.single_source_energy(4.0, 1.0, 0.2, "gaussian") - (
        nl.single_source_energy(4.0, 1.0, 0.0, "gaussian") - 0.2 * nl.int_D4(4.0, 1.0, "gaussian"))
    assert stress == pytest.approx(2.2948903e-5, rel=1e-6)
    assert nl.local_quartic_remainder_bound(4.0, 1.0, 0.2) == pytest.approx(2.3763320e-5, rel=1e-6)


# --- Section 11: extended probes with the one-loop Dirac measure ---------------
def test_vacuum_polarization_against_feynman_parameter_integral():
    """The momentum routes use Pi_bar; check it, including the small-k series branch."""
    for k2 in ("1e-5", "0.0099", "0.0101", "0.5", "10", "1e4"):
        with mp.workdps(30):
            k2 = mp.mpf(k2)
            feynman = 2 * mp.mpf(ALPHA) / mp.pi * mp.quad(
                lambda t: t * (1 - t) * mp.log(1 + t * (1 - t) * k2), [0, 0.5, 1])
            assert abs(nl.vacuum_polarization(k2, ALPHA) / feynman - 1) < mp.mpf("1e-24")


def test_gaussian_laplacian_polynomials_and_uehling_moment():
    y = sp.Symbol("y", positive=True)
    lap = lambda f: sp.diff(f, y, 2) + 2 / y * sp.diff(f, y)
    f = sp.exp(-y ** 2)
    for k in (1, 2, 3):
        f = lap(f)
        assert sp.simplify(f / sp.exp(-y ** 2) - nl._GAUSS_LAPLACIAN[k](y)) == 0
    # int dnu/x^4 = (2 alpha/3 pi) int_2^inf (1 + 2/x^2) sqrt(1 - 4/x^2) x^-3 dx = alpha/(15 pi),
    # so 4 pi r lap(rho) int dnu/x^4 = (4 alpha/15) r lap(rho)
    x = sp.Symbol("x", positive=True)
    moment = sp.integrate((1 + 2 / x ** 2) * sp.sqrt(1 - 4 / x ** 2) / x ** 3, (x, 2, sp.oo))
    assert sp.simplify(moment - sp.Rational(1, 10)) == 0
    with mp.workdps(30):
        quad = mp.quad(lambda u: nl.dirac_dnu(ALPHA)(u) / u ** 4, [2, 3, mp.inf])
        assert abs(quad / (mp.mpf(ALPHA) / (15 * mp.pi)) - 1) < mp.mpf("1e-25")


@pytest.mark.parametrize("r", [5, 15, 30])
def test_gaussian_dirac_profile_two_independent_routes(r):
    """Spectral density + smeared Yukawa against Feynman-parameter Pi_bar + Fourier."""
    spectral = nl.gaussian_dirac_phi_lin(r, 10, ALPHA)
    momentum = nl.gaussian_dirac_phi_lin_momentum(r, 10, ALPHA)
    assert abs(spectral / momentum - 1) < 1e-14
    # the local Uehling term carries the profile to a few per cent
    assert abs(nl.gaussian_local_uehling_phi(r, 10, ALPHA) / spectral - 1) < 0.03


def _threshold_endpoint_gamma(r, R, alpha, dps=40):
    """Independent far-tail Gamma of the Gaussian probe, with no finite difference.

    For 2 <= x <= 3 and r/R - 3R/2 >= 10 the erfc factors of the smeared Yukawa
    kernel are saturated (relative error e^{-(r/R - 3R/2)^2}), so Phi is
    proportional to int e^{R^2 x^2/4 - r x} dnu there; the rest of the integral
    is smaller by e^{5R^2/4 - r} or less. Uses the one-loop density written out
    here, not the module's; its constant factor cancels in the ratio.
    """
    with mp.workdps(dps):
        r, R = mp.mpf(r), mp.mpf(R)
        w = lambda x: (mp.e ** (R * R * (x * x - 4) / 4 - r * (x - 2))
                       * x * (1 + 2 / x ** 2) * mp.sqrt(1 - 4 / x ** 2))
        nodes = [2, 2 + 1 / r, 2 + 4 / r, 2 + 16 / r, mp.mpf("2.5"), 3]
        return mp.quad(lambda x: x * w(x), nodes) / mp.quad(w, nodes)


def test_relative_quadrature_refuses_an_unresolved_integral():
    """mp.quad stops on an absolute error; at 1e-200 it returns 0.2762 for 5/18 silently."""
    with mp.workdps(30):
        tiny = mp.mpf("1e-200")
        kink = lambda x: tiny * abs(x - mp.mpf(1) / 3)
        with pytest.raises(ArithmeticError):
            nl.quad_relative(kink, [0, 1], tiny)
        value = nl.quad_relative(kink, [0, mp.mpf(1) / 3, 1], tiny)
        assert abs(value / tiny / (mp.mpf(5) / 18) - 1) < mp.mpf("1e-25")


def test_gaussian_probe_effective_mass_lies_below_the_threshold():
    """A non-compact probe breaks Gamma >= M_* = 2m at linear order (CHECKED, two routes)."""
    spectral = lambda u: nl.gaussian_dirac_phi_lin(u, 10, ALPHA, dps=40)
    momentum = lambda u: nl.gaussian_dirac_phi_lin_momentum(u, 10, ALPHA, dps=40)
    for r, quoted in ((30, 0.48395), (50, 0.93240)):
        g_spec = nl.log_slope(spectral, r, dps=40)
        assert abs(g_spec - nl.log_slope(momentum, r, dps=40)) < mp.mpf("1e-9")
        assert g_spec == pytest.approx(quoted, abs=5e-6)
        assert g_spec < 2
    lin = lambda u: nl.gaussian_dirac_phi_lin(u, 10, ALPHA)
    g100, g120 = nl.log_slope(lin, 100), nl.log_slope(lin, 120)
    assert g100 == pytest.approx(1.93672, abs=5e-6) and g100 < 2
    assert g120 == pytest.approx(2.12222, abs=5e-6) and g120 > g100   # not monotone
    g300 = nl.log_slope(lin, 300)                                      # Yukawa tail at r >> mR^2
    assert abs(g300 - _threshold_endpoint_gamma(300, 10, ALPHA)) < mp.mpf("1e-12")
    assert g300 == pytest.approx(2.00752, abs=5e-6)


def test_gaussian_dirac_matched_crossover():
    rx = nl.gaussian_dirac_crossover(0.3, 10, ALPHA, (50, 60))
    assert float(rx) == pytest.approx(55.9067264857, abs=1e-8)
    for r, sign in ((50, 1), (60, -1), (100, -1)):
        total = nl.gaussian_dirac_phi_lin(r, 10, ALPHA) + nl.gaussian_dirac_phi_nl(r, 0.3, 10, ALPHA)
        assert sign * total > 0
    c = nl.eh_c(ALPHA)
    assert float(nl.gaussian_dirac_phi_nl(100, 0.3, 10, ALPHA)) == pytest.approx(
        -c * 0.09 / (math.pi ** 2 * 100 ** 6), rel=1e-12)


def test_exterior_lemma_uniform_ball_against_fourier_route():
    """Outside a compact radial source the profile is int e^{-rx} F dnu, F >= 1."""
    exterior = nl.exterior_dirac_phi_lin(11, 10, ALPHA, dps=40)
    fourier = nl.ball_dirac_phi_lin_momentum(11, 10, ALPHA, dps=40)
    assert abs(exterior / fourier - 1) < mp.mpf("1e-30")
    with mp.workdps(30):
        for x in (0.01, 1, 2, 5, 40):
            F = nl.ball_exterior_factor(x, 10)
            z = mp.mpf(x) * 10
            assert 1 <= F <= mp.sinh(z) / z
            Fp = nl.polynomial2_exterior_factor(x, 10)
            assert 1 <= Fp <= mp.sinh(z) / z
            assert abs(Fp / nl.polynomial_exterior_factor(x, 10, 2) - 1) < mp.mpf("1e-20")


def test_exterior_factor_needs_a_non_negative_source():
    """F >= 1 fails for a signed source: charge 2 inside u < 1/2, -1 in the shell up to 1."""
    rho = lambda u: 12 / mp.pi if u < 0.5 else -6 / (7 * mp.pi)
    with mp.workdps(30):
        moment = lambda f: mp.quad(lambda u: 4 * mp.pi * u * u * rho(u) * f(u), [0, 0.5, 1])
        assert abs(moment(lambda u: 1) - 1) < mp.mpf("1e-25")
        F4 = moment(lambda u: mp.sinh(4 * u) / (4 * u))
        closed = (15 * nl.ball_exterior_factor(4, 0.5) - 8 * nl.ball_exterior_factor(4, 1)) / 7
        assert abs(F4 - closed) < mp.mpf("1e-25")
        assert F4 == pytest.approx(-1.2578597964, abs=1e-10)


def test_compact_probe_effective_mass_decreases_to_threshold():
    lin = lambda u: nl.exterior_dirac_phi_lin(u, 10, ALPHA)
    quoted = {11: 2.94681, 15: 2.25339, 30: 2.07112, 50: 2.03647}
    values = [nl.log_slope(lin, r) for r in quoted]
    for r, g in zip(quoted, values):
        assert abs(g - nl.exterior_dirac_gamma(r, 10, ALPHA)) < mp.mpf("1e-12")
        assert g == pytest.approx(quoted[r], abs=5e-6)
    assert all(2 < b < a for a, b in zip(values, values[1:]))


def test_compact_probe_matched_crossovers():
    ball = nl.exterior_dirac_crossover(0.3, 10, ALPHA, (18, 25))
    poly = nl.exterior_dirac_crossover(0.3, 10, ALPHA, (15, 25), nl.polynomial2_exterior_factor)
    assert float(ball) == pytest.approx(20.4822190112, abs=1e-8)
    assert float(poly) == pytest.approx(18.9502732027, abs=1e-8)
    with mp.workdps(30):
        point = float(nl.crossover(1.0, ALPHA))
    assert point < float(poly) < float(ball)


def test_two_sided_energy_bound_for_a_nonradial_lattice_source():
    """0 <= U_c - U_0 + c sum D0^4 <= 8 c^2 sum D0^6 for three unequal point charges."""
    import scipy.sparse.linalg as spla
    G, index = nl.lattice_gradient(41)
    rho = np.zeros(G.shape[1])
    rho[index[15, 20]], rho[index[25, 22]], rho[index[20, 12]] = 3.0, -3.0, 1.5
    base = nl.lattice_energy(G, rho, 0.0)
    D0 = base["D"]
    I4, I6 = np.sum(D0 ** 4), np.sum(D0 ** 6)
    ratios = []
    for c in (1e-4, 1e-3, 1e-2, 0.05, 0.2):
        got = nl.lattice_energy(G, rho, c)
        assert abs(got["primal"] - got["dual"]) < 1e-12
        assert got["residual"] < 1e-12
        rem = got["primal"] - (base["primal"] - c * I4)
        assert 0 < rem < 8 * c * c * I6
        ratios.append(rem / (8 * c * c * I6))
    assert ratios == pytest.approx([0.98679, 0.98091, 0.92647, 0.75136, 0.46049], abs=1e-5)
    # second-order coefficient: 8 sum D0^6 - (1/2)|P_perp(4 D0^3)|^2
    w = 4 * D0 ** 3
    transverse = w - G @ spla.spsolve((G.T @ G).tocsc(), G.T @ w)
    U2 = 8 * I6 - 0.5 * np.sum(transverse ** 2)
    rem = nl.lattice_energy(G, rho, 1e-4)["primal"] - (base["primal"] - 1e-4 * I4)
    assert rem / 1e-8 == pytest.approx(U2, rel=1e-3)
    assert np.sum(transverse ** 2) > 0.1     # the source is genuinely non-radial


def test_interaction_remainder_window():
    """The bound controls the O(c) interaction of two Gaussians only for r < r_V."""
    c, q, R = nl.eh_c(ALPHA), 0.3, 10.0
    ratio = lambda r: nl.interaction_remainder_bound(r, q, -q, R, R, c) / abs(
        nl.u4_interaction(r, q, -q, R, R, c, "gaussian", "gaussian"))
    assert ratio(50.0) == pytest.approx(2.1315e-12, rel=1e-4)
    assert ratio(1e4) == pytest.approx(2.3058e-3, rel=1e-4)
    assert ratio(4.5e4) < 1 < ratio(4.6e4)          # r_V = 4.5637e4 / m
    # the O(c) interaction is the polarizability law at large r
    W = nl.self_energy(R, "gaussian") * q * q
    A = 5 * c / (12 * math.pi ** 2) * 2 * W * q * q
    assert -nl.u4_interaction(1e4, q, -q, R, R, c, "gaussian", "gaussian") == pytest.approx(A / 1e16, rel=1e-3)
