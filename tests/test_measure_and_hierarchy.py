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
from spectral_models import Model, build_models, dirac_density   # noqa: E402
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
# Finite necessary conditions: discriminating counterexamples and refusals
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


def test_localizer_rejects_signed_measure_that_passes_old_gate():
    with mp.workdps(60):
        m = Model("signed", "H1 counterexample",
                  atoms=[(1, 1), (mp.exp(1), 2), (-mp.exp(9)/1000, 10)],
                  M_star=1, positive=False)
        a = m.moments(1, 4)
        assert all(v > 0 for v in a)
        assert a[0]*a[2]-a[1]**2 > 0
        assert abs(a[1]*a[3]-a[2]**2 + mp.mpf("0.09")) < mp.mpf("1e-50")
        ok, reason, diag = positivity_gate(m, 1, 3)
        assert not ok and "G3 violated" in reason
        assert diag["status"] == "CHECKED_INCOMPATIBLE"
        with pytest.raises(ValueError, match="G3 violated"):
            hankel_bound(m, 1, 1)


def test_finite_pass_does_not_certify_signed_measure_is_positive():
    m = Model("hidden", "negative atom invisible at low order",
              atoms=[(1, 1), (1, 2), (1, 3), ("-0.000001", 4)],
              M_star=1, positive=False)
    ok, _, diag = positivity_gate(m, 1, 5)
    assert ok and diag["status"] == "CHECKED_COMPATIBLE"
    assert not positivity_gate(m, 1, 7)[0]


def test_singular_positive_measure_needs_lower_order_not_refutation():
    m = MODELS["A_single_atom"]
    ok, _, diag = positivity_gate(m, 1, 3)
    assert not ok and diag["status"] == "UNRESOLVED_RANK_OR_PRECISION"
    with pytest.raises(ValueError, match="unresolved"):
        hankel_bound(m, 1, 1)
    assert abs(hankel_bound(m, 1, 0)-3) < mp.mpf("1e-40")


def test_atom_at_zero_has_valid_semidefinite_localizer():
    m = Model("zero", "gapless atom", atoms=[(1, 0)], M_star=0)
    assert positivity_gate(m, 1, 1)[0]
    assert hankel_bound(m, 1, 0) == 0


@pytest.mark.parametrize("value", [mp.nan, mp.inf, -mp.inf, mp.mpc(1, 1)])
def test_nonfinite_or_complex_moments_refused(value):
    class BadData:
        def scaled_a(self, n, r):
            return value if n == 1 else mp.mpf(1)

        def moments(self, r, count):
            return [self.scaled_a(n, r) for n in range(count)]
    assert not positivity_gate(BadData(), 1, 1)[0]
    with pytest.raises(ValueError, match="finite and real"):
        hankel_bound(BadData(), 1, 0)


@pytest.mark.parametrize("radius,order", [(0, 1), (-1, 1), (mp.inf, 1),
                                         (1, -1), (1, 1.5), (1, True)])
def test_gate_input_domain(radius, order):
    with pytest.raises(ValueError):
        positivity_gate(MODELS["A_single_atom"], radius, order)


def test_even_order_checks_last_available_moment():
    m = MODELS["B_two_atoms"]
    assert positivity_gate(m, 1, 3)[0]
    # H0 at K=2 is singular; ignoring a4 would incorrectly pass this request.
    ok, _, diag = positivity_gate(m, 1, 4)
    assert not ok and diag["status"] == "UNRESOLVED_RANK_OR_PRECISION"


def test_precision_refusal_can_be_resolved_without_changing_measure():
    m = MODELS["I_wide_dynamic_range"]
    with mp.workdps(60):
        ok, _, diag = positivity_gate(m, 1, 3)
        assert not ok and diag["status"] == "UNRESOLVED_RANK_OR_PRECISION"
    with mp.workdps(200):
        assert positivity_gate(m, 1, 3)[0]
        assert abs(hankel_bound(m, 1, 1)-2) < mp.mpf("1e-100")


# --------------------------------------------------------------------------
# H2 is a real restriction
# --------------------------------------------------------------------------

def test_gapless_model_drives_gamma_to_zero():
    m = MODELS["K_no_gap"]
    assert m.Gamma(mp.mpf(1000)) < mp.mpf("0.01")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
