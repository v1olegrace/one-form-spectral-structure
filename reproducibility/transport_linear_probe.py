"""Linear-probe transport from <F F> to the static observables (note E2c).

notes/E2c_transport_linear_probe.md states that, for a two-point function of
the field strength of the form S(p) = T_E(p) a(p^2) with
a(p^2) = int dmu(s)/(p^2 + s), the static potential and the field of a static
line see only the slice a^(3)(r) = int dt a(t, r), which equals
int dmu(s) exp(-sqrt(s) r)/(4 pi r).  This module checks those steps by routes
that share no code:

  yukawa_time_integral   the 4D propagator sqrt(s) K1(sqrt(s)|x|)/(4 pi^2 |x|)
                         integrated over Euclidean time, by quadrature
  a_reg, a3_reg          a heat-kernel regulated kernel and its time slice,
                         each from its own one-dimensional integral
  surface_cumulant       (1/2) int_R int_R S_0101 over the planar rectangle R,
                         with S_0101 = -(a'' + a'/rho) the in-plane Laplacian
  boundary_cumulant      (1/2) oint oint dx.dy a(x - y), the Feynman-gauge form
  potential_T            V_T(r) = (q^2/T) * boundary_cumulant

Regulator.  a_eps(rho) = sum_k w_k int_eps^inf dtau exp(-(tau - eps) s_k)
exp(-rho^2/(4 tau))/(16 pi^2 tau^2) has Fourier transform
exp(-eps p^2) sum_k w_k/(p^2 + s_k): every Fourier mode keeps its sign, and
eps -> 0 restores the generalized free field with measure sum_k w_k delta_{s_k}.
The substitution tau = eps/y turns it into an integral over y in (0, 1].
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, special


def _check_measure(weights, masses2):
    w = np.atleast_1d(np.asarray(weights, dtype=float))
    s = np.atleast_1d(np.asarray(masses2, dtype=float))
    if w.shape != s.shape:
        raise ValueError("weights and masses2 must have the same length")
    if np.any(~np.isfinite(w)) or np.any(~np.isfinite(s)) or np.any(s < 0):
        raise ValueError("masses2 must be finite and non-negative, weights finite")
    return w, s


# --- unregulated generalized free field ---------------------------------------
def delta4(s, rho):
    """4D Euclidean propagator of mass^2 s at distance rho > 0."""
    if s == 0:
        return 1.0 / (4.0 * math.pi ** 2 * rho ** 2)
    m = math.sqrt(s)
    return m * special.k1(m * rho) / (4.0 * math.pi ** 2 * rho)


def yukawa(s, r):
    return math.exp(-math.sqrt(s) * r) / (4.0 * math.pi * r)


def yukawa_time_integral(s, r):
    """int_{-inf}^{inf} dt delta4(s, sqrt(t^2 + r^2)), by quadrature."""
    f = lambda t: delta4(s, math.hypot(t, r))
    val, err = integrate.quad(f, 0.0, np.inf, epsabs=0.0, epsrel=1e-12, limit=400)
    return 2.0 * val, 2.0 * err


# --- heat-kernel regulated kernel ---------------------------------------------
def _a_reg_one(rho, s, eps):
    if s == 0:
        x = rho * rho / (4.0 * eps)
        if x < 1e-8:
            return (1.0 - x / 2.0) / (16.0 * math.pi ** 2 * eps)
        return -math.expm1(-x) / (4.0 * math.pi ** 2 * rho * rho)
    g = lambda y: math.exp(-eps * s * (1.0 / y - 1.0) - rho * rho * y / (4.0 * eps)) if y > 0 else 0.0
    val, _ = integrate.quad(g, 0.0, 1.0, epsabs=0.0, epsrel=1e-12, limit=400)
    return val / (16.0 * math.pi ** 2 * eps)


def a_reg(rho, weights, masses2, eps):
    w, s = _check_measure(weights, masses2)
    return float(sum(wk * _a_reg_one(rho, sk, eps) for wk, sk in zip(w, s)))


def _lap_reg_one(rho, s, eps):
    """In-plane Laplacian a'' + a'/rho of the regulated radial kernel.

    Differentiating exp(-rho^2 y/(4 eps)) under the y-integral gives the factor
    -y/eps + rho^2 y^2/(4 eps^2); this holds for every s, s = 0 included.
    """
    h = lambda y: ((-y / eps + rho * rho * y * y / (4.0 * eps * eps))
                   * math.exp(-eps * s * (1.0 / y - 1.0) - rho * rho * y / (4.0 * eps))
                   if y > 0 else 0.0)
    val, _ = integrate.quad(h, 0.0, 1.0, epsabs=0.0, epsrel=1e-11, limit=400)
    return val / (16.0 * math.pi ** 2 * eps)


def S0101_reg(rho, weights, masses2, eps):
    """S_{01,01} = -(a'' + a'/rho) on the plane, for S = -T_E(d) a."""
    w, s = _check_measure(weights, masses2)
    return float(-sum(wk * _lap_reg_one(rho, sk, eps) for wk, sk in zip(w, s)))


def a3_reg(r, weights, masses2, eps):
    """Time slice int dt a_eps(sqrt(t^2 + r^2)), from its own integral.

    int dt of the 4D heat kernel is the 3D one, and tau = eps/z^2 gives
    a3 = 2 eps (4 pi eps)^(-3/2) int_0^1 dz exp(-eps s (1/z^2 - 1) - r^2 z^2/(4 eps)).
    """
    w, s = _check_measure(weights, masses2)
    pref = 2.0 * eps / (4.0 * math.pi * eps) ** 1.5
    tot = 0.0
    for wk, sk in zip(w, s):
        g = lambda z: (math.exp(-eps * sk * (1.0 / (z * z) - 1.0) - r * r * z * z / (4.0 * eps))
                       if z > 0 else (0.0 if sk > 0 else math.exp(-r * r * z * z / (4.0 * eps))))
        val, _ = integrate.quad(g, 0.0, 1.0, epsabs=0.0, epsrel=1e-12, limit=400)
        tot += wk * pref * val
    return tot


def a3_unregulated(r, weights, masses2):
    w, s = _check_measure(weights, masses2)
    return float(sum(wk * yukawa(sk, r) for wk, sk in zip(w, s)))


# --- the planar rectangle ------------------------------------------------------
def surface_cumulant(T, r, S_radial):
    """(1/2) int_R int_R S(x - y) over R = [0,T] x [0,r], S radial in the plane.

    In relative coordinates (u, v) the double integral has weight
    (T - |u|)(r - |v|); by symmetry it is 4 int_0^T int_0^r.
    """
    f = lambda v, u: (T - u) * (r - v) * S_radial(math.hypot(u, v))
    val, err = integrate.dblquad(f, 0.0, T, 0.0, r, epsabs=1e-13, epsrel=1e-10)
    return 2.0 * val, 2.0 * err


def boundary_cumulant(T, r, a_radial):
    """(1/2) oint oint dx.dy a(x - y) around the same rectangle.

    Parallel sides only: time-like sides int_{-T}^{T} du (T-|u|)[a(u,0) - a(u,r)],
    space-like sides int_{-r}^{r} dv (r-|v|)[a(0,v) - a(T,v)], each with
    coefficient 1 after the overall 1/2.  (Before 3 October this docstring and
    the note printed a coefficient 2; the code below was always right.)
    """
    ft = lambda u: (T - u) * (a_radial(u) - a_radial(math.hypot(u, r)))
    fs = lambda v: (r - v) * (a_radial(v) - a_radial(math.hypot(T, v)))
    It, et = integrate.quad(ft, 0.0, T, epsabs=0.0, epsrel=1e-12, limit=800)
    Is, es = integrate.quad(fs, 0.0, r, epsabs=0.0, epsrel=1e-12, limit=800)
    # the 1/2 of the cumulant times 2 (two parallel pairs) times 2 (u -> |u|)
    return 2.0 * (It + Is), 2.0 * (et + es)


def potential_T(T, r, a_radial, q2=1.0):
    """V_T(r) = -(1/T) log W from the quadratic cumulant = (q^2/T) * boundary_cumulant."""
    c, _ = boundary_cumulant(T, r, a_radial)
    return q2 * c / T


def potential_limit(r, a3, q2=1.0):
    """T -> infinity: q^2 [a3(0) - a3(r)]."""
    return q2 * (a3(0.0) - a3(r))


# --- the field of a static line and the sphere flux ----------------------------
def flux_profile(r, weights, masses2):
    """-4 pi r^2 d/dr a3(r) for the unregulated slice: the sphere flux.

    Equals sum_k w_k (1 + sqrt(s_k) r) exp(-sqrt(s_k) r); the s = 0 weight is
    the Coulomb residue g_R^2.
    """
    w, s = _check_measure(weights, masses2)
    return float(sum(wk * (1.0 + math.sqrt(sk) * r) * math.exp(-math.sqrt(sk) * r)
                     for wk, sk in zip(w, s)))


def flux_profile_numeric(r, weights, masses2, rel_step=1e-4):
    """Central difference with a step relative to r: a3 ~ 1/r near the origin,
    so an absolute step leaves a truncation error ~ (h/r)^2."""
    a3 = lambda x: a3_unregulated(x, weights, masses2)
    h = rel_step * r
    der = (a3(r + h) - a3(r - h)) / (2.0 * h)
    return -4.0 * math.pi * r * r * der


# --- a local term that violates Bianchi -----------------------------------------
# G is the tensor structure that multiplies D(x^2) in the stochastic vacuum
# model, but a local contact c G delta^4 is not that nonlocal function: its
# area slope q^2 c/(8 pi eps) diverges as the regulator is removed.
def heat_kernel4(rho, eps):
    """4D heat kernel at time eps: a smeared delta^4, integral one."""
    return math.exp(-rho * rho / (4.0 * eps)) / (16.0 * math.pi ** 2 * eps * eps)


def area_term_slope(c, eps, q2=1.0):
    """Predicted slope dV/dr of the G term c*G*heat_kernel4, for r >> sqrt(eps).

    The in-plane integral of the 4D heat kernel is 1/(4 pi eps), so
    V -> (q^2/2) c r /(4 pi eps).
    """
    return q2 * c / (8.0 * math.pi * eps)
