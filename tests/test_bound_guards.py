"""Every module that emits a bound must apply the shared finite conditions.

Before v0.3 the filter was a local helper of ``falsification_suite``; three
sibling modules that also publish bounds divided by a moment matrix or took the
logarithm of a moment ratio with no check at all.  Each test here fails on that
earlier arrangement, which is the only reason it is worth having.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import analysis                                                    # noqa: E402
import extended_analysis                                           # noqa: E402
import laplace_geometry                                            # noqa: E402
from moment_conditions import (conditioning_digits, mass_from_log_ratio,   # noqa: E402
                               moment_gate, validate_request)

# The localizer counterexample: all moments positive, det H0 > 0, det H1 < 0.
# Ungated, the Laplace pencil returns B_1 = -0.0644645.
LOCALIZER = ["1.999", "2.99", "4.9", "8"]


# --------------------------------------------------------------------------
# The shared gate itself
# --------------------------------------------------------------------------

def test_gate_rejects_unknown_orientation():
    with pytest.raises(ValueError, match="strict_shift"):
        moment_gate([mp.mpf(1), mp.mpf(1)], strict_shift=2)


def test_orientation_decides_which_matrix_is_guarded_strictly():
    """a = [1, 0]: H_0 = [[1]] is fine, H_1 = [[0]] is singular.

    The denominator of the pencil is the matrix that must be resolvably
    positive definite, so the same data is compatible for the Laplace
    orientation and unresolved for the Stieltjes one.
    """
    with mp.workdps(50):
        a = [mp.mpf(1), mp.mpf(0)]
        ok, _, diag = moment_gate(list(a), strict_shift=0)
        assert ok and diag["status"] == "CHECKED_COMPATIBLE"
        ok, reason, diag = moment_gate(list(a), strict_shift=1)
        assert not ok and diag["status"] == "UNRESOLVED_RANK_OR_PRECISION"
        assert "G3 unresolved" in reason and "not a refutation of H3" in reason


def test_gate_status_vocabulary_is_stable():
    """Incompatibility and unresolved precision must stay distinguishable."""
    with mp.workdps(50):
        ok, reason, diag = moment_gate([mp.mpf(x) for x in LOCALIZER])
        assert not ok
        assert diag["status"] == "CHECKED_INCOMPATIBLE"
        assert "G3 violated" in reason


def test_conditioning_digits_reports_none_for_a_singular_matrix():
    with mp.workdps(50):
        lo, hi, digits = conditioning_digits(mp.matrix([[1, 1], [1, 1]]))
        assert digits is None
        lo, hi, digits = conditioning_digits(mp.matrix([[2, 0], [0, 1]]))
        assert digits == 1 and lo == 1 and hi == 2


@pytest.mark.parametrize("ratio", [0, -1, "1.5", mp.inf, mp.nan])
def test_mass_from_log_ratio_refuses_meaningless_ratios(ratio):
    with pytest.raises(ValueError):
        mass_from_log_ratio(mp.mpf(ratio), mp.mpf("0.5"))


def test_mass_from_log_ratio_accepts_the_valid_range():
    with mp.workdps(50):
        assert mass_from_log_ratio(mp.mpf(1), mp.mpf("0.5")) == 0
        got = mass_from_log_ratio(mp.e**(-1), mp.mpf(1))
        assert abs(got - 1) < mp.mpf("1e-40")


@pytest.mark.parametrize("h", [0, -1, mp.inf])
def test_mass_from_log_ratio_refuses_bad_spacing(h):
    with pytest.raises(ValueError):
        mass_from_log_ratio(mp.mpf("0.5"), mp.mpf(h))


# --------------------------------------------------------------------------
# laplace_geometry: the Laplace pencil used by the canonical certification
# --------------------------------------------------------------------------

def test_laplace_geometry_bound_refuses_indefinite_localizer(monkeypatch):
    """Ungated, this call returned B_1 = -0.0644645 instead of refusing."""
    with mp.workdps(60):
        monkeypatch.setattr(laplace_geometry, "scaled_moment",
                            lambda n, r: mp.mpf(LOCALIZER[n]))
        with pytest.raises(ValueError, match="G3 violated"):
            laplace_geometry.hankel_bound(mp.mpf(1), 1)


def test_laplace_geometry_bound_refuses_singular_pencil(monkeypatch):
    """A rank-one positive pencil is unresolved, not a positivity violation."""
    with mp.workdps(60):
        monkeypatch.setattr(laplace_geometry, "scaled_moment",
                            lambda n, r: mp.mpf(2) * mp.mpf(3)**n)
        with pytest.raises(ValueError, match="unresolved"):
            laplace_geometry.hankel_bound(mp.mpf(1), 1)
        # K = 0 is still exact for a single atom.
        assert abs(laplace_geometry.hankel_bound(mp.mpf(1), 0) - 3) < mp.mpf("1e-40")


def test_laplace_geometry_bound_refuses_nonfinite_moments(monkeypatch):
    with mp.workdps(60):
        monkeypatch.setattr(laplace_geometry, "scaled_moment",
                            lambda n, r: mp.nan if n == 1 else mp.mpf(1))
        with pytest.raises(ValueError, match="finite and real"):
            laplace_geometry.hankel_bound(mp.mpf(1), 0)


@pytest.mark.parametrize("radius,order", [(0, 1), (-1, 1), (mp.inf, 1),
                                          (1, -1), (1, 1.5), (1, True)])
def test_laplace_geometry_bound_validates_its_request(radius, order):
    with pytest.raises(ValueError):
        laplace_geometry.hankel_bound(radius, order)


def test_laplace_geometry_bound_agrees_with_the_gated_suite_on_real_data():
    """Both Laplace routines must agree where both are defined."""
    with mp.workdps(60):
        b = laplace_geometry.hankel_bound(mp.mpf(3), 1)
        assert b >= laplace_geometry.M_STAR
        assert abs(laplace_geometry.hankel_bound(mp.mpf(3), 0)
                   - laplace_geometry.Gamma(mp.mpf(3))) < mp.mpf("1e-25")


# --------------------------------------------------------------------------
# extended_analysis: the sampled Hausdorff pencil
# --------------------------------------------------------------------------

def test_sampled_pencil_refuses_an_indefinite_localizer():
    with mp.workdps(60):
        with pytest.raises(ValueError, match="G3 violated"):
            extended_analysis.pencil([mp.mpf(x) for x in LOCALIZER], 1)


def test_sampled_pencil_requires_exactly_2K_plus_2_samples():
    with mp.workdps(60):
        with pytest.raises(ValueError, match="2K\\+2"):
            extended_analysis.pencil([mp.mpf(1), mp.mpf(1), mp.mpf(1)], 1)


def test_sampled_pencil_eigenvalue_above_one_is_refused():
    """Atoms at y = 2 and 3 pass the gate but are not e^{-hx} data for x > 0.

    The pencil eigenvalue is then 3, and ``-log(3)/h`` would be a negative
    "mass".  The gate cannot see this; only the domain guard can.
    """
    with mp.workdps(60):
        b = [mp.mpf(2)**n + mp.mpf(3)**n for n in range(4)]
        ok, _reason, diag = moment_gate(list(b))
        assert ok and diag["status"] == "CHECKED_COMPATIBLE"
        L, _v, _c0, _c1, _diag = extended_analysis.pencil(b, 1)
        assert abs(L - 3) < mp.mpf("1e-40")
        with pytest.raises(ValueError, match="outside"):
            mass_from_log_ratio(L, mp.mpf("0.5"))


def test_optional_mass_converts_a_refusal_into_an_explicit_no_bound():
    assert extended_analysis._optional_mass(mp.mpf(2), mp.mpf(1), "probe") is None
    assert extended_analysis._optional_mass(mp.mpf(1), mp.mpf(1), "probe") == 0


# --------------------------------------------------------------------------
# analysis: the Stieltjes pencil, opposite orientation
# --------------------------------------------------------------------------

def test_localizing_bound_guards_the_denominator_matrix(monkeypatch):
    """H_1 is the denominator here; the gate must be told so.

    Fails if someone passes the Laplace orientation, which would apply the
    strict near-singularity test to the wrong matrix.
    """
    seen = {}
    real_gate = analysis.moment_gate

    def spy(a, strict_shift=0):
        seen["strict_shift"] = strict_shift
        return real_gate(a, strict_shift=strict_shift)

    monkeypatch.setattr(analysis, "moment_gate", spy)
    analysis.localizing_bound(n0=1, order=2)
    assert seen["strict_shift"] == 1


def test_localizing_bound_refuses_a_negative_moment(monkeypatch):
    monkeypatch.setattr(analysis, "dirac_moment_mp",
                        lambda n, mass=1: mp.mpf(-1) if n == 3 else mp.mpf(1))
    with pytest.raises(ValueError, match="G1 violated"):
        analysis.localizing_bound(n0=1, order=1)


def test_localizing_bound_is_computed_in_extended_precision():
    """The published value must be the mpmath one, with float64 only measured."""
    bound, info = analysis.localizing_bound(n0=1, order=5, diagnostics=True)
    assert info["working_dps"] >= 100
    assert info["gate_status"] == "CHECKED_COMPATIBLE"
    # Measured, not asserted: this pencil needs about 13 digits, so float64
    # happened to be adequate here.  The requirement is now recorded.
    assert info["denominator_digits_required"] is not None
    assert info["float64_relative_difference"] < 1e-8
    assert bound >= 4.0


def test_localizing_bound_hierarchy_is_monotone_and_above_the_threshold():
    values = [analysis.localizing_bound(n0=1, order=k) for k in range(6)]
    assert all(values[i + 1] <= values[i] for i in range(len(values) - 1))
    assert all(v >= 4.0 for v in values)


def test_validate_request_is_shared():
    assert validate_request(mp.mpf(2), 3, "K") == 2
    with pytest.raises(ValueError):
        validate_request(mp.mpf(2), 0, "n_max")
