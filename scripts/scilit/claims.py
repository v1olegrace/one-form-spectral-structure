"""Claim register and equation-level findings.

Every row here is the product of an actual read, with a locator.  The database
triggers refuse a strong relation without one, so nothing in this file can be
an impression dressed up as a finding.

The claim ids follow the master audit list (A-K), and are cross-referenced to
the existing `data/claims_matrix.csv` ids (C1-C8) where they correspond.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scilit import db as sdb  # noqa: E402

CLAIMS = [
    ("A", "Phi(r) = delta(r)/r^2 is the Laplace transform of a positive measure "
          "whose support edge is the lowest threshold of the charged sector "
          "(conditional on H3).", "PROVED_CONDITIONALLY", "Theorem A / eq. (1)"),
    ("B", "Complete monotonicity of Phi acts as an operational falsifier of H3.",
     "PROVED_CONDITIONALLY", "Theorem B"),
    ("C", "The logarithmic slope Gamma(r) = -d log Phi / dr is a monotone "
          "decreasing upper bound on the threshold M_*.", "CLASSICAL_APPLICATION",
     "Theorem C"),
    ("D", "Edge law Gamma(r) = M_* + p/r + beta p/r^2 + ...", "PROVED",
     "Theorem D"),
    ("E", "Hankel/Jacobi pencil hierarchy B_K(r) = lambda_min(H_1,H_0) gives a "
          "monotone improving bound on M_*.", "PROVED_CONDITIONALLY", "Theorem E"),
    ("F", "Sampled Hausdorff-Hankel hierarchy from Phi(r+jh) without numerical "
          "differentiation.", "PROVED", "Theorem F/G"),
    ("G", "Mellin bridge between the radial profile and inverse spectral moments.",
     "PROVED", "eq. (26)-(27)"),
    ("H", "Finite-window inability to resolve arbitrarily weak spectral weight "
          "below the dominant threshold; crossover radius r_x ~ log(1/eps)/(M-mu).",
     "PROVED_CONDITIONALLY", "Theorem H"),
    ("I", "Pole / pole+continuum / continuum edge morphology is distinguishable "
          "from the subleading edge law.", "PROVED_CONDITIONALLY", "Theorem I"),
    ("J", "The construction is an operational probe of approximate one-form "
          "symmetry restoration.", "CONJECTURE", "Discussion"),
    ("K", "What additional input is required for a WGC-like inference.",
     "CONJECTURE", "Discussion"),
]

# Equation-level findings. Each tuple:
#   (claim, work_id, relation, confidence, equation, theorem, evidence, notes)
#
# RELATION SEMANTICS (see db.RELATIONS):
#   IDENTICAL                -- same statement about the same object
#   STRICTLY_STRONGER_PRIOR  -- prior work proves more, or from weaker hypotheses
#   SPECIAL_CASE_PRIOR       -- prior work proves our statement in a special case
#   USES_SAME_MATH           -- same machinery, different object
#   SUPPORTS_ASSUMPTION      -- establishes a hypothesis we assume
FINDINGS = [
    # ---------------------------------------------------------------------
    # Raman 2026, "Lecture Notes on Positivity Properties of Scattering
    # Amplitudes", arXiv:2603.28454. READ AT EQUATION LEVEL.
    # ---------------------------------------------------------------------
    ("A", "arxiv:2603.28454v1", "SUPPORTS_ASSUMPTION", 9,
     "eq. (119)-(120)", "Sec. 3.3.1",
     "States and derives: 'If Pi(Q^2) is the vacuum polarization function then "
     "-Pi(Q^2)/Q^2 is a Stieltjes function.' Derivation is the once-subtracted "
     "Kallen-Lehmann dispersion relation eq. (119) "
     "Pi(q^2) = q^2 int_{s_thr}^inf rho(s)/(s(s-q^2)) ds, followed by u=1/s, "
     "Q^2=-q^2 giving eq. (120) Pi(Q^2) = -Q^2 int_0^{1/s_thr} rho(1/u)/(1+uQ^2) du, "
     "with rho(s)>=0 for s>=s_thr guaranteed by unitarity.",
     "DECISIVE FOR P0.1. The Stieltjes property of the ABELIAN vacuum "
     "polarization -- the analytic content of Corollary A1 -- is standard and is "
     "stated as a known result in a 2026 review. H3 must therefore NOT be "
     "presented as a new analytic structure at the VP level. What remains open "
     "is H3 for the NONPERTURBATIVE GAUGE-INVARIANT STATIC RESPONSE, which this "
     "reference does not address: it contains no static potential, no Wilson "
     "loop and no position-space potential."),

    # NOTE ON RELATION CHOICE. An earlier version of this file recorded Raman
    # as STRICTLY_STRONGER_PRIOR. That was wrong in an important way: Raman is
    # not the prior, Raman is a POINTER TO the prior. Eq. (19)-(22) is
    # Bernstein-Widder/Hausdorff (1920s-40s); eq. (120) is Kallen-Lehmann plus
    # a subtracted dispersion relation, standard since the 1950s-60s. Citing a
    # 2026 lecture note for either would be flagged by any referee. The relation
    # is therefore BACKGROUND_ONLY: the work ATTESTS CLASSICALITY, it does not
    # hold priority. references.bib must cite Widder and Kallen-Lehmann directly.
    ("B", "arxiv:2603.28454v1", "BACKGROUND_ONLY", 9,
     "eq. (19), (20)-(21), (22)", "Sec. 2.1.2",
     "Defines exactly our Hankel hierarchy from derivatives: "
     "(H_0)_ij = (-1)^(i+j) f^(i+j)(x), (H_1)_ij = (-1)^(i+j+1) f^(i+j+1)(x), "
     "and proves PSD via "
     "sum_ij (-1)^(i+j+l) f^(i+j+l)(x) xi_i xi_j "
     "= int_0^inf dt mu(t) e^(-xt) t^l (sum_i t^i xi_i)^2 >= 0. "
     "Eq. (22) is the 2x2 log-convexity determinant.",
     "The equivalence 'complete monotonicity <=> PSD Hankel matrices of "
     "derivatives' is classical and is presented as review material. Theorem B "
     "and the H_0/H_1 construction of Theorem E are therefore CLASSICAL as "
     "mathematics. Novelty cannot be claimed for the hierarchy itself."),

    ("E", "arxiv:2603.28454v1", "USES_SAME_MATH", 9,
     "eq. (19)", "Sec. 2.1.2",
     "Same H_0, H_1 pencil objects, same positivity proof.",
     "NOT identical: the review builds the Hankel matrices to CERTIFY complete "
     "monotonicity. It never forms the generalized eigenvalue problem "
     "lambda_min(H_1,H_0) and never extracts inf supp mu. The threshold-"
     "extraction step of Theorem E is absent here."),

    ("J", "arxiv:2603.28454v1", "CHALLENGES_ASSUMPTION", 8,
     "abstract, Sec. 3", None,
     "The programme 'CM/Stieltjes positivity as a property of QFT observables' "
     "is an established, actively reviewed research area covering the cusp "
     "anomalous dimension (eq. 99), scalar Feynman integrals (eq. 102, 114), "
     "the vacuum polarization (eq. 120) and Coulomb-branch amplitudes in N=4 SYM.",
     "Our framing cannot be presented as opening this programme. The defensible "
     "position is a NEW OBSERVABLE within an existing programme, not a new "
     "programme."),
]


# Works read at ABSTRACT level only. The relations below are deliberately the
# ones that do NOT require an equation locator, because no equations were read.
# Promoting any of these to IDENTICAL or STRICTLY_STRONGER_PRIOR requires the
# full text, and the database will refuse it until then.
ABSTRACT_FINDINGS = [
    ("E", "doi:10.48550/arxiv.2408.11766", "USES_SAME_MATH", 8, None, None,
     "Lawrence 2024: recasts spectral reconstruction from Euclidean correlators "
     "as a convex optimization problem and, via Lagrange duality, obtains bounds "
     "on arbitrary integrals of the spectral density from positivity alone. "
     "Bounds are stated to be 'information-theoretically complete': for any point "
     "within the bounds there exists a consistent spectral density.",
     "HIGH THREAT TO THEOREM E's OPTIMALITY, AND THE OBVIOUS ESCAPE DOES NOT "
     "WORK. It is tempting to reply that M_* is not a linear functional so the "
     "completeness claim does not reach it. But nu([M_*, M]) = int_{[0,M]} dnu "
     "IS linear, and bisecting on M answers 'is there weight below M', so a "
     "complete bound on linear functionals reaches the edge through a FAMILY of "
     "them. That escape will not survive a referee. Either read Lawrence at "
     "equation level and establish where the bisection actually degrades (the "
     "likely answer: the bound on nu([0,M]) becomes uninformative as M -> M_*, "
     "which is precisely the Theorem H resolution question), or remove every "
     "optimality-flavoured word about Theorem E."),

    ("C", "arxiv:2512.19594", "ANALOGOUS", 9, None, None,
     "Mutzel & Tilloy 2025: linear-programming extraction of the MASS GAP from a "
     "static EQUAL-TIME two-point function at spatial separation, by recasting "
     "Kallen-Lehmann inversion as convex optimization. Tested on 1+1d phi^4 with "
     "relativistic continuous matrix product states.",
     "CLOSEST PUBLISHED ANALOGUE TO THE CORE METHOD. Same input class (a static "
     "spatial correlator), same target (the mass gap / spectral edge), same "
     "hypothesis (positive Kallen-Lehmann density). Differs in algorithm (linear "
     "programming vs Hankel pencil) and in the error statement (a posteriori "
     "bound on correlator error vs our monotone deterministic bound). This is a "
     "stronger precedent than the lattice effective mass, because the geometry "
     "-- spatial separation rather than Euclidean time -- matches ours."),

    ("H", "doi:10.1088/0266-5611/24/4/045018", "BACKGROUND_ONLY", 7, None, None,
     "Pham Ngoc 2007/2008: minimax upper and lower bounds for estimating a "
     "compactly supported DENSITY from noisy moments (Hausdorff moment problem).",
     "DOES NOT PREEMPT THEOREM H. The estimand is the density, not the endpoint "
     "of the support. Relevant as the correct minimax framework to cite, and as "
     "evidence that the noisy Hausdorff problem has a developed statistical "
     "theory that our deterministic envelope should be compared against."),

    ("H", "doi:10.1063/1.2930799", "ANALOGOUS", 8, None, None,
     "Cover 2008: a hypothesis test in relaxation-spectrum space whose null is "
     "'there exists a relaxation spectrum with NO signal below 40 ms consistent "
     "with the observed T2 decay'. Applied to detecting the myelin signal in "
     "brain MRI.",
     "STRUCTURALLY THE TINY-ATOM QUESTION, posed as a falsifiable test, in the "
     "NMR/MRI literature since 2008. The CONCEPT of testing for undetectable "
     "spectral weight below a threshold is therefore NOT new. No closed-form "
     "detection limit is given, so the crossover law r_x ~ log(1/eps)/(M-mu) is "
     "not preempted in closed form -- but Theorem H must be framed as supplying "
     "the quantitative law for a known qualitative phenomenon."),
]


# ---------------------------------------------------------------------------
# THE CORRECTION THAT MATTERS MOST IN THIS FILE.
#
# An earlier draft of WHAT_IS_ACTUALLY_NEW.md claimed:
#
#   "In every other setting found in this search -- amplitudes, Feynman
#    integrals, lattice correlators -- positivity of the spectral measure is
#    guaranteed by unitarity and reflection positivity, so the hierarchy can
#    only ever confirm."
#
# THAT IS FALSE. Violation of reflection positivity in the Landau-gauge gluon
# propagator is a STANDARD CONFINEMENT DIAGNOSTIC: one computes the temporal
# Schwinger function, observes it go negative, and concludes the gluon is not a
# physical asymptotic state. Using spectral positivity as a falsifiable physical
# hypothesis tested on a Euclidean correlator is therefore established practice
# in exactly our field.
#
# The search missed it through a vocabulary inversion that this project's own
# saturation report warns about: every round searched for positivity
# CONSTRAINTS ("reflection positivity constraints on the static potential"),
# and none searched for positivity VIOLATION USED AS A DIAGNOSTIC. Round 18 was
# added to repair this.
# ---------------------------------------------------------------------------
POSITIVITY_VIOLATION_FINDINGS = [
    ("B", "doi:10.1103/physrevd.106.l011502", "CHALLENGES_ASSUMPTION", 9,
     None, None,
     "'Schwinger function, confinement, and positivity violation in pure gauge "
     "QED' (Phys. Rev. D 106, L011502). Positivity violation of the photon "
     "Schwinger function -- equivalently of the Kallen-Lehmann spectral density "
     "-- is used directly as a confinement diagnostic.",
     "REFUTES THE UNQUALIFIED FORM OF OUR STRONGEST NOVELTY CLAIM. Spectral "
     "positivity as a FALSIFIABLE hypothesis, tested on a Euclidean correlator "
     "of a gauge field, is established practice. The claim 'nobody else uses "
     "positivity as a falsifier' must be withdrawn. What survives is narrower "
     "and must be stated narrowly: the standard diagnostic is a SINGLE SIGN "
     "CHECK (does the Schwinger function go negative), whereas our gate is the "
     "full Hankel hierarchy, which rejects a signed measure that passes both "
     "Phi > 0 and -Phi' > 0 and would therefore survive the standard test."),
]


def load(con):
    for cid, text, status, loc in CLAIMS:
        con.execute("INSERT OR REPLACE INTO claims (claim_id, claim_text, status,"
                    " paper_location) VALUES (?,?,?,?)", (cid, text, status, loc))
    con.commit()


def record(con, findings=FINDINGS):
    """Insert findings. Fails loudly if a work was not actually read."""
    ok = fail = 0
    for cid, wid, rel, conf, eq, thm, ev, notes in findings:
        try:
            con.execute(
                "INSERT OR REPLACE INTO claim_work_relation (claim_id, work_id,"
                " relation, confidence, evidence, equation, theorem, notes)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (cid, wid, rel, conf, ev, eq, thm, notes))
            ok += 1
        except Exception as exc:   # noqa: BLE001 - we want the reason printed
            print(f"  REFUSED {cid} x {wid} [{rel}]: {exc}")
            fail += 1
    con.commit()
    return ok, fail


if __name__ == "__main__":
    con = sdb.connect()
    load(con)
    # The read must be recorded BEFORE the relation, or the trigger refuses it.
    con.execute("UPDATE relevance SET read_status='EQUATION_LEVEL_READ',"
                " access_note='arXiv HTML full text read' "
                "WHERE work_id='arxiv:2603.28454v1'")
    for wid in ("doi:10.48550/arxiv.2408.11766", "arxiv:2512.19594",
                "doi:10.1088/0266-5611/24/4/045018", "doi:10.1063/1.2930799"):
        con.execute("UPDATE relevance SET read_status='ABSTRACT_READ',"
                    " access_note='arXiv abstract page read; full text NOT read' "
                    "WHERE work_id=?", (wid,))
    con.commit()
    con.execute("UPDATE relevance SET read_status='ABSTRACT_READ',"
                " access_note='title+abstract via Crossref/OpenAlex; full text NOT read'"
                " WHERE work_id='doi:10.1103/physrevd.106.l011502'")
    con.commit()
    ok, fail = record(con)
    ok2, fail2 = record(con, ABSTRACT_FINDINGS)
    ok3, fail3 = record(con, POSITIVITY_VIOLATION_FINDINGS)
    ok2 += ok3; fail2 += fail3
    print(f"claims loaded: {len(CLAIMS)}; findings recorded: {ok + ok2}; "
          f"refused: {fail + fail2}")
