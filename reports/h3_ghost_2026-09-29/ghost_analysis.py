#!/usr/bin/env python
"""Where exactly does H3 break in the Dyson/RPA kernel?  The spacelike ghost.

Object of study (appendix conventions, m = q = 1, hbar = c = 1):

    Pibar(Q2) = Q2 * int_{4}^{L2} rho(s) ds / (s (s + Q2))          >= 0
    G(Q2)     = g2 / ( Q2 * [1 - g2 * Pibar(Q2)] )
    rho(s)    = (1/12 pi^2) (1 + 2/s) sqrt(1 - 4/s)       (one-loop Dirac)

Central identity (exact, partial fractions Q2/(s(s+Q2)) = 1/s - 1/(s+Q2)):

    W(Q2) := 1 - g2 Pibar(Q2) = Z3 + g2 * int rho(s) ds/(s + Q2),
    Z3 := 1 - g2 * int rho(s)/s ds.

So W(0) = 1 identically and W(inf) = Z3.  W is strictly decreasing.

CLAIM UNDER TEST. G belongs to the general Stieltjes class iff Z3 >= 0.
Contact-free H3 additionally requires G(infinity)=0. With a finite cutoff,
the critical case Z3=0 has a positive constant and fails contact-free H3,
despite having no spacelike pole. For Z3<0 a spacelike pole obstructs even
the general Stieltjes representation while the continuum remains positive.

This is a model computation inside the RPA/bubble structure.  It does NOT
establish H3 for the gauge-invariant nonperturbative static response.
"""
from __future__ import annotations

import sys
import warnings
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "reproducibility"))

from rpa_kernel_conditions import RPAHypotheses, classify_rpa_kernel

S_THR = 4.0                      # threshold s = 4 m^2, in units m = 1
PREF = 1.0 / (12.0 * np.pi**2)   # one-loop Dirac prefactor, q = 1


# ----------------------------------------------------------------- densities
def rho(s):
    """One-loop Dirac spectral density of the matter current.  rho >= 0."""
    s = np.asarray(s, dtype=float)
    out = np.zeros_like(s)
    m = s > S_THR
    out[m] = PREF * (1.0 + 2.0 / s[m]) * np.sqrt(1.0 - S_THR / s[m])
    return out


def _rho_scalar(s):
    if s <= S_THR:
        return 0.0
    return PREF * (1.0 + 2.0 / s) * np.sqrt(1.0 - S_THR / s)


def _validate_model(g2, L2):
    if (isinstance(g2, (bool, np.bool_)) or isinstance(L2, (bool, np.bool_))
            or not np.isfinite(g2) or g2 <= 0
            or not np.isfinite(L2) or L2 <= S_THR):
        raise ValueError("require finite g2 > 0 and L2 > threshold")


def Pi_infinity(L2):
    """int_{4}^{L2} rho(s)/s ds, via s = 4 e^t so the log range is tamed."""
    T = np.log(L2 / S_THR)
    val, err = quad(lambda t: _rho_scalar(S_THR * np.exp(t)), 0.0, T,
                    limit=400, epsabs=1e-13, epsrel=1e-12)
    return val, err


def Z3_of(g2, L2):
    P, _ = Pi_infinity(L2)
    return 1.0 - g2 * P


def g2_critical(L2):
    """Coupling at which Z3 = 0 for this cutoff."""
    P, _ = Pi_infinity(L2)
    return 1.0 / P


def _quad(f, lo, hi, **kw):
    """quad with the convergence message kept, not discarded to the terminal.

    SciPy's abserr is an ESTIMATE. When QUADPACK reports non-convergence or
    roundoff in the extrapolation table, that estimate is not even an estimate
    of the achieved accuracy, and any downstream "resolved" label is unearned.
    """
    kw.setdefault("limit", 400)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", IntegrationWarning)
        val, err, info, *msg = quad(f, lo, hi, full_output=1, **kw)
    messages = [str(w.message) for w in caught
                if issubclass(w.category, IntegrationWarning)]
    messages += [str(m) for m in msg if m]
    if not np.isfinite(val) or not np.isfinite(err):
        messages.append("Nonfinite quadrature result or error estimate")
    return val, err, ("; ".join(dict.fromkeys(messages)) if messages else None)


def _z3_estimate(g2, L2):
    _validate_model(g2, L2)
    P, err, message = _quad(lambda t: _rho_scalar(S_THR * np.exp(t)), 0.0,
                           np.log(L2 / S_THR), epsabs=1e-13, epsrel=1e-12)
    if not np.isfinite(P) or not np.isfinite(err):
        raise RuntimeError("UNRESOLVED: nonfinite polarization estimate")
    g, p, e = map(Fraction, (float(g2), float(P), float(abs(err))))
    return (1 - g * (p + e), 1 - g * (p - e)), err, message


