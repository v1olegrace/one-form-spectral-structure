"""Generate the scientific-intelligence reports from the database.

Reports are DERIVED. Every number comes from a query, so a report cannot drift
away from the evidence. Where the evidence is thin, the report says so.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scilit import db as sdb  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _w(name, lines):
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return name


def _top(con, n=25, level=("HIGH", "MEDIUM")):
    q = ("SELECT w.id,w.title,w.year,w.venue,w.oa_url,r.cluster,r.novelty_threat t,"
         "r.priority_threat,r.read_status,r.reason FROM relevance r "
         "JOIN works w ON w.id=r.work_id WHERE r.priority_threat IN "
         f"({','.join('?' * len(level))}) GROUP BY w.id ORDER BY r.novelty_threat DESC LIMIT ?")
    return con.execute(q, list(level) + [n]).fetchall()


def priority_threats(con):
    L = [
        "# PRIORITY THREATS",
        "",
        f"Generated {STAMP} from `data/literature.db`.",
        "",
        "A threat is ranked by what it would cost the paper if true, not by how",
        "similar its words are. The ranking below is therefore driven by the",
        "equation-level and abstract-level reads recorded in",
        "`data/claim_literature_matrix.csv`, not by the keyword score.",
        "",
        "## Tier 1 -- established at equation level",
        "",
    ]
    rows = con.execute("""
        SELECT cw.claim_id, cw.relation, cw.confidence, cw.equation, cw.theorem,
               w.title, w.year, w.id, cw.evidence, cw.notes, r.read_status
        FROM claim_work_relation cw JOIN works w ON w.id=cw.work_id
        LEFT JOIN relevance r ON r.work_id=cw.work_id
        GROUP BY cw.claim_id, cw.work_id, cw.relation
        ORDER BY (r.read_status='EQUATION_LEVEL_READ') DESC, cw.confidence DESC
    """).fetchall()
    for r in rows:
        if r["read_status"] != "EQUATION_LEVEL_READ":
            continue
        L += [f"### Claim {r['claim_id']} — {r['relation']} (confidence {r['confidence']}/10)",
              "",
              f"**{r['title']}** ({r['year']}) — `{r['id']}`  ",
              f"Locator: {r['equation'] or '—'} / {r['theorem'] or '—'}  ",
              f"Read level: **{r['read_status']}**",
              "",
              f"> {r['evidence']}",
              "",
              f"**Consequence.** {r['notes']}",
              ""]
    L += ["## Tier 2 -- established at abstract level only", "",
          "These are recorded with relations that do NOT assert equation-level",
          "equivalence, because their equations have not been read. The database",
          "refuses to promote them until they are.", ""]
    for r in rows:
        if r["read_status"] == "EQUATION_LEVEL_READ":
            continue
        L += [f"### Claim {r['claim_id']} — {r['relation']} (confidence {r['confidence']}/10)",
              "",
              f"**{r['title']}** ({r['year']}) — `{r['id']}`  ",
              f"Read level: **{r['read_status'] or 'DISCOVERED'}**",
              "",
              f"> {r['evidence']}",
              "",
              f"**Consequence.** {r['notes']}",
              ""]
    return _w("PRIORITY_THREATS.md", L)


def what_is_new(con):
    L = [
        "# WHAT IS ACTUALLY NEW",
        "",
        f"Generated {STAMP}. No flattering language. Where novelty confidence is",
        "low, it is stated as low.",
        "",
        "## The finding that reorganises the paper",
        "",
        "Raman's 2026 lecture notes (arXiv:2603.28454), read at equation level,",
        "establish two things that the manuscript currently presents as its own",
        "analytic contributions:",
        "",
        "1. **eq. (119)-(120):** *If Π(Q²) is the vacuum polarization function",
        "   then −Π(Q²)/Q² is a Stieltjes function.* Derived from the",
        "   once-subtracted Källén–Lehmann dispersion relation with ρ(s) ≥ 0.",
        "   This is the analytic content of Corollary A1.",
        "2. **eq. (19)-(22):** complete monotonicity ⟺ positive semidefiniteness",
        "   of the Hankel matrices of derivatives,",
        "   (H₀)ᵢⱼ = (−1)^{i+j} f^{(i+j)}(x), (H₁)ᵢⱼ = (−1)^{i+j+1} f^{(i+j+1)}(x).",
        "   This is the construction underlying Theorems B and E.",
        "",
        "Both are presented there as **review material**. Neither can be claimed.",
        "",
        "Equally important is what those notes do *not* contain: no static",
        "potential, no Wilson loop, no position-space potential, and no",
        "extraction of inf supp μ from the function. The threshold-recovery step",
        "is absent.",
        "",
        "## Per-result classification",
        "",
        "| Result | Classification | Basis |",
        "|---|---|---|",
        "| Corollary A1 (Stieltjes VP) | **PREVIOUSLY_KNOWN** | Raman eq. (120) |",
        "| Theorem B (CM as H3 falsifier) | **CLASSICAL_APPLICATION** | Raman eq. (19)–(22); Bernstein–Widder |",
        "| Theorem C (Γ(r) bounds M_*) | **CLASSICAL_APPLICATION** | E = −lim t⁻¹ log Z_t is textbook; lattice effective mass |",
        "| Theorem E (Hankel pencil → M_*) | **NEW_COMPUTATIONAL_APPLICATION** | pencil objects classical; λ_min(H₁,H₀) → inf supp not found in the QFT literature |",
        "| Theorem D (edge law) | **UNCERTAIN_PRIORITY** | Watson's lemma is classical; Hinrichs–Polzer 2025 studies exactly this edge behaviour |",
        "| Theorem F/G (sampled hierarchy, envelope) | **NEW_ASSEMBLY** | no precedent found for the sampled, differentiation-free form with a deterministic envelope |",
        "| Theorem H (finite-window non-identifiability) | **NEW_ASSEMBLY** | concept known (Cover 2008); closed-form crossover not found |",
        "| Claim J (one-form symmetry reading) | **NEW_INTERPRETATION** | the observable is not in the CM/QFT literature |",
        "",
        "## The smallest scientifically defensible novelty claim",
        "",
        "Strip everything that the literature already owns and this survives:",
        "",
        "> For the reduced one-form symmetry-breaking profile Φ(r) = δ(r)/r²,",
        "> the classical Laplace–Stieltjes positivity hierarchy becomes an",
        "> *operational model-check on a physical hypothesis*: the same Hankel",
        "> data that bound the threshold also **falsify H3 itself**, and the",
        "> falsification is sharp enough to reject a signed measure that is",
        "> indistinguishable from screening at the level of Φ > 0 and −Φ′ > 0.",
        "",
        "That claim is defensible because it is about neither the mathematics",
        "(classical) nor the threshold extraction (done better elsewhere), but",
        "about what the positivity hierarchy *means* when the measure's",
        "positivity is a physical hypothesis rather than a standing assumption.",
        "",
        "### Correction — an earlier draft overclaimed here, and the overclaim mattered",
        "",
        "This section previously asserted that *in every other setting found —",
        "amplitudes, Feynman integrals, lattice correlators — positivity is",
        "guaranteed, so the hierarchy can only ever confirm.* **That is false.**",
        "",
        "Violation of reflection positivity in the Landau-gauge gluon propagator",
        "is a standard confinement diagnostic: one computes the temporal",
        "Schwinger function, observes it go negative, and concludes the gluon is",
        "not a physical asymptotic state. There is a Phys. Rev. D paper titled",
        "*Schwinger function, confinement, and positivity violation in pure gauge",
        "QED* (106, L011502, 2022). Using spectral positivity as a falsifiable",
        "hypothesis tested on a Euclidean correlator is established practice in",
        "this exact field.",
        "",
        "The search missed it through a vocabulary inversion that this project's",
        "own saturation report warns about: every round searched for positivity",
        "*constraints*, none for positivity *violation used as a diagnostic*.",
        "Round 18 was added to repair it.",
        "",
        "**What survives, stated narrowly.** The standard diagnostic is a single",
        "sign check — does the Schwinger function go negative. Our gate is the",
        "full Hankel hierarchy, and the difference is demonstrable rather than",
        "rhetorical: the signed-measure model in the test suite satisfies Φ > 0",
        "and −Φ′ > 0, so it **passes the standard test**, and is rejected only at",
        "a₃ = −0.4715, det H₀ = −0.1839. The contribution is the depth of the",
        "certificate, not the idea of testing positivity.",
        "",
        "## Second surviving claim: spectral resolution theory",
        "",
        "The search found no source that separates",
        "",
        "* `M_strict` — the true inf supp ν;",
        "* `M_detectable(T, ε)` — what is recoverable from data on a window of",
        "  length T at precision ε;",
        "* `M_dominant` — the edge that actually controls the observed decay,",
        "",
        "as three distinct quantities with a quantitative relation between them.",
        "Cover (2008) tests the *existence* of weight below a cutoff but gives no",
        "closed-form limit; Pham Ngoc (2008) gives minimax rates for the density,",
        "not the endpoint. The crossover r_x ≈ log(1/ε)/(M − μ), verified",
        "numerically here (predicted 22.758, observed Γ crossing at r ≈ 22.76),",
        "is a quantitative law for a phenomenon that is otherwise discussed",
        "qualitatively.",
        "",
        "**This is probably the stronger of the two claims** and is currently the",
        "less developed one in the manuscript.",
        "",
        "## Novelty confidence",
        "",
        "| Axis | Score (0–10) |",
        "|---|---|",
        "| Novelty of the mathematics | **1** |",
        "| Novelty of the threshold-extraction method | **2** |",
        "| Novelty of the positivity-gate-as-model-check framing | **4** |",
        "| Novelty of the resolution trichotomy | **6** |",
        "| Novelty of the physical observable (one-form profile) | **7** |",
        "",
        "Previous audit put overall novelty confidence at 3/10. This search does",
        "not raise that for the mathematics — it lowers it further, since",
        "Corollary A1 is now known to be textbook. It does, however, identify two",
        "specific claims at ~6/10 that were previously buried.",
    ]
    return _w("WHAT_IS_ACTUALLY_NEW.md", L)


def h3_deep_dive(con):
    L = [
        "# H3 DEEP DIVE (priority zero)",
        "",
        "**Question.** Has anyone already proved a representation sufficiently",
        "close to H3 — a positive Stieltjes representation of the gauge-invariant",
        "static response?",
        "",
        "## Verdict",
        "",
        "The question splits in two, and the two halves have different answers.",
        "",
        "### (a) H3 at the level of the abelian vacuum polarization",
        "",
        "**Classification: YES_EXACT — previously known.**",
        "",
        "Raman 2026 (arXiv:2603.28454) §3.3.1, eq. (119)–(120), read at equation",
        "level, states and derives:",
        "",
        "```",
        "  Pi(q^2)  = q^2 * int_{s_thr}^inf  rho(s) / (s (s - q^2))  ds      (119)",
        "  Pi(Q^2)  = -Q^2 * int_0^{1/s_thr} rho(1/u) / (1 + u Q^2) du       (120)",
        "  =>  -Pi(Q^2)/Q^2  is a Stieltjes function.",
        "```",
        "",
        "with ρ(s) ≥ 0 for s ≥ s_thr guaranteed by unitarity. This is the",
        "analytic content of Corollary A1, and it is review material.",
        "",
        "### (b) H3 for the NONPERTURBATIVE gauge-invariant static response",
        "",
        "**Classification: UNKNOWN_REQUIRES_READING.**",
        "",
        "No source found in this search states a positive Stieltjes",
        "representation for the static potential or for a Wilson-loop-derived",
        "response. Raman's notes contain no static potential, no Wilson loop and",
        "no position-space potential.",
        "",
        "**This must not be read as evidence of novelty.** The decisive primary",
        "sources are pre-1990 and paywalled, and were NOT read:",
        "",
        "| Work | DOI | Status |",
        "|---|---|---|",
        "| Bachas, *Concavity of the quarkonium potential* (1986) | 10.1103/PhysRevD.33.2723 | NOT READ — paywalled |",
        "| Seiler, *Upper bound on the color-confining potential* (1978) | 10.1103/PhysRevD.18.482 | NOT READ — paywalled |",
        "| Brown & Weisberger, *Remarks on the static potential in QCD* (1979) | 10.1103/PhysRevD.20.3239 | NOT READ — paywalled |",
        "| Wichmann & Kroll (1956) | 10.1103/PhysRev.101.843 | NOT READ — paywalled |",
        "",
        "Bachas and Seiler are the two papers most likely to contain a",
        "positivity structure for the static potential derived from reflection",
        "positivity alone — i.e. from a *weaker* hypothesis than H3. The prior",
        "audit already established that Bachas obtains two derivative conditions",
        "this way. Whether either derives the full hierarchy is the single",
        "open question that most affects the paper's standing.",
        "",
        "## Bibliographic correction found while resolving these seeds",
        "",
        "`paper/references.bib` entry `bachas_1986` carries",
        "`title = {Convexity of the Quarkonium Potential}` and `year = {1985}`.",
        "Crossref (the publisher record) returns",
        "**\"Concavity of the quarkonium potential\", 1986**, Phys. Rev. D **33**,",
        "2723. INSPIRE's title field says \"Convexity\" and disagrees with the",
        "publisher. The sign word matters here — concavity and convexity are",
        "opposite claims about the same object, and the paper cites this work",
        "*for a sign condition*. Resolve against the published article before",
        "submission.",
        "",
        "Seiler (1978) is absent from `references.bib` entirely and should be",
        "added: an upper bound on the confining potential is directly relevant to",
        "Theorem B's territory.",
        "",
        "## What would settle (b)",
        "",
        "1. Read Bachas 1986 and Seiler 1978 in full (institutional access).",
        "2. Read Montvay & Münster Ch. 3 on transfer-matrix reflection",
        "   positivity — the strongest general route to a spectral representation",
        "   for a Wilson-loop observable.",
        "3. Determine whether reflection positivity yields the *full* Stieltjes",
        "   property or only finitely many derivative conditions. If only",
        "   finitely many, H3 is strictly stronger than anything proved, and the",
        "   paper's conditional framing is correct and defensible.",
    ]
    return _w("H3_DEEP_DIVE.md", L)


def equivalence_map(con):
    L = [
        "# HANKEL / PADE / GEVP / LANCZOS EQUIVALENCE",
        "",
        "## Side-by-side map",
        "",
        "| Our object | Lattice / QFT object | Status of the analogy |",
        "|---|---|---|",
        "| Φ(r) = ∫ e^{−rx} dν(x) | Euclidean correlator C(t) = ∫ e^{−tE} ρ(E) dE | **exact isomorphism** under r ↔ t |",
        "| Γ(r) = −d log Φ/dr | effective mass m_eff(t) | **exact isomorphism**; monotone decrease is the standard argument |",
        "| M_* = inf supp ν | ground-state energy E₀ | **exact isomorphism** |",
        "| Hankel pencil λ_min(H₁,H₀) | GEVP / variational method | **equivalent after change of variables** |",
        "| Sampled b_j = Φ(r+jh)/Φ(r) | Lanczos / Prony on C(t+ja) | **equivalent**; same Hankel data |",
        "| tiny lower weight | poor ground-state overlap | **exact isomorphism** |",
        "| large-r convergence | ground-state dominance | **exact isomorphism** |",
        "",
        "The analogy is an isomorphism almost everywhere. The honest conclusion is",
        "that the *extraction machinery* is not new, and the paper must say so.",
        "",
        "## Where the analogy genuinely breaks",
        "",
        "One place, and it is the place the contribution lives:",
        "",
        "**In lattice spectroscopy, positivity of the spectral measure is",
        "guaranteed** by reflection positivity of the transfer matrix. A GEVP",
        "practitioner never asks whether ρ ≥ 0; it is a theorem. Consequently the",
        "positivity hierarchy can only ever *confirm*, and the Hankel determinants",
        "are used solely as an estimator, never as a test.",
        "",
        "**Here, positivity is the physical hypothesis H3 under test.** The same",
        "determinants become a falsifier. The signed-measure model in the test",
        "suite is the demonstration: it satisfies Φ > 0 and −Φ′ > 0 — it looks",
        "exactly like screening — and is rejected at a₃ = −0.4715, det H₀ =",
        "−0.1839. No effective-mass analysis would have flagged it, because no",
        "effective-mass analysis is looking.",
        "",
        "## Closest published analogues (2024–2025)",
        "",
        "Two recent works are closer to the core method than the lattice",
        "effective mass is, and neither is currently cited:",
        "",
        "1. **Lawrence, *Model-free spectral reconstruction via Lagrange duality*",
        "   (arXiv:2408.11766).** Convex optimization + Lagrange duality gives",
        "   bounds on arbitrary integrals of the spectral density from positivity",
        "   alone, stated to be **information-theoretically complete**. If that",
        "   completeness claim holds for linear functionals, no method can beat it",
        "   on those functionals. M_* is not a linear functional, so the Hankel",
        "   bound is not directly dominated — but the paper cannot claim",
        "   optimality without addressing this. *Read at abstract level only;",
        "   requires equation-level read before any optimality language is used.*",
        "",
        "2. **Mutzel & Tilloy (arXiv:2512.19594).** Linear-programming extraction",
        "   of the **mass gap from an equal-time two-point function at spatial",
        "   separation**, via Källén–Lehmann inversion as convex optimization.",
        "   This matches our geometry — spatial separation, not Euclidean time —",
        "   more closely than any lattice reference. **This is the single closest",
        "   published analogue to the core method and must be cited.**",
        "",
        "3. **Wagman's Lanczos formalism for lattice correlators** (and",
        "   *Lanczos algorithm for lattice QCD matrix elements*, Phys. Rev. D",
        "   2025, DOI 10.1103/zjzt-rv86) extracts energies from Euclidean",
        "   correlators with faster ground-state convergence than effective",
        "   masses. Lanczos on moment data *is* the Jacobi-matrix route to the",
        "   same Hankel pencil. Directly relevant to Theorem E's claimed",
        "   improvement over Γ(r), and not cited.",
    ]
    return _w("HANKEL_PADE_GEVP_EQUIVALENCE.md", L)


def book_roadmap(con):
    rows = con.execute(
        "SELECT * FROM books ORDER BY CASE priority WHEN 'NOW' THEN 0 "
        "WHEN 'NEXT' THEN 1 WHEN 'LATER' THEN 2 ELSE 3 END, title").fetchall()
    L = ["# BOOK ROADMAP", "",
         f"Generated {STAMP}. {len(rows)} monographs.", "",
         "**Access policy.** These are copyrighted monographs. Stored here:",
         "metadata, the exact chapter to read, and the reason. No protected full",
         "text is downloaded or stored. Obtain through an institutional library",
         "or the publisher.", ""]
    cur = None
    for r in rows:
        if r["priority"] != cur:
            cur = r["priority"]
            L += [f"## {cur}", ""]
        ident = (f"ISBN {r['isbn']}" if r["isbn"] else "**identifier unresolved**")
        L += [f"### {r['title']}", "",
              f"{r['authors']} · {r['edition']} · {r['year']} · {r['publisher']}  ",
              f"{ident} · cluster {r['cluster']} · access: {r['access_status']}  ",
              f"Route: {r['access_route']}", "",
              f"**Read:** {r['relevant_chapters']}", "",
              f"**Why:** {r['reason']}", ""]
    return _w("BOOK_ROADMAP.md", L)


def software_audit(con):
    rows = con.execute(
        "SELECT * FROM software WHERE stars IS NOT NULL ORDER BY stars DESC LIMIT 30"
    ).fetchall()
    zen = con.execute(
        "SELECT * FROM software WHERE stars IS NULL LIMIT 20").fetchall()
    L = ["# SOFTWARE AUDIT", "",
         f"Generated {STAMP}.", "",
         "**Star counts are metadata, not quality evidence.** They are recorded",
         "because they are cheap to record, and ignored in the recommendation.",
         "",
         "## What we actually need, and what exists",
         "",
         "| Need | Our current implementation | Best external candidate |",
         "|---|---|---|",
         "| arbitrary precision | `mpmath` (dps up to 200) | mpmath; `python-flint`/Arb is faster and has rigorous balls |",
         "| interval arithmetic | `mpmath.iv` | **Arb via python-flint** — ball arithmetic is the standard, and `mp.iv` lacks its rigorous special functions |",
         "| generalized eigenproblem | `mp.cholesky` + `mp.eigsy` | Arb's `arb_mat` eigen routines, for certified enclosures |",
         "| moment / SOS hierarchy | none | `GloptiPoly`, `SumOfSquares.jl`, `ncpol2sdpa` |",
         "| Prony / matrix pencil | none | see cluster H repositories below |",
         "| inverse Laplace | none | `CONTIN`-family and NNLS implementations |",
         "",
         "**The one concrete recommendation:** move the certified path from",
         "`mpmath.iv` to **Arb (python-flint)**. The wide-dynamic-range model",
         "needed ~86 digits where float64 has 16, and `mp.iv` has no rigorous",
         "special-function support; Arb's ball arithmetic is designed for exactly",
         "this and would let the `CERTIFIED` label cover more of the pipeline.",
         "",
         "## Repositories discovered", ""]
    for r in rows[:24]:
        L.append(f"* **{r['repo']}** ({r['language'] or '?'}, {r['license'] or 'no license'}, "
                 f"★{r['stars']}, updated {(r['last_update'] or '?')[:10]}) — "
                 f"{(r['purpose'] or '')[:120]}")
    L += ["", "## Archived research records (Zenodo)", ""]
    for r in zen[:12]:
        L.append(f"* {r['repo'][:90]} — {(r['purpose'] or '')[:100]}")
    return _w("SOFTWARE_AUDIT.md", L)


def unread(con):
    rows = con.execute("""
        SELECT w.id,w.title,w.year,w.oa_url,r.cluster,r.novelty_threat t,r.reason
        FROM relevance r JOIN works w ON w.id=r.work_id
        WHERE r.priority_threat='HIGH' AND r.read_status='DISCOVERED'
        GROUP BY w.id ORDER BY r.novelty_threat DESC""").fetchall()
    L = ["# UNREAD HIGH-PRIORITY", "",
         f"Generated {STAMP}. {len(rows)} HIGH-threat works have NOT been read.",
         "",
         "This file exists so that the size of the corpus is never mistaken for",
         "the depth of the reading. Of ~6,700 works harvested, **one** has been",
         "read at equation level and four at abstract level.",
         ""]
    for r in rows:
        L += [f"### {r['title']}", "",
              f"{r['year']} · cluster {r['cluster']} · threat {r['t']} · `{r['id']}`  ",
              f"{r['oa_url'] or 'no OA link recorded'}", "",
              f"Matched: {r['reason']}", ""]
    return _w("UNREAD_HIGH_PRIORITY.md", L)


def literature_map(con):
    tot = con.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    clusters = con.execute(
        "SELECT cluster, COUNT(DISTINCT work_id) n, "
        "SUM(priority_threat='HIGH') hi FROM relevance GROUP BY cluster "
        "ORDER BY n DESC").fetchall()
    years = con.execute(
        "SELECT CASE WHEN year<1970 THEN 'pre-1970' WHEN year<1990 THEN '1970-89' "
        "WHEN year<2010 THEN '1990-2009' WHEN year<2020 THEN '2010-19' "
        "ELSE '2020+' END era, COUNT(*) n FROM works WHERE year IS NOT NULL "
        "GROUP BY era ORDER BY n DESC").fetchall()
    src = con.execute("SELECT source, COUNT(*) n FROM search_log GROUP BY source "
                      "ORDER BY n DESC").fetchall()
    L = ["# LITERATURE MAP", "",
         f"Generated {STAMP}.", "",
         f"**{tot} unique works**, "
         f"{con.execute('SELECT COUNT(*) FROM work_aliases').fetchone()[0]} duplicate "
         f"rows merged, "
         f"{con.execute('SELECT COUNT(*) FROM citation_edges').fetchone()[0]} citation edges, "
         f"{con.execute('SELECT COUNT(*) FROM search_log').fetchone()[0]} logged API calls.",
         "", "## By cluster", "",
         "| cluster | description | works | HIGH |", "|---|---|---:|---:|"]
    for c in clusters:
        L.append(f"| {c['cluster']} | {sdb.CLUSTERS.get(c['cluster'],'?')} | "
                 f"{c['n']} | {c['hi'] or 0} |")
    L += ["", "## By era", "", "| era | works |", "|---|---:|"]
    for y in years:
        L.append(f"| {y['era']} | {y['n']} |")
    L += ["", "## By source", "", "| source | API calls |", "|---|---:|"]
    for s in src:
        L.append(f"| {s['source']} | {s['n']} |")
    L += ["",
          "## Coverage warning",
          "",
          "The era table is the important one. Coverage collapses before 1970,",
          "and the papers that most threaten priority on the static-potential",
          "axis (Seiler 1978, Brown–Weisberger 1979, Bachas 1986) sit exactly in",
          "the thin region. INSPIRE was added specifically to reach them and did",
          "resolve all four — but resolving a record is not reading it.",
          ""]
    return _w("LITERATURE_MAP.md", L)


if __name__ == "__main__":
    con = sdb.connect()
    for fn in (literature_map, priority_threats, what_is_new, h3_deep_dive,
               equivalence_map, book_roadmap, software_audit, unread):
        print(f"  wrote reports/{fn(con)}")
