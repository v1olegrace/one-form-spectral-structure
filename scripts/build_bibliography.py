"""Generate paper/references.bib from the verified harvest.

Only fields actually returned by INSPIRE/Crossref/Semantic Scholar are written.
A field left as PENDING_VERIFICATION is OMITTED from the BibTeX entry rather
than guessed, and is listed in the header comment so the omission is visible.

Books and monographs that have no DOI/arXiv record are added from a small
hand-curated table; each carries an explicit ``verified`` note stating what was
and was not checked.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARVEST = ROOT / "data" / "literature_harvest.json"
OUT = ROOT / "paper" / "references.bib"
PENDING = "PENDING_VERIFICATION"

# Monographs: no API record exists, so metadata is hand-entered and marked.
BOOKS = [
    dict(key="widder1941laplace", type="book",
         author="Widder, David Vernon", title="The Laplace Transform",
         publisher="Princeton University Press", year="1941", address="Princeton",
         note="Chapter IV: Bernstein--Widder theorem on completely monotone functions. "
              "Bibliographic details hand-entered; not API-verified."),
    dict(key="akhiezer1965moment", type="book",
         author="Akhiezer, Naum Ilyich", title="The Classical Moment Problem and Some Related Questions in Analysis",
         publisher="Oliver and Boyd", year="1965", address="Edinburgh",
         note="Carleman's criterion for determinacy. Hand-entered; not API-verified."),
    dict(key="chihara1978orthogonal", type="book",
         author="Chihara, Theodore Seio", title="An Introduction to Orthogonal Polynomials",
         publisher="Gordon and Breach", year="1978", address="New York",
         note="True interval of orthogonality; zeros of orthogonal polynomials versus "
              "the support edge. Specific theorem numbers PENDING_VERIFICATION."),
    dict(key="schmudgen2017moment", type="book",
         author="Schm{\\\"u}dgen, Konrad", title="The Moment Problem",
         series="Graduate Texts in Mathematics", volume="277",
         publisher="Springer", year="2017",
         note="Determinacy and support of representing measures. Specific theorem "
              "numbers PENDING_VERIFICATION."),
    dict(key="bakergravesmorris1996pade", type="book",
         author="Baker, George A. and Graves-Morris, Peter",
         title="Pad{\\'e} Approximants", edition="2",
         series="Encyclopedia of Mathematics and its Applications", volume="59",
         publisher="Cambridge University Press", year="1996",
         note="Pade approximants to series of Stieltjes: bounding properties and the "
              "equivalence with orthogonal polynomials and Hankel determinants. "
              "Cited as the classical origin of the Hankel hierarchy."),
    dict(key="dlmf", type="misc",
         author="{NIST}", title="{NIST} Digital Library of Mathematical Functions",
         howpublished="\\url{https://dlmf.nist.gov/2.3.ii}", year="2026",
         note="Section 2.3(ii): Watson's lemma. Release verified 2026-09-11."),
]

TYPE_BY_JOURNAL = {"": "misc"}


def bib_escape(s):
    return s.replace("&", "\\&").replace("_", "\\_")


def entry_from_record(rec):
    key = rec["key"]
    fields = []
    omitted = []

    authors = rec.get("authors", PENDING)
    if authors != PENDING:
        # INSPIRE returns "Last, First"; join with " and " for BibTeX.
        fields.append(("author", " and ".join(a.strip() for a in authors.split(";") if a.strip())))
    else:
        omitted.append("author")

    for bib_name, rec_name in [("title", "title"), ("year", "year"),
                               ("journal", "journal"), ("volume", "volume"),
                               ("pages", "pages"), ("doi", "doi")]:
        v = rec.get(rec_name, PENDING)
        if v and v != PENDING:
            fields.append((bib_name, v))
        else:
            omitted.append(bib_name)

    arxiv = rec.get("arxiv", PENDING)
    if arxiv != PENDING:
        fields.append(("eprint", arxiv))
        fields.append(("archivePrefix", "arXiv"))
    else:
        omitted.append("eprint")

    etype = "article" if rec.get("journal", PENDING) != PENDING else "misc"
    prov = rec.get("provenance", "{}")
    note = f"Metadata verified via {', '.join(sorted(set(json.loads(prov).values())))}."
    if omitted:
        note += f" Omitted (not returned by any API): {', '.join(omitted)}."
    fields.append(("note", note))

    body = ",\n  ".join(f"{k:14s}= {{{bib_escape(str(v))}}}" for k, v in fields)
    return f"@{etype}{{{key},\n  {body}\n}}\n"


def entry_from_book(b):
    etype = b.pop("type")
    key = b.pop("key")
    body = ",\n  ".join(f"{k:14s}= {{{v}}}" for k, v in b.items())
    return f"@{etype}{{{key},\n  {body}\n}}\n"


def main():
    records = json.loads(HARVEST.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)

    n_pending = sum(1 for r in records for v in r.values() if v == PENDING)
    header = (
        "% paper/references.bib -- generated by scripts/build_bibliography.py\n"
        "% DO NOT EDIT BY HAND: regenerate from data/literature_harvest.json\n"
        "%\n"
        "% Academic sources only. Wikipedia, Scribd, ResearchGate upload pages,\n"
        "% Medium, StackExchange, PDFCoffee, blogs and AI-generated summaries are\n"
        "% forbidden as scholarly support and are absent by construction: every\n"
        "% article entry below comes from INSPIRE-HEP, Crossref or Semantic Scholar.\n"
        "%\n"
        f"% {len(records)} API-verified article records; {len(BOOKS)} hand-entered monographs.\n"
        f"% {n_pending} harvested fields were PENDING_VERIFICATION and are OMITTED,\n"
        "% never guessed. Each entry's note field records its provenance.\n\n"
    )

    chunks = [header]
    chunks += [entry_from_record(r) for r in records]
    chunks.append("\n% ---- Monographs and reference works (hand-entered) ----\n\n")
    chunks += [entry_from_book(dict(b)) for b in BOOKS]

    OUT.write_text("\n".join(chunks), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(records)} articles + {len(BOOKS)} books")
    print(f"{n_pending} fields omitted as PENDING_VERIFICATION")


if __name__ == "__main__":
    main()
