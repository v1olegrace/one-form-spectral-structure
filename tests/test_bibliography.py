"""Bibliography validation.

Enforces the audit's hard rules:

  * no forbidden discovery-source domains appear as scholarly references;
  * every article entry carries author, title, year and at least one persistent
    identifier (DOI or arXiv eprint);
  * no field contains the literal PENDING_VERIFICATION (such fields must be
    OMITTED, not written as a placeholder);
  * every \\cite key used in the LaTeX sources resolves to an entry.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "paper" / "references.bib"

FORBIDDEN = [
    "wikipedia.org", "scribd.com", "researchgate.net", "medium.com",
    "math.stackexchange", "stackexchange.com", "stackoverflow.com",
    "pdfcoffee", "academia.edu", "chegg", "coursehero", "quora.com",
    "blogspot", "wordpress.com", "chatgpt", "openai.com/chat",
]


def bib_text():
    assert BIB.exists(), f"{BIB} missing -- run scripts/build_bibliography.py"
    return BIB.read_text(encoding="utf-8")


def parse_entries(text):
    """Return {key: {field: value}} for every @type{key, ...} entry."""
    out = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        etype, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}(?=,\s*\n|\s*$)", body, re.S):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        fields["__type__"] = etype
        out[key] = fields
    return out


def test_bibliography_exists_and_parses():
    entries = parse_entries(bib_text())
    assert len(entries) >= 20, f"only {len(entries)} entries parsed"


def test_no_forbidden_domains():
    # Strip % comments first: the generated header legitimately NAMES the banned
    # sources when stating that they are excluded.
    text = " ".join(line for line in bib_text().splitlines()
                    if not line.lstrip().startswith("%")).lower()
    hits = [d for d in FORBIDDEN if d in text]
    assert not hits, f"forbidden discovery sources cited as scholarly support: {hits}"


def test_no_pending_placeholders_written_into_entries():
    """PENDING fields must be omitted, never written as a literal placeholder."""
    for key, f in parse_entries(bib_text()).items():
        for name, val in f.items():
            if name in ("note", "__type__"):
                continue          # the note legitimately *mentions* omissions
            assert "PENDING_VERIFICATION" not in val, (
                f"{key}.{name} contains a placeholder instead of being omitted")


def test_articles_have_identifiers_and_core_fields():
    problems = []
    for key, f in parse_entries(bib_text()).items():
        if f["__type__"] != "article":
            continue
        for required in ("author", "title", "year"):
            if required not in f:
                problems.append(f"{key}: missing {required}")
        if "doi" not in f and "eprint" not in f:
            problems.append(f"{key}: no DOI and no arXiv eprint")
    assert not problems, problems


def test_every_entry_records_provenance():
    for key, f in parse_entries(bib_text()).items():
        assert "note" in f and f["note"], f"{key}: no provenance note"


def test_latex_citations_resolve():
    """Every \\cite{...} in paper/*.tex must exist in references.bib."""
    tex = list((ROOT / "paper").glob("*.tex"))
    if not tex:
        pytest.skip("no LaTeX sources yet")
    entries = set(parse_entries(bib_text()))
    used = set()
    for path in tex:
        body = path.read_text(encoding="utf-8")
        for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]+)\}", body):
            used.update(k.strip() for k in m.group(1).split(","))
    missing = sorted(used - entries)
    assert not missing, f"cited but not in references.bib: {missing}"


def test_high_threat_papers_are_cited():
    """The adversarial audit's HIGH-threat precedents must appear in the paper.

    Omitting them would be the failure mode the audit exists to prevent.
    """
    tex = list((ROOT / "paper").glob("*.tex"))
    if not tex:
        pytest.skip("no LaTeX sources yet")
    body = "\n".join(p.read_text(encoding="utf-8") for p in tex)
    for key in ["luscher_wolff_1990", "blossier_et_al_gevp_2009",
                "masjuan_peris_2009", "bachas_1986"]:
        assert key in body, f"HIGH/MEDIUM-threat precedent {key} is not cited"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
