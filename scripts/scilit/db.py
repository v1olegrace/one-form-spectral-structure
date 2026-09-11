"""Scientific-intelligence database: schema and integrity constraints.

The schema encodes two honesty rules as *enforced constraints*, not conventions,
because this project has already been bitten once by a fuzzy title match that
silently resolved "Pade Approximants" to a different 1968 paper.

RULE 1 -- VERIFIED is unreachable by fuzzy match.
    A work with no DOI, arXiv id, ISBN or trusted institutional identifier may
    not have read_status above DISCOVERED.  Fuzzy matching produces CANDIDATES.

RULE 2 -- asserted relations are separated from evidenced relations.
    A claim_work_relation of IDENTICAL / STRICTLY_STRONGER_PRIOR /
    COUNTEREXAMPLE is a finding, not an opinion, so it requires a non-empty
    equation/theorem locator AND read_status at least ABSTRACT_READ.

The read_status ladder is strictly ordered:

    DISCOVERED < METADATA_VERIFIED < ABSTRACT_READ < FULLTEXT_ACQUIRED
              < EQUATION_LEVEL_READ < CROSSCHECKED

A restated equation found in a later paper, with attribution, is legitimate
evidence -- but it is recorded at ABSTRACT_READ/FULLTEXT_ACQUIRED of the
*restating* work, never promoted to EQUATION_LEVEL_READ of the original.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "literature.db"

READ_STATES = ["DISCOVERED", "METADATA_VERIFIED", "ABSTRACT_READ",
               "FULLTEXT_ACQUIRED", "EQUATION_LEVEL_READ", "CROSSCHECKED"]

RELATIONS = ["IDENTICAL", "STRICTLY_STRONGER_PRIOR", "STRICTLY_WEAKER_PRIOR",
             "SPECIAL_CASE_PRIOR", "GENERALIZATION_PRIOR", "ANALOGOUS",
             "USES_SAME_MATH", "SUPPORTS_ASSUMPTION", "CHALLENGES_ASSUMPTION",
             "COUNTEREXAMPLE", "NUMERICAL_METHOD", "BACKGROUND_ONLY"]

# Relations that are findings rather than impressions, and therefore need a
# locator plus a real read.
EVIDENCE_REQUIRED = {"IDENTICAL", "STRICTLY_STRONGER_PRIOR", "COUNTEREXAMPLE"}

CLUSTERS = {
    "A": "Laplace / completely monotone / Bernstein-Stieltjes functions",
    "B": "Moment problems, Hankel matrices, orthogonal polynomials",
    "C": "Spectral edge, support recovery, Tauberian/Watson asymptotics",
    "D": "Rational approximation, Pade, continued fractions, Gauss quadrature",
    "E": "Lattice / QFT: Euclidean correlators, effective mass, GEVP",
    "F": "QED vacuum polarization: Uehling, Wichmann-Kroll, dispersion",
    "G": "Gauge theory static potential, Wilson loops, convexity/positivity",
    "H": "Inverse problems, exponential fitting, Prony, resolution limits",
    "I": "Positivity bounds / EFT moments / bootstrap",
    "J": "WGC, species, generalized symmetries, quantum gravity",
    "X": "Cross-domain: signal processing, NMR, rheology, statistics, approximation theory",
}

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS works (
    id                TEXT PRIMARY KEY,        -- canonical: doi:... | arxiv:... | isbn:... | openalex:...
    title             TEXT NOT NULL,
    authors           TEXT,
    year              INTEGER,
    venue             TEXT,
    doi               TEXT,
    arxiv_id          TEXT,
    isbn              TEXT,
    openalex_id       TEXT,
    source            TEXT NOT NULL,           -- which API produced this row
    document_type     TEXT,                    -- article | book | thesis | software | preprint
    oa_status         TEXT,
    oa_url            TEXT,
    publisher_url     TEXT,
    abstract          TEXT,
    citation_count    INTEGER,
    reference_count   INTEGER,
    discovered_round  INTEGER,
    discovered_via    TEXT,                    -- query or snowball edge that surfaced it
    title_key         TEXT,                    -- normalized title, for de-duplication ONLY
    UNIQUE (id)
);

CREATE INDEX IF NOT EXISTS idx_works_titlekey ON works(title_key);

-- Records every de-duplication decision, so merges are auditable and
-- reversible. A merge is a statement that two ROWS describe one work (e.g. the
-- arXiv preprint and the journal version); it is never a claim about what that
-- work says, so it does not interact with the read_status ladder.
CREATE TABLE IF NOT EXISTS work_aliases (
    alias_id     TEXT PRIMARY KEY,
    canonical_id TEXT NOT NULL,
    basis        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relevance (
    work_id                 TEXT NOT NULL REFERENCES works(id) ON DELETE CASCADE,
    cluster                 TEXT NOT NULL,
    score                   INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
    reason                  TEXT NOT NULL,
    claim_ids               TEXT,
    priority_threat         TEXT CHECK (priority_threat IN ('NONE','LOW','MEDIUM','HIGH','FATAL')),
    novelty_threat          INTEGER CHECK (novelty_threat BETWEEN 0 AND 100),
    foundational_value      INTEGER CHECK (foundational_value BETWEEN 0 AND 100),
    implementation_value    INTEGER CHECK (implementation_value BETWEEN 0 AND 100),
    reading_priority        INTEGER CHECK (reading_priority BETWEEN 0 AND 100),
    equation_level_required INTEGER NOT NULL DEFAULT 0,
    read_status             TEXT NOT NULL DEFAULT 'DISCOVERED'
                            CHECK (read_status IN
                              ('DISCOVERED','METADATA_VERIFIED','ABSTRACT_READ',
                               'FULLTEXT_ACQUIRED','EQUATION_LEVEL_READ','CROSSCHECKED')),
    access_note             TEXT,
    PRIMARY KEY (work_id, cluster)
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id       TEXT PRIMARY KEY,
    claim_text     TEXT NOT NULL,
    status         TEXT,
    paper_location TEXT,
    novelty_status TEXT
);

CREATE TABLE IF NOT EXISTS claim_work_relation (
    claim_id   TEXT NOT NULL REFERENCES claims(claim_id) ON DELETE CASCADE,
    work_id    TEXT NOT NULL REFERENCES works(id) ON DELETE CASCADE,
    relation   TEXT NOT NULL,
    confidence INTEGER CHECK (confidence BETWEEN 0 AND 10),
    evidence   TEXT,
    page       TEXT,
    equation   TEXT,
    theorem    TEXT,
    notes      TEXT,
    PRIMARY KEY (claim_id, work_id, relation)
);

CREATE TABLE IF NOT EXISTS citation_edges (
    citing TEXT NOT NULL,
    cited  TEXT NOT NULL,
    source TEXT,
    PRIMARY KEY (citing, cited)
);

CREATE TABLE IF NOT EXISTS authors (
    author       TEXT PRIMARY KEY,
    orcid        TEXT,
    affiliations TEXT,
    topics       TEXT,
    work_count   INTEGER
);

CREATE TABLE IF NOT EXISTS software (
    repo        TEXT PRIMARY KEY,
    url         TEXT,
    language    TEXT,
    license     TEXT,
    stars       INTEGER,
    last_update TEXT,
    paper_ids   TEXT,
    purpose     TEXT,
    cluster     TEXT
);

CREATE TABLE IF NOT EXISTS books (
    title             TEXT NOT NULL,
    authors           TEXT,
    edition           TEXT,
    year              INTEGER,
    isbn              TEXT,
    publisher         TEXT,
    relevant_chapters TEXT,
    access_status     TEXT,   -- OPEN_ACCESS | PUBLIC_DOMAIN | PAYWALLED_METADATA_ONLY
    access_route      TEXT,   -- where to obtain legally
    reason            TEXT,
    cluster           TEXT,
    priority          TEXT CHECK (priority IN ('NOW','NEXT','LATER','REFERENCE_ONLY')),
    PRIMARY KEY (title, edition)
);

-- Reproducibility ledger: every API call is recorded.
CREATE TABLE IF NOT EXISTS search_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    source        TEXT NOT NULL,
    query         TEXT NOT NULL,
    round         INTEGER,
    timestamp     TEXT NOT NULL,
    cursor        TEXT,
    response_hash TEXT,
    n_results     INTEGER,
    result_ids    TEXT,
    http_status   TEXT
);

CREATE TABLE IF NOT EXISTS saturation (
    round                INTEGER PRIMARY KEY,
    query_families       TEXT,
    papers_seen          INTEGER,
    new_unique           INTEGER,
    new_high             INTEGER,
    new_medium           INTEGER,
    new_low              INTEGER,
    new_clusters         INTEGER,
    new_priority_threats INTEGER,
    note                 TEXT
);

CREATE INDEX IF NOT EXISTS idx_rel_score ON relevance(score DESC);
CREATE INDEX IF NOT EXISTS idx_works_year ON works(year);
CREATE INDEX IF NOT EXISTS idx_edges_cited ON citation_edges(cited);
"""

