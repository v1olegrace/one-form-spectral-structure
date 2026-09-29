"""Spectral model zoo for falsification of the Laplace tomography.

Each model supplies a positive (or deliberately signed) measure ``nu`` on
``[0, inf)`` together with

    Phi(r)   = int e^{-rx} dnu(x)
    a_n(r)   = int x^n e^{-rx} dnu(x)          (= (-1)^n Phi^(n)(r))

and the *ground truth* ``M_star = inf supp nu``.

Design rules
------------
1.  Atoms are handled by explicit summation, never by a density formula.  This
    exercises the weighted-pushforward definition of ``nu`` (audit correction F)
    rather than assuming absolute continuity.
2.  Continuum pieces are integrated after the substitution
    ``x = edge + y^2/r`` with the common factor ``e^{-r*edge}`` removed *before*
    quadrature.  At large ``r`` the raw integral is ~e^{-160}; an absolute
    quadrature tolerance is then met with no relative accuracy whatsoever.
    Every model therefore returns ``exp(+r*edge) * a_n(r)`` internally and the
    scale is reinstated only in ratios, where it cancels exactly.
3.  Models flagged ``positive = False`` are deliberate counterexamples.
    The gate never reads that flag or the ground-truth edge. Some signed
    measures pass finite necessary conditions; the suite must distinguish
    that limitation from a missed violation of a condition it actually tests.

Nothing in this module is an interval certificate.  ``mp.quad`` carries no
rigorous error bound; results are CHECKED, not CERTIFIED.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import mpmath as mp


# ---------------------------------------------------------------------------
# Core representation
# ---------------------------------------------------------------------------

@dataclass
class Model:
    """A spectral measure: finitely many atoms plus continuum branches.

    atoms     : list of (weight, position).  Weights may be negative only when
                ``positive=False``.
    branches  : list of (edge, density, exponent_p) where ``density(x)`` is
                dnu/dx on [edge, inf) and ``exponent_p`` is the analytically
                known edge exponent ``p`` in dnu/dx ~ C (x-edge)^{p-1}, or None.
    M_star    : ground-truth inf supp nu.
    positive  : False marks a deliberately non-positive model.
    """

    name: str
    description: str
    atoms: list = field(default_factory=list)
    branches: list = field(default_factory=list)
    M_star: float = 0.0
    positive: bool = True
    edge_p: float | None = None      # edge exponent of the *lowest* branch
    note: str = ""

    # -- scaled moments ----------------------------------------------------
    def scaled_a(self, n, r):
        """Return e^{+r*M_star} * a_n(r).

        The common exponential is removed before quadrature; it cancels in every
        ratio the tomography forms (Gamma, B_K, sampling pencils).
        """
        r = mp.mpf(r)
        total = mp.mpf(0)
        shift = mp.mpf(self.M_star)
        for w, pos in self.atoms:
            pos = mp.mpf(pos)
            total += mp.mpf(w) * pos**n * mp.e ** (-r * (pos - shift))
        for edge, density, _p in self.branches:
            edge = mp.mpf(edge)
            pre = mp.e ** (-r * (edge - shift))

            def integrand(y, edge=edge, density=density, n=n, r=r):
                x = edge + y * y / r
                return 2 * y / r * x**n * mp.e ** (-y * y) * density(x)

            total += pre * mp.quad(integrand, [0, 1, 3, 8, mp.inf])
        return total

    def Phi_scaled(self, r):
        return self.scaled_a(0, r)

    def Gamma(self, r):
        """Gamma(r) = a_1/a_0; the e^{r M_star} factors cancel exactly."""
        return self.scaled_a(1, r) / self.scaled_a(0, r)

    def moments(self, r, count):
        return [self.scaled_a(n, r) for n in range(count)]

    # -- sampling (Theorem G) ---------------------------------------------
    def samples(self, r, h, count):
        """b_j = Phi(r+jh)/Phi(r), computed from scaled quantities.

        Phi(r+jh)/Phi(r) = e^{-jh M_star} * Phi_scaled(r+jh)/Phi_scaled(r).
        """
        base = self.Phi_scaled(r)
        out = []
        for j in range(count):
            out.append(
                mp.e ** (-mp.mpf(j) * mp.mpf(h) * mp.mpf(self.M_star))
                * self.Phi_scaled(mp.mpf(r) + j * mp.mpf(h)) / base
            )
        return out


# ---------------------------------------------------------------------------
# Densities
# ---------------------------------------------------------------------------

def dirac_density(m=1.0, q=1.0, g2=1.0):
    """dnu/dx for one weakly gauged Dirac fermion.

    rho_J(s) = q^2/(12 pi^2) (1 + 2m^2/s) sqrt(1 - 4m^2/s),  dnu = g^2 2x rho dx.
    Edge exponent: dnu/dx ~ C (x-2m)^{1/2}, i.e. p = 3/2.
    """
    m, q, g2 = mp.mpf(m), mp.mpf(q), mp.mpf(g2)

    def rho(x):
        s = x * x
        if s <= 4 * m**2:
            return mp.mpf(0)
        return q**2 / (12 * mp.pi**2) * (1 + 2 * m**2 / s) * mp.sqrt(1 - 4 * m**2 / s)

    return lambda x: g2 * 2 * x * rho(x)


def scalar_density(m=1.0, q=1.0, g2=1.0):
    """dnu/dx for one weakly gauged complex scalar.

    rho_J(s) = q^2/(48 pi^2) (1 - 4m^2/s)^{3/2}.
    Edge exponent: dnu/dx ~ C (x-2m)^{3/2}, i.e. p = 5/2.
    The different edge power from the Dirac case is the discriminating
    prediction of Theorem D: Gamma -> 2m + (5/2)/r instead of 2m + (3/2)/r.
    """
    m, q, g2 = mp.mpf(m), mp.mpf(q), mp.mpf(g2)

    def rho(x):
        s = x * x
        if s <= 4 * m**2:
            return mp.mpf(0)
        return q**2 / (48 * mp.pi**2) * (1 - 4 * m**2 / s) ** mp.mpf(1.5)

    return lambda x: g2 * 2 * x * rho(x)


def power_density(edge, C, p, decay=1.0):
    """C (x-edge)^{p-1} e^{-decay (x-edge)}: exact edge exponent p."""
    edge, C, p, decay = mp.mpf(edge), mp.mpf(C), mp.mpf(p), mp.mpf(decay)

    def d(x):
        t = x - edge
        if t <= 0:
            return mp.mpf(0)
        return C * t ** (p - 1) * mp.e ** (-decay * t)

    return d


# ---------------------------------------------------------------------------
# The zoo
# ---------------------------------------------------------------------------

def build_models():
    """Return the labelled battery.  Keys match the audit's test list A..N."""
    M = {}

    M["A_single_atom"] = Model(
        name="A single atom",
        description="dnu = Z delta(x-M). Phi = Z e^{-Mr} exactly.",
        atoms=[(2.0, 3.0)], M_star=3.0, edge_p=None,
        note="Gamma = M and B_K = M exactly for every K; the pencil is rank one "
             "so K>=1 is singular and must be rank-reduced, not reported.",
    )

    M["B_two_atoms"] = Model(
        name="B two atoms",
        description="dnu = delta(x-2) + 3 delta(x-5).",
        atoms=[(1.0, 2.0), (3.0, 5.0)], M_star=2.0,
        note="Exactly resolved at K=1; K>=2 singular.",
    )

    M["C_atom_plus_continuum"] = Model(
        name="C atom + separated continuum",
        description="atom at 2, continuum from 4; gap d=2 so Gamma-M_* = O(e^{-2r}).",
        atoms=[(1.0, 2.0)],
        branches=[(4.0, power_density(4.0, 1.0, 1.5), 1.5)],
        M_star=2.0,
        note="Exponential convergence branch of Theorem D.",
    )

    M["D_dirac"] = Model(
        name="D spinor QED continuum",
        description="one Dirac fermion, m=q=g=1; M_*=2m=2, edge exponent p=3/2.",
        branches=[(2.0, dirac_density(), 1.5)], M_star=2.0, edge_p=1.5,
        note="Gamma = 2m + 3/(2r) - 5/(16 m r^2) + 45/(32 m^2 r^3) + ...",
    )

    M["E_scalar"] = Model(
        name="E scalar QED continuum",
        description="one complex scalar, m=q=g=1; M_*=2, edge exponent p=5/2.",
        branches=[(2.0, scalar_density(), 2.5)], M_star=2.0, edge_p=2.5,
        note="Discriminates Theorem D: leading coefficient 5/2, not 3/2.",
    )

    M["F_multi_species"] = Model(
        name="F multiple charged species",
        description="Dirac m=1 plus Dirac m=1.7 plus scalar m=2.5.",
        branches=[(2.0, dirac_density(1.0), 1.5),
                  (3.4, dirac_density(1.7), 1.5),
                  (5.0, scalar_density(2.5), 2.5)],
        M_star=2.0, edge_p=1.5,
        note="Lowest threshold must still be recovered from the aggregate.",
    )

    M["G_near_degenerate"] = Model(
        name="G near-degenerate thresholds",
        description="atoms at 2.00 and 2.02 with comparable weights.",
        atoms=[(1.0, 2.0), (1.0, 2.02)], M_star=2.0,
        note="Tests resolution of closely spaced edges.",
    )

    # ---- CRUEL TEST 1 ----------------------------------------------------
    M["H_tiny_weight_at_edge"] = Model(
        name="H tiny weight at the true lowest threshold",
        description="dnu = 1e-12 delta(x-2) + continuum from 3.",
        atoms=[(1e-12, 2.0)],
        branches=[(3.0, power_density(3.0, 1.0, 1.5), 1.5)],
        M_star=2.0,
        note="inf supp nu = 2 exactly, but the dominant spectrum sits at 3. "
             "Gamma and the low-order pencils tested at moderate r stay near 3. "
             "Theorem H excludes uniform finite-precision recovery without "
             "extra information; it does not forbid recovery with sufficiently "
             "precise data, higher order or a correct parametric model.",
    )

    # ---- CRUEL TEST 2 ----------------------------------------------------
    M["J_signed_measure"] = Model(
        name="J signed measure (H3 violated)",
        description="dnu = delta(x-1) - 0.5 delta(x-2): NOT a positive measure.",
        atoms=[(1.0, 1.0), (-0.5, 2.0)], M_star=1.0, positive=False,
        note="Phi>0 and -Phi'>0 for all r>0, so a screening-only check passes. "
             "Complete monotonicity fails at order n once e^r < 2^{n-1}, and "
             "H_0 loses positive definiteness. The pipeline MUST refuse to "
             "report any B_K here.",
    )

    M["K_no_gap"] = Model(
        name="K gapless continuum (H2 violated)",
        description="dnu = e^{-x} dx from 0: M_* = 0, no positive gap.",
        branches=[(0.0, power_density(0.0, 1.0, 1.0), 1.0)],
        M_star=0.0, edge_p=1.0,
        note="Models the massless multi-photon cut. Gamma must descend to 0, "
             "not to any matter threshold.",
    )

    M["I_wide_dynamic_range"] = Model(
        name="I wide dynamic range",
        description="atoms at 2 and 200 with weights 1 and 1e6.",
        atoms=[(1.0, 2.0), (1e6, 200.0)], M_star=2.0,
        note="Conditioning stress test for the Hankel pencil.",
    )

    return M
