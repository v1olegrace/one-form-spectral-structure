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
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad
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


def kernel_diagnostic(g2, L2):
    """Model classification using ESTIMATED quadrature uncertainty, not a certificate.

    The analytic Dirac density at a finite cutoff verifies the listed model
    hypotheses. Rational endpoint arithmetic avoids additional rounding when
    propagating the reported quadrature error. It cannot make that error rigorous.
    A numerical g2_critical never asserts the exact identity Z3=0.
    """
    if not np.isfinite(g2) or g2 <= 0 or not np.isfinite(L2) or L2 <= S_THR:
        raise ValueError("require finite g2 > 0 and L2 > threshold")
    P, err = Pi_infinity(L2)
    g, p, e = map(Fraction, (float(g2), float(P), float(err)))
    diag = classify_rpa_kernel(
        (1 - g * (p + e), 1 - g * (p - e)),
        hypotheses=RPAHypotheses(
            nonnegative_measure=True, nonzero_measure=True, positive_support=True,
            finite_inverse_moment=True, positive_coupling=True,
            subtracted_dyson_representation=True),
        total_mass="finite", interval_kind="estimated")
    diag["model"] = "one-loop Dirac density, hard spectral cutoff, RPA"
    diag["quadrature_absolute_error_estimate"] = err
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
    z3 = Z3_of(g2, L2)
    if z3 >= 0.0:
        return None
    lo = 1e-6
    # W(0)=1>0 and W(inf)=Z3<0, so a bracket always exists when Z3<0.
    while W(hi, g2, L2) > 0 and hi < 1e300:
        hi *= 10.0
    return brentq(lambda q: W(q, g2, L2), lo, hi, rtol=1e-13, maxiter=300)


# --------------------------------------------------- continuum spectral density
def W_on_cut(s, g2, L2):
    """W(Q2 -> -s - i0) = 1 + g2 s PV int rho/(sig(sig-s)) dsig + i pi g2 rho(s)."""
    f = lambda sig: _rho_scalar(sig) / sig
    pv, _ = quad(f, S_THR, L2, weight='cauchy', wvar=s, limit=400,
                 epsabs=1e-12, epsrel=1e-11)
    return complex(1.0 + g2 * s * pv, np.pi * g2 * _rho_scalar(s))


def density(s, g2, L2):
    """dsigma/ds = (1/pi) Im G(-s - i0).  Should be >= 0 for every coupling."""
    Wc = W_on_cut(s, g2, L2)
    Gc = g2 / ((-s) * Wc)
    return Gc.imag / np.pi


def density_closed_form(s, g2, L2):
    """Hand-derived: g2^2 rho(s) / (s |W|^2).  Cross-check on `density`."""
    Wc = W_on_cut(s, g2, L2)
    return g2**2 * _rho_scalar(s) / (s * abs(Wc)**2)


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
