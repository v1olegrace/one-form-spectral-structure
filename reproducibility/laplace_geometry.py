"""Certification of the positive Laplace geometry of one-form symmetry breaking.

Companion to manuscript/apendice_geometria_laplace.qmd.

Benchmark: one Dirac fermion of mass m and charge q, weakly gauged with
coupling g.  Units m = q = g = 1, so the true charged threshold is M_* = 2m = 2.

The script checks selected benchmark identities in extended precision (mpmath).
These are numerical checks, not interval certificates or proofs of all claims:

  A  master identity        delta(r) = r^2 * Laplace[dnu](r), dnu >= 0
     (a) delta(r) equals Basile-Golmohammadi eq. (13) verbatim
     (b) delta(r) equals -r q'(r)/q_inf with q(r) built from the Gauss law
     (c) (-1)^n Phi^(n)(r) equals the local Laplace moment a_n(r) > 0
  L4 universal cap          0 <= delta(r) <= g^2 q^2 / (6 pi^2), saturated at r->0
  B  complete monotonicity  (-1)^n Phi^(n) >= 0
  C  threshold estimator    Gamma(r) = -dlog Phi/dr  decreases to M_*
  D  edge law               Gamma(r) = 2m + 3/(2r) - 5/(16 m r^2) + O(r^-3)
  E  Hankel hierarchy       M_* <= B_K(r) = lambda_min(H_1, H_0), B_{K+1} <= B_K

IMPORTANT (pencil orientation).  These are *Laplace* moments with positive
powers, a_n = int x^n e^{-rx} dnu.  The correct bound is lambda_min(H_1, H_0).
This is the opposite pencil to analysis.py's localizing_bound(), which handles
*Stieltjes* moments c_n = int dmu/s^{n+1} with negative powers and bounds
s_0 <= lambda_min(H_0, H_1).  Do not interchange the two routines.

Usage:  python reproducibility/laplace_geometry.py
Exit code is non-zero if any numerical check fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moment_conditions import moment_gate, validate_request   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "output" / "data"

WORKING_DPS = 30      # identity chain, caps, monotonicity
HANKEL_DPS = 80       # ill-conditioned generalized eigenvalue problem

M = mp.mpf(1)         # fermion mass
Q = mp.mpf(1)         # integer charge
G2 = mp.mpf(1)        # g^2
M_STAR = 2 * M        # true threshold sqrt(s_*) = 2m

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    """Record a numerical check, without an interval error certificate."""
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# --------------------------------------------------------------------------
# Spectral data
# --------------------------------------------------------------------------

def rho_J(s):
    """One-loop Dirac current spectral density; zero below threshold."""
    if s <= 4 * M**2:
        return mp.mpf(0)
    return Q**2 / (12 * mp.pi**2) * (1 + 2 * M**2 / s) * mp.sqrt(1 - 4 * M**2 / s)


def dnu_density(x):
    """dnu/dx = g^2 * 2 x rho_J(x^2) on x in [2m, inf); the positive measure."""
    return G2 * 2 * x * rho_J(x**2)


# Substitution x = 2m + t^2 removes the inverse-square-root edge singularity,
# which is what lets mp.quad reach full working precision near the threshold.
# After it the integrand carries e^{-r t^2}, of width t ~ 1/sqrt(r); at large r
# the panels must track that width or the quadrature silently loses digits.
def _panels(r=None):
    """Quadrature panels in t, where x = 2m + t^2.

    LOAD-BEARING: the panel widths must scale as r^{-1/2}.  With fixed panels
    the edge-law test at r = 40, 80 silently loses digits and the third decimal
    of r*(Gamma-2m) comes out wrong -- it looks converged but is not.  Do not
    replace this with a constant panel list.
    """
    if r is None or r <= 4:
        return [0, mp.mpf("0.5"), 2, 6, mp.inf]
    w = 1 / mp.sqrt(r)
    return sorted({mp.mpf(0), w, 4 * w, 12 * w, mp.mpf(6)}) + [mp.inf]


def edge_integral(fun, r=None):
    """Integrate fun(x) over x in [2m, inf) with the edge-softening substitution."""
    return mp.quad(lambda t: 2 * t * fun(2 * M + t**2), _panels(r))


def a_moment(n, r):
    """Local Laplace moment a_n(r) = int x^n e^{-rx} dnu(x)."""
    return edge_integral(
        lambda x: x**n * mp.e ** (-r * x) * dnu_density(x), r
    )


def scaled_moment(n, r):
    """e^(2mr) a_n(r), with y=sqrt(r(x-2m)).

    Removing the tiny common exponential BEFORE quadrature avoids false
    convergence from absolute quadrature tolerances at large r.
    """
    if r <= 0 or n < 0:
        raise ValueError("r must be positive and n nonnegative")
    return mp.quad(
        lambda y: 2*y/r * (2*M+y*y/r)**n * mp.exp(-y*y)
        * dnu_density(2*M+y*y/r), [0, 1, 3, 8, mp.inf]
    )


def Phi(r):
    """Reduced breaking profile Phi(r) = delta(r)/r^2 = a_0(r)."""
    return a_moment(0, r)


def delta(r):
    """Breaking profile delta(r) = -(r/q_inf) dq/dr, sign fixed so screening > 0."""
    return r**2 * Phi(r)


def delta_basile_golmohammadi(r):
    """Their eq. (13): (g^2 q^2/6 pi^2) int_{2m}^inf dp p r^2 e^{-pr} (...)."""
    def integrand(p):
        return (
            p * r**2 * mp.e ** (-p * r)
            * (1 + 2 * M**2 / p**2)
            * mp.sqrt(1 - 4 * M**2 / p**2)
        )
    return G2 * Q**2 / (6 * mp.pi**2) * edge_integral(integrand, r)


def q_effective(r):
    """q(r)/q_inf from the Gauss law, Lemma 3, at O(g^2):
    q(r)/q_inf = 1 + g^2 int ds rho_J(s) (1/s + r/sqrt s) e^{-r sqrt s}."""
    return 1 + edge_integral(
        lambda x: dnu_density(x) * (1 / x**2 + r / x) * mp.e ** (-r * x), r
    )


def Gamma(r):
    """Threshold estimator Gamma(r) = -dlog Phi/dr = a_1/a_0."""
    return scaled_moment(1, r) / scaled_moment(0, r)


def hankel_bound(r, K, *, diagnostics=False):
    """B_K(r) = lambda_min(H_1, H_0), the pencil for POSITIVE-power moments.

    The finite necessary conditions of ``moment_conditions.moment_gate`` are
    checked on the moments this routine actually uses, exactly as in
    ``falsification_suite.hankel_bound``.  A refusal raises instead of emitting
    a number: an unresolved pencil is not a threshold.  Even after the checks
    the bound remains conditional on a positive measure, and it is CHECKED
    rather than CERTIFIED because ``mp.quad`` carries no error enclosure.
    """
    r = validate_request(r, K, "K")
    a = [scaled_moment(n, r) for n in range(2 * K + 2)]
    ok, reason, diag = moment_gate(a, strict_shift=0)
    if not ok:
        raise ValueError(f"No bound: {reason}")
    H0 = mp.matrix(K + 1, K + 1)
    H1 = mp.matrix(K + 1, K + 1)
    for i in range(K + 1):
        for j in range(K + 1):
            H0[i, j] = a[i + j]
            H1[i, j] = a[i + j + 1]
    # H0 passed G2 above (Thm E-i), so reduce the pencil by Cholesky.
    L_inv = mp.inverse(mp.cholesky(H0))
    S = L_inv * H1 * L_inv.T
    S = (S + S.T) / 2                      # symmetrize against round-off
    bound = min(mp.eigsy(S, eigvals_only=True))
    if not mp.isfinite(bound) or bound < 0:
        raise ValueError("No bound: negative or nonfinite eigenvalue; precision unresolved")
    return (bound, diag) if diagnostics else bound


# --------------------------------------------------------------------------
# Certifications
# --------------------------------------------------------------------------

def certify_identity_chain() -> dict:
    print("\n== Theorem A: master identity ==")
    out: dict = {}

    rows = []
    for rs in ["0.3", "1", "2.5", "6"]:
        r = mp.mpf(rs)
        ours, theirs = delta(r), delta_basile_golmohammadi(r)
        rel = abs(ours - theirs) / theirs
        rows.append({"r": rs, "delta_ours": mp.nstr(ours, 18),
                     "delta_BG_eq13": mp.nstr(theirs, 18), "rel_diff": mp.nstr(rel, 3)})
        check(f"A(a) delta(r={rs}) == Basile-Golmohammadi eq.(13)",
              rel < mp.mpf("1e-25"), f"rel diff {mp.nstr(rel, 3)}")
    out["vs_basile_golmohammadi"] = rows

    rows = []
    for rs in ["0.5", "1", "3"]:
        r = mp.mpf(rs)
        gauss = -r * mp.diff(q_effective, r)      # -(r/q_inf) dq/dr
        rel = abs(gauss - delta(r)) / delta(r)
        rows.append({"r": rs, "minus_r_dq_dr": mp.nstr(gauss, 15),
                     "delta": mp.nstr(delta(r), 15), "rel_diff": mp.nstr(rel, 3)})
        check(f"A(b) -(r/q_inf) dq/dr == delta(r) at r={rs}",
              rel < mp.mpf("1e-20"), f"rel diff {mp.nstr(rel, 3)}")
    out["gauss_law_closure"] = rows

    rows = []
    for rs in ["0.7", "2.0"]:
        r = mp.mpf(rs)
        for n in range(4):
            deriv = (-1) ** n * mp.diff(Phi, r, n)
            mom = a_moment(n, r)
            rel = abs(deriv - mom) / mom
            rows.append({"r": rs, "n": n, "signed_derivative": mp.nstr(deriv, 12),
                         "a_n": mp.nstr(mom, 12), "rel_diff": mp.nstr(rel, 3)})
            check(f"A(c)/B  (-1)^{n} Phi^({n})(r={rs}) == a_{n} > 0",
                  rel < mp.mpf("1e-15") and mom > 0, f"a_{n}={mp.nstr(mom, 10)}")
    out["derivatives_are_moments"] = rows
    return out


def certify_cap() -> dict:
    print("\n== Lemma 4: universal cap and COR coefficient ==")
    cap = G2 * Q**2 / (6 * mp.pi**2)
    rows, prev, decreasing = [], None, True
    for rs in ["0.001", "0.01", "0.1", "0.5", "1", "2", "4", "8"]:
        r = mp.mpf(rs)
        d = delta(r)
        if prev is not None and d > prev:
            decreasing = False
        prev = d
        rows.append({"r": rs, "delta": mp.nstr(d, 12), "Delta": mp.nstr(d / cap, 10)})
        check(f"L4 delta(r={rs}) <= g^2q^2/6pi^2", d <= cap,
              f"Delta={mp.nstr(d / cap, 8)}")
    sat = delta(mp.mpf("0.001")) / cap
    check("L4 saturation delta(r->0) -> g^2q^2/6pi^2", abs(sat - 1) < mp.mpf("1e-5"),
          f"Delta(0.001)={mp.nstr(sat, 10)}")
    check("L4 Delta decreasing on test grid", decreasing)
    return {"cap_g2q2_over_6pi2": mp.nstr(cap, 12), "profile": rows,
            "Delta_decreasing": decreasing}


def certify_gamma() -> dict:
    print("\n== Theorem C: threshold estimator Gamma(r) ==")
    rows, prev = [], None
    for mr in ["0.5", "1", "2", "3", "5", "10"]:
        r = mp.mpf(mr)
        gam = Gamma(r)
        rows.append({"mr": mr, "Gamma_over_m": mp.nstr(gam / M, 9),
                     "Gamma_over_2m": mp.nstr(gam / M_STAR, 9),
                     "excess_percent": mp.nstr((gam / M_STAR - 1) * 100, 6)})
        check(f"C(i)  Gamma(mr={mr}) >= M_* = 2m", gam >= M_STAR,
              f"Gamma/2m={mp.nstr(gam / M_STAR, 8)}")
        if prev is not None:
            check(f"C(ii) Gamma decreasing at mr={mr}", gam <= prev)
        prev = gam
    return {"table": rows}


def certify_edge_law() -> dict:
    print("\n== Theorem D: edge law  Gamma = 2m + 3/(2r) - 5/(16 m r^2) ==")
    # Phi(80) ~ e^{-160}; the O(r^-3) residual we are resolving is ~1e-6 on top
    # of Gamma ~ 2, so the working precision must be raised for this test.
    saved_dps, mp.mp.dps = mp.mp.dps, 60
    rows, residuals = [], []
    for rv in [10, 20, 40, 80]:
        r = mp.mpf(rv)
        gam = Gamma(r)
        leading = r * (gam - M_STAR)                       # -> alpha + 1 = 3/2
        two_term = M_STAR + mp.mpf(3) / (2 * r) - mp.mpf(5) / (16 * M * r**2)
        residuals.append(abs(gam - two_term))
        with mp.workdps(90):
            higher_precision = Gamma(r)
        check(f"D precision stability 60 vs 90 dps at r={rv}",
              abs(gam-higher_precision) < mp.mpf("1e-45"))
        rows.append({"r": rv, "Gamma": mp.nstr(gam, 16),
                     "r_times_Gamma_minus_2m": mp.nstr(leading, 10),
                     "two_term_prediction": mp.nstr(two_term, 12),
                     "residual": mp.nstr(gam - two_term, 12),
                     "scaled_cubic_residual": mp.nstr(r**3*(gam-two_term), 12)})
        check(f"D  r[Gamma(r)-2m] approaches 3/2 at r={rv}",
              abs(leading - mp.mpf("1.5")) < mp.mpf("0.05"),
              f"= {mp.nstr(leading, 8)}")
    # The residual to the two-term formula must fall like r^-3 (factor ~8 per doubling).
    ratios = [float(residuals[i] / residuals[i + 1]) for i in range(len(residuals) - 1)]
    check("D  residual to (D') scales as r^-3 (doubling ratio in [4,16])",
          all(4 <= x <= 16 for x in ratios),
          "ratios " + ", ".join(f"{x:.2f}" for x in ratios))
    mp.mp.dps = saved_dps
    return {"table": rows, "residual_doubling_ratios": [round(x, 3) for x in ratios]}


def certify_hankel() -> dict:
    print("\n== Theorem E: local Hankel hierarchy, pencil (H_1, H_0) ==")
    mp.mp.dps = HANKEL_DPS
    out = {}
    for mr in [1, 3]:
        r = mp.mpf(mr)
        rows, prev = [], None
        for K in range(6):
            B, diag = hankel_bound(r, K, diagnostics=True)
            rows.append({"K": K, "B_K_over_m": mp.nstr(B / M, 10),
                         "excess_percent": mp.nstr((B / M_STAR - 1) * 100, 6),
                         "gate_status": diag["status"],
                         "min_eig_H0": diag["min_eig_H0"],
                         "min_eig_H1": diag["min_eig_H1"]})
            check(f"E  finite moment conditions hold at mr={mr}, K={K}",
                  diag["status"] == "CHECKED_COMPATIBLE", diag["status"])
            check(f"E(ii)  B_{K}(mr={mr}) >= M_* = 2m", B >= M_STAR,
                  f"B_{K}/m={mp.nstr(B / M, 10)}")
            if prev is not None:
                check(f"E(iii) B_{K} <= B_{K - 1} at mr={mr}", B <= prev)
            prev = B
        check(f"E  B_0(mr={mr}) == Gamma(mr={mr})",
              abs(hankel_bound(r, 0) - Gamma(r)) / Gamma(r) < mp.mpf("1e-20"))
        out[f"mr_{mr}"] = rows
    mp.mp.dps = WORKING_DPS
    return out


def main() -> int:
    FAILURES.clear()
    mp.mp.dps = WORKING_DPS
    print("Positive Laplace geometry of one-form symmetry breaking")
    print(f"Dirac benchmark: m={M}, q={Q}, g^2={G2}, true M_* = {M_STAR}")
    print(f"working precision {WORKING_DPS} dps, Hankel precision {HANKEL_DPS} dps")

    results = {
        "status": "CHECKED",
        "scope": "multiprecision quadrature and identity checks; no interval error enclosure",
        "benchmark": {"m": 1, "q": 1, "g_squared": 1, "true_M_star": 2,
                      "working_dps": WORKING_DPS, "hankel_dps": HANKEL_DPS},
        "theorem_A_identity_chain": certify_identity_chain(),
        "lemma_4_cap": certify_cap(),
        "theorem_C_gamma": certify_gamma(),
        "theorem_D_edge_law": certify_edge_law(),
        "theorem_E_hankel": certify_hankel(),
    }
    results["all_checks_passed"] = not FAILURES
    results["failures"] = FAILURES

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target = DATA_DIR / "laplace_geometry_certification.json"
    target.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {target.relative_to(ROOT)}")

    if FAILURES:
        print(f"\n{len(FAILURES)} NUMERICAL CHECK FAILURE(S): {FAILURES}")
        return 1
    print("\nAll numerical checks passed (CHECKED, not interval-certified).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
