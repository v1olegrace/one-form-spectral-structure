"""The static Wilson loop at fourth order in the probe charge (note E3).

Each test checks one statement of notes/E3_nonlinear_probe_EH.md. The two-centre
integrals are evaluated by quadrature in bipolar coordinates and compared with
closed forms obtained by a different route (an average of 1/u^5 over the second
source), with an expansion fitted in the source radius, or with each other. The
crossover uses the paper's own one-loop Dirac measure from spectral_models.py.
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


def test_linear_coefficient_is_isolated_by_oddness():
    gR2, c, r = 4 * math.pi * ALPHA, 1e3, 3.0
    for qW in (0.5, 1.0, 2.0):
        lin = (8 * nl.flux_E(r, qW, gR2, c) - nl.flux_E(r, 2 * qW, gR2, c)) / (6 * qW)
        assert lin == pytest.approx(1.0, rel=1e-12)


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
