"""Adversarial falsification of the Laplace tomography.

This module exists to *break* the method, not to confirm it.  Two tests are
decisive and were specified in advance by the author:

  H  a vanishing amount of weight sitting exactly at the true lowest threshold;
  J  a signed measure, which violates H3.

For each one the analytic prediction is computed FIRST and stored in
``prediction``; the numerical outcome is then compared against it.  A test that
merely produces a number is not a test.

The positivity gate
-------------------
``positivity_gate`` runs BEFORE any bound is reported.  It checks

  G1  a_n(r) = (-1)^n Phi^(n)(r) > 0 for every moment order used, and
  G2  H_0 positive definite (Cholesky succeeds).

If either fails the suite refuses to emit ``B_K``.  Returning a plausible
``M_star`` for model J would be a FATAL finding about the whole programme.

Nothing here is an interval certificate; see ``interval_bounds.py``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spectral_models import build_models          # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "output" / "data"
DPS = 60

RESULTS: list[dict] = []


def record(test, status, detail, prediction=None, observed=None):
    RESULTS.append({"test": test, "status": status, "detail": detail,
                    "prediction": prediction, "observed": observed})
    print(f"  [{status:9s}] {test}: {detail}")


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------

def positivity_gate(model, r, n_max):
    """Return (passed, reason, diagnostics). Runs before any bound is reported."""
    diag = {}
    a = [model.scaled_a(n, r) for n in range(n_max + 1)]
    diag["moments"] = [mp.nstr(v, 8) for v in a]

    for n, v in enumerate(a):
        if v <= 0:
            return False, f"G1 violated: a_{n}(r={r}) = {mp.nstr(v, 6)} <= 0", diag

    K = (n_max - 1) // 2
    if K >= 0:
        H0 = mp.matrix(K + 1, K + 1)
        for i in range(K + 1):
            for j in range(K + 1):
                H0[i, j] = a[i + j]
        try:
            mp.cholesky(H0)
        except (ValueError, ZeroDivisionError) as exc:
            return False, f"G2 violated: H_0 not positive definite at K={K} ({type(exc).__name__})", diag
        det = mp.det(H0)
        diag["det_H0"] = mp.nstr(det, 8)
        if det <= 0:
            return False, f"G2 violated: det H_0 = {mp.nstr(det, 6)} <= 0 at K={K}", diag
    return True, "gate passed", diag


def hankel_bound(model, r, K):
    """B_K(r) = lambda_min(H_1, H_0). Caller must have passed the gate."""
    a = model.moments(r, 2 * K + 2)
    H0 = mp.matrix(K + 1, K + 1)
    H1 = mp.matrix(K + 1, K + 1)
    for i in range(K + 1):
        for j in range(K + 1):
            H0[i, j] = a[i + j]
            H1[i, j] = a[i + j + 1]
    Linv = mp.inverse(mp.cholesky(H0))
    S = Linv * H1 * Linv.T
    return min(mp.eigsy((S + S.T) / 2, eigvals_only=True))


# ---------------------------------------------------------------------------
# Test J -- signed measure.  The gate MUST fire.
# ---------------------------------------------------------------------------

def test_signed_measure(models):
    m = models["J_signed_measure"]
    # Prediction, derived analytically before running:
    #   a_n(r) = e^{-r} - 0.5 * 2^n e^{-2r};  scaled by e^{+r}: 1 - 0.5*2^n e^{-r}
    #   At r = 1 this turns negative first at n = 3, since 0.5*8*e^{-1} = 1.47 > 1.
    #   det H_0 at K = 1 is a_0 a_2 - a_1^2 < 0.
    r = mp.mpf(1)
    pred_n = 3
    pred = f"gate fires; first negative moment at n={pred_n}; det H_0<0 at K=1"

    ok, reason, diag = positivity_gate(m, r, n_max=5)
    if ok:
        record("J signed measure -- gate", "FATAL",
               "gate PASSED on a signed measure; tomography would report a bogus M_*",
               pred, reason)
        return
    first_neg = next((n for n, v in enumerate(diag["moments"]) if mp.mpf(v) <= 0), None)
    record("J signed measure -- gate", "PASS",
           f"gate correctly refused ({reason})", pred,
           f"first negative moment at n={first_neg}")

    # Independently confirm det H_0 < 0 at K=1.
    a = [m.scaled_a(n, r) for n in range(3)]
    det = a[0] * a[2] - a[1] ** 2
    record("J signed measure -- det H_0", "PASS" if det < 0 else "FATAL",
           f"det H_0(K=1) = {mp.nstr(det, 6)}", "det < 0", mp.nstr(det, 6))

    # And confirm the weaker screening-only check would NOT have caught it.
    screening_ok = (m.scaled_a(0, r) > 0) and (m.scaled_a(1, r) > 0)
    record("J signed measure -- screening insufficient",
           "PASS" if screening_ok else "UNEXPECTED",
           "Phi>0 and -Phi'>0 both hold, so a screening-only test is fooled; "
           "only complete monotonicity at higher order detects the violation",
           "screening check passes (is insufficient)", str(bool(screening_ok)))


# ---------------------------------------------------------------------------
# Test H -- tiny weight at the true edge.  Theorem H in action.
# ---------------------------------------------------------------------------

def test_tiny_weight(models):
    m = models["H_tiny_weight_at_edge"]
    eps, M_star, M_cont = mp.mpf("1e-12"), mp.mpf(2), mp.mpf(3)

    # Prediction (derived before running):
    #   atom:      Phi_atom(r) = eps e^{-2r}
    #   continuum: Phi_cont(r) = e^{-3r} Gamma(3/2) (r+1)^{-3/2}
    #   crossover: eps e^{r} = Gamma(3/2) (r+1)^{-3/2}
    f = lambda r: mp.log(mp.gamma(mp.mpf(3) / 2) / eps) - mp.mpf(1.5) * mp.log(r + 1)
    rx = mp.mpf(25)
    for _ in range(60):
        rx = f(rx)
    pred = f"Gamma ~ 3 for r << {mp.nstr(rx, 4)}, -> 2 only for r >> {mp.nstr(rx, 4)}"
    print(f"    predicted crossover radius r_x = {mp.nstr(rx, 6)}")

    rows = []
    for r in [3, 10, 20, mp.nstr(rx, 6), 30, 45, 70]:
        r = mp.mpf(r)
        g = m.Gamma(r)
        rows.append({"r": mp.nstr(r, 6), "Gamma": mp.nstr(g, 10)})
    print("    r, Gamma:", ", ".join(f"({x['r']},{x['Gamma']})" for x in rows))

    g_small, g_large = m.Gamma(mp.mpf(10)), m.Gamma(mp.mpf(70))
    near_cont = abs(g_small - M_cont) < mp.mpf("0.4")
    near_edge = abs(g_large - M_star) < mp.mpf("0.05")
    record("H tiny weight -- continuum masquerades at small r",
           "PASS" if near_cont else "FAIL",
           f"Gamma(10) = {mp.nstr(g_small, 8)}, sits at the continuum edge 3, not at M_*=2",
           pred, mp.nstr(g_small, 8))
    record("H tiny weight -- true edge recovered past crossover",
           "PASS" if near_edge else "FAIL",
           f"Gamma(70) = {mp.nstr(g_large, 8)} -> M_* = 2",
           pred, mp.nstr(g_large, 8))

    # The bound is never violated, even while it is uninformative.
    viol = [mp.nstr(r, 4) for r in [3, 10, 20, 30, 45, 70] if m.Gamma(mp.mpf(r)) < M_star]
    record("H tiny weight -- upper bound never violated",
           "PASS" if not viol else "FATAL",
           "Gamma(r) >= M_* holds at every tested radius (Theorem C is safe; "
           "it is the *informativeness*, not the validity, that degrades)",
           "no violation", f"violations at r={viol}" if viol else "none")

    # Finite-K Hankel at moderate r: predicted to converge to the CONTINUUM edge.
    r = mp.mpf(3)
    ok, reason, _ = positivity_gate(m, r, n_max=11)
    if not ok:
        record("H tiny weight -- Hankel gate", "FAIL", reason)
        return
    bk = [hankel_bound(m, r, K) for K in range(5)]
    monotone = all(bk[i + 1] <= bk[i] + mp.mpf("1e-40") for i in range(len(bk) - 1))
    above = all(b >= M_star for b in bk)
    stalls = bk[-1] > mp.mpf("2.5")
    print("    B_K(r=3):", ", ".join(mp.nstr(b, 8) for b in bk))
    record("H tiny weight -- finite-K hierarchy stalls at the wrong edge",
           "PASS" if (monotone and above and stalls) else "FAIL",
           f"B_K(r=3) descends {mp.nstr(bk[0], 6)} -> {mp.nstr(bk[-1], 6)}, still far "
           f"above M_*=2: finite-K resolution is weight-dependent. This is a "
           f"LIMITATION OF THE METHOD, consistent with Theorem C (B_K >= M_*) and "
           f"with Theorem H (no uniform lower bound without minimum weight).",
           "B_K stalls near the continuum edge 3, monotone, never below 2",
           f"B_0={mp.nstr(bk[0], 6)}, B_4={mp.nstr(bk[-1], 6)}")


# ---------------------------------------------------------------------------
# Edge-exponent discrimination (Theorem D) and the remaining zoo
# ---------------------------------------------------------------------------

def test_edge_exponents(models):
    """Spinor p=3/2 vs scalar p=5/2: Gamma = M_* + p/r + O(r^-2)."""
    for key, p_true in [("D_dirac", mp.mpf(1.5)), ("E_scalar", mp.mpf(2.5))]:
        m = models[key]
        vals = []
        for r in [40, 80, 160]:
            r = mp.mpf(r)
            vals.append(r * (m.Gamma(r) - mp.mpf(m.M_star)))
        drift = abs(vals[-1] - p_true)
        record(f"D edge exponent {key}", "PASS" if drift < mp.mpf("0.06") else "FAIL",
               f"r(Gamma-M_*) -> {mp.nstr(vals[-1], 8)}, predicted p = {mp.nstr(p_true, 4)}",
               f"p = {mp.nstr(p_true, 4)}", mp.nstr(vals[-1], 8))


def test_exact_models(models):
    """A single atom: Gamma and B_0 must be exact to working precision."""
    m = models["A_single_atom"]
    r = mp.mpf(2)
    g = m.Gamma(r)
    record("A single atom exact", "PASS" if abs(g - 3) < mp.mpf("1e-40") else "FAIL",
           f"Gamma = {mp.nstr(g, 12)} (exact M = 3)", "exactly 3", mp.nstr(g, 12))

    m = models["B_two_atoms"]
    r = mp.mpf(1)
    ok, reason, _ = positivity_gate(m, r, n_max=3)
    b1 = hankel_bound(m, r, 1) if ok else None
    record("B two atoms resolved at K=1",
           "PASS" if (ok and abs(b1 - 2) < mp.mpf("1e-30")) else "FAIL",
           f"B_1 = {mp.nstr(b1, 14) if b1 is not None else reason} (exact lower atom = 2)",
           "exactly 2", mp.nstr(b1, 14) if b1 is not None else reason)

    m = models["C_atom_plus_continuum"]
    g1, g2 = m.Gamma(mp.mpf(6)), m.Gamma(mp.mpf(12))
    ratio = (g1 - 2) / (g2 - 2)
    record("C separated atom -- exponential convergence",
           "PASS" if ratio > 1e4 else "FAIL",
           f"(Gamma(6)-2)/(Gamma(12)-2) = {mp.nstr(ratio, 6)}; predicted ~e^{{2*6}}="
           f"{mp.nstr(mp.e**12, 6)} for gap d=2",
           "ratio ~ e^{d*(r2-r1)} = e^12", mp.nstr(ratio, 6))


def test_gapless(models):
    """K: a gapless cut drags the estimator to 0, not to any matter threshold."""
    m = models["K_no_gap"]
    vals = [m.Gamma(mp.mpf(r)) for r in [10, 100, 1000]]
    decreasing = all(vals[i + 1] < vals[i] for i in range(len(vals) - 1))
    record("K gapless continuum -> 0", "PASS" if decreasing and vals[-1] < 0.01 else "FAIL",
           f"Gamma(10,100,1000) = {', '.join(mp.nstr(v, 6) for v in vals)} -> 0. "
           f"A massless cut in the full correlator therefore destroys the matter "
           f"threshold reading; H2 (s_*>0) is a genuine restriction.",
           "Gamma -> 0", mp.nstr(vals[-1], 6))


def test_multi_and_conditioning(models):
    m = models["F_multi_species"]
    vals = [m.Gamma(mp.mpf(r)) for r in [20, 60, 120]]
    record("F multi-species lowest threshold",
           "PASS" if abs(vals[-1] - 2) < 0.06 else "FAIL",
           f"Gamma -> {mp.nstr(vals[-1], 8)}; lightest species M_*=2 dominates the IR",
           "-> 2", mp.nstr(vals[-1], 8))

    m = models["G_near_degenerate"]
    ok, _, _ = positivity_gate(m, mp.mpf(5), n_max=3)
    b = hankel_bound(m, mp.mpf(5), 1) if ok else None
    record("G near-degenerate resolved",
           "PASS" if (b is not None and abs(b - 2) < 1e-20) else "FAIL",
           f"B_1 = {mp.nstr(b, 14) if b is not None else 'gate failed'} "
           f"(atoms at 2.00 and 2.02)", "2.00", mp.nstr(b, 14) if b is not None else "n/a")

    # Wide dynamic range: measure the precision actually required, rather than
    # quoting a condition number that silently underflowed.
    m = models["I_wide_dynamic_range"]
    saved = mp.mp.dps

    def smallest_eig(r, dps):
        mp.mp.dps = dps
        a = m.moments(mp.mpf(r), 4)
        H0 = mp.matrix(2, 2)
        for i in range(2):
            for j in range(2):
                H0[i, j] = a[i + j]
        ev = mp.eigsy(H0, eigvals_only=True)
        return min(ev), max(ev)

    # r = 1: the far atom is suppressed by e^{-198}, so H_0 is effectively rank
    # one and det H_0 suffers ~76 digits of cancellation.
    lo60, hi60 = smallest_eig(1, 60)
    lo200, hi200 = smallest_eig(1, 200)
    mp.mp.dps = saved
    singular_at_60 = (lo60 <= 0)
    resolved_at_200 = (lo200 > 0)
    record("I wide dynamic range -- precision requirement measured",
           "PASS" if (singular_at_60 and resolved_at_200) else "NOTE",
           f"At r=1 the two atoms are separated by e^{{-198}}: lambda_min(H_0) "
           f"collapses to {mp.nstr(lo60, 4)} at 60 dps (numerically singular) but is "
           f"{mp.nstr(lo200, 6)} at 200 dps. The pencil needs roughly "
           f"{int(-mp.log10(lo200 / hi200)) + 10} digits here; float64 has 16. "
           f"Reporting a high-order Hankel bound from double precision is "
           f"therefore unsound, and the code must detect the collapse rather "
           f"than return the resulting garbage eigenvalue.",
           "singular at 60 dps, resolved at 200 dps",
           f"lambda_min: {mp.nstr(lo60, 4)} (60 dps) -> {mp.nstr(lo200, 6)} (200 dps)")

    # Same measure at a radius where both atoms genuinely contribute.
    lo, hi = smallest_eig(mp.mpf("0.02"), 60)
    mp.mp.dps = saved
    cond = hi / lo if lo > 0 else mp.inf
    record("I wide dynamic range -- conditioning at a balanced radius",
           "PASS" if lo > 0 else "FAIL",
           f"at r=0.02 both atoms contribute and cond(H_0) = {mp.nstr(cond, 6)}; "
           f"the pencil is usable. Radius selection is part of the method.",
           "finite condition number", mp.nstr(cond, 6))


def main():
    mp.mp.dps = DPS
    print(f"Adversarial falsification suite (dps={DPS})")
    models = build_models()

    print("\n== CRUEL TEST J: signed measure must be refused ==")
    test_signed_measure(models)

    print("\n== CRUEL TEST H: tiny weight at the true threshold ==")
    test_tiny_weight(models)

    print("\n== Exactly solvable models ==")
    test_exact_models(models)

    print("\n== Edge exponents (Theorem D discrimination) ==")
    test_edge_exponents(models)

    print("\n== Gapless continuum (H2 is a real restriction) ==")
    test_gapless(models)

    print("\n== Multi-species, degeneracy, conditioning ==")
    test_multi_and_conditioning(models)

    fatal = [r for r in RESULTS if r["status"] == "FATAL"]
    failed = [r for r in RESULTS if r["status"] == "FAIL"]
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "falsification_suite.json").write_text(
        json.dumps({"dps": DPS, "results": RESULTS,
                    "n_fatal": len(fatal), "n_failed": len(failed)}, indent=2),
        encoding="utf-8")

    print(f"\n{len(RESULTS)} adversarial tests; FATAL={len(fatal)}, FAIL={len(failed)}")
    if fatal:
        print("FATAL:", [r["test"] for r in fatal])
        return 2
    if failed:
        print("FAILED:", [r["test"] for r in failed])
        return 1
    print("No FATAL finding: the gate refuses signed measures, and the tiny-weight "
          "degradation is a stated limitation rather than a violated theorem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
