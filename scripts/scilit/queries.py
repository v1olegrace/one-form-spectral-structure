"""Query registry: the vocabulary of the search, organised by round.

THE CENTRAL METHODOLOGICAL POINT
--------------------------------
Searching for our own words finds only people who chose our words.  The real
priority risk is THE SAME MATHEMATICAL STRUCTURE UNDER A DIFFERENT NAME.  The
object in question is

    Phi(r) = int_{M_*}^inf e^{-r x} dnu(x),   dnu >= 0,

i.e. a completely monotone function whose Laplace support edge we want to
recover from samples.  That object is standard equipment in at least six
communities, each with its own vocabulary:

    hep-th / lattice   "spectral representation", "effective mass", "GEVP"
    QED                "Uehling", "vacuum polarization", "dispersion relation"
    classical analysis "completely monotone", "Bernstein", "Stieltjes"
    moment theory      "Hausdorff moment problem", "Hankel", "Pade"
    approximation      "Schoenberg", "radial positive definite", "kernel"
    inverse problems   "multi-exponential fitting", "Prony", "relaxation
                       spectrum", "inverse Laplace transform", "NMR T2"

A query family is recorded with every result, so the saturation curve can be
reported honestly as "saturated UNDER THESE FAMILIES" rather than the much
stronger and unearned "the literature contains nothing else".
"""

from __future__ import annotations

# Each entry: (family, cluster, query). Cluster keys are defined in db.CLUSTERS.

# ---------------------------------------------------------------------------
# ROUND 1 -- PRIORITY ZERO. P0.1 = H3: has anyone already established a positive
# spectral (Stieltjes) representation for the gauge-invariant static response?
# ---------------------------------------------------------------------------
R1_H3 = [
    ("H3.static_spectral", "G", "spectral representation of the static quark potential"),
    ("H3.static_spectral", "G", "Kallen-Lehmann representation static potential gauge theory"),
    ("H3.static_spectral", "G", "dispersion relation for the heavy quark static potential"),
    ("H3.static_spectral", "G", "Wilson loop spectral decomposition transfer matrix positivity"),
    ("H3.positivity", "G", "reflection positivity constraints on the static potential"),
    ("H3.positivity", "G", "concavity convexity of the static quark antiquark potential"),
    ("H3.positivity", "G", "positivity of the static potential derivatives lattice"),
    ("H3.vp_positivity", "F", "positivity of the vacuum polarization spectral function"),
    ("H3.vp_positivity", "F", "Uehling potential superposition of Yukawa potentials"),
    ("H3.vp_positivity", "F", "Wichmann-Kroll vacuum polarization potential"),
    ("H3.vp_positivity", "F", "spectral representation of the photon propagator positivity"),
    ("H3.screening", "G", "charge screening function spectral representation gauge theory"),
    ("H3.running_coupling", "F", "analytic properties of the running coupling spectral density"),
]

# ---------------------------------------------------------------------------
# ROUND 2 -- CROSS-DOMAIN. The highest-yield round: same mathematics, other words.
# ---------------------------------------------------------------------------
R2_CROSS = [
    ("CM.classical", "A", "completely monotone functions Bernstein Widder representation"),
    ("CM.classical", "A", "Stieltjes function complete monotonicity characterization"),
    ("CM.potential", "X", "completely monotone radial kernel positive definite Schoenberg"),
    ("CM.potential", "X", "superposition of Yukawa potentials positive measure"),
    ("CM.potential", "X", "Bernstein function screened Coulomb potential"),
    ("INV.exp", "H", "multi-exponential decay fitting resolution limit ill-posed"),
    ("INV.exp", "H", "inverse Laplace transform exponential sum ill-posedness"),
    ("INV.exp", "H", "Prony method exponential fitting noise sensitivity"),
    ("INV.relax", "X", "relaxation spectrum inversion rheology ill-posed"),
    ("INV.relax", "X", "NMR T2 relaxation inverse Laplace transform regularization"),
    ("INV.edge", "C", "estimating the support edge of a positive measure from Laplace transform"),
    ("INV.edge", "C", "recovering the smallest exponent from sampled exponential sums"),
    ("MOM.hankel", "B", "Hankel matrix positivity Hausdorff moment problem truncated"),
    ("MOM.hankel", "B", "truncated moment problem lower bound smallest support point"),
    ("MOM.pade", "D", "Pade approximants Stieltjes series convergence bounds"),
    ("MOM.pade", "D", "continued fraction Stieltjes moment problem quadrature bounds"),
]

