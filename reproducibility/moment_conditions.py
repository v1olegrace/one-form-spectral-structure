"""Finite necessary conditions shared by every routine that emits a bound.

This module exists so that the filter is not a local helper of one script.
Before v0.3 the checks lived inside ``falsification_suite.py`` while three
sibling modules that also publish bounds had no equivalent guard; the
documentation nevertheless described the filter as a property of "the bound
routine".  Everything that divides by a moment matrix or takes the logarithm of
a moment ratio now imports from here.

What the gate does and does not mean
-----------------------------------
  G1  finite real moments, a_0 > 0 and a_n >= 0;
  G2  the H_0 Hankel matrix at the requested order;
  G3  the H_1 localizer (support in [0, infinity)).

Exactly one of the two matrices is the *denominator* of the pencil being
reduced, and only that one gets the strict near-singularity refusal:
``strict_shift=0`` for the Laplace pencil (H_1, H_0) used by
``laplace_geometry`` and ``falsification_suite``; ``strict_shift=1`` for the
Stieltjes pencil (H_0, H_1) used by ``analysis.localizing_bound``.  Passing the
wrong orientation would guard the wrong matrix, which is why the caller must
say which it is.  See the pencil-orientation warning in ``laplace_geometry``.

Passing means compatibility with these FINITE necessary conditions.  It is not
positivity of the underlying measure and not a proof of H3.  A refusal is one
of two distinct things, and the distinction is load-bearing:

  CHECKED_INCOMPATIBLE          a tested necessary condition is violated;
  UNRESOLVED_RANK_OR_PRECISION  the pencil is numerically singular or the
                                working precision is insufficient.  This calls
                                for a lower order, rank reduction or more
                                digits.  It is NOT a refutation of H3, and a
                                singular positive atomic measure lands here.

Nothing here is an interval certificate; results built on it are CHECKED.
"""

from __future__ import annotations

import mpmath as mp

SCOPE = "finite necessary conditions; not a proof of H3"


def moment_gate(a, strict_shift=0):
    """Finite numerical compatibility check, never a spectral certificate.

    ``a`` is coerced to real in place when the imaginary parts vanish.  The
    precision guard is a refusal heuristic, not an error enclosure.  No
    negative eigenvalue is clipped into an accepted positive one: the guard can
    only turn an acceptance into a refusal.
    """
    if strict_shift not in (0, 1):
        raise ValueError("strict_shift must be 0 (H_0 denominator) or 1 (H_1 denominator)")
    diag = {"status": "CHECKED_INCOMPATIBLE", "n_max": len(a) - 1,
            "dps": mp.mp.dps, "support_lower_bound": "0",
            "strict_shift": strict_shift, "scope": SCOPE}
    diag["moments"] = [mp.nstr(v, 8) for v in a]
    for n, v in enumerate(a):
        if not mp.isfinite(v) or mp.im(v) != 0:
            return False, f"G1 invalid: a_{n} is not finite and real", diag
        v = a[n] = mp.re(v)
        if v < 0 or (n == 0 and v == 0):
            return False, f"G1 violated: a_{n} = {mp.nstr(v, 6)}; require a_0>0 and a_n>=0", diag
    for shift, label in [(0, "G2"), (1, "G3")]:
        # Use every available moment, including the last one for even n_max.
        K = (len(a) - 1 - shift) // 2
        if K < 0:
            continue
        H = mp.matrix([[a[i + j + shift] for j in range(K + 1)]
                       for i in range(K + 1)])
        lo = min(mp.eigsy(H, eigvals_only=True))
        scale = max(abs(v) for v in H)
        guard = 100 * (K + 1) * mp.eps * scale
        diag[f"min_eig_H{shift}"] = mp.nstr(lo, 12)
        if shift == 0:
            diag["det_H0"] = mp.nstr(mp.det(H), 8)
        if lo < -guard:
            return False, f"{label} violated: H_{shift} has a negative eigenvalue at K={K}", diag
        strict = (shift == strict_shift)
        if (strict and lo <= guard) or (not strict and lo < 0):
            diag["status"] = "UNRESOLVED_RANK_OR_PRECISION"
            return False, (f"{label} unresolved: H_{shift} at K={K}; increase precision, "
                           "reduce order or use rank reduction; not a refutation of H3"), diag
    diag["status"] = "CHECKED_COMPATIBLE"
    return True, "finite moment conditions passed; H3 remains an assumption", diag


def validate_request(r, order, name):
    """Reject radii and orders outside the domain before any quadrature runs."""
    if type(order) is not int or order < (1 if name == "n_max" else 0):
        raise ValueError(f"{name} must be an integer >= {1 if name == 'n_max' else 0}")
    r = mp.mpf(r)
    if not mp.isfinite(r) or r <= 0:
        raise ValueError("radius must be finite and positive")
    return r


def mass_from_log_ratio(ratio, h, *, what="sampled pencil eigenvalue"):
    """Return -log(ratio)/h, refusing the inputs for which it is meaningless.

    For samples b_j = Phi(r+jh)/Phi(r) the pencil eigenvalue is an average of
    y = e^{-hx} over a positive measure, so it must lie in (0, 1].  Outside
    that range the logarithm is complex or the ``mass`` is negative; taking it
    anyway is how an unresolved pencil turns into a published number.
    """
    h = mp.mpf(h)
    if not mp.isfinite(h) or h <= 0:
        raise ValueError("spacing h must be finite and positive")
    if not mp.isfinite(ratio) or mp.im(ratio) != 0:
        raise ValueError(f"No bound: {what} is not finite and real")
    ratio = mp.re(ratio)
    if not 0 < ratio <= 1:
        raise ValueError(f"No bound: {what} = {mp.nstr(ratio, 8)} outside (0,1]; "
                         "unresolved pencil, not a threshold")
    return -mp.log(ratio) / h


def conditioning_digits(matrix):
    """Return (min_eig, max_eig, decimal digits needed) for a symmetric matrix.

    Used to state the precision a pencil actually requires instead of quoting a
    condition number that already underflowed.
    """
    ev = mp.eigsy(matrix, eigvals_only=True)
    lo, hi = min(ev), max(ev)
    if lo <= 0 or hi <= 0:
        return lo, hi, None
    return lo, hi, int(-mp.log10(lo / hi)) + 1
