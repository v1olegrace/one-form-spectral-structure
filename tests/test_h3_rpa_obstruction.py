"""Refutation tests for the RPA spacelike-obstruction analysis.

Each test here fails on a plausible WRONG implementation, which is the only
reason it is worth having.  Scope: the RPA/Dyson model of
``reports/h3_ghost_2026-09-29/ghost_analysis.py``.  Nothing here is evidence
about H3 for the gauge-invariant nonperturbative kernel.

The analysis module lives under ``reports/`` rather than ``reproducibility/``
because it is a dated working artefact, not part of the canonical pipeline.
Moving it would be a restructuring decision, not a test decision.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_ANALYSIS = Path(__file__).resolve().parents[1] / "reports" / "h3_ghost_2026-09-29"
sys.path.insert(0, str(_ANALYSIS))

import ghost_analysis as ga  # Required source: absence must fail, never silently skip.

L2 = 1.0e6


@pytest.fixture(scope="module")
def g2c():
    return ga.g2_critical(L2)


# --- 1. subcritical: positive representation, no pole, decays to zero --------
def test_subcritical_has_positive_representation(g2c):
    g2 = 0.5 * g2c
    assert ga.Z3_of(g2, L2) > 0
    assert ga.ghost_root(g2, L2) is None
    for q in np.logspace(-3, 8, 25):
        assert ga.G(q, g2, L2) > 0
    # bounded by g2/(Q2 Z3) and therefore -> 0
    big = 1e10
    assert ga.G(big, g2, L2) <= g2 / (big * ga.Z3_of(g2, L2)) * (1 + 1e-9)
    assert ga.G(big, g2, L2) < 1e-8


# --- 2. critical, finite mass: NO pole, yet H3 fails via the constant -------
def test_critical_finite_mass_fails_H3_through_the_constant(g2c):
    """Z3 = 0 exactly.  No spacelike pole, but G -> 1/mu > 0, so H3 fails."""
    from scipy.integrate import quad
    g2 = g2c
    assert abs(ga.Z3_of(g2, L2)) < 1e-12
    assert ga.ghost_root(g2, L2) is None, "there must be no pole at Z3 = 0"

    mu, _ = quad(lambda t: ga._rho_scalar(ga.S_THR * np.exp(t)) * ga.S_THR * np.exp(t),
                 0.0, np.log(L2 / ga.S_THR), limit=400)
    assert np.isfinite(mu) and mu > 0, "finite cutoff must give finite total mass"

    limit = ga.G(1e14, g2, L2)
    assert limit == pytest.approx(1.0 / mu, rel=1e-3), \
        "at Z3 = 0 the kernel must tend to 1/mu, not to zero"
    assert limit > 0, "a strictly positive limit is exactly the H3 failure"


# --- 3. supercritical: pole present, residue negative -----------------------
def test_supercritical_pole_has_negative_residue(g2c):
    g2 = 1.5 * g2c
    xs = ga.ghost_root(g2, L2)
    assert xs is not None and xs > 0
    h = xs * 1e-6
    Wp = (ga.W(xs + h, g2, L2) - ga.W(xs - h, g2, L2)) / (2 * h)
    assert Wp < 0, "W must be strictly decreasing at the root"
    res_formula = g2 / (xs * Wp)
    res_numeric = (xs * (1 + 1e-7) - xs) * ga.G(xs * (1 + 1e-7), g2, L2)
    assert res_formula < 0, "residue must be negative"
    assert res_formula == pytest.approx(res_numeric, rel=1e-5)


# --- 4. the blind spot: continuum passes the gate although a pole exists ----
def test_continuum_gate_is_blind_to_the_pole(g2c):
    """Documents a scope limit of moment_conditions.moment_gate, not a bug."""
    import mpmath as mp
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
    from moment_conditions import moment_gate

    g2 = 1.5 * g2c
    assert ga.ghost_root(g2, L2) is not None, "this case must have a pole"
    # mp.mp.dps is GLOBAL mpmath state: leaving it lowered breaks the
    # high-precision assertions in test_measure_and_hierarchy.py, which runs
    # after this file alphabetically.  Restore it unconditionally.
    _dps = mp.mp.dps
    try:
        mp.mp.dps = 30
        a = [mp.mpf(v) for v in ga.continuum_moments(1.0, 3, g2, L2)]
        ok, _reason, diag = moment_gate(a, strict_shift=0)
    finally:
        mp.mp.dps = _dps
    assert ok and diag["status"] == "CHECKED_COMPATIBLE", (
        "if this ever starts FAILING, the blind spot was closed and the "
        "report's section 6 must be updated")


# --- 5. a fixed spacelike grid does not certify absence of poles ------------
def test_fixed_grid_misses_a_distant_pole(g2c):
    """Z3 slightly negative pushes the pole beyond any fixed grid."""
    g2 = 1.0005 * g2c
    z3 = ga.Z3_of(g2, L2)
    assert z3 < 0, "this case must be supercritical"
    xs = ga.ghost_root(g2, L2)
    assert xs is not None

    grid = np.logspace(-3, 6, 200)            # a plausible "thorough" grid
    assert xs > grid.max(), (
        f"pole at {xs:.3e} should sit beyond the grid max {grid.max():.3e}")
    assert all(ga.G(q, g2, L2) > 0 for q in grid), (
        "every grid point looks healthy — a finite mesh cannot certify "
        "global absence of poles; only the monotonicity argument can")


# --- 6. an interval for Z3 straddling zero must stay undecided --------------
def test_uncertain_Z3_is_unresolved_not_guessed():
    from rpa_kernel_conditions import RPAHypotheses, classify_rpa_kernel
    assumptions = RPAHypotheses(True, True, True, True, True, True)
    for interval, expected in [
        ((-1e-9, 1e-9), "UNRESOLVED"),
        ((-1e-3, -1e-6), "SPACELIKE_POLE_DETECTED"),
        ((1e-6, 1e-3), "NO_SPACELIKE_POLE"),
        ((-5e-16, 5e-16), "UNRESOLVED"),
    ]:
        assert classify_rpa_kernel(interval, hypotheses=assumptions)["status"] == expected


@pytest.mark.parametrize("k,status", [(0.5, "NO_SPACELIKE_POLE"),
                                    (1.0, "UNRESOLVED"),
                                    (1.5, "SPACELIKE_POLE_DETECTED")])
def test_actual_dirac_diagnostic_propagates_quadrature_uncertainty(g2c, k, status):
    diag = ga.kernel_diagnostic(k * g2c, L2)
    assert diag["status"] == status
    assert diag["interval_kind"] == "estimated"
    assert diag["evidence"] == "CHECKED_CONDITIONAL"


# --- 7. the path actually used to produce the published numbers -------------
@pytest.mark.parametrize("k,z3_expected,pole_expected", [
    (0.5, +0.5, None),
    (1.0, 0.0, None),
    (1.02, -0.02, 3.718e6),
    (1.5, -0.5, 1.773e4),
    (3.0, -2.0, 2.979e2),
])
def test_published_table_row_reproduces(g2c, k, z3_expected, pole_expected):
    """Exercises the same functions that produced the report's table 7-bis."""
    g2 = k * g2c
    z3 = ga.Z3_of(g2, L2)
    assert z3 == pytest.approx(z3_expected, abs=1e-9)
    # the identity the reviewer asked to be checked row by row
    assert z3 == pytest.approx(1.0 - g2 / g2c, abs=1e-12)
    root = ga.ghost_root(g2, L2)
    if pole_expected is None:
        assert root is None
    else:
        assert root == pytest.approx(pole_expected, rel=1e-3)


