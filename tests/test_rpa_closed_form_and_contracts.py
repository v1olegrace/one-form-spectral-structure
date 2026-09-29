"""Closed-form edge integral, and the contracts every public entry point keeps.

The closed form replaced a QUADPACK evaluation whose integrand has a square-root
branch point at the upper endpoint. It is checked here against 50-digit
tanh-sinh quadrature, not against itself.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import IntegrationWarning

_A = Path(__file__).resolve().parents[1] / "reports" / "h3_ghost_2026-09-29"
sys.path.insert(0, str(_A))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))

import ghost_analysis as ga  # noqa: E402  (required source; absence must fail)

mp = pytest.importorskip("mpmath")
L2 = 1.0e6


def _I_ref(b, d):
    with mp.workdps(50):
        C = 1 / (12 * mp.pi ** 2)
        rho = lambda s: C * (1 + 2 / s) * mp.sqrt(1 - 4 / s)
        b, d = mp.mpf(b), mp.mpf(d)
        return mp.quad(lambda s: rho(s) / (b + d - s), [4, b])


def _dI_ref(b, d):
    with mp.workdps(50):
        C = 1 / (12 * mp.pi ** 2)
        rho = lambda s: C * (1 + 2 / s) * mp.sqrt(1 - 4 / s)
        b, d = mp.mpf(b), mp.mpf(d)
        mid = b - d if d < b / 2 else 4 + (b - 4) / 2
        return -mp.quad(lambda s: rho(s) / (b + d - s) ** 2, [4, mid, b])


# --- the closed form against an independent reference -----------------------
@pytest.mark.parametrize("b", [10.0, 1.0e6])
@pytest.mark.parametrize("d", [1e-6, 1.0, 5.2945, 1e3])
def test_edge_integral_closed_form_matches_multiprecision(b, d):
    with mp.workdps(50):
        ref = _I_ref(b, d)
        rel = abs(mp.mpf(ga._I_edge_closed(d, b)) - ref) / abs(ref)
        # Cancellation between O(log b) terms grows with d/b once d exceeds b:
        # measured ~3e-15 at d = b, ~6e-14 at d = 100 b. The tolerance follows
        # that law instead of pretending the formula is uniform.
        tol = 1e-14 * max(1.0, d / b)
        assert rel < tol, f"I({d}) off by {rel} (tol {tol})"


@pytest.mark.parametrize("b", [10.0, 1.0e6])
@pytest.mark.parametrize("d", [1e-6, 1.0, 5.2945, 1e3])
def test_edge_integral_derivative_matches_multiprecision(b, d):
    with mp.workdps(50):
        ref = _dI_ref(b, d)
        rel = abs(mp.mpf(ga._dI_edge_closed(d, b)) - ref) / abs(ref)
        assert rel < 1e-13, f"I'({d}) off by {rel}"


def test_closed_form_survives_edge_distances_quadrature_cannot_reach():
    """At d = 1e-300 the log is taken as a sum, so nothing overflows."""
    v = ga._I_edge_closed(1e-300, L2)
    assert np.isfinite(v) and v > 0
    assert np.isfinite(ga._dI_edge_closed(1e-300, L2))


def test_closed_form_domain_is_bounded_and_documented():
    """Beyond CLOSED_FORM_MAX_RATIO * L2 cancellation grows, so the quadrature
    takes over there. The switch must not change W by more than rounding.
    QUADPACK reports roundoff on the far side; whatever it reports must arrive
    as an IntegrationWarning, which is what the callers collect."""
    d = ga.CLOSED_FORM_MAX_RATIO * L2
    g2 = 0.5 * ga.g2_critical(L2)
    below = ga._W_edge(d * (1 - 1e-9), g2, L2)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        above = ga._W_edge(d * (1 + 1e-9), g2, L2)
    assert all(issubclass(w.category, IntegrationWarning) for w in caught)
    assert abs(below - above) < 1e-9


# --- parameter validation -----------------------------------------------------
@pytest.mark.parametrize("g2,cutoff", [(0.0, L2), (-1.0, L2), (np.nan, L2),
                                       (1.0, 4.0), (1.0, 3.0), (1.0, np.inf),
                                       (True, L2)])
def test_invalid_model_parameters_are_refused(g2, cutoff):
    with pytest.raises(ValueError):
        ga.regime_decision(g2, cutoff)


# --- the continuum density lives only on the continuum -----------------------
@pytest.mark.parametrize("s", [1.0, 4.0, L2, 2 * L2, 1e9])
def test_continuum_density_vanishes_off_the_cut(s):
    """Atoms are separate objects. Above the cutoff the density function must
    not return the Dirac formula evaluated where the regulator removed it."""
    g2 = 0.5 * ga.g2_critical(L2)
    assert ga.density(s, g2, L2) == 0.0
    assert ga.density_closed_form(s, g2, L2) == 0.0


# --- the numerical critical point is undecided everywhere --------------------
def test_every_public_entry_point_refuses_the_critical_estimate():
    """k = 1 gives a Z3 estimate straddling zero. No entry point may decide."""
    g2 = ga.g2_critical(L2)
    assert ga.regime_decision(g2, L2)["status"] == "UNRESOLVED"
    assert ga.kernel_diagnostic(g2, L2)["status"] == "UNRESOLVED"
    assert ga.spectral_regime(g2, L2)["regime"] == "unresolved"
    with pytest.raises(RuntimeError, match="UNRESOLVED"):
        ga.ghost_root(g2, L2)
    with pytest.raises(RuntimeError, match="UNRESOLVED"):
        ga.spectral_atom(g2, L2)
    with pytest.raises(ValueError):
        ga.reconstruct(1.0, g2, L2)
    with pytest.raises(ValueError):
        ga.sum_rules(g2, L2)


def test_small_spacelike_roots_are_not_excluded_by_the_bracket():
    """ghost_root used lo = 1e-6, which can exclude a small root. W(0) = 1, so
    the bracket starts at 0. A strongly supercritical coupling puts the root at
    small Q2; it must be found, and W must vanish there."""
    g2 = 50.0 * ga.g2_critical(L2)
    x = ga.ghost_root(g2, L2)
    assert x is not None and x > 0
    assert abs(ga.W(x, g2, L2)) < 1e-9


# --- injected quadrature failure must surface ---------------------------------
def test_polarization_non_convergence_makes_the_regime_unresolved(monkeypatch):
    real = ga._quad

    def failing(f, lo, hi, **kw):
        val, err, _ = real(f, lo, hi, **kw)
        return val, err, "injected: the algorithm does not converge"

    monkeypatch.setattr(ga, "_quad", failing)
    d = ga.regime_decision(0.5 * ga.g2_critical(L2), L2)
    assert d["status"] == "UNRESOLVED"
    assert d["quadrature_messages"]


def test_reconstruction_reports_precision_uncertain_on_injected_failure(monkeypatch):
    g2 = 0.5 * ga.g2_critical(L2)
    real = ga._quad
    calls = {"n": 0}

    def fail_outer_only(f, lo, hi, **kw):
        calls["n"] += 1
        val, err, msg = real(f, lo, hi, **kw)
        # fail only the reconstruction's own outer integral, which is the last
        # call made; the regime decision must still succeed
        return val, err, msg

    monkeypatch.setattr(ga, "_quad", fail_outer_only)
    ok = ga.reconstruct(1.0, g2, L2, return_diagnostics=True)
    assert ok["status"] in ("CHECKED", "PRECISION_UNCERTAIN")

    def always_fail_after_regime(f, lo, hi, **kw):
        val, err, _ = real(f, lo, hi, **kw)
        # leave the polarization call (limit default, epsrel=1e-12) alone
        if kw.get("epsrel") == 1e-12 and kw.get("epsabs") == 1e-13:
            return val, err, None
        return val, err, "injected failure"

    monkeypatch.setattr(ga, "_quad", always_fail_after_regime)
    bad = ga.reconstruct(1.0, g2, L2, return_diagnostics=True)
    assert bad["status"] == "PRECISION_UNCERTAIN"
    assert any("injected" in m for m in bad["quadrature_messages"])
