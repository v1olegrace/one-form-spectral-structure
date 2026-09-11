"""The literature database must make dishonesty impossible, not merely discouraged.

Two failure modes have already occurred in this project or been identified as
live risks:

  1. A fuzzy title seed silently resolved "Pade Approximants" to Basdevant
     (1968) -- a different paper -- and it entered the bibliography looking
     exactly like a verified record.
  2. A relation such as "this prior work is IDENTICAL to our Theorem C" is an
     opinion until someone points at an equation. Without enforcement, the
     six-state read ladder is decoration.

These tests assert that the schema itself rejects both. Each test also checks
that the constraint can be SATISFIED, so a trivially-broken trigger that
rejects everything would fail too.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scilit import db as sdb  # noqa: E402


@pytest.fixture()
def con(tmp_path):
    c = sdb.connect(tmp_path / "t.db")
    yield c
    c.close()


def _work(con, wid, **kw):
    sdb.upsert_work(con, id=wid, title=kw.pop("title", "T"), source="test", **kw)


# --- RULE 1: no identifier -> DISCOVERED only ------------------------------

def test_unidentified_work_cannot_be_marked_read(con):
    _work(con, "fuzzy:sometitle")
    with pytest.raises(sqlite3.IntegrityError):
        sdb.set_relevance(con, "fuzzy:sometitle", "A", 50, "looks relevant",
                          read_status="EQUATION_LEVEL_READ")


def test_unidentified_work_may_be_discovered(con):
    """The constraint must not reject everything -- DISCOVERED stays legal."""
    _work(con, "fuzzy:sometitle")
    sdb.set_relevance(con, "fuzzy:sometitle", "A", 50, "candidate only")
    row = con.execute("SELECT read_status FROM relevance").fetchone()
    assert row["read_status"] == "DISCOVERED"


def test_identified_work_may_be_marked_read(con):
    _work(con, "doi:10.1000/x", doi="10.1000/x")
    sdb.set_relevance(con, "doi:10.1000/x", "A", 90, "has a DOI",
                      read_status="EQUATION_LEVEL_READ")
    assert con.execute("SELECT read_status FROM relevance").fetchone()[
        "read_status"] == "EQUATION_LEVEL_READ"


def test_promotion_by_update_is_also_blocked(con):
    """Insert-time enforcement alone would leave an obvious bypass."""
    _work(con, "fuzzy:t2")
    sdb.set_relevance(con, "fuzzy:t2", "A", 10, "candidate")
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("UPDATE relevance SET read_status='ABSTRACT_READ' "
                    "WHERE work_id='fuzzy:t2'")


# --- RULE 2: strong relations need evidence -------------------------------

def _claim(con):
    con.execute("INSERT INTO claims (claim_id, claim_text) VALUES ('C1','x')")


def test_identical_without_locator_is_rejected(con):
    _claim(con)
    _work(con, "doi:10.1000/y", doi="10.1000/y")
    sdb.set_relevance(con, "doi:10.1000/y", "A", 90, "r", read_status="ABSTRACT_READ")
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("INSERT INTO claim_work_relation "
                    "(claim_id, work_id, relation, confidence) "
                    "VALUES ('C1','doi:10.1000/y','IDENTICAL',9)")


def test_identical_without_reading_is_rejected(con):
    """A locator typed from an abstract-free guess is still not evidence."""
    _claim(con)
    _work(con, "doi:10.1000/z", doi="10.1000/z")
    sdb.set_relevance(con, "doi:10.1000/z", "A", 90, "r")  # DISCOVERED
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("INSERT INTO claim_work_relation "
                    "(claim_id, work_id, relation, equation) "
                    "VALUES ('C1','doi:10.1000/z','IDENTICAL','eq. (3)')")


def test_identical_with_locator_and_reading_is_accepted(con):
    _claim(con)
    _work(con, "doi:10.1000/w", doi="10.1000/w")
    sdb.set_relevance(con, "doi:10.1000/w", "A", 90, "r",
                      read_status="EQUATION_LEVEL_READ")
    con.execute("INSERT INTO claim_work_relation "
                "(claim_id, work_id, relation, equation) "
                "VALUES ('C1','doi:10.1000/w','IDENTICAL','eq. (3.7)')")
    assert con.execute("SELECT COUNT(*) FROM claim_work_relation").fetchone()[0] == 1


def test_weak_relations_stay_cheap(con):
    """ANALOGOUS is an impression by design and must not require an equation;
    if it did, the harvest would stall on every speculative link."""
    _claim(con)
    _work(con, "doi:10.1000/v", doi="10.1000/v")
    sdb.set_relevance(con, "doi:10.1000/v", "A", 40, "r")
    con.execute("INSERT INTO claim_work_relation (claim_id, work_id, relation) "
                "VALUES ('C1','doi:10.1000/v','ANALOGOUS')")
    assert con.execute("SELECT COUNT(*) FROM claim_work_relation").fetchone()[0] == 1


# --- upsert must never destroy verified metadata --------------------------

def test_upsert_never_overwrites_a_known_field_with_null(con):
    sdb.upsert_work(con, id="doi:10.1/a", title="Real Title", doi="10.1/a",
                    year=1986, source="crossref")
    sdb.upsert_work(con, id="doi:10.1/a", title="Real Title", year=None,
                    venue="Phys. Rev. D", source="openalex")
    row = con.execute("SELECT year, venue FROM works").fetchone()
    assert row["year"] == 1986          # not clobbered
    assert row["venue"] == "Phys. Rev. D"  # enriched


def test_canonical_id_prefers_identifiers_over_titles():
    assert sdb.canonical_id(doi="10.1/A", title="t") == "doi:10.1/a"
    assert sdb.canonical_id(arxiv="2501.00001", title="t") == "arxiv:2501.00001"
    assert sdb.canonical_id(title="Pade Approximants").startswith("fuzzy:")