# --- 8. the two verdicts are SEPARATE and can disagree on the same input ----
def test_continuum_compatibility_and_kernel_obstruction_coexist(g2c):
    """The decisive separation test: same coupling, opposite conclusions.

    A compatible continuum is not evidence about the full kernel. If this ever
    starts failing, either the blind spot was closed or the two diagnostics
    were wrongly coupled; both require updating the report's section 6.
    """
    import mpmath as mp
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
    from moment_conditions import moment_gate

    g2 = 1.5 * g2c

    kernel = ga.kernel_diagnostic(g2, L2)
    assert kernel["status"] == "SPACELIKE_POLE_DETECTED"
    assert kernel["h3_status"] == "FAILS_UNDER_ASSUMPTIONS"

    _dps = mp.mp.dps
    try:
        mp.mp.dps = 30
        a = [mp.mpf(v) for v in ga.continuum_moments(1.0, 3, g2, L2)]
        ok, _reason, moments = moment_gate(a, strict_shift=0)
    finally:
        mp.mp.dps = _dps

    assert ok and moments["status"] == "CHECKED_COMPATIBLE"
    assert moments["scope"] != kernel["scope"], "the two scopes must stay distinct"
    assert "pole" not in moments["status"].lower(), \
        "moment_gate must not claim anything about poles"