def z3_interval(g2, L2):
    """(lo, hi) for Z3 from the reported quadrature error on Pi(inf).

    An ESTIMATE propagated exactly through Fraction arithmetic. It is not an
    enclosure, and it is the only Z3 information any public function here is
    allowed to branch on.
    """
    interval, _, message = _z3_estimate(g2, L2)
    if message:
        raise RuntimeError("UNRESOLVED: polarization quadrature: " + message)
    return interval


_HYP = RPAHypotheses(nonnegative_measure=True, nonzero_measure=True,
                     positive_support=True, finite_inverse_moment=True,
                     positive_coupling=True, subtracted_dyson_representation=True)


def regime_decision(g2, L2):
    """The ONE regime decision every public function shares.

    Delegates to rpa_kernel_conditions.classify_rpa_kernel so that a Z3 interval
    straddling zero is UNRESOLVED everywhere, not only in the classifier. A point
    estimate never decides the boundary, a slightly negative estimate never
    proves absence of an atom, and an exact critical identity stays a separate
    input that this numerical path cannot supply.
    """
    (lo, hi), error, message = _z3_estimate(g2, L2)
    d = classify_rpa_kernel((lo, hi), hypotheses=_HYP, total_mass="finite",
                            interval_kind="estimated")
    d["z3_lo"], d["z3_hi"] = float(lo), float(hi)
    d["quadrature_absolute_error_estimate"] = error
    d["quadrature_messages"] = [message] if message else []
    if message:
        d.update(status="UNRESOLVED", h3_status="UNRESOLVED",
                 pole_status="UNRESOLVED", reason="Polarization quadrature did not converge")
    return d


def kernel_diagnostic(g2, L2):
    """Model classification using ESTIMATED quadrature uncertainty, not a certificate.

    The analytic Dirac density at a finite cutoff verifies the listed model
    hypotheses. Rational endpoint arithmetic avoids additional rounding when
    propagating the reported quadrature error. It cannot make that error rigorous.
    A numerical g2_critical never asserts the exact identity Z3=0.
    """
    diag = regime_decision(g2, L2)
    diag["model"] = "one-loop Dirac density, hard spectral cutoff, RPA"
    return diag


# ------------------------------------------------------------------ kernel W
def W(Q2, g2, L2):
    """W = Z3 + g2 * int rho/(s+Q2) ds.  Computed in the t = log(s/4) variable."""
    T = np.log(L2 / S_THR)
    integ, _ = quad(lambda t: _rho_scalar(S_THR * np.exp(t)) * S_THR * np.exp(t)
                    / (S_THR * np.exp(t) + Q2), 0.0, T,
                    limit=400, epsabs=1e-13, epsrel=1e-12)
    return Z3_of(g2, L2) + g2 * integ


def G(Q2, g2, L2):
    """Static response kernel.  Diverges at a ghost root of W."""
    return g2 / (Q2 * W(Q2, g2, L2))


def ghost_root(g2, L2, hi=1e18):
    """Locate the spacelike zero of W, or return None when there is none."""
    decision = regime_decision(g2, L2)
    if decision["status"] == "NO_SPACELIKE_POLE":
        return None
    if decision["status"] != "SPACELIKE_POLE_DETECTED":
        raise RuntimeError("UNRESOLVED: cannot decide spacelike pole from a critical estimate")
    lo = 0.0  # W(0)=1; a fixed positive lower bound can miss a small root.
    # W(0)=1>0 and W(inf)=Z3<0, so a bracket always exists when Z3<0.
    while W(hi, g2, L2) > 0 and hi < 1e300:
        hi *= 10.0
    return brentq(lambda q: W(q, g2, L2), lo, hi, rtol=1e-13, maxiter=300)


# --------------------------------------------------- continuum spectral density
def W_on_cut(s, g2, L2):
    """W(Q2 -> -s - i0) = 1 + g2 s PV int rho/(sig(sig-s)) dsig + i pi g2 rho(s)."""
    _validate_model(g2, L2)
    if not np.isfinite(s) or s <= 0 or s in (S_THR, L2):
        raise ValueError("require positive s away from branch endpoints")
    f = lambda sig: _rho_scalar(sig) / sig
    pv, _ = quad(f, S_THR, L2, weight='cauchy', wvar=s, limit=400,
                 epsabs=1e-12, epsrel=1e-11)
    imag = np.pi * g2 * _rho_scalar(s) if S_THR < s < L2 else 0.0
    return complex(1.0 + g2 * s * pv, imag)


def density(s, g2, L2):
    """dsigma/ds = (1/pi) Im G(-s - i0).  Should be >= 0 for every coupling."""
    _validate_model(g2, L2)
    if not np.isfinite(s):
        raise ValueError("s must be finite")
    if not S_THR < s < L2:
        return 0.0  # Continuum only; discrete atoms are handled separately.
    Wc = W_on_cut(s, g2, L2)
    Gc = g2 / ((-s) * Wc)
    return Gc.imag / np.pi


