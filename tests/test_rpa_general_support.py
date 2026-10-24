"""Exact refutations of overgeneral RPA atom counting on arbitrary support.

These mathematical witnesses test theorem domains, independently of the
Dirac-specific numerical implementation. They do not certify that code.
"""
from fractions import Fraction

import mpmath as mp
import sympy as sp


def test_endpoint_vanishing_density_has_no_upper_atom_despite_positive_z3():
    s = sp.Symbol("s", positive=True)
    inverse_moment = sp.integrate((10 - s) / s, (s, 4, 10))
    edge_integral = sp.integrate(sp.cancel((10 - s) / (10 - s)), (s, 4, 10))
    assert sp.simplify(inverse_moment - (10 * sp.log(sp.Rational(5, 2)) - 6)) == 0
    assert edge_integral == 6
    edge_limit = sp.simplify(1 - (inverse_moment + edge_integral) / 100)
    assert sp.simplify(edge_limit - (1 - sp.log(sp.Rational(5, 2)) / 10)) == 0
    # log(x) < x-1 for x>1 gives exact positive rational lower bounds.
    assert 1 - (10 * sp.Rational(3, 2) - 6) / 100 > 0
    assert 1 - sp.Rational(3, 2) / 10 > 0
    # Independently integrate on several exterior points. Together with the
    # proved positive derivative, the edge limit excludes every upper root.
    with mp.workdps(60):
        g2 = mp.mpf(1) / 100
        z3 = 1 - g2 * mp.quad(lambda x: (10 - x) / x, [4, 10])
        values = [z3 - g2 * mp.quad(lambda x: (10 - x) / (t - x), [4, 10])
                  for t in (mp.mpf("10.0001"), 11, 20, 100)]
        assert all(0 < a < b for a, b in zip(values, values[1:]))


def test_internal_gap_has_exact_positive_atom_at_criticality():
    s = sp.Symbol("s", real=True)
    inverse_moment = sp.integrate(1 / s, (s, 4, 5)) + sp.integrate(1 / s, (s, 9, 10))
    assert sp.simplify(sp.logcombine(inverse_moment, force=True) - sp.log(sp.Rational(25, 18))) == 0
    # The real logarithm ratios multiply to one, so W(-7) vanishes exactly.
    assert Fraction(2, 3) * Fraction(3, 2) == 1
    derivative_integral = sp.integrate(1 / (s - 7) ** 2, (s, 4, 5)) + sp.integrate(1 / (s - 7) ** 2, (s, 9, 10))
    assert derivative_integral == sp.Rational(1, 3)
    assert 1 / (7 * derivative_integral) == sp.Rational(3, 7)
    with mp.workdps(60):
        g2 = 1 / mp.log(mp.mpf(25) / 18)
        z3 = 1 - g2 * sum(mp.quad(lambda x: 1 / x, interval) for interval in ([4, 5], [9, 10]))
        w_at_7 = z3 + g2 * sum(mp.quad(lambda x: 1 / (x - 7), interval) for interval in ([4, 5], [9, 10]))
        assert abs(z3) < mp.mpf("1e-55")
        assert abs(w_at_7) < mp.mpf("1e-55")


def test_critical_limit_moves_the_upper_atom_into_the_constant():
    """At Z3 = 0, eta = 1_[4,10]: G = c*/x + 1/mu + int sigma/(x+s), mu = 6 (RPA note, (b))."""
    with mp.workdps(40):
        a, b = mp.mpf(4), mp.mpf(10)
        c_star = 1 / mp.log(b / a)
        G = lambda x: 1 / (x * mp.log((b + x) / (a + x)))       # c*/(x W*(x))
        sigma = lambda s: 1 / (s * (mp.log((b - s) / (s - a)) ** 2 + mp.pi ** 2))
        for x in (mp.mpf("0.01"), 1, 10, 1000):
            rest = mp.quad(lambda s: sigma(s) / (x + s), [a, 5, 7, 9, b])
            assert abs((G(x) - c_star / x - 1 / (b - a)) / rest - 1) < mp.mpf("1e-30")
        # W*(-t) = c* log((t-10)/(t-4)) < 0 for every t > 10: no upper atom is left.
        assert all(mp.log((t - b) / (t - a)) < 0 for t in (mp.mpf("10.001"), 100, 10 ** 6))
        # Below c* the upper atom t_c escapes to infinity, and weight/t_c -> 1/mu.
        gaps = []
        for eps in ("1e-3", "1e-5"):
            c = c_star * (1 - mp.mpf(eps))
            z3 = 1 - c * mp.log(b / a)
            W = lambda t: z3 + c * mp.log((t - b) / (t - a))     # W_c(-t) above the cut
            t = mp.findroot(W, b / z3)
            gaps.append(abs(c / (t * mp.diff(W, t)) / t - 1 / (b - a)))
        assert gaps[1] < gaps[0] < mp.mpf("1e-3")


def test_subthreshold_positivity_does_not_require_nonnegative_z3():
    with mp.workdps(50):
        g2 = mp.mpf(100)  # strongly supercritical for uniform [4,10]
        z3 = 1 - g2 * mp.log(mp.mpf(10) / 4)
        assert z3 < 0
        for t in (mp.mpf("0.1"), 1, mp.mpf("3.9")):
            direct = z3 + g2 * mp.quad(lambda s: 1 / (s - t), [4, 10])
            subtracted = 1 + g2 * t * mp.quad(lambda s: 1 / (s * (s - t)), [4, 10])
            assert direct > 1
            assert abs(direct - subtracted) < mp.mpf("1e-45")
