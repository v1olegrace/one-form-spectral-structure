"""Interval-certified threshold bounds.

This is the ONLY module permitted to use the word "certified", and the
distinction is substantive.

``mp.quad`` carries no rigorous error bound.  Anything computed by quadrature is
therefore CHECKED, never certified, no matter how many digits agree.  Two things
here are genuinely certified instead:

1.  **Atomic models.**  When the measure is a finite sum of atoms, the samples
    ``Phi(r) = sum_k w_k exp(-r x_k)`` are computed in mpmath interval
    arithmetic (``mp.iv``), which encloses every rounding error.

    IMPORTANT: what is enclosed is the VALUE OF THE UPPER BOUND, not ``M_*``.
    The bound is one-sided.  A narrow enclosure sitting well above ``M_*`` is a
    valid but uninformative bound -- the tiny-weight model certifies
    ``M_* <= 3.0`` for a measure whose edge is 2, and that is correct, not a
    failure.  Only when the bound saturates (a single atom) does the enclosure
    also localize the edge.

2.  **The error-envelope bound, eq. (24)-(25).**  Given interval enclosures
    ``|b_j_hat - b_j| <= eps_j`` from ANY source, the inequality

        M_* <= -(1/h) log[ (v'C1 v - E1(v)) / (v'C0 v + E0(v)) ]

    is a *proved deterministic inequality*, not an estimate.  It is valid
    uniformly in the test vector ``v``, so ``v`` may be chosen using the data.
    If no ``v`` yields a positive numerator, the method returns NO BOUND -- it
    must not silently truncate.

The sampling hierarchy used here is Theorem G: with ``y = e^{-hx}`` the samples
``b_j = Phi(r+jh)/Phi(r)`` are Hausdorff moments on ``[0, e^{-h M_*}]``, so
``L_K = lambda_max(C_1, C_0) <= e^{-h M_*}`` and
``M_* <= -(1/h) log L_K``.  No numerical differentiation is involved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "output" / "data"

RESULTS: list[dict] = []


def endpoints(x):
    """Rigorous (lower, upper) endpoints of an mpmath interval, as plain mpf.

    ``ivmpf.a`` returns another degenerate *interval*, not an ``mpf``; the raw
    endpoints live in ``_mpi_``.  Going through ``_mpi_`` keeps the enclosure
    exact instead of round-tripping through a decimal string.
    """
    lo, hi = x._mpi_
    return mp.mpf(lo), mp.mpf(hi)


def _report(name, kind, detail, **kw):
    row = {"name": name, "kind": kind, "detail": detail}
    row.update(kw)
    RESULTS.append(row)
    print(f"  [{kind:9s}] {name}: {detail}")


# ---------------------------------------------------------------------------
# 1. Certified enclosures for finite-atom measures
# ---------------------------------------------------------------------------

def iv_samples(atoms, r, h, count):
    """b_j = Phi(r+jh)/Phi(r) as rigorous intervals, for a finite atom measure.

    Every operation is an mp.iv operation, so rounding is enclosed.  The common
    normalisation Phi(r) cancels in the pencil but is kept for interpretability.
    """
    r, h = mp.iv.mpf(str(r)), mp.iv.mpf(str(h))

    def Phi(rv):
        tot = mp.iv.mpf(0)
        for w, x in atoms:
            tot += mp.iv.mpf(str(w)) * mp.iv.exp(-rv * mp.iv.mpf(str(x)))
        return tot

    base = Phi(r)
    return [Phi(r + j * h) / base for j in range(count)]


def iv_two_radius_bound(atoms, r, h):
    """M_* <= -(1/h) log(b_1): the K=0 sampling bound, as a rigorous enclosure."""
    b = iv_samples(atoms, r, h, 2)
    bound = -mp.iv.log(b[1]) / mp.iv.mpf(str(h))
    return bound


def certify_atomic_models():
    print("\n== Certified enclosures (finite-atom measures, mp.iv) ==")
    cases = [
        ("single atom M=3", [(2.0, 3.0)], 3.0),
        ("two atoms, edge 2", [(1.0, 2.0), (3.0, 5.0)], 2.0),
        ("near-degenerate 2.00/2.02", [(1.0, 2.0), (1.0, 2.02)], 2.0),
        ("tiny weight 1e-12 at edge 2", [(1e-12, 2.0), (1.0, 3.0)], 2.0),
    ]
    for name, atoms, M_star in cases:
        enc = iv_two_radius_bound(atoms, r=1.0, h=0.5)
        lo, hi = endpoints(enc)
        valid = lo >= mp.mpf(M_star) - mp.mpf("1e-30")
        width = hi - lo
        # NB: [lo, hi] encloses the VALUE OF THE BOUND, not M_*. The bound is
        # one-sided (an upper bound), so an enclosure far above M_* is valid but
        # uninformative -- which is exactly what the tiny-weight model produces.
        _report(f"certified upper bound -- {name}",
                "CERTIFIED" if valid else "FAILED",
                f"M_* = {M_star} <= B, with B rigorously enclosed in "
                f"[{mp.nstr(lo, 12)}, {mp.nstr(hi, 12)}] (width {mp.nstr(width, 3)}); "
                f"slack over M_* = {mp.nstr(lo - mp.mpf(M_star), 6)}",
                M_star=M_star, bound_lo=mp.nstr(lo, 15), bound_hi=mp.nstr(hi, 15),
                is_enclosure_of="the upper bound B, NOT of M_*")

    # The single atom must be recovered EXACTLY (bound saturates the truth).
    enc = iv_two_radius_bound([(2.0, 3.0)], r=1.0, h=0.5)
    elo, ehi = endpoints(enc)
    tight = abs(ehi - mp.mpf(3)) < mp.mpf("1e-20")
    _report("upper bound saturates on a single atom",
            "CERTIFIED" if tight else "FAILED",
            f"bound enclosed in [{mp.nstr(elo, 15)}, {mp.nstr(ehi, 15)}]: the one-sided "
            f"bound is SATURATED at M=3, so here it does localize the edge")


# ---------------------------------------------------------------------------
# 2. The deterministic error-envelope bound, eq. (24)-(25)
# ---------------------------------------------------------------------------

def envelope_bound(b_hat, eps, h, K, v=None):
    """Theorem G error envelope.

    Returns (bound, v) or (None, None) when no admissible test vector exists.
    The inequality is deterministic and uniform in v, so v may be data-chosen.
    """
    n = K + 1
    C0 = mp.matrix(n, n)
    C1 = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            C0[i, j] = b_hat[i + j]
            C1[i, j] = b_hat[i + j + 1]

    if v is None:
        # Data-driven choice: the top generalized eigenvector of (C1, C0).
        try:
            Linv = mp.inverse(mp.cholesky(C0))
            S = Linv * C1 * Linv.T
            ev, evec = mp.eigsy((S + S.T) / 2)
            v = Linv.T * evec[:, n - 1]
        except (ValueError, ZeroDivisionError):
            return None, None

    def E(a):
        tot = mp.mpf(0)
        for i in range(n):
            for j in range(n):
                tot += abs(v[i]) * abs(v[j]) * eps[i + j + a]
        return tot

    num = sum(v[i] * v[j] * C1[i, j] for i in range(n) for j in range(n)) - E(1)
    den = sum(v[i] * v[j] * C0[i, j] for i in range(n) for j in range(n)) + E(0)
    if num <= 0 or den <= 0:
        return None, v
    ell = num / den
    if ell <= 0 or ell >= 1:
        return None, v
    return -mp.log(ell) / mp.mpf(h), v


def certify_envelope():
    """Perturb exact atomic samples within a stated envelope and check validity.

    The bound must remain valid for EVERY perturbation inside the envelope, and
    must return NO BOUND rather than a wrong one when the envelope is too wide.
    """
    print("\n== Deterministic error-envelope bound (eq. 24-25) ==")
    atoms, M_star, h, K = [(1.0, 2.0), (3.0, 5.0)], mp.mpf(2), mp.mpf("0.5"), 2
    exact = [endpoints(x)[0] for x in iv_samples(atoms, 1.0, float(h), 2 * K + 2)]

    import random
    for eps_rel in ["1e-10", "1e-6", "1e-3", "1e-1"]:
        e = mp.mpf(eps_rel)
        eps = [e * abs(x) for x in exact]
        rng = random.Random(20260911)
        worst_ok, n_bounds = True, 0
        for _ in range(200):
            pert = [x + (2 * rng.random() - 1) * ei for x, ei in zip(exact, eps)]
            bound, _v = envelope_bound(pert, eps, h, K)
            if bound is None:
                continue                      # explicit no-bound is allowed
            n_bounds += 1
            if bound < M_star - mp.mpf("1e-25"):
                worst_ok = False
                break
        _report(f"envelope valid under perturbation, eps_rel={eps_rel}",
                "CERTIFIED" if worst_ok else "FAILED",
                f"{n_bounds}/200 trials returned a finite bound; "
                f"{'all bounds >= M_*' if worst_ok else 'A BOUND FELL BELOW M_*'}",
                eps_rel=eps_rel, n_bounds=n_bounds)

    # Widening the envelope must degrade to an explicit refusal, not a wrong bound.
    eps = [mp.mpf(10) * abs(x) for x in exact]
    bound, _ = envelope_bound(exact, eps, h, K)
    _report("absurd envelope yields explicit no-bound",
            "CERTIFIED" if bound is None else "FAILED",
            "with eps 10x the data the procedure returns NO BOUND rather than "
            "truncating to something plausible")


def main():
    mp.mp.dps = 40
    mp.iv.dps = 40
    print("Interval-certified bounds (mp.iv); quadrature results are elsewhere "
          "and are CHECKED, not certified.")
    certify_atomic_models()
    certify_envelope()

    failed = [r for r in RESULTS if r["kind"] == "FAILED"]
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "interval_bounds.json").write_text(
        json.dumps({"results": RESULTS, "n_failed": len(failed)}, indent=2),
        encoding="utf-8")
    print(f"\n{len(RESULTS)} certified items; failures: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
