"""Proof checks, not empirical sampling tests for polynomial inequalities."""

from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import builtins
import hashlib
import json
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
import spectral_weight_certificates as certificates


def two_atom_intervals(degree, eta=F(0)):
    moments = [F(1, 5) * F(4, 5) ** j + F(4, 5) * F(3, 10) ** j
               for j in range(degree + 1)]
    return [(F(1), F(1))] + [
        (b + (-1) ** j * eta / 2 - eta, b + (-1) ** j * eta / 2 + eta)
        for j, b in enumerate(moments[1:], 1)
    ]


def rehash(record):
    """An adversary can update a checksum; exact checks must still protect proof."""
    payload = {key: record[key] for key in certificates._PROOF_KEYS}
    record["payload_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    record.pop("validation", None)
    return record


@pytest.fixture(scope="module")
def atomic_pair():
    data = two_atom_intervals(6, F(1, 10 ** 6))
    return [certificates.propose_certificate(data, F(3, 5), 6, kind=kind)
            for kind in ("lower", "upper")]


def test_atomic_measure_is_enclosed_and_recovered_usefully(atomic_pair):
    lower, upper = atomic_pair
    assert F(19, 100) < F(lower["bound"]) <= F(1, 5)
    assert F(1, 5) <= F(upper["bound"]) < F(21, 100)
    for record in atomic_pair:
        assert certificates.verify_certificate(record)["valid"]
        assert json.loads(json.dumps(record)) == record


def test_uniform_continuum_is_enclosed():
    data = [(F(1, j + 1), F(1, j + 1)) for j in range(7)]
    lower = certificates.propose_certificate(data, F(3, 5), 6)
    upper = certificates.propose_certificate(data, F(3, 5), 6, kind="upper")
    assert 0 < F(lower["bound"]) <= F(2, 5)
    assert F(2, 5) <= F(upper["bound"]) < 1


@pytest.mark.parametrize("kind", ["lower", "upper"])
def test_atom_at_cutoff_is_safe(kind):
    z = F(3, 5)
    data = [(z ** j, z ** j) for j in range(5)]
    result = certificates.propose_certificate(data, z, 4, kind=kind)
    assert certificates.verify_certificate(result)["valid"]
    if kind == "lower":
        # Continuity plus the closed left constraint gives q(z)<=0.
        assert F(result["bound"]) == 0
    else:
        assert F(result["bound"]) >= 1


@pytest.mark.parametrize("kind,expected", [("lower", "0"), ("upper", "1")])
def test_large_errors_return_trivial_bounds(kind, expected):
    data = [(F(1), F(1))] + [(F(-1), F(2))] * 6
    result = certificates.propose_certificate(data, F(3, 5), 6, kind=kind)
    assert result["bound"] == expected
    assert result["optimizer"]["status"] == "trivial_no_useful_proposal"


def test_shared_normalization_uncertainty_is_propagated():
    data = certificates.normalize_sample_intervals([(F(9), F(11)), (F(4), F(6))])
    assert data == [(F(1), F(1)), (F(4, 11), F(2, 3))]
    # Dividing by a central denominator would incorrectly exclude the extremes.
    assert data[1][0] < F(4, 10) and data[1][1] > F(6, 10)
    with pytest.raises(ValueError, match="positive"):
        certificates.normalize_sample_intervals([(F(0), F(1))])


def test_bernstein_conversion_known_quadratic():
    # y^2 on [1/4, 3/4]: [a^2, ab, b^2] in degree two Bernstein basis.
    assert certificates.bernstein_coefficients([0, 0, 1], F(1, 4), F(3, 4)) == [
        F(1, 16), F(3, 16), F(9, 16)
    ]


@pytest.mark.parametrize("field", ["bound", "coefficients", "partition", "moment_intervals"])
def test_tampering_is_rejected(atomic_pair, field):
    record = deepcopy(atomic_pair[0])
    if field == "bound":
        record[field] = "1"
    elif field == "coefficients":
        record[field][0] = str(F(record[field][0]) + 1)
    elif field == "partition":
        record[field].pop()
    else:
        record[field].pop()
    with pytest.raises(certificates.CertificateVerificationError):
        certificates.verify_certificate(record)


def test_false_polynomial_fails_even_with_recomputed_hash(atomic_pair):
    record = deepcopy(atomic_pair[0])
    record["coefficients"][0] = str(F(record["coefficients"][0]) + 10)
    with pytest.raises(certificates.CertificateVerificationError, match="Bernstein"):
        certificates.verify_certificate(rehash(record))


def test_false_reported_bound_fails_even_with_recomputed_hash(atomic_pair):
    record = deepcopy(atomic_pair[0])
    record["bound"] = "1"
    with pytest.raises(certificates.CertificateVerificationError, match="objective"):
        certificates.verify_certificate(rehash(record))


def test_false_normalization_is_rejected(atomic_pair):
    record = deepcopy(atomic_pair[0])
    record["moment_intervals"][0] = {"lower": "99/100", "upper": "101/100"}
    with pytest.raises(certificates.CertificateVerificationError, match="b0"):
        certificates.verify_certificate(rehash(record))


def test_verifier_needs_no_numerical_library(atomic_pair, monkeypatch):
    ordinary_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split(".")[0] in {"scipy", "numpy", "mpmath", "sympy", "flint"}:
            raise AssertionError("Verifier imported a numerical dependency")
        return ordinary_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    assert certificates.verify_certificate(atomic_pair[0])["valid"]


def test_inputs_do_not_silently_accept_inexact_floats():
    with pytest.raises(ValueError, match="Rational"):
        certificates.propose_certificate([(1, 1), (0.2, 0.3)], F(1, 2), 1)


def test_consistency_is_not_misreported(atomic_pair):
    result = certificates.verify_certificate(atomic_pair[0])
    assert result["conditional_on_valid_moment_enclosures_and_positive_measure"]
    assert result["moment_feasibility_checked"] is False