def density_closed_form(s, g2, L2):
    """Hand-derived: g2^2 rho(s) / (s |W|^2).  Cross-check on `density`."""
    _validate_model(g2, L2)
    if not np.isfinite(s):
        raise ValueError("s must be finite")
    if not S_THR < s < L2:
        return 0.0
    Wc = W_on_cut(s, g2, L2)
    return g2**2 * _rho_scalar(s) / (s * abs(Wc)**2)


# ------------------------------------------- discrete spectrum above the cutoff
def _W_above_cutoff(t, g2, L2):
    """W(Q2 = -t) for t > L2, where W is real again (no cut there)."""
    T = np.log(L2 / S_THR)
    I, _ = quad(lambda u: _rho_scalar(S_THR * np.exp(u)) * S_THR * np.exp(u)
                / (t - S_THR * np.exp(u)), 0.0, T,
                limit=400, epsabs=1e-14, epsrel=1e-12)
    return Z3_of(g2, L2) - g2 * I


# Closed form of the edge integral, derived with s = 4/(1 - v^2).  Checked
# against 50-digit tanh-sinh quadrature for b in {10, 1e6} and d from 1e-30 to
# 1e8 (agreement 1e-41 .. 1e-51), and in binary64 against the same reference:
# ~1e-16 for d <= 1e3*b ... degrading by cancellation to 4e-13 at d = 100*b and
# 1.5e-11 at d = 1e4*b.  Beyond CLOSED_FORM_MAX_RATIO * L2 the quadrature is used,
# where t - s >= 99*L2 makes the integrand smooth.
CLOSED_FORM_MAX_RATIO = 100.0


def _edge_logs(d, L2):
    t = L2 + d
    v = np.sqrt(1.0 - S_THR / L2)
    a = np.sqrt(1.0 - S_THR / t)
    # log(t b (a+v)^2 / (4d)) as a sum, so d = 1e-300 does not overflow
    L = np.log(t) + np.log(L2) + 2.0 * np.log(a + v) - np.log(4.0) - np.log(d)
    return t, v, a, L


def _I_edge_closed(d, L2):
    """int_4^{L2} rho(s)/(L2 + d - s) ds, exactly."""
    t, v, a, L = _edge_logs(d, L2)
    return PREF * (a * (1.0 + 2.0 / t) * L
                   - (np.log(L2) + 2.0 * np.log(1.0 + v) - np.log(4.0))
                   - 4.0 * v / t)


def _dI_edge_closed(d, L2):
    """d/dd of _I_edge_closed; equals -int rho/(t-s)^2 ds.

    Uses d/dt[a(1 + 2/t)] = 12/(t^3 a), which follows from (1+2/t) - a^2 = 6/t.
    """
    t, v, a, L = _edge_logs(d, L2)
    return PREF * (12.0 * L / (t ** 3 * a)
                   + a * (1.0 + 2.0 / t) * (1.0 / t + 4.0 / (t ** 2 * a * (a + v)) - 1.0 / d)
                   + 4.0 * v / t ** 2)


def _W_edge(d, g2, L2):
    """W at t = L2 + d, parametrised by the DISTANCE d > 0 to the cutoff edge.

    For d <= CLOSED_FORM_MAX_RATIO * L2 the edge integral is evaluated in closed
    form: no quadrature, no branch-point trouble, and valid down to d = 1e-300.
    Beyond that, adaptive quadrature in x = L2 - s, whose integrand is smooth
    there.  The earlier all-quadrature path missed the atom position by ~1.2e-6
    relative because the integrand has a square-root branch point at the upper
    endpoint that QUADPACK does not resolve; that path is gone for the atom range.
    """
    if not np.isfinite(d) or d <= 0:
        raise ValueError("edge distance must be finite and positive")
    if d <= CLOSED_FORM_MAX_RATIO * L2:
        return Z3_of(g2, L2) - g2 * _I_edge_closed(d, L2)
    top = L2 - S_THR
    I, _, message = _quad(lambda x: _rho_scalar(L2 - x) / (x + d), 0.0, top,
                          limit=400, epsabs=1e-16, epsrel=1e-12)
    if message:
        warnings.warn(message, IntegrationWarning, stacklevel=2)
    return Z3_of(g2, L2) - g2 * I


