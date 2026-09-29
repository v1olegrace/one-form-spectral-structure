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
@pytest.mark.parametrize("k,tol_d,tol_w", [(0.5, 3e-6, 5e-6), (0.1, 1e-7, 5e-6)])
def test_float64_path_accuracy_is_what_we_measured(k, tol_d, tol_w):
    """Pins the ACTUAL accuracy against the reference, not the requested one.

    These tolerances come from comparison with multiprecision arithmetic.  They
    are far looser than the 1e-14 asked of the quadrature, and that gap is the
    finding: QUADPACK's error estimate does not bound the error here, because
    the integrand has a square-root branch point at the upper endpoint.
    """
    g2 = k * ga.g2_critical(L2)
    got = ga.spectral_atom(g2, L2)
    want = ref.dirac_reference(k, L2, dps=50)
    with mp.workdps(60):
        ld_ref, w_ref = mp.re(want["log10_edge_distance"]), mp.re(want["weight"])
        rel_d = abs(mp.mpf(got["log10_edge_distance"]) - ld_ref) / abs(ld_ref)
        rel_w = abs(mp.mpf(got["weight_independent"]) - w_ref) / abs(w_ref)
        assert rel_d < tol_d, f"log10(d) off by {rel_d}"
        assert rel_w < tol_w, f"weight off by {rel_w}"


def test_the_two_float64_routes_are_not_independent():
    """They agree far better than either is accurate.  Record why.

    Both consume the same located edge distance, so their agreement measures
    consistency of two derivative formulas, not accuracy of the result.
    """
    g2 = 0.5 * ga.g2_critical(L2)
    got = ga.spectral_atom(g2, L2)
    want = ref.dirac_reference(0.5, L2, dps=50)
    with mp.workdps(60):
        w_ref = mp.re(want["weight"])
        agreement = mp.mpf(got["weight_routes_agree_rel"])
        accuracy = abs(mp.mpf(got["weight_independent"]) - w_ref) / abs(w_ref)
        assert agreement < accuracy / 50, (
            f"mutual agreement {agreement} should be much tighter than the true "
            f"error {accuracy}; if this ever fails the routes became independent "
            "or the float64 path became accurate, and the note must be updated")


# --- the quadrature estimate does not bound the error -----------------------
def test_quadpack_estimate_does_not_bound_the_integral_error():
    """The same integral, same d, in two quadratures: QUADPACK is off by ~1e-7
    relative while requesting 1e-14, because of the endpoint branch point."""
    import numpy as np
    from scipy.integrate import quad
    d, top = 5.2945, L2 - ga.S_THR
    hi = np.log(top / d)
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
