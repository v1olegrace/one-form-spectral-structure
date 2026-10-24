"""The massless three-photon tail and the QED window of the pair threshold (note E4).

Route A computes the cut from the Euler-Heisenberg vertex in exact rational
arithmetic; route B maps the published QCD coefficient of Groote and Pivovarov
to QED. The amplitude is checked against the low-energy light-by-light cross
section, and the cut normalization against the one-loop Dirac density.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

import mpmath as mp
import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import three_photon_window as tpw  # noqa: E402

ALPHA = 1.0 / 137.035999


def test_eh_polynomial_is_the_euler_heisenberg_lagrangian():
    """kappa e^4 P = (2 alpha^2/45 m^4)[(E^2-B^2)^2 + 7 (E.B)^2]."""
    P, closed = tpw.eh_polynomial((Fr(1, 2), Fr(-2, 3), Fr(3, 5)), (Fr(2, 7), Fr(1, 3), Fr(-1, 4)))
    assert P == closed
    alpha, m = sp.symbols("alpha m", positive=True)
    kappa = 1 / (180 * (4 * sp.pi) ** 2 * m ** 4)
    assert sp.simplify(kappa * (4 * sp.pi * alpha) ** 2 * 8 - 2 * alpha ** 2 / (45 * m ** 4)) == 0


def test_amplitude_reproduces_low_energy_light_by_light():
    """Gamberg-Kalbfleisch-Milton, hep-ph/9906526, eqs. (42)-(43), spin-1/2 loop."""
    c = sp.Symbol("c", positive=True)
    dsig, sigma = tpw.light_by_light_cross_section()
    assert sp.simplify(dsig - sp.Rational(139, 32400) / sp.pi ** 2 * (3 + c ** 2) ** 2) == 0
    assert sp.simplify(sigma - sp.Rational(973, 10125) / sp.pi) == 0


@pytest.mark.parametrize("s", [5, 9, 40, 1000])
def test_cut_formula_reproduces_the_one_loop_dirac_density(s):
    """The prefactor e^2/(6 pi s) and dPhi_2 give (alpha/3 pi)(1 + 2/s) beta; d nu = rho ds."""
    got = tpw.pair_cut_density(s)
    expected = (1 + sp.Rational(2, s)) * sp.sqrt(1 - sp.Rational(4, s)) / (3 * sp.pi)
    assert sp.simplify(got - expected) == 0
    x = mp.sqrt(s)
    with mp.workdps(30):
        dnu = tpw.nl.dirac_dnu(ALPHA)(x)
        assert abs(dnu / (2 * x) / (mp.mpf(ALPHA) * float(expected)) - 1) < 1e-14


def test_three_body_phase_space_normalisation():
    dalitz, recursive = tpw.three_body_phase_space()
    assert sp.simplify(dalitz - recursive) == 0
    assert sp.simplify(dalitz - 1 / (256 * sp.pi ** 3)) == 0


def test_route_a_three_photon_density():
    """sum|Q|^2 = s^4 [(139/9) e2^2 - (148/9) e3]; int S = 17/45 > 0."""
    coeffs, residuals, integral = tpw.three_photon_polynomial()
    A, B, C, D = sp.symbols("A B C D")
    assert coeffs == {A: 0, B: 0, C: sp.Rational(-148, 9), D: sp.Rational(139, 9)}
    assert all(r == 0 for r in residuals) and len(residuals) == len(tpw.CONFIGS)
    assert integral == sp.Rational(17, 45)
    assert tpw.route_a_coefficient(integral) == sp.Rational(17, 11664000) > 0


def test_route_b_matches_and_the_naive_substitution_does_not():
    """The QCD coefficient with four legs reproduces route A; one leg is 16 times too small."""
    assert tpw.route_b_coefficient() == tpw.three_photon_rho_coefficient() == sp.Rational(17, 11664000)
    naive = sp.Rational(17, 243000) * sp.Rational(1, 3) / 256
    assert tpw.three_photon_rho_coefficient() / naive == 16
    # Portoles-Ruiz-Femenia eq. (8) is the same QCD result in their normalization: Pi = Pi_GP/(12 pi^2)
    assert sp.Rational(17, 243000) / (12 * sp.pi ** 2) == sp.Rational(17, 2916000) / sp.pi ** 2


def test_laplace_tail_of_the_three_photon_density():
    r, x, a = sp.symbols("r x alpha", positive=True)
    rho = tpw.three_photon_rho_coefficient() * (a / sp.pi) ** 4 * x ** 8      # s = x^2, m = 1
    phi = sp.integrate(sp.exp(-r * x) * rho * 2 * x, (x, 0, sp.oo))
    assert sp.simplify(phi - sp.Rational(238, 225) * (a / sp.pi) ** 4 / r ** 10) == 0
    with mp.workdps(30):
        assert abs(tpw.phi_three_photon(20, ALPHA) * 20 ** 10
                   / (mp.mpf(238) / 225 * (mp.mpf(ALPHA) / mp.pi) ** 4) - 1) < mp.mpf("1e-25")


E_FIELD, B_FIELD = (Fr(1, 2), Fr(-2, 3), Fr(3, 5)), (Fr(2, 7), Fr(1, 3), Fr(-1, 4))


def test_invariant_forms_split_the_euler_heisenberg_form():
    """Q(F, F, F, F) = ((E^2-B^2)^2, (E.B)^2), and 8 Q_X + 56 Q_Y is the one-loop form."""
    M = tpw.field_tensor(E_FIELD, B_FIELD)
    X = sum(e * e for e in E_FIELD) - sum(b * b for b in B_FIELD)
    Y = sum(e * b for e, b in zip(E_FIELD, B_FIELD))
    assert tpw.invariant_forms([M] * 4) == (X * X, Y * Y)
    legs = [tpw.wedge(k, e) for k, e in (((2, 1, 3, 1), (1, 2, 0, 3)), ((4, 1, 1, 2), (0, 3, 1, 1)),
                                         ((3, 2, 1, 2), (2, 1, 3, 0)), ((5, 1, 2, 3), (1, 1, 2, 4)))]
    qx, qy = tpw.invariant_forms(legs)
    assert (qx, qy) == (Fr(6094, 3), Fr(1867, 6))
    assert 8 * qx + 56 * qy == tpw.quartic_form(legs)


def test_two_loop_coefficients_from_the_self_dual_closed_form():
    """Ritus's 40/9 and 1315/252 give 25/4 for 4 c1 - c2, as the self-dual closed form does."""
    d1, d2 = tpw.TWO_LOOP_EH
    assert tpw.self_dual_two_loop_ratio() == Fr(25, 4) == (4 * d1 - 7 * d2) / (4 - 7)
    # the expansions used there, against direct evaluation at kappa = 1000
    with mp.workdps(60):
        kap = mp.mpf(1000)
        xi = lambda k: -k * (mp.digamma(k) - mp.log(k) + 1 / (2 * k))
        A2 = kap ** 2 * (3 * xi(kap) ** 2 - mp.diff(xi, kap))
        I1 = mp.quad(lambda t: (t ** 2 * mp.coth(t) ** 2 - 1 - 2 * t ** 2 / 3) / t ** 3 * mp.exp(-2 * kap * t),
                     [mp.mpf("1e-8"), 1 / kap, 10 / kap, 1, mp.inf])
        assert abs(A2 / (mp.mpf(5) / 48) - 1) < 1e-6
        assert abs(kap ** 2 * I1 / (mp.mpf(1) / 60) - 1) < 1e-6