def atom_weight_integral(d_a, L2):
    """w_a = 1 / (s_a * int rho_J(s)/(s_a - s)^2 ds), an INDEPENDENT route.

    From w = g2/((-s_a) W'(-s_a)) with W'(Q2) = -g2 int rho/(s+Q2)^2 the coupling
    cancels, so this shares no arithmetic with the finite-difference route.

    Parametrised by the EDGE DISTANCE d_a = s_a - L2. In the raw variable the
    integrand is a spike of width ~d/L2, which adaptive quadrature walks straight
    past: at L2 = 1e6 and d = 5.3 it returned a NEGATIVE value for a positive
    integrand. Substituting x = L2 - s and then x = d e^u gives

        int rho/(s_a-s)^2 ds = (1/d) int rho(L2 - d e^u) e^u/(1+e^u)^2 du,

    whose integrand is O(1) and decays both ways, so the spike is resolved.
    """
    top = L2 - S_THR
    val, err, msg = _quad(
        lambda u: _rho_scalar(L2 - d_a * np.exp(u)) * np.exp(u) / (1.0 + np.exp(u)) ** 2,
        -40.0, np.log(top / d_a), epsabs=1e-16, epsrel=1e-13)
    integral = val / d_a
    return 1.0 / ((L2 + d_a) * integral), err, msg


def spectral_atom(g2, L2, log10_d_range=(-300.0, 250.0)):
    """The discrete atom of sigma above the hard cutoff, as a structured result.

    A hard cutoff leaves the real interval (L2, inf) outside the cut, so W is
    real there.  On it W is strictly increasing, runs to -inf as t -> L2+, and
    tends to Z3.  Hence EXACTLY ONE root iff Z3 > 0 (Proposition 4).  The atom
    has positive weight at positive s, so it does not break positivity; what it
    breaks is the claim that sigma stays inside the support of rho_J.

    The regime comes from ``regime_decision``, the same interval-based call the
    classifier uses.  A Z3 estimate that straddles zero yields UNRESOLVED here
    too: a point estimate must not decide the boundary, and a slightly negative
    estimate must not prove absence.

    Returns None only when the regime is decidedly supercritical.  Otherwise a
    dict with s_atom, edge_distance, weight, weight_independent, status and
    quadrature_ok.  ``status`` separates three different things:

      RESOLVED                  root bracketed, position representable
      RESOLVED_EDGE_UNRESOLVED  root found but d < L2*eps, so s_atom rounds to
                                L2; the weight is still meaningful, the position
                                is known only as "within machine epsilon of L2"
      PRECISION_UNCERTAIN       a quadrature call reported non-convergence, so
                                no precision claim is supported even though a
                                root was located

    Raises RuntimeError when the regime is UNRESOLVED, or when Z3 > 0 but the
    root is not bracketed.  Existence follows from Proposition 4, so failing to
    locate it is an unresolved numerical result, never absence.
    """
    dec = regime_decision(g2, L2)
    if dec["status"] == "SPACELIKE_POLE_DETECTED":
        return None
    if dec["status"] != "NO_SPACELIKE_POLE":
        raise RuntimeError(
            f"regime is {dec['status']} (Z3 in [{dec['z3_lo']:.3e}, "
            f"{dec['z3_hi']:.3e}]): the atom question is UNRESOLVED, not settled. "
            "A point estimate of Z3 does not decide the boundary.")
    lo, hi = log10_d_range
    msgs = []

    def evaluate_edge(distance):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", IntegrationWarning)
            val = _W_edge(distance, g2, L2)
        msgs.extend(str(w.message) for w in caught
                    if issubclass(w.category, IntegrationWarning))
        if not np.isfinite(val):
            raise RuntimeError("UNRESOLVED: nonfinite edge-kernel evaluation")
        return val

    def f(v):
        return evaluate_edge(10.0 ** v)

    f_lo, f_hi = f(lo), f(hi)
    if not (f_lo < 0 < f_hi):
        raise RuntimeError(
            f"Z3 in [{dec['z3_lo']:.3e}, {dec['z3_hi']:.3e}] is positive, so "
            f"exactly one atom exists by Proposition 4, but its edge distance is "
            f"outside 10^[{lo}, {hi}] (W={f_lo:.3e} .. {f_hi:.3e}). UNRESOLVED, "
            "not absence: at small coupling d falls below binary64, which is a "
            "limit of this float64 path, not of the mathematics.")
    # brentq stops at |dv| < xtol + rtol*|v|, and its DEFAULT xtol is 2e-12
    # absolute: that, not the closed form, capped log10(d) at ~1e-13 relative.
    # rtol is set to scipy's floor, 4*eps.
    v_a = brentq(f, lo, hi, xtol=1e-300, rtol=4 * np.finfo(float).eps, maxiter=400)
    d_a = 10.0 ** v_a
    s_a = L2 + d_a

    h = d_a * 1e-6
    dW_dQ2 = -(evaluate_edge(d_a + h) - evaluate_edge(d_a - h)) / (2 * h)
    if not np.isfinite(dW_dQ2) or dW_dQ2 >= 0:
        raise RuntimeError("UNRESOLVED: atom derivative is nonfinite or has invalid sign")
    w_fd = g2 / ((-s_a) * dW_dQ2)
    # Primary weight: analytic derivative of the closed-form edge integral,
    # w = g2/((-s_a) W'(-s_a)) = -1/(s_a I'(d)).  No subtraction, no quadrature.
    w_analytic = None
    if d_a <= CLOSED_FORM_MAX_RATIO * L2:
        dI = _dI_edge_closed(d_a, L2)
        if np.isfinite(dI) and dI < 0:
            w_analytic = -1.0 / (s_a * dI)
    w_int, w_err, w_msg = atom_weight_integral(d_a, L2)
    if w_msg:
        msgs.append(w_msg)
    if not np.isfinite(w_int) or w_int <= 0:
        msgs.append("Independent atom weight is nonfinite or nonpositive")
    msgs = list(dict.fromkeys(msgs))

    ok = not msgs
    status = "RESOLVED" if s_a > L2 else "RESOLVED_EDGE_UNRESOLVED"
    if not ok:
        status = "PRECISION_UNCERTAIN"
    return {"s_atom": s_a, "edge_distance": d_a, "log10_edge_distance": v_a,
            "weight": w_analytic if w_analytic is not None else w_fd,
            "weight_method": "analytic closed form" if w_analytic is not None
                             else "finite difference",
            "weight_finite_difference": w_fd, "weight_independent": w_int,
            "weight_routes_agree_rel": abs(w_fd - w_int) / abs(w_int) if w_int else None,
            "status": status, "quadrature_ok": ok,
            "position_representable": bool(s_a > L2), "evidence": "CHECKED",
            "quadrature_messages": msgs,
            "regime": dec["status"], "z3_interval": [dec["z3_lo"], dec["z3_hi"]]}


