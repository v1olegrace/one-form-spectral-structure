"""Exports, knowledge graph, and the saturation report.

Produces the machine-readable artifacts from the database. Everything here is
derived: the database is the single source of truth, and re-running this script
after more harvesting regenerates every file.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scilit import db as sdb  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"


def _write_csv(path, rows, header):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def export_all(con):
    out = {}

    # --- master literature table -------------------------------------------
    rows = con.execute("""
        SELECT w.id, w.title, w.authors, w.year, w.venue, w.doi, w.arxiv_id,
               w.openalex_id, w.oa_status, w.oa_url, w.citation_count,
               w.discovered_round, w.discovered_via, w.source,
               r.cluster, r.score, r.novelty_threat, r.foundational_value,
               r.implementation_value, r.reading_priority, r.priority_threat,
               r.read_status, r.equation_level_required, r.reason
        FROM works w JOIN relevance r ON r.work_id = w.id
        ORDER BY r.novelty_threat DESC, w.year
    """).fetchall()
    out["literature_master.csv"] = _write_csv(
        DATA / "literature_master.csv", [tuple(r) for r in rows], rows[0].keys()
        if rows else ["id"])

    # --- citation edges -----------------------------------------------------
    edges = con.execute("SELECT citing, cited, source FROM citation_edges").fetchall()
    out["citation_edges.csv"] = _write_csv(
        DATA / "citation_edges.csv", [tuple(e) for e in edges],
        ["citing", "cited", "source"])

    # --- software -----------------------------------------------------------
    sw = con.execute("SELECT repo,url,language,license,stars,last_update,"
                     "paper_ids,purpose,cluster FROM software "
                     "ORDER BY (stars IS NULL), stars DESC").fetchall()
    out["software_master.csv"] = _write_csv(
        DATA / "software_master.csv", [tuple(s) for s in sw],
        ["repo", "url", "language", "license", "stars", "last_update",
         "paper_ids", "purpose", "cluster"])

    # --- claim x literature matrix -----------------------------------------
    cw = con.execute("""
        SELECT c.claim_id, c.status, cw.work_id, w.title, w.year, cw.relation,
               cw.confidence, cw.equation, cw.theorem, r.read_status,
               cw.evidence, cw.notes
        FROM claim_work_relation cw
        JOIN claims c ON c.claim_id = cw.claim_id
        JOIN works w ON w.id = cw.work_id
        LEFT JOIN relevance r ON r.work_id = cw.work_id
        GROUP BY c.claim_id, cw.work_id, cw.relation
        ORDER BY c.claim_id, cw.confidence DESC
    """).fetchall()
    out["claim_literature_matrix.csv"] = _write_csv(
        DATA / "claim_literature_matrix.csv", [tuple(r) for r in cw],
        ["claim_id", "claim_status", "work_id", "title", "year", "relation",
         "confidence", "equation", "theorem", "read_status", "evidence", "notes"])

    # --- reading queue: what to read next, and why --------------------------
    rq = con.execute("""
        SELECT w.id, w.title, w.year, r.cluster, r.novelty_threat,
               r.reading_priority, r.read_status, w.oa_url, r.reason
        FROM works w JOIN relevance r ON r.work_id = w.id
        WHERE r.priority_threat IN ('HIGH','MEDIUM')
          AND r.read_status IN ('DISCOVERED','METADATA_VERIFIED')
        ORDER BY r.novelty_threat DESC LIMIT 120
    """).fetchall()
    out["reading_queue.csv"] = _write_csv(
        DATA / "reading_queue.csv", [tuple(r) for r in rq],
        ["id", "title", "year", "cluster", "novelty_threat", "reading_priority",
         "read_status", "oa_url", "reason"])

    # --- parquet, when pandas is available ----------------------------------
    try:
        import pandas as pd
        df = pd.read_csv(DATA / "literature_master.csv")
        df.to_parquet(DATA / "literature_master.parquet", index=False)
        out["literature_master.parquet"] = len(df)
    except Exception as exc:  # noqa: BLE001
        out["literature_master.parquet"] = f"SKIPPED ({type(exc).__name__})"

    # --- knowledge graph ----------------------------------------------------
    out["knowledge_graph.graphml"] = _graphml(con)

    # --- provenance ---------------------------------------------------------
    log = con.execute("SELECT source, COUNT(*) n FROM search_log "
                      "GROUP BY source ORDER BY n DESC").fetchall()
    prov = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": str(DB_REL := DATA / "literature.db"),
        "api_calls_by_source": {r["source"]: r["n"] for r in log},
        "total_api_calls": sum(r["n"] for r in log),
        "works": con.execute("SELECT COUNT(*) FROM works").fetchone()[0],
        "relevance_rows": con.execute("SELECT COUNT(*) FROM relevance").fetchone()[0],
        "citation_edges": len(edges),
        "merged_duplicates": con.execute(
            "SELECT COUNT(*) FROM work_aliases").fetchone()[0],
        "legal_note": (
            "Official APIs only. No paywall circumvention, no HTML scraping "
            "where an API exists, no protected full text stored. Polite-pool "
            "identification and conservative rate limits on every request."),
    }
    (DATA / "retrieval_provenance.json").write_text(
        json.dumps(prov, indent=2), encoding="utf-8")
    out["retrieval_provenance.json"] = prov["total_api_calls"]
    return out


def _graphml(con):
    """Knowledge graph: works as nodes, citations as edges, cluster as attribute."""
    # citation_edges store OpenAlex ids; map them onto canonical work ids.
    oa2id = {r["openalex_id"]: r["id"] for r in con.execute(
        "SELECT id, openalex_id FROM works WHERE openalex_id IS NOT NULL")}
    edges = []
    linked = set()
    for e in con.execute("SELECT citing, cited FROM citation_edges"):
        a, b = oa2id.get(e["citing"]), oa2id.get(e["cited"])
        if a and b and a != b:
            edges.append((a, b))
            linked.update((a, b))

    # A graph of only the top-threat works has almost no internal edges: the
    # citation structure lives between them and the seeds they hang off. So the
    # node set is "interesting OR connected", which is what makes the graph
    # navigable rather than a scatter of isolated points.
    nodes = con.execute("""
        SELECT w.id, w.title, w.year, r.cluster, r.novelty_threat, r.priority_threat
        FROM works w JOIN relevance r ON r.work_id = w.id
        WHERE r.priority_threat IN ('HIGH','MEDIUM') OR r.novelty_threat >= 25
        GROUP BY w.id
    """).fetchall()
    keep = {n["id"] for n in nodes} | linked
    nodes = con.execute(f"""
        SELECT w.id, w.title, w.year, r.cluster, r.novelty_threat, r.priority_threat
        FROM works w JOIN relevance r ON r.work_id = w.id
        WHERE w.id IN ({','.join('?' * len(keep))})
        GROUP BY w.id
    """, list(keep)).fetchall() if keep else []
    keep = {n["id"] for n in nodes}
    edges = [(a, b) for a, b in edges if a in keep and b in keep]

    def esc(s):
        return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">']
    for k, t in [("title", "string"), ("year", "int"), ("cluster", "string"),
                 ("threat", "int"), ("level", "string")]:
        parts.append(f'<key id="{k}" for="node" attr.name="{k}" attr.type="{t}"/>')
    parts.append('<graph edgedefault="directed">')
    for n in nodes:
        parts.append(
            f'<node id="{esc(n["id"])}">'
            f'<data key="title">{esc(n["title"][:180])}</data>'
            f'<data key="year">{n["year"] or 0}</data>'
            f'<data key="cluster">{esc(n["cluster"])}</data>'
            f'<data key="threat">{n["novelty_threat"] or 0}</data>'
            f'<data key="level">{esc(n["priority_threat"])}</data></node>')
    for i, (a, b) in enumerate(edges):
        parts.append(f'<edge id="e{i}" source="{esc(a)}" target="{esc(b)}"/>')
    parts += ["</graph>", "</graphml>"]
    (ROOT / "knowledge_graph.graphml").write_text("\n".join(parts), encoding="utf-8")
    return f"{len(nodes)} nodes, {len(edges)} edges"


def saturation_report(con):
    """The saturation curve, reported with its honest qualifier."""
    rows = con.execute("SELECT * FROM saturation ORDER BY round").fetchall()
    lines = [
        "# Search saturation report",
        "",
        "## What this measures -- and what it does not",
        "",
        "Saturation here means: **no new HIGH-threat work appeared under the",
        "query families listed below**. That is a statement about the exhaustion",
        "of *our query vocabulary*, which is strictly weaker than the exhaustion",
        "of the literature. A predecessor that shares our mathematics but none of",
        "our words is invisible to every keyword round, by construction.",
        "",
        "The citation-snowball rounds (7 and 17) exist to break that circularity,",
        "because they reach works whose vocabulary was never guessed. Round 17",
        "specifically traverses pre-1990 HEP through INSPIRE, where OpenAlex and",
        "Crossref coverage thins out badly.",
        "",
        "| round | papers seen | new unique | new HIGH | new MED | families |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(f"| {r['round']} | {r['papers_seen']} | {r['new_unique']} | "
                     f"{r['new_high']} | {r['new_medium']} | "
                     f"{(r['query_families'] or '')[:70]} |")

    tot_seen = sum(r["papers_seen"] for r in rows)
    tot_new = sum(r["new_unique"] for r in rows)
    lines += [
        "",
        f"Totals: {tot_seen} records examined, {tot_new} unique works retained.",
        "",
        "## Saturation status, per the stated criterion",
        "",
        "The criterion requires THREE consecutive waves with no new HIGH/FATAL",
        "threat, <1% growth of the HIGH corpus, and no new distinct method.",
        "",
    ]
    hi = [r for r in rows if r["round"] in range(1, 18)]
    tail = [r for r in hi[-3:]]
    if tail and all(r["new_high"] == 0 for r in tail):
        lines.append("Rounds " + ", ".join(str(r["round"]) for r in tail) +
                     " produced no new HIGH-threat work.")
        lines.append("")
        lines.append("**Status: NOT SATURATED.** The last three rounds were "
                     "thematically narrow (history, robustness, INSPIRE "
                     "snowball). A quiet tail on narrow rounds is not evidence "
                     "of saturation across the whole search universe; the "
                     "criterion demands quiet rounds that were also BROAD.")
    else:
        lines.append("**Status: NOT SATURATED.** HIGH-threat works were still "
                     "appearing in the final rounds.")
    lines += [
        "",
        "Unfinished axes, stated explicitly so that absence of evidence is not",
        "mistaken for evidence of absence:",
        "",
        "* Backward references of the HIGH-threat set have not been traversed.",
        "* No book-length source has been read; the moment-problem monographs",
        "  (Akhiezer, Schmudgen, Chihara, Widder) are metadata-only.",
        "* Paywalled pre-1990 primary sources (Bachas 1986, Seiler 1978,",
        "  Brown-Weisberger 1979, Wichmann-Kroll 1956) were NOT read; their",
        "  content is known here only through later restatements.",
        "* Only 1 work has been read at equation level in this pass.",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "SEARCH_SATURATION_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8")
    return len(rows)


if __name__ == "__main__":
    con = sdb.connect()
    for k, v in export_all(con).items():
        print(f"  {k:36s} {v}")
    print(f"  SEARCH_SATURATION_REPORT.md          {saturation_report(con)} rounds")