# ---------------------------------------------------------------------------
# ROUND 3 -- the lattice threat (P0.2): effective mass / GEVP identity.
# ---------------------------------------------------------------------------
R3_LATTICE = [
    ("LAT.effmass", "E", "effective mass monotonic upper bound lowest energy lattice correlator"),
    ("LAT.effmass", "E", "variational method generalized eigenvalue problem lattice spectroscopy"),
    ("LAT.effmass", "E", "rigorous bound ground state energy Euclidean correlation function"),
    ("LAT.effmass", "E", "excited state contamination effective mass plateau"),
    ("LAT.spectral", "E", "spectral density reconstruction Euclidean correlator Backus-Gilbert"),
    ("LAT.spectral", "E", "Bayesian reconstruction of spectral functions lattice QCD"),
    ("LAT.string", "E", "static potential lattice string breaking threshold"),
]

# ---------------------------------------------------------------------------
# ROUND 4 -- threshold extraction from vacuum polarization moments (P0.3).
# ---------------------------------------------------------------------------
R4_THRESHOLD = [
    ("THR.moments", "F", "extracting resonance masses from vacuum polarization moments Pade"),
    ("THR.moments", "F", "Taylor coefficients of the vacuum polarization threshold determination"),
    ("THR.moments", "B", "moment based determination of the lowest mass in a spectral function"),
    ("THR.qcdsr", "F", "QCD sum rules lowest resonance mass bound moments"),
    ("THR.qcdsr", "F", "rigorous bounds on hadron masses from correlator moments"),
]

# ---------------------------------------------------------------------------
# ROUND 5 -- positivity bounds / EFT moments (P0.4), and generalized symmetry.
# ---------------------------------------------------------------------------
R5_EFT = [
    ("EFT.positivity", "I", "positivity bounds effective field theory dispersion moments"),
    ("EFT.positivity", "I", "arcs and moments positivity bounds Wilson coefficients"),
    ("EFT.bootstrap", "I", "S-matrix bootstrap positivity extremal spectral density"),
    ("SYM.oneform", "J", "one-form symmetry breaking gauge theory generalized global symmetry"),
    ("SYM.oneform", "J", "approximate higher form symmetry violation charge screening"),
    ("SYM.wgc", "J", "weak gravity conjecture tower species scale spectrum"),
]

# ---------------------------------------------------------------------------
# ROUND 6 -- precision/noise limits on the inverse problem (P0.5, P0.6).
# ---------------------------------------------------------------------------
R6_NOISE = [
    ("NOISE.cond", "H", "ill-conditioning Hankel matrix exponential sum condition number"),
    ("NOISE.cond", "H", "numerical stability of the Hausdorff moment problem"),
    ("NOISE.minimax", "H", "minimax rate estimation of support boundary deconvolution"),
    ("NOISE.minimax", "H", "optimal rates for recovering the smallest decay rate"),
    ("NOISE.precision", "H", "exponential analysis finite precision arithmetic limitations"),
]

ROUNDS = {
    1: ("P0.1 -- H3: prior positive spectral representation of a static response", R1_H3),
    2: ("CROSS-DOMAIN -- same mathematics, other vocabulary", R2_CROSS),
    3: ("P0.2 -- lattice effective mass / GEVP equivalence", R3_LATTICE),
    4: ("P0.3 -- threshold from vacuum-polarization moments", R4_THRESHOLD),
    5: ("P0.4 -- positivity bounds, EFT moments, generalized symmetry", R5_EFT),
    6: ("P0.5/P0.6 -- noise, conditioning and resolution limits", R6_NOISE),
}

# Seed works for citation snowballing. Identifier-first: every seed is addressed
# by DOI or arXiv id, never by a title string. A title seed already mis-resolved
# once in this project ("Pade Approximants" -> Basdevant 1968).
#
# EVERY DOI BELOW WAS RESOLVED AGAINST CROSSREF AND/OR INSPIRE BEFORE BEING
# WRITTEN HERE. An earlier version of this list carried
# "10.1016/0370-2693(86)91126-2" for Bachas, typed from memory; Crossref returns
# NOT FOUND for it. The correct record is Phys. Rev. D 33, 2723 (1986). That is
# exactly the failure mode the identifier-first rule exists to prevent, and it
# survived until INSPIRE was added -- general indexes resolve pre-1990 HEP badly.
SEEDS = [
    ("10.1103/PhysRevD.33.2723", "Bachas, concavity of the quarkonium potential (1986)"),
    ("10.1103/PhysRevD.18.482", "Seiler, upper bound on the color-confining potential (1978)"),
    ("10.1103/PhysRevD.20.3239", "Brown & Weisberger, static potential (1979)"),
    ("10.1103/PhysRev.48.55", "Uehling, polarization effects in the positron theory (1935)"),
    ("10.1103/PhysRev.101.843", "Wichmann & Kroll, strong Coulomb field (1956)"),
    ("10.1016/0550-3213(90)90540-T", "Luscher & Wolff, variational method (1990)"),
    ("10.1088/1126-6708/2009/04/094", "Blossier et al., GEVP (2009)"),
    ("10.1103/PhysRevD.80.094504", "Masjuan & Peris, Pade to vacuum polarization"),
    ("10.1007/JHEP02(2015)172", "Gaiotto-Kapustin-Seiberg-Willett, generalized symmetries"),
]