def spectral_regime(g2, L2):
    """Name the regime and list every term the representation needs.

    Delegates the regime to ``regime_decision`` so classification, location and
    reconstruction cannot disagree near the boundary.
    """
    dec = regime_decision(g2, L2)
    base = {"z3_interval": [dec["z3_lo"], dec["z3_hi"]], "decision": dec["status"]}
    if dec["status"] == "NO_SPACELIKE_POLE":
        return {**base, "regime": "subcritical",
                "terms": ["coulomb_pole", "continuum", "timelike_atom"],
                "atom": spectral_atom(g2, L2), "spacelike_pole": None,
                "reconstruction_supported": True,
                "note": "positive Stieltjes representation, no constant"}
    if dec["status"] == "SPACELIKE_POLE_DETECTED":
        return {**base, "regime": "supercritical",
                "terms": ["coulomb_pole", "continuum", "spacelike_pole_negative_residue"],
                "atom": None, "spacelike_pole": ghost_root(g2, L2),
                "reconstruction_supported": False,
                "note": "a spacelike pole is not a Stieltjes term; no representation"}
    return {**base, "regime": "unresolved",
            "terms": ["coulomb_pole", "continuum", "UNDETERMINED"],
            "atom": None, "spacelike_pole": None,
            "reconstruction_supported": False,
            "note": "Z3 estimate straddles zero; the boundary case needs an exact "
                    "identity this numerical path cannot supply"}


def reconstruct(Q2, g2, L2, include_atom=True, *, return_diagnostics=False):
    """Rebuild G(Q2) - g2/Q2 from the spectral terms actually implemented.

    ONLY the subcritical regime (Z3 > 0) is supported.  At Z3 = 0 the additive
    constant is not implemented; at Z3 < 0 the object is not a Stieltjes
    representation at all.  Both REFUSE rather than returning a number that
    would silently look like a reconstruction.

    ``include_atom=False`` reproduces the INCOMPLETE reconstruction that hid the
    atom inside what looked like quadrature error.  It is kept so a test can
    assert that dropping the atom is detectable.
    Use return_diagnostics=True for structured convergence status. The scalar
    convenience result emits IntegrationWarning if any component did not converge.
    """
    if not np.isfinite(Q2) or Q2 <= 0:
        raise ValueError("Q2 must be finite and positive")
    info = spectral_regime(g2, L2)
    if not info["reconstruction_supported"]:
        raise ValueError(
            f"reconstruction not implemented for the {info['regime']} regime "
            f"(Z3 in {info['z3_interval']}): {info['note']}")
    T = np.log(L2 / S_THR)
    total, error, message = _quad(lambda u: density(S_THR * np.exp(u), g2, L2) * S_THR * np.exp(u)
                    / (S_THR * np.exp(u) + Q2), 0.0, T,
                    limit=400, epsabs=1e-18, epsrel=1e-12)
    messages = [message] if message else []
    if include_atom:
        atom = info["atom"]
        total += atom["weight"] / (Q2 + atom["s_atom"])
        messages.extend(atom["quadrature_messages"])
    result = {"value": total, "status": "PRECISION_UNCERTAIN" if messages else "CHECKED",
              "quadrature_messages": list(dict.fromkeys(messages)),
              "outer_quadrature_error_estimate": error,
              "error_scope": "outer integral estimate only; not a total error bound",
              "includes_atom": bool(include_atom)}
    if return_diagnostics:
        return result
    if messages:
        warnings.warn("Reconstruction precision uncertain: " + "; ".join(result["quadrature_messages"]),
                      IntegrationWarning, stacklevel=2)
    return total


