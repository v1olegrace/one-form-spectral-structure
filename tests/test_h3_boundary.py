"""Exact counterexample to identifying general Stieltjes with contact-free H3."""
import sympy as sp


def test_single_pole_critical_limit_has_contact():
    z, g2, s0 = sp.symbols('z g2 s0', positive=True)
    kernel = g2 / (z * (1 - z / (s0 + z)))
    assert sp.simplify(kernel - g2 / z - g2 / s0) == 0
    assert sp.limit(kernel, z, sp.oo) == g2 / s0


def test_subcritical_single_pole_has_positive_shifted_residue():
    z, g2, s0, t = sp.symbols('z g2 s0 t', positive=True)
    c = t / (1 + t)  # parametrizes every 0<c<1
    kernel = g2 / (z * (1 - c * z / (s0 + z)))
    residue = g2 * c / (1 - c)
    pole = s0 / (1 - c)
    assert sp.simplify(kernel - g2 / z - residue / (z + pole)) == 0
    assert sp.simplify(residue).is_positive
    assert sp.simplify(pole - s0).is_positive
    assert sp.limit(kernel, z, sp.oo) == 0