# ---------------------------------------------------------------------------
# Integrity triggers: the two honesty rules, enforced by the database.
# ---------------------------------------------------------------------------

TRIGGERS = """
-- RULE 1: no identifier -> read_status may not exceed DISCOVERED.
CREATE TRIGGER IF NOT EXISTS trg_verified_needs_identifier
BEFORE INSERT ON relevance
FOR EACH ROW
WHEN NEW.read_status <> 'DISCOVERED'
 AND (SELECT COALESCE(doi,'') || COALESCE(arxiv_id,'') || COALESCE(isbn,'')
      FROM works WHERE id = NEW.work_id) = ''
BEGIN
    SELECT RAISE(ABORT,
      'read_status above DISCOVERED requires a DOI, arXiv id or ISBN: fuzzy matches stay CANDIDATES');
END;

CREATE TRIGGER IF NOT EXISTS trg_verified_needs_identifier_upd
BEFORE UPDATE OF read_status ON relevance
FOR EACH ROW
WHEN NEW.read_status <> 'DISCOVERED'
 AND (SELECT COALESCE(doi,'') || COALESCE(arxiv_id,'') || COALESCE(isbn,'')
      FROM works WHERE id = NEW.work_id) = ''
BEGIN
    SELECT RAISE(ABORT,
      'read_status above DISCOVERED requires a DOI, arXiv id or ISBN');
END;

-- RULE 2: strong relations are findings and need a locator plus a real read.
CREATE TRIGGER IF NOT EXISTS trg_strong_relation_needs_evidence
BEFORE INSERT ON claim_work_relation
FOR EACH ROW
WHEN NEW.relation IN ('IDENTICAL','STRICTLY_STRONGER_PRIOR','COUNTEREXAMPLE')
 AND (COALESCE(NEW.equation,'') = '' AND COALESCE(NEW.theorem,'') = '')
BEGIN
    SELECT RAISE(ABORT,
      'IDENTICAL / STRICTLY_STRONGER_PRIOR / COUNTEREXAMPLE require an equation or theorem locator');
END;

CREATE TRIGGER IF NOT EXISTS trg_strong_relation_needs_read
BEFORE INSERT ON claim_work_relation
FOR EACH ROW
WHEN NEW.relation IN ('IDENTICAL','STRICTLY_STRONGER_PRIOR','COUNTEREXAMPLE')
 AND NOT EXISTS (SELECT 1 FROM relevance
                 WHERE work_id = NEW.work_id
                   AND read_status IN ('ABSTRACT_READ','FULLTEXT_ACQUIRED',
                                       'EQUATION_LEVEL_READ','CROSSCHECKED'))
BEGIN
    SELECT RAISE(ABORT,
      'a strong relation requires read_status at least ABSTRACT_READ for that work');
END;
"""


