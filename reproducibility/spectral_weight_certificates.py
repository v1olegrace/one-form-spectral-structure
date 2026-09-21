"""Exact dual certificates for a probability measure on [0, 1].

The target is W = P([z, 1]).  An optional floating-point LP proposes a
polynomial; the proof consists ONLY of rational Bernstein inequalities and
an exact objective evaluated over rational moment intervals.  Verification
needs the Python standard library.  Certificates are conditional on valid
input enclosures and existence of the stated positive probability measure.
They do not certify moment feasibility or a physical spectral hypothesis.

The lower polynomial is constrained to <= 0 on the CLOSED left interval
[0, z], including z. Continuity already forces this at z; the finite-degree
Bernstein inequalities, rather than endpoint closure, can be conservative.
The upper polynomial is constrained to >= 1 on the closed interval [z, 1].
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import comb, isfinite


SCHEMA = "spectral-weight-bernstein-v1"
_PROOF_KEYS = (
    "schema", "kind", "degree", "cutoff", "subdivisions", "partition",
    "coefficients", "moment_intervals", "raw_bound", "bound",
)


class CertificateVerificationError(ValueError):
    """The supplied record fails structural or exact mathematical checks."""


def _fraction(value):
    """Require exact rational inputs; do not silently convert binary floats."""
    if isinstance(value, bool) or not isinstance(value, (str, int, Fraction)):
        raise ValueError("Rational inputs must be Fraction, integer, or string")
    return Fraction(value)


def _intervals(values):
    result = []
    for item in values:
        if isinstance(item, dict):
            if set(item) != {"lower", "upper"}:
                raise ValueError("Interval records require exactly lower and upper")
            lo, hi = item["lower"], item["upper"]
        else:
            if len(item) != 2:
                raise ValueError("Each interval must have exactly two endpoints")
            lo, hi = item
        lo, hi = _fraction(lo), _fraction(hi)
        if lo > hi:
            raise ValueError("Reversed interval")
        result.append((lo, hi))
    return result


def normalize_sample_intervals(raw_samples):
    """Enclose Phi(r0+jh)/Phi(r0), propagating the COMMON denominator.

    All raw intervals must be nonnegative and the zeroth lower endpoint
    strictly positive.  b0 is exactly 1 because the numerator and denominator
    there are the same variable.  Ratios with j > 0 are [Lj/U0, Uj/L0].
    This operation alone does not assume or prove complete monotonicity.
    """
    samples = _intervals(raw_samples)
    if not samples or samples[0][0] <= 0:
        raise ValueError("Normalization requires a positive zeroth lower bound")
    if any(lo < 0 for lo, _ in samples):
        raise ValueError("Raw sample intervals must be nonnegative")
    lo0, hi0 = samples[0]
    return [(Fraction(1), Fraction(1))] + [
        (lo / hi0, hi / lo0) for lo, hi in samples[1:]
    ]


def _partition(cutoff, subdivisions):
    result = []
    for side, start, end, target in (
        ("left", Fraction(0), cutoff, "0"),
        ("right", cutoff, Fraction(1), "1"),
    ):
        for i in range(subdivisions):
            result.append({
                "side": side,
                "a": str(start + (end - start) * i / subdivisions),
                "b": str(start + (end - start) * (i + 1) / subdivisions),
                "target": target,
            })
    return result


def bernstein_coefficients(coefficients, a, b):
    """Convert power coefficients to Bernstein coefficients on [a,b].

    The transformation is exact, including degree elevation for trailing
    zero power coefficients.  Returned coefficients bound the polynomial on
    the entire closed interval, rather than on finitely sampled points.
    """
    coefficients = [_fraction(c) for c in coefficients]
    a, b = _fraction(a), _fraction(b)
    if not coefficients or not a < b:
        raise ValueError("Require a nonempty polynomial and a < b")
    degree = len(coefficients) - 1
    local_power = [
        sum((coefficients[j] * comb(j, ell) * a ** (j - ell)
             for j in range(ell, degree + 1)), Fraction(0)) * (b - a) ** ell
        for ell in range(degree + 1)
    ]
    return [
        sum((local_power[ell] * Fraction(comb(k, ell), comb(degree, ell))
             for ell in range(k + 1)), Fraction(0))
        for k in range(degree + 1)
    ]


def _matrix(degree, a, b):
    columns = []
    for j in range(degree + 1):
        unit = [Fraction(0)] * (degree + 1)
        unit[j] = Fraction(1)
        columns.append(bernstein_coefficients(unit, a, b))
    return list(zip(*columns))


def _objective(coefficients, intervals, kind):
    center = sum((c * (lo + hi) / 2 for c, (lo, hi)
                  in zip(coefficients, intervals)), Fraction(0))
    uncertainty = sum((abs(c) * (hi - lo) / 2 for c, (lo, hi)
                       in zip(coefficients, intervals)), Fraction(0))
    raw = center - uncertainty if kind == "lower" else center + uncertainty
    # Clip using W >= 0 or W <= 1 only; do not hide an inconsistent >1 lower
    # or <0 upper result by clipping BOTH ends.
    bound = max(Fraction(0), raw) if kind == "lower" else min(Fraction(1), raw)
    return raw, bound, center, uncertainty


def _checksum(record):
    payload = {key: record[key] for key in _PROOF_KEYS}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_inputs(intervals, cutoff, degree, subdivisions, kind):
    if kind not in ("lower", "upper"):
        raise ValueError("kind must be lower or upper")
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    if type(subdivisions) is not int or subdivisions < 1:
        raise ValueError("subdivisions must be a positive integer")
    if not 0 < cutoff < 1:
        raise ValueError("Require 0 < cutoff < 1")
    if len(intervals) != degree + 1:
        raise ValueError("Use exactly degree+1 moment intervals; slice explicitly")
    if intervals[0] != (Fraction(1), Fraction(1)):
        raise ValueError("b0 must be exactly [1,1]")


def verify_certificate(record):
    """Recompute a complete certificate with exact standard-library arithmetic.

    Return a JSON-serializable validation dictionary, or raise
    CertificateVerificationError.  The checksum detects accidental edits;
    it is not an authenticity signature.  Even with a freshly recomputed
    checksum, the complete Bernstein and objective checks must pass.
    """
    try:
        if not isinstance(record, dict) or record.get("schema") != SCHEMA:
            raise ValueError("Unrecognized certificate schema")
        intervals = _intervals(record["moment_intervals"])
        cutoff = _fraction(record["cutoff"])
        degree, subdivisions, kind = (
            record["degree"], record["subdivisions"], record["kind"]
        )
        _validate_inputs(intervals, cutoff, degree, subdivisions, kind)
        coefficients = [_fraction(c) for c in record["coefficients"]]
        if len(coefficients) != degree + 1:
            raise ValueError("Coefficient length does not match degree")
        partition = _partition(cutoff, subdivisions)
        if record["partition"] != partition:
            raise ValueError("Partition does not exactly cover the prescribed intervals")
        if record.get("payload_sha256") != _checksum(record):
            raise ValueError("Proof payload checksum mismatch")
        worst_slack = None
        for item in partition:
            target = _fraction(item["target"])
            betas = bernstein_coefficients(coefficients, item["a"], item["b"])
            for beta in betas:
                slack = target - beta if kind == "lower" else beta - target
                if slack < 0:
                    raise ValueError("A full-interval Bernstein inequality fails")
                worst_slack = slack if worst_slack is None else min(worst_slack, slack)
        raw, bound, center, uncertainty = _objective(coefficients, intervals, kind)
        if _fraction(record["raw_bound"]) != raw or _fraction(record["bound"]) != bound:
            raise ValueError("Reported bound does not equal the exact robust objective")
        result = {
            "valid": True,
            "arithmetic": "fractions.Fraction (exact rational)",
            "bound": str(bound),
            "raw_bound": str(raw),
            "center_objective": str(center),
            "uncertainty_penalty": str(uncertainty),
            "minimum_bernstein_slack": str(worst_slack),
            "intervals_checked": len(partition),
            "inequalities_checked": len(partition) * (degree + 1),
            "conditional_on_valid_moment_enclosures_and_positive_measure": True,
            "moment_feasibility_checked": False,
        }
        if "validation" in record and record["validation"] != result:
            raise ValueError("Stored validation differs from recomputed validation")
        return result
    except (ValueError, TypeError, KeyError, ZeroDivisionError, OverflowError) as exc:
        raise CertificateVerificationError(str(exc)) from exc


def propose_certificate(intervals, cutoff, degree, subdivisions=8, kind="lower"):
    """Propose, repair and exactly verify a polynomial spectral-weight bound.

    A failed or non-useful numerical proposal returns the valid trivial
    bound (0 lower, 1 upper).  The optimization is not a feasibility proof,
    and fixed-degree Bernstein constraints need not attain the moment optimum.
    """
    intervals = _intervals(intervals)
    cutoff = _fraction(cutoff)
    _validate_inputs(intervals, cutoff, degree, subdivisions, kind)
    partition = _partition(cutoff, subdivisions)
    coefficients = [Fraction(0)] * (degree + 1)
    if kind == "upper":
        coefficients[0] = Fraction(1)
    optimizer = {"status": "trivial_fallback", "proof_role": "none"}
    try:
        # These are optional for proposal and are NEVER imported by verifier.
        import numpy as np
        from scipy.optimize import linprog

        size = degree + 1
        centers = np.array([float((lo + hi) / 2) for lo, hi in intervals])
        radii = np.array([float((hi - lo) / 2) for lo, hi in intervals])
        direction = -1 if kind == "lower" else 1
        objective = np.concatenate([direction * centers, radii])
        rows, rhs = [], []
        for item in partition:
            sign = 1 if kind == "lower" else -1
            for row in _matrix(degree, _fraction(item["a"]), _fraction(item["b"])):
                rows.append([sign * float(x) for x in row] + [0.0] * size)
                rhs.append(sign * float(_fraction(item["target"])))
        for j in range(size):
            for sign in (1.0, -1.0):
                row = [0.0] * (2 * size)
                row[j], row[size + j] = sign, -1.0
                rows.append(row)
                rhs.append(0.0)
        proposal = linprog(
            objective, A_ub=np.asarray(rows), b_ub=np.asarray(rhs),
            bounds=[(None, None)] * size + [(0, None)] * size,
            method="highs",
        )
        optimizer["solver_status"] = int(proposal.status)
        optimizer["message"] = str(proposal.message)
        if proposal.success and all(isfinite(float(x)) for x in proposal.x[:size]):
            # Fixed decimal denominator keeps all subsequent exact sums compact.
            denominator = 10 ** 12
            candidate = [Fraction(round(Fraction(str(float(x))) * denominator), denominator)
                         for x in proposal.x[:size]]
            repair = Fraction(0)
            for item in partition:
                betas = bernstein_coefficients(candidate, item["a"], item["b"])
                target = _fraction(item["target"])
                violation = (max(betas) - target if kind == "lower"
                             else target - min(betas))
                repair = max(repair, violation)
            candidate[0] += -repair if kind == "lower" else repair
            candidate_bound = _objective(candidate, intervals, kind)[1]
            useful = candidate_bound > 0 if kind == "lower" else candidate_bound < 1
            if useful:
                coefficients = candidate
                optimizer["status"] = "rationalized_and_repaired"
            else:
                optimizer["status"] = "trivial_no_useful_proposal"
            optimizer["constant_repair_magnitude"] = str(repair)
            optimizer["rationalization_denominator"] = str(denominator)
    except (ImportError, ValueError, OverflowError, ArithmeticError) as exc:
        optimizer["message"] = f"Proposal unavailable: {type(exc).__name__}: {exc}"

    raw, bound, _, _ = _objective(coefficients, intervals, kind)
    record = {
        "schema": SCHEMA,
        "kind": kind,
        "degree": degree,
        "cutoff": str(cutoff),
        "subdivisions": subdivisions,
        "partition": partition,
        "coefficients": [str(c) for c in coefficients],
        "moment_intervals": [{"lower": str(lo), "upper": str(hi)} for lo, hi in intervals],
        "raw_bound": str(raw),
        "bound": str(bound),
        "optimizer": optimizer,
        "scope": "W=P([cutoff,1]) for a positive probability measure on [0,1]",
    }
    record["payload_sha256"] = _checksum(record)
    record["validation"] = verify_certificate(record)
    return record


def _main():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", type=Path, required=True,
                        help="JSON containing one certificate or a list of certificates")
    args = parser.parse_args()
    loaded = json.loads(args.verify.read_text(encoding="utf-8"))
    records = loaded if isinstance(loaded, list) else [loaded]
    for record in records:
        verify_certificate(record)
    print(json.dumps({"valid": True, "certificates_verified": len(records)}))


if __name__ == "__main__":
    _main()
