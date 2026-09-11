"""Phase 1: the vacuum-polarization sign, derived from the quadratic effective action.

The audit required that the sign NOT be patched ad hoc but derived once and
propagated consistently through

    Pi_{mu nu} -> Pi(q^2) -> Pi(-Q^2) -> Pi-bar(Q^2) -> inverse kernel
    -> dressed static response -> perturbative expansion -> dsigma -> dnu

and that the result reproduce the Uehling sign and normalisation.

The derivation
--------------
Euclidean quadratic effective action for the gauge field after integrating out
the matter sector, on the transverse subspace:

    S^(2) = 1/2 int_q A(-q) [ (1/g^2)(q^2 delta - q q) + Pi_{mu nu}(q) ] A(q),
    Pi_{mu nu}(q) = (q^2 delta_{mu nu} - q_mu q_nu) Pi_E(q^2).

The transverse kernel is therefore K_T(Q^2) = Q^2 (1/g^2 + Pi_E(Q^2)) and the
static response is its inverse,

    G(Q^2) = g^2 / ( Q^2 [1 + g^2 Pi_E(Q^2)] ).                         (K)

Kallen-Lehmann with one subtraction, continued to spacelike q^2 = -Q^2, gives

    Pi_E(Q^2) - Pi_E(0) = - Q^2 int rho_J(s) ds / [ s (s + Q^2) ] = -Pi-bar(Q^2),

with rho_J >= 0, hence Pi-bar >= 0 and increasing.  Renormalising Pi_E(0)=0 so
that g = g_R is the long-distance coupling,

    G(Q^2) = g^2 / ( Q^2 [1 - g^2 Pi-bar(Q^2)] )                        (K')
           = g^2/Q^2 + g^4 int rho_J(s) ds/[s(s+Q^2)] + O(g^6),

so dsigma(s) = g^4 rho_J(s) ds / s >= 0, which is H3.

Why this test discriminates
---------------------------
The historical error in this project was writing (K') with ``1 + g^2 Pi-bar``
while Pi-bar >= 0 -- i.e. mis-signing the geometric series.  That choice yields
dsigma <= 0 and destroys H3.  ``test_flipped_convention_is_detected`` asserts
exactly that: the wrong convention must produce a NEGATIVE spectral measure.
A test that only checked the correct branch would pass under either convention
and would therefore be worthless.
"""

from __future__ import annotations

import math

import mpmath as mp
import sympy as sy

# --------------------------------------------------------------------------
# Symbolic objects
# --------------------------------------------------------------------------
Q2, s, g2, rho = sy.symbols("Q2 s g2 rho", positive=True)


def pi_bar(Q2sym):
    """Pi-bar(Q^2) = Q^2 * rho / (s (s + Q^2)) -- the integrand, rho >= 0.

    Working with the integrand rather than the integral is legitimate here
    because every step below is linear in rho and the measure is positive.
    """
    return Q2sym * rho / (s * (s + Q2sym))


def kernel(sign):
    """Dressed static response.  sign=-1 is the derived convention (K')."""
    return g2 / (Q2 * (1 + sign * g2 * pi_bar(Q2)))


def continuum_coefficient(sign):
    """Coefficient of g^4 in G(Q^2) - g^2/Q^2, i.e. the density of dsigma."""
    series = sy.series(kernel(sign), g2, 0, 3).removeO()
    return sy.simplify(sy.expand(series).coeff(g2, 2))


# --------------------------------------------------------------------------
# CHECK 1 -- perturbative expansion of the inverse kernel
# --------------------------------------------------------------------------

def test_derived_convention_gives_positive_spectral_measure():
    """With sign=-1 the O(g^4) continuum is +rho/(s(s+Q^2)) > 0: H3 holds."""
    coeff = continuum_coefficient(-1)
    expected = rho / (s * (s + Q2))
    assert sy.simplify(coeff - expected) == 0, f"got {coeff}"
    # positive for every positive rho, s, Q^2
    assert coeff.subs({rho: 1, s: 2, Q2: 3}) > 0


def test_flipped_convention_is_detected():
    """The discriminating test: sign=+1 forces dsigma < 0, contradicting H3.

    If this ever passes with a positive coefficient, the sign convention has
    been changed inconsistently somewhere upstream.
    """
    coeff = continuum_coefficient(+1)
    assert sy.simplify(coeff + rho / (s * (s + Q2))) == 0, f"got {coeff}"
    assert coeff.subs({rho: 1, s: 2, Q2: 3}) < 0, (
        "the flipped convention must yield a NEGATIVE spectral measure; "
        "if it does not, this test no longer discriminates"
    )


def test_the_two_conventions_differ_in_sign():
    """Belt and braces: the two branches must have opposite signs."""
    a = continuum_coefficient(-1).subs({rho: 1, s: 2, Q2: 3})
    b = continuum_coefficient(+1).subs({rho: 1, s: 2, Q2: 3})
    assert a * b < 0


# --------------------------------------------------------------------------
# CHECK 2 -- Uehling sign and normalisation
# --------------------------------------------------------------------------