def test_two_loop_light_by_light_factor():
    """sigma weights 2(a-b)^2 + (a+b)^2, a = c1/4 and b = c2/16 the (FF)^2 and (FF~)^2 coefficients.

    The factor 1 + (25555/2502) alpha/pi differs from the 1 + (186685/17514) alpha/pi
    that Dicus-Kao-Repko (hep-ph/9709415, note [10]) give from the same coefficients.
    """
    W, kappa = tpw.gamma_gamma_two_loop()
    c1, c2 = sp.symbols("c1 c2")
    a, b = c1 / 4, c2 / 16
    rate = sum(c * d * sp.Rational(str(W[i][j])) for i, c in enumerate((c1, c2)) for j, d in enumerate((c1, c2)))
    assert sp.expand(rate - sp.Rational(64, 9) * (2 * (a - b) ** 2 + (a + b) ** 2)) == 0
    assert rate.subs({c1: 1, c2: 7}) == sp.Rational(139, 36)          # 973 = 7 * 139 in sigma
    assert kappa == Fr(25555, 2502) == Fr(178885, 17514) != Fr(186685, 17514)
    # kappa = 2 d2 + w (d1 - d2), w/2 = 20/139 the c1 share of the rate; theirs has w = -40/139
    d1, d2 = tpw.TWO_LOOP_EH
    assert kappa == 2 * d2 + Fr(40, 139) * (d1 - d2)
    assert Fr(186685, 17514) == 2 * d2 - Fr(40, 139) * (d1 - d2)