# Columns added after a database may already exist in the wild. SQLite's
# CREATE TABLE IF NOT EXISTS is a no-op on an existing table, so new columns
# have to be added explicitly or an older database fails at index creation.
MIGRATIONS = [("works", "title_key", "TEXT")]


def _migrate(con):
    for table, column, decl in MIGRATIONS:
        cols = {r[1] for r in con.execute(f"PRAGMA table_info({table})")}
        if cols and column not in cols:
            con.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def connect(path=DB_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA.split("CREATE INDEX IF NOT EXISTS idx_works_titlekey")[0])
    _migrate(con)
    con.executescript(SCHEMA)
    con.executescript(TRIGGERS)
    return con


def canonical_id(doi=None, arxiv=None, isbn=None, openalex=None, title=None):
    """Canonical work id. Identifier-first; title only as a last resort.

    A title-derived id is deliberately prefixed ``fuzzy:`` so that it is
    visible everywhere, and RULE 1 keeps such rows at DISCOVERED.
    """
    if doi:
        return "doi:" + doi.strip().lower().replace("https://doi.org/", "")
    if arxiv:
        return "arxiv:" + str(arxiv).strip().lower().replace("arxiv:", "")
    if isbn:
        return "isbn:" + str(isbn).replace("-", "").strip()
    if openalex:
        return "openalex:" + str(openalex).rsplit("/", 1)[-1]
    if title:
        import re
        return "fuzzy:" + re.sub(r"\W+", "", title.lower())[:60]
    raise ValueError("cannot build a canonical id with no identifier and no title")


