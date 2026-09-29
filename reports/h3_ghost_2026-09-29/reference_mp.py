#!/usr/bin/env python
"""Independent multiprecision reference for the RPA atom.

Nothing here shares code with ``ghost_analysis``: different arithmetic (mpmath
instead of binary64), different quadrature (mpmath.quad / Gauss-Legendre instead
of QUADPACK), different root finder (mpmath.findroot instead of brentq).

Two purposes.

1.  A deviation between the two sides of a sum rule measures the inconsistency
    of the two computed sides.  It does NOT say which component was wrong and it
    is NOT an error bound.  Fixing a test tolerance to an observed deviation is a
    regression test, not a precision claim.  These references are what makes a
    precision statement possible at all: run at increasing dps and watch the
    value settle.

2.  The uniform density is fully closed-form, so it is an EXACT anchor, not
    merely a second opinion.

Representability note: an edge distance like 1e-517 is outside binary64, not
outside arithmetic.  mpmath handles it directly, and the log10 coordinate does
too.  "Irrepresentable" was the wrong word for a float64 limitation.
"""
from __future__ import annotations

import mpmath as mp

S_THR = 4


# ---------------------------------------------------------------- exact anchor
def uniform_exact(a, b, g2, dps=50):
    """rho = 1 on [a,b].  Atom position and weight in closed form.

    Pi(inf) = log(b/a);  Z3 = 1 - g2 log(b/a);
    W(-t) = Z3 + g2 log((t-b)/(t-a)) for t > b, so the root solves

        log((t-b)/(t-a)) = -Z3/g2,     i.e.   (t-b)/(t-a) = e^{-Z3/g2}.

    Solving the linear equation:  t = (b - a*K) / (1 - K),  K = e^{-Z3/g2}.
    And w = 1 / (t * [1/(t-b) - 1/(t-a)]), from int_a^b ds/(t-s)^2.
    """
    with mp.workdps(dps):
        a, b, g2 = mp.mpf(a), mp.mpf(b), mp.mpf(g2)
        Z3 = 1 - g2 * mp.log(b / a)
        if Z3 <= 0:
            return {"Z3": Z3, "atom": None}
        K = mp.e ** (-Z3 / g2)
        t = (b - a * K) / (1 - K)
        w = 1 / (t * (1 / (t - b) - 1 / (t - a)))
        return {"Z3": Z3, "s_atom": t, "edge_distance": t - b, "weight": w,
                "residual_W_at_root": Z3 + g2 * mp.log((t - b) / (t - a))}


# ------------------------------------------------- multiprecision Dirac kernel
def _rho(s):
    return (1 + 2 / s) * mp.sqrt(1 - S_THR / s) / (12 * mp.pi ** 2)


def _pi_inf(L2):
    return mp.quad(lambda u: _rho(S_THR * mp.e ** u), [0, mp.log(L2 / S_THR)])


def dirac_reference(k, L2, dps=60):
    """Atom for the one-loop Dirac density at coupling k * g2_critical.

    Uses the same two substitutions as the float64 path for the same reason --
    the integrand is a spike of width ~d/L2 -- but everything else differs, and
    dps is a free knob so convergence can be watched rather than assumed.
    """
    with mp.workdps(dps):
        L2 = mp.mpf(L2)
        P = _pi_inf(L2)
        g2 = mp.mpf(k) / P
        Z3 = 1 - g2 * P
        if Z3 <= 0:
            return {"Z3": Z3, "atom": None, "dps": dps}
        top = L2 - S_THR

        def W_edge(d):
            I = mp.quad(lambda u: _rho(L2 - d * mp.e ** u) * mp.e ** u / (mp.e ** u + 1),
                        [-40, mp.log(top / d)])
            return Z3 - g2 * I

        v = mp.findroot(lambda v: W_edge(mp.mpf(10) ** v), mp.mpf(-1), solver='secant',
                        tol=mp.mpf(10) ** (-dps + 10))
        d = mp.mpf(10) ** v
        integral = mp.quad(lambda u: _rho(L2 - d * mp.e ** u) * mp.e ** u / (1 + mp.e ** u) ** 2,
                           [-40, mp.log(top / d)]) / d
        return {"Z3": Z3, "g2": g2, "edge_distance": d, "log10_edge_distance": v,
                "s_atom": L2 + d, "weight": 1 / ((L2 + d) * integral),
                "residual_W_at_root": W_edge(d), "dps": dps}


def convergence_table(k, L2, dps_list=(30, 40, 60)):
    """Same case at increasing precision: the value must settle, not just exist."""
    out = []
    for dps in dps_list:
        r = dirac_reference(k, L2, dps=dps)
        out.append({"dps": dps, "log10_d": r["log10_edge_distance"],
                    "weight": r["weight"], "residual": r["residual_W_at_root"]})
    return out


if __name__ == "__main__":
    print("=== exact anchor: rho = 1 on [4,10], g2 = 1/(2 log(5/2)) ===")
    g2 = 1 / (2 * mp.log(mp.mpf(5) / 2))
    r = uniform_exact(4, 10, g2, dps=50)
    print(f"  Z3            = {mp.nstr(r['Z3'], 25)}   (expect 1/2)")
    print(f"  s_atom        = {mp.nstr(r['s_atom'], 25)}   (expect 14)")
    print(f"  weight        = {mp.nstr(r['weight'], 25)}   (expect 10/21 = "
          f"{mp.nstr(mp.mpf(10)/21, 25)})")
    print(f"  W at the root = {mp.nstr(r['residual_W_at_root'], 5)}")

    print("\n=== Dirac, L2 = 1e6, increasing precision ===")
    for k in (0.5, 0.1):
        print(f"  k = {k}")
        for row in convergence_table(k, 1e6):
            print(f"    dps={row['dps']:>3}  log10(d)={mp.nstr(row['log10_d'], 18):>22}"
                  f"  w={mp.nstr(row['weight'], 18):>24}"
                  f"  |W(root)|={mp.nstr(abs(row['residual']), 3)}")
