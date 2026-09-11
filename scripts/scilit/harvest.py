"""Round-based harvest driver with an honest saturation curve.

Pipeline per round:
    query family -> OpenAlex (+ arXiv / S2 cross-source) -> dedupe by canonical
    id -> score on four axes -> store -> record what was NEW.

Saturation is measured as "no new HIGH-relevance work appeared in the last N
rounds UNDER THE QUERY FAMILIES LISTED".  That qualifier is not decoration: a
keyword-driven search saturates when the QUERY VOCABULARY is exhausted, which
is a strictly weaker statement than the literature being exhausted.  The
citation-snowball rounds exist precisely because they discover works whose
vocabulary we never guessed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scilit import db as sdb            # noqa: E402
from scilit import queries as q         # noqa: E402
from scilit import sources as src       # noqa: E402


def classify(rec, cluster):
    """Four-axis score from title+abstract+venue. Transparent and recomputable."""
    text = " ".join(filter(None, [rec.get("title"), rec.get("abstract"),
                                  rec.get("venue")]))
    threat, tterms, groups = q.score_threat(text)
    found, _ = q.score_terms(text, q.FOUND_TERMS)
    impl, _ = q.score_terms(text, q.IMPL_TERMS)

    low = text.lower()
    cross = any(term in low for term in q.CROSS_DOMAIN_BONUS)
    if cross and groups >= 2:
        # A structural match from another field is the scenario we are least
        # likely to find by any other route, so it is boosted -- but only when
        # the structural conjunction is actually present. Otherwise "NMR" alone
        # would promote every unrelated spectroscopy paper.
        threat = min(100, threat + 15)

    score = min(100, int(0.55 * threat + 0.25 * found + 0.20 * impl))
    if threat >= 55:
        level = "HIGH"
    elif threat >= 33:
        level = "MEDIUM"
    else:
        level = "LOW"

    reason = (f"[{groups}/3 groups] " +
              (", ".join(tterms[:8]) if tterms else "no concept terms matched"))
    if cross:
        reason += " [CROSS-DOMAIN]"
    return {
        "score": score, "level": level, "novelty_threat": threat,
        "foundational_value": found, "implementation_value": impl,
        "reading_priority": min(100, int(0.6 * threat + 0.4 * found)),
        "reason": reason, "cross_domain": cross,
        "equation_level_required": int(threat >= 55),
    }


def store(con, rec, cluster, round_no, family):
    """Insert a normalized record. Returns (work_id, is_new, level)."""
    wid = sdb.canonical_id(doi=rec.get("doi"), arxiv=rec.get("arxiv_id"),
                           isbn=rec.get("isbn"), openalex=rec.get("openalex_id"),
                           title=rec.get("title"))
    payload = {k: v for k, v in rec.items() if not k.startswith("_")}
    payload["id"] = wid
    payload.setdefault("discovered_round", round_no)
    payload["discovered_via"] = f"{family}|{rec.get('discovered_via','')}"[:200]
    # upsert may redirect to a canonical row after de-duplication, so the id it
    # returns -- not the one computed above -- is the valid foreign key.
    wid, is_new = sdb.upsert_work(con, **payload)

    c = classify(rec, cluster)
    existing = con.execute(
        "SELECT score FROM relevance WHERE work_id=? AND cluster=?",
        (wid, cluster)).fetchone()
    if existing is None or c["score"] > existing["score"]:
        sdb.set_relevance(con, wid, cluster, c["score"], c["reason"],
                          priority_threat=c["level"],
                          novelty_threat=c["novelty_threat"],
                          foundational_value=c["foundational_value"],
                          implementation_value=c["implementation_value"],
                          reading_priority=c["reading_priority"],
                          equation_level_required=c["equation_level_required"])
    return wid, is_new, c["level"]


def run_round(con, round_no, cross_sources=True, verbose=True):
    """Execute one keyword round; return its saturation statistics."""
    label, families = q.ROUNDS[round_no]
    seen = new = n_high = n_med = n_low = 0
    fams = set()
    if verbose:
        print(f"\n=== ROUND {round_no}: {label} ===")

    # Clusters whose literature lives in INSPIRE. For these, INSPIRE is the
    # canonical index: it covers pre-1990 HEP that OpenAlex and Crossref resolve
    # badly, and it is curated rather than crawled.
    HEP_CLUSTERS = {"E", "F", "G", "I", "J"}

    for family, cluster, query in families:
        fams.add(family)
        recs = src.oa_search(query, con, round_no, per_page=50, pages=1)
        if cross_sources:
            recs += src.arxiv_search(query, con, round_no, max_results=25)
            if cluster in HEP_CLUSTERS:
                recs += src.inspire_search(query, con, round_no, size=25)
        got_new = 0
        for rec in recs:
            seen += 1
            _wid, is_new, level = store(con, rec, cluster, round_no, family)
            if is_new:
                new += 1
                got_new += 1
                n_high += level == "HIGH"
                n_med += level == "MEDIUM"
                n_low += level == "LOW"
        if verbose:
            print(f"  [{family:22s}] {len(recs):4d} hits, {got_new:4d} new  "
                  f"| {query[:52]}")
        con.commit()

    con.execute(
        "INSERT OR REPLACE INTO saturation (round, query_families, papers_seen,"
        " new_unique, new_high, new_medium, new_low, new_clusters,"
        " new_priority_threats, note) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (round_no, ", ".join(sorted(fams)), seen, new, n_high, n_med, n_low,
         len({c for _, c, _ in families}), n_high, label))
    con.commit()
    if verbose:
        print(f"  -> seen {seen}, new {new} (HIGH {n_high}, MED {n_med}, LOW {n_low})")
    return {"round": round_no, "seen": seen, "new": new, "high": n_high}


def snowball(con, round_no=7, verbose=True):
    """ROUND 7: citation snowballing from identifier-addressed seeds.

    Forward (who cites the seed) and backward (what the seed cites).  This is
    the round that finds works whose vocabulary we never guessed, so it is the
    only honest check on keyword saturation.
    """
    if verbose:
        print(f"\n=== ROUND {round_no}: citation snowball (forward + backward) ===")
    stats = {"seen": 0, "new": 0, "high": 0}
    for doi, label in q.SEEDS:
        seed = src.oa_by_doi(doi, con, round_no)
        if seed is None or not seed.get("openalex_id"):
            if verbose:
                print(f"  [seed MISSING] {label} ({doi})")
            continue
        oid = seed["openalex_id"]
        store(con, seed, "G", round_no, "seed")

        fwd = src.oa_cited_by(oid, con, round_no, per_page=100, pages=2)
        back = src.oa_by_ids(seed.get("_referenced_works", []), con, round_no,
                             via=f"refs_of:{oid}")
        for rec, direction in [(r, "fwd") for r in fwd] + [(r, "back") for r in back]:
            stats["seen"] += 1
            _w, is_new, level = store(con, rec, "G", round_no, f"snowball_{direction}")
            if is_new:
                stats["new"] += 1
                stats["high"] += level == "HIGH"
            if direction == "fwd":
                con.execute("INSERT OR IGNORE INTO citation_edges VALUES (?,?,?)",
                            (rec.get("openalex_id") or "?", oid, "openalex"))
            else:
                con.execute("INSERT OR IGNORE INTO citation_edges VALUES (?,?,?)",
                            (oid, rec.get("openalex_id") or "?", "openalex"))
        if verbose:
            print(f"  [{label[:44]:44s}] fwd {len(fwd):4d}  back {len(back):3d}")
        con.commit()

    con.execute(
        "INSERT OR REPLACE INTO saturation (round, query_families, papers_seen,"
        " new_unique, new_high, new_medium, new_low, new_clusters,"
        " new_priority_threats, note) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (round_no, "citation_snowball", stats["seen"], stats["new"],
         stats["high"], 0, 0, 1, stats["high"],
         "forward+backward citations from identifier-addressed seeds"))
    con.commit()
    if verbose:
        print(f"  -> seen {stats['seen']}, new {stats['new']}, HIGH {stats['high']}")
    return stats


def inspire_snowball(con, round_no=17, verbose=True):
    """INSPIRE-native citation traversal for the historical HEP seeds.

    OpenAlex covers post-2000 well but thins out badly before 1990, which is
    exactly where the precedents for Theorems B and C would live.  INSPIRE's
    ``refersto recid`` query is the reliable path to "who used Bachas' or
    Seiler's inequality afterwards".
    """
    if verbose:
        print(f"\n=== ROUND {round_no}: INSPIRE citation snowball (historical HEP) ===")
    stats = {"seen": 0, "new": 0, "high": 0}
    for recid, label in q.INSPIRE_SEEDS:
        cites = src.inspire_citations(recid, con, round_no, size=100, pages=2)
        for rec in cites:
            stats["seen"] += 1
            _w, is_new, level = store(con, rec, "G", round_no, "inspire_fwd")
            if is_new:
                stats["new"] += 1
                stats["high"] += level == "HIGH"
        if verbose:
            print(f"  [{label[:52]:52s}] {len(cites):4d} citing records")
        con.commit()

    con.execute(
        "INSERT OR REPLACE INTO saturation (round, query_families, papers_seen,"
        " new_unique, new_high, new_medium, new_low, new_clusters,"
        " new_priority_threats, note) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (round_no, "inspire_snowball", stats["seen"], stats["new"], stats["high"],
         0, 0, 1, stats["high"],
         "forward citations of pre-1990 HEP seeds via INSPIRE refersto"))
    con.commit()
    if verbose:
        print(f"  -> seen {stats['seen']}, new {stats['new']}, HIGH {stats['high']}")
    return stats


def harvest_software(con, round_no=8, verbose=True):
    if verbose:
        print(f"\n=== ROUND {round_no}: software and archived research code ===")
    targets = [
        ("inverse Laplace transform exponential fitting", "H"),
        ("moment problem Hankel positivity", "B"),
        ("Pade approximant rational approximation", "D"),
        ("lattice QCD spectral reconstruction", "E"),
        ("arbitrary precision interval arithmetic", "H"),
        ("NNLS exponential decay relaxation spectrum", "X"),
    ]
    n = 0
    for query, cluster in targets:
        rows = src.github_search(query, con, round_no, per_page=10)
        rows += src.zenodo_search(query, con, round_no, size=10)
        for r in rows:
            if not r.get("repo"):
                continue
            con.execute(
                "INSERT OR IGNORE INTO software (repo,url,language,license,stars,"
                "last_update,paper_ids,purpose,cluster) VALUES (?,?,?,?,?,?,?,?,?)",
                (r["repo"], r.get("url"), r.get("language"), r.get("license"),
                 r.get("stars"), r.get("last_update"), r.get("paper_ids"),
                 r.get("purpose"), cluster))
            n += 1
        if verbose:
            print(f"  [{cluster}] {len(rows):3d} candidates | {query[:48]}")
        con.commit()
    return n


def main(argv=None):
    argv = argv or sys.argv[1:]
    con = sdb.connect()
    only = [int(a) for a in argv if a.isdigit()]
    # Rounds 7 and 8 are not keyword rounds; dispatch them separately.
    for rnd in (only or list(q.ROUNDS)):
        if rnd in q.ROUNDS:
            run_round(con, rnd)
    if not only or 7 in only:
        snowball(con)
    if not only or 8 in only:
        harvest_software(con)
    if not only or 17 in only:
        inspire_snowball(con)

    total = con.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    high = con.execute(
        "SELECT COUNT(DISTINCT work_id) FROM relevance WHERE priority_threat='HIGH'"
    ).fetchone()[0]
    print(f"\nTOTAL works {total}; HIGH-threat {high}")
    con.close()


if __name__ == "__main__":
    main()