def title_key(title):
    """Normalized title used ONLY to merge duplicate rows for the same work.

    The arXiv preprint and the journal version of one paper arrive from
    different APIs with different identifiers, and counting them twice would
    inflate every number in the report.  Normalisation is aggressive
    (alphanumerics only, lowercased) because it is applied together with a year
    check and, critically, is never used to ASSERT an identity against an
    external record -- that still requires a DOI/arXiv/ISBN.
    """
    import re
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())[:90]


def resolve_alias(con, wid):
    row = con.execute("SELECT canonical_id FROM work_aliases WHERE alias_id=?",
                      (wid,)).fetchone()
    return row["canonical_id"] if row else wid


def find_duplicate(con, tkey, year, exclude_id):
    """An existing row for the same work, or None.

    Requires an exact normalized-title match and a year within 1 (journal
    publication routinely lags the preprint by a year).  A title shorter than
    25 normalized characters is too generic to merge on.
    """
    if not tkey or len(tkey) < 25:
        return None
    for row in con.execute(
            "SELECT id, year FROM works WHERE title_key=? AND id<>?",
            (tkey, exclude_id)):
        if year is None or row["year"] is None or abs(row["year"] - year) <= 1:
            return row["id"]
    return None


def _rank(wid):
    """Identifier quality: prefer DOI, then arXiv, then ISBN, then OpenAlex."""
    for i, p in enumerate(("doi:", "arxiv:", "isbn:", "openalex:", "fuzzy:")):
        if wid.startswith(p):
            return i
    return 9


