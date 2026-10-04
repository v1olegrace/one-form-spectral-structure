"""Literature harvester for the priority audit.

Queries structured APIs in the order INSPIRE-HEP -> Crossref -> Semantic Scholar.
HTML is never scraped when an API exists; Google Scholar is not touched
(manual only, per its terms).

Design rules
------------
* Never fabricate a field.  Anything not returned by an API is written as
  ``PENDING_VERIFICATION``.
* Every raw API response is stored under ``data/api_responses/``, so the
  default run is offline and the provenance of each field is auditable.  A
  failed fetch is never stored: a stored ``null`` would block the retry.
* ``data/literature_harvest.json`` is the curated record.  Hand fields
  (``correction``, ``added``) and hand corrections of API values live there and
  are never overwritten by a run.
* Deduplicate on DOI, then arXiv id, then normalised title.
* Exponential backoff, a descriptive User-Agent that points to the repository
  (no personal e-mail in request headers), and a courtesy delay between calls.

Modes
-----
    python scripts/literature_harvester.py            # verify, offline (default)
    python scripts/literature_harvester.py --fetch    # fill missing caches, online
    python scripts/literature_harvester.py --add      # append new SEEDS, online

``verify`` re-derives every committed record from the cached responses and
compares it field by field.  A difference is accepted only where the record
carries a ``correction`` note naming that field, or where the record is listed
in ``MANUAL`` with the reason.  It also checks that the CSV is the export of
the JSON.  It exits non-zero on any unexplained difference or missing cache,
and writes nothing.  ``--add`` writes only records for seeds that are not yet
in the JSON; existing records are never touched.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "api_responses"
OUT_CSV = ROOT / "data" / "literature_harvest.csv"
OUT_JSON = ROOT / "data" / "literature_harvest.json"

UA = "priority-audit/1.0 (+https://github.com/v1olegrace/one-form-spectral-structure)"
PENDING = "PENDING_VERIFICATION"
COURTESY_DELAY = 1.0
FIELDS = ["title", "authors", "year", "journal", "volume", "pages",
          "doi", "arxiv", "inspire_id"]
CSV_COLS = ["key", "seed_query", *FIELDS, "provenance"]

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
    # Added by hand to the curated JSON on 2026-09-21 (paper v0.2), outside
    # this list and without cached responses; seeded here on 2026-10-03 so that
    # every cited record can be re-derived offline.
    ("raman_2026_positivity_notes", "arxiv", "2603.28454"),
    ("wagman_2025_lanczos", "arxiv", "2406.20009"),
    ("hackett_wagman_2025_block_lanczos", "arxiv", "2412.04444"),
    ("lawrence_2024_lagrange_duality", "arxiv", "2408.11766"),
    ("mutzel_tilloy_2025", "arxiv", "2512.19594"),
    ("loveridge_oliveira_silva_2022", "arxiv", "2203.00676"),
    ("seiler_1978", "doi", "10.1103/PhysRevD.18.482"),
    ("hinrichs_polzer_2025", "arxiv", "2511.02867"),
    # Resummation producing a discrete physical-sheet pole outside the input
    # spectral support, positive residue, closed by a spectral sum rule. Read
    # in full text (HTML) on 2026-09-29; cited as prior art for the atom
    # above the hard cutoff in the resummed bubble chain.
    ("giacosa_wolkanowski_2012", "arxiv", "1209.2332"),
    # Field-strength correlators: the split into D (Bianchi-violating, string
    # tension) and D1 (Bianchi-compatible, perimeter and potential), and D = 0
    # in abelian theories without monopoles. Read in full text (sections 2.1,
    # 3.1, 3.2, 4.2) on 2026-10-01; cited for the area-law structure that
    # Bianchi on the T-product excludes in the linear-probe transport.
    ("di_giacomo_dosch_shevchenko_simonov_2002", "arxiv", "hep-ph/0007223"),
]

# Records whose committed fields cannot be re-derived from any cached API
# response, with the reason.  verify() reports them instead of failing.
MANUAL: dict[str, str] = {}

OFFLINE = True


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
                time.sleep(2 ** (attempt + 1))
                continue
            return None
        except Exception:
            if attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            return None
    return None


def cache_path(key):
    return CACHE / (re.sub(r"[^A-Za-z0-9._-]", "_", key) + ".json")


def _cached(key, fetch):
    """Cached response for ``key``.  Offline, a missing file is reported, not
    fetched.  Online, a missing file or a stored failure is fetched again, and
    only a successful response is written."""
    path = cache_path(key)
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("raw") is not None or OFFLINE:
            return payload
    elif OFFLINE:
        return {"fetched": None, "raw": None, "missing": True}
    raw = fetch()
    time.sleep(COURTESY_DELAY)
    payload = {"fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "raw": raw}
    if raw is not None:
        CACHE.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8", newline="\n")
    return payload


def inspire(kind, value, missing=None):
    """Query INSPIRE-HEP. kind in {'arxiv','doi'}."""
    q = {"arxiv": f"arxiv:{value}", "doi": f"doi:{value}"}[kind]
    url = ("https://inspirehep.net/api/literature?q="
           + urllib.parse.quote(q)
           + "&fields=titles,authors,publication_info,dois,arxiv_eprints,"
             "earliest_date,control_number&size=1")
    payload = _cached(f"inspire_{kind}_{value}", lambda: _get(url))
    if payload.get("missing") and missing is not None:
        missing.append(f"inspire_{kind}_{value}")
    blob = payload["raw"]
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
    # The year of the journal publication when there is one; the preprint
    # date (earliest_date) otherwise.  An article number (artid) is the page
    # for journals that use one; page_start is then 1 or absent.
    year = pub.get("year") or str(md.get("earliest_date", PENDING))[:4]
    pages = pub.get("artid") or pub.get("page_start") or PENDING
    return {
        "source_api": "inspire",
        "title": md.get("titles", [{}])[0].get("title", PENDING),
        "authors": "; ".join(authors) if authors else PENDING,
        "year": str(year),
        "journal": pub.get("journal_title", PENDING),
        "volume": str(pub.get("journal_volume", PENDING)),
        "pages": str(pages),
        "doi": (md.get("dois") or [{}])[0].get("value", PENDING),
        "arxiv": (md.get("arxiv_eprints") or [{}])[0].get("value", PENDING),
        "inspire_id": str(md.get("control_number", PENDING)),
    }


def crossref(doi, missing=None):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    payload = _cached(f"crossref_{doi}", lambda: _get(url))
    if payload.get("missing") and missing is not None:
        missing.append(f"crossref_{doi}")
    blob = payload["raw"]
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


def semantic_scholar(kind, value, missing=None):
    ident = {"arxiv": f"arXiv:{value}", "doi": f"DOI:{value}"}.get(kind)
    if not ident:
        return None
    url = (f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(ident)}"
           "?fields=title,authors,year,venue,externalIds")
    payload = _cached(f"s2_{kind}_{value}", lambda: _get(url))
    if payload.get("missing") and missing is not None:
        missing.append(f"s2_{kind}_{value}")
    blob = payload["raw"]
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
    for k in FIELDS:
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


def api_records(kind, value, missing=None):
    """One record per API for a seed, from cache (offline) or network."""
    recs = [inspire(kind, value, missing)]
    if kind == "doi":
        recs.append(crossref(value, missing))
    elif recs[0] and recs[0].get("doi") not in (None, PENDING):
        recs.append(crossref(recs[0]["doi"], missing))
    recs.append(semantic_scholar(kind, value, missing))
    return recs


def derive(label, kind, value, missing=None):
    """The merged record the APIs give for one seed."""
    rec = merge(*api_records(kind, value, missing))
    rec["key"] = label
    rec["seed_query"] = f"{kind}:{value}"
    return rec


# ---------------------------------------------------------------------------
# serialisation: byte-for-byte the committed format, LF line endings
# ---------------------------------------------------------------------------
def dump_json(records):
    return json.dumps(records, indent=1, ensure_ascii=False)


def dump_csv(records):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_COLS, lineterminator="\n",
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(records)
    return buf.getvalue()


def write_outputs(records):
    OUT_JSON.write_text(dump_json(records), encoding="utf-8", newline="\n")
    OUT_CSV.write_text(dump_csv(records), encoding="utf-8", newline="\n")


def load_committed():
    return json.loads(OUT_JSON.read_text(encoding="utf-8"))


def _signature(r):
    for field in ("doi", "arxiv"):
        if r[field] != PENDING:
            return (field, r[field].lower())
    return ("title", re.sub(r"\W+", "", r["title"]).lower())


API_NAMES = ("inspire", "crossref", "semantic_scholar")


def _documented(note, field, value):
    """A hand correction counts only if its note quotes the committed value; a
    value shorter than four characters must also be named by its field.  A note
    that only names the field would accept any value."""
    if value not in note:
        return False
    return len(value) >= 4 or bool(re.search(rf"\b{field}\b", note))


def check_record(rec, by_api):
    """Each committed value must be returned by the API its provenance names,
    or be a hand correction documented in the record's ``correction`` note.

    Returns (problems, fields accepted by note, PENDING fields an API now fills)."""
    prov = json.loads(rec.get("provenance", "{}"))
    note = rec.get("correction", "")
    bad, by_note, fillable = [], [], []
    for f in FIELDS:
        value = rec.get(f, PENDING)
        if value == PENDING:
            for api in API_NAMES:
                v = by_api.get(api, {}).get(f, PENDING)
                if v not in (PENDING, "None", "", "nan"):
                    fillable.append((f, v, api))
                    break
            continue
        source = prov.get(f)
        if source in API_NAMES:
            got = by_api.get(source, {}).get(f, PENDING)
            if got == value:
                continue
            if _documented(note, f, value):
                by_note.append(f)
                continue
            bad.append(f"{f}: committed {value!r}, {source} gives {got!r}")
        elif source is None:
            bad.append(f"{f}: value {value!r} has no provenance")
        elif _documented(note, f, value):
            by_note.append(f)
        else:
            bad.append(f"{f}: provenance {source!r} is not an API and no correction note explains it")
    return bad, by_note, fillable


# ---------------------------------------------------------------------------
# modes
# ---------------------------------------------------------------------------
def verify(records=None, quiet=False):
    """Compare every committed record with what the cached responses give.

    Returns a list of problems; empty means the record set is reproducible."""
    records = load_committed() if records is None else records
    problems = []
    seeds = {s[0]: s for s in SEEDS}
    for rec in records:
        key = rec["key"]
        if key not in seeds:
            problems.append(f"{key}: not in SEEDS, so it cannot be re-derived")
            continue
        _, kind, value = seeds[key]
        if rec["seed_query"] != f"{kind}:{value}":
            problems.append(f"{key}: seed_query {rec['seed_query']} != {kind}:{value}")
        if key in MANUAL:
            if not quiet:
                print(f"  {key:44s} MANUAL: {MANUAL[key]}")
            continue
        missing = []
        by_api = {r["source_api"]: r for r in api_records(kind, value, missing) if r}
        used = set(json.loads(rec.get("provenance", "{}")).values()) & set(API_NAMES)
        prefix = {"inspire": "inspire_", "crossref": "crossref_", "semantic_scholar": "s2_"}
        needed = [m for m in missing if any(m.startswith(prefix[a]) for a in used)]
        if needed:
            problems.append(f"{key}: no cached response for {', '.join(needed)}")
            continue
        bad, by_note, fillable = check_record(rec, by_api)
        if bad:
            problems.append(f"{key}: " + "; ".join(bad))
        elif not quiet:
            extra = f" (hand correction, documented: {', '.join(by_note)})" if by_note else ""
            print(f"  {key:44s} OK{extra}")
        for f, v, api in fillable:
            print(f"  {key:44s} note: {f} is PENDING here, {api} now gives {v!r}")
    keys = [r["key"] for r in records]
    if len(set(keys)) != len(keys):
        problems.append("duplicate keys in the JSON")
    sigs = [_signature(r) for r in records]
    if len(set(sigs)) != len(sigs):
        problems.append("duplicate DOI/arXiv/title signatures in the JSON")
    csv_now = OUT_CSV.read_bytes().replace(b"\r\n", b"\n").decode("utf-8") if OUT_CSV.exists() else ""
    if csv_now != dump_csv(records):
        problems.append(f"{OUT_CSV.relative_to(ROOT)} is not the export of the JSON")
    return problems


def fetch_missing():
    """Fill missing caches for every seed, online.  Writes cache files only."""
    global OFFLINE
    OFFLINE = False
    for label, kind, value in SEEDS:
        print(f"  {label}")
        derive(label, kind, value)


def add_new():
    """Append records for seeds not yet in the JSON, online.  Existing records,
    including their hand fields and corrections, are left exactly as they are."""
    global OFFLINE
    OFFLINE = False
    records = load_committed()
    have = {r["key"] for r in records}
    sigs = {_signature(r) for r in records}
    added = 0
    for label, kind, value in SEEDS:
        if label in have:
            continue
        rec = derive(label, kind, value)
        if _signature(rec) in sigs:
            print(f"  {label}: duplicate of an existing record, skipped")
            continue
        rec["added"] = time.strftime("%Y-%m-%d")
        records.append(rec)
        sigs.add(_signature(rec))
        added += 1
        print(f"  {label}: added")
    write_outputs(records)
    print(f"{added} records added; {len(records)} in total")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--fetch", action="store_true", help="fill missing caches (online)")
    mode.add_argument("--add", action="store_true", help="append records for new seeds (online)")
    args = ap.parse_args(argv)
    if args.fetch:
        fetch_missing()
        return 0
    if args.add:
        add_new()
        return 0
    print("Verifying data/literature_harvest.json against cached API responses (offline)")
    problems = verify()
    for p in problems:
        print(f"  !! {p}")
    if problems:
        print(f"{len(problems)} problem(s); nothing was written.")
        return 1
    n = len(load_committed())
    print(f"{n} records reproduced from cache; CSV is the export of the JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