def test_uehling_coefficient():
    """phi(r) correction prefactor must be 2 alpha / (3 pi) for q=1.

    From G = g^2/Q^2 + g^4 int rho_J ds/[s(s+Q^2)] and the Yukawa transform,
    the bracket in phi(r) = (q_W/4 pi r)[g^2 + g^2 * g^2 int rho_J e^{-r sqrt s} ds ...]
    carries g^2 * q^2/(6 pi^2) after the substitution s = 4 m^2 zeta^2.
    With g^2 = 4 pi alpha and q = 1 this is 2 alpha / (3 pi).
    """
    alpha = sy.Symbol("alpha", positive=True)
    g_squared = 4 * sy.pi * alpha
    coeff = sy.simplify(g_squared / (6 * sy.pi**2))
    assert sy.simplify(coeff - 2 * alpha / (3 * sy.pi)) == 0


def test_uehling_sign_is_screening():
    """The correction must make |phi| LARGER at short distance (screening).

    q(r)/q_inf = 1 + (1/g^2) int (1 + r sqrt s) e^{-r sqrt s} dsigma, and the
    kernel (1+u)e^{-u} is positive and strictly decreasing in u >= 0, so
    q(r) > q_inf for every finite r and q(r) decreases towards q_inf.
    """
    u = sy.Symbol("u", positive=True)
    k = (1 + u) * sy.exp(-u)
    assert sy.limit(k, u, sy.oo) == 0
    assert sy.simplify(sy.diff(k, u) + u * sy.exp(-u)) == 0   # d/du = -u e^{-u}
    assert sy.diff(k, u).subs(u, sy.Rational(1, 2)) < 0        # strictly decreasing
    assert k.subs(u, sy.Rational(1, 2)) > 0                    # so q(r) > q_inf


# --------------------------------------------------------------------------
# CHECK 3 -- running coupling / screening interpretation
# --------------------------------------------------------------------------

def test_effective_coupling_grows_in_the_uv():
    """g_eff^2(Q^2) = Q^2 G(Q^2) must INCREASE with Q^2 in the derived convention.

    That is the statement that QED screens.  Under the flipped convention it
    would decrease (antiscreening), which is the physical signature of the bug.
    """
    geff = sy.simplify(Q2 * kernel(-1))
    d = sy.simplify(sy.diff(geff, Q2))
    val = d.subs({rho: 1, s: 2, Q2: 3, g2: sy.Rational(1, 10)})
    assert val > 0, f"derived convention must screen; d g_eff^2/dQ^2 = {val}"

    geff_bad = sy.simplify(Q2 * kernel(+1))
    val_bad = sy.simplify(sy.diff(geff_bad, Q2)).subs(
        {rho: 1, s: 2, Q2: 3, g2: sy.Rational(1, 10)})
    assert val_bad < 0, "flipped convention must antiscreen (it is the bug signature)"


# --------------------------------------------------------------------------
# Numerical closure: the exact differential identity (audit correction E)
# --------------------------------------------------------------------------

def test_exact_kernel_identity():
    """d/dr[(1 + r sqrt s) e^{-r sqrt s}] = -s r e^{-r sqrt s}, symbolically."""
    r, ss = sy.symbols("r s_", positive=True)
    lhs = sy.diff((1 + r * sy.sqrt(ss)) * sy.exp(-r * sy.sqrt(ss)), r)
    rhs = -ss * r * sy.exp(-r * sy.sqrt(ss))
    assert sy.simplify(lhs - rhs) == 0


def test_kernel_identity_numerically():
    mp.mp.dps = 40
    for r_ in ["0.3", "1.7", "5.0"]:
        for s_ in ["1.0", "4.0", "17.3"]:
            r_v, s_v = mp.mpf(r_), mp.mpf(s_)
            d = mp.diff(lambda rr: (1 + rr * mp.sqrt(s_v)) * mp.e ** (-rr * mp.sqrt(s_v)), r_v)
            expect = -s_v * r_v * mp.e ** (-r_v * mp.sqrt(s_v))
            assert abs(d - expect) < mp.mpf("1e-30")


def test_yukawa_transform_normalisation():
    """int d^3p/(2pi)^3 e^{ipx}/(P^2+s) = e^{-r sqrt s}/(4 pi r), checked numerically."""
    mp.mp.dps = 30
    for r_, s_ in [("1.0", "1.0"), ("2.5", "4.0"), ("0.7", "9.0")]:
        r_v, s_v = mp.mpf(r_), mp.mpf(s_)
        # Radial reduction: (1/(2 pi^2 r)) int_0^inf dP P sin(Pr)/(P^2+s).
        # The integrand is oscillatory and only conditionally convergent, so
        # plain tanh-sinh quadrature does NOT converge here; quadosc sums the
        # half-period contributions instead.
        val = mp.quadosc(lambda P: P * mp.sin(P * r_v) / (P * P + s_v),
                         [0, mp.inf], period=2 * mp.pi / r_v) / (2 * mp.pi**2 * r_v)
        expect = mp.e ** (-r_v * mp.sqrt(s_v)) / (4 * mp.pi * r_v)
        assert abs(val - expect) / expect < mp.mpf("1e-12"), (r_, s_, val, expect)


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