# INSPIRE recids for the same seeds, where INSPIRE is the canonical HEP record.
# Used for reference/citation traversal that DOI-based indexes cover poorly.
INSPIRE_SEEDS = [
    (218332, "Bachas (1986) concavity of the quarkonium potential"),
    (135816, "Seiler (1978) upper bound on the color-confining potential"),
    (141197, "Brown & Weisberger (1979) static potential in QCD"),
    (40014, "Uehling (1935) polarization effects in the positron theory"),
    (45608, "Wichmann & Kroll (1956) vacuum polarization in a strong Coulomb field"),
]

# ---------------------------------------------------------------------------
# EXTENDED AXES. These implement the search fronts that the keyword rounds above
# do not reach, and they are where the structural predecessors are most likely
# to be hiding. Three deserve comment:
#
#   I  (Prony / matrix pencil / ESPRIT) -- this signal-processing literature may
#      already contain exact finite-atom recovery and robustness theorems
#      strictly stronger than ours, stated for "modal analysis" rather than
#      spectral measures.
#   P  (Lasserre moment-SOS hierarchy) -- our Hankel hierarchy may be the
#      one-dimensional specialization of an existing general hierarchy.
#   K  (hidden spectral weight) -- the sharpest version of the question, and the
#      one that distinguishes three DIFFERENT thresholds that the paper has so
#      far conflated into one M_*:
#          M_strict           true inf supp nu
#          M_detectable(T,e)  recoverable from data on a window T at precision e
#          M_dominant         the edge that actually controls the observed decay
#      If that trichotomy is absent from the literature, it is a stronger and
#      more defensible contribution than threshold reconstruction per se.
# ---------------------------------------------------------------------------

R9_PRONY = [
    ("PRONY.core", "H", "Prony method matrix pencil exponential parameter estimation"),
    ("PRONY.core", "H", "ESPRIT algorithm frequency estimation subspace"),
    ("PRONY.core", "H", "generalized pencil of function method transient electromagnetic"),
    ("PRONY.recovery", "H", "super-resolution positive spike recovery total variation"),
    ("PRONY.recovery", "H", "Vandermonde decomposition Hankel low rank recovery"),
    ("PRONY.recovery", "H", "finite rate of innovation annihilating filter sampling"),
    ("PRONY.robust", "H", "matrix pencil perturbation theory noise exponential estimation"),
]

R10_MOMENT_OPT = [
    ("OPT.lasserre", "B", "Lasserre moment SOS hierarchy semidefinite relaxation support"),
    ("OPT.lasserre", "B", "localizing matrix truncated moment problem semidefinite"),
    ("OPT.christoffel", "B", "Christoffel function support estimation orthogonal polynomials"),
    ("OPT.jacobi", "G", "extreme zeros orthogonal polynomials smallest zero support endpoint"),
    ("OPT.jacobi", "G", "Gauss Radau quadrature bounds spectral endpoints Jacobi matrix"),
    ("OPT.canonical", "B", "canonical moments Krein moment problem Nevanlinna parametrization"),
]

R11_HIDDEN = [
    ("HID.mixture", "H", "detecting a small weight component exponential mixture identifiability"),
    ("HID.mixture", "H", "minimax support estimation mixture model separation"),
    ("HID.window", "C", "finite window nonidentifiability Laplace transform truncated data"),
    ("HID.window", "C", "resolution limit two close decay rates exponential analysis"),
    ("HID.lattice", "E", "small overlap ground state contamination variational lattice"),
    ("HID.dynamic", "H", "dynamic range limitation multiexponential decay number of components"),
]

R12_TAUBERIAN = [
    ("TAU.classic", "C", "Watson lemma Laplace method endpoint asymptotic expansion"),
    ("TAU.classic", "C", "Tauberian theorem Laplace transform Karamata regular variation"),
    ("TAU.mellin", "C", "Mellin transform asymptotics spectral density threshold behaviour"),
    ("TAU.edge", "C", "edge singularity spectral density Laplace transform asymptotics"),
]

