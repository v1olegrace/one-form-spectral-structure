"""Validated one-loop Dirac/scalar Laplace data using Arb and an analytic tail.

All dimensional inputs are exact rationals.  x=2*m+t**2 removes the threshold
square root, and exp(-2*m*r) is factored out during integration.  The backend
encloses the finite integral; positivity and a closed analytic majorant enclose
the omitted tail.  Results are certificates for the specified ONE-LOOP model,
conditional on FLINT/Arb's arithmetic, not for interacting QED or H3 in general.
"""
from __future__ import annotations

from fractions import Fraction
from flint import acb, arb, ctx


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, Fraction)):
        raise ValueError("Use exact rational strings, integers or Fraction inputs")
    return Fraction(value)


def ball(value):
    return arb(str(rational(value)))


def endpoints(value):
    """Outward dyadic endpoints, converted to exact fractions, never decimals."""
    if not value.is_finite():
        raise ArithmeticError("Nonfinite Arb enclosure")
    return Fraction(str(value.lower().fmpq())), Fraction(str(value.upper().fmpq()))


def interval_record(pair):
    return {"lower": str(pair[0]), "upper": str(pair[1])}


def _integrand(kind, radius, mass, coupling2, charge):
    r, m, amplitude = ball(radius), ball(mass), ball(coupling2) * ball(charge)**2
    pi2 = arb.pi()**2

    def function(t, analytic):
        t2 = t*t
        x = 2*m + t2
        # Forwarding analytic is essential, including away from the real path.
        root = (4*m + t2).sqrt(analytic=analytic)
        if kind == "dirac":
            density_jacobian = amplitude*t2*root*(1 + 2*m*m/(x*x))/(3*pi2)
        elif kind == "scalar":
            density_jacobian = amplitude*t2*t2*root**3/(12*pi2*x*x)
        else:
            raise ValueError("kind must be dirac or scalar")
        return (-r*t2).exp()*density_jacobian
    return function


def _finite(kind, radius, mass, coupling2, charge, upper, tolerance):
    value = acb.integral(
        _integrand(kind, radius, mass, coupling2, charge), 0, acb(upper),
        rel_tol=ball(tolerance), abs_tol=ball(tolerance),
        eval_limit=200000, depth_limit=100,
    )
    if not value.is_finite() or not value.imag.contains(0):
        raise ArithmeticError("Integration failed to enclose a real value")
    return value.real


def certify_sample(kind, radius, *, mass="1", coupling2="1", charge="1",
                   t_max="8", bits=160, tolerance="1e-28", max_relative_width="1e-20"):
    r, m, g2, q, T = map(rational, (radius, mass, coupling2, charge, t_max))
    if kind not in ("dirac", "scalar") or min(r, m, g2, T) <= 0 or q == 0:
        raise ValueError("Require Dirac/scalar, r,m,g²,T>0 and q!=0")
    if type(bits) is not int or bits < 64:
        raise ValueError("bits must be an integer >=64")
    if rational(tolerance) <= 0 or rational(max_relative_width) <= 0:
        raise ValueError("Error tolerances must be positive")
    with ctx.workprec(bits):
        finite = _finite(kind, r, m, g2, q, ball(T), tolerance)
        flo, fhi = endpoints(finite)
        # dnu_D/dx <= g²q² x/(4pi²); dnu_S/dx <= g²q² x/(24pi²).
        A = 2*ball(m) + ball(T)**2
        factor = ball(g2)*ball(q)**2 / ((4 if kind == "dirac" else 24)*arb.pi()**2)
        tail = factor * (-ball(r)*ball(T)**2).exp()*(A/ball(r) + 1/ball(r)**2)
        tail_hi = endpoints(tail)[1]
        slo, shi = max(Fraction(0), flo), fhi + tail_hi
        exponent = (-2*ball(m)*ball(r)).exp()
        lo = endpoints(ball(slo)*exponent)[0]
        hi = endpoints(ball(shi)*exponent)[1]
        if lo <= 0 or (hi-lo)/lo > rational(max_relative_width):
            raise ArithmeticError("Positive enclosure did not achieve requested width")
        return {
            "kind": kind, "radius": str(r), "mass": str(m), "coupling2": str(g2),
            "charge": str(q), "bits": bits, "t_max": str(T), "x_max": str(2*m+T*T),
            "tolerance_goal": str(tolerance), "backend": "FLINT/Arb acb.integral",
            "raw": interval_record((lo, hi)), "scaled": interval_record((slo, shi)),
            "finite_scaled": interval_record((flo, fhi)), "tail_scaled_upper": str(tail_hi),
            "finite_scaled_width": str(fhi-flo), "raw_relative_width": str((hi-lo)/lo),
            "certificate_scope": "one-loop model; arithmetic and quadrature plus analytic tail",
        }


def cutoff_enclosure(mass_cutoff, spacing, *, bits=160):
    c, h = rational(mass_cutoff), rational(spacing)
    if c <= 0 or h <= 0:
        raise ValueError("Require positive cutoff and spacing")
    with ctx.workprec(bits):
        return endpoints((-ball(c)*ball(h)).exp())


def certify_weight(kind, radius, mass_cutoff, *, mass="1", bits=160,
                   denominator=None, tolerance="1e-28"):
    """Direct benchmark integral; not supplied to the inference methods.

    Integrate up to sqrt(cutoff-2m), itself an Arb enclosure. acb.integral
    handles uncertain endpoints. Total denominator is from certify_sample.
    """
    c, m, r = map(rational, (mass_cutoff, mass, radius))
    if r <= 0 or m <= 0:
        raise ValueError("Require positive radius and mass")
    if c <= 2*m:
        return interval_record((Fraction(0), Fraction(0)))
    if denominator is None:
        denominator = certify_sample(kind, r, mass=m, bits=bits)
    if (denominator["kind"] != kind or Fraction(denominator["radius"]) != r
            or Fraction(denominator["mass"]) != m
            or Fraction(denominator["coupling2"]) != 1 or Fraction(denominator["charge"]) != 1):
        raise ValueError("Denominator must match the model and radius")
    with ctx.workprec(bits):
        part = _finite(kind, r, m, "1", "1", (ball(c)-2*ball(m)).sqrt(), tolerance)
        plo, phi = endpoints(part)
        dlo, dhi = (Fraction(denominator["scaled"][k]) for k in ("lower", "upper"))
        return interval_record((max(Fraction(0), plo/dhi), min(Fraction(1), phi/dlo)))


def upper_mass_from_ratio(ratio, spacing, *, bits=160):
    """Certified upper endpoint for -log(ratio)/h, given rational 0<ratio<=1."""
    ratio, h = rational(ratio), rational(spacing)
    if not 0 < ratio <= 1 or h <= 0:
        raise ValueError("Require 0<ratio<=1 and h>0")
    with ctx.workprec(bits):
        return endpoints(-ball(ratio).log()/ball(h))[1]
