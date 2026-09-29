"""Adversarial checks of the production RPA classifier, not a test-local mock."""
from dataclasses import fields, replace
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
from rpa_kernel_conditions import RPAHypotheses, classify_rpa_kernel

H = RPAHypotheses(True, True, True, True, True, True)


@pytest.mark.parametrize("field", [f.name for f in fields(H)])
def test_each_missing_hypothesis_prevents_classification(field):
    result = classify_rpa_kernel((-2, -1), hypotheses=replace(H, **{field: False}))
    assert result["status"] == "UNRESOLVED"
    assert field in result["reason"]


def test_hypotheses_are_not_assumed_by_default():
    assert classify_rpa_kernel((-2, -1))["status"] == "UNRESOLVED"


@pytest.mark.parametrize("interval", [(0, 0), (0, "0.1"), ("-0.1", 0), (-1, 1)])
def test_touching_zero_requires_independent_exact_identity(interval):
    result = classify_rpa_kernel(interval, hypotheses=H, total_mass="finite")
    assert result["h3_status"] == result["pole_status"] == "UNRESOLVED"


def test_exact_atomic_critical_case_has_no_pole_but_fails_contact_free_h3():
    # rho=delta_1, g2=1 gives G(x)=1/x+1 exactly.
    result = classify_rpa_kernel((0, 0), hypotheses=H, exact_critical=True,
                                interval_kind="exact", total_mass="finite")
    assert result["status"] == "BOUNDARY_CONSTANT_FAILURE"
    assert result["pole_status"] == "ABSENT"
    assert result["h3_status"] == "FAILS_UNDER_ASSUMPTIONS"


def test_infinite_mass_boundary_is_distinct_from_finite_cutoff():
    # rho(s)=s^(-1/2) on [1,infinity): inverse moment=2, total mass=infinity.
    result = classify_rpa_kernel((0, 0), hypotheses=H, exact_critical=True,
                                interval_kind="exact", total_mass="infinite")
    assert result["h3_status"] == "HOLDS_UNDER_ASSUMPTIONS"


def test_unknown_critical_mass_keeps_h3_unresolved_but_excludes_pole():
    result = classify_rpa_kernel((0, 0), hypotheses=H, exact_critical=True,
                                interval_kind="exact")
    assert result["status"] == result["h3_status"] == "UNRESOLVED"
    assert result["pole_status"] == "ABSENT"


@pytest.mark.parametrize("interval,status", [
    (("-2e-1000", "-1e-1000"), "SPACELIKE_POLE_DETECTED"),
    (("1e-1000", "2e-1000"), "NO_SPACELIKE_POLE"),
])
def test_endpoint_conversion_does_not_underflow(interval, status):
    assert classify_rpa_kernel(interval, hypotheses=H)["status"] == status


@pytest.mark.parametrize("interval", [(1, -1), (float("nan"), 1),
                                     (0, float("inf")), (0,), (True, 1)])
def test_invalid_interval_is_not_an_acceptance(interval):
    with pytest.raises(ValueError):
        classify_rpa_kernel(interval, hypotheses=H)


@pytest.mark.parametrize("interval,kind", [((-1, 1), "exact"), ((0, 0), "estimated")])
def test_exact_critical_assertion_must_match_evidence(interval, kind):
    with pytest.raises(ValueError):
        classify_rpa_kernel(interval, hypotheses=H, exact_critical=True,
                            interval_kind=kind, total_mass="finite")


def test_inconsistent_z3_does_not_produce_a_positive_verdict():
    assert classify_rpa_kernel((1, 2), hypotheses=H)["status"] == "UNRESOLVED"


def test_classifier_does_not_change_global_precision_or_claim_certification():
    import mpmath as mp
    before = mp.mp.dps
    result = classify_rpa_kernel(("0.1", "0.2"), hypotheses=H)
    assert mp.mp.dps == before
    assert result["evidence"] == "CHECKED_CONDITIONAL"
    assert result["interval_kind"] == "estimated"