R13_TILTING = [
    ("TILT.stat", "X", "exponential tilting Esscher transform cumulant generating function"),
    ("TILT.stat", "X", "logarithmic derivative Laplace transform mean variance tilted measure"),
    ("TILT.stat", "X", "large deviations Legendre transform cumulant generating function"),
]

R14_SIGNED = [
    ("SGN.tests", "B", "completely monotone sequences Hausdorff finite difference criterion"),
    ("SGN.tests", "B", "positive definite sequence Hankel determinant criterion signed measure"),
    ("SGN.tests", "B", "total positivity tests positivity certificates truncated moments"),
    ("SGN.tests", "A", "quasi-definite moment functional indefinite orthogonal polynomials"),
]

R15_ROBUST = [
    ("ROB.moment", "H", "noisy moment problem perturbation of the moment matrix error bounds"),
    ("ROB.moment", "H", "regularization truncated moment problem stability estimate"),
    ("ROB.pencil", "H", "pseudospectrum Hankel pencil conditioning generalized eigenvalue"),
]

R16_HISTORY = [
    ("HIST.qed", "F", "history of vacuum polarization coordinate space potential"),
    ("HIST.confine", "G", "correlation inequalities lattice gauge theory upper bound potential"),
    ("HIST.confine", "G", "Seiler bound confining potential linear rise upper bound"),
    ("HIST.cm", "A", "history completely monotone functions Hausdorff Bernstein moment"),
]

ROUNDS.update({
    9: ("EXT-I -- Prony / matrix pencil / ESPRIT (exact recovery, robustness)", R9_PRONY),
    10: ("EXT-P/G -- moment-SOS hierarchy, Christoffel, Jacobi endpoints", R10_MOMENT_OPT),
    11: ("EXT-K -- hidden spectral weight, M_strict vs M_detectable vs M_dominant", R11_HIDDEN),
    12: ("EXT-L -- Tauberian / Abelian / Mellin, the edge law's classical home", R12_TAUBERIAN),
    13: ("EXT-M -- exponential tilting: Gamma(r)=E_r[X], Gamma'(r)=-Var_r(X)", R13_TILTING),
    14: ("EXT-N -- signed measures and positivity certificates", R14_SIGNED),
    15: ("EXT-O -- robust / noisy moment problems, pencil perturbation theory", R15_ROBUST),
    16: ("EXT-hist -- historical lineage, pre-1990 literature", R16_HISTORY),
})

# ---------------------------------------------------------------------------
# Scoring. Weights are explicit and auditable rather than learned, so any
# reader can recompute a score by hand.
#
# WHY CONJUNCTIONS, NOT TERM DENSITY
# ----------------------------------
# A first version of this scorer summed isolated term weights.  It ranked
# "Analytical matrix elements of the Uehling potential in three-body systems"
# as the top novelty threat, because "Uehling" + "vacuum polarization" +
# "screening" happen to co-occur in atomic-physics precision calculations.
# Those papers threaten nothing here: they compute a known potential, they do
# not derive a spectral representation or a bound from one.
#
# The claims at issue all have the same shape:
#
#     SPECTRAL MACHINERY  applied to  A TARGET OBJECT  to obtain  A RESULT.
#
# So a work is a threat only when all three are present.  Term density inside
# one group is nearly worthless; co-occurrence ACROSS groups is the signal.
# ---------------------------------------------------------------------------

# (1) The mathematical machinery: Laplace/Stieltjes/moment structure.
STRUCTURE_TERMS = {
    "completely monotone": 40, "complete monotonicity": 40,
    "bernstein function": 35, "bernstein theorem": 30,
    "stieltjes": 28, "hausdorff moment": 35, "moment problem": 35,
    "hankel": 30, "hamburger": 30,
    "pade approximant": 28, "pade approximation": 28, "continued fraction": 20,
    "spectral representation": 26, "kallen-lehmann": 34, "källén-lehmann": 34,
    "spectral function": 20, "spectral density": 20,
    "dispersion relation": 22, "laplace transform": 24, "inverse laplace": 32,
    "exponential sum": 30, "multiexponential": 32, "multi-exponential": 32,
    "sum of exponentials": 30, "prony": 30, "relaxation spectrum": 26,
    "positive measure": 28, "positive definite": 20, "orthogonal polynomial": 22,
    "transfer matrix": 18, "reflection positivity": 30,
}