def test_two_loop_coefficients_from_the_published_two_loop_amplitudes():
    """Abdul Hameed-Chaubey-Shao, arXiv:2604.00099, anc/Amp2L_LE.wl and anc/Amp1L_LE.wl. Leading
    two-loop over one-loop helicity amplitudes, with alpha_s C_F -> alpha for QED: all-plus goes as
    a - b, the mixed ones as a + b, so the ratios are Ritus's coefficients in those combinations."""
    d1, d2 = tpw.TWO_LOOP_EH
    two_pppp, one_pppp = Fr(5, 12), Fr(1, 15)       # (+) Nc Qf^4 a^2 (a/pi) (5/12) S2 ; (-)(-1/15) S2
    two_mmpp, one_mmpp = Fr(-391, 324), Fr(-11, 45)  # (+)(a/pi)(-391/324) s^2 ; (-)(11/45) s^2
    assert two_pppp / one_pppp == (4 * d1 - 7 * d2) / (4 - 7) == Fr(25, 4)
    assert two_mmpp / one_mmpp == (4 * d1 + 7 * d2) / 11 == Fr(1955, 396)


def test_two_loop_three_photon_factor():
    """rho weights 5(a-b)^2 + 3(a+b)^2; the leading coefficient gains 1 + (1555/153) alpha/pi."""
    I, kappa = tpw.three_photon_two_loop()
    assert I == [[Fr(1, 540), Fr(-1, 8640)], [Fr(-1, 8640), Fr(1, 8640)]]
    c1, c2 = sp.symbols("c1 c2")
    a, b = c1 / 4, c2 / 16
    rate = sum(c * d * sp.Rational(str(I[i][j])) for i, c in enumerate((c1, c2)) for j, d in enumerate((c1, c2)))
    assert sp.expand(rate - (5 * (a - b) ** 2 + 3 * (a + b) ** 2) / 270) == 0
    assert rate.subs({c1: 8, c2: 56}) == sp.Rational(17, 45)          # route A at one loop
    assert kappa == Fr(1555, 153)
    assert 0.0236 < float(kappa) * ALPHA / mp.pi < 0.0237


def test_qed_window_of_the_pair_threshold():
    """Leading terms: the pair dominates Phi for r < 22.60/m, and Gamma >= 2m only for r < 20.70/m."""
    r_x, r_g = tpw.window(ALPHA)
    assert float(r_x) == pytest.approx(22.6006910205, abs=1e-8)
    assert float(r_g) == pytest.approx(20.7024828448, abs=1e-8)
    for r in (5, 10, 15, 20):
        assert tpw.total_gamma(r, ALPHA) > 2
    for r, tail in ((25, 0.43166), (30, 0.33334), (40, 0.25)):
        g = tpw.total_gamma(r, ALPHA)
        assert g < 2 and g == pytest.approx(tail, abs=1e-5)        # -> 10/r
    # sensitivity: a factor 2 in K, an s^5 term, the Coulomb factor on the pair
    for kw, bound in ((dict(factor=2), 0.45), (dict(factor=0.5), 0.45), (dict(b=2), 0.08),
                      (dict(b=-2), 0.08), (dict(sommerfeld=True), 0.05)):
        shifted = tpw.window(ALPHA, **kw)
        assert abs(shifted[0] - r_x) < bound and abs(shifted[1] - r_g) < bound
