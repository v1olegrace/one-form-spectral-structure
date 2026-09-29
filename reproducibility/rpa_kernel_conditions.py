"""Conditional RPA kernel diagnostics, independent of finite moment tests.

The caller supplies evidence for the model hypotheses and an interval for Z3.
This module neither proves those hypotheses nor constructs an error enclosure.
In particular, a QUADPACK error estimate is not an interval certificate.
No result here certifies H3 for a gauge-invariant Wilson-loop observable.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction


@dataclass(frozen=True)
class RPAHypotheses:
    """Explicit caller assertions; absent or non-True assertions fail closed."""

    nonnegative_measure: bool = False
    nonzero_measure: bool = False
    positive_support: bool = False
    finite_inverse_moment: bool = False
    positive_coupling: bool = False
    subtracted_dyson_representation: bool = False


def classify_rpa_kernel(z3_interval, *, hypotheses=None, total_mass="unknown",
                        exact_critical=False, interval_kind="estimated"):
    """Classify the contact-free RPA Stieltjes representation conditionally.

    Endpoints accept Fraction, Decimal, integer, float or rational/decimal text.
    Fraction conversion preserves their sign without binary64 underflow. A
    float is interpreted as its exact stored value, not its unknown true value.
    Invalid intervals raise ValueError. Missing hypotheses return UNRESOLVED.

    Every interval touching zero remains UNRESOLVED, including [0, 0], unless
    ``exact_critical=True`` explicitly asserts an independent exact identity
    Z3=0. That assertion requires the singleton [0, 0] and interval_kind='exact'.
    The critical case additionally needs finite/infinite total-mass evidence.
    A negative upper endpoint implies a unique pole by the monotonicity theorem;
    SPACELIKE_POLE_DETECTED does not mean its position has been computed.
    """
    if total_mass not in ("unknown", "finite", "infinite"):
        raise ValueError("total_mass must be unknown, finite or infinite")
    if interval_kind not in ("estimated", "enclosed", "exact"):
        raise ValueError("interval_kind must be estimated, enclosed or exact")
    if type(exact_critical) is not bool:
        raise ValueError("exact_critical must be a boolean")
    try:
        lo, hi = z3_interval
        if isinstance(lo, bool) or isinstance(hi, bool):
            raise ValueError("boolean endpoint")
        lo, hi = Fraction(lo), Fraction(hi)
    except (TypeError, ValueError, OverflowError, ZeroDivisionError) as exc:
        raise ValueError("Z3 requires two finite real endpoints") from exc
    if lo > hi:
        raise ValueError("Z3 interval endpoints are reversed")
    if exact_critical and (lo != 0 or hi != 0 or interval_kind != "exact"):
        raise ValueError("exact critical identity requires [0, 0] and exact evidence")
    if hypotheses is None:
        hypotheses = RPAHypotheses()
    if not isinstance(hypotheses, RPAHypotheses):
        raise ValueError("hypotheses must be RPAHypotheses")
    assertions = asdict(hypotheses)
    result = {
        "status": "UNRESOLVED", "h3_status": "UNRESOLVED",
        "pole_status": "UNRESOLVED", "pole_location": None,
        "scope": "conditional RPA contact-free Stieltjes kernel; not physical H3",
        "evidence": "CHECKED_CONDITIONAL", "interval_kind": interval_kind,
        "z3_interval": [str(lo), str(hi)], "hypotheses": assertions,
        "total_mass": total_mass, "exact_critical": exact_critical,
    }
    missing = [name for name, value in assertions.items() if value is not True]
    if missing:
        result["reason"] = "Unverified model hypotheses: " + ", ".join(missing)
    elif lo >= 1:
        result["reason"] = "Z3 >= 1 conflicts with positive coupling and nonzero positive measure"
    elif hi < 0:
        result.update(status="SPACELIKE_POLE_DETECTED",
                      h3_status="FAILS_UNDER_ASSUMPTIONS", pole_status="PRESENT",
                      reason="Negative Z3 implies a unique spacelike pole with negative residue")
    elif lo > 0:
        result.update(status="NO_SPACELIKE_POLE",
                      h3_status="HOLDS_UNDER_ASSUMPTIONS", pole_status="ABSENT",
                      reason="Positive Z3 gives a Stieltjes kernel decaying to zero")
    elif exact_critical:
        result["pole_status"] = "ABSENT"
        if total_mass == "finite":
            result.update(status="BOUNDARY_CONSTANT_FAILURE",
                          h3_status="FAILS_UNDER_ASSUMPTIONS",
                          reason="Exact Z3=0 and finite nonzero mass give a positive constant at infinity")
        elif total_mass == "infinite":
            result.update(status="NO_SPACELIKE_POLE",
                          h3_status="HOLDS_UNDER_ASSUMPTIONS",
                          reason="Exact Z3=0 and infinite mass give zero constant at infinity")
        else:
            result["reason"] = "Exact critical identity, but total mass is unknown"
    else:
        result["reason"] = "Z3 interval contains zero; an estimate cannot decide the boundary"
    return result
