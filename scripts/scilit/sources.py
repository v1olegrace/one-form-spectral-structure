"""Legitimate API clients for the scientific-intelligence harvest.

LEGAL AND ETHICAL CONSTRAINTS -- these are hard requirements, not preferences:

  * Official APIs only.  No HTML scraping where an API exists.
  * No paywall circumvention, no authentication bypass, no rate-limit evasion.
  * No downloading of copyright-protected books.
  * Polite-pool identification (mailto / User-Agent) on every request.
  * Conservative self-imposed rate limits, well under each service's published
    ceiling, with exponential backoff on 429/5xx.
  * For paywalled works: metadata only (ISBN/DOI/edition/TOC when public), plus
    a record of the legitimate route to access.  Nothing is fabricated.

Every response is cached under ``data/api_responses/`` and every call is written
to the ``search_log`` table, so the whole harvest is replayable offline and the
provenance of every field is auditable.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "api_responses"

# Identify the client. OpenAlex and Crossref give faster, more reliable service
# to requests that carry a contact address ("polite pool").
CONTACT = "mauro.lycanwp@gmail.com"
UA = f"scilit-harvester/1.0 (research use; mailto:{CONTACT})"

# Self-imposed minimum seconds between calls, per host. Deliberately slower than
# each service's published limit.
RATE = {
    "api.openalex.org": 0.20,      # published: 10/s polite pool
    "api.crossref.org": 0.40,      # published: 50/s polite pool
    "export.arxiv.org": 3.10,      # published: 1 per 3 s
    "api.semanticscholar.org": 1.10,   # unauthenticated: ~1/s
    "zenodo.org": 0.60,
    "api.github.com": 1.10,        # unauthenticated: 60/hour -- used sparingly
    "inspirehep.net": 1.10,
}
_last_call: dict[str, float] = {}


class FetchError(RuntimeError):
    pass


def _throttle(host):
    gap = RATE.get(host, 1.0)
    prev = _last_call.get(host)
    if prev is not None:
        wait = gap - (time.monotonic() - prev)
        if wait > 0:
            time.sleep(wait)
    _last_call[host] = time.monotonic()


def fetch(url, con=None, source="", query="", round_no=None, parse="json",
          max_retries=4, force=False):
    """GET a URL through the cache, with throttling, backoff and logging.

    ``parse`` is "json", "xml" or "text".  Returns the parsed payload.
    A cached response is returned without any network call.
    """
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    path = CACHE / f"{source or 'http'}_{key}.{'xml' if parse == 'xml' else 'json'}"
    CACHE.mkdir(parents=True, exist_ok=True)

    raw = None
    status = "CACHED"
    if path.exists() and not force:
        raw = path.read_text(encoding="utf-8")
    else:
        host = urllib.parse.urlparse(url).netloc
        delay = 2.0
        for attempt in range(max_retries):
            _throttle(host)
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "application/json, text/xml;q=0.8",
                "From": CONTACT})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    raw = resp.read().decode("utf-8", errors="replace")
                    status = str(resp.status)
                break
            except urllib.error.HTTPError as exc:
                status = f"HTTP {exc.code}"
                if exc.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                    # Honour Retry-After when the service supplies it.
                    ra = exc.headers.get("Retry-After") if exc.headers else None
                    time.sleep(float(ra) if ra and ra.isdigit() else delay)
                    delay *= 2
                    continue
                raise FetchError(f"{status} for {url}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                status = f"NETWORK {exc}"
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise FetchError(f"{status} for {url}") from exc
        if raw is None:
            raise FetchError(f"no payload for {url}")
        path.write_text(raw, encoding="utf-8")

    if parse == "json":
        payload = json.loads(raw)
    elif parse == "xml":
        payload = ET.fromstring(raw)
    else:
        payload = raw

    if con is not None:
        n = _count(payload, parse)
        con.execute(
            "INSERT INTO search_log (source, query, round, timestamp, "
            "response_hash, n_results, http_status) VALUES (?,?,?,?,?,?,?)",
            (source, query or url, round_no,
             datetime.now(timezone.utc).isoformat(timespec="seconds"),
             hashlib.sha256(raw.encode()).hexdigest()[:16], n, status))
    return payload


def _count(payload, parse):
    if parse == "json" and isinstance(payload, dict):
        for k in ("results", "data", "items", "hits"):
            v = payload.get(k)
            if isinstance(v, list):
                return len(v)
            if isinstance(v, dict) and isinstance(v.get("hits"), list):
                return len(v["hits"])
        if isinstance(payload.get("message"), dict):
            return len(payload["message"].get("items", []) or [])
    if parse == "xml":
        return len(payload.findall("{http://www.w3.org/2005/Atom}entry"))
    return 0


# ---------------------------------------------------------------------------
# OpenAlex -- the backbone. Full-text search, forward citations via `cites:`,
# backward via referenced_works, and concept tagging.
# ---------------------------------------------------------------------------

OA = "https://api.openalex.org"


def _oa_abstract(inv):
    """OpenAlex ships abstracts as an inverted index; reconstruct in order."""
    if not inv:
        return None
    pos = [(i, w) for w, idxs in inv.items() for i in idxs]
    pos.sort()
    return " ".join(w for _, w in pos)


def oa_normalize(rec, source="openalex", via="", round_no=None):
    ids = rec.get("ids") or {}
    doi = (ids.get("doi") or "").replace("https://doi.org/", "") or None
    loc = rec.get("primary_location") or {}
    best = rec.get("best_oa_location") or {}
    arxiv = None
    for lo in (rec.get("locations") or []):
        src = (lo.get("source") or {})
        if "arxiv" in (src.get("display_name") or "").lower():
            lid = lo.get("landing_page_url") or ""
            if "/abs/" in lid:
                arxiv = lid.rsplit("/abs/", 1)[-1]
    authors = "; ".join(
        (a.get("author") or {}).get("display_name") or ""
        for a in (rec.get("authorships") or [])[:12])
    return {
        "title": rec.get("display_name") or "(untitled)",
        "authors": authors or None,
        "year": rec.get("publication_year"),
        "venue": (loc.get("source") or {}).get("display_name"),
        "doi": doi,
        "arxiv_id": arxiv,
        "openalex_id": (rec.get("id") or "").rsplit("/", 1)[-1] or None,
        "source": source,
        "document_type": rec.get("type"),
        "oa_status": (rec.get("open_access") or {}).get("oa_status"),
        "oa_url": best.get("pdf_url") or best.get("landing_page_url"),
        "publisher_url": loc.get("landing_page_url"),
        "abstract": _oa_abstract(rec.get("abstract_inverted_index")),
        "citation_count": rec.get("cited_by_count"),
        "reference_count": len(rec.get("referenced_works") or []),
        "discovered_round": round_no,
        "discovered_via": via,
        "_referenced_works": [w.rsplit("/", 1)[-1] for w in (rec.get("referenced_works") or [])],
    }


OA_FIELDS = ("id,ids,display_name,publication_year,type,authorships,"
             "primary_location,best_oa_location,locations,open_access,"
             "cited_by_count,referenced_works,abstract_inverted_index")


def oa_search(query, con=None, round_no=None, per_page=50, pages=1,
              extra_filter=None, title_only=False):
    """Full-text (or title/abstract) search. Returns normalized records."""
    out, cursor = [], "*"
    field = "title_and_abstract.search" if title_only else "default.search"
    for _ in range(pages):
        filt = f"{field}:{query}"
        if extra_filter:
            filt += "," + extra_filter
        url = (f"{OA}/works?filter={urllib.parse.quote(filt, safe=':,')}"
               f"&per-page={per_page}&cursor={urllib.parse.quote(cursor)}"
               f"&select={OA_FIELDS}&mailto={CONTACT}")
        try:
            data = fetch(url, con, "openalex", f"search:{query}", round_no)
        except FetchError:
            break
        for rec in data.get("results", []):
            out.append(oa_normalize(rec, via=f"oa_search:{query}", round_no=round_no))
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not cursor or len(data.get("results", [])) < per_page:
            break
    return out


def oa_cited_by(openalex_id, con=None, round_no=None, per_page=100, pages=3):
    """FORWARD citations: everything citing this work.

    ``cited_by_api_url`` is absent from the selected fields, but the
    ``cites:`` filter is equivalent and pages cleanly.
    """
    out, cursor = [], "*"
    for _ in range(pages):
        url = (f"{OA}/works?filter=cites:{openalex_id}&per-page={per_page}"
               f"&cursor={urllib.parse.quote(cursor)}&select={OA_FIELDS}"
               f"&mailto={CONTACT}")
        try:
            data = fetch(url, con, "openalex", f"cites:{openalex_id}", round_no)
        except FetchError:
            break
        for rec in data.get("results", []):
            out.append(oa_normalize(rec, via=f"cites:{openalex_id}", round_no=round_no))
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not cursor or len(data.get("results", [])) < per_page:
            break
    return out


def oa_by_ids(openalex_ids, con=None, round_no=None, via="references"):
    """BACKWARD citations: fetch works by OpenAlex id, 50 at a time."""
    out = []
    ids = [i for i in openalex_ids if i]
    for i in range(0, len(ids), 50):
        chunk = "|".join(ids[i:i + 50])
        url = (f"{OA}/works?filter=openalex_id:{chunk}&per-page=50"
               f"&select={OA_FIELDS}&mailto={CONTACT}")
        try:
            data = fetch(url, con, "openalex", f"ids:{chunk[:60]}", round_no)
        except FetchError:
            continue
        for rec in data.get("results", []):
            out.append(oa_normalize(rec, via=via, round_no=round_no))
    return out


def oa_by_doi(doi, con=None, round_no=None):
    url = f"{OA}/works/doi:{urllib.parse.quote(doi)}?select={OA_FIELDS}&mailto={CONTACT}"
    try:
        return oa_normalize(fetch(url, con, "openalex", f"doi:{doi}", round_no),
                            via=f"doi_lookup:{doi}", round_no=round_no)
    except (FetchError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# arXiv -- Atom XML, NOT json. Used for abstracts and for full-text HTML checks.
# ---------------------------------------------------------------------------

ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"


def arxiv_search(query, con=None, round_no=None, max_results=50, start=0):
    url = ("http://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(query)
           + f"&start={start}&max_results={max_results}"
           + "&sortBy=relevance&sortOrder=descending")
    try:
        root = fetch(url, con, "arxiv", query, round_no, parse="xml")
    except (FetchError, ET.ParseError):
        return []
    out = []
    for e in root.findall(f"{ATOM}entry"):
        aid = (e.findtext(f"{ATOM}id") or "").rsplit("/abs/", 1)[-1]
        doi = e.findtext(f"{ARX}doi")
        published = e.findtext(f"{ATOM}published") or ""
        out.append({
            "title": " ".join((e.findtext(f"{ATOM}title") or "").split()),
            "authors": "; ".join(
                a.findtext(f"{ATOM}name") or "" for a in e.findall(f"{ATOM}author")[:12]),
            "year": int(published[:4]) if published[:4].isdigit() else None,
            "venue": e.findtext(f"{ARX}journal_ref") or "arXiv",
            "doi": doi, "arxiv_id": aid, "openalex_id": None,
            "source": "arxiv", "document_type": "preprint",
            "oa_status": "green", "oa_url": f"https://arxiv.org/abs/{aid}",
            "publisher_url": None,
            "abstract": " ".join((e.findtext(f"{ATOM}summary") or "").split()),
            "citation_count": None, "reference_count": None,
            "discovered_round": round_no, "discovered_via": f"arxiv:{query}",
            "_referenced_works": [],
        })
    return out


# ---------------------------------------------------------------------------
# Crossref -- authoritative DOI metadata; used to VERIFY, not to discover.
# ---------------------------------------------------------------------------

def crossref_by_doi(doi, con=None, round_no=None):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={CONTACT}"
    try:
        msg = fetch(url, con, "crossref", f"doi:{doi}", round_no)["message"]
    except (FetchError, KeyError, json.JSONDecodeError):
        return None
    issued = (msg.get("issued") or {}).get("date-parts") or [[None]]
    return {
        "title": (msg.get("title") or ["(untitled)"])[0],
        "authors": "; ".join(
            f"{a.get('given','')} {a.get('family','')}".strip()
            for a in (msg.get("author") or [])[:12]) or None,
        "year": issued[0][0],
        "venue": (msg.get("container-title") or [None])[0],
        "doi": msg.get("DOI"), "document_type": msg.get("type"),
        "publisher_url": msg.get("URL"),
        "reference_count": msg.get("reference-count"),
        "citation_count": msg.get("is-referenced-by-count"),
        "isbn": (msg.get("ISBN") or [None])[0],
        "source": "crossref",
    }


# ---------------------------------------------------------------------------
# Semantic Scholar -- independent citation graph; good cross-check on OpenAlex.
# ---------------------------------------------------------------------------

def s2_search(query, con=None, round_no=None, limit=50):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?query="
           + urllib.parse.quote(query)
           + f"&limit={limit}&fields=title,year,abstract,externalIds,"
             "citationCount,referenceCount,venue,authors,openAccessPdf")
    try:
        data = fetch(url, con, "s2", query, round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    out = []
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        out.append({
            "title": p.get("title") or "(untitled)",
            "authors": "; ".join((a.get("name") or "") for a in (p.get("authors") or [])[:12]) or None,
            "year": p.get("year"), "venue": p.get("venue"),
            "doi": ext.get("DOI"), "arxiv_id": ext.get("ArXiv"),
            "openalex_id": None, "source": "s2",
            "document_type": "article", "oa_status": None,
            "oa_url": (p.get("openAccessPdf") or {}).get("url"),
            "publisher_url": None, "abstract": p.get("abstract"),
            "citation_count": p.get("citationCount"),
            "reference_count": p.get("referenceCount"),
            "discovered_round": round_no, "discovered_via": f"s2:{query}",
            "_referenced_works": [],
        })
    return out


# ---------------------------------------------------------------------------
# INSPIRE-HEP -- the CANONICAL metadata source whenever a HEP record exists.
#
# For hep-th, INSPIRE beats every general index: it carries the literature back
# to the 1950s with curated author disambiguation, and it holds records for
# pre-DOI papers that Crossref and OpenAlex resolve badly or not at all.  The
# Bachas (1986) seed failed to resolve by DOI precisely because the DOI carried
# in this project was never verified; INSPIRE resolves it from the journal
# coordinates instead.
#
# Published rate limit: 15 requests per 5 seconds. RATE[] throttles well under.
# ---------------------------------------------------------------------------

INSPIRE = "https://inspirehep.net/api"


def inspire_normalize(rec, via="", round_no=None):
    md = rec.get("metadata") or rec
    ids = {d.get("schema"): d.get("value") for d in (md.get("arxiv_eprints") or [])}
    arxiv = None
    for e in (md.get("arxiv_eprints") or []):
        arxiv = e.get("value")
    doi = None
    for d in (md.get("dois") or []):
        doi = d.get("value")
        break
    pub = (md.get("publication_info") or [{}])[0]
    year = md.get("earliest_date") or ""
    titles = md.get("titles") or [{}]
    absts = md.get("abstracts") or [{}]
    return {
        "title": titles[0].get("title", "(untitled)"),
        "authors": "; ".join(
            a.get("full_name", "") for a in (md.get("authors") or [])[:12]) or None,
        "year": int(year[:4]) if year[:4].isdigit() else pub.get("year"),
        "venue": pub.get("journal_title"),
        "doi": doi, "arxiv_id": arxiv, "openalex_id": None,
        "source": "inspire", "document_type": (md.get("document_type") or ["article"])[0],
        "oa_status": None,
        "oa_url": f"https://arxiv.org/abs/{arxiv}" if arxiv else None,
        "publisher_url": f"https://inspirehep.net/literature/{rec.get('id') or md.get('control_number')}",
        "abstract": absts[0].get("value") if absts else None,
        "citation_count": md.get("citation_count"),
        "reference_count": len(md.get("references") or []),
        "discovered_round": round_no, "discovered_via": via,
        "_inspire_id": rec.get("id") or md.get("control_number"),
        "_referenced_works": [],
    }


INSPIRE_FIELDS = ("titles,authors,arxiv_eprints,dois,publication_info,abstracts,"
                  "citation_count,earliest_date,document_type,control_number")


def inspire_search(query, con=None, round_no=None, size=25, sort="mostcited"):
    url = (f"{INSPIRE}/literature?q={urllib.parse.quote(query)}&size={size}"
           f"&sort={sort}&fields={INSPIRE_FIELDS}")
    try:
        data = fetch(url, con, "inspire", query, round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    return [inspire_normalize(h, f"inspire:{query}", round_no)
            for h in ((data.get("hits") or {}).get("hits") or [])]


def inspire_lookup(identifier, con=None, round_no=None):
    """Resolve one record by arXiv id, DOI, or INSPIRE recid.

    This is the VERIFICATION path: it turns a guessed or partial reference into
    a curated record, or fails loudly. It never fuzzy-matches a title.
    """
    if identifier.startswith("10."):
        url = f"{INSPIRE}/doi/{identifier}?fields={INSPIRE_FIELDS}"
    elif identifier.replace(".", "").replace("/", "").isdigit() and "." in identifier:
        url = f"{INSPIRE}/arxiv/{identifier}?fields={INSPIRE_FIELDS}"
    elif identifier.isdigit():
        url = f"{INSPIRE}/literature/{identifier}?fields={INSPIRE_FIELDS}"
    else:
        url = f"{INSPIRE}/arxiv/{identifier}?fields={INSPIRE_FIELDS}"
    try:
        return inspire_normalize(fetch(url, con, "inspire", f"lookup:{identifier}",
                                       round_no), f"inspire_lookup:{identifier}", round_no)
    except (FetchError, json.JSONDecodeError, KeyError):
        return None


def inspire_references(recid, con=None, round_no=None):
    """Backward references of an INSPIRE record, as normalized stubs."""
    url = f"{INSPIRE}/literature/{recid}?fields=references"
    try:
        data = fetch(url, con, "inspire", f"refs:{recid}", round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    out = []
    for ref in ((data.get("metadata") or {}).get("references") or []):
        r = ref.get("reference") or {}
        rid = (ref.get("record") or {}).get("$ref", "")
        out.append({
            "title": (r.get("title") or {}).get("title") or r.get("misc", ["(untitled)"])[0]
            if isinstance(r.get("misc"), list) else (r.get("title") or {}).get("title", "(untitled)"),
            "doi": r.get("dois", [None])[0] if isinstance(r.get("dois"), list) else None,
            "arxiv_id": r.get("arxiv_eprint"),
            "year": r.get("publication_info", {}).get("year") if isinstance(r.get("publication_info"), dict) else None,
            "inspire_ref": rid.rsplit("/", 1)[-1] if rid else None,
        })
    return out


def inspire_citations(recid, con=None, round_no=None, size=100, pages=2):
    """Forward citations: records citing this INSPIRE recid."""
    out = []
    for page in range(1, pages + 1):
        url = (f"{INSPIRE}/literature?q=refersto%20recid%20{recid}&size={size}"
               f"&page={page}&fields={INSPIRE_FIELDS}&sort=mostcited")
        try:
            data = fetch(url, con, "inspire", f"refersto:{recid}:p{page}", round_no)
        except (FetchError, json.JSONDecodeError):
            break
        hits = (data.get("hits") or {}).get("hits") or []
        out += [inspire_normalize(h, f"cites_inspire:{recid}", round_no) for h in hits]
        if len(hits) < size:
            break
    return out


def inspire_bibtex(recid, con=None):
    """Authoritative BibTeX for a record. Used to build references_master.bib."""
    url = f"{INSPIRE}/literature/{recid}?format=bibtex"
    try:
        return fetch(url, con, "inspire_bib", f"bibtex:{recid}", parse="text")
    except FetchError:
        return None


# ---------------------------------------------------------------------------
# Unpaywall -- legal open-access resolution. Returns the OA location if one
# exists; it never provides access to anything that is not already free.
# ---------------------------------------------------------------------------

def unpaywall(doi, con=None, round_no=None):
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={CONTACT}"
    try:
        d = fetch(url, con, "unpaywall", f"doi:{doi}", round_no)
    except (FetchError, json.JSONDecodeError):
        return None
    best = d.get("best_oa_location") or {}
    return {
        "is_oa": bool(d.get("is_oa")),
        "oa_status": d.get("oa_status"),
        "oa_url": best.get("url_for_pdf") or best.get("url"),
        "host_type": best.get("host_type"),
        "license": best.get("license"),
    }


# ---------------------------------------------------------------------------
# DOAB -- Directory of Open Access Books. The only book source from which full
# text may be taken, because every record there IS open access by definition.
# ---------------------------------------------------------------------------

def doab_search(query, con=None, round_no=None, size=20):
    url = ("https://directory.doabooks.org/rest/search?query="
           + urllib.parse.quote(query) + f"&expand=metadata&limit={size}")
    try:
        data = fetch(url, con, "doab", query, round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    out = []
    for rec in (data if isinstance(data, list) else []):
        md = {m.get("key"): m.get("value") for m in (rec.get("metadata") or [])}
        out.append({
            "title": rec.get("name") or md.get("dc.title") or "(untitled)",
            "authors": md.get("dc.contributor.author"),
            "year": (md.get("dc.date.issued") or "")[:4] or None,
            "isbn": md.get("dc.identifier.isbn"),
            "publisher": md.get("dc.publisher"),
            "access_status": "OPEN_ACCESS",
            "access_route": rec.get("handle") and
            f"https://directory.doabooks.org/handle/{rec['handle']}",
        })
    return out


# ---------------------------------------------------------------------------
# Software: Zenodo (archived research code with DOIs) and GitHub.
# ---------------------------------------------------------------------------

def zenodo_search(query, con=None, round_no=None, size=20):
    url = ("https://zenodo.org/api/records?q=" + urllib.parse.quote(query)
           + f"&size={size}&type=software&sort=mostrecent")
    try:
        data = fetch(url, con, "zenodo", query, round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    out = []
    for h in ((data.get("hits") or {}).get("hits") or []):
        md = h.get("metadata") or {}
        out.append({
            "repo": md.get("title") or "(untitled)",
            "url": h.get("links", {}).get("self_html") or md.get("doi"),
            "language": None,
            "license": ((md.get("license") or {}).get("id")
                        if isinstance(md.get("license"), dict) else md.get("license")),
            "stars": None, "last_update": md.get("publication_date"),
            "paper_ids": md.get("doi"), "purpose": (md.get("description") or "")[:300],
        })
    return out


def github_search(query, con=None, round_no=None, per_page=15):
    url = ("https://api.github.com/search/repositories?q="
           + urllib.parse.quote(query) + f"&sort=stars&per_page={per_page}")
    try:
        data = fetch(url, con, "github", query, round_no)
    except (FetchError, json.JSONDecodeError):
        return []
    return [{
        "repo": r.get("full_name"), "url": r.get("html_url"),
        "language": r.get("language"),
        "license": (r.get("license") or {}).get("spdx_id"),
        "stars": r.get("stargazers_count"), "last_update": r.get("pushed_at"),
        "paper_ids": None, "purpose": (r.get("description") or "")[:300],
    } for r in data.get("items", []) or []]
