"""Literature harvester for the priority audit.

Queries structured APIs in the order INSPIRE-HEP -> Crossref -> Semantic Scholar
-> Unpaywall.  HTML is never scraped when an API exists; Google Scholar is not
touched (manual only, per its terms).

Design rules
------------
* Never fabricate a field.  Anything not returned by an API is written as
  ``PENDING_VERIFICATION``.
* Cache every raw response under ``data/cache/`` so a rerun is offline and the
  provenance of each field is auditable.
* Deduplicate on DOI, then arXiv id, then normalised title.
* Exponential backoff, a descriptive User-Agent with contact address, and a
  courtesy delay between calls.

Usage
-----
    python scripts/literature_harvester.py                # harvest seed list
    python scripts/literature_harvester.py --refs 2202.05866   # + its references
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache"
OUT_CSV = ROOT / "data" / "literature_harvest.csv"
OUT_JSON = ROOT / "data" / "literature_harvest.json"

UA = "priority-audit/1.0 (mailto:mauro.lycanwp@gmail.com)"
PENDING = "PENDING_VERIFICATION"
COURTESY_DELAY = 1.0

# Seeds for the adversarial audit.  Each is (label, query-kind, query).
# NOTE: no fuzzy "title" seeds. A title query for "Pade Approximants" silently
# resolved to Basdevant (1968), a different work; monographs are hand-entered
# in scripts/build_bibliography.py instead, with their verification stated.
SEEDS = [
    ("cordova_ohmori_rudelius_2022", "arxiv", "2202.05866"),
    ("basile_golmohammadi_2025", "arxiv", "2503.19628"),
    ("masjuan_peris_2009", "arxiv", "0903.0294"),
    ("gaiotto_kapustin_seiberg_willett_2015", "arxiv", "1412.5148"),
    ("harlow_ooguri_2018", "arxiv", "1810.05338"),
    ("banks_seiberg_2010", "arxiv", "1011.5120"),
    ("arkanihamed_motl_nicolis_vafa_2006", "arxiv", "hep-th/0601001"),
    ("harlow_heidenreich_reece_rudelius_2022", "arxiv", "2201.08380"),
    ("bachas_1986", "doi", "10.1103/PhysRevD.33.2723"),
    ("uehling_1935", "doi", "10.1103/PhysRev.48.55"),
    ("wichmann_kroll_1956", "doi", "10.1103/PhysRev.101.843"),
    ("brown_weisberger_1979", "doi", "10.1103/PhysRevD.20.3239"),
    ("bellazzini_positive_moments_2020", "arxiv", "2011.00037"),
    ("dvali_species_2007", "arxiv", "0706.2050"),
    ("beneke_ruizfemenia_2016", "arxiv", "1606.02434"),
    ("luscher_wolff_1990", "doi", "10.1016/0550-3213(90)90540-T"),
    ("blossier_et_al_gevp_2009", "arxiv", "0902.1265"),
    ("pobylitsa_wilson_loop_inequalities_2007", "arxiv", "hep-th/0702123"),
]


def _get(url, headers=None, tries=4):
    """GET with exponential backoff.  Returns decoded text or None."""
    hdr = {"User-Agent": UA}
    hdr.update(headers or {})
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=hdr)
            with urllib.request.urlopen(req, timeout=30) as fh:
                return fh.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            return None
        except Exception:
            if attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            return None
    return None


def _cached(key, fetch):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (re.sub(r"[^A-Za-z0-9._-]", "_", key) + ".json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    raw = fetch()
    payload = {"fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "raw": raw}
    path.write_text(json.dumps(payload), encoding="utf-8")
    return payload


def inspire(kind, value):
    """Query INSPIRE-HEP. kind in {'arxiv','doi','title'}."""
    q = {"arxiv": f"arxiv:{value}", "doi": f"doi:{value}",
         "title": f'title "{value}"'}[kind]
    url = ("https://inspirehep.net/api/literature?q="
           + urllib.parse.quote(q)
           + "&fields=titles,authors,publication_info,dois,arxiv_eprints,"
             "earliest_date,control_number&size=1")
    blob = _cached(f"inspire_{kind}_{value}", lambda: _get(url))["raw"]
    if not blob:
        return None
    try:
        hits = json.loads(blob)["hits"]["hits"]
    except (KeyError, json.JSONDecodeError):
        return None
    if not hits:
        return None
    md = hits[0]["metadata"]
    pub = (md.get("publication_info") or [{}])[0]
    authors = [a.get("full_name", PENDING) for a in md.get("authors", [])]
    return {
        "source_api": "inspire",
        "title": md.get("titles", [{}])[0].get("title", PENDING),
        "authors": "; ".join(authors) if authors else PENDING,
        "year": str(md.get("earliest_date", PENDING))[:4],
        "journal": pub.get("journal_title", PENDING),
        "volume": str(pub.get("journal_volume", PENDING)),
        "pages": str(pub.get("page_start", PENDING)),
        "doi": (md.get("dois") or [{}])[0].get("value", PENDING),
        "arxiv": (md.get("arxiv_eprints") or [{}])[0].get("value", PENDING),
        "inspire_id": str(md.get("control_number", PENDING)),
    }


def crossref(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    blob = _cached(f"crossref_{doi}", lambda: _get(url))["raw"]
    if not blob:
        return None
    try:
        m = json.loads(blob)["message"]
    except (KeyError, json.JSONDecodeError):
        return None
    auth = "; ".join(
        f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
        for a in m.get("author", [])
    )
    return {
        "source_api": "crossref",
        "title": (m.get("title") or [PENDING])[0],
        "authors": auth or PENDING,
        "year": str((m.get("issued", {}).get("date-parts") or [[PENDING]])[0][0]),
        "journal": (m.get("container-title") or [PENDING])[0],
        "volume": m.get("volume", PENDING),
        "pages": m.get("page", m.get("article-number", PENDING)),
        "doi": m.get("DOI", PENDING),
        "arxiv": PENDING,
        "inspire_id": PENDING,
    }


def semantic_scholar(kind, value):
    ident = {"arxiv": f"arXiv:{value}", "doi": f"DOI:{value}"}.get(kind)
    if not ident:
        return None
    url = (f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(ident)}"
           "?fields=title,authors,year,venue,externalIds")
    blob = _cached(f"s2_{kind}_{value}", lambda: _get(url))["raw"]
    if not blob:
        return None
    try:
        m = json.loads(blob)
    except json.JSONDecodeError:
        return None
    if "title" not in m:
        return None
    ext = m.get("externalIds") or {}
    return {
        "source_api": "semantic_scholar",
        "title": m.get("title", PENDING),
        "authors": "; ".join(a.get("name", "") for a in m.get("authors", [])) or PENDING,
        "year": str(m.get("year", PENDING)),
        "journal": m.get("venue") or PENDING,
        "volume": PENDING, "pages": PENDING,
        "doi": ext.get("DOI", PENDING),
        "arxiv": ext.get("ArXiv", PENDING),
        "inspire_id": PENDING,
    }


def merge(*records):
    """First non-PENDING value wins, in API priority order."""
    out, provenance = {}, {}
    keys = ["title", "authors", "year", "journal", "volume", "pages",
            "doi", "arxiv", "inspire_id"]
    for k in keys:
        out[k] = PENDING
        for rec in records:
            if not rec:
                continue
            v = rec.get(k, PENDING)
            if v and v not in (PENDING, "None", "", "nan"):
                out[k], provenance[k] = v, rec["source_api"]
                break
    out["provenance"] = json.dumps(provenance)
    return out


def harvest(label, kind, value):
    print(f"  {label:45s} ", end="", flush=True)
    recs = []
    recs.append(inspire(kind, value))
    time.sleep(COURTESY_DELAY)
    if kind == "doi":
        recs.append(crossref(value))
        time.sleep(COURTESY_DELAY)
    elif recs[0] and recs[0].get("doi") not in (None, PENDING):
        recs.append(crossref(recs[0]["doi"]))
        time.sleep(COURTESY_DELAY)
    recs.append(semantic_scholar(kind, value))
    time.sleep(COURTESY_DELAY)
    rec = merge(*recs)
    rec["key"] = label
    rec["seed_query"] = f"{kind}:{value}"
    n_pending = sum(1 for k, v in rec.items() if v == PENDING)
    print(f"{rec['title'][:48]:50s} pending={n_pending}")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", help="also fetch references of this arXiv id")
    args = ap.parse_args()

    print("Harvesting seed list (INSPIRE -> Crossref -> Semantic Scholar)")
    rows = [harvest(*s) for s in SEEDS]

    # Deduplicate: DOI, then arXiv, then normalised title.
    seen, unique = set(), []
    for r in rows:
        for field in ("doi", "arxiv"):
            if r[field] != PENDING:
                sig = (field, r[field].lower())
                break
        else:
            sig = ("title", re.sub(r"\W+", "", r["title"]).lower())
        if sig in seen:
            continue
        seen.add(sig)
        unique.append(r)

    import csv
    cols = ["key", "seed_query", "title", "authors", "year", "journal", "volume",
            "pages", "doi", "arxiv", "inspire_id", "provenance"]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(unique)
    OUT_JSON.write_text(json.dumps(unique, indent=2), encoding="utf-8")

    pend = sum(1 for r in unique for v in r.values() if v == PENDING)
    print(f"\n{len(unique)} unique records -> {OUT_CSV.relative_to(ROOT)}")
    print(f"{pend} fields marked {PENDING} (never guessed)")


if __name__ == "__main__":
    main()