def upsert_work(con, **kw):
    """Insert or enrich a work. Never overwrites a non-null field with null.

    Returns ``(canonical_id, is_new)``.  The returned id may differ from the
    one passed in, because the row may have been merged into a better-
    identified duplicate; callers MUST use the returned id for any foreign key.
    """
    wid = resolve_alias(con, kw["id"])
    kw["id"] = wid
    kw.setdefault("title_key", title_key(kw.get("title")))

    dup = find_duplicate(con, kw["title_key"], kw.get("year"), wid)
    if dup is not None:
        # Keep the better-identified row as canonical and fold the other in.
        keep, drop = (wid, dup) if _rank(wid) < _rank(dup) else (dup, wid)
        if keep != drop:
            con.execute("INSERT OR REPLACE INTO work_aliases VALUES (?,?,?)",
                        (drop, keep, f"exact normalized title + year match"))
            if drop == wid:
                kw["id"] = wid = keep
            else:
                _merge_rows(con, drop, keep)
                wid = keep
    cur = con.execute("SELECT * FROM works WHERE id = ?", (wid,))
    existing = cur.fetchone()
    if existing is None:
        cols = [k for k in kw if k in {
            "id", "title", "authors", "year", "venue", "doi", "arxiv_id", "isbn",
            "openalex_id", "source", "document_type", "oa_status", "oa_url",
            "publisher_url", "abstract", "citation_count", "reference_count",
            "discovered_round", "discovered_via", "title_key"}]
        con.execute(
            f"INSERT INTO works ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            [kw[c] for c in cols])
        return wid, True
    updates = {k: v for k, v in kw.items()
               if k != "id" and v not in (None, "") and existing[k] in (None, "")}
    if updates:
        con.execute("UPDATE works SET " + ",".join(f"{k}=?" for k in updates)
                    + " WHERE id=?", list(updates.values()) + [wid])
    return wid, False


def _merge_rows(con, drop, keep):
    """Fold row ``drop`` into ``keep``: enrich fields, move relevance and edges.

    Field enrichment is one-directional -- a null in ``keep`` may be filled
    from ``drop``, but a value present in ``keep`` is never replaced. The best
    relevance score per cluster survives.
    """
    src = con.execute("SELECT * FROM works WHERE id=?", (drop,)).fetchone()
    dst = con.execute("SELECT * FROM works WHERE id=?", (keep,)).fetchone()
    if src is None or dst is None:
        return
    fill = {k: src[k] for k in src.keys()
            if k != "id" and src[k] not in (None, "") and dst[k] in (None, "")}
    if fill:
        con.execute("UPDATE works SET " + ",".join(f"{k}=?" for k in fill)
                    + " WHERE id=?", list(fill.values()) + [keep])

    for rel in con.execute("SELECT * FROM relevance WHERE work_id=?", (drop,)):
        cur = con.execute("SELECT score FROM relevance WHERE work_id=? AND cluster=?",
                          (keep, rel["cluster"])).fetchone()
        if cur is None or rel["score"] > cur["score"]:
            con.execute(
                "INSERT INTO relevance (work_id,cluster,score,reason,priority_threat,"
                "novelty_threat,foundational_value,implementation_value,"
                "reading_priority,equation_level_required,read_status) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(work_id,cluster) DO UPDATE SET score=excluded.score,"
                "reason=excluded.reason,priority_threat=excluded.priority_threat,"
                "novelty_threat=excluded.novelty_threat",
                (keep, rel["cluster"], rel["score"], rel["reason"],
                 rel["priority_threat"], rel["novelty_threat"],
                 rel["foundational_value"], rel["implementation_value"],
                 rel["reading_priority"], rel["equation_level_required"],
                 rel["read_status"]))
    con.execute("DELETE FROM relevance WHERE work_id=?", (drop,))
    for col in ("citing", "cited"):
        con.execute(f"UPDATE OR IGNORE citation_edges SET {col}=? WHERE {col}=?",
                    (keep, drop))
    con.execute("DELETE FROM works WHERE id=?", (drop,))


def dedupe_existing(con, verbose=True):
    """One-shot merge of duplicates already in the table."""
    con.execute("UPDATE works SET title_key=NULL WHERE title_key=''")
    for row in con.execute("SELECT id, title FROM works WHERE title_key IS NULL").fetchall():
        con.execute("UPDATE works SET title_key=? WHERE id=?",
                    (title_key(row["title"]), row["id"]))
    merged = 0
    groups = con.execute(
        "SELECT title_key FROM works WHERE title_key IS NOT NULL "
        "AND length(title_key)>=25 GROUP BY title_key HAVING COUNT(*)>1").fetchall()
    for g in groups:
        ids = [r["id"] for r in con.execute(
            "SELECT id FROM works WHERE title_key=? ORDER BY id", (g["title_key"],))]
        ids.sort(key=_rank)
        keep = ids[0]
        for drop in ids[1:]:
            con.execute("INSERT OR REPLACE INTO work_aliases VALUES (?,?,?)",
                        (drop, keep, "exact normalized title match (batch dedupe)"))
            _merge_rows(con, drop, keep)
            merged += 1
    con.commit()
    if verbose:
        print(f"deduplication: merged {merged} duplicate rows into canonical records")
    return merged


def set_relevance(con, work_id, cluster, score, reason, **kw):
    con.execute("""
        INSERT INTO relevance (work_id, cluster, score, reason, claim_ids,
            priority_threat, novelty_threat, foundational_value,
            implementation_value, reading_priority, equation_level_required,
            read_status, access_note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(work_id, cluster) DO UPDATE SET
            score=excluded.score, reason=excluded.reason,
            priority_threat=excluded.priority_threat,
            novelty_threat=excluded.novelty_threat,
            reading_priority=excluded.reading_priority
    """, (work_id, cluster, score, reason, kw.get("claim_ids"),
          kw.get("priority_threat", "NONE"), kw.get("novelty_threat", 0),
          kw.get("foundational_value", 0), kw.get("implementation_value", 0),
          kw.get("reading_priority", 0), int(kw.get("equation_level_required", 0)),
          kw.get("read_status", "DISCOVERED"), kw.get("access_note")))
