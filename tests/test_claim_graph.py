"""The review inventory must refuse newly introduced, unreviewed claims."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("claim_graph", ROOT / "scripts/build_claim_graph.py")
graph_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph_module)


def reviewed_copy(tmp_path):
    for filename in ["paper/paper.tex", "paper/appendix.tex", "README.md", ".agent/claim_catalog.json"]:
        target = tmp_path / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / filename, target)
    return tmp_path


def test_current_claim_surface_is_reviewed():
    graph = graph_module.build()
    assert not graph["coverage"]["uncovered"]
    assert {"abstract", "discussion"} <= {s for c in graph["claims"] for s in c["surfaces"]}
    assert all(c["status"] != "CERTIFIED" or c["code_location"] for c in graph["claims"])


def test_a_new_theorem_cannot_silently_inherit_review(tmp_path):
    root = reviewed_copy(tmp_path)
    with (root / "paper/appendix.tex").open("a", encoding="utf-8") as output:
        output.write("\n\\begin{theorem}\\label{thm:unreviewed}\nA new physics assertion.\\end{theorem}\n")
    with pytest.raises(ValueError, match="Unreviewed formal"):
        graph_module.build(root)


def test_new_readme_claim_requires_a_graph_entry(tmp_path):
    root = reviewed_copy(tmp_path)
    path = root / "README.md"
    path.write_text(path.read_text("utf-8").replace("## Claim ledger", "## Claim ledger\n\n| C99 | Unreviewed claim | PROVED |"), "utf-8")
    with pytest.raises(ValueError, match="README claims absent"):
        graph_module.build(root)


def test_a_nonexistent_logical_premise_is_refused(tmp_path):
    root = reviewed_copy(tmp_path)
    path = root / ".agent/claim_catalog.json"
    catalog = json.loads(path.read_text("utf-8"))
    catalog["claims"][0]["depends_on"]["lemmas"].append("MISSING-THEOREM")
    path.write_text(json.dumps(catalog), "utf-8")
    with pytest.raises(ValueError, match="unknown logical dependency"):
        graph_module.build(root)


def test_a_paragraph_unit_stops_at_the_next_formal_environment():
    """A definition or the bibliography after a paragraph is not part of its text (R11)."""
    source = ("\\paragraph{Static potential.} Prose here.\n"
              "\\begin{definition}\\label{def:x} A defined object.\\end{definition}\n"
              "\\paragraph{Data.} More prose.\n\\bibliography{references}\n\\end{document}\n")
    units = {u["unit_id"]: u["text"] for u in graph_module.inventory({"paper/paper.tex": source})}
    assert "definition" not in units["paper/paper.tex#paragraph:Static potential."]
    assert "bibliography" not in units["paper/paper.tex#paragraph:Data."]


# Catalog status -> (claims_matrix status, phrases the README status may use).
_VOCABULARY = {
    "PROVED": ("PROVED", ("proved",)),
    "PROVED_CONDITIONALLY": ("PROVED_CONDITIONALLY", ("proved conditionally", "proved in the model")),
    "CLASSICAL": ("CLASSICAL_APPLICATION", ("classical",)),
}
_STRENGTH = ["PROVED_CONDITIONALLY", "PROVED"]      # a bundled claim takes its weakest part


def test_readme_catalog_and_matrix_agree_on_every_claim_status():
    """The audit found C4 and C8 with different statuses in the three places (R11)."""
    import csv
    import re
    catalog = json.loads((ROOT / ".agent/claim_catalog.json").read_text(encoding="utf-8-sig"))["claims"]
    matrix = {r["claim_id"]: r["status"] for r in
              csv.DictReader((ROOT / "data/claims_matrix.csv").open(encoding="utf-8"))}
    ledger = re.search(r"## Claim ledger(.*?)## Status", (ROOT / "README.md").read_text("utf-8"), re.S).group(1)
    readme = {m.group(1): m.group(2).strip().lower()
              for m in re.finditer(r"^\| (C\d+) \| [^|]+\| ([^|]+)\|", ledger, re.M)}
    assert readme
    for cid, text in readme.items():
        statuses = {c["status"] for c in catalog if c.get("readme_claim_id") == cid}
        assert statuses and statuses <= set(_VOCABULARY), (cid, statuses)
        for status in statuses:
            assert any(p in text for p in _VOCABULARY[status][1]), (cid, status, text)
        if statuses <= set(_STRENGTH):
            expected = min(statuses, key=_STRENGTH.index)
        else:
            assert len(statuses) == 1, (cid, statuses)
            expected = next(iter(statuses))
        assert matrix[cid] == _VOCABULARY[expected][0], (cid, matrix[cid], statuses)
