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


# --- 9. the measure leaves the support of the input density -----------------
def test_resummation_creates_an_atom_above_the_cutoff(g2c):
    """Refutes the claim that sigma stays inside supp(rho_J).

    A hard cutoff leaves (L2, inf) off the cut, so W is real there and vanishes
    exactly once when Z3 > 0. The resulting atom has positive weight, so the
    Stieltjes positivity verdict survives -- only the SUPPORT claim was wrong.
    """
    atom = ga.spectral_atom(0.5 * g2c, L2)
    assert atom is not None, "Z3 > 0 must produce exactly one atom above L2"
    assert atom["status"] == "RESOLVED"
    assert atom["edge_distance"] > 0, "the atom sits OUTSIDE the input support"
    assert atom["s_atom"] > L2
    assert atom["weight"] > 0, "positive weight: the atom does not break positivity"

    # uniqueness: W is strictly increasing on (L2, inf)
    ts = [L2 * f for f in (1.01, 2.0, 10.0, 100.0)]
    vals = [ga._W_edge(t - L2, 0.5 * g2c, L2) for t in ts]
    assert all(b > a for a, b in zip(vals, vals[1:])), "W must increase on (L2, inf)"


def test_no_atom_when_Z3_is_negative(g2c):
    """Z3 < 0 keeps W negative on the whole of (L2, inf): no atom there."""
    assert ga.spectral_atom(1.5 * g2c, L2) is None
    assert ga.ghost_root(1.5 * g2c, L2) is not None, "but the spacelike ghost is present"


@pytest.mark.parametrize("Q2", [1.0, 10.0, 100.0, 1000.0])
def test_reconstruction_needs_the_atom(g2c, Q2):
    """THE test that would have caught the error: dropping the atom must fail.

    The continuum-only reconstruction agrees to ~1e-8, which reads as quadrature
    error and is not. Including the atom improves it by four orders of magnitude.
    """
    g2 = 0.5 * g2c
    target = ga.G(Q2, g2, L2) - g2 / Q2
    without = ga.reconstruct(Q2, g2, L2, include_atom=False)
    with_atom = ga.reconstruct(Q2, g2, L2, include_atom=True)

    err_without = abs(target - without) / abs(target)
    err_with = abs(target - with_atom) / abs(target)

    assert err_without > 1e-9, (
        "the incomplete reconstruction must be measurably wrong; if this passes "
        "the atom vanished and the analysis changed")
    assert err_with < 1e-10, "including the atom must close the decomposition"
    assert err_with < err_without / 100, (
        f"the atom must dominate the residual: {err_without:.2e} -> {err_with:.2e}")


# --- 10. global sum rules: local agreement cannot see a missing term --------
def test_sum_rules_hold_and_detect_a_dropped_atom(g2c):
    """Two identities from the z -> inf expansion of z*G(z) = g2 / W(z).

        (1)  g2 + int dsigma + sum w_a = g2 / Z3
        (2)  int s dsigma + sum w_a s_a = g2^2 mu / Z3^2,  mu = int rho_J ds

    These constrain the TOTAL weight, so a forgotten contribution cannot hide
    the way it hid behind agreement at four values of Q2.
    """
    g2 = 0.5 * g2c
    r = ga.sum_rules(g2, L2)
    assert r["regime"] == "subcritical"
    assert r["rule1"]["rel"] < 1e-7, r["rule1"]
    assert r["rule2"]["rel"] < 1e-6, r["rule2"]

    # dropping the atom must break rule (1) far outside its achieved accuracy
    rel_without = abs(r["rule1"]["lhs"] - r["atom_w"] - r["rule1"]["rhs"]) / r["rule1"]["rhs"]
    assert rel_without > 100 * r["rule1"]["rel"], (
        f"the sum rule must detect the missing atom: {rel_without:.2e} vs "
        f"{r['rule1']['rel']:.2e}")


@pytest.mark.parametrize("k", [0.3, 0.5, 0.8])
def test_sum_rules_across_subcritical_couplings(g2c, k):
    r = ga.sum_rules(k * g2c, L2)
    assert r["rule1"]["rel"] < 1e-6 and r["rule2"]["rel"] < 1e-5


@pytest.mark.parametrize("cutoff", [1e4, 1e6, 1e8])
def test_sum_rules_across_cutoffs(cutoff):
    g2 = 0.5 * ga.g2_critical(cutoff)
    r = ga.sum_rules(g2, cutoff)
    assert r["rule1"]["rel"] < 1e-6 and r["rule2"]["rel"] < 1e-5


# --- 11. the numerically hard regimes --------------------------------------
def test_small_coupling_atom_is_unresolved_never_reported_absent(g2c):
    """At small coupling the atom approaches the edge exponentially.

    d ~ (L2 - 4m^2) * exp(-Z3 / (g2 rho(L2))). The finder must degrade to an
    explicit unresolved status or raise -- never to None, which would assert
    absence against Proposition 4.
    """
    atom = ga.spectral_atom(0.1 * g2c, L2)
    assert atom is not None and atom["status"] == "RESOLVED_EDGE_UNRESOLVED", atom
    assert atom["weight"] > 0 and atom["edge_distance"] > 0

    with pytest.raises(RuntimeError, match="UNRESOLVED, not absence"):
        ga.spectral_atom(0.01 * g2c, L2)


def test_supercritical_refuses_reconstruction_and_sum_rules(g2c):
    g2 = 1.5 * g2c
    assert ga.spectral_atom(g2, L2) is None
    with pytest.raises(ValueError, match="supercritical"):
        ga.reconstruct(1.0, g2, L2)
    with pytest.raises(ValueError, match="subcritical regime only"):
        ga.sum_rules(g2, L2)


def test_critical_regime_refuses_because_the_constant_is_not_implemented(g2c):
    with pytest.raises(ValueError, match="critical"):
        ga.reconstruct(1.0, g2c, L2)
    info = ga.spectral_regime(g2c, L2)
    assert "additive_constant" in info["terms"]
    assert info["reconstruction_supported"] is False


# --- 12. the uniform counterexample, with exact position and residue --------
def test_uniform_counterexample_exact():
    """rho = 1 on [4,10], g2 = 1/(2 log(5/2)) gives Z3 = 1/2, an atom at s = 14
    with residue 10/21 -- all exactly, independent of the Dirac machinery."""
    import math
    g2 = 1.0 / (2.0 * math.log(2.5))
    Z3 = 1.0 - g2 * math.log(10.0 / 4.0)
    assert Z3 == pytest.approx(0.5, abs=1e-15)

    W = lambda t: Z3 + g2 * math.log((t - 10.0) / (t - 4.0))
    assert W(14.0) == pytest.approx(0.0, abs=1e-15)

    # residue of G = g2/(Q2 W(Q2)) at Q2 = -14, via dW/dQ2 at that point
    h = 1e-6
    dW_dQ2 = -(W(14.0 + h) - W(14.0 - h)) / (2 * h)
    assert g2 / ((-14.0) * dW_dQ2) == pytest.approx(10.0 / 21.0, rel=1e-8)