def sum_rules(g2, L2):
    """Global weight checks.  Local agreement at a few Q2 cannot see a missing term.

    From z*G(z) = g2 / W(z) and W(inf) = Z3, expanding both sides at z -> inf:

        (1)  g2 + int dsigma_cont + sum_a w_a  =  g2 / Z3
        (2)  int s dsigma_cont + sum_a w_a s_a =  g2^2 * mu / Z3^2,   mu = int rho_J ds

    Moments exist because s * dsigma/ds = g2^2 rho/|W|^2 is bounded on the
    compact support, and the atom contributes finitely.

    Returned errors are ESTIMATES from adaptive quadrature, not enclosures.
    """
    info = spectral_regime(g2, L2)
    if info["regime"] != "subcritical":
        raise ValueError(f"sum rules implemented for the subcritical regime only "
                         f"(got {info['regime']}, Z3 in {info['z3_interval']})")
    # The INTERVAL decided the regime; the identity itself needs a value, and the
    # interval is strictly positive here, so the point estimate is admissible.
    z3 = Z3_of(g2, L2)
    atom = info["atom"]
    s_a, w = atom["s_atom"], atom["weight"]
    T = np.log(L2 / S_THR)

    mass, mass_err, mass_msg = _quad(lambda u: density(S_THR * np.exp(u), g2, L2) * S_THR * np.exp(u),
                          0.0, T, limit=500, epsabs=1e-18, epsrel=1e-12)
    first, first_err, first_msg = _quad(lambda u: (S_THR * np.exp(u))
                            * density(S_THR * np.exp(u), g2, L2) * S_THR * np.exp(u),
                            0.0, T, limit=500, epsabs=1e-16, epsrel=1e-12)
    mu, mu_err, mu_msg = _quad(lambda u: _rho_scalar(S_THR * np.exp(u)) * S_THR * np.exp(u),
                      0.0, T, limit=500, epsabs=1e-15, epsrel=1e-13)

    lhs1, rhs1 = g2 + mass + w, g2 / z3
    lhs2, rhs2 = first + w * s_a, g2**2 * mu / z3**2
    messages = list(dict.fromkeys(atom["quadrature_messages"] +
                                  [m for m in (mass_msg, first_msg, mu_msg) if m]))
    return {
        "status": "PRECISION_UNCERTAIN" if messages else "CHECKED",
        "quadrature_messages": messages,
        "error_scope": "quadrature estimates omit root/weight and inner-integral errors; not total bounds",
        "regime": info["regime"], "Z3": z3, "z3_interval": info["z3_interval"],
        "atom_s": s_a, "atom_w": w, "atom_status": atom["status"],
        "rule1": {"lhs": lhs1, "rhs": rhs1, "rel": abs(lhs1 - rhs1) / abs(rhs1),
                  "quad_err_estimate": mass_err},
        "rule2": {"lhs": lhs2, "rhs": rhs2, "rel": abs(lhs2 - rhs2) / abs(rhs2),
                  "quad_err_estimate": first_err + g2**2 * mu_err / z3**2},
        "evidence": "CHECKED: adaptive-quadrature estimates, not interval enclosures",
    }


# ------------------------------------------------------- moments for the gate
def continuum_moments(r, n_max, g2, L2):
    """a_n(r) = int s^(n/2) e^(-r sqrt s) dsigma(s), continuum part only."""
    out = []
    T = np.log(L2 / S_THR)
    for n in range(n_max + 1):
        def integrand(t, n=n):
            s = S_THR * np.exp(t)
            return s**(n / 2.0) * np.exp(-r * np.sqrt(s)) * density(s, g2, L2) * s
        val, _ = quad(integrand, 0.0, T, limit=300, epsabs=1e-14, epsrel=1e-10)
        out.append(val)
    return out


