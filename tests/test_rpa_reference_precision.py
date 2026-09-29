"""Independent references for the RPA atom: exact anchor and multiprecision.

Why this file exists.  A sum-rule deviation measures the inconsistency of two
computed sides.  It does not say which component was wrong and it is not an
error bound, so fixing a tolerance to an observed deviation is a regression
test, not a precision claim.  Everything here compares the production float64
path against arithmetic that shares nothing with it.

What it established, and it was not what we expected: the two float64 weight
routes agree with each other to ~5e-9, but BOTH differ from the multiprecision
reference by ~2e-6.  They agreed because they share the located edge distance,
not because either is accurate to 5e-9.

The closed-form edge integral removed that shared error.  The primary weight
is now held to 1e-13 of the reference at k = 0.5 and 1e-12 at k = 0.1; the
finite-difference route is kept as a reported cross-check and must lose to it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_A = Path(__file__).resolve().parents[1] / "reports" / "h3_ghost_2026-09-29"
sys.path.insert(0, str(_A))

mp = pytest.importorskip("mpmath")
ga = pytest.importorskip("ghost_analysis")
ref = pytest.importorskip("reference_mp")

L2 = 1.0e6


# --- the exact anchor: everything closed form -------------------------------
def test_uniform_anchor_is_exact():
    """rho = 1 on [4,10] with g2 = 1/(2 log(5/2)): atom at s = 14, weight 10/21."""
    with mp.workdps(50):
        g2 = 1 / (2 * mp.log(mp.mpf(5) / 2))
        r = ref.uniform_exact(4, 10, g2, dps=50)
        assert abs(r["Z3"] - mp.mpf(1) / 2) < mp.mpf(10) ** -20
        assert abs(r["s_atom"] - 14) < mp.mpf(10) ** -20
        assert abs(r["weight"] - mp.mpf(10) / 21) < mp.mpf(10) ** -20
        # W really vanishes at the located root, not merely nearly
        assert abs(r["residual_W_at_root"]) < mp.mpf(10) ** -40


# --- the multiprecision reference settles under increasing precision --------
@pytest.mark.parametrize("k", [0.5, 0.1])
def test_reference_converges_with_precision(k):
    rows = ref.convergence_table(k, L2, dps_list=(30, 45))
    a, b = rows[0], rows[1]
    with mp.workdps(60):
        d_shift = abs(mp.re(a["log10_d"]) - mp.re(b["log10_d"]))
        w_rel = abs(mp.re(a["weight"]) - mp.re(b["weight"])) / abs(mp.re(b["weight"]))
        assert d_shift < mp.mpf(10) ** -12, f"log10(d) must settle, moved {d_shift}"
        assert w_rel < mp.mpf(10) ** -8, f"weight must settle, moved {w_rel}"


# --- the measured accuracy of the production path ---------------------------
@pytest.mark.parametrize("k,tol_d,tol_w", [(0.5, 1e-13, 1e-13), (0.1, 1e-14, 1e-12)])
def test_float64_path_accuracy_is_what_we_measured(k, tol_d, tol_w):
    """Pins the accuracy of the reported quantities against the reference.

    Measured after the edge integral moved to closed form: log10(d) to ~2e-15
    and the weight to ~3e-15 at k = 0.5; at k = 0.1 the weight floor is ~3e-14,
    because d = 3.3e-42 is reached through log10(d) = -41.5 and converting
    amplifies the error by |log10 d| ln 10 ~ 95. Tolerances carry margin over
    those values. Before the closed form both were ~2e-6.
    """
    g2 = k * ga.g2_critical(L2)
    got = ga.spectral_atom(g2, L2)
    want = ref.dirac_reference(k, L2, dps=50)
    with mp.workdps(60):
        ld_ref, w_ref = mp.re(want["log10_edge_distance"]), mp.re(want["weight"])
        rel_d = abs(mp.mpf(got["log10_edge_distance"]) - ld_ref) / abs(ld_ref)
        rel_w = abs(mp.mpf(got["weight"]) - w_ref) / abs(w_ref)
        assert rel_d < tol_d, f"log10(d) off by {rel_d}"
        assert rel_w < tol_w, f"reported weight off by {rel_w}"
        # The quadrature route for the weight, now fed the accurate root, lands
        # near 1e-11. The earlier 2e-6 came entirely from the root, not from
        # this integral. Checked loosely so an improvement here is not blocked.
        rel_q = abs(mp.mpf(got["weight_independent"]) - w_ref) / abs(w_ref)
        assert rel_q < 1e-9, f"quadrature weight route off by {rel_q}"


def test_primary_weight_is_accurate_and_crosschecks_are_reported():
    """The production weight now comes from the closed-form derivative.

    History, kept because it is the point: the earlier production path found
    the edge distance by QUADPACK on an integrand with a square-root branch
    point, and missed it by ~1.2e-6. Two weight routes then agreed with each
    other to 4.8e-9 and BOTH missed the multiprecision value by 2e-6, because
    they consumed the same located root. Their agreement measured consistency,
    not accuracy. test_quadpack_estimate_does_not_bound_the_integral_error keeps
    the raw form of that failure; this test no longer requires it of production.
    """
    g2 = 0.5 * ga.g2_critical(L2)
    got = ga.spectral_atom(g2, L2)
    assert got["weight_method"] == "analytic closed form"
    assert got["status"] == "RESOLVED" and got["quadrature_ok"]
    want = ref.dirac_reference(0.5, L2, dps=50)
    with mp.workdps(60):
        w_ref = mp.re(want["weight"])
        rel = abs(mp.mpf(got["weight"]) - w_ref) / abs(w_ref)
        assert rel < 1e-13, f"primary weight off by {rel}"
        # the cross-checks are still reported, and still weaker than the primary
        fd = abs(mp.mpf(got["weight_finite_difference"]) - w_ref) / abs(w_ref)
        assert fd < 1e-6, f"finite-difference cross-check off by {fd}"
        assert rel < fd, "the analytic route must beat the finite difference"


# --- the quadrature estimate does not bound the error -----------------------
def test_quadpack_estimate_does_not_bound_the_integral_error():
    """The same integral, same d, in two quadratures: QUADPACK is off by ~1e-7
    relative while requesting 1e-14, because of the endpoint branch point.
    It also warns of roundoff here; the warning is silenced because this test
    is about the returned estimate, which is the number callers used."""
    import warnings
    import numpy as np
    from scipy.integrate import IntegrationWarning, quad
    d, top = 5.2945, L2 - ga.S_THR
    hi = np.log(top / d)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        v64, est = quad(lambda u: ga._rho_scalar(L2 - d * np.exp(u)) * np.exp(u)
                        / (np.exp(u) + 1.0), -40.0, hi,
                        limit=2000, epsabs=1e-18, epsrel=1e-14)
    with mp.workdps(50):
        vmp = mp.quad(lambda u: ref._rho(mp.mpf(L2) - mp.mpf(d) * mp.e ** u)
                      * mp.e ** u / (mp.e ** u + 1),
                      [-40, mp.log(mp.mpf(top) / mp.mpf(d))])
        actual = abs(mp.mpf(v64) - vmp)
        assert actual > 100 * mp.mpf(est), (
            f"actual error {actual} vs reported estimate {est}: the point of this "
            "test is that the estimate is optimistic by orders of magnitude")