# (2) The object the machinery is applied to.
TARGET_TERMS = {
    "static potential": 38, "static quark": 32, "quark antiquark potential": 34,
    "wilson loop": 26, "heavy quark potential": 32,
    "effective mass": 32, "ground state energy": 28, "lowest state": 26,
    "lowest mass": 30, "mass gap": 26, "energy gap": 22,
    "threshold": 24, "lowest threshold": 34, "support": 18,
    "smallest exponent": 34, "decay rate": 20, "relaxation time": 20,
    "vacuum polarization": 24, "uehling": 20, "photon propagator": 22,
    "screening": 16, "running coupling": 20,
    "one-form symmetry": 34, "higher-form symmetry": 34,
    "correlation function": 18, "correlator": 20, "euclidean correlator": 32,
    "wilson coefficient": 24, "form factor": 16,
}

# (3) What is derived: a bound, a constraint, a reconstruction, a theorem.
RESULT_TERMS = {
    "rigorous bound": 34, "upper bound": 26, "lower bound": 26,
    "bound on": 22, "bounds on": 22, "inequality": 24, "inequalities": 24,
    "constraint": 20, "constraints": 20, "positivity bound": 34,
    "monotonic": 24, "monotonicity": 26, "convexity": 26, "concavity": 26,
    "variational": 20, "generalized eigenvalue": 34,
    "reconstruct": 24, "reconstruction": 24, "extraction": 20,
    "determination": 18, "estimate": 16, "estimation": 18,
    "necessary and sufficient": 30, "characterization": 22,
    "ill-posed": 28, "regularization": 22, "resolution limit": 32,
    "condition number": 26, "error bound": 30,
}

# Retained for backward compatibility with any caller expecting one table;
# the conjunction logic in score_threat() is what actually drives ranking.
THREAT_TERMS = {**STRUCTURE_TERMS, **TARGET_TERMS, **RESULT_TERMS}

# Terms indicating durable background value (foundational).
FOUND_TERMS = {
    "theorem": 8, "representation theorem": 20, "characterization": 10,
    "review": 12, "lecture notes": 10, "monograph": 14,
    "rigorous": 12, "proof": 8, "necessary and sufficient": 18,
}

# Terms indicating reusable method or code (implementation).
IMPL_TERMS = {
    "algorithm": 14, "numerical method": 14, "regularization": 12,
    "software": 16, "implementation": 10, "condition number": 14,
    "stability": 10, "error bound": 18, "interval arithmetic": 20,
    "arbitrary precision": 18, "reconstruction": 12,
}

# A work matching a cross-domain term gets a bonus: these are exactly the works
# that keyword-matching on our own vocabulary would have missed.
CROSS_DOMAIN_BONUS = {
    "nmr", "rheology", "relaxation", "geophysic", "chemometric",
    "signal processing", "spectroscopy", "fluorescence", "kinetics",
    "approximation theory", "spatial statistics", "random field",
    "renewal", "queueing", "reliability", "survival analysis",
}


def score_terms(text, table):
    """Sum weights for every term present. Returns (score, matched_terms)."""
    t = (text or "").lower()
    hits = [(term, w) for term, w in table.items() if term in t]
    return min(100, sum(w for _, w in hits)), [term for term, _ in hits]


def _best(text, table, k=2):
    """Strength of the k strongest matches from one group, plus the terms.

    Taking the best few rather than the sum stops a paper from scoring highly
    by repeating near-synonyms ("spectral function", "spectral density",
    "spectral representation") that carry one idea between them.
    """
    t = (text or "").lower()
    hits = sorted(((w, term) for term, w in table.items() if term in t),
                  reverse=True)
    return sum(w for w, _ in hits[:k]), [term for _, term in hits[:k]]


def score_threat(text):
    """Novelty threat as a CONJUNCTION across the three concept groups.

    Returns (score, matched_terms, groups_present).

    A work scores highly only when it brings spectral machinery TO a target
    object AND derives something.  Two groups is suggestive; one group is
    background vocabulary and is scored near zero.
    """
    s, st = _best(text, STRUCTURE_TERMS)
    g, gt = _best(text, TARGET_TERMS)
    r, rt = _best(text, RESULT_TERMS)

    groups = sum(x > 0 for x in (s, g, r))
    base = (s + g + r) / 3.0

    if groups == 3:
        mult = 1.30          # machinery + object + result: a genuine threat
    elif groups == 2:
        mult = 0.62          # suggestive, needs a human look
    else:
        mult = 0.22          # vocabulary overlap only

    # The strongest single signal available: an explicit complete-monotonicity
    # or moment-problem statement about a physical target. Nothing else in the
    # corpus means what this means.
    t = (text or "").lower()
    if groups >= 2 and any(k in t for k in
                           ("completely monotone", "complete monotonicity",
                            "moment problem", "bernstein function")):
        mult += 0.35

    return min(100, int(base * mult)), st + gt + rt, groups
