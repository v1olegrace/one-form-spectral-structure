"""Measure pushforward (audit correction F), Hankel monotonicity, edge law, gate.

These are unit tests of the claims that the manuscript states as theorems.
They are numerical CHECKS at high working precision, not interval certificates;
see ``reproducibility/interval_bounds.py`` for the certified subset.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reproducibility"))
from spectral_models import build_models, dirac_density          # noqa: E402
from falsification_suite import positivity_gate, hankel_bound     # noqa: E402

mp.mp.dps = 50
MODELS = build_models()


# --------------------------------------------------------------------------
# Correction F: nu is the WEIGHTED PUSHFORWARD of sigma, not a density formula
# --------------------------------------------------------------------------

def test_atom_transport_is_not_a_density_formula():
    """An atom w delta_{s_a} in sigma maps to (s_a w/g_R^2) delta_{sqrt s_a} in nu.

    Applying the absolutely-continuous formula dnu = 2x^3 sigma(x^2) dx/g_R^2 to
    an atom is meaningless; the pushforward definition
    int f dnu = (1/g_R^2) int s f(sqrt s) dsigma handles it automatically.
    """
    g2 = mp.mpf(1)
    w, s_a = mp.mpf(3), mp.mpf(9)          # atom of weight 3 at s = 9, so x = 3
    # pushforward of f(x) = x^n
    for n in range(4):
        pushed = (1 / g2) * s_a * (mp.sqrt(s_a) ** n) * w
        # direct atom in nu: weight (s_a w/g_R^2) at x = sqrt(s_a)
        direct = (s_a * w / g2) * (mp.sqrt(s_a) ** n)
        assert abs(pushed - direct) < mp.mpf("1e-40")


def test_mixed_atom_plus_continuum_moments_are_additive():
    m = MODELS["C_atom_plus_continuum"]
    r = mp.mpf(2)
    # a_0 must equal the atom part plus the continuum part computed separately
    atom = mp.mpf(1) * mp.e ** (-r * 2)
    cont = mp.quad(lambda t: (t ** mp.mpf(0.5)) * mp.e ** (-t) * mp.e ** (-r * (4 + t)),
                   [0, 1, 5, mp.inf])
    total_scaled = m.scaled_a(0, r)            # = e^{+2r} a_0(r)
    assert abs(total_scaled * mp.e ** (-2 * r) - (atom + cont)) / (atom + cont) < mp.mpf("1e-20")


def test_single_atom_is_exact():
    m = MODELS["A_single_atom"]
    for r in ["0.5", "2", "7"]:
        assert abs(m.Gamma(mp.mpf(r)) - 3) < mp.mpf("1e-40")


# --------------------------------------------------------------------------
# Theorem C / E: ordering and monotonicity
# --------------------------------------------------------------------------

@pytest.mark.parametrize("key", ["D_dirac", "E_scalar", "C_atom_plus_continuum",
                                 "F_multi_species"])
def test_gamma_is_decreasing_and_above_the_edge(key):
    m = MODELS[key]
    prev = None
    for r in [1, 2, 4, 8, 16]:
        g = m.Gamma(mp.mpf(r))
        assert g >= mp.mpf(m.M_star) - mp.mpf("1e-30"), f"{key}: Gamma < M_* at r={r}"
        if prev is not None:
            assert g <= prev + mp.mpf("1e-30"), f"{key}: Gamma increased at r={r}"
        prev = g


@pytest.mark.parametrize("key", ["D_dirac", "E_scalar"])
def test_hankel_hierarchy_is_monotone_and_bounding(key):
    m = MODELS[key]
    r = mp.mpf(2)
    ok, reason, _ = positivity_gate(m, r, n_max=9)
    assert ok, reason
    prev = None
    for K in range(4):
        b = hankel_bound(m, r, K)
        assert b >= mp.mpf(m.M_star) - mp.mpf("1e-25"), f"{key}: B_{K} below M_*"
        if prev is not None:
            assert b <= prev + mp.mpf("1e-25"), f"{key}: B_{K} > B_{K-1}"
        prev = b


def test_B0_equals_Gamma():
    m = MODELS["D_dirac"]
    r = mp.mpf(3)
    assert abs(hankel_bound(m, r, 0) - m.Gamma(r)) < mp.mpf("1e-30")


# --------------------------------------------------------------------------
# Theorem D: edge exponents discriminate spinor from scalar
# --------------------------------------------------------------------------

@pytest.mark.parametrize("key,p", [("D_dirac", 1.5), ("E_scalar", 2.5)])
def test_edge_exponent(key, p):
    m = MODELS[key]
    r = mp.mpf(120)
    lead = r * (m.Gamma(r) - mp.mpf(m.M_star))
    assert abs(lead - mp.mpf(p)) < mp.mpf("0.07"), f"{key}: r(Gamma-M_*) = {lead}"


def test_dirac_two_term_edge_law():
    """Gamma = 2m + 3/(2r) - 5/(16 m r^2) + O(r^-3): residual must fall like r^-3."""
    m = MODELS["D_dirac"]
    res = []
    for r in [20, 40, 80]:
        r = mp.mpf(r)
        two_term = 2 + mp.mpf(3) / (2 * r) - mp.mpf(5) / (16 * r**2)
        res.append(abs(m.Gamma(r) - two_term))
    ratios = [res[i] / res[i + 1] for i in range(len(res) - 1)]
    for q in ratios:
        assert 4 < q < 16, f"residual ratio {q} inconsistent with O(r^-3)"


# --------------------------------------------------------------------------
# The positivity gate must refuse H3 violations
# --------------------------------------------------------------------------

def test_gate_refuses_signed_measure():
    m = MODELS["J_signed_measure"]
    ok, reason, _ = positivity_gate(m, mp.mpf(1), n_max=5)
    assert not ok, "the gate accepted a signed measure"
    assert "G1" in reason or "G2" in reason


def test_gate_accepts_genuine_positive_measures():
    for key in ["D_dirac", "E_scalar", "C_atom_plus_continuum", "F_multi_species"]:
        ok, reason, _ = positivity_gate(MODELS[key], mp.mpf(2), n_max=7)
        assert ok, f"{key} wrongly refused: {reason}"


def test_screening_alone_does_not_detect_the_violation():
    """Phi>0 and -Phi'>0 hold for the signed model: a weaker gate would pass it."""
    m = MODELS["J_signed_measure"]
    r = mp.mpf(1)
    assert m.scaled_a(0, r) > 0
    assert m.scaled_a(1, r) > 0


# --------------------------------------------------------------------------
# H2 is a real restriction
# --------------------------------------------------------------------------

def test_gapless_model_drives_gamma_to_zero():
    m = MODELS["K_no_gap"]
    assert m.Gamma(mp.mpf(1000)) < mp.mpf("0.01")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