# ------------------------------------------------------------------- the tests
def run_tests(verbose=True):
    L2 = 1.0e6
    g2c = g2_critical(L2)
    say = print if verbose else (lambda *a, **k: None)
    say(f"cutoff L2 = {L2:.3g}   critical coupling g2c = {g2c:.6f}")
    say(f"  (QED physical value g2 = 4*pi/137 = {4*np.pi/137:.6f}, "
        f"ratio g2/g2c = {4*np.pi/137/g2c:.3e})")

    # ---- T1: exact endpoint values of W
    for g2 in (0.3 * g2c, g2c, 1.7 * g2c):
        w0 = W(1e-12, g2, L2)
        winf = W(1e14, g2, L2)
        z3 = Z3_of(g2, L2)
        assert abs(w0 - 1.0) < 1e-6, f"W(0) should be 1, got {w0}"
        assert abs(winf - z3) < 1e-6, f"W(inf) should be Z3={z3}, got {winf}"
    say("T1 OK   W(0) = 1 and W(inf) = Z3, for every coupling tested")

    # ---- T2: ghost exists iff Z3 < 0; location diverges as Z3 -> 0^-
    assert ghost_root(0.5 * g2c, L2) is None
    assert ghost_root(g2c, L2) is None                     # Z3 = 0 exactly
    roots = {}
    for k in (1.02, 1.1, 1.5, 3.0):
        q = ghost_root(k * g2c, L2)
        assert q is not None and q > 0.0
        roots[k] = q
    assert roots[1.02] > roots[1.1] > roots[1.5] > roots[3.0], \
        "ghost should move IN as the coupling grows / out as Z3 -> 0^-"
    say("T2 OK   ghost root exists iff Z3 < 0; it runs to infinity as Z3 -> 0^-")
    for k, q in roots.items():
        say(f"          g2/g2c = {k:>5}   Z3 = {Z3_of(k*g2c, L2):+.4f}   "
            f"Q2_ghost = {q:.4e}")

    # ---- T3: continuum density stays >= 0 on BOTH sides of the threshold
    grid = np.array([4.5, 6.0, 10.0, 50.0, 500.0, 1e4, 1e5])
    for g2 in (0.5 * g2c, g2c, 1.5 * g2c, 3.0 * g2c):
        for s in grid:
            d = density(s, g2, L2)
            assert d >= 0.0, f"density negative at s={s}, g2/g2c={g2/g2c}"
            dc = density_closed_form(s, g2, L2)
            assert abs(d - dc) <= 1e-9 * max(1.0, abs(d)), \
                f"closed form disagrees at s={s}: {d} vs {dc}"
    say("T3 OK   continuum density >= 0 for every coupling, including Z3 < 0")
    say("        and it matches the hand-derived g2^2 rho /(s |W|^2)")

    # ---- T4: G > 0 on (0,inf) iff Z3 >= 0; sign flip across the ghost
    qs = np.logspace(-3, 8, 40)
    for g2 in (0.5 * g2c, g2c):
        assert all(G(q, g2, L2) > 0 for q in qs)
    qg = ghost_root(1.5 * g2c, L2)
    assert G(qg * 0.5, 1.5 * g2c, L2) > 0 > G(qg * 2.0, 1.5 * g2c, L2), \
        "G must change sign across the ghost pole"
    say("T4 OK   G > 0 everywhere iff Z3 >= 0; G changes sign across the ghost")

    # ---- T5: the project's own moment gate, applied to the CONTINUUM part
    import mpmath as mp
    from moment_conditions import moment_gate
    mp.mp.dps = 30
    verdicts = {}
    for label, g2 in (("Z3>0", 0.5 * g2c), ("Z3<0", 1.5 * g2c)):
        a = [mp.mpf(v) for v in continuum_moments(1.0, 3, g2, L2)]
        ok, reason, diag = moment_gate(a, strict_shift=0)
        verdicts[label] = (ok, diag["status"])
        say(f"T5      continuum moments, {label}: {diag['status']}")
    assert verdicts["Z3>0"][0], "continuum part must pass when Z3>0"
    # The finding: the gate ALSO passes when Z3<0, because the violation lives
    # in the discrete ghost, not in the continuum density.
    assert verdicts["Z3<0"][0], \
        "expected the continuum-only gate to be blind to the ghost"
    say("T5 OK   BLIND SPOT CONFIRMED: a continuum-only moment gate passes even")
    say("        when Z3 < 0.  The H3 violation is carried by the discrete")
    say("        spacelike pole, which no continuum moment sees.")

    # ---- T6: weak-coupling limit reproduces the leading-order measure
    g2 = 1e-4 * g2c
    for s in (6.0, 20.0, 200.0):
        lo = g2**2 * _rho_scalar(s) / s          # dsigma_LO = g^4 rho/s
        got = density(s, g2, L2)
        assert abs(got - lo) <= 5e-3 * lo, f"LO limit off at s={s}: {got} vs {lo}"
    say("T6 OK   g2 -> 0 reproduces dsigma_LO = g_R^4 rho(s)/s (appendix A)")

    say("\nall assertions passed")
    return {"L2": L2, "g2c": g2c, "roots": roots}


