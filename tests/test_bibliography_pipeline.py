"""The bibliography pipeline reproduces the committed files, offline.

Before 3 October 2026, `python make.py bib` would have rewritten the harvest:
eight cited records were missing from the seed list and had no cached API
response, INSPIRE years were preprint years, article numbers were lost to
page_start, stored fetch failures blocked retries, and the JSON was rewritten
in another format without its hand fields. These tests pin the repaired
behaviour: every committed value is returned by the API its provenance names
or is a documented hand correction, the outputs are byte-for-byte the
committed ones, and a tampered field is caught.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_bibliography as bb  # noqa: E402
import literature_harvester as lh  # noqa: E402


def _committed(path):
    """The file as committed: the checkout, with CRLF normalised to LF."""
    return (ROOT / path).read_bytes().replace(b"\r\n", b"\n").decode("utf-8")


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setattr(lh, "OFFLINE", True)
    monkeypatch.setattr(lh, "_get", lambda *a, **k: pytest.fail("network used offline"))


def test_every_record_is_reproduced_from_the_cache():
    assert lh.verify(quiet=True) == []


def test_every_cited_record_is_seeded():
    seeded = {s[0] for s in lh.SEEDS}
    assert {r["key"] for r in lh.load_committed()} <= seeded


@pytest.mark.parametrize("field,value", [
    ("year", "2021"),
    ("title", "A different title"),
    ("pages", "999"),
])
def test_a_tampered_field_is_caught(field, value):
    records = copy.deepcopy(lh.load_committed())
    rec = next(r for r in records if r["key"] == "cordova_ohmori_rudelius_2022")
    rec[field] = value
    problems = lh.verify(records, quiet=True)
    assert any(p.startswith("cordova_ohmori_rudelius_2022") and field in p for p in problems)


def test_an_undocumented_hand_value_is_caught():
    """A value no API returns passes only with a correction note."""
    records = copy.deepcopy(lh.load_committed())
    rec = next(r for r in records if r["key"] == "banks_seiberg_2010")
    rec["year"] = "2010"
    rec.pop("correction")
    assert any(p.startswith("banks_seiberg_2010: year") for p in lh.verify(records, quiet=True))


def test_a_correction_note_does_not_cover_a_different_value():
    """The note on Masjuan-Peris documents the journal year 2010; any other
    year must still fail."""
    records = copy.deepcopy(lh.load_committed())
    rec = next(r for r in records if r["key"] == "masjuan_peris_2009")
    assert "correction" in rec
    rec["year"] = "1999"
    assert any(p.startswith("masjuan_peris_2009: year") for p in lh.verify(records, quiet=True))


def test_the_json_and_csv_round_trip_byte_for_byte():
    records = lh.load_committed()
    assert lh.dump_json(records) == _committed("data/literature_harvest.json")
    assert lh.dump_csv(records) == _committed("data/literature_harvest.csv")


def test_references_bib_is_what_the_harvest_produces():
    text, _, _ = bb.render()
    assert text == _committed("paper/references.bib")


def test_inspire_takes_the_journal_year_and_the_article_number():
    """Banks-Seiberg is Phys. Rev. D 83 (2011) 084019; the preprint is 2010."""
    rec = lh.inspire("arxiv", "1011.5120")
    assert rec["year"] == "2011" and rec["pages"] == "084019"
    rec = lh.inspire("arxiv", "2201.08380")      # Rev. Mod. Phys. 95 (2023) 035003
    assert rec["pages"] == "035003"


def test_a_failed_fetch_is_not_stored(tmp_path, monkeypatch):
    monkeypatch.setattr(lh, "CACHE", tmp_path)
    monkeypatch.setattr(lh, "OFFLINE", False)
    monkeypatch.setattr(lh, "COURTESY_DELAY", 0.0)
    payload = lh._cached("inspire_arxiv_0000.00000", lambda: None)
    assert payload["raw"] is None and not list(tmp_path.iterdir())
    payload = lh._cached("inspire_arxiv_0000.00001", lambda: '{"hits": {"hits": []}}')
    assert len(list(tmp_path.iterdir())) == 1


def test_offline_mode_reports_a_missing_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(lh, "CACHE", tmp_path)
    missing = []
    assert lh.inspire("arxiv", "0000.00002", missing) is None
    assert missing == ["inspire_arxiv_0000.00002"]


def test_no_personal_address_in_request_headers():
    assert "@" not in lh.UA and "mailto" not in lh.UA
