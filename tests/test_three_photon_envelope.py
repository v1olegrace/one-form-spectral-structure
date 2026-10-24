"""The envelope of the truncated gamma* -> 3 gamma amplitude (note E4, Section 12).

Each constant of the bound is checked against the code's own quadratic form,
slot operators, numerators and traces, and the bound against the unexpanded
amplitude. The bound is analytic and evaluated in float64: CHECKED, not
certified.
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import three_photon_amplitude as tpa  # noqa: E402

ALPHA = 1.0 / 137.035999
# interior points, two collinear pairs (y3 = 0, y1 = 0) and a soft photon
DALITZ = [(1 / 3, 1 / 3, 1 / 3), (0.31, 0.27, 0.42), (0.5, 0.5, 0.0), (0.0, 0.4, 0.6), (0.98, 0.01, 0.01)]


def _orderings(s, y):
    p, pols = tpa.decay_kinematics(s, y)
    Ev_leg = [np.array([tpa.slash(e) for e in pl]) for pl in pols]
    for perm in itertools.permutations([1, 2, 3]):
        yield tpa._ordering_traces([p[0]] + [p[i] for i in perm], [Ev_leg[0]] + [Ev_leg[i] for i in perm])


def test_envelope_integral_is_the_dirichlet_moment():
    """n!(n+1)!/(2n+3)! = int over the simplex (volume 1/6) of x3^n (x0+x1)^n."""
    def moment(a):
        return Fraction(math.prod(math.factorial(e) for e in a), math.factorial(sum(a) + 3))
    for n in range(8):
        brute = sum(math.comb(n, i) * moment((i, n - i, 0, n)) for i in range(n + 1))
        assert Fraction(math.factorial(n) * math.factorial(n + 1), math.factorial(2 * n + 3)) == brute
        assert tpa.envelope_integral(n) == pytest.approx(float(brute), rel=1e-15)


@pytest.mark.parametrize("y", DALITZ)
def test_quadratic_form_and_its_moments(y):
    """0 <= R <= 1/4 at every node of every ordering, and the code's int R^n is below the bound."""
    x, w = tpa.simplex_rule(14)                  # exact for int R^n up to n = 12
    for K, T0, T2, T4 in _orderings(1.0, y):
        R = tpa._feynman_R(K, x)
        assert R.min() >= -1e-14 and R.max() <= 0.25 + 1e-14
        for n in range(8, 13):
            assert (w * R ** n).sum() <= tpa.envelope_integral(n) * (1 + 1e-12)


@pytest.mark.parametrize("y", DALITZ)
def test_slots_numerators_and_traces_obey_their_bounds(y):
    x, _ = tpa.simplex_rule(6)
    for K, T0, T2, T4 in _orderings(1.0, y):
        for j in range(4):
            for xi in x[::7]:
                v = np.array([float(i == j) - xi[i] for i in range(3)]) @ K
                assert np.linalg.norm(tpa.slash(v), 2) <= tpa.SLOT_NORM + 1e-12
        N0, N2 = tpa._numerators(T0, T2, x)
        for jd in range(5):
            assert np.abs(N0[..., jd]).max() <= tpa.N0_BOUND[jd]
        for jd in range(3):
            assert np.abs(N2[..., jd]).max() <= tpa.N2_BOUND[jd]
        assert np.abs(T4).max() <= tpa.T4_BOUND


@pytest.mark.parametrize("s", [0.75, 1.5])
def test_envelope_bounds_the_unexpanded_amplitude(s):
    """|A - A_K| <= E for every polarization, K = 8 and 12; a violation would be a derivation error.

    The envelope is about 4000-5600 times the actual remainder at s = 0.5-1.5 (R9 record).
    """
    rule = tpa.simplex_rule(10)
    for y in DALITZ[1:3]:
        p, pols = tpa.decay_kinematics(s, y)
        full = tpa.box(p, pols, rule, full=True)
        coeffs = tpa.box(p, pols, rule, kmax=12)
        for K in (8, 12):
            remainder = np.abs(full - coeffs[..., 1:K + 1].sum(-1)).max()
            assert 0 < remainder <= tpa.amplitude_envelope(s, K)


def test_moment_bounds_use_the_same_model_as_the_window():
    """model_M0 and model_D are the three-photon M0 and M1 - 2 M0 of profile_moments."""
    import mpmath as mp
    M, _ = tpa.amplitude_products(6, 5, 4)
    with mp.workdps(30):
        r = mp.mpf(21)
        t0 = tpa.profile_moments(r, ALPHA, 0)[1]
        t1 = tpa.profile_moments(r, ALPHA, 1)[1]
    b = tpa.truncation_moment_bounds(21, ALPHA, M, 6, 0.5)
    assert abs(b["model_M0"] / t0 - 1) < 1e-12
    assert abs(b["model_D"] / (t1 - 2 * t0) - 1) < 1e-12
    assert b["assumed_M0"] < b["model_M0"] and all(v > 0 for k, v in b.items() if k != "model_D")
    with pytest.raises(ValueError):
        tpa.truncation_moment_bounds(21, ALPHA, M, 6, 4)


def test_stored_products_reproduce_the_series_and_are_recomputed():
    M, K = tpa.products_matrix()
    assert K == 22 and np.allclose(M, M.T)
    orders = range(4, K + 1, 2)
    for n, c in enumerate(tpa.SERIES):
        diag = sum(M[a, b] for a in orders for b in orders if a + b == 8 + 2 * n)
        assert abs(diag / c - 1) < 1e-13
    fresh, worst = tpa.amplitude_products(6, 5, 4)          # exact rules for kmax = 6
    assert worst < 1e-13
    for a, b in ((4, 4), (4, 6), (6, 6)):
        assert abs(fresh[a, b] / M[a, b] - 1) < 1e-12


def test_truncation_bound_on_the_radii():
    """Note E4, Section 12.4: split at s1 = 1.5 m^2, point probe, two-loop leading term."""
    import mpmath as mp
    M, K = tpa.products_matrix()
    r_g, dDdr = mp.mpf("20.6363851158"), mp.mpf("6.28722e-24")
    b = tpa.truncation_moment_bounds(r_g, ALPHA, M, K, 1.5)
    assert b["bounded_D"] / dDdr < 2e-4 and b["assumed_D"] / dDdr < 1.3e-4
    assert b["assumed_M0"] / b["model_M0"] < 5e-4
    with mp.workdps(20):
        assert tpa.density_envelope(1.0, K, M) / tpa.density_truncated(1.0, M) < 0.01


def test_envelope_domain_and_monotonicity():
    with pytest.raises(ValueError):
        tpa.amplitude_envelope(4.0, 22)
    with pytest.raises(ValueError):
        tpa.amplitude_envelope(0.0, 22)
    for s in (0.3, 1.0, 1.5):
        assert tpa.amplitude_envelope(s, 22) < tpa.amplitude_envelope(s, 18) < tpa.amplitude_envelope(s, 14)