# ------------------------------------------------------------------- figures
def make_figures(outdir: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    L2 = 1.0e6
    g2c = g2_critical(L2)
    outdir.mkdir(parents=True, exist_ok=True)

    # Fig 1 -- W(Q2): the zero crossing is the whole story
    fig, ax = plt.subplots(figsize=(7, 4.4))
    q = np.logspace(-2, 10, 220)
    for k, c in ((0.5, "#2E6B4F"), (1.0, "#17334C"), (1.5, "#A64B2A"), (3.0, "#8A3324")):
        w = np.array([W(x, k * g2c, L2) for x in q])
        ax.semilogx(q, w, color=c, lw=1.8,
                    label=f"$g^2/g^2_c={k}$,  $Z_3={Z3_of(k*g2c, L2):+.3f}$")
    ax.axhline(0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("$Q^2\\;[m^2]$"); ax.set_ylabel("$W(Q^2)=1-g^2\\bar\\Pi$")
    ax.set_title("$W(0)=1$ always, $W(\\infty)=Z_3$.  A zero at $Q^2>0$ is the ghost.")
    ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(outdir / "fig1_W_zero_crossing.png", dpi=150)
    plt.close(fig)

    # Fig 2 -- ghost location vs Z3, diverging as Z3 -> 0^-
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ks = np.linspace(1.005, 4.0, 60)
    z3s, qgs = [], []
    for k in ks:
        r = ghost_root(k * g2c, L2)
        if r:
            z3s.append(Z3_of(k * g2c, L2)); qgs.append(r)
    ax.semilogy(z3s, qgs, color="#A64B2A", lw=2)
    ax.set_xlabel("$Z_3$  (negative side only)")
    ax.set_ylabel("$Q^2_{\\rm ghost}\\;[m^2]$")
    ax.set_title("The ghost runs to infinity as $Z_3\\to0^-$: no ghost for $Z_3\\geq 0$")
    ax.invert_xaxis(); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(outdir / "fig2_ghost_location.png", dpi=150)
    plt.close(fig)

    # Fig 3 -- continuum density stays positive on both sides
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ss = np.logspace(np.log10(4.01), 5, 160)
    for k, c in ((0.5, "#2E6B4F"), (1.5, "#A64B2A"), (3.0, "#8A3324")):
        d = np.array([density(s, k * g2c, L2) for s in ss])
        ax.loglog(ss, d, color=c, lw=1.7,
                  label=f"$g^2/g^2_c={k}$,  $Z_3={Z3_of(k*g2c, L2):+.3f}$")
    ax.set_xlabel("$s\\;[m^2]$"); ax.set_ylabel("$d\\sigma/ds$")
    ax.set_title("Continuum density is $\\geq 0$ even when $Z_3<0$ — the blind spot")
    ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")
    fig.tight_layout(); fig.savefig(outdir / "fig3_density_positive.png", dpi=150)
    plt.close(fig)

    # Fig 4 -- G itself, with the pole
    fig, ax = plt.subplots(figsize=(7, 4.4))
    q = np.logspace(-1, 9, 300)
    for k, c in ((0.5, "#2E6B4F"), (1.5, "#A64B2A")):
        g = np.array([G(x, k * g2c, L2) for x in q])
        ax.plot(np.log10(q), np.sign(g) * np.log10(1 + abs(g)), color=c, lw=1.7,
                label=f"$g^2/g^2_c={k}$,  $Z_3={Z3_of(k*g2c, L2):+.3f}$")
    qg = ghost_root(1.5 * g2c, L2)
    ax.axvline(np.log10(qg), color="#8A3324", ls=":", lw=1.4,
               label=f"ghost at $Q^2={qg:.2e}$")
    ax.axhline(0, color="k", lw=.8, ls="--")
    ax.set_xlabel("$\\log_{10} Q^2$")
    ax.set_ylabel("signed $\\log_{10}(1+|\\mathcal{G}|)$")
    ax.set_title("A Stieltjes function cannot have a pole at spacelike $Q^2$")
    ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(outdir / "fig4_G_pole.png", dpi=150)
    plt.close(fig)
    return outdir


def sensitivity():
    """How Z3 and the ghost respond to the cutoff and the coupling."""
    rows = []
    for L2 in (1e4, 1e6, 1e10, 1e20):
        g2c = g2_critical(L2)
        P, err = Pi_infinity(L2)
        rows.append((L2, P, err, g2c, Z3_of(4 * np.pi / 137, L2)))
    return rows


if __name__ == "__main__":
    info = run_tests()
    print("\n--- conditional kernel diagnostics (estimated uncertainty) ---")
    for k in (0.5, 1.0, 1.5):
        diag = kernel_diagnostic(k * g2_critical(1e6), 1e6)
        print(k, diag["status"], diag["h3_status"])
    print("\n--- sensitivity: cutoff dependence ---")
    print(f"{'L2':>10} {'Pi(inf)':>12} {'quad err':>11} {'g2_crit':>10} {'Z3(QED)':>10}")
    for L2, P, err, g2c, z3 in sensitivity():
        print(f"{L2:>10.0e} {P:>12.6f} {err:>11.2e} {g2c:>10.4f} {z3:>10.6f}")
    out = make_figures(Path(__file__).resolve().parent / "figures")
    print(f"\nfigures written to {out}")
